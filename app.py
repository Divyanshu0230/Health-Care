from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the model once at startup
saved_model = joblib.load('model_cdss.pkl')

@app.route('/api', methods=['POST'])
def predict():
    data = request.get_json()
    print("Received data:", data)  # Debug print
    # Expecting: {"data": [[list of numbers as strings or ints]]}
    try:
        b = data['data'][0]
        a = list(range(2, 134))
        # Convert to float if value contains a dot, else int
        b = [float(x) if '.' in str(x) else int(x) for x in b]
        count = 0
        while count < len(b):
            item_to_replace = b[count]
            replacement_value = 1
            indices_to_replace = [i for i, x in enumerate(a) if x == item_to_replace]
            count += 1
            for i in indices_to_replace:
                a[i] = replacement_value
        a = [0 if x != 1 else x for x in a]
        y_diagnosis = saved_model.predict([a])
        print("Prediction:", y_diagnosis[0])  # Debug print
        return jsonify({'prediction': [str(y_diagnosis[0])]})
    except Exception as e:
        print("Error:", e)  # Debug print
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050) 