import argparse
import urllib.request
import json
import re
import os
import pandas as pd

def download_swagger_json(rest_endpoint, deployment, api_key):
    SWAGGER_DIR_PATH = './swagger'
    TEST_DIR_PATH = './testdata'
    SWAGGER_JSON_PATH = f'{SWAGGER_DIR_PATH}/swagger_spec.json'
    EXAMPLE_JSON_PATH = f'{TEST_DIR_PATH}/example.json'
    EXAMPLE_JSON_EXIST = True
    # Set headers with Authorization token
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key, 'azureml-model-deployment': deployment}
    # replace "/score" part with "/swagger.json" by regex expression.
    url = re.sub(r'/score', '/swagger.json', rest_endpoint)
    # Create a request object
    req = urllib.request.Request(url, headers=headers)

    try:
        if os.path.exists(SWAGGER_JSON_PATH):
          os.remove(SWAGGER_JSON_PATH)
          print(f"DELETED swagger json path ({SWAGGER_JSON_PATH})")
        if os.path.exists(EXAMPLE_JSON_PATH):
          os.remove(EXAMPLE_JSON_PATH)
          print(f"DELETED example json path ({EXAMPLE_JSON_PATH})")
        
        # Make the request and read the response
        result = urllib.request.urlopen(req).read()
        json_string = result.decode('utf-8')
        # Parse JSON string to Python dictionary
        data = json.loads(json_string)
        os.makedirs(SWAGGER_DIR_PATH, exist_ok=True)
        # Save the JSON data to a file
        with open(SWAGGER_JSON_PATH, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        
        with open(SWAGGER_JSON_PATH, 'r') as file:
              swagger_data = json.load(file)
              if example:=swagger_data['definitions']['ServiceInput']['example']:
                first_key = list(example.keys())[0]
                # NOTE: if example json exists..
                if data:=example[first_key]:
                    # whether each key/value is empty.
                    for key, value in data.items():
                        if not value:
                            # if value is empty, break out block.
                            EXAMPLE_JSON_EXIST = False
                            break
                    if EXAMPLE_JSON_EXIST:
                        with open(EXAMPLE_JSON_PATH, 'w') as json_file:
                            json.dump(example, json_file, indent=2)
                else:
                    pass

        print(f'The JSON data has been saved to {SWAGGER_JSON_PATH}')

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Swagger JSON from a REST endpoint.')
    parser.add_argument('--rest_endpoint', required=True, help='REST endpoint URL')
    parser.add_argument('--deployment', required=True, help='Deployment Name')
    parser.add_argument('--api_key', required=True, help='API key for authorization')
    args = parser.parse_args()
    download_swagger_json(args.rest_endpoint, args.deployment, args.api_key)
