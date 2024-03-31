from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import requests

from failure_predictor import FailurePredictor


failrePredictor = FailurePredictor()


# class for getting the server resource usage
class get_resource_usage_metrics(Resource):
    def get(self):
        resource_data_api_url = "http://192.168.8.152:5000/get-resource-usage"  # URL of the API to get the resource usage metrics
        try:
            response = requests.get(resource_data_api_url)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to call data streamer"})

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Internal server error in data streamer"})


# class for getting the prediction results
class get_prediction_results(Resource):
    def get(self):
        prediction_data_api_url = "http://192.168.8.152:5000/get-prediction-data"  # URL of the API to get the failure prediction data
        try:
            response = requests.get(prediction_data_api_url)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to call data streamer"})

        if response.status_code == 200:
            data = response.json()
            prediction_data = data["prediction_data"]

            if len(prediction_data) == 0:
                return jsonify(
                    {
                        "contains_data": 1,
                        "time_stamps": [""],
                        "failure_probabilities": [0],
                        "log_predictions": [0],
                        "resource_predictions": [0],
                        "combined_predictions": [0],
                    }
                )

            if len(prediction_data) > 10:
                prediction_data = prediction_data[-20:]

            (
                log_predictions,
                resource_predictions,
                combined_predictions,
                time_stamps,
                failure_probabilities,
            ) = failrePredictor.get_predictions(prediction_data)

            return jsonify(
                {
                    "contains_data": 1,
                    "time_stamps": time_stamps,
                    "failure_probabilities": failure_probabilities,
                    "log_predictions": log_predictions,
                    "resource_predictions": resource_predictions,
                    "combined_predictions": combined_predictions,
                }
            )

        else:
            return jsonify({"error": "Internal server error in data streamer"})


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    # adding the routes
    api.add_resource(get_resource_usage_metrics, "/get-resource-usage-metrics")
    api.add_resource(get_prediction_results, "/get-prediction-results")

    app.run(debug=False, port=8080)
