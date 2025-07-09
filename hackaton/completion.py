import requests

def call_llm(prompt: str) -> str:
    print(f"Prompt sent to LLM: {prompt}")
    response = requests.post(
        "https://trussedaisb1.geico.net/provider/generic/chat/completions",
        json={
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 0.9,
        },
        headers={"Authorization": "Bearer gS8QX3YfEdPoFnJT7eIM2RLXmXDpiGfxbDodqLuTwiyZ82gU",
                 "Content-Type": "application/json",
                 "User-Agent": "insomnia/10.3.0"}
    )
    print(f"Response status code: {response.status_code}")
    #print(f"Response content: {response.text}")
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from LLM")

if __name__ == "__main__":
    prompt = "Say hi"
    response = call_llm(prompt)
    print(f"Response from LLM: {response}")