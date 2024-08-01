import utilities

def test_parse_completion_into_list_of_dicts():
    test_input = '''```json
                [
                    {
                        "Side 1": "concomitant",
                        "Side 2": "occurring or existing at the same time; accompanying."
                    },
                    {
                        "Side 1": "abstrait",
                        "Side 2": "abstract; existing in thought or as an idea but not having a physical or concrete existence."
                    },
                    {
                        "Side 1": "l'ergonomie",
                        "Side 2": "ergonomics; the study of people's efficiency in their working environment."
                    },
                    {
                        "Side 1": "la corrélation",
                        "Side 2": "correlation; a mutual relationship or connection between two or more things."
                    },
                    {
                        "Side 1": "l'innovation",
                        "Side 2": "innovation; the process of making an idea or invention popular or widespread."
                    },
                    {
                        "Side 1": "la proposition",
                        "Side 2": "proposal; a plan or suggestion put forward for consideration or discussion."
                    },
                    {
                        "Side 1": "l'évolution",
                        "Side 2": "evolution; the gradual development of something, especially from a simple to a more complex form."
                    },
                    {
                        "Side 1": "la divergence",
                        "Side 2": "divergence; the process or state of diverging or moving apart."
                    },
                    {
                        "Side 1": "l'ambiguïté",
                        "Side 2": "ambiguity; the quality of being open to more than one interpretation; inexactness."
                    },
                    {
                        "Side 1": "la durabilité",
                        "Side 2": "sustainability; the ability to be maintained at a certain rate or level; avoiding the depletion of natural resources."
                    }
                ]
                ```'''
    output = utilities.parse_completion_into_list_of_dicts(test_input)
    assert isinstance(output, list)

def test_list_to_dict():
    # def list_to_dict(list_string_list: list[list[str]]):
    test_input = [['une boîte,a box'], ['réussir,to succeed']]
    output = utilities.list_to_dict(test_input)
    assert isinstance(output, dict)
