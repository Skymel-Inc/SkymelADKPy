import base64
import json
from typing import Dict, List, Optional, Any
from .commonValidators import CommonValidators


class SkymelECGraphUtils:
    # Graph Type Constants
    GRAPH_TYPE_BASE = "base"
    GRAPH_TYPE_SPLIT_INFERENCE_RUNNER = "splitInferenceRunner"
    GRAPH_TYPE_AUTOREGRESSIVE_INFERENCE_RUNNER = "autoregressiveInferenceRunner"
    
    # Node Type Constants
    NODE_TYPE_BASE = "base"
    NODE_TYPE_LOCAL_INFERENCE_RUNNER = "localInferenceRunner"
    NODE_TYPE_REMOTE_INFERENCE_RUNNER = "remoteInferenceRunner"
    NODE_TYPE_EXTERNAL_API_CALLER = "externalApiCaller"
    NODE_TYPE_TRANSFORMERJS_PROCESSOR = "transformerJSProcessor"
    NODE_TYPE_LLM_INPUT_PREPARER = "llmInputPreparer"
    NODE_TYPE_LLM_OUTPUT_LOGITS_TO_TOKEN_ID_GREEDY_SEARCHER = "llmOutputLogitsToTokenIdGreedySearcher"
    NODE_TYPE_DATA_PROCESSING = "dataProcessing"

    def __init__(self):
        raise RuntimeError("This class should not be instantiated; use static methods instead")

    @staticmethod
    def get_external_input_names_to_values_dict_from_graph_execution_config(graph_execution_config: Optional[Dict]) -> Optional[Dict]:
        """
        Extracts external input names to values dictionary from graph execution config.
        
        Args:
            graph_execution_config: The graph execution configuration
            
        Returns:
            Dictionary mapping external input names to values, or None if not found
        """
        if CommonValidators.is_empty(graph_execution_config):
            return None
        
        return CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            graph_execution_config, 'externalInputNamesToValuesDict', None
        )

    @staticmethod
    def get_external_input_names_from_graph_initialization_config(graph_initialization_config: Optional[Dict]) -> List[str]:
        """
        Gets external input names from graph initialization config.
        
        Args:
            graph_initialization_config: The graph initialization configuration
            
        Returns:
            List of external input names
        """
        if CommonValidators.is_empty(graph_initialization_config):
            return []
        
        external_inputs = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            graph_initialization_config, 'externalInputNames', []
        )
        
        if not CommonValidators.is_list(external_inputs):
            return []
            
        return external_inputs

    @staticmethod
    def get_file_data_and_details_dict_from_html_file_input_element(file_object) -> Dict[str, Any]:
        """
        Processes a file object and returns data and details dictionary.
        This is a Python adaptation of the JavaScript file processing logic.
        
        Args:
            file_object: File object (could be from various sources)
            
        Returns:
            Dictionary containing file data and details
        """
        try:
            if hasattr(file_object, 'read'):
                # File-like object
                content = file_object.read()
                if isinstance(content, bytes):
                    content_b64 = base64.b64encode(content).decode('utf-8')
                else:
                    content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                
                return {
                    'name': getattr(file_object, 'name', 'unknown'),
                    'type': 'application/octet-stream',
                    'size': len(content),
                    'lastModified': 0,  # Default value
                    'content': content_b64
                }
            elif isinstance(file_object, dict):
                # Dictionary with file data
                return {
                    'name': file_object.get('name', 'unknown'),
                    'type': file_object.get('type', 'application/octet-stream'),
                    'size': file_object.get('size', 0),
                    'lastModified': file_object.get('lastModified', 0),
                    'content': file_object.get('content', '')
                }
            else:
                # String content
                content_b64 = base64.b64encode(str(file_object).encode('utf-8')).decode('utf-8')
                return {
                    'name': 'text_content',
                    'type': 'text/plain',
                    'size': len(str(file_object)),
                    'lastModified': 0,
                    'content': content_b64
                }
        except Exception as e:
            raise RuntimeError(f"Error processing file object: {str(e)}")

    @staticmethod
    def validate_graph_json_object(graph_json: Dict) -> bool:
        """
        Validates that a graph JSON object has the required structure.
        
        Args:
            graph_json: The graph JSON object to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not CommonValidators.is_non_empty_dict(graph_json):
            return False
        
        # Check for required keys
        required_keys = ['graphType', 'graphInitializationConfig']
        for key in required_keys:
            if not CommonValidators.is_non_empty_dict_and_has_key(graph_json, key):
                return False
        
        # Validate graph type
        graph_type = graph_json['graphType']
        valid_graph_types = [
            SkymelECGraphUtils.GRAPH_TYPE_BASE,
            SkymelECGraphUtils.GRAPH_TYPE_SPLIT_INFERENCE_RUNNER,
            SkymelECGraphUtils.GRAPH_TYPE_AUTOREGRESSIVE_INFERENCE_RUNNER
        ]
        
        if graph_type not in valid_graph_types:
            return False
        
        # Validate initialization config
        init_config = graph_json['graphInitializationConfig']
        if not CommonValidators.is_non_empty_dict(init_config):
            return False
        
        return True

    @staticmethod
    def validate_node_json_object(node_json: Dict) -> bool:
        """
        Validates that a node JSON object has the required structure.
        
        Args:
            node_json: The node JSON object to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not CommonValidators.is_non_empty_dict(node_json):
            return False
        
        # Check for required keys
        required_keys = ['nodeType', 'nodeInitializationConfig']
        for key in required_keys:
            if not CommonValidators.is_non_empty_dict_and_has_key(node_json, key):
                return False
        
        # Validate node type
        node_type = node_json['nodeType']
        valid_node_types = [
            SkymelECGraphUtils.NODE_TYPE_BASE,
            SkymelECGraphUtils.NODE_TYPE_LOCAL_INFERENCE_RUNNER,
            SkymelECGraphUtils.NODE_TYPE_REMOTE_INFERENCE_RUNNER,
            SkymelECGraphUtils.NODE_TYPE_EXTERNAL_API_CALLER,
            SkymelECGraphUtils.NODE_TYPE_TRANSFORMERJS_PROCESSOR,
            SkymelECGraphUtils.NODE_TYPE_LLM_INPUT_PREPARER,
            SkymelECGraphUtils.NODE_TYPE_LLM_OUTPUT_LOGITS_TO_TOKEN_ID_GREEDY_SEARCHER,
            SkymelECGraphUtils.NODE_TYPE_DATA_PROCESSING
        ]
        
        if node_type not in valid_node_types:
            return False
        
        # Validate initialization config
        init_config = node_json['nodeInitializationConfig']
        if not CommonValidators.is_non_empty_dict(init_config):
            return False
        
        return True