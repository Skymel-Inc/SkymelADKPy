import time
from typing import Dict, List, Optional, Set, Any, Union
from .commonValidators import CommonValidators
from .commonHashUtils import CommonHashUtils
from .commonGraphAlgorithms import CommonGraphAlgorithms
from .skymelECGraphUtils import SkymelECGraphUtils
from .skymelECGraphNode import SkymelECGraphNode


class SkymelECGraph:
    def __init__(self, initialization_config: Dict):
        """
        Initialize a SkymelECGraph instance.
        
        Args:
            initialization_config: Configuration dictionary for graph initialization
        """
        self.node_id_to_object = {}
        self.initialization_config = initialization_config
        
        # Extract graph ID or generate one
        graph_id = None
        if (CommonValidators.is_non_empty_dict_and_has_key(initialization_config, 'graphId') and 
            CommonValidators.is_non_empty_string(initialization_config['graphId'])):
            graph_id = initialization_config['graphId']
        else:
            graph_id = CommonHashUtils.generate_unique_id()
        
        # Set external input names
        if (CommonValidators.is_non_empty_dict_and_has_key(initialization_config, 'externalInputNames') and 
            CommonValidators.is_list(initialization_config['externalInputNames'])):
            self.external_input_names = set(initialization_config['externalInputNames'])
        else:
            self.external_input_names = None
        
        # Set callbacks
        self.success_callback = None
        if (CommonValidators.is_non_empty_dict_and_has_key(initialization_config, 'successCallback') and 
            CommonValidators.is_callable_method(initialization_config['successCallback'])):
            self.success_callback = initialization_config['successCallback']
        
        self.error_callback = None
        if (CommonValidators.is_non_empty_dict_and_has_key(initialization_config, 'errorCallback') and 
            CommonValidators.is_callable_method(initialization_config['errorCallback'])):
            self.error_callback = initialization_config['errorCallback']
        
        self.graph_last_modified_timestamp = time.time() * 1000  # Convert to milliseconds
        self.set_graph_id(graph_id)
        
        # Execution-related attributes
        self.execution_graph_of_nodes = None
        self.external_input_names_to_values_dict = None
        self.graph_execution_config = None

    @staticmethod
    def is_skymel_ec_graph_node_instance(input_object) -> bool:
        """Check if input object is a SkymelECGraphNode instance."""
        return isinstance(input_object, SkymelECGraphNode)

    @staticmethod
    def is_skymel_ec_graph_instance(input_object) -> bool:
        """Check if input object is a SkymelECGraph instance."""
        return isinstance(input_object, SkymelECGraph)

    def set_graph_id(self, graph_id: str):
        """Set the graph ID."""
        self.graph_id = str(graph_id)

    def get_graph_id(self) -> str:
        """Get the graph ID."""
        return self.graph_id

    def get_graph_type(self) -> str:
        """Get the graph type."""
        return SkymelECGraphUtils.GRAPH_TYPE_BASE

    def get_type(self) -> str:
        """Get the graph type (alias for get_graph_type)."""
        return self.get_graph_type()

    def get_graph_last_modified_timestamp(self) -> float:
        """Get the last modified timestamp."""
        return self.graph_last_modified_timestamp

    def get_initialization_config(self) -> Dict:
        """Get the initialization configuration."""
        return self.initialization_config

    def add_node(self, node: Union[SkymelECGraphNode, Dict, 'SkymelECGraph']) -> Optional[str]:
        """
        Add a node to the graph.
        
        Args:
            node: Can be a SkymelECGraphNode, SkymelECGraph, or a dict with node config
            
        Returns:
            The node ID of the added node, or None for graphs
        """
        if self.is_skymel_ec_graph_instance(node):
            self.node_id_to_object[node.get_graph_id()] = node
            return None
        
        if not self.is_skymel_ec_graph_node_instance(node):
            node = SkymelECGraphNode(node)
        
        self.node_id_to_object[node.get_node_id()] = node
        self.graph_last_modified_timestamp = time.time() * 1000
        return node.get_node_id()

    def get_node_by_id(self, node_id: str) -> Optional[Union[SkymelECGraphNode, 'SkymelECGraph']]:
        """Get a node by its ID."""
        if CommonValidators.is_non_empty_string(node_id):
            return CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
                self.node_id_to_object, node_id, None
            )
        return None

    def get_list_of_all_node_ids(self) -> List[str]:
        """Get a list of all node IDs in the graph."""
        return list(self.node_id_to_object.keys())

    @staticmethod
    def is_graph_id_prefix_for_node_id(node_id: str) -> bool:
        """Check if node_id has a graph ID prefix pattern."""
        import re
        return bool(re.match(r"^(([a-zA-Z0-9_]+)\.)+([a-zA-Z0-9_]+)$", node_id))

    @staticmethod
    def get_graph_id_from_node_id_with_graph_id(node_id_with_graph_id: str) -> str:
        """Extract graph ID from a node ID with graph prefix."""
        parts = node_id_with_graph_id.split(".")
        return parts[0]

    @staticmethod
    def get_node_id_from_node_id_with_graph_id(node_id_with_graph_id: str) -> str:
        """Extract node ID from a node ID with graph prefix."""
        parts = node_id_with_graph_id.split(".")
        return parts[1]

    @staticmethod
    def remove_graph_id_from_output_name(output_name: str) -> str:
        """Remove graph ID prefix from output name."""
        parts = output_name.split(".")
        return ".".join(parts[1:])

    def contains_node_output_names(self, node_outputs: List[str]) -> bool:
        """Check if the graph contains all specified node output names."""
        if not CommonValidators.is_list(node_outputs) or len(node_outputs) == 0:
            return False
        
        external_inputs_to_graph = set() if CommonValidators.is_empty(self.external_input_names) else self.external_input_names
        
        for node_output_name in node_outputs:
            if node_output_name in external_inputs_to_graph:
                continue
            
            node_id = SkymelECGraphNode.get_node_id_from_output_name(node_output_name)
            
            if self.is_graph_id_prefix_for_node_id(node_id):
                input_graph_id = self.get_graph_id_from_node_id_with_graph_id(node_id)
                if input_graph_id not in self.node_id_to_object:
                    return False
                external_graph_output_name = self.remove_graph_id_from_output_name(node_output_name)
                return self.node_id_to_object[input_graph_id].contains_node_output_names([external_graph_output_name])
            
            if node_id not in self.node_id_to_object:
                return False
            
            if not self.node_id_to_object[node_id].contains_node_output_name(node_output_name):
                return False
        
        return True

    async def is_graph_valid(self) -> bool:
        """Check if the graph is valid (all dependencies are satisfied)."""
        set_of_dependencies = set()
        
        for node_id in self.node_id_to_object:
            node_obj = self.node_id_to_object[node_id]
            
            if self.is_skymel_ec_graph_instance(node_obj):
                is_external_graph_valid = await node_obj.is_graph_valid()
                if not is_external_graph_valid:
                    return False
                
                external_graph_node_ids = await node_obj.get_output_node_ids()
                if not CommonValidators.is_empty(external_graph_node_ids):
                    external_graph_id = node_obj.get_graph_id()
                    for ext_node_id in external_graph_node_ids:
                        set_of_dependencies.add(f"{external_graph_id}.{ext_node_id}")
                continue
            
            if self.is_skymel_ec_graph_node_instance(node_obj) and not node_obj.is_node_valid(self):
                return False
            
            dependent_nodes = node_obj.get_node_ids_from_which_this_node_derives_inputs()
            set_of_dependencies.update(dependent_nodes)
        
        # Build available node IDs
        available_graph_node_ids = set()
        for node_id in self.node_id_to_object:
            node_obj = self.node_id_to_object[node_id]
            
            if self.is_skymel_ec_graph_instance(node_obj):
                external_graph_node_ids = await node_obj.get_output_node_ids()
                if not CommonValidators.is_empty(external_graph_node_ids):
                    external_graph_id = node_obj.get_graph_id()
                    for ext_node_id in external_graph_node_ids:
                        available_graph_node_ids.add(f"{external_graph_id}.{ext_node_id}")
                continue
            
            available_graph_node_ids.add(node_id)
        
        # Add external node IDs
        external_node_ids = self.get_set_of_node_ids_from_external_input_names()
        if not CommonValidators.is_empty(external_node_ids):
            available_graph_node_ids.update(external_node_ids)
        
        return self.is_set_1_subset_of_set_2(set_of_dependencies, available_graph_node_ids)

    @staticmethod
    def is_set_1_subset_of_set_2(set1: Set, set2: Set) -> bool:
        """Check if set1 is a subset of set2."""
        if len(set1) > len(set2):
            return False
        return set1.issubset(set2)

    def get_set_of_node_ids_from_external_input_names(self) -> Optional[Set[str]]:
        """Get set of node IDs from external input names."""
        if CommonValidators.is_empty(self.external_input_names):
            return None
        
        output = set()
        for value in self.external_input_names:
            node_id = SkymelECGraphNode.get_node_id_from_output_name(value)
            output.add(node_id)
        return output

    def get_execution_dependency_graph(self) -> Dict:
        """Build the execution dependency graph."""
        dependency_graph = {}
        
        for node_id in self.node_id_to_object:
            node_object = self.node_id_to_object[node_id]
            
            if self.is_skymel_ec_graph_instance(node_object):
                continue
            
            dependencies = node_object.get_node_ids_from_which_this_node_derives_inputs()
            for parent_node_id in dependencies:
                if parent_node_id not in dependency_graph:
                    dependency_graph[parent_node_id] = set()
                dependency_graph[parent_node_id].add(node_id)
            
            if node_id not in dependency_graph:
                dependency_graph[node_id] = set()
        
        return self.clean_execution_dependency_graph(dependency_graph)

    def clean_execution_dependency_graph(self, input_execution_dependency_graph: Dict) -> Dict:
        """Clean up the execution dependency graph."""
        for node_id in input_execution_dependency_graph:
            if len(input_execution_dependency_graph[node_id]) == 0:
                input_execution_dependency_graph[node_id] = None
        return input_execution_dependency_graph

    async def get_graph_node_execution_order(self, store_last_executed_graph_of_nodes: bool = False) -> List[str]:
        """Get the topological order for graph execution."""
        execution_dependency_graph = self.get_execution_dependency_graph()
        if store_last_executed_graph_of_nodes:
            self.store_last_executed_graph_of_nodes(execution_dependency_graph)
        return CommonGraphAlgorithms.topological_sort(execution_dependency_graph)

    def store_last_executed_graph_of_nodes(self, graph_of_nodes: Dict):
        """Store the last executed graph of nodes."""
        self.execution_graph_of_nodes = graph_of_nodes

    def get_last_executed_graph_of_nodes(self) -> Optional[Dict]:
        """Get the last executed graph of nodes."""
        return getattr(self, 'execution_graph_of_nodes', None)

    async def execute_graph(self, graph_execution_config: Optional[Dict] = None, measure_execution_time: bool = True) -> bool:
        """
        Execute the graph.
        
        Args:
            graph_execution_config: Configuration for graph execution
            measure_execution_time: Whether to measure execution time
            
        Returns:
            True if execution succeeded, False otherwise
        """
        self.set_graph_execution_config(graph_execution_config)
        execution_order = await self.get_graph_node_execution_order(store_last_executed_graph_of_nodes=True)
        
        executed_external_graphs = set()
        executed_nodes = set()
        external_node_ids = set() if CommonValidators.is_empty(self.external_input_names) else self.get_set_of_all_node_ids_from_external_input_names()
        
        external_input_names_to_values_dict = SkymelECGraphUtils.get_external_input_names_to_values_dict_from_graph_execution_config(graph_execution_config)
        if not CommonValidators.is_empty(external_input_names_to_values_dict) and CommonValidators.is_dict(external_input_names_to_values_dict):
            external_node_ids_which_have_been_assigned_values = self.set_values_for_external_input_names_and_return_node_ids(external_input_names_to_values_dict)
            executed_nodes = set(external_node_ids_which_have_been_assigned_values)
        
        is_graph_valid = await self.is_graph_valid()
        if not is_graph_valid:
            raise RuntimeError("Graph is not valid. Most likely due to missing dependencies.")
        
        overall_execution_succeeded = True
        for current_node_id in execution_order:
            if current_node_id in external_node_ids:
                continue
            
            if self.is_graph_id_prefix_for_node_id(current_node_id):
                external_graph_id = self.get_graph_id_from_node_id_with_graph_id(current_node_id)
                if external_graph_id not in executed_external_graphs:
                    execution_status_of_external_graph = await self.node_id_to_object[external_graph_id].execute_graph(graph_execution_config, measure_execution_time)
                    if execution_status_of_external_graph:
                        executed_external_graphs.add(external_graph_id)
                    else:
                        return False
                
                if external_graph_id in executed_external_graphs:
                    executed_nodes.add(current_node_id)
                continue
            
            node = self.node_id_to_object[current_node_id]
            input_names = node.get_node_input_names()
            
            if input_names is None or len(input_names) == 0:
                run_status = await node.execute(self, None, measure_execution_time)
            else:
                graph_node_input_names = node.get_node_input_names()
                graph_node_input_values = self.get_executed_graph_node_outputs(graph_node_input_names, executed_nodes)
                run_status = await node.execute(self, graph_node_input_values, measure_execution_time)
            
            if run_status is False:
                overall_execution_succeeded = False
                break
            
            executed_nodes.add(current_node_id)
        
        if overall_execution_succeeded and self.success_callback is not None:
            await self.success_callback(self)
        
        if not overall_execution_succeeded and self.error_callback is not None:
            await self.error_callback(self)
        
        return overall_execution_succeeded

    def get_executed_graph_node_outputs(self, list_of_desired_graph_node_output_names: List[str], set_of_executed_nodes: Set[str]) -> Dict:
        """Get outputs from executed graph nodes."""
        output = {}
        
        for desired_output_name in list_of_desired_graph_node_output_names:
            node_id = SkymelECGraphNode.get_node_id_from_output_name(desired_output_name)
            
            if node_id not in set_of_executed_nodes:
                raise RuntimeError(f"Node {node_id} is not in the set of executed nodes.")
            
            if (not CommonValidators.is_empty(self.external_input_names_to_values_dict) and 
                desired_output_name in self.external_input_names_to_values_dict):
                output[desired_output_name] = self.external_input_names_to_values_dict[desired_output_name]
                continue
            
            if self.is_graph_id_prefix_for_node_id(node_id):
                external_graph_id = self.get_graph_id_from_node_id_with_graph_id(node_id)
                external_graph_output_name = self.remove_graph_id_from_output_name(desired_output_name)
                external_graph_node_id = self.get_node_id_from_node_id_with_graph_id(node_id)
                external_execution_result = self.node_id_to_object[external_graph_id].get_last_execution_result_from_node(external_graph_node_id)
                
                if external_execution_result is None:
                    raise RuntimeError(f"Result {external_graph_output_name} could not be obtained.")
                
                if external_graph_output_name not in external_execution_result:
                    raise RuntimeError(f"Node {node_id} has not produced the output {desired_output_name}.")
                
                output[desired_output_name] = external_execution_result[external_graph_output_name]
            else:
                last_node_execution_result = self.node_id_to_object[node_id].get_last_execution_result()
                
                if last_node_execution_result is None:
                    raise RuntimeError(f"Node {node_id} has not been executed yet.")
                
                if desired_output_name not in last_node_execution_result:
                    raise RuntimeError(f"Node {node_id} has not produced the output {desired_output_name}.")
                
                output[desired_output_name] = last_node_execution_result[desired_output_name]
        
        return output

    def set_values_for_external_input_names_and_return_node_ids(self, input_names_to_values_dict: Dict) -> Set[str]:
        """Set values for external input names and return corresponding node IDs."""
        self.external_input_names_to_values_dict = {}
        
        if CommonValidators.is_empty(input_names_to_values_dict):
            return set()
        
        output = set()
        for input_name in input_names_to_values_dict:
            if input_name not in self.external_input_names:
                continue
            
            node_id = SkymelECGraphNode.get_node_id_from_output_name(input_name)
            output.add(node_id)
            self.external_input_names_to_values_dict[input_name] = input_names_to_values_dict[input_name]
        
        return output

    def get_set_of_all_node_ids_from_external_input_names(self) -> Optional[Set[str]]:
        """Get set of all node IDs from external input names."""
        if CommonValidators.is_empty(self.external_input_names):
            return None
        
        output = set()
        for input_name in self.external_input_names:
            node_id = SkymelECGraphNode.get_node_id_from_output_name(input_name)
            output.add(node_id)
        return output

    def set_graph_execution_config(self, graph_execution_config: Optional[Dict]):
        """Set the graph execution configuration."""
        self.graph_execution_config = graph_execution_config

    def get_graph_execution_config(self) -> Optional[Dict]:
        """Get the graph execution configuration."""
        return getattr(self, 'graph_execution_config', None)

    def get_last_execution_result(self, get_results_from_all_nodes: bool = False) -> Optional[Dict]:
        """Get the last execution result."""
        last_executed_graph_of_nodes = self.get_last_executed_graph_of_nodes()
        if last_executed_graph_of_nodes is None:
            return None
        
        leaf_nodes_list = CommonGraphAlgorithms.get_list_of_leaf_node_ids(last_executed_graph_of_nodes)
        if leaf_nodes_list is None or len(leaf_nodes_list) == 0:
            return None
        
        output = {}
        nodes_to_get_results_from = list(self.node_id_to_object.keys()) if get_results_from_all_nodes else leaf_nodes_list
        
        for node_id in nodes_to_get_results_from:
            if node_id not in self.node_id_to_object:
                return None
            
            node_object = self.node_id_to_object[node_id]
            last_node_execution_result = node_object.get_last_execution_result()
            
            if last_node_execution_result is not None:
                for key in last_node_execution_result:
                    key_name = f"{self.get_graph_id()}.{key}"
                    output[key_name] = last_node_execution_result[key]
        
        return output

    def get_last_execution_result_from_node(self, node_id: str) -> Optional[Dict]:
        """Get the last execution result from a specific node."""
        if not CommonValidators.is_non_empty_string(node_id):
            return None
        
        if node_id not in self.node_id_to_object:
            return None
        
        return self.node_id_to_object[node_id].get_last_execution_result()

    async def get_output_node_ids(self) -> Optional[List[str]]:
        """Get the output node IDs of the graph."""
        is_graph_valid = await self.is_graph_valid()
        if not is_graph_valid:
            return None
        
        execution_graph = self.get_execution_dependency_graph()
        output_nodes = CommonGraphAlgorithms.get_list_of_leaf_node_ids(execution_graph)
        
        return output_nodes if output_nodes else []

    async def dispose(self) -> bool:
        """Dispose of the graph and clean up resources."""
        if CommonValidators.is_empty(self.node_id_to_object):
            return True
        
        for node_id in list(self.node_id_to_object.keys()):
            disposal_result = await self.node_id_to_object[node_id].dispose()
            if disposal_result:
                del self.node_id_to_object[node_id]
        
        return True
