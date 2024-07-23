import config
import utilities

import csv
import json
import logging

from openai import OpenAI

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

openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

def query_openai(number: int, topic: str) -> dict:
    logger.info('Querying open AI for {n} key/values'.format(n=number))

    SYSTEM_ROLE = """You generate flashcards to be used as a learning aid. The flashcards should follow the format of Side 1 equals the object/idea/word/topic and side 2 is the explanation/translation/definition for side 1.\
    Please return the flashcards in a JSON format. I emphasize that the results must be returned in JSON format.
    """
    USER_ROLE = "Generate a deck of {n} number of flashcards on the topic of {topic}.".format(n=number, topic=topic)

    try:
        completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        # messages=[
        #     {"role": "system", "content": "You generate flashcards to be used as a learning aid. The flashcards should follow the format of Side 1 equals the object/idea/word/topic and side 2 is the explanation/translation/definition for side 1. Please return the flashcards in a json format."},
        #     {"role": "user", "content": "Generate a deck of {n} number of flashcards on the topic of {topic}.".format(n=number, topic=topic)}
        #     ]
        messages=[
            {"role": "system", "content": SYSTEM_ROLE},
            {"role": "user", "content": USER_ROLE}
            ]
        )

        content = completion.choices[0].message.content
    except Exception as e:
        logger.exception(e)
    
    return parse_completion_into_list_of_dicts(content)

def parse_completion_into_list_of_dicts(completion_content: str) -> dict:
    start_index = completion_content.find('[')
    end_index = completion_content.rfind(']') + 1
    
    # Extract the JSON string
    json_str = completion_content[start_index:end_index]

    # Parse the JSON string into a dictionary
    data = json.loads(json_str)
    return data

def list_to_dict(list_string_list: list[list[str]]):
    #input_list = [['une boîte,a box'], ['réussir,to succeed']]

    data = list_string_list
    dict = {}
    for key_value in data:
        split = key_value[0].split(',')
        key = split[0]
        value = split[1]
        dict[key] = value

    return dict

def dict_to_csv(dict: dict, output_csv_file) -> None:
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the headers
        writer.writerow(['word', 'definition'])

        # Write the data
        for word, definition in dict.items():
            writer.writerow([word, definition])

def query_and_get_csv(desired_count: int, batch_size: int, query: str):
    logger.info('Starting process')
    logging.info('Attempting to reach target count of {desired_count} with batch size of {batch_size}'.format(desired_count=desired_count, batch_size=batch_size))

    input_list = []
    while len(input_list) <= desired_count:
        response = query_openai(batch_size, query)

        #Response = [{'Side 1': 'abordable', 'Side 2': 'affordable'}]
        for item in response:
            input_string = ''
            try:
                input_string += str(item.get('Side 1')) + ',' + str(item.get('Side 2'))
                input_list.append(input_string.split('\n'))
            except Exception as e:
                print('Exception occured: {e}'.format(e=e))

        logger.info('Length of preprocessed list: {length}'.format(length=len(input_list)))

    #input_list = [['une boîte,a box'], ['réussir,to succeed']]
    dict = list_to_dict(input_list)
    logging.info('Total items in output dict: {n}'.format(n=len(dict)))

    dict_to_csv(dict, 'test.csv')