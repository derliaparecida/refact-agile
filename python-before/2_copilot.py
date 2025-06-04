# Introduce Assertion
def getExpenseLimit(self):
    assert self.expenseLimit != NULL_EXPENSE or self.primaryProject is not None
    return (
        self.expenseLimit
        if self.expenseLimit != NULL_EXPENSE
        else self.primaryProject.getMemberExpenseLimit()
    )
