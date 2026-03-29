# DevOps Toolkit — CI/CD Showcase

A Python utility library built **CI/CD-first**: every commit triggers linting, matrix testing across Python 3.10/3.11/3.12, security scanning, and coverage enforcement — all via GitHub Actions.

![CI](https://github.com/Vedadweep/devops-toolkit/actions/workflows/ci.yml/badge.svg)

---

## Purpose

This project demonstrates professional software engineering practices that go beyond just writing code:
- **Test-driven design** — 30+ unit tests, >90% coverage enforced in CI
- **Multi-version compatibility** — tested on Python 3.10, 3.11, and 3.12 simultaneously via matrix builds
- **Code quality gates** — black formatter, isort, and flake8 must all pass before tests run
- **Security scanning** — bandit checks for common vulnerabilities on every push
- **Clean OOP** — each module follows single-responsibility principle with documented interfaces

---

## Modules

### `TextSanitizer` & `WordCounter`
Text cleaning pipeline and frequency analysis with stop-word filtering.
```python
from app.text_utils import WordCounter
wc = WordCounter(stop_words={"the", "a", "is"})
wc.top_n("the quick brown fox is a quick animal", n=2)
# → [('quick', 2), ('brown', 1)]
```

### `DataValidator`
Validates emails, amounts, strings, and integer ranges — returns structured `ValidationResult` objects.
```python
from app.data_validator import DataValidator
result = DataValidator.validate_email("bad-email")
print(result.is_valid)  # False
print(result.errors)    # ["'bad-email' is not a valid email address"]
```

### `BatchProcessor`
Memory-efficient batch processing with error isolation and timing stats.
```python
from app.performance import BatchProcessor
bp = BatchProcessor(batch_size=50)
result = bp.process(range(1000), lambda x: x ** 2)
print(result["processed"])  # 1000
print(result["elapsed_seconds"])  # ~0.001
```

---

## CI/CD Pipeline

The pipeline has **4 sequential jobs**:

```
push → [lint] → [test (3.10)] ─┐
              → [test (3.11)] ─┼─→ [build-summary ✅]
              → [test (3.12)] ─┘
              → [security scan] ─┘
```

| Job | Tool | Gate |
|---|---|---|
| Lint | flake8 + black + isort | Must pass before tests run |
| Test | pytest + pytest-cov | >90% coverage required |
| Security | bandit | Medium/high severity = fail |
| Summary | — | Only runs if all above pass |

---

## Running Locally

```bash
git clone https://github.com/Vedadweep/devops-toolkit.git
cd devops-toolkit
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=app --cov-report=term-missing

# Run linters
black app/ tests/
isort app/ tests/
flake8 app/ tests/

# Security scan
bandit -r app/ -ll
```

---

## Project Structure

```
devops-toolkit/
├── app/
│   ├── __init__.py
│   ├── text_utils.py       # TextSanitizer, WordCounter
│   ├── data_validator.py   # DataValidator, ValidationResult
│   └── performance.py      # BatchProcessor
├── tests/
│   └── test_all.py         # 30+ unit tests, >90% coverage
├── .github/
│   └── workflows/
│       └── ci.yml          # 4-job pipeline: lint → test (matrix) → security → summary
├── requirements.txt
└── README.md
```
