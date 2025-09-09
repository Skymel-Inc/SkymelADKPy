#!/usr/bin/env python3
"""
Example usage of SkymelECGraphNodeForExternalApiCall
"""

import asyncio
import json
from skymel import (
    SkymelECGraph, 
    SkymelECGraphNodeForExternalApiCall,
    SkymelECGraphNodeForDataProcessing,
    SkymelExecutionGraphLoader
)

async def main():
    """
    Example demonstrating how to use the external API call nodes
    """
    
    # Example 1: Direct external API call node usage
    print("=== Example 1: Direct External API Call Node ===")
    
    try:
        # Create an external API call node configuration
        api_node_config = {
            'nodeId': 'api_caller_node',
            'nodeInputNames': ['external.prompt'],
            'nodeOutputNames': ['response', 'metadata'],
            'endpointUrl': 'https://api.example.com/chat',  # Replace with actual endpoint
            'apiKey': 'your-api-key-here',  # Replace with actual API key
            'isEndpointWebSocketUrl': False,
            'nodeInputNameToBackendInputNameMap': {
                'external.prompt': 'message'
            },
            'backendOutputNameToNodeOutputNameMap': {
                'response': 'api_caller_node.response',
                'result': 'api_caller_node.metadata'
            },
            'nodePrivateAttributesAndValues': {
                'model': 'gpt-3.5-turbo',
                'temperature': 0.7,
                'max_tokens': 150
            },
            'requestTimeout': 30.0,
            'maxRetries': 3
        }
        
        # Create the node
        api_node = SkymelECGraphNodeForExternalApiCall(api_node_config)
        
        print(f"API Node created: {api_node.get_node_id()}")
        print(f"Endpoint: {api_node.endpoint_url}")
        print(f"Input mappings: {api_node.node_input_name_to_backend_input_name_map}")
        
        # Note: To actually test this, you'd need a real API endpoint
        print("(Note: This example uses a placeholder API endpoint)")
        
    except Exception as e:
        print(f"Error creating API node: {e}")
    
    # Example 2: Create a graph with external API call using JSON configuration
    print("\n=== Example 2: Graph with External API Call from JSON ===")
    
    try:
        # JSON configuration for a graph with an external API call node
        graph_config = {
            'graphType': 'base',
            'graphInitializationConfig': {
                'graphId': 'api_test_graph',
                'externalInputNames': ['external.user_input']
            },
            'children': [
                {
                    'nodeType': 'externalApiCaller',
                    'nodeInitializationConfig': {
                        'nodeId': 'openai_api_node',
                        'nodeInputNames': ['external.user_input'],
                        'nodeOutputNames': ['ai_response'],
                        'endpointUrl': 'https://api.openai.com/v1/chat/completions',
                        'apiKey': 'your-openai-api-key',
                        'nodeInputNameToBackendInputNameMap': {
                            'external.user_input': 'messages'
                        },
                        'backendOutputNameToNodeOutputNameMap': {
                            'choices': 'openai_api_node.ai_response'
                        },
                        'nodePrivateAttributesAndValues': {
                            'model': 'gpt-3.5-turbo',
                            'temperature': 0.7,
                            'max_tokens': 100
                        }
                    }
                }
            ]
        }
        
        # Load the graph
        graph = SkymelExecutionGraphLoader.load_graph_from_json_object(graph_config)
        
        if graph:
            print(f"Graph loaded successfully: {graph.get_graph_id()}")
            print(f"Graph nodes: {graph.get_list_of_all_node_ids()}")
            
            # Check if graph is valid
            is_valid = await graph.is_graph_valid()
            print(f"Graph is valid: {is_valid}")
            
            if is_valid:
                print("Graph is ready for execution (requires valid API key and endpoint)")
        else:
            print("Failed to load graph from JSON")
            
    except Exception as e:
        print(f"Error loading graph: {e}")
    
    # Example 3: Data processing node with custom processing
    print("\n=== Example 3: Custom Data Processing Node ===")
    
    class CustomTextProcessor(SkymelECGraphNodeForDataProcessing):
        def process_data(self, input_data):
            """Custom text processing logic."""
            if not input_data:
                return "No input provided"
            
            # Extract text from input
            text = input_data.get('external.text', '')
            
            # Custom processing: uppercase and add prefix
            processed = f"PROCESSED: {text.upper()}"
            
            return {
                'processed_text': processed,
                'original_length': len(text),
                'processed_length': len(processed)
            }
    
    try:
        # Create custom processor configuration
        processor_config = {
            'nodeId': 'custom_text_processor',
            'nodeInputNames': ['external.text'],
            'nodeOutputNames': ['processed_text', 'original_length', 'processed_length'],
            'dataProcessingConfig': {
                'inputValidationEnabled': True,
                'outputFormattingEnabled': True,
                'errorHandlingMode': 'strict'
            }
        }
        
        # Create the custom processor
        processor = CustomTextProcessor(processor_config)
        
        # Create a simple graph with the processor
        simple_graph_config = {
            'graphId': 'text_processing_graph',
            'externalInputNames': ['external.text']
        }
        
        graph = SkymelECGraph(simple_graph_config)
        graph.add_node(processor)
        
        print(f"Custom processor graph created: {graph.get_graph_id()}")
        
        # Execute the graph
        is_valid = await graph.is_graph_valid()
        if is_valid:
            execution_config = {
                'externalInputNamesToValuesDict': {
                    'external.text': 'Hello, this is a test message!'
                }
            }
            
            success = await graph.execute_graph(execution_config)
            if success:
                result = graph.get_last_execution_result()
                print(f"Processing result: {json.dumps(result, indent=2)}")
                
                # Get processing statistics
                stats = processor.get_processing_statistics()
                print(f"Processing statistics: {json.dumps(stats, indent=2)}")
        
    except Exception as e:
        print(f"Error with custom processor: {e}")
    
    # Example 4: Mock external API for testing
    print("\n=== Example 4: Mock External API for Testing ===")
    
    class MockApiNode(SkymelECGraphNodeForExternalApiCall):
        """Mock API node that simulates external API calls without network requests."""
        
        async def make_http_request(self, payload):
            """Override to simulate API response."""
            # Simulate processing time
            await asyncio.sleep(0.1)
            
            # Mock response based on payload
            mock_response = {
                'response': f"Mock API processed: {payload.get('message', 'no message')}",
                'status': 'success',
                'timestamp': '2024-01-01T00:00:00Z'
            }
            
            self.last_response_time = 100  # Mock 100ms response time
            self.last_status_code = 200
            
            return mock_response
    
    try:
        # Create mock API node
        mock_config = {
            'nodeId': 'mock_api_node',
            'nodeInputNames': ['external.input'],
            'nodeOutputNames': ['response'],
            'endpointUrl': 'https://mock-api.example.com/test',
            'nodeInputNameToBackendInputNameMap': {
                'external.input': 'message'
            },
            'backendOutputNameToNodeOutputNameMap': {
                'response': 'mock_api_node.response'
            }
        }
        
        mock_node = MockApiNode(mock_config)
        
        # Create graph with mock node
        mock_graph_config = {
            'graphId': 'mock_api_graph',
            'externalInputNames': ['external.input']
        }
        
        mock_graph = SkymelECGraph(mock_graph_config)
        mock_graph.add_node(mock_node)
        
        # Execute the mock graph
        is_valid = await mock_graph.is_graph_valid()
        if is_valid:
            execution_config = {
                'externalInputNamesToValuesDict': {
                    'external.input': 'Test message for mock API'
                }
            }
            
            success = await mock_graph.execute_graph(execution_config)
            if success:
                result = mock_graph.get_last_execution_result()
                print(f"Mock API result: {json.dumps(result, indent=2)}")
                
                # Get API statistics
                api_stats = mock_node.get_api_statistics()
                print(f"Mock API statistics: {json.dumps(api_stats, indent=2)}")
        
    except Exception as e:
        print(f"Error with mock API: {e}")

if __name__ == "__main__":
    asyncio.run(main())