import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
# client = openai.OpenAI() # not acceptable in streamlit
# curl https://api.openai.com/v1/models -H "Authorization: Bearer sk-proj-FcKBzwDnp"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def aichat(messages, openai_api_key):
    try:
        client = openai.OpenAI(api_key = openai_api_key)
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0125",
            # stream=True,
            # max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def ai_vision(var_for, openai_api_key, model_v, base64_image):
    try:
        client = openai.OpenAI(api_key = openai_api_key)
        response = client.chat.completions.create(
            model=model_v,
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": var_for},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                    },
                ],
                }
            ],
            max_tokens=1024,
        )

        return response.choices[0].message.content
        # return response.choices[0]
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def get_embedding(text, model="text-embedding-3-small"):
    # client = openai.OpenAI(api_key = openai_api_key)
    text = text.replace("\n", " ")
    # return client.embeddings.create(input = [text], model=model).data[0].embedding

# text = "test embedding"
# embeddings = get_embedding(text)