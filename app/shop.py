class Shop:
    def __init__(self):
        self.cart = {}

    def add_to_cart(self, item, quantity=1):
        """Добавляет товар в корзину."""
        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        self.cart[item] = self.cart.get(item, 0) + quantity
        return self.cart

    def calculate_total(self, prices):
        """Рассчитывает общую стоимость корзины."""
        total = 0
        for item, quantity in self.cart.items():
            total += prices.get(item, 0) * quantity
        return total

    def apply_discount(self, total, discount):
        """Применяет скидку к общей стоимости."""
        if discount < 0 or discount > 100:
            raise ValueError("Скидка должна быть от 0 до 100")
        return total - (total * discount / 100)
