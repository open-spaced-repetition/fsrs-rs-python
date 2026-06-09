#![feature(try_blocks)]

mod simulator_config;
use fsrs::ComputeParametersInput;
use simulator_config::SimulatorConfig;

use std::sync::Mutex;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

fn fsrs_error_to_py(error: fsrs::FSRSError) -> PyErr {
    PyValueError::new_err(error.to_string())
}

fn convert_training_config(
    training_config: Option<&TrainingConfig>,
) -> PyResult<Option<fsrs::TrainingConfig>> {
    training_config
        .map(TrainingConfig::as_valid_fsrs)
        .transpose()
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug)]
pub struct FSRS(Mutex<fsrs::FSRS>);
#[pymethods]
impl FSRS {
    #[new]
    pub fn new(parameters: Vec<f32>) -> PyResult<Self> {
        Ok(Self(Mutex::new(
            fsrs::FSRS::new(&parameters).map_err(fsrs_error_to_py)?,
        )))
    }
    #[pyo3(signature=(current_memory_state,desired_retention,days_elapsed))]
    pub fn next_states(
        &self,
        current_memory_state: Option<MemoryState>,
        desired_retention: f32,
        days_elapsed: u32,
    ) -> PyResult<NextStates> {
        self.0
            .lock()
            .unwrap()
            .next_states(
                current_memory_state.map(|x| x.0),
                desired_retention,
                days_elapsed,
            )
            .map(NextStates)
            .map_err(fsrs_error_to_py)
    }
    #[pyo3(signature = (fsrs_items, card_ids=None, enable_short_term=true, num_relearning_steps=None, training_config=None))]
    pub fn compute_parameters(
        &self,
        fsrs_items: Vec<FSRSItem>,
        card_ids: Option<Vec<i64>>,
        enable_short_term: bool,
        num_relearning_steps: Option<usize>,
        training_config: Option<&TrainingConfig>,
    ) -> PyResult<Vec<f32>> {
        let training_config = convert_training_config(training_config)?;

        fsrs::compute_parameters(ComputeParametersInput {
            train_set: fsrs_items.into_iter().map(|x| x.0).collect(),
            card_ids,
            progress: None,
            enable_short_term,
            num_relearning_steps,
            training_config,
        })
        .map_err(fsrs_error_to_py)
    }
    #[pyo3(signature = (fsrs_items, card_ids=None, enable_short_term=true, num_relearning_steps=None, training_config=None))]
    pub fn benchmark(
        &self,
        fsrs_items: Vec<FSRSItem>,
        card_ids: Option<Vec<i64>>,
        enable_short_term: bool,
        num_relearning_steps: Option<usize>,
        training_config: Option<&TrainingConfig>,
    ) -> PyResult<Vec<f32>> {
        let training_config = convert_training_config(training_config)?;

        Ok(fsrs::benchmark(ComputeParametersInput {
            train_set: fsrs_items.into_iter().map(|x| x.0).collect(),
            card_ids,
            progress: None,
            enable_short_term,
            num_relearning_steps,
            training_config,
        }))
    }
    pub fn memory_state_from_sm2(
        &self,
        ease_factor: f32,
        interval: f32,
        sm2_retention: f32,
    ) -> PyResult<MemoryState> {
        self.0
            .lock()
            .unwrap()
            .memory_state_from_sm2(ease_factor, interval, sm2_retention)
            .map(MemoryState)
            .map_err(fsrs_error_to_py)
    }
    #[pyo3(signature = (item, starting_state=None))]
    pub fn memory_state(
        &self,
        item: FSRSItem,
        starting_state: Option<MemoryState>,
    ) -> PyResult<MemoryState> {
        self.0
            .lock()
            .unwrap()
            .memory_state(item.0, starting_state.map(|x| x.0))
            .map(MemoryState)
            .map_err(fsrs_error_to_py)
    }

    #[pyo3(signature = (stability, desired_retention, rating))]
    pub fn next_interval(
        &self,
        stability: Option<f32>,
        desired_retention: f32,
        rating: u32,
    ) -> f32 {
        self.0
            .lock()
            .unwrap()
            .next_interval(stability, desired_retention, rating)
    }

