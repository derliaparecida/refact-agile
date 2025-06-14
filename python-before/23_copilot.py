# Replace Conditional With Polymorphism
class Bird:
    def getSpeed(self):
        raise NotImplementedError()


class European(Bird):
    def getSpeed(self):
        return self.getBaseSpeed()


class African(Bird):
    def getSpeed(self):
        return self.getBaseSpeed() - self.getLoadFactor() * self.numberOfCoconuts


class NorwegianBlue(Bird):
    def getSpeed(self):
        return 0 if self.isNailed else self.getBaseSpeed(self.voltage)
