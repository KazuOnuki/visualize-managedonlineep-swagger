### Check whether ServiceInputs/example exists
import json
import pandas as pd
import argparse


def download_swagger_json(testdata):
  SWAGGER_DIR_PATH = './swagger'
  SWAGGER_JSON_PATH = f'{SWAGGER_DIR_PATH}/swagger_spec.json'

  # JSONファイルを読み込む
  with open(SWAGGER_JSON_PATH, 'r') as file:
      swagger_data = json.load(file)

      # ServiceInputの例データが空なら
      if not swagger_data['definitions']['ServiceInput']['example']:
        df = pd.read_csv(testdata, index_col=None)
        example = json.loads(df[df.index==0].to_json(orient='split'))
        # 最終的なデータ形式
        final_data = {"input_data": example}
        swagger_data['definitions']['ServiceInput']['example'] = final_data

        # 更新したSwagger JSONを保存
        with open(SWAGGER_JSON_PATH, 'w') as json_file:
            json.dump(swagger_data, json_file, indent=2)

        print("added ServiceInput example")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Example Json from testdata csv')
    parser.add_argument('--testdata', required=True, help='ACTUAL TestData CSV Path')
    args = parser.parse_args()

    # 使用例
    download_swagger_json(args.testdata)