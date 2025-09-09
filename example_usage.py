#!/usr/bin/env python3
"""
Example usage of the Python Skymel Agent Development Kit
"""

import asyncio
from skymel import SkymelAgent, SkymelECGraph, SkymelECGraphNode, SkymelExecutionGraphLoader

async def main():
    """
    Example demonstrating how to use the Skymel Python library
    """
    
    # Example 1: Create a SkymelAgent
    print("=== Example 1: Creating a SkymelAgent ===")
    agent = SkymelAgent(
        api_key="your-api-key-here",
        agent_name_string="TestAgent",
        agent_definition_string="A test agent for demonstration purposes",
        agent_restrictions_string="Follow all safety guidelines"
    )
    
    print(f"Agent created with endpoint: {agent.get_agent_creation_endpoint_url()}")
    print(f"Developer config: {agent.agent_developer_configuration_string}")
    
    # Example 2: Create a simple execution graph manually
    print("\n=== Example 2: Creating a simple execution graph ===")
    
    # Define a simple node subroutine
    async def simple_processor(inputs=None):
        if inputs and 'text' in inputs:
            return {'processed_text': f"Processed: {inputs['text']}"}
        return {'processed_text': "Processed: default text"}
    
    # Create graph configuration
    graph_config = {
        'graphId': 'simple_test_graph',
        'externalInputNames': ['external.text']
    }
    
    # Create the graph
    graph = SkymelECGraph(graph_config)
    
    # Create and add a node
    node_config = {
        'nodeId': 'processor_node',
        'nodeInputNames': ['external.text'],
        'nodeOutputNames': ['processed_text'],
        'nodeSubroutine': simple_processor
    }
    
    node = SkymelECGraphNode(node_config)
    graph.add_node(node)
    
    print(f"Graph created with ID: {graph.get_graph_id()}")
    print(f"Graph nodes: {graph.get_list_of_all_node_ids()}")
    
    # Example 3: Execute the graph
    print("\n=== Example 3: Executing the graph ===")
    
    try:
        # Check if graph is valid
        is_valid = await graph.is_graph_valid()
        print(f"Graph is valid: {is_valid}")
        
        if is_valid:
            # Execute with inputs
            execution_config = {
                'externalInputNamesToValuesDict': {
                    'external.text': 'Hello, Skymel!'
                }
            }
            
            success = await graph.execute_graph(execution_config)
            print(f"Execution succeeded: {success}")
            
            if success:
                result = graph.get_last_execution_result()
                print(f"Execution result: {result}")
        
    except Exception as e:
        print(f"Error during execution: {e}")
    
    # Example 4: Load graph from JSON configuration  
    print("\n=== Example 4: Loading graph from JSON ===")
    
    json_config = {
        'graphType': 'base',
        'graphInitializationConfig': {
            'graphId': 'json_loaded_graph',
            'externalInputNames': ['external.input']
        },
        'children': [
            {
                'nodeType': 'base',
                'nodeInitializationConfig': {
                    'nodeId': 'test_node',
                    'nodeInputNames': ['external.input'],
                    'nodeOutputNames': ['output'],
                    'nodeSubroutine': lambda x=None: {'output': 'JSON loaded node executed!'}
                }
            }
        ]
    }
    
    try:
        loaded_graph = SkymelExecutionGraphLoader.load_graph_from_json_object(json_config)
        if loaded_graph:
            print(f"Successfully loaded graph from JSON: {loaded_graph.get_graph_id()}")
            print(f"Loaded graph nodes: {loaded_graph.get_list_of_all_node_ids()}")
        else:
            print("Failed to load graph from JSON")
    except Exception as e:
        print(f"Error loading from JSON: {e}")

if __name__ == "__main__":
    asyncio.run(main())