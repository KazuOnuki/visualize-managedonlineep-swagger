﻿### Check whether ServiceInputs/example exists
import json
import pandas as pd
import argparse


def download_swagger_json(testdata):
  SWAGGER_DIR_PATH = './swagger'
  SWAGGER_JSON_PATH = f'{SWAGGER_DIR_PATH}/swagger_spec.json'

  # read ./swagger/swagger_spec.json
  with open(SWAGGER_JSON_PATH, 'r') as file:
      swagger_data = json.load(file)
      example = swagger_data['definitions']['ServiceInput']['example']
      first_key = list(example.keys())[0]
      df = pd.read_csv(testdata, index_col=None)
      example_data = json.loads(df[df.index==0].to_json(orient='split'))
      # final json scheme
      final_data = {f"{first_key}": example_data}
      swagger_data['definitions']['ServiceInput']['example'] = final_data

      # update ./swagger/swagger_spec.json
      with open(SWAGGER_JSON_PATH, 'w') as json_file:
          json.dump(swagger_data, json_file, indent=2)
        
      print("added ServiceInput example")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Example Json from testdata csv')
    parser.add_argument('--testdata', required=True, help='ACTUAL TestData CSV Path')
    args = parser.parse_args()
    download_swagger_json(args.testdata)
