import re

from commonUtils import generate_unique_string_key, maybe_convert_bytes_to_string
from skymel.commonValidators import CommonValidators


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