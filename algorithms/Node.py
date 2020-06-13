# noinspection PyShadowingBuiltins
class Node:
    def __init__(self, id: str = None):
        self.id = str(id)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __ne__(self, other) -> bool:
        return self.id != other.id

    def __add__(self, other):
        return Node(self.id + '+' + other.id)

    def __str__(self):
        return "'%s'" % self.id

    def __hash__(self):
        return hash(self.id)