    #[pyo3(signature = (items, starting_states=None))]
    pub fn memory_state_batch(
        &self,
        items: Vec<FSRSItem>,
        starting_states: Option<Vec<Option<MemoryState>>>,
    ) -> PyResult<Vec<MemoryState>> {
        let starting_states =
            starting_states.unwrap_or_else(|| (0..items.len()).map(|_| None).collect());
        self.0
            .lock()
            .unwrap()
            .memory_state_batch(
                items.into_iter().map(|x| x.0).collect(),
                starting_states
                    .into_iter()
                    .map(|state| state.map(|x| x.0))
                    .collect(),
            )
            .map(|states| states.into_iter().map(MemoryState).collect())
            .map_err(fsrs_error_to_py)
    }

    #[pyo3(signature = (item, starting_state=None))]
    pub fn historical_memory_states(
        &self,
        item: FSRSItem,
        starting_state: Option<MemoryState>,
    ) -> PyResult<Vec<MemoryState>> {
        self.0
            .lock()
            .unwrap()
            .historical_memory_states(item.0, starting_state.map(|x| x.0))
            .map(|states| states.into_iter().map(MemoryState).collect())
            .map_err(fsrs_error_to_py)
    }

    #[pyo3(signature = (items, starting_states=None))]
    pub fn historical_memory_state_batch(
        &self,
        items: Vec<FSRSItem>,
        starting_states: Option<Vec<Option<MemoryState>>>,
    ) -> PyResult<Vec<Vec<MemoryState>>> {
        self.0
            .lock()
            .unwrap()
            .historical_memory_state_batch(
                items.into_iter().map(|x| x.0).collect(),
                starting_states
                    .map(|states| states.into_iter().map(|state| state.map(|x| x.0)).collect()),
            )
            .map(|states| {
                states
                    .into_iter()
                    .map(|row| row.into_iter().map(MemoryState).collect())
                    .collect()
            })
            .map_err(fsrs_error_to_py)
    }

    pub fn evaluate(&self, fsrs_items: Vec<FSRSItem>) -> PyResult<ModelEvaluation> {
        self.0
            .lock()
            .unwrap()
            .evaluate(fsrs_items.into_iter().map(|x| x.0).collect(), |_| true)
            .map(ModelEvaluation)
            .map_err(fsrs_error_to_py)
    }
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct TrainingConfig(fsrs::TrainingConfig);

impl TrainingConfig {
    fn as_valid_fsrs(&self) -> PyResult<fsrs::TrainingConfig> {
        if self.0.batch_size == 0 || !self.0.learning_rate.is_finite() || !self.0.gamma.is_finite()
        {
            return Err(PyValueError::new_err(
                "batch_size must be greater than 0, and learning_rate and gamma must be finite",
            ));
        }

        Ok(self.0)
    }
}

#[pymethods]
impl TrainingConfig {
    #[new]
    #[pyo3(signature = (num_epochs=5, batch_size=512, seed=2023, learning_rate=4e-2, max_seq_len=256, gamma=1.0))]
    pub fn new(
        num_epochs: usize,
        batch_size: usize,
        seed: u64,
        learning_rate: f64,
        max_seq_len: usize,
        gamma: f64,
    ) -> PyResult<Self> {
        let config = Self(fsrs::TrainingConfig {
            num_epochs,
            batch_size,
            seed,
            learning_rate,
            max_seq_len,
            gamma,
        });
        config.as_valid_fsrs()?;
        Ok(config)
    }

    #[getter]
    pub fn num_epochs(&self) -> usize {
        self.0.num_epochs
    }

    #[setter]
    pub fn set_num_epochs(&mut self, value: usize) {
        self.0.num_epochs = value;
    }

    #[getter]
    pub fn batch_size(&self) -> usize {
        self.0.batch_size
    }

    #[setter]
    pub fn set_batch_size(&mut self, value: usize) -> PyResult<()> {
        if value == 0 {
            return Err(PyValueError::new_err("batch_size must be greater than 0"));
        }
        self.0.batch_size = value;
        Ok(())
    }

    #[getter]
    pub fn seed(&self) -> u64 {
        self.0.seed
    }

    #[setter]
    pub fn set_seed(&mut self, value: u64) {
        self.0.seed = value;
    }

    #[getter]
    pub fn learning_rate(&self) -> f64 {
        self.0.learning_rate
    }

    #[setter]
    pub fn set_learning_rate(&mut self, value: f64) -> PyResult<()> {
        if !value.is_finite() {
            return Err(PyValueError::new_err("learning_rate must be finite"));
        }
        self.0.learning_rate = value;
        Ok(())
    }

