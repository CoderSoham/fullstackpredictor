from flask import Flask, request, jsonify
from predictor import fetch_data_and_train_model, predict_and_plot_realtime_price
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Placeholder to store trained models
trained_models = {}

@app.route('/predict', methods=['POST'])
def predict():
    print(request.json)

    # Get the stock symbol from the request
    symbol = request.json.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Stock symbol is required'}), 400

    # Check if the model is already trained for the given symbol
    if symbol not in trained_models:
        # If the model is not trained, fetch data and train the model
        try:
            model = fetch_data_and_train_model(symbol)
            trained_models[symbol] = model
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Predict and plot real-time price using the trained model
    try:
        prediction_plot = predict_and_plot_realtime_price(trained_models[symbol], symbol)
        return jsonify({'prediction_plot': prediction_plot}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
