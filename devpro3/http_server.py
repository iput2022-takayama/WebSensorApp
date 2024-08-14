import csv
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

CSV_FILE = 'sensor_data.csv'

def read_sensor_data(filename):
    data_list = []
    try:
        with open(filename, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader, None)  # ヘッダーをスキップ
            for row in csv_reader:
                if len(row) == 5:
                    data_list.append({
                        'Name': row[0],
                        'Temperature': float(row[1]),
                        'Humidity': float(row[2]),
                        'Pressure': float(row[3]),
                        'CO2': float(row[4])
                    })
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
    return data_list

def calculate_averages(data_list):
    if not data_list:
        return {'Humidity': 0.0, 'Pressure': 0.0, 'CO2': 0.0}

    humidity_list = [item['Humidity'] for item in data_list]
    pressure_list = [item['Pressure'] for item in data_list]
    co2_list = [item['CO2'] for item in data_list]

    return {
        'Humidity': sum(humidity_list) / len(humidity_list),
        'Pressure': sum(pressure_list) / len(pressure_list),
        'CO2': sum(co2_list) / len(co2_list)
    }

@app.route("/", methods=["GET"])
def index():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_filename = os.path.join(current_dir, CSV_FILE)

    try:
        sensor_data = read_sensor_data(default_filename)
        averages = calculate_averages(sensor_data)
    except FileNotFoundError:
        return "CSV file not found", 404

    return render_template('index.html', sensor_data=sensor_data, averages=averages)

@app.route("/data", methods=["GET"])
def data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_filename = os.path.join(current_dir, CSV_FILE)

    try:
        sensor_data = read_sensor_data(default_filename)
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    return jsonify(sensor_data)

@app.route("/add_data", methods=["POST"])
def add_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_filename = os.path.join(current_dir, CSV_FILE)

    try:
        new_name = request.form.get('new_name')
        new_temperature = float(request.form.get('new_temperature'))

        sensor_data = read_sensor_data(default_filename)
        averages = calculate_averages(sensor_data)

        with open(default_filename, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            new_row = [new_name, new_temperature, averages['Humidity'], averages['Pressure'], averages['CO2']]
            csv_writer.writerow(new_row)
        return jsonify({"status": "success"})
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
