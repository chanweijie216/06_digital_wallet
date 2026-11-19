import pytest

from wallet_affordability import can_afford


# ---------------------------------------------------------------- valid inputs
@pytest.mark.parametrize("balance_cents, price_cents",[
    (1000, 500),
    (500, 500),
    (0, 0)],
    ids=["balance_above_price", "balance_equals_price", "zero_price_zero_balance"],
)
def test_balance_covers_price_returns_true_valid(balance_cents, price_cents):
    """balance >= price (incl. a zero price) is affordable."""
    # Arrange: balance_cents and price_cents come from parametrize

    # Act
    result = can_afford(balance_cents, price_cents)

    # Assert
    assert result is True


def test_balance_below_price_returns_false_valid():
    """a lower balance (one cent short) cannot cover the price."""
    # Arrange
    balance_cents = 499
    price_cents = 500

    # Act
    result = can_afford(balance_cents, price_cents)

    # Assert
    assert result is False


# ------------------------------------------------------ invalid: out of range
def test_negative_balance_raises_value_error_invalid():
    """a negative balance raises ValueError."""
    # Arrange
    balance_cents = -1
    price_cents = 500

    # Act & Assert
    with pytest.raises(ValueError):
        can_afford(balance_cents, price_cents)


def test_negative_price_raises_value_error_invalid():
    """a negative price raises ValueError."""
    # Arrange
    balance_cents = 1000
    price_cents = -1

    # Act & Assert
    with pytest.raises(ValueError):
        can_afford(balance_cents, price_cents)


# ------------------------------------------------------- invalid: wrong type
@pytest.mark.parametrize("balance_cents, price_cents",[
    (1000.0, 500),
    (1000, "500"),
    (1000, None)],
    ids=["balance_float", "price_str", "price_none"],
)
def test_non_integer_argument_raises_type_error_invalid(balance_cents, price_cents):
    """a float, str or None argument raises TypeError."""
    # Arrange: balance_cents and price_cents come from parametrize

    # Act & Assert
    with pytest.raises(TypeError):
        can_afford(balance_cents, price_cents)


@pytest.mark.parametrize("balance_cents, price_cents",[
    (True, 0),
    (1000, True)],
    ids=["balance_True", "price_True"],
)
def test_boolean_argument_raises_type_error_invalid(balance_cents, price_cents):
    """booleans are not valid integers."""
    # Arrange: balance_cents and price_cents come from parametrize

    # Act & Assert
    with pytest.raises(TypeError):
        can_afford(balance_cents, price_cents)
