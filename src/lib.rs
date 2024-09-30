use pyo3::prelude::*;
#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct FSRS(fsrs::FSRS);
#[pymethods]
impl FSRS {
    #[new]
    pub fn new() -> Self {
        Self(fsrs::FSRS::new(Some(&[])).unwrap())
    }
    #[pyo3(signature=(current_memory_state,desired_retention,days_elapsed ))]
    pub fn next_states(
        &self,
        current_memory_state: Option<MemoryState>,
        desired_retention: f32,
        days_elapsed: u32,
    ) -> NextStates {
        NextStates(
            self.0
                .next_states(
                    current_memory_state.map(|x| x.0),
                    desired_retention,
                    days_elapsed,
                )
                .unwrap(),
        )
    }
}
#[pyclass(module = "fsrs_rs_python")]
#[derive(Debug, Clone)]
pub struct MemoryState(fsrs::MemoryState);

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
        MemoryState(self.0.memory.clone())
    }
    pub fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn fsrs_rs_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<FSRS>()?;
    m.add_class::<MemoryState>()?;
    m.add_class::<NextStates>()?;
    m.add_class::<ItemState>()?;
    Ok(())
}
