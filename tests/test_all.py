import pytest
from app.text_utils import TextSanitizer, WordCounter
from app.data_validator import DataValidator
from app.performance import BatchProcessor


# ===================== TextSanitizer Tests =====================


class TestTextSanitizer:
    def test_remove_special_chars(self):
        assert TextSanitizer.remove_special_chars("Hello, World!") == "Hello World"

    def test_remove_special_chars_keeps_alphanumeric(self):
        assert TextSanitizer.remove_special_chars("abc123") == "abc123"

    def test_remove_special_chars_type_error(self):
        with pytest.raises(TypeError):
            TextSanitizer.remove_special_chars(123)

    def test_normalize_whitespace(self):
        assert TextSanitizer.normalize_whitespace("  hello   world  ") == "hello world"

    def test_to_lowercase(self):
        assert TextSanitizer.to_lowercase("HELLO World") == "hello world"

    def test_full_clean_pipeline(self):
        result = TextSanitizer.full_clean("  Hello, WORLD!!!  ")
        assert result == "hello world"

    def test_full_clean_empty(self):
        assert TextSanitizer.full_clean("") == ""


# ===================== WordCounter Tests =====================


class TestWordCounter:
    def setup_method(self):
        self.counter = WordCounter()
        self.counter_with_stops = WordCounter(stop_words={"the", "a", "is"})

    def test_basic_count(self):
        result = self.counter.count("hello world hello")
        assert result["hello"] == 2
        assert result["world"] == 1

    def test_empty_text(self):
        assert self.counter.count("") == {}

    def test_stop_words_filtered(self):
        result = self.counter_with_stops.count("the cat is a hero")
        assert "the" not in result
        assert "a" not in result
        assert "cat" in result

    def test_top_n(self):
        text = "a a a b b c"
        tops = self.counter.top_n(text, n=2)
        assert tops[0][0] == "a"
        assert tops[0][1] == 3

    def test_top_n_invalid(self):
        with pytest.raises(ValueError):
            self.counter.top_n("hello", n=0)

    def test_unique_word_count(self):
        assert self.counter.unique_word_count("hello world hello") == 2

    def test_special_chars_ignored(self):
        result = self.counter.count("hello! world? hello.")
        assert result.get("hello") == 2


# ===================== DataValidator Tests =====================


class TestDataValidator:
    def test_valid_email(self):
        assert DataValidator.validate_email("user@example.com")

    def test_invalid_email_no_at(self):
        result = DataValidator.validate_email("userexample.com")
        assert not result
        assert len(result.errors) > 0

    def test_empty_email(self):
        result = DataValidator.validate_email("")
        assert not result

    def test_non_string_email(self):
        result = DataValidator.validate_email(123)
        assert not result

    def test_valid_amount(self):
        assert DataValidator.validate_amount(500.0)

    def test_negative_amount(self):
        result = DataValidator.validate_amount(-10)
        assert not result

    def test_zero_amount_valid(self):
        assert DataValidator.validate_amount(0)

    def test_amount_too_large(self):
        result = DataValidator.validate_amount(99_000_000)
        assert not result

    def test_non_number_amount(self):
        result = DataValidator.validate_amount("abc")
        assert not result

    def test_valid_non_empty_string(self):
        assert DataValidator.validate_non_empty_string("hello", "Name")

    def test_empty_string_invalid(self):
        result = DataValidator.validate_non_empty_string("   ", "Name")
        assert not result

    def test_integer_range_valid(self):
        assert DataValidator.validate_integer_range(5, 1, 10, "Month")

    def test_integer_range_out_of_bounds(self):
        result = DataValidator.validate_integer_range(15, 1, 12, "Month")
        assert not result

    def test_integer_range_non_integer(self):
        result = DataValidator.validate_integer_range(3.5, 1, 12)
        assert not result


# ===================== BatchProcessor Tests =====================


class TestBatchProcessor:
    def test_basic_processing(self):
        bp = BatchProcessor(batch_size=2)
        result = bp.process([1, 2, 3, 4], lambda x: x * 2)
        assert result["results"] == [2, 4, 6, 8]
        assert result["processed"] == 4
        assert result["errors"] == 0

    def test_error_handling(self):
        bp = BatchProcessor(batch_size=10)

        def risky(x):
            if x == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return 10 / x

        result = bp.process([1, 0, 2], risky)
        assert result["errors"] == 1
        assert result["processed"] == 2

    def test_invalid_batch_size(self):
        with pytest.raises(ValueError):
            BatchProcessor(batch_size=0)

    def test_empty_input(self):
        bp = BatchProcessor()
        result = bp.process([], lambda x: x)
        assert result["total"] == 0
        assert result["processed"] == 0

    def test_batches_generator(self):
        bp = BatchProcessor(batch_size=3)
        batches = list(bp.batches([1, 2, 3, 4, 5]))
        assert batches == [[1, 2, 3], [4, 5]]

    def test_stats_property(self):
        bp = BatchProcessor()
        bp.process([1, 2, 3], lambda x: x)
        assert bp.stats["processed"] == 3
        assert bp.stats["errors"] == 0

    def test_elapsed_time_recorded(self):
        bp = BatchProcessor()
        result = bp.process(list(range(50)), lambda x: x**2)
        assert "elapsed_seconds" in result
        assert result["elapsed_seconds"] >= 0
