# Replace Parameter With Method Call
basePrice = quantity * itemPrice
finalPrice = discountedPrice(basePrice, self.getSeasonalDiscount(), self.getFees())
