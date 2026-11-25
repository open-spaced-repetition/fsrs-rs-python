import math
import unittest
from typing import List, Optional, Sequence, Tuple

from fsrs_rs_python import (
    DEFAULT_PARAMETERS,
    FSRS,
    FSRS6_DEFAULT_PARAMETERS,
    Card,
    FSRSItem,
    FSRSReview,
    MemoryState,
    ModelVersion,
    NextStates,
    TrainingConfig,
    check_and_fill_parameters,
    default_simulator_config,
    evaluate_with_time_series_splits,
    optimal_retention,
    simulate,
)


def small_config():
    config = default_simulator_config()
    config.deck_size = 20
    config.learn_span = 30
    config.learn_limit = 1
    return config


def synthetic_items(fraction: float = 0.0) -> List[FSRSItem]:
    """Deterministic review histories, expanded into one item per long-term review.

    `fraction` is added to every non-zero `delta_t`, so flooring gives the default dataset.
    """
    items: List[FSRSItem] = []
    for card in range(120):
        delta_ts = [0, 1 + card % 3, 3 + card % 5, 7 + card % 7, 15 + card % 11]
        reviews: List[FSRSReview] = []
        for n, delta_t in enumerate(delta_ts):
            if n == 0:
                rating = card % 4 + 1
            elif (card + n) % 7 == 0:
                rating = 1
            else:
                rating = 3 + (card + n) % 2
            reviews.append(FSRSReview(rating, delta_t + fraction if delta_t > 0 else delta_t))
            if delta_t > 0:
                items.append(FSRSItem(list(reviews)))
    return items


def all_states(next_states: NextStates) -> List[MemoryState]:
    return [
        next_states.again.memory,
        next_states.hard.memory,
        next_states.good.memory,
        next_states.easy.memory,
    ]


def item_with_delta_ts(delta_ts: Sequence[float]) -> FSRSItem:
    return FSRSItem([FSRSReview(3, delta_t) for delta_t in delta_ts])


def state_values(state: MemoryState) -> Tuple[float, float, float]:
    return (state.stability, state.difficulty, state.stability_fast)


def next_state_values(next_states: NextStates) -> List[Tuple[float, ...]]:
    items = (next_states.again, next_states.hard, next_states.good, next_states.easy)
    return [(*state_values(item.memory), item.interval) for item in items]


CHEAP_TRAINING = TrainingConfig(num_epochs=1)
# The FSRS-6 defaults of fsrs-rs-python 0.9.x (fsrs 6 `TrainingConfig::default()`).
LEGACY_FSRS6_TRAINING = TrainingConfig(num_epochs=5, learning_rate=0.04, max_seq_len=256)


