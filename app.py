from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import pandas as pd
import impedance
import base64
from io import BytesIO
from bode_plot import create_bode_plot

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['cellImage']
    cell_condition = request.form['cellCondition']

    nominal_voltage = request.form['nominalVoltage']
    nominal_energy = request.form['nominalEnergy']
    voltage_range = request.form['voltageRange']

    # Generate unique Cell ID
    cell_id = str(uuid.uuid4())[:10]

    # Generate barcode
    barcode_img = generate_barcode(cell_id)

    # Save file and data to MySQL database

    return jsonify({'cellId': cell_id, 'barcode': barcode_img})

@app.route('/csv', methods=['POST'])
def upload_csv():
    data_file = request.files['dataFile']
    if data_file:
        df = pd.read_csv(data_file)
        frequencies = df.iloc[:, 0].values
        Z_real = df.iloc[:, 1].values
        Z_imag = df.iloc[:, 2].values
        Z = Z_real + 1j * Z_imag

        graphJSON = create_bode_plot(frequencies, Z)

    # Return the JSON representation of the plot
    return jsonify(graphJSON=graphJSON)

def generate_barcode(cell_id):
    Code128 = barcode.get_barcode_class('code128')
    barcode_instance = Code128(cell_id, writer=ImageWriter())
    buffer = BytesIO()
    barcode_instance.write(buffer)
    return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
