# Static analysis findings

Line numbers refer to the original `parcel_tracker.py` from `SETAPESU26/L5_35_parcel_tracker` (main branch). Findings are ordered by severity. All listed problems were addressed in the cleaned file.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| B602: shell command injection | Bandit, High | 55 | A hub address was concatenated into a command run with `shell=True`. | Validate the address and pass an argument list to `subprocess.run` with no shell. Resolve the ping executable to an absolute path. |
| B306: insecure temporary name | Bandit, Medium | 50 | `tempfile.mktemp` returns a path without creating it, allowing a race. | Use `NamedTemporaryFile(delete=False)` to create the file atomically. |
| W0102: mutable default argument | Pylint, bug | 11 | The same `history=[]` list is reused across calls. | Default to `None`; append only when a caller supplies a history list. |
| W0718: broad exception | Pylint, bug | 37 | `except Exception` hides unrelated failures. | Catch only `KeyError` for an unknown tracking ID. |
| B311: predictable delivery OTP | Bandit, Low | 72 | `random.randint` is unsuitable for a security code. | Use `secrets.randbelow` while retaining a four-digit OTP. |
| B404: subprocess import review | Bandit, Low | 2 | Importing subprocess requires review because process execution can be dangerous. | Keep the optional ping feature, validate the address, avoid a shell, and document the reviewed import with a focused Bandit suppression. |
| C0103 and C0116: naming and documentation | Pylint, style | 11–58 | Camel-case identifiers and missing docstrings reduce readability. | Use snake_case names and add concise module and function docstrings. |
| E225, E231, E261, E305 | Flake8, style | 28, 71, 74–75 | Missing spaces and blank lines break PEP 8 formatting. | Correct spacing and place the demo call behind a main guard. |

The final reports include two narrowly suppressed low-severity subprocess warnings (B404 and B603). The final ping implementation validates the address, uses an absolute executable path, passes arguments separately, and does not invoke a shell.

