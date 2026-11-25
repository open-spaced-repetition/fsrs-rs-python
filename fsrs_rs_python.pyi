from typing import Callable, ClassVar, List, Optional, Sequence

class ModelVersion:
    """The FSRS algorithm version.

    fsrs selects it from the parameter count: 17, 19 or 21 parameters are FSRS-6;
    34 parameters (or none) are FSRS-7.
    """

    FSRS6: ClassVar[ModelVersion]
    FSRS7: ClassVar[ModelVersion]

class FSRS:
    ...
    def __init__(self, parameters: Sequence[float]) -> None: ...
    @property
    def model_version(self) -> ModelVersion: ...
    def next_states(
        self,
        current_memory_state: Optional[MemoryState],
        desired_retention: float,
        days_elapsed: float,
    ) -> NextStates:
        """`days_elapsed` must be finite and non-negative, otherwise `ValueError` is raised.

        Pass fractional days (e.g. `timedelta.total_seconds() / 86400`): FSRS-6 floors them to
        whole days (same-day reviews count as 0), FSRS-7 uses them as-is.
        """
    def current_retrievability(self, state: MemoryState, days_elapsed: float) -> float:
        """`days_elapsed` must be finite and non-negative, otherwise `ValueError` is raised.

        Pass fractional days (e.g. `timedelta.total_seconds() / 86400`): FSRS-6 floors them to
        whole days (same-day reviews count as 0), FSRS-7 uses them as-is.
        """
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
        model_version: Optional[ModelVersion] = None,
        enable_sched_penalties: bool = False,
    ) -> List[float]:
        """Train parameters for `model_version`.

        `model_version=None` uses this instance's version. `training_config=None` uses the
        version's defaults: FSRS-6 trains 5 epochs, learning rate 0.04, max_seq_len 256
        (unchanged from 0.9.x); FSRS-7 trains 9 epochs, learning rate 0.0118, max_seq_len 1024.

        Review `delta_t`s: FSRS-6 floors them to whole days (same-day reviews count as 0),
        FSRS-7 uses them as-is.
        """
    def benchmark(
        self,
        fsrs_items: Sequence[FSRSItem],
        card_ids: Optional[Sequence[int]] = None,
        enable_short_term: bool = True,
        num_relearning_steps: Optional[int] = None,
        training_config: Optional[TrainingConfig] = None,
        model_version: Optional[ModelVersion] = None,
        enable_sched_penalties: bool = False,
    ) -> List[float]:
        """Benchmark training for `model_version`.

        `model_version=None` uses this instance's version. `training_config=None` uses the
        version's defaults: FSRS-6 trains 5 epochs, learning rate 0.04, max_seq_len 256
        (unchanged from 0.9.x); FSRS-7 trains 9 epochs, learning rate 0.0118, max_seq_len 64.

        Review `delta_t`s: FSRS-6 floors them to whole days (same-day reviews count as 0),
        FSRS-7 uses them as-is.
        """
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
    """Training hyperparameters.

    `num_epochs=0` and `learning_rate=0.0` mean the model version's default
    (FSRS-7: 9 epochs and 0.0118; FSRS-6: 5 epochs and 0.04). `TrainingConfig()` uses
    max_seq_len 256 for both versions.
    """

    num_epochs: int
    batch_size: int
    seed: int
    learning_rate: float
    max_seq_len: int
    gamma: float
    def __init__(
        self,
        num_epochs: int = 0,
        batch_size: int = 512,
        seed: int = 2023,
        learning_rate: float = 0.0,
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
    def __init__(self, rating: int, delta_t: float) -> None:
        """`delta_t` is in days and must be finite and non-negative, otherwise `ValueError`.

        Pass fractional days; the review stores them as given. On FSRS-6 paths the binding
        floors them to whole days (same-day reviews count as 0); FSRS-7 uses them as-is.
        """

class MemoryState:
    def __init__(
        self, stability: float, difficulty: float, stability_fast: Optional[float] = None
    ) -> None:
        """`stability_fast=None` uses `stability`, which matches FSRS-6 semantics."""
    stability: float
    difficulty: float
    stability_fast: float

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
    introduced_cnt_per_day: list[int]
    cards: List[Card]

class Card:
    id: int
    difficulty: float
    stability: float
    last_date: float
    due: float
    interval: float
    reps: int
    lapses: int
    desired_retention: float
    parameters: List[float]
    def __init__(self) -> None: ...
    def retention_on(self, date: float) -> float: ...
    def retrievability(self) -> float: ...
    def scheduled_due(self) -> float: ...

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
def optimal_retention(
    config: SimulatorConfig,
    parameters: Sequence[float],
    cards: Optional[Sequence[Card]] = None,
    target: Optional[Callable[[SimulationResult, Sequence[float]], float]] = None,
) -> float: ...
def default_simulator_config() -> SimulatorConfig: ...
def evaluate_with_time_series_splits(
    fsrs_items: Sequence[FSRSItem],
    card_ids: Optional[Sequence[int]] = None,
    enable_short_term: bool = True,
    num_relearning_steps: Optional[int] = None,
    training_config: Optional[TrainingConfig] = None,
    model_version: Optional[ModelVersion] = None,
    enable_sched_penalties: bool = False,
) -> ModelEvaluation:
    """`model_version=None` means FSRS-7. `training_config=None` uses the version's defaults:
    FSRS-6 trains 5 epochs, learning rate 0.04, max_seq_len 256 (unchanged from 0.9.x);
    FSRS-7 trains 9 epochs, learning rate 0.0118, max_seq_len 1024.

    Review `delta_t`s: FSRS-6 floors them to whole days (same-day reviews count as 0),
    FSRS-7 uses them as-is.
    """

def filter_outlier(
    dataset_for_initialization: Sequence[FSRSItem],
    trainset: Sequence[FSRSItem],
) -> tuple[List[FSRSItem], List[FSRSItem]]: ...
def check_and_fill_parameters(parameters: Sequence[float]) -> List[float]: ...

DEFAULT_PARAMETERS: List[float]
"""FSRS-7 default parameters (34 values)."""
FSRS6_DEFAULT_PARAMETERS: List[float]
"""FSRS-6 default parameters (21 values)."""
