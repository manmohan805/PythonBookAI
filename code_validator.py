import ast
import re


def extract_python_code(answer: str) -> list[str]:
    """Extract Python code blocks from an AI-generated answer."""

    pattern = r"```(?:python)?\s*(.*?)```"

    return re.findall(
        pattern,
        answer,
        flags=re.DOTALL | re.IGNORECASE
    )


def check_syntax(code: str) -> tuple[bool, str]:
    """Check Python syntax using the AST parser."""

    try:
        ast.parse(code)
        return True, "Syntax is valid."

    except SyntaxError as error:
        return False, (
            f"Syntax error at line {error.lineno}: {error.msg}"
        )


def check_python2_patterns(code: str) -> list[str]:
    """Detect some obvious Python 2 patterns."""

    warnings = []

    if "<type '" in code:
        warnings.append(
            "Python 2-style type output detected."
        )

    if re.search(
        r"^\s*print\s+[^(]",
        code,
        flags=re.MULTILINE
    ):
        warnings.append(
            "Possible Python 2-style print statement detected."
        )

    if re.search(r"\bxrange\s*\(", code):
        warnings.append(
            "xrange() is Python 2 syntax; use range() in Python 3."
        )

    return warnings


def check_identity_examples(code: str) -> list[str]:
    """
    Detect potentially misleading identity comparisons.

    This is a heuristic check, not a complete Python analyzer.
    """

    warnings = []

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return warnings

    # Find whether the code contains both equality and identity
    # comparisons, regardless of spaces around the operators.
    has_equality = any(
        isinstance(node, ast.Compare)
        and any(
            isinstance(operator, ast.Eq)
            for operator in node.ops
        )
        for node in ast.walk(tree)
    )

    has_identity = any(
        isinstance(node, ast.Compare)
        and any(
            isinstance(operator, (ast.Is, ast.IsNot))
            for operator in node.ops
        )
        for node in ast.walk(tree)
    )

    if not (has_equality and has_identity):
        return warnings

    # Collect simple variable assignments to string literals.
    string_assignments = {}

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    string_assignments[target.id] = (
                        node.value.value
                    )

    # Detect two variables assigned equal string values.
    identical_string_pairs = set()

    variables = list(string_assignments)

    for i, first in enumerate(variables):
        for second in variables[i + 1:]:
            if (
                string_assignments[first]
                == string_assignments[second]
            ):
                identical_string_pairs.add(
                    frozenset((first, second))
                )

    # Check whether an identity comparison uses one of these pairs.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue

        identity_operator_used = any(
            isinstance(operator, (ast.Is, ast.IsNot))
            for operator in node.ops
        )

        if not identity_operator_used:
            continue

        compared_names = []

        operands = [node.left] + node.comparators

        for operand in operands:
            if isinstance(operand, ast.Name):
                compared_names.append(operand.id)

        for i, first in enumerate(compared_names):
            for second in compared_names[i + 1:]:
                if frozenset((first, second)) in identical_string_pairs:
                    warnings.append(
                        "Potentially unreliable string identity "
                        "comparison detected. Do not assume that "
                        "identical string values are different "
                        "objects. Use lists or explicit shared "
                        "references to teach object identity."
                    )
                    return warnings

    return warnings


def validate_code(answer: str) -> dict:
    """
    Validate Python code blocks in an AI-generated answer.

    Checks:
    1. Python code extraction
    2. Syntax
    3. Common Python 2 patterns
    4. Potentially misleading identity comparisons
    """

    code_blocks = extract_python_code(answer)

    if not code_blocks:
        return {
            "has_code": False,
            "valid": True,
            "errors": [],
            "warnings": [],
            "code_blocks": []
        }

    errors = []
    warnings = []

    for index, code in enumerate(code_blocks, start=1):

        # Syntax validation
        valid, message = check_syntax(code)

        if not valid:
            errors.append(
                f"Code block {index}: {message}"
            )

        # Python 2 checks
        for warning in check_python2_patterns(code):
            warnings.append(
                f"Code block {index}: {warning}"
            )

        # Identity comparison checks
        for warning in check_identity_examples(code):
            warnings.append(
                f"Code block {index}: {warning}"
            )

    return {
        "has_code": True,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "code_blocks": code_blocks
    }