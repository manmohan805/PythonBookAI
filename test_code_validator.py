from code_validator import validate_code


def test_valid_python():
    answer = (
        "Example:\n"
        "```python\n"
        "a = [1, 2, 3]\n"
        "print(a)\n"
        "```\n"
    )

    result = validate_code(answer)

    assert result["has_code"] is True
    assert result["valid"] is True

    print("PASS: Valid Python code")


def test_invalid_python():
    answer = (
        "```python\n"
        "if True print('Hello')\n"
        "```\n"
    )

    result = validate_code(answer)

    assert result["has_code"] is True
    assert result["valid"] is False

    print("PASS: Invalid Python syntax detected")


def test_unsafe_string_identity():
    answer = (
        "```python\n"
        "a = 'Python is fun!'\n"
        "b = 'Python is fun!'\n"
        "print(a == b)\n"
        "print(a is b)\n"
        "```\n"
    )

    result = validate_code(answer)

    assert result["has_code"] is True
    assert any(
        "identity" in warning.lower()
        for warning in result["warnings"]
    )

    print("PASS: Unsafe string identity warning detected")


def test_safe_list_identity():
    answer = (
        "```python\n"
        "a = [1, 2, 3]\n"
        "b = [1, 2, 3]\n"
        "print(a == b)\n"
        "print(a is b)\n"
        "```\n"
    )

    result = validate_code(answer)

    assert result["has_code"] is True
    assert not any(
        "identity" in warning.lower()
        for warning in result["warnings"]
    )

    print("PASS: Safe list identity example")


def test_answer_without_code():
    answer = "A list is an ordered, mutable collection in Python."

    result = validate_code(answer)

    assert result["has_code"] is False

    print("PASS: Answer without code")


if __name__ == "__main__":
    test_valid_python()
    test_invalid_python()
    test_unsafe_string_identity()
    test_safe_list_identity()
    test_answer_without_code()

    print("\nAll tests passed!")