from typing import List, Optional

class FSRS:
    ...
    def __init__(self, parameters: List[float]) -> None: ...
    def next_states(
        self,
        current_memory_state: Optional[MemoryState],
        desired_retention: float,
        days_elapsed: int,
    ) -> NextStates: ...
    def compute_parameters(self, fsrs_items: List[FSRSItem]) -> List[float]: ...
    def memory_state_from_sm2(
        self, ease_factor: float, interval: float, sm2_retention: float
    ) -> MemoryState: ...

class FSRSItem:
    ...
    def __init__(self, reviews: List[FSRSReview]) -> None: ...
    def long_term_review_cnt(self) -> int: ...

class FSRSReview:
    ...
    def __init__(self, rating: int, delta_t: int) -> None: ...

class MemoryState:
    def __init__(self, stability, difficulty) -> None: ...
    ...

class NextStates:
    hard: ItemState
    good: ItemState
    again: ItemState
    easy: ItemState

class ItemState:
    memory: MemoryState
    interval: float

DEFAULT_PARAMETERS: List[float]