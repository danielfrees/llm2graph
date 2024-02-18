from flask import Flask, json, request, jsonify
import os
import json
import predictionguard as pg
from flask_cors import CORS

# Set your Prediction Guard token as an environmental variable.
os.environ["PREDICTIONGUARD_TOKEN"] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"

messages = [
    {
        "role": "user",
        "content": "What's up!"
    },
    {
        "role": "assistant",
        "content": "Well, technically vertically out from the center of the earth."
    },
]


api = Flask(__name__)
CORS(api)
@api.route('/', methods=['GET'])
def get_response():
  return json.dumps(messages[-1])

# Endpoint to create a new guide
@api.route('/', methods=["POST"])
def post_response():
    role = request.json['role']
    content = request.json['content']
    messages.append({
        "role": role,
        "content": content
    })

    result = pg.Chat.create(
        model="Neural-Chat-7B",
        messages=messages
    )
    messages.append({"role": "assistant", "content": result['choices'][-1]['message']['content']})
    
    return json.dumps(messages[-1])

@api.route('/', methods=["DELETE"])
def delete_response():
    messages.clear()
    return

if __name__ == '__main__':
    api.run()