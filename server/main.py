from flask import Flask, json, request
import os
import json
import predictionguard as pg

# Set your Prediction Guard token as an environmental variable.
os.environ["PREDICTIONGUARD_TOKEN"] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"

messages = [
    {
        "role": "user",
        "content": "Hello!"
    },
    {
        "role": "assistant",
        "content": "What can I help you with today?"
    },
    {
        "role": "user",
        "content": "Give me the attributes and actions that one can do with banana in a list format. Do not give me any other output or explanations. Example for you to learn: A banana has attributes such as color, weight, nutritional value, and require skills such as peeling."
    }
]

result = pg.Chat.create(
    model="Neural-Chat-7B",
    messages=messages
)

print(json.dumps(
    result,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
))

api = Flask(__name__)
messages = []
@api.route('/', methods=['GET'])
def get_response():
  return json.dumps(messages)

# Endpoint to create a new guide
@api.route('/', methods=["POST"])
def post_response():
    role = request.json['role']
    content = request.json['content']
    messages.append({
        "role": role,
        "content": content
    })

    return 

@api.route('/', methods=["DELETE"])
def delete_response():
    messages.clear()
    return

if __name__ == '__main__':
    api.run()