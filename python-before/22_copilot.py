# Introduce Null Object
class NullCustomer:
    def getPlan(self):
        return BillingPlan.basic()


customer = customer or NullCustomer()
plan = customer.getPlan()
