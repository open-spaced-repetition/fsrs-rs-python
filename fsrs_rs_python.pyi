from typing import List, Optional, Sequence

class FSRS:
    ...
    def __init__(self, parameters: Sequence[float]) -> None: ...
    def next_states(
        self,
        current_memory_state: Optional[MemoryState],
        desired_retention: float,
        days_elapsed: int,
    ) -> NextStates: ...
    def next_interval(
        self,
        stability: Optional[float],
        desired_retention: float,
        rating: int,
    ) -> float: ...
    def compute_parameters(
        self,
        fsrs_items: Sequence[FSRSItem],
        card_ids: Optional[Sequence[int]] = None,
        enable_short_term: bool = True,
        num_relearning_steps: Optional[int] = None,
        training_config: Optional[TrainingConfig] = None,
    ) -> List[float]: ...
    def benchmark(
        self,
        fsrs_items: Sequence[FSRSItem],
        card_ids: Optional[Sequence[int]] = None,
        enable_short_term: bool = True,
        num_relearning_steps: Optional[int] = None,
        training_config: Optional[TrainingConfig] = None,
    ) -> List[float]: ...
    def memory_state_from_sm2(
        self, ease_factor: float, interval: float, sm2_retention: float
    ) -> MemoryState: ...
    def memory_state(
        self, item: FSRSItem, starting_state: Optional[MemoryState] = None
    ) -> MemoryState: ...
    def memory_state_batch(
        self,
        items: Sequence[FSRSItem],
        starting_states: Optional[Sequence[Optional[MemoryState]]] = None,
    ) -> List[MemoryState]: ...
    def historical_memory_states(
        self, item: FSRSItem, starting_state: Optional[MemoryState] = None
    ) -> List[MemoryState]: ...
    def historical_memory_state_batch(
        self,
        items: Sequence[FSRSItem],
        starting_states: Optional[Sequence[Optional[MemoryState]]] = None,
    ) -> List[List[MemoryState]]: ...
    def evaluate(self, fsrs_items: Sequence[FSRSItem]) -> ModelEvaluation: ...

class TrainingConfig:
    num_epochs: int
    batch_size: int
    seed: int
    learning_rate: float
    max_seq_len: int
    gamma: float
    def __init__(
        self,
        num_epochs: int = 5,
        batch_size: int = 512,
        seed: int = 2023,
        learning_rate: float = 4e-2,
        max_seq_len: int = 256,
        gamma: float = 1.0,
    ) -> None: ...

class ModelEvaluation:
    log_loss: float
    rmse_bins: float

class FSRSItem:
    ...
    reviews: List[FSRSReview]
    def __init__(self, reviews: Sequence[FSRSReview]) -> None: ...
    def long_term_review_cnt(self) -> int: ...

class FSRSReview:
    ...
    def __init__(self, rating: int, delta_t: int) -> None: ...

class MemoryState:
    def __init__(self, stability: float, difficulty: float) -> None: ...
    stability: float
    difficulty: float

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
    correct_cnt_per_day: list[int]
    average_desired_retention: Optional[float]
    introduced_cnt_per_day: list[int]

class SimulatorConfig:
    deck_size: int
    learn_span: int
    max_cost_perday: float
    max_ivl: float
    first_rating_prob: list[float]  # List of 4 floats
    review_rating_prob: list[float]  # List of 3 floats
    learning_step_transitions: list[list[float]]  # 3 rows of 4 floats
    relearning_step_transitions: list[list[float]]  # 3 rows of 4 floats
    state_rating_costs: list[list[float]]  # 3 rows of 4 floats
    learning_step_count: int
    relearning_step_count: int
    learn_limit: int
    review_limit: int
    new_cards_ignore_review_limit: bool
    suspend_after_lapses: Optional[int] = None
    def __init__(
        self,
        deck_size: int,
        learn_span: int,
        max_cost_perday: float,
        max_ivl: float,
        first_rating_prob: Sequence[float],
        review_rating_prob: Sequence[float],
        learn_limit: int,
        review_limit: int,
        new_cards_ignore_review_limit: bool,
        learning_step_transitions: Sequence[Sequence[float]],
        relearning_step_transitions: Sequence[Sequence[float]],
        state_rating_costs: Sequence[Sequence[float]],
        learning_step_count: int,
        relearning_step_count: int,
        suspend_after_lapses: Optional[int] = None,
    ) -> None: ...

def simulate(
    w: Sequence[float],
    desired_retention: float,
    config: Optional[SimulatorConfig] = None,
    seed: Optional[int] = None,
) -> SimulationResult: ...
def default_simulator_config() -> SimulatorConfig: ...
def evaluate_with_time_series_splits(
    fsrs_items: Sequence[FSRSItem],
    card_ids: Optional[Sequence[int]] = None,
    enable_short_term: bool = True,
    num_relearning_steps: Optional[int] = None,
    training_config: Optional[TrainingConfig] = None,
) -> ModelEvaluation: ...
def filter_outlier(
    dataset_for_initialization: Sequence[FSRSItem],
    trainset: Sequence[FSRSItem],
) -> tuple[List[FSRSItem], List[FSRSItem]]: ...
def check_and_fill_parameters(parameters: Sequence[float]) -> List[float]: ...

DEFAULT_PARAMETERS: List[float]
