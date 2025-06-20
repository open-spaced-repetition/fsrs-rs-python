# FSRS-RS-Python

<a href="https://pypi.org/project/fsrs-rs-python/"><img src="https://img.shields.io/pypi/v/fsrs-rs-python"></a>

Python bindings for [fsrs-rs](https://github.com/open-spaced-repetition/fsrs-rs), use burn-rs, instead of pytorch.

```
pip install fsrs-rs-python
```

---

## Usage

see [examples](./examples)

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
