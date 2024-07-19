import config

from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# openai_client = OpenAI(
#     api_key=config.OPENAI_API_KEY
# )
# completion = openai_client.chat.completions.create(
#   model="gpt-4o-mini",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# focus on type hints for functions
@app.get("/")
async def root():
    return 'hello world'