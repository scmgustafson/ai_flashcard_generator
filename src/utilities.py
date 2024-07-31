import csv
import json
import logging
import datetime

from openai import OpenAI

import config

class WatchfilesFilter(logging.Filter):
    def filter(self, record):
        return 'watchfiles' not in record.name

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

    for handler in logging.getLogger().handlers:
        handler.addFilter(WatchfilesFilter())

    return logging.getLogger(__name__)

logger = setup_logging()

openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

def query_openai(number: int, topic: str) -> dict:
    logger.info('Querying open AI for {n} key/values'.format(n=number))

    SYSTEM_ROLE = """You generate flashcards to be used as a learning aid.\
        The flashcards should follow the format of Side 1 equals the object/idea/word/topic\
        and side 2 is the explanation/translation/definition for side 1.\
        Please return the flashcards in a JSON format. I emphasize that the results must be returned in JSON format.
        """
    USER_ROLE = "Generate a deck of {n} number of flashcards \
        on the topic of {topic}.".format(n=number, topic=topic)

    try:
        completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_ROLE},
            {"role": "user", "content": USER_ROLE}
            ]
        )

        content = completion.choices[0].message.content
    except Exception as e:
        logger.exception("\n@@@@@@@@@@@@@ An exception occurred \
                         while querying OpenAI @@@@@@@@@@@@@")
        logger.exception(e)

    return parse_completion_into_list_of_dicts(content)

def parse_completion_into_list_of_dicts(completion_content: str) -> dict:
    """ Returns a dictionary of key/values parsed from the returned OpenAI completion
    """
    try:
        start_index = completion_content.find('[')
        end_index = completion_content.rfind(']') + 1

        # Extract and load into JSON
        json_str = completion_content[start_index:end_index]
        data = json.loads(json_str)

        return data
    except Exception as e:
        logger.exception("\n@@@@@@@@@@@@@ An exception occurred \
                         while querying OpenAI @@@@@@@@@@@@@")
        logger.exception(e)
        return None

def list_to_dict(list_string_list: list[list[str]]):
    """Take an awful list of lists of strings and parse into a dict
    """

    #list_string_list = [['une boîte,a box'], ['réussir,to succeed']]
    data = list_string_list
    if type(data) != type([]):
        raise TypeError('Input object not list. List expected.')

    dict = {}
    for key_value in data:
        split = key_value[0].split(',')
        key = split[0]
        value = split[1]
        dict[key] = value

    return dict

def dict_to_csv(dict: dict, output_csv_file: str) -> None:
    """ Takes in a dictionary and outputs as a CSV file with headers of 'word' and 'defition'
    """
    if type(dict) !=  type(dict()):
        raise TypeError('Input object not dictionary. Dictionary expected.')

    try:
        with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write the headers
            writer.writerow(['word', 'definition'])

            # Write the data
            for word, definition in dict.items():
                writer.writerow([word, definition])
    except Exception as e:
        logger.exception("\n@@@@@@@@@@@@@ An exception occurred \
                         while querying OpenAI @@@@@@@@@@@@@")
        logger.exception(e)

def query_and_get_dict(desired_count: int, batch_size: int,
                       query: str, output_to_file: bool) -> dict:
    """ Main logic of the program
    Queries OpenAI for completions N number of times for J batch sizes until a target count is met
    Set output_to_file to True to generate a csv file
    """
    logger.info('Starting process')
    logger.info(('Attempting to reach target count of '
                '{desired_count} with batch size of {batch_size}').format(desired_count=desired_count, 
                                                        batch_size=batch_size))

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
    logging.debug('Total items in output dict: {n}'.format(n=len(dict)))

    # Optional flag to export results to a .csv file
    if output_to_file:
        now = datetime.now()
        dict_to_csv(dict, 'output-{timestamp}.csv'.format(timestamp = now))

    return dict