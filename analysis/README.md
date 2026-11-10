# Analysis workspace

This directory is the workspace for processing Cowrie JSON logs and producing
analysis outputs. Keep original logs in `data/raw/` unchanged; write derived
data to `data/processed/` and tables or figures to `results/`.

The fixture in `tests/fixtures/` is synthetic and is only for developing and
testing processing code. It is not evidence from the lab and must not be used
in research results. Confirm the schema against real Cowrie smoke-test logs
before finalizing the WP-05 data contract.

Install the listed dependencies with `python -m pip install -r analysis/requirements.txt`
and run the fixture checks with `python -m pytest analysis/tests`.
