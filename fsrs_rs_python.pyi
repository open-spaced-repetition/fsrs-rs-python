from dataclasses import dataclass
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
    def benchmark(self, fsrs_items: List[FSRSItem]) -> List[float]: ...
    def memory_state_from_sm2(
        self, ease_factor: float, interval: float, sm2_retention: float
    ) -> MemoryState: ...
    def memory_state(
        self, item: FSRSItem, starting_state: Optional[MemoryState] = None
    ) -> MemoryState: ...

class FSRSItem:
    ...
    def __init__(self, reviews: List[FSRSReview]) -> None: ...
    def long_term_review_cnt(self) -> int: ...

class FSRSReview:
    ...
    def __init__(self, rating: int, delta_t: int) -> None: ...

class MemoryState:
    def __init__(self, stability: float, difficulty: float) -> None: ...
    ...

class NextStates:
    hard: ItemState
    good: ItemState
    again: ItemState
    easy: ItemState

class ItemState:
    memory: MemoryState
    interval: float

class SimulationResult:
    memorized_cnt_per_day: list[float]
    review_cnt_per_day: list[int]
    learn_cnt_per_day: list[int]
    cost_per_day: list[float]

@dataclass
class SimulatorConfig:
    deck_size: int
    learn_span: int
    max_cost_perday: float
    max_ivl: float
    learn_costs: list[float]  # List of 4 floats
    review_costs: list[float]  # List of 4 floats
    first_rating_prob: list[float]  # List of 4 floats
    review_rating_prob: list[float]  # List of 3 floats
    first_rating_offsets: list[float]  # List of 4 floats
    first_session_lens: list[float]  # List of 4 floats
    forget_rating_offset: float
    forget_session_len: float
    loss_aversion: float
    learn_limit: int
    review_limit: int
    new_cards_ignore_review_limit: bool
    suspend_after_lapses: Optional[int] = None

def simulate(
    w: list[float],  # List of floats
    desired_retention: float,
    config: Optional[SimulatorConfig] = None,
    seed: Optional[int] = None,
) -> SimulationResult: ...
def default_simulator_config() -> SimulatorConfig: ...

DEFAULT_PARAMETERS: List[float]
