import completion
from vector_searcher import search_similar

def truncate_context(chunks, max_chars: 1000):
    context = ""
    for chunk in chunks:
        chunk_text = chunk.get("content")
        if len(context) + len(chunk_text) > max_chars:
            # Truncate the chunk_text to fit within max_chars
            remaining_chars = max_chars - len(context)
            context += chunk_text[:remaining_chars] + "..."
            break
        context += chunk_text + "\n\n"

    return context.strip()

def build_prompt(question, retrieved_chunks):
    context = truncate_context(retrieved_chunks, max_chars=1000)
    prompt = f"""You are an AI assistant specialized in answering questions based on the provided context.
                    Context: {context}
                    Question: {question}
            Answer:"""
    return prompt

if __name__ == "__main__":
    question = "Tell me more about A438FT"
    retrieved_chunks = search_similar(question=question, index="document", top_k=3)

    prompt = build_prompt(question, retrieved_chunks)
    print(f"Generated Prompt: {prompt}")
    
    response = completion.call_llm(prompt)
    print("Question")
    print(question)
    print("LLM Response")
    print(response)