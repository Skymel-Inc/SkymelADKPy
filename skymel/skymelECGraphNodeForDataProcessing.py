import time
import json
from typing import Dict, List, Optional, Any, Union
from .skymelECGraphNode import SkymelECGraphNode
from .commonValidators import CommonValidators


class SkymelECGraphNodeForDataProcessing(SkymelECGraphNode):
    """
    Base class for data processing nodes in SkymelECGraph.
    
    This class extends SkymelECGraphNode to provide common functionality
    for nodes that process data, such as input validation, output formatting,
    and data transformation utilities.
    """
    
    def __init__(self, initialization_config: Dict):
        """
        Initialize a data processing node.
        
        Args:
            initialization_config: Configuration dictionary for node initialization
        """
        super().__init__(initialization_config)
        
        # Data processing specific attributes
        self.data_processing_config = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'dataProcessingConfig', {}
        )
        
        self.input_validation_enabled = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            self.data_processing_config, 'inputValidationEnabled', True
        )
        
        self.output_formatting_enabled = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            self.data_processing_config, 'outputFormattingEnabled', True
        )
        
        self.error_handling_mode = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            self.data_processing_config, 'errorHandlingMode', 'strict'
        )
        
        # Processing statistics
        self.processed_data_count = 0
        self.processing_errors = []
        self.last_processing_metadata = None

    def validate_input_data(self, input_data: Any) -> bool:
        """
        Validate input data before processing.
        
        Args:
            input_data: Data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if not self.input_validation_enabled:
            return True
        
        try:
            # Basic validation - can be overridden in subclasses
            if input_data is None:
                return False
            
            # Check if input is a dictionary (expected format for most nodes)
            if not isinstance(input_data, dict):
                return self.error_handling_mode != 'strict'
            
            return True
            
        except Exception as e:
            error_msg = f"Input validation error: {str(e)}"
            self.processing_errors.append(error_msg)
            
            if self.node_log_errors:
                self.log_node_error(error_msg)
            
            return self.error_handling_mode == 'lenient'

    def format_output_data(self, processed_data: Any) -> Dict[str, Any]:
        """
        Format processed data into the expected output format.
        
        Args:
            processed_data: Data that has been processed
            
        Returns:
            Formatted output dictionary
        """
        if not self.output_formatting_enabled:
            return processed_data if isinstance(processed_data, dict) else {'result': processed_data}
        
        try:
            # Create standardized output format
            output = {}
            
            # Handle different data types
            if isinstance(processed_data, dict):
                output.update(processed_data)
            elif isinstance(processed_data, (list, tuple)):
                output['items'] = list(processed_data)
                output['count'] = len(processed_data)
            else:
                output['result'] = processed_data
            
            # Add metadata if available
            if self.last_processing_metadata:
                output['metadata'] = self.last_processing_metadata
            
            # Add processing statistics
            output['processing_stats'] = {
                'processed_count': self.processed_data_count,
                'node_id': self.node_id,
                'processing_timestamp': time.time() * 1000
            }
            
            return output
            
        except Exception as e:
            error_msg = f"Output formatting error: {str(e)}"
            self.processing_errors.append(error_msg)
            
            if self.node_log_errors:
                self.log_node_error(error_msg)
            
            # Return minimal output on formatting error
            return {
                'result': processed_data,
                'error': error_msg,
                'node_id': self.node_id
            }

    def process_data(self, input_data: Any) -> Any:
        """
        Abstract method for data processing logic.
        Must be implemented by subclasses.
        
        Args:
            input_data: Data to process
            
        Returns:
            Processed data
        """
        raise NotImplementedError("Subclasses must implement process_data method")

    def pre_process_hook(self, input_data: Any) -> Any:
        """
        Hook called before data processing.
        Can be overridden by subclasses for preprocessing.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Preprocessed data
        """
        return input_data

    def post_process_hook(self, processed_data: Any, input_data: Any) -> Any:
        """
        Hook called after data processing.
        Can be overridden by subclasses for postprocessing.
        
        Args:
            processed_data: Data after processing
            input_data: Original input data
            
        Returns:
            Final processed data
        """
        return processed_data

    async def execute(self, parent_graph, input_values: Dict = None, measure_execution_time: bool = True) -> bool:
        """
        Execute the data processing node.
        
        Args:
            parent_graph: The parent graph containing this node
            input_values: Input values for the node
            measure_execution_time: Whether to measure execution time
            
        Returns:
            True if execution succeeded, False otherwise
        """
        start_time = time.time() * 1000 if measure_execution_time else None
        
        try:
            # Validate inputs
            if not self.validate_input_data(input_values):
                error_msg = "Input validation failed"
                if self.node_log_errors:
                    self.log_node_error(error_msg)
                self.execution_run_success_statuses.append(False)
                return False
            
            # Extract actual data from input values
            processing_input = input_values if input_values is not None else {}
            
            # Pre-processing hook
            preprocessing_result = self.pre_process_hook(processing_input)
            
            # Main data processing
            processed_data = self.process_data(preprocessing_result)
            
            # Post-processing hook
            final_processed_data = self.post_process_hook(processed_data, processing_input)
            
            # Format output
            formatted_output = self.format_output_data(final_processed_data)
            
            # Store result
            self.last_execution_result = formatted_output
            self.processed_data_count += 1
            
            # Record success
            self.execution_run_success_statuses.append(True)
            
            if measure_execution_time:
                execution_time = time.time() * 1000 - start_time
                self.execution_timings_milliseconds.append(execution_time)
            
            # Call completion callback if available
            if self.on_execution_complete_callback is not None:
                await self.on_execution_complete_callback(self)
            
            return True
            
        except Exception as e:
            error_message = f"Error executing data processing node {self.node_id}: {str(e)}"
            
            if self.node_log_errors:
                self.log_node_error(error_message)
            
            self.processing_errors.append(error_message)
            self.execution_run_success_statuses.append(False)
            
            if measure_execution_time:
                execution_time = time.time() * 1000 - start_time
                self.execution_timings_milliseconds.append(execution_time)
            
            return False

    def get_processing_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics for this node.
        
        Returns:
            Dictionary containing processing statistics
        """
        return {
            'node_id': self.node_id,
            'processed_data_count': self.processed_data_count,
            'processing_errors_count': len(self.processing_errors),
            'recent_errors': self.processing_errors[-5:] if self.processing_errors else [],
            'last_processing_metadata': self.last_processing_metadata,
            'average_execution_time_ms': self.get_average_execution_time_milliseconds(),
            'last_execution_time_ms': self.get_last_measured_execution_time_milliseconds()
        }

    def reset_processing_statistics(self):
        """Reset processing statistics and error logs."""
        self.processed_data_count = 0
        self.processing_errors.clear()
        self.last_processing_metadata = None

    def set_processing_metadata(self, metadata: Dict[str, Any]):
        """
        Set metadata for the current processing operation.
        
        Args:
            metadata: Metadata dictionary
        """
        self.last_processing_metadata = metadata