# Lab 5 reflection

The supplied PDF ends after the deliverables section and does not print four reflection questions. These four questions cover the learning outcomes stated in the handout.

## 1. What did each static analysis tool find?

Pylint found the shared mutable default argument, overly broad exception handler, naming problems, and missing docstrings. Bandit found shell command injection, an unsafe temporary filename, and a predictable OTP. Flake8 found whitespace and blank-line violations. The before reports record the exact findings.

## 2. Which findings were most important, and why?

The shell command was the highest priority because a hub address could become a command executed by the shell. The temporary filename was next because another process could claim the path before the program used it. I then fixed the shared list, broad exception, and predictable OTP before style issues.

## 3. How were the fixes verified without changing the program's purpose?

I ran the original demonstration, then the cleaned demonstration, and compared the routes, statuses, courier flags, costs, unknown-ID response, and parcel count. The OTP stays four digits but changes each run. I reran all three analyzers and saved before and after reports. The cleaned file reaches a Pylint score of 10.00/10 and has no Flake8 findings. Bandit's remaining subprocess checks are explicitly documented and suppressed after replacing the shell call with validated, separate arguments.

## 4. What are the limits of static analysis?

Static analysis can point to risky patterns but cannot prove the business rules are correct or that every runtime path works. For example, the scanners do not verify shipping prices or parcel state transitions. Conversely, Bandit flags any subprocess use even when the command is constrained. Running the demo and reviewing each finding are necessary alongside the reports.

