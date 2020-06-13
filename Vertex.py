class Vertex:

    def __init__(self, id:str=None, other=None):
        if other:
            self.id = other.id
        elif id:
            self.id = str(id)
        else:
            raise Exception("ID or other must be provided")

    def getId(self):
        return self.id

    def setId(self, new_id:str) -> None:
        new_id = new_id.strip()
        self.id = new_id

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def  __ne__(self, other) -> bool:
        return  self.id != other.id

    def __add__(self, other):
        return Vertex(self.id + '+' + other.id)

    def __str__(self):
        return "'%s'" % self.id

    def __hash__(self):
        return hash(self.id)