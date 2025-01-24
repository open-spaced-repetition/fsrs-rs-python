from datetime import date
from itertools import chain, cycle, islice
from typing import List, Tuple

from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS, FSRSItem, FSRSReview


def main():
    # Create review histories for cards
    review_histories_of_cards = create_review_histories_for_cards()

    # Convert review histories to FSRSItems
    fsrs_items = list(
        chain.from_iterable(convert_to_fsrs_item(x) for x in review_histories_of_cards)
    )
    print(f"{len(fsrs_items) = }")

    # Create an FSRS instance with default parameters
    fsrs = FSRS(parameters=DEFAULT_PARAMETERS)
    print(f"{DEFAULT_PARAMETERS = }")

    # Optimize the FSRS model using the created items
    optimized_parameters = fsrs.compute_parameters(fsrs_items)
    print(f"{optimized_parameters = }")


def create_review_histories_for_cards():
    # This vector represents a collection of review histories for multiple cards.
    # Each inner vector represents the review history of a single card.
    # The structure is as follows:
    # - Outer vector: Contains review histories for multiple cards
    # - Inner vector: Represents the review history of a single card
    #   - Each element is a tuple: (Date, Rating)
    #     - Date: The date of the review (date)
    #     - Rating: The rating given during the review (int)
    #
    # The ratings typically follow this scale:
    # 1: Again, 2: Hard, 3: Good, 4: Easy
    #
    # This sample data includes various review patterns, such as:
    # - Cards with different numbers of reviews
    # - Various intervals between reviews
    # - Different rating patterns (e.g., consistently high, mixed, or improving over time)
    #
    # The data is then cycled and repeated to create a larger dataset of 100 cards.
    review_histories = [
        [
            (date(2023, 1, 1), 3),
            (date(2023, 1, 2), 4),
            (date(2023, 1, 5), 3),
            (date(2023, 1, 15), 4),
            (date(2023, 2, 1), 3),
            (date(2023, 2, 20), 4),
        ],
        [
            (date(2023, 1, 1), 2),
            (date(2023, 1, 2), 3),
            (date(2023, 1, 4), 4),
            (date(2023, 1, 12), 3),
            (date(2023, 1, 28), 4),
            (date(2023, 2, 15), 3),
            (date(2023, 3, 5), 4),
        ],
        [
            (date(2023, 1, 1), 4),
            (date(2023, 1, 8), 4),
            (date(2023, 1, 24), 3),
            (date(2023, 2, 10), 4),
            (date(2023, 3, 1), 3),
        ],
        [
            (date(2023, 1, 1), 1),
            (date(2023, 1, 2), 1),
            (date(2023, 1, 3), 3),
            (date(2023, 1, 6), 4),
            (date(2023, 1, 16), 4),
            (date(2023, 2, 1), 3),
            (date(2023, 2, 20), 4),
        ],
        [
            (date(2023, 1, 1), 3),
            (date(2023, 1, 3), 3),
            (date(2023, 1, 8), 2),
            (date(2023, 1, 10), 4),
            (date(2023, 1, 22), 3),
            (date(2023, 2, 5), 4),
            (date(2023, 2, 25), 3),
        ],
        [
            (date(2023, 1, 1), 4),
            (date(2023, 1, 9), 3),
            (date(2023, 1, 19), 4),
            (date(2023, 2, 5), 3),
            (date(2023, 2, 25), 4),
        ],
        [
            (date(2023, 1, 1), 2),
            (date(2023, 1, 2), 3),
            (date(2023, 1, 5), 4),
            (date(2023, 1, 15), 3),
            (date(2023, 1, 30), 4),
            (date(2023, 2, 15), 3),
            (date(2023, 3, 5), 4),
        ],
        [
            (date(2023, 1, 1), 3),
            (date(2023, 1, 4), 4),
            (date(2023, 1, 14), 4),
            (date(2023, 2, 1), 3),
            (date(2023, 2, 20), 4),
        ],
        [
            (date(2023, 1, 1), 1),
            (date(2023, 1, 1), 3),
            (date(2023, 1, 2), 1),
            (date(2023, 1, 2), 3),
            (date(2023, 1, 3), 3),
            (date(2023, 1, 7), 3),
            (date(2023, 1, 15), 4),
            (date(2023, 1, 31), 3),
            (date(2023, 2, 15), 4),
            (date(2023, 3, 5), 3),
        ],
        [
            (date(2023, 1, 1), 4),
            (date(2023, 1, 10), 3),
            (date(2023, 1, 20), 4),
            (date(2023, 2, 5), 4),
            (date(2023, 2, 25), 3),
            (date(2023, 3, 15), 4),
        ],
        [
            (date(2023, 1, 1), 1),
            (date(2023, 1, 2), 2),
            (date(2023, 1, 3), 3),
            (date(2023, 1, 4), 4),
            (date(2023, 1, 10), 3),
            (date(2023, 1, 20), 4),
            (date(2023, 2, 5), 3),
            (date(2023, 2, 25), 4),
        ],
        [
            (date(2023, 1, 1), 3),
            (date(2023, 1, 5), 4),
            (date(2023, 1, 15), 3),
            (date(2023, 1, 30), 4),
            (date(2023, 2, 15), 3),
            (date(2023, 3, 5), 4),
        ],
        [
            (date(2023, 1, 1), 2),
            (date(2023, 1, 3), 3),
            (date(2023, 1, 7), 4),
            (date(2023, 1, 17), 3),
            (date(2023, 2, 1), 4),
            (date(2023, 2, 20), 3),
            (date(2023, 3, 10), 4),
        ],
        [
            (date(2023, 1, 1), 4),
            (date(2023, 1, 12), 3),
            (date(2023, 1, 25), 4),
            (date(2023, 2, 10), 3),
            (date(2023, 3, 1), 4),
        ],
    ]
    return list(islice(cycle(review_histories), 100))


def convert_to_fsrs_item(history: List[Tuple[date, int]]) -> List[FSRSItem]:
    reviews: List[FSRSReview] = []
    last_date = history[0][0]
    items: List[FSRSItem] = []
    for date_, rating in history:
        delta_t = (date_ - last_date).days
        reviews.append(FSRSReview(rating=rating, delta_t=delta_t))
        items.append(FSRSItem(reviews=reviews.copy()))
        last_date = date_

    return [x for x in items if x.long_term_review_cnt() > 0]


if __name__ == "__main__":
    main()
