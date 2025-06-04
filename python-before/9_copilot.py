# Replace Magic Number With Symbolic Constant
GRAVITY = 9.81


def potentialEnergy(mass, height):
    return mass * height * GRAVITY
