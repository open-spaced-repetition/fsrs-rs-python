mod simulator_config;
use fsrs::ComputeParametersInput;
use simulator_config::SimulatorConfig;

use std::sync::Mutex;

use pyo3::prelude::*;
#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug)]
pub struct FSRS(Mutex<fsrs::FSRS>);
#[pymethods]
impl FSRS {
    #[new]
    pub fn new(parameters: Vec<f32>) -> Self {
        Self(fsrs::FSRS::new(Some(&parameters)).unwrap().into())
    }
    #[pyo3(signature=(current_memory_state,desired_retention,days_elapsed))]
    pub fn next_states(
        &self,
        current_memory_state: Option<MemoryState>,
        desired_retention: f32,
        days_elapsed: u32,
    ) -> NextStates {
        NextStates(
            self.0
                .lock()
                .unwrap()
                .next_states(
                    current_memory_state.map(|x| x.0),
                    desired_retention,
                    days_elapsed,
                )
                .unwrap(),
        )
    }
    pub fn compute_parameters(&self, train_set: Vec<FSRSItem>) -> Vec<f32> {
        self.0
            .lock()
            .unwrap()
            .compute_parameters(ComputeParametersInput {
                train_set: train_set.iter().map(|x| x.0.clone()).collect(),
                progress: None,
                enable_short_term: true,
                num_relearning_steps: None,
            })
            .unwrap_or_default()
    }
    pub fn benchmark(&self, train_set: Vec<FSRSItem>) -> Vec<f32> {
        self.0.lock().unwrap().benchmark(ComputeParametersInput {
            train_set: train_set.iter().map(|x| x.0.clone()).collect(),
            progress: None,
            enable_short_term: true,
            num_relearning_steps: None,
        })
    }
    pub fn memory_state_from_sm2(
        &self,
        ease_factor: f32,
        interval: f32,
        sm2_retention: f32,
    ) -> MemoryState {
        MemoryState(
            self.0
                .lock()
                .unwrap()
                .memory_state_from_sm2(ease_factor, interval, sm2_retention)
                .unwrap(),
        )
    }
    #[pyo3(signature = (item, starting_state=None))]
    pub fn memory_state(&self, item: FSRSItem, starting_state: Option<MemoryState>) -> MemoryState {
        MemoryState(
            self.0
                .lock()
                .unwrap()
                .memory_state(item.0, starting_state.map(|x| x.0))
                .unwrap(),
        )
    }
}
#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct MemoryState(fsrs::MemoryState);

#[pymethods]
impl MemoryState {
    #[new]
    pub fn new(stability: f32, difficulty: f32) -> Self {
        Self(fsrs::MemoryState {
            stability,
            difficulty,
        })
    }
    #[getter]
    pub fn stability(&self) -> f32 {
        self.0.stability
    }
    #[getter]
    pub fn difficulty(&self) -> f32 {
        self.0.difficulty
    }
    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct NextStates(fsrs::NextStates);
#[pymethods]
impl NextStates {
    #[getter]
    pub fn hard(&self) -> ItemState {
        ItemState(self.0.hard.clone())
    }
    #[getter]
    pub fn good(&self) -> ItemState {
        ItemState(self.0.good.clone())
    }
    #[getter]
    pub fn easy(&self) -> ItemState {
        ItemState(self.0.easy.clone())
    }
    #[getter]
    pub fn again(&self) -> ItemState {
        ItemState(self.0.again.clone())
    }
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct ItemState(fsrs::ItemState);

#[pymethods]
impl ItemState {
    #[getter]
    pub fn memory(&self) -> MemoryState {
        MemoryState(self.0.memory)
    }
    #[getter]
    pub fn interval(&self) -> f32 {
        self.0.interval
    }
    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct FSRSItem(fsrs::FSRSItem);

#[pymethods]
impl FSRSItem {
    #[new]
    pub fn new(reviews: Vec<FSRSReview>) -> Self {
        Self(fsrs::FSRSItem {
            reviews: reviews.iter().map(|x| x.0).collect(),
        })
    }
    #[getter]
    pub fn get_reviews(&self) -> Vec<FSRSReview> {
        self.0.reviews.iter().map(|x| FSRSReview(*x)).collect()
    }
    #[setter]
    pub fn set_reviews(&mut self, other: Vec<FSRSReview>) {
        self.0.reviews = other.iter().map(|x| x.0).collect()
    }

    pub fn long_term_review_cnt(&self) -> usize {
        self.0
            .reviews
            .iter()
            .filter(|review| review.delta_t > 0)
            .count()
    }
    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct FSRSReview(fsrs::FSRSReview);

#[pymethods]
impl FSRSReview {
    #[new]
    pub fn new(rating: u32, delta_t: u32) -> Self {
        Self(fsrs::FSRSReview { rating, delta_t })
    }
    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(module = "fsrs_rs_python")]
pub struct SimulationResult(fsrs::SimulationResult);
#[pymethods]
impl SimulationResult {
    #[getter]
    pub fn memorized_cnt_per_day(&self) -> Vec<f32> {
        self.0.memorized_cnt_per_day.clone()
    }
    #[getter]
    pub fn review_cnt_per_day(&self) -> Vec<usize> {
        self.0.review_cnt_per_day.clone()
    }
    #[getter]
    pub fn learn_cnt_per_day(&self) -> Vec<usize> {
        self.0.learn_cnt_per_day.clone()
    }
    #[getter]
    pub fn cost_per_day(&self) -> Vec<f32> {
        self.0.cost_per_day.clone()
    }
    #[getter]
    pub fn correct_cnt_per_day(&self) -> Vec<usize> {
        self.0.correct_cnt_per_day.clone()
    }
}

#[pyfunction]
#[pyo3(signature=(w,desired_retention,config=None,seed=None))]
fn simulate(
    w: Vec<f32>,
    desired_retention: f32,
    config: Option<&SimulatorConfig>,
    seed: Option<u64>,
) -> SimulationResult {
    let default_config = SimulatorConfig::default();
    let config = config.unwrap_or(&default_config);
    SimulationResult(fsrs::simulate(&config.0, &w, desired_retention, seed, None).unwrap())
}

#[pyfunction]
fn default_simulator_config() -> SimulatorConfig {
    SimulatorConfig::default()
}

/// A Python module implemented in Rust.
#[pymodule]
fn fsrs_rs_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FSRS>()?;
    m.add_class::<MemoryState>()?;
    m.add_class::<NextStates>()?;
    m.add_class::<ItemState>()?;
    m.add_class::<FSRSItem>()?;
    m.add_class::<FSRSReview>()?;
    m.add_function(wrap_pyfunction!(simulate, m)?)?;
    m.add_function(wrap_pyfunction!(default_simulator_config, m)?)?;
    m.add(
        "DEFAULT_PARAMETERS",
        [
            0.40255, 1.18385, 3.173, 15.69105, 7.1949, 0.5345, 1.4604, 0.0046, 1.54575, 0.1192,
            1.01925, 1.9395, 0.11, 0.29605, 2.2698, 0.2315, 2.9898, 0.51655, 0.6621,
        ],
    )?;
    Ok(())
}
