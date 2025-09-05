from skymel.commonUtils import maybe_get_length_of_object
from skymel.commonValidators import CommonValidators


class CommonGraphAlgorithms(object):
    def __init__(self):
        raise RuntimeError('CommonGraphAlgorithms cannot be instantiated')

    @staticmethod
    def __sort_mixed_list_of_int_and_string(list_of_int_and_string):
        new_tuples_list = []
        for x in list_of_int_and_string:
            new_tuples_list.append((str(x), x))
        new_tuples_list.sort()
        output = [x[1] for x in new_tuples_list]
        return output

    @staticmethod
    def remove_duplicate_node_ids_from_list(list_of_node_ids: list[str] | list[int], sort_returned_list: bool = True) -> \
            list[str]:
        if list_of_node_ids is None or not isinstance(list_of_node_ids, list):
            return []
        if len(list_of_node_ids) == 0:
            return []
        deduplicated_list_of_node_ids = list(set(list_of_node_ids))
        if sort_returned_list:
            deduplicated_list_of_node_ids = CommonGraphAlgorithms.__sort_mixed_list_of_int_and_string(
                deduplicated_list_of_node_ids)
        return deduplicated_list_of_node_ids

    @staticmethod
    def is_empty_graph(graph_dict: dict) -> bool:
        if graph_dict is None or not isinstance(graph_dict, dict):
            return True
        if len(graph_dict.keys()) == 0:
            return True
        return False

    @staticmethod
    def is_valid_list_or_set_of_child_node_ids(sub_graph: list[str] | set[str] | None) -> bool:
        if isinstance(sub_graph, set):
            return True
        if isinstance(sub_graph, list):
            return True
        return False

    @staticmethod
    def is_empty_list_or_set_of_child_node_ids(sub_graph: list[str] | set[str] | None) -> bool:
        if sub_graph is None:
            return True
        if isinstance(sub_graph, set) and len(sub_graph) == 0:
            return True
        if isinstance(sub_graph, list) and len(sub_graph) == 0:
            return True
        return False

    @staticmethod
    def is_valid_node_id(node_id: str | int) -> bool:
        if node_id is None or not (isinstance(node_id, str) or isinstance(node_id, int)):
            return False
        return True

    @staticmethod
    def is_node_in_graph(graph_dict: dict, node_id: str | int) -> bool:
        if CommonGraphAlgorithms.is_empty_graph(graph_dict) or not CommonGraphAlgorithms.is_valid_node_id(node_id):
            return False
        return node_id in graph_dict

    @staticmethod
    def is_parent_node(graph_dict: dict, potential_parent_node_id: str | int,
                       potential_child_node_id: str | int) -> bool:

        if not CommonGraphAlgorithms.is_node_in_graph(graph_dict,
                                                      potential_parent_node_id) or not CommonGraphAlgorithms.is_node_in_graph(
            graph_dict, potential_child_node_id):
            return False
        child_tree = graph_dict[potential_parent_node_id]
        if child_tree is None or not isinstance(child_tree, dict):
            return False
        return potential_child_node_id in child_tree

    @staticmethod
    def is_child_node(graph_dict: dict, potential_child_node_id: str | int,
                      potential_parent_node_id: str | int, ) -> bool:
        return CommonGraphAlgorithms.is_parent_node(graph_dict, potential_parent_node_id, potential_child_node_id)

    @staticmethod
    def get_list_of_node_ids_in_graph(graph_dict: dict) -> list[str]:
        if CommonGraphAlgorithms.is_empty_graph(graph_dict):
            return []
        return list(graph_dict.keys())

    @staticmethod
    def get_list_of_children_node_ids(graph_dict: dict, query_node_id: str | int) -> list[str]:
        if not CommonGraphAlgorithms.is_node_in_graph(graph_dict, query_node_id):
            return []
        list_or_set_of_child_node_ids = graph_dict[query_node_id]
        if CommonGraphAlgorithms.is_empty_list_or_set_of_child_node_ids(list_or_set_of_child_node_ids):
            return []
        return CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(list(list_or_set_of_child_node_ids),
                                                                         sort_returned_list=False)

    @staticmethod
    def get_list_of_parent_node_ids(graph_dict: dict, query_node_id: str | int) -> list[str]:
        if not CommonGraphAlgorithms.is_node_in_graph(graph_dict, query_node_id):
            return []
        parent_node_ids = []
        for node_id in graph_dict:
            list_or_set_of_child_node_ids = graph_dict[node_id]
            if CommonGraphAlgorithms.is_empty_list_or_set_of_child_node_ids(list_or_set_of_child_node_ids):
                continue
            if query_node_id in list_or_set_of_child_node_ids:
                parent_node_ids.append(node_id)
        return CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(parent_node_ids, sort_returned_list=False)

    @staticmethod
    def get_list_of_sibling_node_ids(graph_dict: dict, query_node_id: str | int) -> list[str]:
        if not CommonGraphAlgorithms.is_node_in_graph(graph_dict, query_node_id):
            return []
        parent_node_ids = CommonGraphAlgorithms.get_list_of_parent_node_ids(graph_dict, query_node_id)
        if len(parent_node_ids) == 0:
            return []
        sibling_node_ids = set()
        for node_id in parent_node_ids:
            list_or_set_of_child_node_ids = graph_dict[node_id]
            if CommonGraphAlgorithms.is_empty_list_or_set_of_child_node_ids(list_or_set_of_child_node_ids):
                continue
            sibling_node_ids += set(list_or_set_of_child_node_ids)
        if len(sibling_node_ids) == 0:
            return []
        sibling_node_ids.remove(query_node_id)
        return CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(list(sibling_node_ids),
                                                                         sort_returned_list=False)

    @staticmethod
    def get_list_of_leaf_node_ids(graph_dict: dict) -> list[str]:
        if CommonGraphAlgorithms.is_empty_graph(graph_dict):
            return []
        leaf_node_ids = set()
        for node_id in graph_dict:
            list_or_set_of_child_node_ids = graph_dict[node_id]
            if CommonGraphAlgorithms.is_empty_list_or_set_of_child_node_ids(list_or_set_of_child_node_ids):
                leaf_node_ids.add(node_id)
        return CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(list(leaf_node_ids), sort_returned_list=False)

    @staticmethod
    def get_list_of_root_node_ids(graph_dict: dict) -> list[str]:
        if CommonGraphAlgorithms.is_empty_graph(graph_dict):
            return []
        root_node_ids = set()
        for node_id in graph_dict:
            parent_node_ids_list = CommonGraphAlgorithms.get_list_of_parent_node_ids(graph_dict, node_id)
            if len(parent_node_ids_list) == 0:
                root_node_ids.add(node_id)
        return CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(list(root_node_ids), sort_returned_list=False)

    @staticmethod
    def __return_callable_result(callable_method: callable(...), *args, **kwargs):
        if CommonValidators.is_callable_method(callable_method):
            return callable_method(*args, **kwargs)
        return None

    @staticmethod
    def depth_first_search(graph_dict, start_node_ids_list: list[str] | list[int] | None = None,
                           stop_search_check_method: callable(...) = None,
                           stop_searching_children_check_method: callable(...) = None,
                           on_search_stop_processing_method: callable(...) = None) -> any:
        """

        :param graph_dict: The graph to search, represented as a dictionary such as ``{'a':['b', 'c'], 'b':['d'],
        'c':['e'], 'd': [], 'e': []}``

        :param start_node_ids_list: A list of nodeIds from which to start the Depth-First Search. If null, we find the
        roots of the current graph and use them as startNodeIds.

        :param stop_search_check_method: It's a method that takes as inputs: `current_node_id, current_visitation_depth,
        visited_node_ids_to_first_visitation_depth_map,to_visit_nodes_and_visitation_depth_stack,
        current_visitation_path`.
        The method must return true or false. If true is returned, the entire search is stopped.

        :param stop_searching_children_check_method: It's a method that takes as inputs: `current_node_id,
        currentNodeVisitationDepth,visitedNodeIdToFirstVisitDepthMap, toVisitNodesAndVisitationDepthStackArray,
        currentVisitationPath`. The method must return true or false. If true is returned, the children of the
        `currentNodeId` are not added to the search stack.

        :param on_search_stop_processing_method:  A method to compute the final result on stop criteria being met.
        It's provided the following inputs :
        `     current_node_id,
              current_visitation_depth,
              visited_node_ids_to_first_visitation_depth_map,
              to_visit_nodes_and_visitation_depth_stack,
              current_visitation_path`

        :return: Returns the result of `on_search_stop_processing_method` if it is not null. Else it returns nothing.
        """
        if CommonValidators.is_empty(graph_dict):
            return None
        if CommonValidators.is_empty(start_node_ids_list):
            start_node_ids_list = CommonGraphAlgorithms.get_list_of_root_node_ids(graph_dict)
        if maybe_get_length_of_object(start_node_ids_list) == 0:
            return None
        visited_node_ids_to_first_visitation_depth_map = {}
        to_visit_nodes_and_visitation_depth_stack = []
        for node_id in start_node_ids_list:
            if not CommonGraphAlgorithms.is_node_in_graph(graph_dict=graph_dict, node_id=node_id):
                continue
            to_visit_nodes_and_visitation_depth_stack.append((node_id, 0))
        if len(to_visit_nodes_and_visitation_depth_stack) == 0:
            return None

        current_visitation_path = []
        current_visitation_path_depths = []

        while len(to_visit_nodes_and_visitation_depth_stack) > 0:
            current_node_id, current_visitation_depth = to_visit_nodes_and_visitation_depth_stack.pop()
            if current_visitation_depth == 0:
                current_visitation_path_depths = [0]
                current_visitation_path = [current_node_id]
            else:
                while current_visitation_path_depths[-1] >= current_visitation_depth:
                    current_visitation_path.pop()
                    current_visitation_path_depths.pop()
                current_visitation_path_depths.append(current_visitation_depth)
                current_visitation_path.append(current_node_id)
            if CommonValidators.is_callable_method(stop_search_check_method) and stop_search_check_method(
                    current_node_id, current_visitation_depth, visited_node_ids_to_first_visitation_depth_map,
                    to_visit_nodes_and_visitation_depth_stack, current_visitation_path):
                return CommonGraphAlgorithms.__return_callable_result(on_search_stop_processing_method,
                                                                      current_node_id,
                                                                      current_visitation_depth,
                                                                      visited_node_ids_to_first_visitation_depth_map,
                                                                      to_visit_nodes_and_visitation_depth_stack,
                                                                      current_visitation_path
                                                                      )
            if current_node_id in visited_node_ids_to_first_visitation_depth_map:
                continue
            visited_node_ids_to_first_visitation_depth_map[current_node_id] = current_visitation_depth
            if CommonValidators.is_callable_method(
                    stop_searching_children_check_method) and stop_searching_children_check_method(
                current_node_id, current_visitation_depth, visited_node_ids_to_first_visitation_depth_map,
                to_visit_nodes_and_visitation_depth_stack, current_visitation_path):
                continue
            children_of_current_node = CommonGraphAlgorithms.get_list_of_children_node_ids(graph_dict=graph_dict,
                                                                                           query_node_id=current_node_id)
            for child_node_id in children_of_current_node:
                to_visit_nodes_and_visitation_depth_stack.append((child_node_id, current_visitation_depth + 1))

        return CommonGraphAlgorithms.__return_callable_result(on_search_stop_processing_method, None, None,
                                                              visited_node_ids_to_first_visitation_depth_map,
                                                              to_visit_nodes_and_visitation_depth_stack,
                                                              current_visitation_path, )

    @staticmethod
    def is_cyclic_graph(graph_dict):
        if CommonValidators.is_empty(graph_dict):
            return False

        def stop_search_check_method(current_node_id,
                                     current_visitation_depth,
                                     visited_node_ids_to_first_visitation_depth_map,
                                     to_visit_nodes_and_visitation_depth_stack,
                                     current_visitation_path):
            if current_node_id not in visited_node_ids_to_first_visitation_depth_map:
                return False
            for visitation_path_node in current_visitation_path:
                if visitation_path_node == current_node_id:
                    return True
            return False

        def on_search_stop_processing_method(current_node_id,
                                             current_visitation_depth,
                                             visited_node_ids_to_first_visitation_depth_map,
                                             to_visit_nodes_and_visitation_depth_stack,
                                             current_visitation_path):
            if current_node_id not in visited_node_ids_to_first_visitation_depth_map:
                return False
            for visitation_path_node in current_visitation_path[:-2]:
                if visitation_path_node == current_node_id:
                    return True
            return False

        result = CommonGraphAlgorithms.depth_first_search(graph_dict=graph_dict,
                                                          stop_search_check_method=stop_search_check_method,
                                                          on_search_stop_processing_method=on_search_stop_processing_method
                                                          )
        if result not in {True, False}:
            return True
        return result

    @staticmethod
    def get_list_of_all_edges_in_graph(graph_dict):
        if CommonValidators.is_empty(graph_dict):
            return []
        output = []
        for node_id in graph_dict:
            child_node_ids = CommonGraphAlgorithms.get_list_of_children_node_ids(graph_dict=graph_dict,
                                                                                 query_node_id=node_id)
            for child_node_id in child_node_ids:
                output.append((node_id, child_node_id))
        return output

    @staticmethod
    def has_inbound_edges_to_node_in_edge_list(edge_list, node_id):
        for edge in edge_list:
            if edge[1] == node_id:
                return True
        return False

    @staticmethod
    def get_edge_index_in_edge_list(edge_list, edge):
        try:
            return edge_list.index(edge)
        except ValueError:
            return -1

    @staticmethod
    def topological_sort(graph_dict):
        if CommonValidators.is_empty(graph_dict):
            return None
        if CommonGraphAlgorithms.is_cyclic_graph(graph_dict):
            return None
        list_of_all_edges_in_graph = CommonGraphAlgorithms.get_list_of_all_edges_in_graph(graph_dict)
        sorted_nodes = []
        to_visit_nodes = CommonGraphAlgorithms.get_list_of_root_node_ids(graph_dict)
        while len(to_visit_nodes) > 0:
            current_node_id = to_visit_nodes.pop()
            sorted_nodes.append(current_node_id)
            children_of_current_node = CommonGraphAlgorithms.get_list_of_children_node_ids(graph_dict=graph_dict,
                                                                                           query_node_id=current_node_id)
            for child_node_id in children_of_current_node:
                index_of_child_node_edge_in_graph = CommonGraphAlgorithms.get_edge_index_in_edge_list(
                    edge_list=list_of_all_edges_in_graph,
                    edge=(current_node_id, child_node_id))
                if index_of_child_node_edge_in_graph != - 1:
                    list_of_all_edges_in_graph.pop(index_of_child_node_edge_in_graph)
                    if not CommonGraphAlgorithms.has_inbound_edges_to_node_in_edge_list(
                            edge_list=list_of_all_edges_in_graph, node_id=child_node_id):
                        to_visit_nodes.append(child_node_id)
        return sorted_nodes

    @staticmethod
    def get_all_nodes_encountered_while_traversing_directed_acyclic_graph(graph_dict, source_node_id,
                                                                          destination_node_id,
                                                                          include_source_node_id=True,
                                                                          include_destination_node_id=True):

        if CommonValidators.is_empty(graph_dict):
            return None
        if CommonGraphAlgorithms.is_cyclic_graph(graph_dict) or not CommonGraphAlgorithms.is_node_in_graph(graph_dict,
                                                                                                           source_node_id) or not CommonGraphAlgorithms.is_node_in_graph(
                graph_dict, destination_node_id):
            return None
        if source_node_id == destination_node_id and CommonGraphAlgorithms.is_node_in_graph(graph_dict=graph_dict,
                                                                                            node_id=source_node_id):
            if include_source_node_id and include_destination_node_id:
                return [source_node_id]
            return []
        all_encountered_nodes = set()
        nodes_encountered_on_connected_paths = set()
        stop_repeating_dfs = False
        last_visitation_path = []

        def nodes_array_equals(a, b):
            if len(a) != len(b):
                return False
            for x, y in zip(a, b):
                if x != y:
                    return False
            return True

        def stop_search_check_method(current_node_id,
                                     current_visitation_depth,
                                     visited_node_ids_to_first_visitation_depth_map,
                                     to_visit_nodes_and_visitation_depth_stack,
                                     current_visitation_path, ):
            return current_node_id == destination_node_id

        def stop_searching_children_check_method(current_node_id, current_visitation_depth,
                                                 visited_node_ids_to_first_visitation_depth_map,
                                                 to_visit_nodes_and_visitation_depth_stack,
                                                 current_visitation_path, ):
            return current_node_id in all_encountered_nodes

        def on_search_stop_processing_method(current_node_id,
                                             current_visitation_depth,
                                             visited_node_ids_to_first_visitation_depth_map,
                                             to_visit_nodes_and_visitation_depth_stack,
                                             current_visitation_path):
            nonlocal stop_repeating_dfs
            nonlocal last_visitation_path
            nonlocal nodes_encountered_on_connected_paths
            nonlocal all_encountered_nodes
            if current_node_id is None or nodes_array_equals(current_visitation_path, last_visitation_path):
                stop_repeating_dfs = True
            if current_node_id == destination_node_id:
                last_visitation_path = current_visitation_path
                for node_id in current_visitation_path:
                    if node_id == source_node_id and not include_source_node_id:
                        continue
                    if node_id == destination_node_id and not include_destination_node_id:
                        continue
                    nodes_encountered_on_connected_paths.add(node_id)
            for node_id in visited_node_ids_to_first_visitation_depth_map:
                if node_id == source_node_id or node_id == destination_node_id:
                    continue
                all_encountered_nodes.add(node_id)

        while not stop_repeating_dfs:
            CommonGraphAlgorithms.depth_first_search(graph_dict=graph_dict, start_node_ids_list=[source_node_id],
                                                     stop_search_check_method=stop_search_check_method,
                                                     stop_searching_children_check_method=stop_searching_children_check_method,
                                                     on_search_stop_processing_method=on_search_stop_processing_method)
        result = list(nodes_encountered_on_connected_paths) if not CommonValidators.is_empty(
            nodes_encountered_on_connected_paths) else []
        return result

    @staticmethod
    def get_sub_graph_node_ids(graph_dict, source_node_ids, destination_node_ids, include_source_node_ids=True, include_destination_node_ids=True):
        sub_graph_nodes = set()


acyclic_graph_dict = {'a': ['b', 'c'], 'b': ['d'], 'c': ['e', 'd'], 'd': [], 'e': []}
cyclic_graph_dict = {'a': ['b', 'c'], 'b': ['d'], 'c': ['e'], 'd': ['a'], 'e': []}

print(CommonGraphAlgorithms.is_cyclic_graph(acyclic_graph_dict))
print(CommonGraphAlgorithms.is_cyclic_graph(cyclic_graph_dict))
print([(1, 2), (2, 3), (3, 4)].index((1, 2)))
print(CommonGraphAlgorithms.topological_sort(acyclic_graph_dict))

# elsa = 1
#
#
# def m():
#     nonlocal elsa
#     elsa = 2
#
#
# print(elsa)
# print(m())
# print(elsa)
print(CommonGraphAlgorithms.get_all_nodes_encountered_while_traversing_directed_acyclic_graph(acyclic_graph_dict, 'a', 'd'))
