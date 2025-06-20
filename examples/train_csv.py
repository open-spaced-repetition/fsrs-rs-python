import csv
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import DefaultDict, Dict, List, Tuple

from fsrs_rs_python import FSRS, FSRSItem, FSRSReview


def main():
    # Read revlog.csv
    p = Path(__file__).parent
    if not (p / "revlog.csv").exists():
        urllib.request.urlretrieve(
            "https://github.com/open-spaced-repetition/fsrs-rs/files/15046782/revlog.csv",
            (p / "revlog.csv"),
        )
    with (p / "revlog.csv").open("r") as file:
        records = list(csv.DictReader(file))

    print(f"{len(records) = }")
    start_time = time.time()

    # Group by card_id
    reviews_by_card = group_reviews_by_card(records)

    # Remove revlog before last learning
    reviews_by_card = {k: remove_revlog_before_last_learning(v) for k, v in reviews_by_card.items()}
    reviews_by_card = {k: v for k, v in reviews_by_card.items() if len(v) > 0}

    # Convert to FSRSItems
    fsrs_items_with_date = [
        item for items in map(convert_to_fsrs_item, reviews_by_card.values()) for item in items
    ]
    fsrs_items_with_date = sorted(fsrs_items_with_date, key=lambda x: x[0])
    fsrs_items = [item[1] for item in fsrs_items_with_date]
    print(f"{len(fsrs_items) = }")

    # Create FSRS instance and optimize
    fsrs = FSRS([])
    optimized_parameters = fsrs.compute_parameters(fsrs_items)
    print("optimized parameters:", optimized_parameters)
    end_time = time.time()
    print(f"Full training time: {end_time - start_time:.2f}s\n")


def remove_revlog_before_last_learning(
    entries: List[Tuple[datetime, int, int]],
) -> List[Tuple[datetime, int, int]]:
    """
    Remove review log entries before the last learning block.

    Args:
        entries: List of (datetime, rating) tuples representing review history

    Returns:
        List of entries starting from the last learning block, or empty list if no learning found
    """

    def is_learning_state(entry: Tuple[datetime, int, int]) -> bool:
        # Rating 0 = New, Rating 1 = Learning
        return entry[2] in [0, 1]

    last_learning_block_start = -1

    # Find the start of the last learning block by scanning backwards
    for i in range(len(entries) - 1, -1, -1):
        if is_learning_state(entries[i]):
            last_learning_block_start = i
        elif last_learning_block_start != -1:
            break

    # Return entries from the last learning block onwards, or empty list if no learning found
    return entries[last_learning_block_start:] if last_learning_block_start != -1 else []


def group_reviews_by_card(
    records: List[Dict],
) -> DefaultDict[str, List[Tuple[datetime, int, int]]]:
    reviews_by_card: DefaultDict[str, List[Tuple[datetime, int, int]]] = defaultdict(list)

    for record in records:
        card_id = record["card_id"]
        # Convert millisecond timestamp to second timestamp
        timestamp = int(record["review_time"]) // 1000
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        # Convert to UTC+8 first
        date = date + timedelta(hours=8)
        # Then subtract 4 hours for next day cutoff
        date = date - timedelta(hours=4)

        reviews_by_card[card_id].append(
            (date, int(record["review_rating"]), int(record["review_state"]))
        )

    # Ensure reviews for each card are sorted by time
    for reviews in reviews_by_card.values():
        reviews.sort(key=lambda x: x[0])

    return reviews_by_card


def convert_to_fsrs_item(
    history: List[Tuple[datetime, int, int]],
) -> List[Tuple[datetime, FSRSItem]]:
    reviews: List[FSRSReview] = []
    last_date = history[0][0]
    items: List[Tuple[datetime, FSRSItem]] = []

    for date, rating, _ in history:
        delta_t = date_diff_in_days(last_date, date)
        reviews.append(FSRSReview(rating, delta_t))
        if delta_t > 0:  # the last review is not the same day
            items.append((date, FSRSItem(reviews)))
        last_date = date

    return [item for item in items if item[1].long_term_review_cnt() > 0]


def date_diff_in_days(a: datetime, b: datetime) -> int:
    a_date = a.replace(hour=0, minute=0, second=0, microsecond=0)
    b_date = b.replace(hour=0, minute=0, second=0, microsecond=0)
    return (b_date - a_date).days


if __name__ == "__main__":
    main()
