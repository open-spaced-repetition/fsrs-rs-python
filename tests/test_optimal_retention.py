import unittest
from collections.abc import Sequence
from typing import Callable, cast

from fsrs_rs_python import (
    DEFAULT_PARAMETERS,
    Card,
    SimulationResult,
    default_simulator_config,
    optimal_retention,
)


def small_config():
    config = default_simulator_config()
    config.deck_size = 20
    config.learn_span = 30
    config.learn_limit = 1
    return config


class OptimalRetentionTest(unittest.TestCase):
    def test_default_target(self) -> None:
        value = optimal_retention(small_config(), DEFAULT_PARAMETERS)
        self.assertGreaterEqual(value, 0.69)
        self.assertLessEqual(value, 0.96)

    def test_custom_target(self) -> None:
        callback_was_called = False

        def target(result: SimulationResult, parameters: Sequence[float]) -> float:
            nonlocal callback_was_called
            callback_was_called = True
            self.assertEqual(len(parameters), len(DEFAULT_PARAMETERS))
            self.assertIsInstance(result.cards, list)
            return sum(result.cost_per_day) / result.memorized_cnt_per_day[-1]

        optimal_retention(small_config(), DEFAULT_PARAMETERS, target=target)
        self.assertTrue(callback_was_called)

    def test_existing_card(self) -> None:
        card = Card()
        card.id = 1
        card.difficulty = 5.0
        card.stability = 5.0
        card.last_date = -5.0
        card.due = 1.0
        card.interval = 5.0
        card.desired_retention = 0.9
        card.parameters = DEFAULT_PARAMETERS

        value = optimal_retention(small_config(), DEFAULT_PARAMETERS, cards=[card])
        self.assertGreaterEqual(value, 0.69)
        self.assertLessEqual(value, 0.96)
        self.assertEqual(card.scheduled_due(), 0.0)
        self.assertGreaterEqual(card.retrievability(), 0.0)
        self.assertLessEqual(card.retrievability(), 1.0)

    def test_target_error_is_propagated(self) -> None:
        def target(_result: SimulationResult, _parameters: Sequence[float]) -> float:
            raise RuntimeError("callback failed")

        with self.assertRaisesRegex(RuntimeError, "callback failed"):
            optimal_retention(small_config(), DEFAULT_PARAMETERS, target=target)

    def test_non_callable_target_is_rejected(self) -> None:
        target = cast(Callable[[SimulationResult, Sequence[float]], float], 42)
        with self.assertRaises(TypeError):
            optimal_retention(small_config(), DEFAULT_PARAMETERS, target=target)


if __name__ == "__main__":
    unittest.main()
