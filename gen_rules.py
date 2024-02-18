import json
import networkx as nx
import requests
from dotenv import load_dotenv
import os
import predictionguard as pg

load_dotenv()

#Refresh key into env
INTEL_KEY = os.getenv("PREDICTION_GUARD_API")
os.environ["PREDICTIONGUARD_TOKEN"] = INTEL_KEY




def query_prediction_guard(query : str):
    """ 
    Wrapper for querying prediction guard
    """
    
    result = pg.Completion.create(
        model="Nous-Hermes-Llama2-13B",  #"Yi-34B-Chat", sqlcoder-34b-alpha, Nous-Hermes-Llama2-13B
        prompt=query
    )
    return result


def main():
    """ 
    Run LLM knowledge graph extraction experiment.
    """

    print("=== Querying Intel Prediction Guard ===\n")
    input = "Apples pair well with cinnamon."
    
    JSON_PROMPT = f"""
        ### Instruction
        You are an expert in designing nutritious, affordable meals. 
        Users will input rules, such as 'I don't like bananas', and you 
        will extract a json of graph information based on this rule, or 
        rules. 

        `ALLOWED ENTITY TYPES`: Fruit, Vegetable, Carbohydrate, Protein, Fat, Spice 

        `ALLOWED ENTITY FEATURES:` Calories (integer), Protein (integer, unit: grams), Carbs (integer, unit: grams), Fat (integer, unit: grams), Cost (float, unit: US Dollars), Extra (string, brief extra information)

        `ALLOWED RELATION TYPES`: pairsWith (ie. A pairs well with B), badWith (ie. A does not taste good with B), isFavorite (ie. A is always preferred if possible), leastFavorite (ie. A is never desired)

        ie. 

        Input: I don't like bananas.

        Rules: 
        {{
            "items": {{
                "banana" : {{
                    "serving": "1 banana",
                    "type": "fruit"
                    "calories": "110",
                    "protein": "1",
                    "carbs": "28",
                    "fat": "0",
                    "extra": "Bananas are rich in potassium and high in sugar."
                }}
            }},
            "relations": {{
                "from": "banana",
                "to": null,
                "relation": "leastFavorite"
            }}
        }}

        Input: I like bananas.

        Rules: 
        {{
            "items": {{
                "banana" : {{
                    "serving": "1 banana",
                    "type": "fruit"
                    "calories": "110",
                    "protein": "1",
                    "carbs": "28",
                    "fat": "0",
                    "extra": "Bananas are rich in potassium and high in sugar."
                }}
            }},
            "relations": {{
                "from": "banana",
                "to": null,
                "relation": "isFavorite"
            }}
        }}


        Input: Garlic pairs really well with salmon. 

        Rules: 
        {{
            "items": {{
                "garlic" : {{
                    "serving": "1 clove",
                    "type": "spice"
                    "calories": "4", 
                    "protein": "0", 
                    "carbs": "1",
                    "fat": "0",
                    "extra": "Garlic has a strong odor and taste, and is excellent in sauces."
                }},
                "salmon" : {{
                    "serving": "100 grams",
                    "type": "protein"
                    "calories": "136", 
                    "protein": "19", 
                    "carbs": "0",
                    "fat": "7",
                    "extra": "Salmon is an excellent source of Omega 3s."
                }}
            }},
            "relations": {{
                "1": {{
                    "from": "garlic",
                    "to": "salmon",
                    "relation": "pairsWith"
                }},
                "2": {{
                    "from": "salmon",
                    "to": "garlic",
                    "relation": "pairsWith"
                }}
            }}
        }}

        Input: Garlic pairs really poorly with salmon. 

        Rules: 
        {{
            "items": {{
                "garlic" : {{
                    "serving": "1 clove",
                    "type": "spice"
                    "calories": "4", 
                    "protein": "0", 
                    "carbs": "1",
                    "fat": "0",
                    "extra": "Garlic has a strong odor and taste, and is excellent in sauces."
                }},
                "salmon" : {{
                    "serving": "100 grams",
                    "type": "protein"
                    "calories": "136", 
                    "protein": "19", 
                    "carbs": "0",
                    "fat": "7",
                    "extra": "Salmon is an excellent source of Omega 3s."
                }}
            }},
            "relations": {{
                "1": {{
                    "from": "garlic",
                    "to": "salmon",
                    "relation": "badWith"
                }},
                "2": {{
                    "from": "salmon",
                    "to": "garlic",
                    "relation": "badWith"
                }}
            }}
        }}
        
    ### INPUT:
    {input}

    ### RULES:
    """

    result = query_prediction_guard(query = JSON_PROMPT)
    json_rules = result['choices'][0]['text']
    print("\n=== Extracted Recipe Rule Information ===\n")
    print(json_rules)

    print("\n=== TEST ===\n")
    test = query_prediction_guard(query = "Write me a story about a dragon and a castle.")
    print(test['choices'][0]['text'])
    #game_graph = create_graph_from_json(rules)

if __name__ == "__main__":
    main()