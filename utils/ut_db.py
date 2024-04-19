import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt
# client = openai.OpenAI() # not acceptable in streamlit

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



def get_mysql(text, model="text-embedding-3-small"):
    # Database connection parameters
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Your Password',
        'database': 'receipts'
    }
