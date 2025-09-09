import json
from typing import Dict, Optional, Union
from .commonValidators import CommonValidators
from .skymelECGraphUtils import SkymelECGraphUtils
from .skymelEcGraph import SkymelECGraph
from .skymelECGraphNode import SkymelECGraphNode


class SkymelExecutionGraphLoader:
    """
    Loader class for creating SkymelECGraph instances from JSON configurations.
    """
    
    def __init__(self):
        raise RuntimeError("Cannot instantiate this class. It has purely static methods, " +
                         "please call them using class-name scope, such as " +
                         "`SkymelExecutionGraphLoader.load_graph_from_json_object(param)`")

    @staticmethod
    async def load_graph_from_json_file(json_file_path: str) -> Optional[SkymelECGraph]:
        """
        Load a graph from a JSON file.
        
        Args:
            json_file_path: Path to the JSON file
            
        Returns:
            SkymelECGraph instance or None if loading failed
        """
        if not CommonValidators.is_non_empty_string(json_file_path):
            return None
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                json_object = json.load(file)
                
            if not CommonValidators.is_empty(json_object):
                return SkymelExecutionGraphLoader.load_graph_from_json_object(json_object)
                
        except Exception as error:
            print(f"Error loading graph from JSON file: {error}")
        
        return None

    @staticmethod
    def load_graph_from_json_object(json_object: Dict) -> Optional[SkymelECGraph]:
        """
        Load a graph from a JSON object.
        
        Args:
            json_object: JSON object containing graph configuration
            
        Returns:
            SkymelECGraph instance or None if loading failed
        """
        if CommonValidators.is_empty(json_object):
            return None
        
        return SkymelExecutionGraphLoader.get_loaded_graph_and_children_nodes_from_dict(json_object)

    @staticmethod
    def get_loaded_graph_and_children_nodes_from_dict(graph_and_children_nodes_details: Dict) -> Optional[SkymelECGraph]:
        """
        Load graph and child nodes from dictionary configuration.
        
        Args:
            graph_and_children_nodes_details: Dictionary containing graph and node configurations
            
        Returns:
            SkymelECGraph instance or None if loading failed
        """
        if CommonValidators.is_empty(graph_and_children_nodes_details):
            return None
        
        # Extract graph type and initialization config
        graph_type = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            graph_and_children_nodes_details, 'graphType', None
        )
        
        graph_initialization_config = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            graph_and_children_nodes_details, 'graphInitializationConfig', None
        )
        
        if CommonValidators.is_empty(graph_type) or CommonValidators.is_empty(graph_initialization_config):
            return None
        
        # Create the graph object
        current_graph = SkymelExecutionGraphLoader.load_and_return_graph_object(graph_type, graph_initialization_config)
        if CommonValidators.is_empty(current_graph):
            return None
        
        # Process children (nodes and subgraphs)
        current_graph_children = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            graph_and_children_nodes_details, 'children', None
        )
        
        if CommonValidators.is_empty(current_graph_children) or not CommonValidators.is_list(current_graph_children):
            return current_graph
        
        # Add each child to the graph
        for current_child_details in current_graph_children:
            # Handle node children
            if CommonValidators.is_non_empty_dict_and_has_key(current_child_details, 'nodeType'):
                node_type = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
                    current_child_details, 'nodeType', None
                )
                node_config = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
                    current_child_details, 'nodeInitializationConfig', None
                )
                
                if CommonValidators.is_non_empty_string(node_type) and not CommonValidators.is_empty(node_config):
                    node_object = SkymelExecutionGraphLoader.load_and_return_node_object(node_type, node_config)
                    if node_object is not None:
                        current_graph.add_node(node_object)
            
            # Handle subgraph children
            elif CommonValidators.is_non_empty_dict_and_has_key(current_child_details, 'graphType'):
                sub_graph = SkymelExecutionGraphLoader.get_loaded_graph_and_children_nodes_from_dict(current_child_details)
                if not CommonValidators.is_empty(sub_graph):
                    current_graph.add_node(sub_graph)
        
        return current_graph

    @staticmethod
    def load_and_return_graph_object(graph_type: str, graph_initialization_config: Dict) -> Optional[SkymelECGraph]:
        """
        Create a graph object based on type and configuration.
        
        Args:
            graph_type: Type of graph to create
            graph_initialization_config: Configuration for graph initialization
            
        Returns:
            Graph instance or None if creation failed
        """
        if CommonValidators.is_empty(graph_initialization_config) or CommonValidators.is_empty(graph_type):
            return None
        
        # For now, we only support the base graph type in Python
        # Additional graph types can be implemented later
        if graph_type == SkymelECGraphUtils.GRAPH_TYPE_BASE:
            return SkymelECGraph(graph_initialization_config)
        elif graph_type == SkymelECGraphUtils.GRAPH_TYPE_SPLIT_INFERENCE_RUNNER:
            # Could implement SkymelECGraphForSplitInference later
            return SkymelECGraph(graph_initialization_config)
        elif graph_type == SkymelECGraphUtils.GRAPH_TYPE_AUTOREGRESSIVE_INFERENCE_RUNNER:
            # Could implement SkymelECGraphForAutoregressiveInference later
            return SkymelECGraph(graph_initialization_config)
        else:
            return None

    @staticmethod
    def load_and_return_node_object(node_type: str, node_initialization_config: Dict) -> Optional[SkymelECGraphNode]:
        """
        Create a node object based on type and configuration.
        
        Args:
            node_type: Type of node to create
            node_initialization_config: Configuration for node initialization
            
        Returns:
            Node instance or None if creation failed
        """
        if CommonValidators.is_empty(node_type) or CommonValidators.is_empty(node_initialization_config):
            return None
        
        # For now, we support the base node type
        # Additional specialized node types can be implemented later
        if node_type == SkymelECGraphUtils.NODE_TYPE_BASE:
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_LOCAL_INFERENCE_RUNNER:
            # Could implement SkymelECGraphNodeForLocalInference later
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_REMOTE_INFERENCE_RUNNER:
            # Could implement SkymelECGraphNodeForRemoteInference later
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_EXTERNAL_API_CALLER:
            # Could implement SkymelECGraphNodeForExternalApiCall later
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_TRANSFORMERJS_PROCESSOR:
            # Could implement SkymelECGraphNodeForTransformerJSProcessing later
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_LLM_INPUT_PREPARER:
            # Could implement SkymelECGraphNodeForLLMInputPrep later
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_LLM_OUTPUT_LOGITS_TO_TOKEN_ID_GREEDY_SEARCHER:
            # Could implement SkymelECGraphNodeForLLMLogitsGreedySearch later
            return SkymelECGraphNode(node_initialization_config)
        elif node_type == SkymelECGraphUtils.NODE_TYPE_DATA_PROCESSING:
            # Could implement SkymelECGraphNodeForDataProcessing later
            return SkymelECGraphNode(node_initialization_config)
        else:
            return None

    @staticmethod
    def validate_graph_json(json_object: Dict) -> bool:
        """
        Validate that a JSON object has the correct structure for loading a graph.
        
        Args:
            json_object: JSON object to validate
            
        Returns:
            True if valid, False otherwise
        """
        return SkymelECGraphUtils.validate_graph_json_object(json_object)