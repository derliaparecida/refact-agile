# Extract Method
def printOwing(self):
    self.printBanner()
    self.printDetails()


def printDetails(self):
    print("name:", self.name)
    print("amount:", self.getOutstanding())
