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

def search_similar_with_script_score(question, index, top_k=3):
    """
    Alternative search method using script_score query for vector similarity.
    This works with the current mapping where embedding is stored as float array.
    """
    client = get_opensearch_client()
    query_vector = embedding.generate_embedding(question)
    
    # Use script_score query instead of knn query
    search_body = {
        "size": top_k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }

    response = client.search(index=index, body=search_body)
    hits = response["hits"]["hits"]
    print("Script score search results:")
    print(hits)
    return [hit["_source"] for hit in hits]

def search_similar(question, index, top_k=3):
    """
    Search for similar documents in OpenSearch using a vector query.
    This is the original function that requires proper knn_vector mapping.
    """
    client = get_opensearch_client()
    query_vector = embedding.generate_embedding(question)
    search_body = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_vector,
                    "k": top_k
                }
            }
        }
    }

    response = client.search(index=index, body=search_body)
    hits = response["hits"]["hits"]
    print("KNN search results:")
    print(hits)
    return [hit["_source"] for hit in hits]

if __name__ == "__main__":
    question = "What is the broaden our Vacation Liability?"
    index = "document"
    
    print("=== Testing with script_score (works with current mapping) ===")
    try:
        results = search_similar_with_script_score(question, index)
        for result in results:
            print(result)
    except Exception as e:
        print(f"Script score search failed: {e}")
    
    print("\n=== Testing with knn (requires proper mapping) ===")
    try:
        results = search_similar(question, index)
        for result in results:
            print(result)
    except Exception as e:
        print(f"KNN search failed: {e}")
