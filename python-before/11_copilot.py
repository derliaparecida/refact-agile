# Substitute Algorithm
def foundPerson(people):
    for name in ["Don", "John", "Kent"]:
        if name in people:
            return name
    return ""
