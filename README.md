# Skymel Python Library

A Python implementation of the Skymel Agent Development Kit, providing similar functionality to the JavaScript ADK for creating and managing AI agents with execution control graphs.

## Overview

This library allows you to:
- Create dynamic AI agents with configurable behaviors
- Build execution control graphs for complex workflows  
- Load and execute graph configurations from JSON
- Manage agent lifecycle and execution contexts

## Key Components

### Core Classes

- **`SkymelAgent`** - Main entry point for creating AI agents
- **`SkymelECGraph`** - Execution control graph for managing workflows
- **`SkymelECGraphNode`** - Base class for individual nodes in execution graphs
- **`SkymelECGraphNodeForDataProcessing`** - Base class for data processing nodes
- **`SkymelECGraphNodeForExternalApiCall`** - Node for making external API calls
- **`SkymelExecutionGraphLoader`** - Utilities for loading graphs from JSON

### Utility Classes

- **`SkymelECGraphUtils`** - Graph and node type constants and utilities
- **`CommonValidators`** - Data validation utilities
- **`CommonGraphAlgorithms`** - Graph algorithms (topological sort, cycle detection, etc.)
- **`CommonHashUtils`** - Hash and ID generation utilities

## Installation

```python
# Add the skymel directory to your Python path or install as a package
import sys
sys.path.append('/path/to/skymel')

from skymel import SkymelAgent, SkymelECGraph
```

## Basic Usage

### Creating an Agent

```python
from skymel import SkymelAgent

agent = SkymelAgent(
    api_key="your-api-key",
    agent_name_string="MyAgent",
    agent_definition_string="An agent that processes text",
    agent_restrictions_string="Follow safety guidelines"
)
```

### Creating and Executing a Graph

```python
import asyncio
from skymel import SkymelECGraph, SkymelECGraphNode

async def main():
    # Create a graph
    graph_config = {
        'graphId': 'my_graph',
        'externalInputNames': ['external.input']
    }
    graph = SkymelECGraph(graph_config)
    
    # Define a node subroutine
    async def process_text(inputs):
        text = inputs.get('external.input', '')
        return {'result': f"Processed: {text}"}
    
    # Create and add a node
    node_config = {
        'nodeId': 'processor',
        'nodeInputNames': ['external.input'],
        'nodeOutputNames': ['result'],
        'nodeSubroutine': process_text
    }
    node = SkymelECGraphNode(node_config)
    graph.add_node(node)
    
    # Execute the graph
    execution_config = {
        'externalInputNamesToValuesDict': {
            'external.input': 'Hello World!'
        }
    }
    
    success = await graph.execute_graph(execution_config)
    if success:
        result = graph.get_last_execution_result()
        print(result)

asyncio.run(main())
```

### Loading from JSON

```python
from skymel import SkymelExecutionGraphLoader

json_config = {
    'graphType': 'base',
    'graphInitializationConfig': {
        'graphId': 'loaded_graph',
        'externalInputNames': ['external.text']
    },
    'children': [
        {
            'nodeType': 'base', 
            'nodeInitializationConfig': {
                'nodeId': 'my_node',
                'nodeInputNames': ['external.text'],
                'nodeOutputNames': ['output'],
                'nodeSubroutine': lambda x: {'output': 'Hello from JSON!'}
            }
        }
    ]
}

graph = SkymelExecutionGraphLoader.load_graph_from_json_object(json_config)
```

### Using External API Call Nodes

```python
from skymel import SkymelECGraphNodeForExternalApiCall, SkymelECGraph

# Create external API call node
api_config = {
    'nodeId': 'openai_node',
    'nodeInputNames': ['external.prompt'],
    'nodeOutputNames': ['response'],
    'endpointUrl': 'https://api.openai.com/v1/chat/completions',
    'apiKey': 'your-api-key',
    'nodeInputNameToBackendInputNameMap': {
        'external.prompt': 'messages'
    },
    'backendOutputNameToNodeOutputNameMap': {
        'choices': 'openai_node.response'
    },
    'nodePrivateAttributesAndValues': {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.7
    }
}

api_node = SkymelECGraphNodeForExternalApiCall(api_config)

# Add to graph and execute
graph = SkymelECGraph({'graphId': 'api_graph', 'externalInputNames': ['external.prompt']})
graph.add_node(api_node)
```

