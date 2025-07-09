#!/usr/bin/env python3
"""
Script to fix the OpenSearch index mapping for proper KNN vector search.
This script will delete the existing index and recreate it with the correct mapping.
"""

import embedding
from opensearchpy import OpenSearch

def get_opensearch_client():
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=None,
        use_ssl=False,
        verify_certs=False,
    )
    return client

def recreate_index_with_proper_mapping():
    """
    Delete the existing index and recreate it with proper knn_vector mapping.
    """
    client = get_opensearch_client()
    index_name = "document"
    
    # Check if index exists and delete it
    if client.indices.exists(index=index_name):
        print(f"Deleting existing index: {index_name}")
        client.indices.delete(index=index_name)
    
    # Create index with proper mapping for KNN vector search
    mapping = {
        "settings": {
            "index": {
                "knn": True,  # Enable KNN for this index
                "knn.algo_param.ef_search": 100
            }
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 768,  # Based on your nomic-embed model
                    "method": {
                        "name": "hnsw",
                        "space_type": "cosinesimil",  # or "l2" for Euclidean distance
                        "engine": "lucene",  # Use lucene instead of deprecated nmslib
                        "parameters": {
                            "ef_construction": 128,
                            "m": 24
                        }
                    }
                }
            }
        }
    }
    
    print(f"Creating new index: {index_name} with proper KNN mapping")
    client.indices.create(index=index_name, body=mapping)
    print("Index created successfully!")
    
    # Verify the new mapping
    mapping_result = client.indices.get_mapping(index=index_name)
    print(f"New mapping: {mapping_result}")

if __name__ == "__main__":
    recreate_index_with_proper_mapping()
