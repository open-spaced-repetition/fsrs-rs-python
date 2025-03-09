use pyo3::prelude::*;

#[pyclass(module = "fsrs_rs_python")]
#[derive(Default)]
pub struct SimulatorConfig(pub fsrs::SimulatorConfig);

// Define macros outside the impl block
macro_rules! define_getters {
    ($($field:ident: $type:ty),*) => {
        $(
            #[getter]
            pub fn $field(&self) -> $type {
                self.0.$field
            }
        )*
    };
}

macro_rules! define_setters {
    ($($field:ident: $type:ty),*) => {
        $(
            #[setter]
            pub fn set_$field(&mut self, value: $type) {
                self.0.$field = value;
            }
        )*
    };
}

#[pymethods]
impl SimulatorConfig {
    // Constructor for the wrapper struct
    #[new]
    #[pyo3(signature = (
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
        suspend_after_lapses=None
    ))]
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

    // Generate getters using the macro
    define_getters! {
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

    // Generate setters using the macro
    define_setters! {
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
}
