import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

import json

def get_completion_from_messages(system_message, user_message, model="gpt-3.5-turbo-0613", temperature=0, max_tokens=50) -> str:  
    # Ensure that max_tokens does not exceed the token limit per minute
    token_limit_per_minute = 60000  # Token limit per minute for the chosen model
    max_tokens = min(max_tokens, token_limit_per_minute)  

    prompt = f"You: {user_message}\nAI: {system_message}\nYou:"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message}, {"role": "user", "content": user_message}],
        temperature=temperature,
        max_tokens=max_tokens,
        stop=["\nYou:"]
    )

    generated_text = response.choices[0].message.get("content", "").strip()
    print("Generated text:", generated_text)  

    if generated_text:
        try:
            json_response = json.loads(generated_text)
            print("JSON response:", json_response)  
            query = json_response.get("query", "")
            return json.dumps({"query": query})
        except json.JSONDecodeError as e:
            print("JSON decoding error:", e)  
            return generated_text
    else:
        return ""



if __name__ == "__main__":
    system_message = "You are a helpful assistant"
    user_message = "Hello, how are you?"
    print(get_completion_from_messages(system_message, user_message))
