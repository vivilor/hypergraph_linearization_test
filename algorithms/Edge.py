from __future__ import annotations
from uuid import uuid4


class HyperEdge:
    def __init__(self, node_ids: [str]):
        self.id = str(uuid4())
        self.node_ids = node_ids

    def __str__(self):
        result = "(%s)" % (','.join(map(str, self.node_ids)))
        return result

    def __eq__(self, other: HyperEdge):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)