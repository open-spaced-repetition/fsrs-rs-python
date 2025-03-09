use pyo3::prelude::*;

// Define a macro for generating getters
macro_rules! impl_getters {
    ($($field:ident: $type:ty),*) => {
        $(
            #[getter]
            pub fn $field(&self) -> $type {
                self.0.$field
            }
        )*
    };
}

// Define a macro for generating setters
macro_rules! impl_setters {
    ($($field:ident: $type:ty),*) => {
        $(
            #[setter]
            pub fn $field(&mut self, value: $type) {
                self.0.$field = value;
            }
        )*
    };
}

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

    // Generate all getters using the macro
    impl_getters! {
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
        suspend_after_lapses: Option<u32>
    }

    // Generate all setters using the macro
    impl_setters! {
        set_deck_size: usize,
        set_learn_span: usize,
        set_max_cost_perday: f32,
        set_max_ivl: f32,
        set_learn_costs: [f32; 4],
        set_review_costs: [f32; 4],
        set_first_rating_prob: [f32; 4],
        set_review_rating_prob: [f32; 3],
        set_first_rating_offsets: [f32; 4],
        set_first_session_lens: [f32; 4],
        set_forget_rating_offset: f32,
        set_forget_session_len: f32,
        set_loss_aversion: f32,
        set_learn_limit: usize,
        set_review_limit: usize,
        set_new_cards_ignore_review_limit: bool,
        set_suspend_after_lapses: Option<u32>
    }
}
