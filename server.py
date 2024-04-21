from flask import Flask, jsonify, make_response
import socket
from flask import request
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Function to get the computer IP automatically
def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server (doesn't actually send data)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address
        local_ip = s.getsockname()[0]
        print('Here is my IP', local_ip)
        return local_ip
    except Exception as e:
        return str(e)

# Load the saved model
model = joblib.load('course_rating_model.h5')

# Define mappings
satisfaction_mapping = {0: 'Neutral', 1: 'Satisfied', 2: 'Un-Satisfied'}

# Function to map numeric predictions to categorical satisfaction levels
def map_output(prediction):
    # Convert prediction to integer
    prediction_int = int(prediction)
    
    # Return the satisfaction level corresponding to the prediction
    return satisfaction_mapping.get(prediction_int)

@app.route('/predict_satisfaction', methods=['POST'])
def predict_satisfaction():
    try:
        data = request.json  # Assuming JSON data is sent by the client
        if not data:
            # If no data is provided in the request body, return a 400 Bad Request response
            return make_response(jsonify({'error': 'No data provided in the request'}), 400)

        result = []
        for course_info in data:
            # Extract rating from course info
            rating = course_info.get('rating')
            if rating is None:
                # If rating is not provided for a course, return a 400 Bad Request response
                return make_response(jsonify({'error': 'Rating not provided for course {}'.format(course_info.get('course_name'))}), 400)

            # Make prediction
            prediction = model.predict([[rating]])
            
            # Map prediction to satisfaction level
            satisfaction_level = map_output(prediction[0])
            
            # Add course name, rating, and satisfaction level to result
            result.append({'course_name': course_info.get('course_name'), 'rating': rating, 'satisfaction_level': satisfaction_level, 'review_count': course_info.get('review_count')})
        
        return jsonify(result)
    except Exception as e:
        # If an unexpected error occurs, return a 500 Internal Server Error response
        return make_response(jsonify({'error': 'An unexpected error occurred: {}'.format(str(e))}), 500)


# Error handler for 404 Not Found error
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

if __name__ == '__main__':
    ip_address = get_local_ip()
    app.run(host=ip_address, port=5000)






# from flask import Flask, jsonify
# import socket
# from flask import Flask, request, jsonify
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from flask_cors import CORS

# import joblib

# app = Flask(_name_)
# CORS(app)

# def get_local_ip():
#     try:
#         # Create a socket object
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#         # Connect to an external server (doesn't actually send data)
#         s.connect(("8.8.8.8", 80))

#         # Get the local IP address
#         local_ip = s.getsockname()[0]
#         print('Here is my IP', local_ip)
#         return local_ip
#     except Exception as e:
#         return str(e)

# # Load the saved model
# model = joblib.load('course_rating_model.h5')

# # Define mappings
# satisfaction_mapping = {0: 'Neutral', 1: 'Satisfied', 2: 'Un-Satisfied'}

# # Function to map numeric predictions to categorical satisfaction levels
# def map_output(prediction):
#     # Convert prediction to integer
#     prediction_int = int(prediction)
    
#     # Return the satisfaction level corresponding to the prediction
#     return satisfaction_mapping.get(prediction_int)

# @app.route('/predict_satisfaction', methods=['POST'])
# def predict_satisfaction():
#     data = request.json  # Assuming JSON data is sent by the client
#     result = []
    
#     for course_info in data:
#         # Extract rating from course info
#         rating = course_info['rating']
        
#         # Make prediction
#         prediction = model.predict([[rating]])
        
#         # Map prediction to satisfaction level
#         satisfaction_level = map_output(prediction[0])
        
#         # Add course name and satisfaction level to result
#         result.append({'course_name': course_info['course_name'], 'satisfaction_level': satisfaction_level})
#         print(result)
#     return jsonify(result)

# if _name_ == '_main_':
#     ip_address = get_local_ip()
#     app.run(host=ip_address, port=5000)