class ModelVersionTest(unittest.TestCase):
    def test_version_follows_parameter_count(self) -> None:
        self.assertEqual(len(DEFAULT_PARAMETERS), 34)
        self.assertEqual(len(FSRS6_DEFAULT_PARAMETERS), 21)
        self.assertEqual(FSRS(DEFAULT_PARAMETERS).model_version, ModelVersion.FSRS7)
        self.assertEqual(FSRS(FSRS6_DEFAULT_PARAMETERS).model_version, ModelVersion.FSRS6)
        self.assertEqual(FSRS([]).model_version, ModelVersion.FSRS7)
        self.assertEqual(FSRS(FSRS6_DEFAULT_PARAMETERS[:17]).model_version, ModelVersion.FSRS6)
        self.assertNotEqual(ModelVersion.FSRS6, ModelVersion.FSRS7)
        self.assertEqual(len(check_and_fill_parameters([])), 34)
        self.assertEqual(len(check_and_fill_parameters(FSRS6_DEFAULT_PARAMETERS[:19])), 21)

    def test_next_states_fsrs6_keeps_single_stability(self) -> None:
        fsrs = FSRS(FSRS6_DEFAULT_PARAMETERS)
        first = fsrs.next_states(None, 0.9, 0).good.memory
        for days_elapsed in (3, 2.5):
            for state in all_states(fsrs.next_states(first, 0.9, days_elapsed)):
                self.assertTrue(math.isfinite(state.stability))
                self.assertEqual(state.stability_fast, state.stability)

    def test_next_states_fsrs7_tracks_fast_stability(self) -> None:
        fsrs = FSRS(DEFAULT_PARAMETERS)
        first = fsrs.next_states(None, 0.9, 0)
        self.assertTrue(any(s.stability_fast != s.stability for s in all_states(first)))
        whole = fsrs.next_states(first.good.memory, 0.9, 2)
        fractional = fsrs.next_states(first.good.memory, 0.9, 2.5)
        for state in all_states(whole) + all_states(fractional):
            self.assertTrue(math.isfinite(state.stability))
            self.assertTrue(math.isfinite(state.stability_fast))
        self.assertNotEqual(whole.good.memory.stability, fractional.good.memory.stability)

    def test_memory_state_stability_fast_defaults_to_stability(self) -> None:
        self.assertEqual(MemoryState(5.0, 3.0).stability_fast, 5.0)
        self.assertEqual(MemoryState(5.0, 3.0, None).stability_fast, 5.0)
        self.assertEqual(MemoryState(5.0, 3.0, 4.0).stability_fast, 4.0)

    def test_current_retrievability(self) -> None:
        state = MemoryState(10.0, 5.0, 8.0)
        for parameters in (FSRS6_DEFAULT_PARAMETERS, DEFAULT_PARAMETERS):
            fsrs = FSRS(parameters)
            previous = 1.0
            for days_elapsed in (0, 0.5, 3, 10.25, 100):
                value = fsrs.current_retrievability(state, days_elapsed)
                self.assertGreater(value, 0.0)
                self.assertLessEqual(value, 1.0)
                self.assertLessEqual(value, previous)
                previous = value

        # FSRS-6 still matches its closed-form power forgetting curve.
        decay = FSRS6_DEFAULT_PARAMETERS[20]
        factor = 0.9 ** (1 / -decay) - 1
        expected = (1 + factor * 3 / 10.0) ** -decay
        actual = FSRS(FSRS6_DEFAULT_PARAMETERS).current_retrievability(state, 3)
        self.assertAlmostEqual(actual, expected, places=5)

    def test_fractional_review_delta_t(self) -> None:
        fractional = FSRSItem([FSRSReview(3, 0), FSRSReview(3, 0.5), FSRSReview(3, 2.5)])
        whole = FSRSItem([FSRSReview(3, 0), FSRSReview(3, 0), FSRSReview(3, 2)])
        self.assertEqual(fractional.long_term_review_cnt(), 1)
        for parameters in (FSRS6_DEFAULT_PARAMETERS, DEFAULT_PARAMETERS):
            state = FSRS(parameters).memory_state(fractional)
            self.assertTrue(math.isfinite(state.stability))
            self.assertGreater(state.stability, 0.0)
        fsrs7 = FSRS(DEFAULT_PARAMETERS)
        self.assertNotEqual(
            fsrs7.memory_state(fractional).stability, fsrs7.memory_state(whole).stability
        )

    def test_training_config_defaults_mean_version_default(self) -> None:
        config = TrainingConfig()
        self.assertEqual(config.num_epochs, 0)
        self.assertEqual(config.learning_rate, 0.0)
        with self.assertRaises(ValueError):
            TrainingConfig(batch_size=0)
        with self.assertRaises(ValueError):
            TrainingConfig(learning_rate=math.inf)

    def test_compute_parameters_model_version(self) -> None:
        items = synthetic_items()
        fsrs6 = FSRS(FSRS6_DEFAULT_PARAMETERS)
        fsrs7 = FSRS(DEFAULT_PARAMETERS)
        cases = [
            (fsrs7, ModelVersion.FSRS6, 21),
            (fsrs6, ModelVersion.FSRS7, 34),
            (fsrs6, None, 21),
            (fsrs7, None, 34),
        ]
        for fsrs, model_version, expected_len in cases:
            with self.subTest(instance=fsrs.model_version, model_version=model_version):
                parameters = fsrs.compute_parameters(
                    items, training_config=CHEAP_TRAINING, model_version=model_version
                )
                self.assertEqual(len(parameters), expected_len)
                self.assertTrue(all(math.isfinite(value) for value in parameters))
                self.assertEqual(len(check_and_fill_parameters(parameters)), expected_len)

    def test_fsrs6_default_training_config_matches_0_9(self) -> None:
        items = synthetic_items()
        fsrs6 = FSRS(FSRS6_DEFAULT_PARAMETERS)
        legacy = fsrs6.compute_parameters(items, training_config=LEGACY_FSRS6_TRAINING)
        self.assertEqual(fsrs6.compute_parameters(items), legacy)
        self.assertEqual(
            FSRS(DEFAULT_PARAMETERS).compute_parameters(items, model_version=ModelVersion.FSRS6),
            legacy,
        )
        fsrs7_hyperparameters = TrainingConfig(num_epochs=9, learning_rate=0.0118, max_seq_len=1024)
        self.assertNotEqual(
            fsrs6.compute_parameters(items, training_config=fsrs7_hyperparameters), legacy
        )

        def log_loss(training_config: Optional[TrainingConfig]) -> float:
            return evaluate_with_time_series_splits(
                items, training_config=training_config, model_version=ModelVersion.FSRS6
            ).log_loss

        self.assertEqual(log_loss(None), log_loss(LEGACY_FSRS6_TRAINING))

    def test_fsrs6_floors_elapsed_days(self) -> None:
        fsrs = FSRS(FSRS6_DEFAULT_PARAMETERS)
        state = MemoryState(10.0, 5.0)

        def next_states(days: float) -> List[Tuple[float, ...]]:
            return next_state_values(fsrs.next_states(state, 0.9, days))

        self.assertEqual(next_states(7.75), next_states(7))
        self.assertNotEqual(next_states(7.75), next_states(8))
        self.assertEqual(next_states(0.6), next_states(0))
        self.assertEqual(
            fsrs.current_retrievability(state, 7.75), fsrs.current_retrievability(state, 7)
        )
        self.assertNotEqual(
            fsrs.current_retrievability(state, 7.75), fsrs.current_retrievability(state, 8)
        )

    def test_fsrs6_floors_review_delta_t(self) -> None:
        fsrs = FSRS(FSRS6_DEFAULT_PARAMETERS)
        fractional = item_with_delta_ts([0, 0.6, 7.75])
        floored = item_with_delta_ts([0, 0, 7])
        self.assertEqual(
            state_values(fsrs.memory_state(fractional)), state_values(fsrs.memory_state(floored))
        )
        self.assertEqual(
            [state_values(s) for s in fsrs.historical_memory_states(fractional)],
            [state_values(s) for s in fsrs.historical_memory_states(floored)],
        )
        self.assertEqual(
            [state_values(s) for s in fsrs.memory_state_batch([fractional, floored])],
            [state_values(fsrs.memory_state(floored))] * 2,
        )
        batch = fsrs.historical_memory_state_batch([fractional, floored])
        self.assertEqual([state_values(s) for s in batch[0]], [state_values(s) for s in batch[1]])

    def test_fsrs6_training_floors_review_delta_t(self) -> None:
        fractional = synthetic_items(fraction=0.75)
        floored = synthetic_items()
        fsrs6 = FSRS(FSRS6_DEFAULT_PARAMETERS)
        fsrs7 = FSRS(DEFAULT_PARAMETERS)
        expected = fsrs6.compute_parameters(floored, training_config=CHEAP_TRAINING)
        self.assertEqual(
            fsrs6.compute_parameters(fractional, training_config=CHEAP_TRAINING), expected
        )
        self.assertEqual(
            fsrs7.compute_parameters(
                fractional, training_config=CHEAP_TRAINING, model_version=ModelVersion.FSRS6
            ),
            expected,
        )
        self.assertEqual(
            fsrs7.benchmark(
                fractional, training_config=CHEAP_TRAINING, model_version=ModelVersion.FSRS6
            ),
            fsrs6.benchmark(floored, training_config=CHEAP_TRAINING),
        )
        self.assertEqual(fsrs6.evaluate(fractional).log_loss, fsrs6.evaluate(floored).log_loss)

        def log_loss(items: List[FSRSItem]) -> float:
            return evaluate_with_time_series_splits(
                items, training_config=CHEAP_TRAINING, model_version=ModelVersion.FSRS6
            ).log_loss

        self.assertEqual(log_loss(fractional), log_loss(floored))

    def test_fsrs7_keeps_fractional_days(self) -> None:
        fsrs = FSRS(DEFAULT_PARAMETERS)
        state = MemoryState(10.0, 5.0, 8.0)
        self.assertNotEqual(
            next_state_values(fsrs.next_states(state, 0.9, 7.75)),
            next_state_values(fsrs.next_states(state, 0.9, 7)),
        )
        self.assertNotEqual(
            fsrs.current_retrievability(state, 7.75), fsrs.current_retrievability(state, 7)
        )
        self.assertNotEqual(
            state_values(fsrs.memory_state(item_with_delta_ts([0, 0.6, 7.75]))),
            state_values(fsrs.memory_state(item_with_delta_ts([0, 0, 7]))),
        )

    def test_invalid_elapsed_days_are_rejected(self) -> None:
        state = MemoryState(10.0, 5.0)
        for days in (-1.0, math.nan, math.inf):
            with self.subTest(days=days):
                with self.assertRaises(ValueError):
                    FSRSReview(3, days)
                for parameters in (FSRS6_DEFAULT_PARAMETERS, DEFAULT_PARAMETERS):
                    fsrs = FSRS(parameters)
                    with self.assertRaises(ValueError):
                        fsrs.next_states(state, 0.9, days)
                    with self.assertRaises(ValueError):
                        fsrs.current_retrievability(state, days)

    def test_evaluate_with_time_series_splits_model_version(self) -> None:
        evaluation = evaluate_with_time_series_splits(
            synthetic_items(), training_config=CHEAP_TRAINING, model_version=ModelVersion.FSRS6
        )
        self.assertTrue(math.isfinite(evaluation.log_loss))
        self.assertTrue(math.isfinite(evaluation.rmse_bins))

    def test_simulate_and_optimal_retention(self) -> None:
        for parameters in (FSRS6_DEFAULT_PARAMETERS, DEFAULT_PARAMETERS):
            with self.subTest(parameter_count=len(parameters)):
                config = small_config()
                result = simulate(parameters, 0.9, config, seed=42)
                self.assertEqual(len(result.memorized_cnt_per_day), config.learn_span)
                self.assertGreater(result.memorized_cnt_per_day[-1], 0.0)
                value = optimal_retention(config, parameters)
                self.assertGreaterEqual(value, 0.69)
                self.assertLessEqual(value, 0.96)

    def test_card_reps(self) -> None:
        card = Card()
        self.assertEqual(card.reps, 0)
        card.reps = 3
        self.assertEqual(card.reps, 3)


if __name__ == "__main__":
    unittest.main()
