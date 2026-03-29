"""
Data validation utilities.
Demonstrates: defensive programming, clear error messages, edge case handling.
"""

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]

    def __bool__(self):
        return self.is_valid


class DataValidator:
    """Validates common data types with descriptive error messages."""

    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        errors = []
        if not isinstance(email, str):
            return ValidationResult(False, ["Email must be a string"])
        if not email.strip():
            errors.append("Email cannot be empty")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(pattern, email):
            errors.append(f"'{email}' is not a valid email address")
        return ValidationResult(len(errors) == 0, errors)

    @staticmethod
    def validate_amount(amount: Any) -> ValidationResult:
        errors = []
        if not isinstance(amount, (int, float)):
            return ValidationResult(False, ["Amount must be a number"])
        if amount < 0:
            errors.append("Amount cannot be negative")
        if amount > 10_000_000:
            errors.append("Amount exceeds maximum allowed value")
        return ValidationResult(len(errors) == 0, errors)

    @staticmethod
    def validate_non_empty_string(value: Any, field_name: str = "Field") -> ValidationResult:
        if not isinstance(value, str):
            return ValidationResult(False, [f"{field_name} must be a string"])
        if not value.strip():
            return ValidationResult(False, [f"{field_name} cannot be empty or whitespace"])
        return ValidationResult(True, [])

    @staticmethod
    def validate_integer_range(
        value: Any, min_val: int, max_val: int, field_name: str = "Value"
    ) -> ValidationResult:
        errors = []
        if not isinstance(value, int):
            return ValidationResult(False, [f"{field_name} must be an integer"])
        if value < min_val or value > max_val:
            errors.append(f"{field_name} must be between {min_val} and {max_val}, got {value}")
        return ValidationResult(len(errors) == 0, errors)
