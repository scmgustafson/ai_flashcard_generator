import config
import utilities

import csv
import json
import logging

from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY
)
logger = utilities.setup_logging()

@app.get("/")
async def output_dict():
    target_count = 10
    batch_count = 10

    output_dict = utilities.query_and_get_csv(target_count, batch_count, 'French vocabulary at CEFR level C1 where Side 2 is in English', False)
    return output_dict

# TODO
# need to add exception handling and retries for when openai doesnt return values
# better query changes
# find a way to filter out duplicates in the csv (add CSV file into query and say to generate new unique ones?)
# filter out None,None in the CSV

# if __name__ == "__main__":
#     return True 