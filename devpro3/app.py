
from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

# CSVファイルからセンサーデータを読み込む関数
def read_sensor_data(filename):
    data_list = []
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 4:  # CSVファイルの各行は4つの要素を持つことを確認
                data_list.append({
                    'Temperature': float(row[0]),
                    'Humidity': float(row[1]),
                    'Pressure': float(row[2]),
                    'CO2': float(row[3])
                })
            else:
                print(f"Ignoring invalid row: {row}")
    return data_list

# ホームページのルート
@app.route("/", methods=["GET"])
def index():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_filename = os.path.join(current_dir, 'data.csv')

    try:
        sensor_data = read_sensor_data(default_filename)
    except FileNotFoundError:
        return "data.csv file not found", 404

    return render_template("index1.html", sensor_data=sensor_data)

# データを取得するAPIエンドポイント
@app.route("/data", methods=["GET"])
def data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_filename = os.path.join(current_dir, 'data.csv')

    try:
        sensor_data = read_sensor_data(default_filename)
    except FileNotFoundError:
        return jsonify({"error": "data.csv file not found"}), 404

    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
