import numpy as np
import tensorflow as tf
import joblib
from os.path import dirname

# data persistence
RESOURCE_DATA_ARR = []
LOG_DATA_ARR = []
FAILURE_PROBABILITY_ARR = []

NUMBER_OF_CONTENDERS = 20
MSE_THRESHOLD = 0.0262
NO_OF_STEPS = 20
SCALER = joblib.load(f"{dirname(__file__)}/models/scaler.gz")
SCALER.feature_names_in_ = None  # This is to avoid the redundant warning message

# Loading the saved models
log_model = tf.keras.models.load_model(f"{dirname(__file__)}/models/LSTM_log_model.keras")
resource_model = tf.keras.models.load_model(f"{dirname(__file__)}/models/autoencoder_resource_model.keras")

class FailurePredictor:

    # function to predict the anomaly of log data
    def get_log_data_prediction(self, sample, number_of_contenders):
        predicted_label = 0

        if sample == 0:
            return predicted_label

        if len(LOG_DATA_ARR) < 10:
            LOG_DATA_ARR.append(sample)
            return predicted_label
        else:
            np_log_data_arr = np.array(LOG_DATA_ARR)
            log_data_reshaped = np_log_data_arr.reshape(1, 10, 1)
            predicted_log_values = log_model.predict(log_data_reshaped)

            # log data prediction related calculation
            top_contenders = np.argsort(predicted_log_values)[0][-number_of_contenders:]
            if sample in top_contenders:
                predicted_label = 0
            else:
                predicted_label = 1
            LOG_DATA_ARR.append(sample)
            LOG_DATA_ARR.pop(0)
            return predicted_label

    # function to predict the anomaly of resource data
    def get_resource_data_prediction_form_nn(self, sample, mse_threshold):
        predicted_label = 0

        if len(RESOURCE_DATA_ARR) < 9:
            RESOURCE_DATA_ARR.append(sample)
            return predicted_label
        else:
            RESOURCE_DATA_ARR.append(sample)

            np_resource_data_arr = np.array(RESOURCE_DATA_ARR)
            resource_data_reshaped = np_resource_data_arr.reshape(1, 10 * 17)
            prediction_data_tf = tf.convert_to_tensor(
                resource_data_reshaped, dtype=tf.float32
            )
            predicted_values = resource_model.predict(prediction_data_tf)

            # resource data prediction related calculation
            mse = np.mean(np.power(prediction_data_tf - predicted_values, 2))
            if mse > mse_threshold:
                predicted_label = 1
            else:
                predicted_label = 0
            RESOURCE_DATA_ARR.pop(0)

            return predicted_label

    # function to predict the failure probability
    def get_failure_probability_prediction(self, combined_prediction, no_of_steps):
        failure_probability = 0

        if len(FAILURE_PROBABILITY_ARR) < (no_of_steps - 1):
            FAILURE_PROBABILITY_ARR.append(combined_prediction)
            no_of_positive_values = FAILURE_PROBABILITY_ARR.count(1)

            if no_of_positive_values > 0:
                failure_probability = (
                    no_of_positive_values / len(FAILURE_PROBABILITY_ARR)
                ) * 100
            else:
                failure_probability = 0

            return failure_probability

        else:
            FAILURE_PROBABILITY_ARR.append(combined_prediction)
            no_of_positive_values = FAILURE_PROBABILITY_ARR.count(1)

            if no_of_positive_values > 0:
                failure_probability = (
                    no_of_positive_values / len(FAILURE_PROBABILITY_ARR)
                ) * 100
            else:
                failure_probability = 0
            FAILURE_PROBABILITY_ARR.pop(0)

            return failure_probability

    # function to get the failure predictions
    def get_predictions(self, data):
        log_predictions = []
        resource_predictions = []
        combined_predictions = []
        time_stamps = []
        failure_probabilities = []

        for row in data:
            combined_prediction = 0

            resource_data = row[2:]
            resource_data = [int(x) for x in resource_data]
            scaled_resource_data = SCALER.transform([resource_data])

            log_data = row[1]
            timestamp = row[0]

            log_data_prediction = self.get_log_data_prediction(
                log_data, NUMBER_OF_CONTENDERS
            )
            resource_data_prediction = self.get_resource_data_prediction_form_nn(
                scaled_resource_data, MSE_THRESHOLD
            )

            if log_data_prediction == 1 or resource_data_prediction == 1:
                combined_prediction = 1

            failure_probability = self.get_failure_probability_prediction(
                combined_prediction, NO_OF_STEPS
            )
            failure_probability = failure_probability / 100
            failure_probability = round(failure_probability, 1)

            failure_probabilities.append(failure_probability)
            log_predictions.append(log_data_prediction)
            resource_predictions.append(resource_data_prediction)
            combined_predictions.append(combined_prediction)
            time_stamps.append(timestamp)

        return (
            log_predictions,
            resource_predictions,
            combined_predictions,
            time_stamps,
            failure_probabilities,
        )

