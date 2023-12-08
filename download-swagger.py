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
    # Set headers with Authorization token
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key, 'azureml-model-deployment': deployment}
    # /score の部分を正規表現を使用してすべて削除
    url = re.sub(r'/score', '/swagger.json', rest_endpoint)
    # Create a request object
    req = urllib.request.Request(url, headers=headers)

    try:
        # ファイルが存在するか確認してから削除
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
                    print(example)
                    # 各キーおよび値が空であるかどうかを確認
                    for key, value in data.items():
                        if not value:
                            # if value is empty, break out block.
                            break
                    with open(EXAMPLE_JSON_PATH, 'w') as json_file:
                        json.dump(example, json_file, indent=2)
                else:
                    pass

        print(f'The JSON data has been saved to {SWAGGER_JSON_PATH}')

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Swagger JSON from a REST endpoint.')
    parser.add_argument('--rest_endpoint', required=True, help='REST endpoint URL')
    parser.add_argument('--deployment', required=True, help='Deployment Name')
    parser.add_argument('--api_key', required=True, help='API key for authorization')
    args = parser.parse_args()

    # 使用例
    download_swagger_json(args.rest_endpoint, args.deployment, args.api_key)