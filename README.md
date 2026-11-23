# CA2 - Code-Level Vulnerabilities

Four vulnerability classes, each shown in three states: vulnerable, exploited and mitigated.

## Requirements

Python 3.13 or later, standard library only (no `pip install` needed). The recorded run used Python 3.13.9 on macOS. To use a different interpreter, set the `PYTHON` environment variable, e.g. `PYTHON=python3.14 ./run_all.sh`.

## Run everything

From the repository root:

```bash
./run_all.sh
```

The script runs each exploit against both versions and prints an eight-row summary table. Every row should read `OK`: four `RESULT: EXPLOITED` against the vulnerable versions and four `RESULT: BLOCKED` against the mitigated ones. The full output of each class is written to its `test_output.txt`. The whole run takes a few seconds.

## Run a single class

```bash
python3 01-injection/exploit.py vulnerable
python3 01-injection/exploit.py mitigated
```

The exploit prints `RESULT: EXPLOITED` and exits with code 0 when the attack succeeds. It prints `RESULT: BLOCKED` and exits with code 1 when the mitigation stops it.

## Structure

- `01-injection/`: SQL injection in an SQLite catalogue search.
- `02-idor/`: access to another user's booking through a sequential ID.
- `03-crypto-misuse/`: unsalted SHA-256 compared with salted scrypt for password storage.
- `04-toctou/`: concurrent withdrawals with a non-atomic check, and the same operation under a lock.
- `literature/pdfs/`: the sources read for the literature review.
- `sources.md`: verified references and reading notes, grouped by theme.
- `appendix-a.md`: AI use declaration.

Each class folder contains `vulnerable.py`, `exploit.py`, `mitigated.py` and `test_output.txt`.

## Warning

The vulnerable code is intentional and intended only for academic use in a local environment. Do not use it in production.
