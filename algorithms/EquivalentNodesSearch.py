class EquivalentNodesClassSearch:
    def __init__(self, node_ids):
        self.is_failed = False
        self.protected_edges = None
        self.denied_node_ids = {}
        self.node_ids: set = node_ids
        self.finished_node_ids: set = set()
        self.paths = {}

        for node_id in node_ids:
            self.paths[node_id] = []
            self.denied_node_ids[node_id] = []

    def is_finished(self):
        return len(self.node_ids) == len(self.finished_node_ids)