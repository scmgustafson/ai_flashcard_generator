import config
import utilities

import csv
import json
import logging

from fastapi import FastAPI
from openai import OpenAI

#app = FastAPI()
openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

def setup_logging(
    log_file="app.log",
    log_level=logging.INFO,
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    date_format="%Y-%m-%d %H:%M:%S"
):
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )

    return logging.getLogger(__name__)

logger = setup_logging()

# @app.get("/")
# async def root():
#     return 'hello world'

# TODO
# Set up as api endpoint with query param
# need to add exception handling and retries for when openai doesnt return values
# better query changes
# find a way to filter out duplicates in the csv (add CSV file into query and say to generate new unique ones?)
# filter out None,None in the CSV

if __name__ == "__main__":
    target_count = 10
    batch_count = 10

    utilities.query_and_get_csv(target_count, batch_count, 'French vocabulary at CEFR level C1 where Side 2 is in English')


    