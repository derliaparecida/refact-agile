# Replace Error Code With Exception
def getValueForPeriod(periodNumber):
    try:
        return values[periodNumber]
    except IndexError:
        raise Exception("Invalid period number")
