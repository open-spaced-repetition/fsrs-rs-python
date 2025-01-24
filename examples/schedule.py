import datetime
from typing import Optional

from fsrs_rs_python import DEFAULT_PARAMETERS, FSRS, MemoryState


class Card:
    def __init__(self):
        self.due = datetime.datetime.now(datetime.timezone.utc)
        self.memory_state: Optional[MemoryState] = None
        self.scheduled_days = 0
        self.last_review: Optional[datetime.date] = None


def schedule_new_card():
    # Create a new card
    card = Card()

    # Set desired retention
    desired_retention = 0.9

    # Create a new FSRS model
    fsrs = FSRS(parameters=DEFAULT_PARAMETERS)

    # Get next states for a new card
    next_states = fsrs.next_states(card.memory_state, desired_retention, 0)

    # Display the intervals for each rating
    print(f"Again interval: {round(next_states.again.interval, 1)} days")
    print(f"Hard interval: {round(next_states.hard.interval, 1)} days")
    print(f"Good interval: {round(next_states.good.interval, 1)} days")
    print(f"Easy interval: {round(next_states.easy.interval, 1)} days")

    # Assume the card was reviewed and the rating was 'good'
    next_state = next_states.good
    interval = int(max(1, round(next_state.interval)))

    # Update the card with the new memory state and interval
    card.memory_state = next_state.memory
    card.scheduled_days = interval
    card.last_review = datetime.datetime.now(datetime.timezone.utc)
    card.due = card.last_review + datetime.timedelta(days=interval)

    print(f"Next review due: {card.due}")
    print(f"Memory state: {card.memory_state}")


def schedule_existing_card():
    # Create an existing card with memory state and last review date
    card = Card()
    card.due = datetime.datetime.now(datetime.timezone.utc)
    card.last_review = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)
    card.memory_state = MemoryState(stability=7.0, difficulty=5.0)
    card.scheduled_days = 7

    # Set desired retention
    desired_retention = 0.9

    # Create a new FSRS model
    fsrs = FSRS(parameters=DEFAULT_PARAMETERS)

    # Calculate the elapsed time since the last review
    elapsed_days = (datetime.datetime.now(datetime.timezone.utc) - card.last_review).days

    # Get next states for an existing card
    next_states = fsrs.next_states(card.memory_state, desired_retention, elapsed_days)

    # Display the intervals for each rating
    print(f"Again interval: {round(next_states.again.interval, 1)} days")
    print(f"Hard interval: {round(next_states.hard.interval, 1)} days")
    print(f"Good interval: {round(next_states.good.interval, 1)} days")
    print(f"Easy interval: {round(next_states.easy.interval, 1)} days")

    # Assume the card was reviewed and the rating was 'again'
    next_state = next_states.again
    interval = max(1, round(next_state.interval))

    # Update the card with the new memory state and interval
    card.memory_state = next_state.memory
    card.scheduled_days = interval
    card.last_review = datetime.datetime.now(datetime.timezone.utc)
    card.due = card.last_review + datetime.timedelta(days=interval)

    print(f"Next review due: {card.due}")
    print(f"Memory state: {card.memory_state}")


if __name__ == "__main__":
    print("Scheduling a new card:")
    schedule_new_card()

    print("\nScheduling an existing card:")
    schedule_existing_card()
