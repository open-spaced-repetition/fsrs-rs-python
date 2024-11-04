# FSRS-RS-Python

Python bindings for fsrs-rs, use burn-rs, instead of pytorch.

```
pip install fsrs-rs-python
```

---

## Usage

see [examples](./examples)

## Development

```bash
maturin develop
find examples/ -exec python {} \;
```

Note: running `examples/train_csv.py` requires `revlog.csv` file, please download from
[revlog.csv](https://github.com/open-spaced-repetition/fsrs-rs/files/15046782/revlog.csv). Then put it in the root folder of this repository.
