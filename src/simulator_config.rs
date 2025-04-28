use pyo3::prelude::*;

#[pyclass(module = "fsrs_rs_python")]
#[derive(Default)]
pub struct SimulatorConfig(pub fsrs::SimulatorConfig);

#[pymethods]
impl SimulatorConfig {
    // Constructor for the wrapper struct
    #[new]
    #[pyo3(signature = (deck_size, learn_span, max_cost_perday, max_ivl, first_rating_prob, review_rating_prob, learn_limit, review_limit, new_cards_ignore_review_limit, learning_step_transitions, relearning_step_transitions, state_rating_costs, learning_step_count, relearning_step_count, suspend_after_lapses=None))]
    pub fn new(
        deck_size: usize,
        learn_span: usize,
        max_cost_perday: f32,
        max_ivl: f32,
        first_rating_prob: [f32; 4],
        review_rating_prob: [f32; 3],
        learn_limit: usize,
        review_limit: usize,
        new_cards_ignore_review_limit: bool,
        learning_step_transitions: [[f32; 4]; 3],
        relearning_step_transitions: [[f32; 4]; 3],
        state_rating_costs: [[f32; 4]; 3],
        learning_step_count: usize,
        relearning_step_count: usize,
        suspend_after_lapses: Option<u32>,
    ) -> Self {
        Self(fsrs::SimulatorConfig {
            deck_size,
            learn_span,
            max_cost_perday,
            max_ivl,
            first_rating_prob,
            review_rating_prob,
            learn_limit,
            review_limit,
            new_cards_ignore_review_limit,
            suspend_after_lapses,
            post_scheduling_fn: None,
            review_priority_fn: None,
            learning_step_transitions,
            relearning_step_transitions,
            state_rating_costs,
            learning_step_count,
            relearning_step_count,
        })
    }

    // Getters
    #[getter]
    pub fn deck_size(&self) -> usize {
        self.0.deck_size
    }

    #[getter]
    pub fn learn_span(&self) -> usize {
        self.0.learn_span
    }

    #[getter]
    pub fn max_cost_perday(&self) -> f32 {
        self.0.max_cost_perday
    }

    #[getter]
    pub fn max_ivl(&self) -> f32 {
        self.0.max_ivl
    }

    #[getter]
    pub fn first_rating_prob(&self) -> [f32; 4] {
        self.0.first_rating_prob
    }

    #[getter]
    pub fn review_rating_prob(&self) -> [f32; 3] {
        self.0.review_rating_prob
    }

    #[getter]
    pub fn learn_limit(&self) -> usize {
        self.0.learn_limit
    }

    #[getter]
    pub fn review_limit(&self) -> usize {
        self.0.review_limit
    }

    #[getter]
    pub fn new_cards_ignore_review_limit(&self) -> bool {
        self.0.new_cards_ignore_review_limit
    }

    #[getter]
    pub fn suspend_after_lapses(&self) -> Option<u32> {
        self.0.suspend_after_lapses
    }

    // Setters
    #[setter]
    pub fn set_deck_size(&mut self, value: usize) {
        self.0.deck_size = value;
    }

    #[setter]
    pub fn set_learn_span(&mut self, value: usize) {
        self.0.learn_span = value;
    }

    #[setter]
    pub fn set_max_cost_perday(&mut self, value: f32) {
        self.0.max_cost_perday = value;
    }

    #[setter]
    pub fn set_max_ivl(&mut self, value: f32) {
        self.0.max_ivl = value;
    }

    #[setter]
    pub fn set_first_rating_prob(&mut self, value: [f32; 4]) {
        self.0.first_rating_prob = value;
    }

    #[setter]
    pub fn set_review_rating_prob(&mut self, value: [f32; 3]) {
        self.0.review_rating_prob = value;
    }

    #[setter]
    pub fn set_learn_limit(&mut self, value: usize) {
        self.0.learn_limit = value;
    }

    #[setter]
    pub fn set_review_limit(&mut self, value: usize) {
        self.0.review_limit = value;
    }

    #[setter]
    pub fn set_new_cards_ignore_review_limit(&mut self, value: bool) {
        self.0.new_cards_ignore_review_limit = value;
    }

    #[setter]
    pub fn set_suspend_after_lapses(&mut self, value: Option<u32>) {
        self.0.suspend_after_lapses = value;
    }
}
