from collections import Set
from typing import List, Tuple

from algorithms.EquivalentNodesSearch import EquivalentNodesClassSearch
from algorithms.Edge import HyperEdge


def get_next_edges(edges: [HyperEdge], end_node_ids: [str], denied_node_ids=None):
    next_edges = []

    for edge in edges:
        has_denied = False
        has_end_node = False

        for node_id in edge.node_ids:
            if denied_node_ids is not None and node_id in denied_node_ids:
                has_denied = True
                break
            if node_id in end_node_ids:
                has_end_node = True

        if not has_denied and has_end_node:
            next_edges.append(edge)

    return next_edges


def try_to_find_first_path(search: EquivalentNodesClassSearch):
    active_node_ids = search.node_ids - search.finished_node_ids

    for active_node_id in active_node_ids:
        active_node_paths = search.paths[active_node_id]
        indexed_last_edges = enumerate(set([path[-1] for path in active_node_paths]))
        other_active_node_ids = search.node_ids - search.finished_node_ids - {active_node_id}

        for other_active_node_id in other_active_node_ids:
            other_active_node_paths = search.paths[other_active_node_id]

            for other_active_node_path in other_active_node_paths:
                for (i, last_edge) in indexed_last_edges:
                    for other_active_node_path_edge in other_active_node_path:
                        if last_edge == other_active_node_path_edge:
                            search.protected_edges = active_node_paths[i][:-1]
                            search.protected_edges.extend(other_active_node_path)
                            search.finished_node_ids += {active_node_id, other_active_node_id}
                            return


def try_to_protect_edges(search: EquivalentNodesClassSearch):
    if search.protected_edges is None:
        try_to_find_first_path(search)

        if search.protected_edges is None:
            return

    active_node_ids = search.node_ids - search.finished_node_ids

    for active_node_id in active_node_ids:
        active_node_paths = search.paths[active_node_id]
        indexed_last_edges = enumerate(set([path[-1] for path in active_node_paths]))

        for (i, last_edge) in indexed_last_edges:
            for protected_edge in search.protected_edges:
                if protected_edge == last_edge:
                    search.protected_edges.extend(active_node_paths[i][:-1])
                    search.finished_node_ids += {active_node_id}


def find_max_edge_order(edges: [HyperEdge]) -> int:
    max_order = 0

    for edge in edges:
        edge_order = get_edge_order(edge)
        if edge_order > max_order:
            max_order = edge_order

    return max_order


def get_edge_order(edge: HyperEdge) -> int:
    return len(edge.node_ids)


def get_edges_with_lesser_order(edges: List[HyperEdge], order: int) -> List[Tuple[int, HyperEdge]]:
    lesser_order_edges = []

    for i, edge in enumerate(edges):
        edge_order = get_edge_order(edge)

        if edge_order < order:
            lesser_order_edges.append((i, edge))

    return lesser_order_edges


def get_indexed_edges_with_order(edges: List[HyperEdge], order: int):
    edge_tuples = []

    for i, edge in enumerate(edges):
        edge_order = get_edge_order(edge)

        if edge_order is order:
            edge_tuples.append((i, edge))

    return edge_tuples


def has_all_vertices(testing_edge: HyperEdge, target_edge: HyperEdge):
    for testing_edge_node in testing_edge.node_ids:
        target_edge_node_ids = [v.id for v in target_edge.node_ids]

        if testing_edge_node.id not in target_edge_node_ids:
            return False

    return True


def find_sub_edge_indexes_set(edges: List[HyperEdge], super_edge: HyperEdge) -> Set:
    sub_edge_indexes = set()

    sub_edges_tuples = get_edges_with_lesser_order(edges, get_edge_order(super_edge))

    # print('\t\t\t super edge', super_edge)
    # print('\t\t\t found sub edges', [vertices_list_to_str(edge) for i, edge in sub_edges_tuples])

    for i, sub_edge in sub_edges_tuples:
        if has_all_vertices(sub_edge, super_edge):
            sub_edge_indexes += {i}

    # print('\t\t\t found sub edge indexes', sub_edge_indexes)

    return sub_edge_indexes


