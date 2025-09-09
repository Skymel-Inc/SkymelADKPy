import json
from typing import Dict, List, Optional, Any, Union
from .commonValidators import CommonValidators
from .skymelExecutionGraphLoader import SkymelExecutionGraphLoader
from .skymelECGraphUtils import SkymelECGraphUtils
from .skymelEcGraph import SkymelECGraph


class SkymelAgent:
    """
    Main class for creating and managing Skymel AI agents.
    This is the Python equivalent of the JavaScript SkymelAgent class.
    """
    
    def __init__(self, 
                 api_key: str,
                 agent_creation_endpoint_url: str = "/websocket-dynamic-agent-generation-infer",
                 agent_creation_endpoint_url_is_websocket_url: bool = True,
                 agent_name_string: str = "",
                 agent_definition_string: str = "",
                 agent_restrictions_string: str = "",
                 developer_configuration_string: str = "",
                 is_mcp_enabled: bool = False):
        """
        Initialize a SkymelAgent instance.
        
        Args:
            api_key: API key for authentication
            agent_creation_endpoint_url: URL endpoint for agent creation
            agent_creation_endpoint_url_is_websocket_url: Whether endpoint is WebSocket
            agent_name_string: Name of the agent
            agent_definition_string: Definition/purpose of the agent
            agent_restrictions_string: Restrictions for the agent
            developer_configuration_string: Developer-specific configuration
            is_mcp_enabled: Whether MCP (Model Context Protocol) is enabled
        """
        self.api_key = api_key
        self.agent_developer_configuration_string = self.get_developer_configuration_string(
            developer_configuration_string,
            agent_name_string,
            agent_definition_string,
            agent_restrictions_string
        )
        self.agent_creation_endpoint_url = agent_creation_endpoint_url
        self.agent_creation_endpoint_url_is_websocket_url = agent_creation_endpoint_url_is_websocket_url
        self.is_mcp_enabled = is_mcp_enabled
        
        self.agentic_workflow_id_to_json_config = {}

    def get_agent_creation_endpoint_url(self) -> str:
        """Get the agent creation endpoint URL."""
        return self.agent_creation_endpoint_url

    def get_developer_configuration_string(self, 
                                         dev_config: str, 
                                         agent_name: str, 
                                         agent_definition: str, 
                                         agent_restrictions: str) -> str:
        """
        Build the developer configuration string from components.
        
        Args:
            dev_config: Base developer configuration
            agent_name: Name of the agent
            agent_definition: Definition/purpose of the agent
            agent_restrictions: Restrictions for the agent
            
        Returns:
            Combined configuration string
        """
        output = ""
        
        if CommonValidators.is_non_empty_string(agent_name):
            output += f"Your name is {agent_name}.\n"
        
        if CommonValidators.is_non_empty_string(agent_definition):
            output += f"Your purpose is as follows:\n{agent_definition}\n"
        
        if CommonValidators.is_non_empty_string(agent_restrictions):
            output += f"You have to make sure to abide by the following:\n{agent_restrictions}\n"
        
        if CommonValidators.is_non_empty_string(dev_config):
            output += dev_config
        
        return output

    async def get_file_data_and_details_dict_from_file_inputs_for_agent_graph_attachment(self, 
                                                                                       list_of_file_inputs: List) -> List[Dict]:
        """
        Process file inputs and convert them to data and details dictionaries.
        
        Args:
            list_of_file_inputs: List of file input objects
            
        Returns:
            List of file data and details dictionaries
        """
        if not CommonValidators.is_list(list_of_file_inputs):
            raise ValueError('list_of_file_inputs is not a list.')
        
        if len(list_of_file_inputs) == 0:
            raise ValueError('list_of_file_inputs is an empty list.')
        
        results = []
        for i, file_input in enumerate(list_of_file_inputs):
            try:
                file_data = SkymelECGraphUtils.get_file_data_and_details_dict_from_html_file_input_element(file_input)
                results.append(file_data)
            except Exception as error:
                print(f"Error processing file at index {i}: {error}")
                raise error
        
        return results

    def make_json_config_object_to_load_skymel_ec_graph(self, 
                                                       context_id_string: str = '',
                                                       number_of_attached_file_data_and_details_objects: int = 0) -> Dict:
        """
        Create JSON configuration object that can be loaded into a SkymelECGraph instance.
        
        Args:
            context_id_string: String used to group and identify the SkymelECGraph's context
            number_of_attached_file_data_and_details_objects: Number of file attachments
            
        Returns:
            JSON object from which a SkymelECGraph can be created/loaded
        """
        # External input names that are externally provided
        external_input_names = ["external.text"]
        
        # Dictionary mapping SkymelECGraphNode variable names to names used by the external API backend
        input_mappings = {"external.text": "textInput"}
        
        # Add file inputs if needed
        if number_of_attached_file_data_and_details_objects > 0:
            for i in range(number_of_attached_file_data_and_details_objects):
                input_name = f"external.file{i + 1}"
                external_input_names.append(input_name)
                input_mappings[input_name] = f"fileInput{i + 1}"
        
        # Create the graph description
        graph_description_json = {
            'graphType': SkymelECGraphUtils.GRAPH_TYPE_BASE,
            'graphInitializationConfig': {
                'graphId': 'agent_graph_generator',
                'externalInputNames': external_input_names,
            },
            'children': []
        }
        
        # Create the node configuration
        node_1_config_object = {
            'nodeType': SkymelECGraphUtils.NODE_TYPE_EXTERNAL_API_CALLER,
            'nodeInitializationConfig': {
                'nodeId': 'dynamicWorkflowCallerNode',
                'nodeInputNames': external_input_names,
                'nodeOutputNames': ["outputText"],
                'nodePrivateAttributesAndValues': {
                    'contextId': context_id_string,
                    'createNewContextIfContextIsNull': True
                },
                'endpointUrl': self.agent_creation_endpoint_url,
                'apiKey': self.api_key,
                'nodeInputNameToBackendInputNameMap': input_mappings,
                'backendOutputNameToNodeOutputNameMap': {"textOutputs": "dynamicWorkflowCallerNode.outputText"},
                'isEndpointWebSocketUrl': self.agent_creation_endpoint_url_is_websocket_url
            }
        }
        
        graph_description_json['children'].append(node_1_config_object)
        return graph_description_json

    def update_agent_graph_creation_json_config_with_agent_creation_specific_information(self,
                                                                                        agent_creation_graph_json: Dict,
                                                                                        developer_prompt: str = '',
                                                                                        available_inputs: Dict = None,
                                                                                        is_mcp_enabled: bool = False) -> Dict:
        """
        Update agent creation graph JSON config with specific information.
        
        Args:
            agent_creation_graph_json: Base graph JSON configuration
            developer_prompt: Developer prompt string
            available_inputs: Available inputs dictionary
            is_mcp_enabled: Whether MCP is enabled
            
        Returns:
            Updated graph JSON configuration
        """
        if available_inputs is None:
            available_inputs = {}
        
        if ('children' in agent_creation_graph_json and 
            len(agent_creation_graph_json['children']) > 0 and
            'nodeInitializationConfig' in agent_creation_graph_json['children'][0]):
            
            # Update the first child node's private attributes
            current_attributes = agent_creation_graph_json['children'][0]['nodeInitializationConfig'].get(
                'nodePrivateAttributesAndValues', {}
            )
            
            current_attributes.update({
                'developerPrompt': developer_prompt,
                'availableInputs': json.dumps(available_inputs),
                'mcpEnabled': is_mcp_enabled
            })
            
            agent_creation_graph_json['children'][0]['nodeInitializationConfig']['nodePrivateAttributesAndValues'] = current_attributes
        
        return agent_creation_graph_json

    def get_agent_task_or_placeholder(self, agent_task_string: str) -> str:
        """
        Get agent task string or placeholder if empty.
        
        Args:
            agent_task_string: The agent task string
            
        Returns:
            Task string or placeholder
        """
        temporary_task_string = agent_task_string.strip()
        if CommonValidators.is_non_empty_string(temporary_task_string):
            return temporary_task_string
        
        return ("This is a placeholder for a potential user-centric input task. "
                "At the moment, please proceed assuming a default state for every choice required.")

    def get_agent_creation_graph_external_input_values(self,
                                                      agent_task: str,
                                                      file_data_and_details_for_skymel_ec_graph_attachment: List[Dict] = None) -> Dict:
        """
        Get external input values for the agent creation graph.
        
        Args:
            agent_task: The agent task description
            file_data_and_details_for_skymel_ec_graph_attachment: File data for attachment
            
        Returns:
            Dictionary of external input values
        """
        if file_data_and_details_for_skymel_ec_graph_attachment is None:
            file_data_and_details_for_skymel_ec_graph_attachment = []
        
        output = {}
        output["external.text"] = self.get_agent_task_or_placeholder(agent_task)
        
        if (CommonValidators.is_list(file_data_and_details_for_skymel_ec_graph_attachment) and 
            len(file_data_and_details_for_skymel_ec_graph_attachment) > 0):
            
            for i, file_data in enumerate(file_data_and_details_for_skymel_ec_graph_attachment):
                if not CommonValidators.is_non_empty_dict_and_has_key(file_data, 'content'):
                    continue
                
                output[f"external.file{i + 1}"] = file_data['content']
        
        return output

    async def get_agentic_workflow_graph_json_config(self,
                                                   agent_task: str = '',
                                                   file_data_and_details_for_skymel_ec_graph_attachment: List[Dict] = None,
                                                   context_id_string: str = '') -> Optional[Dict]:
        """
        Get the agentic workflow graph JSON configuration.
        
        Args:
            agent_task: The agent task description
            file_data_and_details_for_skymel_ec_graph_attachment: File data for attachment
            context_id_string: Context ID string
            
        Returns:
            Graph JSON configuration or None if failed
        """
        if file_data_and_details_for_skymel_ec_graph_attachment is None:
            file_data_and_details_for_skymel_ec_graph_attachment = []
        
        number_of_attached_files = (len(file_data_and_details_for_skymel_ec_graph_attachment) 
                                   if CommonValidators.is_list(file_data_and_details_for_skymel_ec_graph_attachment) 
                                   else 0)
        
        # Create agent creation graph
        agent_creation_graph_json = self.make_json_config_object_to_load_skymel_ec_graph(
            context_id_string, number_of_attached_files
        )
        
        # Update with agent-specific information
        agent_creation_graph_json = self.update_agent_graph_creation_json_config_with_agent_creation_specific_information(
            agent_creation_graph_json,
            self.agent_developer_configuration_string,
            {},
            self.is_mcp_enabled
        )
        
        # Load the graph
        agent_creation_graph = SkymelExecutionGraphLoader.load_graph_from_json_object(agent_creation_graph_json)
        
        if not isinstance(agent_creation_graph, SkymelECGraph):
            raise RuntimeError('Could not successfully create agent graph.')
        
        # Get external inputs
        external_inputs = self.get_agent_creation_graph_external_input_values(
            agent_task, file_data_and_details_for_skymel_ec_graph_attachment
        )
        
        # Execute the graph
        await agent_creation_graph.execute_graph({'externalInputNamesToValuesDict': external_inputs})
        
        # Get execution result
        agent_creation_graph_execution_result = agent_creation_graph.get_last_execution_result()
        if CommonValidators.is_empty(agent_creation_graph_execution_result):
            raise RuntimeError("Got null value as a result of Agent Graph Creation.")
        
        # Extract agent output
        agent_output_key = 'agent_graph_generator.dynamicWorkflowCallerNode.outputText'
        if not CommonValidators.is_non_empty_dict_and_has_key(agent_creation_graph_execution_result, agent_output_key):
            raise RuntimeError("Got invalid agent creation result.")
        
        try:
            agent_json_graph_object = json.loads(agent_creation_graph_execution_result[agent_output_key])
            self.agentic_workflow_id_to_json_config[context_id_string] = agent_json_graph_object
            return agent_json_graph_object
        except json.JSONDecodeError as parse_error:
            print(f"Encountered error while JSON parsing Agent Creation Graph response: {parse_error}")
            raise RuntimeError("Encountered error while JSON parsing Agent Creation Graph response.")

    async def run_agentic_workflow(self, 
                                 agentic_workflow_graph_json_config: Dict,
                                 input_names_to_values_dict: Dict) -> Any:
        """
        Run an agentic workflow using the provided configuration.
        
        Args:
            agentic_workflow_graph_json_config: Graph configuration for the workflow
            input_names_to_values_dict: Input values for the workflow
            
        Returns:
            Workflow execution result
        """
        # Load the workflow graph
        agentic_workflow_skymel_ec_graph = SkymelExecutionGraphLoader.load_graph_from_json_object(
            agentic_workflow_graph_json_config
        )
        
        if not isinstance(agentic_workflow_skymel_ec_graph, SkymelECGraph):
            raise RuntimeError("Failed to load agentic workflow graph.")
        
        # Get external input names
        list_of_external_inputs = SkymelECGraphUtils.get_external_input_names_from_graph_initialization_config(
            agentic_workflow_skymel_ec_graph.get_initialization_config()
        )
        
        # Execute the workflow
        execution_config = {
            'externalInputNamesToValuesDict': input_names_to_values_dict
        }
        
        success = await agentic_workflow_skymel_ec_graph.execute_graph(execution_config)
        
        if success:
            return agentic_workflow_skymel_ec_graph.get_last_execution_result()
        else:
            raise RuntimeError("Agentic workflow execution failed.")

    def get_cached_workflow_config(self, context_id_string: str) -> Optional[Dict]:
        """
        Get cached workflow configuration by context ID.
        
        Args:
            context_id_string: Context ID string
            
        Returns:
            Cached workflow configuration or None if not found
        """
        return self.agentic_workflow_id_to_json_config.get(context_id_string, None)