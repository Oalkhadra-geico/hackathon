from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import agent
import completion
import vector_searcher
import embedding
from opensearchpy import OpenSearch
import json
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Flask doesn't use the standard json.JSONEncoder, so we'll handle NaN values
# in our data processing functions instead

def get_opensearch_client():
    """Get OpenSearch client"""
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=None,
        use_ssl=False,
        verify_certs=False,
    )
    return client

def clean_data_for_json(data):
    """
    Clean data to make it JSON serializable by replacing NaN values with None.
    
    Args:
        data: list of dictionaries
        
    Returns:
        list: Cleaned data with NaN values replaced by None
    """
    cleaned_records = []
    for record in data:
        cleaned_record = {}
        for key, value in record.items():
            if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
                cleaned_record[key] = None
            else:
                cleaned_record[key] = value
        cleaned_records.append(cleaned_record)
    
    return cleaned_records

def process_filtered_data(filtered_data):
    """Process filtered data and create context for the LLM"""
    if not filtered_data:
        return ""
    
    # Clean the data to handle any NaN values
    cleaned_data = clean_data_for_json(filtered_data)
    
    # Convert filtered data to context string
    context_parts = []
    for record in cleaned_data:
        # Create a context string from the record
        context_str = f"Record: {json.dumps(record, default=str)}"
        context_parts.append(context_str)
    
    return "\n\n".join(context_parts)

@app.route('/query', methods=['POST'])
def handle_query():
    """Handle query requests from the frontend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        query = data.get('query', '')
        filtered_data = data.get('filtered_data', [])
        filter_summary = data.get('filter_summary', {})
        
        print(f"Received query: {query}")
        print(f"Filtered data length: {len(filtered_data)}")
        print(f"Filter summary: {filter_summary}")
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        if not filtered_data:
            return jsonify({"error": "No filtered data provided"}), 400
        
        # Process the filtered data to create context
        data_context = process_filtered_data(filtered_data)
        
        # Create a comprehensive prompt that includes both the filtered data and the query
        prompt = f"""You are an AI assistant specialized in analyzing DOI (Department of Insurance) objection data.

Filter Summary:
- Total Records: {filter_summary.get('total_records', 0)}
- States: {', '.join(filter_summary.get('states', []))}
- Line of Business: {', '.join(filter_summary.get('lobs', []))}
- Filing Types: {', '.join(filter_summary.get('filing_types', []))}
- Response Types: {', '.join(filter_summary.get('response_types', []))}
- Topics: {', '.join(filter_summary.get('topics', []))}
- Carriers: {', '.join(filter_summary.get('carriers', []))}

Filtered Data Context:
{data_context}

User Query: {query}

Please provide a comprehensive analysis based on the filtered data and the user's query. Focus on patterns, insights, and actionable information from the DOI objection data."""

        print(f"Sending prompt to LLM (length: {len(prompt)})")
        
        # Call the LLM
        response = completion.call_llm(prompt)
        
        result = {
            "response": response,
            "query": query,
            "filter_summary": filter_summary,
            "records_analyzed": len(filtered_data)
        }
        
        print(f"Successfully processed query, returning response")
        return jsonify(result)
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return jsonify({"error": f"Invalid JSON data: {str(e)}"}), 400
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return jsonify({"error": f"Error processing query: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Backend server is running"})

if __name__ == '__main__':
    print("Starting backend server on http://localhost:5000")
    print("Make sure OpenSearch is running on localhost:9200")
    app.run(host='0.0.0.0', port=5000, debug=True)