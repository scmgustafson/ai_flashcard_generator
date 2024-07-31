from fastapi import FastAPI

import config
import utilities

app = FastAPI()
logger = utilities.setup_logging()


# @app.get("/")
# async def output_dict():
#     target_count = 50
#     batch_count = 10

#     output_dict = utilities.query_and_get_dict(target_count, batch_count,\
#                                                'French vocabulary at CEFR level C1 where Side 2 is in English',\
#                                                 output_to_file=False)
#     return output_dict  
def main():
    """ Used instead of @app.get("/") route when doing testing
    """
    target_count = 50
    batch_count = 10

    output = utilities.query_and_get_dict(target_count, batch_count,\
                                               'French vocabulary at CEFR level C1 where Side 2 is in English',\
                                                output_to_file=False)
    return output

if __name__ == "__main__":
    main()
# TODO
# need to add exception handling
# retries for when openai doesnt return values
# better query changes
# find a way to filter out duplicates in the csv 
# (add CSV file into query and say to generate new unique ones?)
# filter out None,None in the CSV
