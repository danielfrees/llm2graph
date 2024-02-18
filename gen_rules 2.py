import json
import networkx as nx
import requests
import os
import predictionguard as pg
import re
from matplotlib import pyplot as plt
import textwrap
import random


#Refresh key into env
INTEL_KEY = os.getenv("PREDICTION_GUARD_API")
INTEL_KEY = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E'
os.environ["PREDICTIONGUARD_TOKEN"] = INTEL_KEY
random.seed(123)



def query_prediction_guard(query : str):
    """ 
    Wrapper for querying prediction guard
    """
    
    result = pg.Completion.create(
        model="Nous-Hermes-Llama2-13B",  #"Yi-34B-Chat", sqlcoder-34b-alpha, Nous-Hermes-Llama2-13B
        prompt=query,
        # max_tokens=500
    )
    return result


def main():
    """ 
    Run LLM knowledge graph extraction experiment.
    """

    print("=== Querying Intel Prediction Guard ===\n")
    input = "You can make an apple pie with apples and cinnamon."
    
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
                    "type": "fruit",
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
                    "type": "fruit",
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
                    "type": "spice",
                    "calories": "4", 
                    "protein": "0", 
                    "carbs": "1",
                    "fat": "0",
                    "extra": "Garlic has a strong odor and taste, and is excellent in sauces."
                }},
                "salmon" : {{
                    "serving": "100 grams",
                    "type": "protein",
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
                    "type": "spice",
                    "calories": "4", 
                    "protein": "0", 
                    "carbs": "1",
                    "fat": "0",
                    "extra": "Garlic has a strong odor and taste, and is excellent in sauces."
                }},
                "salmon" : {{
                    "serving": "100 grams",
                    "type": "protein",
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
    output = truncate(json_rules)
    print("\n=== Extracted Recipe Rule Information ===\n")
    print(output)

    # Load the existing JSON data from a file
    with open('output_initial.json', 'r') as file:
        base_graph = json.load(file)

    # Convert the output string to a JSON object (assuming the output is valid JSON)
    try:
        json_data = json.loads(output)
    except json.JSONDecodeError:
        print("The output is not valid JSON.")
        json_data = None

    # If json_data is valid, save it to a file
    if json_data is not None:
        with open('output.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        print("The JSON data has been saved to 'output.json'.")

    #print("\n=== TEST ===\n")
    #test = query_prediction_guard(query = "Write me a story about a dragon and a castle.")
    #print(test['choices'][0]['text'])

    output_json = json.loads(output)
    base_graph.update(output_json)

    create_graph(base_graph)

def truncate(s):
    open_brackets = 0
    close_brackets = 0

    for i in range(len(s)):
        if s[i] == "{":
            open_brackets += 1
        elif s[i] == "}":
            close_brackets += 1

        if open_brackets == close_brackets:
            return s[:i+1]
    return s


def create_graph(json_data):
    # If json_data is already a dictionary, no need to parse it
    if isinstance(json_data, dict):
        data = json_data
    else:
        # If json_data is a string, parse it
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            print("json_data is not valid JSON.")
            return
    # Load JSON data into a Python dictionary

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes to the graph with attributes
    for item, attributes in data['items'].items():
        G.add_node(item, **attributes)

    # Add edges to the graph
    edge_labels = {}
    for relation in data['relations'].values():
        G.add_edge(relation['from'], relation['to'])
        edge_labels[(relation['from'], relation['to'])] = relation['relation']

    # Create a larger figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500)

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Add node attributes as annotations under the nodes
    for node, attributes in G.nodes(data=True):
        # JSON format each attribute line without brackets
        text = "\n".join([f"{key}: {value}" for key, value in attributes.items()])
        lines = text.split("\n")
        wrapped_text = ""
        for line in lines:
            wrapped_line = '\n'.join(textwrap.wrap(line, width=40))  # Wrap line at 40 characters
            wrapped_text += wrapped_line + "\n"

        plt.annotate(wrapped_text, (pos[node][0], pos[node][1]-0.15), ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

    # Get current axes limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Add margins to the axes limits
    x_margin = (xlim[1] - xlim[0]) * 0.1  # 10% margin
    y_margin = (ylim[1] - ylim[0]) * 0.2  # 20% margin

    ax.set_xlim(xlim[0] - x_margin, xlim[1] + x_margin)
    ax.set_ylim(ylim[0] - y_margin, ylim[1] + y_margin)

    plt.show()

if __name__ == "__main__":
    main()