def vertices_list_to_str(edge: HyperEdge) -> str:
    return ','.join([node_id for node_id in edge.node_ids])


def update_denied(denied_edge_ids: List[str], edge: HyperEdge):
    for edge_node_id in edge.node_ids:
        if edge_node_id not in denied_edge_ids:
            denied_edge_ids.append(edge_node_id)


def get_end_node_ids(path: [HyperEdge], start_node_id):
    end_nodes_ids = []

    if not len(path):
        # print('\tfound ends', [])
        return []

    curr_node_ids = path[-1].node_ids
    prev_node_ids = path[-2].node_ids if len(path) > 2 else [start_node_id]

    for curr_node_id in curr_node_ids:
        if curr_node_id not in prev_node_ids:
            end_nodes_ids.append(curr_node_id)

    # print('\tfound ends', end_nodes)
    return end_nodes_ids


def protect_edges_by_equiv_nodes_criteria_step(edges: List[HyperEdge],
                                               searches: List[EquivalentNodesClassSearch]) -> Tuple[bool, bool]:
    all_searches_finished = True
    all_searches_failed = True

    for search in searches:
        if search.is_failed:
            all_searches_failed = all_searches_failed and True
            continue

        all_searches_failed = all_searches_failed and False

        try_to_protect_edges(search)

        if search.is_finished():
            all_searches_finished = all_searches_finished and True
            continue

        all_searches_finished = all_searches_finished and False

        active_node_ids = search.node_ids - search.finished_node_ids

        search_failed = False

        for active_node_id in active_node_ids:
            paths = search.paths[active_node_id]
            denied_node_ids = search.denied_node_ids[active_node_id]

            path_indexes_to_remove = []
            new_paths = []

            if not len(paths):
                new_paths = [[next_edge] for next_edge in get_next_edges(edges, [active_node_id])]
            else:
                for (path_index, path) in enumerate(paths):
                    end_node_ids = get_end_node_ids(path, active_node_id)
                    denied_node_ids = [
                        denied_node_id
                        for denied_node_id in denied_node_ids
                        if denied_node_id not in end_node_ids
                    ]
                    next_edges = get_next_edges(edges, end_node_ids, denied_node_ids)

                    if not len(next_edges):
                        path_indexes_to_remove.append(path_index)
                    else:
                        first_next_edge = next_edges[0]

                        for next_edge in next_edges[1:]:
                            new_path = path.copy()
                            new_path.append(next_edge)
                            new_paths.append(new_path)

                        path.append(first_next_edge)

            if len(path_indexes_to_remove):
                paths = [paths[i] for i in range(len(paths)) if i not in path_indexes_to_remove]
                path_indexes_to_remove = []

            if not len(new_paths):
                search_failed = True
                break

            for new_path in new_paths:
                update_denied(denied_node_ids, new_path[-1])

            paths.extend(new_paths)

            last_edges = [path[-1] for path in paths]

            max_edge_order = find_max_edge_order(last_edges)

            if max_edge_order > 2:
                # print('\tmax edge order', max_edge_order)

                for i in range(max_edge_order):
                    order = max_edge_order - i

                    # print('\t\tcurrent order', order)
                    # print('\t\tedges with current order', super_edges)

                    indexes_super_edges = get_indexed_edges_with_order(last_edges, order)

                    for (_, super_edge) in indexes_super_edges:
                        sub_edge_indexes = find_sub_edge_indexes_set(last_edges, super_edge)

                        path_indexes_to_remove.extend(sub_edge_indexes)
                        print(path_indexes_to_remove)
                        path_indexes_to_remove = list(set(path_indexes_to_remove))

                    # print('\t\tsub edge indexes', path_indexes_to_remove)

            search.paths[active_node_id] = paths
            search.denied_node_ids[active_node_id] = denied_node_ids

        search.is_failed = search_failed

    return all_searches_failed, all_searches_finished
