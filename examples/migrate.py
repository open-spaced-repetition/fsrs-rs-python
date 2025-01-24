from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS, FSRSItem, FSRSReview


def migrate_with_full_history():
    """
    Migrates a card's memory state using full review history.
    """
    # Create a new FSRS model
    fsrs = FSRS(parameters=DEFAULT_PARAMETERS)

    # Simulate a full review history for a card
    reviews = [
        FSRSReview(rating=3, delta_t=0),
        FSRSReview(rating=3, delta_t=1),
        FSRSReview(rating=4, delta_t=3),
        FSRSReview(rating=3, delta_t=7),
    ]
    item = FSRSItem(reviews=reviews)

    # Calculate the current memory state
    memory_state = fsrs.memory_state(item, None)
    print("Migrated memory state:", memory_state)


def migrate_with_partial_history():
    """
    Migrates a card's memory state using partial review history and initial state.
    """
    # Create a new FSRS model
    fsrs = FSRS(parameters=DEFAULT_PARAMETERS)

    # Set the true retention of the original algorithm
    sm2_retention = 0.9

    # Simulate the earliest card state from the first review log of Anki's card
    # - ease_factor: the ratio of the interval to the previous interval
    # - interval: the interval of the first review
    ease_factor = 2.0
    interval = 5.0

    # Calculate the earliest memory state
    initial_state = fsrs.memory_state_from_sm2(ease_factor, interval, sm2_retention)

    # Simulate partial review history
    reviews = [
        FSRSReview(rating=3, delta_t=5),
        FSRSReview(rating=4, delta_t=10),
        FSRSReview(rating=3, delta_t=20),
    ]
    item = FSRSItem(reviews=reviews)

    # Calculate the current memory state, passing the initial state
    memory_state = fsrs.memory_state(item, initial_state)
    print("Migrated memory state:", memory_state)


def migrate_with_latest_state():
    """
    Migrates a card's memory state using only the latest state.
    """
    # Create a new FSRS model
    fsrs = FSRS(parameters=DEFAULT_PARAMETERS)

    # Set the true retention of the original algorithm
    sm2_retention = 0.9

    # Simulate the latest card state from Anki's card
    # - ease_factor: the ratio of the interval to the previous interval
    # - interval: the interval of the last review
    ease_factor = 2.5
    interval = 10.0

    # Calculate the memory state
    memory_state = fsrs.memory_state_from_sm2(ease_factor, interval, sm2_retention)
    print("Migrated memory state:", memory_state)


if __name__ == "__main__":
    print("Migrating with full history:")
    migrate_with_full_history()
    print("\nMigrating with partial history:")
    migrate_with_partial_history()
    print("\nMigrating with latest state only:")
    migrate_with_latest_state()
