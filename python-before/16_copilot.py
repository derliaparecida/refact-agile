# Decompose Conditional
def summerCharge(quantity, summerRate):
    return quantity * summerRate


def winterCharge(quantity, winterRate, winterServiceCharge):
    return quantity * winterRate + winterServiceCharge


def calculateCharge(date, quantity, summerRate, winterRate, winterServiceCharge):
    if date.before(SUMMER_START) or date.after(SUMMER_END):
        charge = winterCharge(quantity, winterRate, winterServiceCharge)
    else:
        charge = summerCharge(quantity, summerRate)
    return charge
