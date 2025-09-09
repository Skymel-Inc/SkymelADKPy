import json
import time
import asyncio
from typing import Dict, List, Optional, Any, Union
from .skymelECGraphNodeForDataProcessing import SkymelECGraphNodeForDataProcessing
from .commonValidators import CommonValidators


class SkymelECGraphNodeForExternalApiCall(SkymelECGraphNodeForDataProcessing):
    """
    Node for making external API calls within a SkymelECGraph.
    
    This class extends SkymelECGraphNodeForDataProcessing to provide functionality
    for calling external APIs, handling authentication, request/response mapping,
    and managing WebSocket connections.
    """
    
    def __init__(self, initialization_config: Dict):
        """
        Initialize an external API call node.
        
        Args:
            initialization_config: Configuration dictionary for node initialization
        """
        super().__init__(initialization_config)
        
        # API configuration
        self.endpoint_url = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'endpointUrl', None
        )
        
        self.api_key = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'apiKey', None
        )
        
        self.is_endpoint_websocket_url = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'isEndpointWebSocketUrl', False
        )
        
        # Input/Output mapping configuration
        self.node_input_name_to_backend_input_name_map = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodeInputNameToBackendInputNameMap', {}
        )
        
        self.backend_output_name_to_node_output_name_map = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'backendOutputNameToNodeOutputNameMap', {}
        )
        
        # Private attributes and values (for context, developer prompts, etc.)
        self.node_private_attributes_and_values = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'nodePrivateAttributesAndValues', {}
        )
        
        # Request configuration
        self.request_timeout = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'requestTimeout', 30.0
        )
        
        self.max_retries = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'maxRetries', 3
        )
        
        self.retry_delay = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'retryDelay', 1.0
        )
        
        # Headers configuration
        self.default_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Skymel-Python-Client/1.0'
        }
        
        if self.api_key:
            self.default_headers['Authorization'] = f'Bearer {self.api_key}'
        
        # Additional headers from config
        additional_headers = CommonValidators.get_key_value_from_dict_or_return_default_on_key_not_found(
            initialization_config, 'headers', {}
        )
        self.default_headers.update(additional_headers)
        
        # API call statistics
        self.api_call_count = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.last_response_time = 0.0
        self.last_status_code = None
        self.last_error_message = None

    def validate_api_configuration(self) -> bool:
        """
        Validate that the API configuration is complete and valid.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not CommonValidators.is_non_empty_string(self.endpoint_url):
            self.last_error_message = "Missing or invalid endpoint URL"
            return False
        
        if not CommonValidators.is_url(self.endpoint_url) and not self.endpoint_url.startswith('/'):
            self.last_error_message = "Invalid endpoint URL format"
            return False
        
        return True

    def map_node_inputs_to_backend_inputs(self, node_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map node input names to backend input names.
        
        Args:
            node_inputs: Dictionary of node inputs
            
        Returns:
            Dictionary with mapped backend input names
        """
        backend_inputs = {}
        
        if not node_inputs:
            return backend_inputs
        
        for node_input_name, value in node_inputs.items():
            # Check if there's a mapping for this input
            if node_input_name in self.node_input_name_to_backend_input_name_map:
                backend_name = self.node_input_name_to_backend_input_name_map[node_input_name]
                backend_inputs[backend_name] = value
            else:
                # Use the node input name as-is if no mapping exists
                backend_inputs[node_input_name] = value
        
        return backend_inputs

    def map_backend_outputs_to_node_outputs(self, backend_outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map backend output names to node output names.
        
        Args:
            backend_outputs: Dictionary of backend outputs
            
        Returns:
            Dictionary with mapped node output names
        """
        node_outputs = {}
        
        if not backend_outputs:
            return node_outputs
        
        for backend_output_name, value in backend_outputs.items():
            # Check if there's a mapping for this output
            if backend_output_name in self.backend_output_name_to_node_output_name_map:
                node_name = self.backend_output_name_to_node_output_name_map[backend_output_name]
                node_outputs[node_name] = value
            else:
                # Use the backend output name as-is if no mapping exists
                node_outputs[backend_output_name] = value
        
        return node_outputs

    def build_request_payload(self, backend_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build the request payload for the API call.
        
        Args:
            backend_inputs: Mapped backend inputs
            
        Returns:
            Request payload dictionary
        """
        payload = {}
        
        # Add mapped inputs
        payload.update(backend_inputs)
        
        # Add private attributes and values
        if self.node_private_attributes_and_values:
            payload.update(self.node_private_attributes_and_values)
        
        return payload

    async def make_http_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an HTTP request to the API endpoint.
        
        Args:
            payload: Request payload
            
        Returns:
            Response data dictionary
        """
        try:
            import aiohttp
        except ImportError:
            raise ImportError("aiohttp is required for HTTP requests. Install with: pip install aiohttp")
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.request_timeout)) as session:
            try:
                async with session.post(
                    self.endpoint_url,
                    json=payload,
                    headers=self.default_headers
                ) as response:
                    self.last_response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                    self.last_status_code = response.status
                    
                    if response.status == 200:
                        response_data = await response.json()
                        self.successful_calls += 1
                        return response_data
                    else:
                        error_text = await response.text()
                        error_msg = f"HTTP {response.status}: {error_text}"
                        self.last_error_message = error_msg
                        raise RuntimeError(error_msg)
                        
            except asyncio.TimeoutError:
                self.last_error_message = f"Request timeout after {self.request_timeout} seconds"
                raise RuntimeError(self.last_error_message)
            except Exception as e:
                self.last_error_message = f"HTTP request error: {str(e)}"
                raise RuntimeError(self.last_error_message)

    async def make_websocket_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a WebSocket request to the API endpoint.
        
        Args:
            payload: Request payload
            
        Returns:
            Response data dictionary
        """
        try:
            import websockets
        except ImportError:
            raise ImportError("websockets is required for WebSocket connections. Install with: pip install websockets")
        
        start_time = time.time()
        
        try:
            # Convert HTTP URL to WebSocket URL if needed
            ws_url = self.endpoint_url
            if ws_url.startswith('http://'):
                ws_url = ws_url.replace('http://', 'ws://', 1)
            elif ws_url.startswith('https://'):
                ws_url = ws_url.replace('https://', 'wss://', 1)
            
            async with websockets.connect(
                ws_url,
                timeout=self.request_timeout,
                extra_headers=self.default_headers
            ) as websocket:
                # Send the payload
                await websocket.send(json.dumps(payload))
                
                # Receive the response
                response_text = await websocket.recv()
                
                self.last_response_time = (time.time() - start_time) * 1000
                
                try:
                    response_data = json.loads(response_text)
                    self.successful_calls += 1
                    return response_data
                except json.JSONDecodeError:
                    # Return as text if not valid JSON
                    return {'response': response_text}
                    
        except Exception as e:
            self.last_error_message = f"WebSocket request error: {str(e)}"
            raise RuntimeError(self.last_error_message)

    async def make_api_call_with_retries(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API call with retry logic.
        
        Args:
            payload: Request payload
            
        Returns:
            Response data dictionary
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if self.is_endpoint_websocket_url:
                    return await self.make_websocket_request(payload)
                else:
                    return await self.make_http_request(payload)
                    
            except Exception as e:
                last_exception = e
                self.failed_calls += 1
                
                if attempt < self.max_retries:
                    # Wait before retrying
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    # Final attempt failed
                    break
        
        # All retries failed
        raise last_exception or RuntimeError("API call failed after all retries")

    def process_data(self, input_data: Any) -> Any:
        """
        Process data by making an external API call.
        This method is called by the parent class during execution.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processed data from API response
        """
        # This method is synchronous, but we need async for API calls
        # The actual API call will be made in the execute method
        return input_data

    async def execute(self, parent_graph, input_values: Dict = None, measure_execution_time: bool = True) -> bool:
        """
        Execute the external API call node.
        
        Args:
            parent_graph: The parent graph containing this node
            input_values: Input values for the node
            measure_execution_time: Whether to measure execution time
            
        Returns:
            True if execution succeeded, False otherwise
        """
        start_time = time.time() * 1000 if measure_execution_time else None
        
        try:
            # Validate API configuration
            if not self.validate_api_configuration():
                if self.node_log_errors:
                    self.log_node_error(self.last_error_message)
                self.execution_run_success_statuses.append(False)
                return False
            
            # Validate inputs
            if not self.validate_input_data(input_values):
                error_msg = "Input validation failed"
                if self.node_log_errors:
                    self.log_node_error(error_msg)
                self.execution_run_success_statuses.append(False)
                return False
            
            self.api_call_count += 1
            
            # Map node inputs to backend inputs
            backend_inputs = self.map_node_inputs_to_backend_inputs(input_values or {})
            
            # Build request payload
            request_payload = self.build_request_payload(backend_inputs)
            
            # Set processing metadata
            self.set_processing_metadata({
                'api_call_count': self.api_call_count,
                'endpoint_url': self.endpoint_url,
                'is_websocket': self.is_endpoint_websocket_url,
                'request_payload_size': len(json.dumps(request_payload))
            })
            
            # Make API call with retries
            api_response = await self.make_api_call_with_retries(request_payload)
            
            # Map backend outputs to node outputs
            mapped_outputs = self.map_backend_outputs_to_node_outputs(api_response)
            
            # Format final output
            formatted_output = self.format_output_data(mapped_outputs)
            
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
            error_message = f"Error executing external API call node {self.node_id}: {str(e)}"
            
            if self.node_log_errors:
                self.log_node_error(error_message)
            
            self.processing_errors.append(error_message)
            self.execution_run_success_statuses.append(False)
            self.failed_calls += 1
            
            if measure_execution_time:
                execution_time = time.time() * 1000 - start_time
                self.execution_timings_milliseconds.append(execution_time)
            
            return False

    def get_api_statistics(self) -> Dict[str, Any]:
        """
        Get API call statistics for this node.
        
        Returns:
            Dictionary containing API call statistics
        """
        base_stats = self.get_processing_statistics()
        
        api_stats = {
            'api_call_count': self.api_call_count,
            'successful_calls': self.successful_calls,
            'failed_calls': self.failed_calls,
            'success_rate': (self.successful_calls / self.api_call_count) if self.api_call_count > 0 else 0,
            'last_response_time_ms': self.last_response_time,
            'last_status_code': self.last_status_code,
            'last_error_message': self.last_error_message,
            'endpoint_url': self.endpoint_url,
            'is_websocket': self.is_endpoint_websocket_url
        }
        
        base_stats.update(api_stats)
        return base_stats

    def reset_api_statistics(self):
        """Reset API call statistics."""
        self.reset_processing_statistics()
        self.api_call_count = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.last_response_time = 0.0
        self.last_status_code = None
        self.last_error_message = None