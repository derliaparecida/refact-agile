# Replace Temp With Query
def calculateTotal():
    if quantity * itemPrice > 1000:
        return quantity * itemPrice * 0.95
    else:
        return quantity * itemPrice * 0.98
