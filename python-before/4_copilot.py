# Introduce Foreign Method
class Report:
    # ...
    def sendReport(self):
        nextDay = self.previousEnd.nextDay()
        # ...


class Date:
    # ...
    def nextDay(self):
        return Date(self.getYear(), self.getMonth(), self.getDate() + 1)
