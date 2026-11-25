# FSRS-RS-Python

<a href="https://pypi.org/project/fsrs-rs-python/"><img src="https://img.shields.io/pypi/v/fsrs-rs-python"></a>

Python bindings for [fsrs-rs](https://github.com/open-spaced-repetition/fsrs-rs), implemented in Rust instead of PyTorch.

```
pip install fsrs-rs-python
```

---

## Usage

see [examples](./examples)

The parameter count selects the model: `DEFAULT_PARAMETERS` (34 values, also used for empty
parameters) is FSRS-7, and `FSRS6_DEFAULT_PARAMETERS` (21 values; 17 and 19 are also accepted)
is FSRS-6. `FSRS.model_version` reports the selected version.

## Online development

go to <https://idx.google.com/import>

## Local development

```bash
maturin build
python -m venv .venv
# active it, then
maturin develop
find examples/ -exec python {} \;
```

Note: running `examples/train_csv.py` requires `revlog.csv` file, please download from
[revlog.csv](https://github.com/open-spaced-repetition/fsrs-rs/files/15046782/revlog.csv). Then put it in the root folder of this repository.