### Creating Custom Data Processing Nodes

```python
from skymel import SkymelECGraphNodeForDataProcessing

class CustomProcessor(SkymelECGraphNodeForDataProcessing):
    def process_data(self, input_data):
        # Custom processing logic
        text = input_data.get('external.text', '')
        return {'processed': text.upper()}

# Use in graph
processor_config = {
    'nodeId': 'custom_processor',
    'nodeInputNames': ['external.text'],
    'nodeOutputNames': ['processed']
}

processor = CustomProcessor(processor_config)
```

## Features Implemented

✅ **Core Graph Functionality**
- Graph creation and management
- Node addition and execution
- Topological sorting for execution order
- Graph validation and dependency checking

✅ **Agent Management**
- Agent creation with configurable parameters
- Developer configuration strings
- File attachment processing
- Workflow generation and caching

✅ **Execution Control**
- Asynchronous graph execution
- Input/output value mapping
- Error handling and logging
- Execution timing measurement

✅ **JSON Configuration**
- Graph loading from JSON objects
- Node type validation
- Configuration validation utilities

✅ **Specialized Node Types**
- Data processing base class with validation and formatting
- External API call nodes with HTTP/WebSocket support
- Input/output mapping for API integration
- Retry logic and error handling for API calls

✅ **Utility Functions**
- Graph algorithms (DFS, topological sort, cycle detection)
- Data validation (types, formats, structures)
- Hash generation and unique ID creation
- File processing utilities

## Comparison with JavaScript ADK

| Feature | JavaScript ADK | Python Library | Status |
|---------|----------------|----------------|--------|
| SkymelAgent | ✅ | ✅ | Complete |
| SkymelECGraph | ✅ | ✅ | Complete |
| SkymelECGraphNode | ✅ | ✅ | Complete |
| Graph Execution | ✅ | ✅ | Complete |
| JSON Loading | ✅ | ✅ | Complete |
| File Processing | ✅ | ✅ | Complete |
| Specialized Nodes | ✅ | ✅ | Data processing & API call nodes |
| WebSocket Support | ✅ | ⚠️ | Needs HTTP client |
| Model Runners | ✅ | ❌ | Not implemented |

## Extending the Library

### Adding Custom Node Types

```python
from skymel import SkymelECGraphNode

class CustomProcessorNode(SkymelECGraphNode):
    async def execute(self, parent_graph, input_values, measure_execution_time=True):
        # Custom execution logic
        result = {'custom_output': 'Custom processing result'}
        self.last_execution_result = result
        return True
```

### Adding Custom Graph Types  

```python
from skymel import SkymelECGraph

class CustomGraph(SkymelECGraph):
    def get_graph_type(self):
        return "custom_graph_type"
    
    async def custom_execution_logic(self):
        # Custom graph execution behavior
        pass
```

## Testing

Run the example script to test the basic functionality:

```bash
python example_usage.py
```

## Limitations and Future Work

1. **Network Communication**: The library currently lacks HTTP/WebSocket clients for actual agent communication
2. **Model Runners**: ONNX, TensorFlow, and other model runner nodes are not implemented
3. **Specialized Nodes**: Only base nodes are implemented; specialized nodes for inference, API calls, etc. need to be added
4. **Error Recovery**: Advanced error recovery and retry mechanisms could be enhanced
5. **Performance**: Optimization for large graphs and parallel execution

## Contributing

To extend this library:

1. Follow the existing code patterns and naming conventions
2. Add type hints for all methods and parameters  
3. Include docstrings following the existing format
4. Test new functionality with example scripts
5. Update this README with new features

## License

This library follows the same license as the original Skymel ADK.