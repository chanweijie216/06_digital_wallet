import pytest

from wallet_withdrawal import withdraw


# ---------------------------------------------------------------- valid inputs
@pytest.mark.parametrize("balance_cents, amount_cents, expected",[
    (1000, 300, 700),
    (1000, 1, 999)],
    ids=["typical_amount", "minimum_amount"],
)
def test_valid_amount_returns_remaining_balance_valid(balance_cents, amount_cents, expected):
    """remaining balance is returned as an int."""
    # Arrange: balance_cents, amount_cents and expected come from parametrize

    # Act
    result = withdraw(balance_cents, amount_cents)

    # Assert
    assert result == expected
    assert type(result) is int


def test_exact_balance_returns_zero_valid():
    """withdrawing the exact balance is allowed and returns zero."""
    # Arrange
    balance_cents = 1000
    amount_cents = 1000

    # Act
    result = withdraw(balance_cents, amount_cents)

    # Assert
    assert result == 0


# ------------------------------------------------------ invalid: out of range
@pytest.mark.parametrize("amount_cents",
    [0, -1],
    ids=["zero_amount", "negative_amount"],
)
def test_zero_or_negative_amount_raises_value_error_invalid(amount_cents):
    """a zero or negative amount raises ValueError."""
    # Arrange
    balance_cents = 1000

    # Act & Assert
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


def test_negative_balance_raises_value_error_invalid():
    """a negative balance raises ValueError."""
    # Arrange
    balance_cents = -1
    amount_cents = 1

    # Act & Assert
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


def test_amount_above_balance_raises_value_error_invalid():
    """a withdrawal above the balance raises ValueError."""
    # Arrange
    balance_cents = 1000
    amount_cents = 1001

    # Act & Assert
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


# ------------------------------------------------------- invalid: wrong type
@pytest.mark.parametrize("balance_cents, amount_cents",[
    (1000.0, 100),
    (1000, "100"),
    (1000, None)],
    ids=["balance_float", "amount_str", "amount_none"],
)
def test_non_integer_argument_raises_type_error_invalid(balance_cents, amount_cents):
    """a float, str or None argument raises TypeError."""
    # Arrange: balance_cents and amount_cents come from parametrize

    # Act & Assert
    with pytest.raises(TypeError):
        withdraw(balance_cents, amount_cents)


@pytest.mark.parametrize("balance_cents, amount_cents",[
    (True, 1),
    (1000, True)],
    ids=["balance_True", "amount_True"],
)
def test_boolean_argument_raises_type_error_invalid(balance_cents, amount_cents):
    """booleans are not valid integers (True must not act as 1)."""
    # Arrange: balance_cents and amount_cents come from parametrize

    # Act & Assert
    with pytest.raises(TypeError):
        withdraw(balance_cents, amount_cents)
