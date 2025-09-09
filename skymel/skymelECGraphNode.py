import re

from .commonUtils import generate_unique_string_key, maybe_convert_bytes_to_string
from .commonValidators import CommonValidators


class SkymelECGraphNode(object):
    def __init__(self, initialization_config):
        self.initialization_config = initialization_config
        self.node_id = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodeId', SkymelECGraphNode.generate_node_id())
        self.node_input_names = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodeInputNames', None)
        self.node_input_names_to_default_values = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodeInputNamesToDefaultValueMap', None)
        self.node_subroutine = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodeSubroutine', None)
        if CommonValidators.is_empty(self.node_subroutine):
            raise RuntimeError(f"No node subroutine for node {self.node_id}")
        self.node_output_names = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodeOutputNames', ['defaultOutput'])
        self.node_log_errors = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, "nodeLogErrors", False)

        self.execution_timings_milliseconds = []
        self.execution_run_success_statuses = []
        self.last_execution_result = None
        self.logged_node_errors = []
        self.on_execution_complete_callback = None



    @staticmethod
    def generate_node_id(node_id_prefix: str | None = None, node_id_suffix: str | None = None) -> str:
        node_id = generate_unique_string_key()
        if not CommonValidators.is_empty(node_id_prefix):
            node_id = node_id_prefix + node_id
        if not CommonValidators.is_empty(node_id_suffix):
            node_id = node_id + node_id_suffix
        return node_id

    @staticmethod
    def is_valid_node_output_name(node_output_name: str) -> bool:
        if not CommonValidators.is_non_empty_string_or_bytes(node_output_name):
            return False
        node_output_name_string = maybe_convert_bytes_to_string(node_output_name)
        if not CommonValidators.is_non_empty_string(node_output_name_string):
            return False
        pattern_matcher = re.compile(r"^(([a-zA-Z0-9_]+)\.)+([a-zA-Z0-9_]+)$")
        if not pattern_matcher.match(node_output_name_string):
            return False
        return True

    @staticmethod
    def get_node_id_from_output_name(node_output_name: str) -> str:
        if not SkymelECGraphNode.is_valid_node_output_name(node_output_name):
            return None
        name_parts = node_output_name.split(".")
        node_id_parts = name_parts[:-2]
        return ".".join(node_id_parts)

    def set_node_id(self, node_id: str):
        self.node_id = node_id

    def get_node_id(self):
        return self.node_id

    def set_node_input_names(self, node_input_names: list[str]):
        self.node_input_names = node_input_names

    def get_node_input_names(self):
        return self.node_input_names

    def set_node_input_names_to_default_values(self, node_input_names_to_default_values: list[str]):
        self.node_input_names_to_default_values = node_input_names_to_default_values

    def get_node_input_names_to_default_values(self):
        return self.node_input_names_to_default_values

    def set_node_subroutine(self, node_subroutine):
        self.node_subroutine = node_subroutine

    def get_node_subroutine(self):
        return self.node_subroutine

    @staticmethod
    def is_valid_input_names(node_input_names: list[str], reference_to_graph = None):
        if not CommonValidators.is_non_empty_list(node_input_names):
            return False
        for node_input_name in node_input_names:
            if not SkymelECGraphNode.is_valid_node_output_name(node_input_name):
                return False
        if reference_to_graph is not None:
            return reference_to_graph.contains_node_output_names(node_input_names)
        return True


    def is_valid_output_names(self, node_input_names: list[str], reference_to_graph = None):
        if not CommonValidators.is_non_empty_list(node_input_names):
            return False


    def set_node_output_names(self, node_output_names: list[str]):
        self.node_output_names = node_output_names

    def get_node_output_names(self):
        return self.node_output_names

    def set_node_log_errors(self, node_log_errors: bool):
        self.node_log_errors = node_log_errors

    def get_node_log_errors(self):
        return self.node_log_errors

    def set_on_execution_complete_callback(self, on_execution_complete_callback):
        self.on_execution_complete_callback = on_execution_complete_callback

    def get_on_execution_complete_callback(self):
        return self.on_execution_complete_callback

    def log_node_error(self, error_message: str | None = None):
        self.logged_node_errors.append(error_message)

    def get_logged_node_errors(self):
        return self.logged_node_errors

    def get_node_ids_from_which_this_node_derives_inputs(self) -> list[str]:
        """Get list of node IDs from which this node derives its inputs."""
        if not CommonValidators.is_non_empty_list(self.node_input_names):
            return []
        
        node_ids = []
        for input_name in self.node_input_names:
            if SkymelECGraphNode.is_valid_node_output_name(input_name):
                node_id = SkymelECGraphNode.get_node_id_from_output_name(input_name)
                node_ids.append(node_id)
        
        return list(set(node_ids))  # Remove duplicates

    def get_input_names(self) -> list[str] | None:
        """Get the input names for this node."""
        return self.node_input_names

    def get_output_names(self) -> list[str]:
        """Get the output names for this node."""
        if not CommonValidators.is_non_empty_list(self.node_output_names):
            return []
        
        # Prefix with node ID to make fully qualified names
        output_names = []
        for output_name in self.node_output_names:
            full_output_name = f"{self.node_id}.{output_name}"
            output_names.append(full_output_name)
        
        return output_names

    def contains_node_output_name(self, output_name: str) -> bool:
        """Check if this node contains the specified output name."""
        if not SkymelECGraphNode.is_valid_node_output_name(output_name):
            return False
        
        # Extract the actual output name (without node ID prefix)
        parts = output_name.split(".")
        if len(parts) < 2:
            return False
        
        actual_output_name = parts[-1]
        return actual_output_name in self.node_output_names

    def get_last_execution_result(self) -> dict | None:
        """Get the last execution result."""
        return self.last_execution_result

    def is_node_valid(self, reference_graph=None) -> bool:
        """Check if this node is valid."""
        if not CommonValidators.is_non_empty_string(self.node_id):
            return False
        
        if CommonValidators.is_empty(self.node_subroutine):
            return False
        
        if not CommonValidators.is_non_empty_list(self.node_output_names):
            return False
        
        # Validate input names if they exist
        if self.node_input_names is not None:
            if not SkymelECGraphNode.is_valid_input_names(self.node_input_names, reference_graph):
                return False
        
        return True

    def get_average_execution_time_milliseconds(self, max_count_of_last_execution_to_average_over: int = 5) -> float:
        """Get the average execution time in milliseconds."""
        if not self.execution_timings_milliseconds:
            return 0.0
        
        recent_timings = self.execution_timings_milliseconds[-max_count_of_last_execution_to_average_over:]
        return sum(recent_timings) / len(recent_timings)

    def get_last_measured_execution_time_milliseconds(self) -> float:
        """Get the last measured execution time in milliseconds."""
        if not self.execution_timings_milliseconds:
            return 0.0
        return self.execution_timings_milliseconds[-1]

    async def execute(self, parent_graph, input_values: dict = None, measure_execution_time: bool = True):
        """
        Execute this node.
        
        Args:
            parent_graph: The parent graph containing this node
            input_values: Input values for the node
            measure_execution_time: Whether to measure execution time
            
        Returns:
            True if execution succeeded, False otherwise
        """
        import time
        
        start_time = time.time() * 1000 if measure_execution_time else None
        
        try:
            # Execute the node subroutine
            if CommonValidators.is_callable_method(self.node_subroutine):
                # Call the subroutine with appropriate parameters
                if input_values is None:
                    result = await self.node_subroutine() if hasattr(self.node_subroutine, '__call__') else self.node_subroutine
                else:
                    result = await self.node_subroutine(input_values) if hasattr(self.node_subroutine, '__call__') else self.node_subroutine
                
                # Store the result
                self.last_execution_result = result if isinstance(result, dict) else {'result': result}
                
                # Record success
                self.execution_run_success_statuses.append(True)
                
                if measure_execution_time:
                    execution_time = time.time() * 1000 - start_time
                    self.execution_timings_milliseconds.append(execution_time)
                
                # Call completion callback if available
                if self.on_execution_complete_callback is not None:
                    await self.on_execution_complete_callback(self)
                
                return True
            else:
                # Handle string-based subroutines or other types
                # For now, just store the subroutine as result
                self.last_execution_result = {'output': str(self.node_subroutine)}
                self.execution_run_success_statuses.append(True)
                
                if measure_execution_time:
                    execution_time = time.time() * 1000 - start_time
                    self.execution_timings_milliseconds.append(execution_time)
                
                return True
                
        except Exception as e:
            error_message = f"Error executing node {self.node_id}: {str(e)}"
            
            if self.node_log_errors:
                self.log_node_error(error_message)
            
            self.execution_run_success_statuses.append(False)
            
            if measure_execution_time:
                execution_time = time.time() * 1000 - start_time
                self.execution_timings_milliseconds.append(execution_time)
            
            return False

    async def dispose(self) -> bool:
        """Dispose of the node and clean up resources."""
        self.last_execution_result = None
        self.execution_timings_milliseconds.clear()
        self.execution_run_success_statuses.clear()
        self.logged_node_errors.clear()
        return True