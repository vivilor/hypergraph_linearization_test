from __future__ import annotations
from enum import Enum, auto
from uuid import uuid4

from Vertex import Vertex


class HyperEdgeCrossingVariants(Enum):
    NOT_CROSSING = auto()
    CROSSING = auto()
    ONE_INSIDE_ANOTHER = auto()
    SAME = auto()


class HyperEdge:

    def __init__(self, *vertices, other: HyperEdge = None):
        self.id = str(uuid4())
        if other:
            self._copy_constructor(other)
        elif vertices:
            self.vertices = set(vertices)
        else:
            raise ValueError("Vertices set can't be empty")

    def _copy_constructor(self, other: HyperEdge):
        self.vertices = other.vertices

    def __str__(self):
        result = "(%s)" % (','.join(map(str, self.vertices)))
        return result

    def __eq__(self, other: HyperEdge):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def getId(self):
        return self.id

    def getVertices(self):
        return self.vertices

    def getDegree(self):
        return len(self.vertices)

    def getCrossingVariant(self, other: HyperEdge) -> HyperEdgeCrossingVariants:
        if self.vertices == other.vertices:
            return HyperEdgeCrossingVariants.SAME

        edge_crossing = self.vertices & other.vertices
        if not edge_crossing:
            return HyperEdgeCrossingVariants.NOT_CROSSING
        elif edge_crossing == self.vertices or edge_crossing == other.vertices:
            return HyperEdgeCrossingVariants.ONE_INSIDE_ANOTHER
        else:
            return HyperEdgeCrossingVariants.CROSSING

    def getCrossingDegree(self, other: HyperEdge) -> int:
        return len(self.vertices & other.vertices)

    def getChildIds(self):
        return {x.getId() for x in self.vertices}

    def isHyperedge(self):
        return self.getDegree() > 2

    def isSimpleEdge(self):
        return self.getDegree() == 2

    def addVertex(self, vertex: Vertex):
        self.vertices.add(vertex)

    def deleteVertex(self, vertex: Vertex):
        self.vertices -= {vertex}

    def renameVertex(self, old_id: str, new_id: str) -> None:
        # TODO make it work considering that self.vertices is set
        for vertex in self.vertices:
            if vertex.getId() == old_id:
                vertex.setId(new_id)
                return

    def compareByVertices(self, other: HyperEdge) -> bool:
        return self.getVertices() == other.getVertices()

    def replaceVertex(self, old: Vertex, new: Vertex):
        self.deleteVertex(old)
        self.addVertex(new)