import sys
import csv
from flask import Flask, render_template

app = Flask(__name__)

DATA_DIR = '.'
CSV_FILENAME = 'data.csv'
default_filename = DATA_DIR + '/' + CSV_FILENAME

@app.route("/", methods=["GET"])
def index1():
    print("Hello! (to Terminal)")

    data_list = []

    # CSVファイルを読み込み
    with open(default_filename, mode='r') as f:
        all_data_iter = csv.reader(f)
        for row in all_data_iter:
            data_list.append([float(row[0]), float(row[1])])  # 気温と湿度をdata_listに追加

    return render_template("ワーク05_html.html", input_from_python=data_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
