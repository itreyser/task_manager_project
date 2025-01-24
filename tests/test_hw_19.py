import pytest
from app.shop import Shop


@pytest.fixture()
def my_shop():
    return Shop()


@pytest.fixture()
def shop_with_items():
    my_cart = Shop()
    my_cart.add_to_cart("Test Item 1", 3)
    my_cart.add_to_cart("Test Item 2", 2)
    return my_cart


@pytest.mark.parametrize(
    "item, quantity, expected",
    [
        ("Test Item 1", 3, {"Test Item 1": 3}),
        ("Test Item 2", 1, {"Test Item 2": 1})
    ]

)
def test_add_to_cart(my_shop, item, quantity, expected):
    assert my_shop.add_to_cart(item, quantity) == expected


@pytest.mark.parametrize(
    "item, quantity",
    [
        ("Test Item 1", 0),
        ("Test Item 2", -10)
    ]

)
def test_add_to_cart_invalid(my_shop, item, quantity):
    with pytest.raises(ValueError):
        my_shop.add_to_cart(item, quantity)


@pytest.mark.parametrize(
    "prices, expected",
    [
        ({"Test Item 1": 12, "Test Item 2": 15}, 66)
    ]
)
def test_calculate_total(shop_with_items, prices, expected):
    assert shop_with_items.calculate_total(prices) == expected


@pytest.mark.parametrize(
    "total, discount, expected",
    [
        (100, 25, 75),
        (50, 50, 25)
    ],
)
def test_apply_discount(my_shop, total, discount, expected):
    assert my_shop.apply_discount(total, discount) == expected


@pytest.mark.parametrize(
    "total, discount",
    [
        (100, -10),  # Отрицательная скидка
        (100, 110),  # Скидка больше 100%
    ],
)
def test_apply_discount_invalid(my_shop, total, discount):
    """Тестирование выброса исключения при некорректных значениях скидки."""
    with pytest.raises(ValueError):
        my_shop.apply_discount(total, discount)
