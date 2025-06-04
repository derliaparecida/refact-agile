# Replace Method With Method Object
class Order:
    # ...
    def price(self):
        return OrderPriceCalculator(self).compute()


class OrderPriceCalculator:
    def __init__(self, order):
        self.order = order

    def compute(self):
        primaryBasePrice = 0
        secondaryBasePrice = 0
        tertiaryBasePrice = 0
        # Perform long computation.
        pass
