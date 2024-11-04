import csv
import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Tuple, Any
from fsrs_rs_python import FSRS, FSRSItem, FSRSReview


def main():
    # Read revlog.csv
    # Please download from
    # https://github.com/open-spaced-repetition/fsrs-rs/files/15046782/revlog.csv
    with open("./revlog.csv", "r") as file:
        records = list(csv.DictReader(file))

    print(f"revlogs.len() = {len(records)}")
    start_time = time.time()

    # Group by card_id
    reviews_by_card = group_reviews_by_card(records)

    # Convert to FSRSItems
    fsrs_items = [
        item
        for items in map(convert_to_fsrs_item, reviews_by_card.values())
        for item in items
    ]
    print(f"fsrs_items.len() = {len(fsrs_items)}")

    # Create FSRS instance and optimize
    fsrs = FSRS([])
    optimized_parameters = fsrs.compute_parameters(fsrs_items)
    print("optimized parameters:", optimized_parameters)
    end_time = time.time()
    print(f"Full training time: {end_time - start_time:.2f}s\n")


def group_reviews_by_card(records: List[Dict]) -> Dict[str, List[Tuple[datetime, int]]]:
    reviews_by_card: Dict[str, List[Tuple[datetime, int]]] = {}

    for record in records:
        card_id = record["card_id"]
        if card_id not in reviews_by_card:
            reviews_by_card[card_id] = []

        # Convert millisecond timestamp to second timestamp
        timestamp = int(record["review_time"]) // 1000
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        # Convert to UTC+8 first
        date = date + timedelta(hours=8)
        # Then subtract 4 hours for next day cutoff
        date = date - timedelta(hours=4)

        reviews_by_card[card_id].append((date, int(record["review_rating"])))

    # Ensure reviews for each card are sorted by time
    for reviews in reviews_by_card.values():
        reviews.sort(key=lambda x: x[0])

    return reviews_by_card


def convert_to_fsrs_item(history: List[Tuple[datetime, int]]) -> List[FSRSItem]:
    reviews: List[FSRSReview] = []
    last_date = history[0][0]
    items: List[FSRSItem] = []

    for date, rating in history:
        delta_t = date_diff_in_days(last_date, date)
        reviews.append(FSRSReview(rating, delta_t))
        if delta_t > 0:  # the last review is not the same day
            items.append(FSRSItem(reviews[:]))
        last_date = date

    return [item for item in items if item.long_term_review_cnt() > 0]


def date_diff_in_days(a: datetime, b: datetime) -> int:
    a_date = a.replace(hour=0, minute=0, second=0, microsecond=0)
    b_date = b.replace(hour=0, minute=0, second=0, microsecond=0)
    return (b_date - a_date).days


if __name__ == "__main__":
    main()
