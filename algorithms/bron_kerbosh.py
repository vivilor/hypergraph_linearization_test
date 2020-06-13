def are_adjacent(node_id_a, node_id_b, edges):
    for edge in edges:
        if node_id_a in edge.node_ids and node_id_b in edge.node_ids:
            return True

    return False


def get_node_neighbours(node_id, edges):
    neighbours = []

    for edge in edges:
        if node_id in edge.node_ids:
            neighbours.extend([
                n_id
                for n_id in edge.node_ids
                if n_id is not node_id and n_id not in neighbours
            ])

    return neighbours


def find_all_cliques(nodes, edges):
    """
    Implements Bron-Kerbosch algorithm, Version 2
    """

    node_ids = [node.id for node in nodes]

    cliques = []
    stack = []
    nd = None
    disc_num = len(node_ids)

    search_node = (set(), set(node_ids), set(), nd, disc_num)

    stack.append(search_node)

    while len(stack):
        (c_compsub, c_candidates, c_not, c_nd, c_disc_num) = stack.pop()

        if not len(c_candidates) and not len(c_not):
            if len(c_compsub) > 1:
                cliques.append(c_compsub)
                continue

        for u in list(c_candidates):
            if c_nd is None or not are_adjacent(u, c_nd, edges):
                c_candidates.remove(u)
                n_u = get_node_neighbours(u, edges)
                new_compsub = set(c_compsub)
                new_compsub.add(u)
                new_candidates = set(c_candidates.intersection(n_u))
                new_not = set(c_not.intersection(n_u))

                if c_nd is not None:
                    if c_nd in new_not:
                        new_disc_num = c_disc_num - 1

                        if new_disc_num > 0:
                            new_search_node = (new_compsub, new_candidates, new_not, c_nd, new_disc_num)
                            stack.append(new_search_node)
                    else:
                        new_disc_num = len(node_ids)
                        new_nd = c_nd

                        for candidate_nd in new_not:
                            candidate_disc_num =\
                                len(new_candidates) -\
                                len(new_candidates.intersection(get_node_neighbours(candidate_nd, edges)))

                            if candidate_disc_num < new_disc_num:
                                new_disc_num = candidate_disc_num
                                new_nd = candidate_nd

                        new_search_node = (new_compsub, new_candidates, new_not, new_nd, new_disc_num)
                        stack.append(new_search_node)
                else:
                    new_search_node = (new_compsub, new_candidates, new_not, c_nd, c_disc_num)
                    stack.append(new_search_node)

                c_not.add(u)
                new_disc_num = 0

                for x in c_candidates:
                    if not are_adjacent(x, u, edges):
                        new_disc_num += 1

                if c_disc_num > new_disc_num > 0:
                    new1_search_node = (c_compsub, c_candidates, c_not, u, new_disc_num)
                    stack.append(new1_search_node)
                else:
                    new1_search_node = (c_compsub, c_candidates, c_not, c_nd, c_disc_num)
                    stack.append(new1_search_node)

    return cliques
