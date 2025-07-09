import requests

def generate_embedding(prompt: str) -> list:
    """
    Sends a request to the embedding API and retrieves the embedding data.

    :param prompt: The input text for which the embedding is generated.
    :return: A list representing the embedding vector.
    """
    #print(f"Embedding rawdata: {prompt}")
    response = requests.post(
        "https://trussedaisb1.geico.net/provider/generic/embeddings",
        json={
            "model": "nomic-embed",
            "input": [prompt],
        },
        headers={
            "Authorization": "Bearer gS8QX3YfEdPoFnJT7eIM2RLXmXDpiGfxbDodqLuTwiyZ82gU",
            "Content-Type": "application/json",
        }
    )
    
    # Check if the response is successful
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve embedding: {response.status_code} - {response.text}")
    
    # Extract the embedding data from the response
    embedding_data = response.json().get("data", [{}])[0].get("embedding", [])   
    if isinstance(embedding_data, list) and len(embedding_data) == 1 and isinstance(embedding_data[0], list):
        embedding_data = embedding_data[0]
    if not all(isinstance(x, float) for x in embedding_data):
        print(f"Embedding data contains non-float values: {embedding_data}")
        return []
    return embedding_data

if __name__ == "__main__":
    prompt = "Please attach the Underwriting Placement Addendum under the Rate/Rule Schedule tab."
    embedding = generate_embedding(prompt)
    print(f"Generated embedding: {embedding}")