use pyo3::prelude::*;

#[pyclass(module = "fsrs_rs_python")]
#[derive(Default)]
pub struct SimulatorConfig(pub fsrs::SimulatorConfig);

#[pymethods]
impl SimulatorConfig {
    // Constructor for the wrapper struct
    #[new]
    #[pyo3(signature = (deck_size, learn_span, max_cost_perday, max_ivl, learn_costs, review_costs, first_rating_prob, review_rating_prob, first_rating_offsets, first_session_lens, forget_rating_offset, forget_session_len, loss_aversion, learn_limit, review_limit, new_cards_ignore_review_limit, suspend_after_lapses=None))]
    pub fn new(
        deck_size: usize,
        learn_span: usize,
        max_cost_perday: f32,
        max_ivl: f32,
        learn_costs: [f32; 4],
        review_costs: [f32; 4],
        first_rating_prob: [f32; 4],
        review_rating_prob: [f32; 3],
        first_rating_offsets: [f32; 4],
        first_session_lens: [f32; 4],
        forget_rating_offset: f32,
        forget_session_len: f32,
        loss_aversion: f32,
        learn_limit: usize,
        review_limit: usize,
        new_cards_ignore_review_limit: bool,
        suspend_after_lapses: Option<u32>,
    ) -> Self {
        Self(fsrs::SimulatorConfig {
            deck_size,
            learn_span,
            max_cost_perday,
            max_ivl,
            learn_costs,
            review_costs,
            first_rating_prob,
            review_rating_prob,
            first_rating_offsets,
            first_session_lens,
            forget_rating_offset,
            forget_session_len,
            loss_aversion,
            learn_limit,
            review_limit,
            new_cards_ignore_review_limit,
            suspend_after_lapses,
            post_scheduling_fn: None,
            review_priority_fn: None,
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
    pub fn learn_costs(&self) -> [f32; 4] {
        self.0.learn_costs
    }

    #[getter]
    pub fn review_costs(&self) -> [f32; 4] {
        self.0.review_costs
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
    pub fn first_rating_offsets(&self) -> [f32; 4] {
        self.0.first_rating_offsets
    }

    #[getter]
    pub fn first_session_lens(&self) -> [f32; 4] {
        self.0.first_session_lens
    }

    #[getter]
    pub fn forget_rating_offset(&self) -> f32 {
        self.0.forget_rating_offset
    }

    #[getter]
    pub fn forget_session_len(&self) -> f32 {
        self.0.forget_session_len
    }

    #[getter]
    pub fn loss_aversion(&self) -> f32 {
        self.0.loss_aversion
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
    pub fn set_learn_costs(&mut self, value: [f32; 4]) {
        self.0.learn_costs = value;
    }

    #[setter]
    pub fn set_review_costs(&mut self, value: [f32; 4]) {
        self.0.review_costs = value;
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
    pub fn set_first_rating_offsets(&mut self, value: [f32; 4]) {
        self.0.first_rating_offsets = value;
    }

    #[setter]
    pub fn set_first_session_lens(&mut self, value: [f32; 4]) {
        self.0.first_session_lens = value;
    }

    #[setter]
    pub fn set_forget_rating_offset(&mut self, value: f32) {
        self.0.forget_rating_offset = value;
    }

    #[setter]
    pub fn set_forget_session_len(&mut self, value: f32) {
        self.0.forget_session_len = value;
    }

    #[setter]
    pub fn set_loss_aversion(&mut self, value: f32) {
        self.0.loss_aversion = value;
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
