# Schema Contract Tester

Bounded record/schema compatibility tests with explicit path errors.

Public offline Python MVP using only the standard library. Inputs are bounded, failures remain visible, and all examples/tests use synthetic data.

## CLI

```bash
python -m schema_contract_tester.cli input.json
python -m unittest discover -s tests -v
python scripts/check.py
```

The public Python API is `schema_contract_tester.core.run(data)`. The CLI accepts the same JSON object from a path or standard input and emits machine-readable JSON.

Apache License 2.0.

