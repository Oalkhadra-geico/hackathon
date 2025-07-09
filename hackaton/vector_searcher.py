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

def search_similar(question, index, top_k=3):
    """
    Search for similar documents in OpenSearch using a vector query.

    :param index: The name of the index to search.
    :param query_vector: The vector to search for similar documents.
    :param top_k: The number of similar documents to return.
    :return: Search results from OpenSearch.
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
    #print(hits)
    return [hit["_source"] for hit in hits]

if __name__ == "__main__":
    question = "What is the  broaden our Vacation Liability?"
    index = "document"
    results = search_similar(question, index)
    for result in results:
        print(result)