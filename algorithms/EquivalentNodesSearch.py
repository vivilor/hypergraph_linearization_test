class EquivalentNodesClassSearch:
    def __init__(self, node_ids):
        self.is_failed = False
        self.protected_edges = []
        self.node_ids: [str] = node_ids
        self.finished_node_ids = []
        self.paths = {}

        for node_id in node_ids:
            self.paths[node_id] = []

    def set_finished_node_id(self, node_id):
        if node_id not in self.node_ids:
            raise Exception('unknown node {}'.format(node_id))

        self.node_ids.remove(node_id)
        self.finished_node_ids.append(node_id)

        return self