    #[getter]
    pub fn max_seq_len(&self) -> usize {
        self.0.max_seq_len
    }

    #[setter]
    pub fn set_max_seq_len(&mut self, value: usize) {
        self.0.max_seq_len = value;
    }

    #[getter]
    pub fn gamma(&self) -> f64 {
        self.0.gamma
    }

    #[setter]
    pub fn set_gamma(&mut self, value: f64) -> PyResult<()> {
        if !value.is_finite() {
            return Err(PyValueError::new_err("gamma must be finite"));
        }
        self.0.gamma = value;
        Ok(())
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct ModelEvaluation(fsrs::ModelEvaluation);

#[pymethods]
impl ModelEvaluation {
    #[getter]
    pub fn log_loss(&self) -> f32 {
        self.0.log_loss
    }

    #[getter]
    pub fn rmse_bins(&self) -> f32 {
        self.0.rmse_bins
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
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
    #[getter]
    pub fn average_desired_retention(&self) -> Option<f32> {
        self.0.average_desired_retention
    }
    #[getter]
    pub fn introduced_cnt_per_day(&self) -> Vec<usize> {
        self.0.introduced_cnt_per_day.clone()
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

#[pyfunction]
#[pyo3(signature = (fsrs_items, card_ids=None, enable_short_term=true, num_relearning_steps=None, training_config=None))]
fn evaluate_with_time_series_splits(
    fsrs_items: Vec<FSRSItem>,
    card_ids: Option<Vec<i64>>,
    enable_short_term: bool,
    num_relearning_steps: Option<usize>,
    training_config: Option<&TrainingConfig>,
) -> PyResult<ModelEvaluation> {
    let training_config = convert_training_config(training_config)?;

    fsrs::evaluate_with_time_series_splits(
        ComputeParametersInput {
            train_set: fsrs_items.into_iter().map(|x| x.0).collect(),
            card_ids,
            progress: None,
            enable_short_term,
            num_relearning_steps,
            training_config,
        },
        |_| true,
    )
    .map(ModelEvaluation)
    .map_err(fsrs_error_to_py)
}

#[pyfunction]
fn filter_outlier(
    dataset_for_initialization: Vec<FSRSItem>,
    trainset: Vec<FSRSItem>,
) -> PyResult<(Vec<FSRSItem>, Vec<FSRSItem>)> {
    if dataset_for_initialization
        .iter()
        .chain(trainset.iter())
        .any(|item| item.0.reviews.is_empty())
    {
        return Err(PyValueError::new_err("FSRSItem reviews must not be empty"));
    }

    let (dataset_for_initialization, trainset) = fsrs::filter_outlier(
        dataset_for_initialization
            .into_iter()
            .map(|item| item.0)
            .collect(),
        trainset.into_iter().map(|item| item.0).collect(),
    );

    Ok((
        dataset_for_initialization
            .into_iter()
            .map(FSRSItem)
            .collect(),
        trainset.into_iter().map(FSRSItem).collect(),
    ))
}

#[pyfunction]
fn check_and_fill_parameters(parameters: Vec<f32>) -> PyResult<Vec<f32>> {
    fsrs::check_and_fill_parameters(&parameters).map_err(fsrs_error_to_py)
}

/// A Python module implemented in Rust.
#[pymodule]
fn fsrs_rs_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FSRS>()?;
    m.add_class::<TrainingConfig>()?;
    m.add_class::<ModelEvaluation>()?;
    m.add_class::<MemoryState>()?;
    m.add_class::<NextStates>()?;
    m.add_class::<ItemState>()?;
    m.add_class::<FSRSItem>()?;
    m.add_class::<FSRSReview>()?;
    m.add_class::<SimulationResult>()?;
    m.add_class::<SimulatorConfig>()?;
    m.add_function(wrap_pyfunction!(simulate, m)?)?;
    m.add_function(wrap_pyfunction!(default_simulator_config, m)?)?;
    m.add_function(wrap_pyfunction!(evaluate_with_time_series_splits, m)?)?;
    m.add_function(wrap_pyfunction!(filter_outlier, m)?)?;
    m.add_function(wrap_pyfunction!(check_and_fill_parameters, m)?)?;
    m.add("DEFAULT_PARAMETERS", fsrs::DEFAULT_PARAMETERS.to_vec())?;
    Ok(())
}
