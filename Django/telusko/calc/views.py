#Foe Comments see veiws1.py file there are comments for explanation

import base64
import cv2
import dlib
import face_recognition
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
import os
import numpy as np
import json
import csv
import time


user_data_path = r"C:\cpp\coding\face\faces.csv"
user_data = {}

# Paths to data and models
shape_predictor_path = r"C:\cpp\coding\Django\Tools\shape_predictor_68_face_landmarks.dat"
face_recognizer_path = r"C:\cpp\coding\Django\Tools\dlib_face_recognition_resnet_model_v1.dat"
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(shape_predictor_path)
face_recognizer = dlib.face_recognition_model_v1(face_recognizer_path)
known_face_encodings = [np.array(user_info["encoding"]) for user_info in user_data.values()]
known_face_names = list(user_data.keys())

if not os.path.exists(user_data_path):
    with open(user_data_path, "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Name", "Contact Number", "Face Encodings"])




def load_user_data_csv():
    user_data = {}
    with open(user_data_path, "r", newline="") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            name, contact, encoding_json = row
            encoding = json.loads(encoding_json)
            user_data[name] = {
                "contact": contact,
                "encoding": encoding
            }
    return user_data



# Function to save user data to a new CSV file, overwriting the old one
def save_user_data_csv(name, user_data):
    with open(user_data_path, "a", newline="") as file:
        csv_writer = csv.writer(file)
        contact = user_data.get(name)["contact"]
        face_encoding = json.dumps(user_data.get(name)["encoding"])
        csv_writer.writerow([name, contact, face_encoding])




def save_user_data_csv1(user_data):
    with open(user_data_path, "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Name", "Contact Number", "Face Encodings"])
        for name, user_info in user_data.items():
            contact = user_info.get("contact")
            face_encoding = json.dumps(user_info.get("encoding"))
            csv_writer.writerow([name, contact, face_encoding])



# Django view functions
# Render the home page
def home(request):
    return render(request, 'calc/home.html')

# Render the sign-in page
def signin(request):
    return render(request, 'calc/signin.html')

# Render the delete page
def delete(request):
    return render(request, 'calc/delete.html')

# Render the signup page
def signup(request):
    return render(request, 'calc/signup.html')




def save_user_data(name, user_data):
    with open(user_data_path, "w") as file:
        json.dump(user_data, file, indent=4)
    data = user_data.get(name)
    if not data:
        return HttpResponseBadRequest(f"User {name} not found in user data.")




def recognize_user(request):
    if request.method == 'POST':
        time.sleep(3)
        captured_frame_path = r"C:\Users\saite\Downloads\captured_frame.jpg"
        captured_frame = cv2.imread(captured_frame_path)

        if captured_frame is None:
            response_data = {
                'success': False,
                'error': 'Failed to load the captured frame.'
            }
            os.remove(captured_frame_path)
            return JsonResponse(response_data)

        face_locations = face_recognition.face_locations(captured_frame)
        if not face_locations:
            response_data = {
                'success': False,
                'error': 'No face detected in the captured frame.'
            }
            os.remove(captured_frame_path)
            return JsonResponse(response_data)

        face_encoding = face_recognition.face_encodings(captured_frame, face_locations)[0]

        recognized_user = None
        min_distance = 0.5
        user_data = load_user_data_csv()

        for name, user_info in user_data.items():
            registered_encoding = user_info["encoding"]
            distance = face_recognition.face_distance([registered_encoding], face_encoding)[0]

            if distance < min_distance:
                min_distance = distance
                recognized_user = name

        if recognized_user:
            contact = user_data[recognized_user]['contact']
            response_data = {
                'success': True,
                'message': f'Face matched with registered user: {recognized_user}. Contact: {contact}'
            }
            os.remove(captured_frame_path)
            return JsonResponse(response_data)
        else:
            response_data = {
                'success': False,
                'error': 'User not recognized.'
            }
            os.remove(captured_frame_path)
            return JsonResponse(response_data)
    else:
        response_data = {
            'success': False,
            'error': 'Invalid request method.'
        }
        os.remove(captured_frame_path)
        return JsonResponse(response_data, status=400)





def register_user(request):
    if request.method == 'POST':
        time.sleep(3)  
        captured_frame_path = r"C:\Users\saite\Downloads\captured_frame.jpg"
        captured_frame = cv2.imread(captured_frame_path)

        if captured_frame is None:
            response_data = {
                'success': False,
                'error': 'Failed to load the captured frame.'
            }
            return JsonResponse(response_data)

        face_locations = face_recognition.face_locations(captured_frame)
        if not face_locations:
            response_data = {
                'success': False,
                'error': 'No face detected in the captured frame.'
            }
            return JsonResponse(response_data)

        face_encoding = face_recognition.face_encodings(captured_frame, face_locations)[0]

        user_data = load_user_data_csv()

        for existing_user, user_info in user_data.items():
            existing_encoding = user_info.get("encoding")
            if existing_encoding is not None:
                distance = face_recognition.face_distance([existing_encoding], face_encoding)[0]
                if distance < 0.6:
                    os.remove(captured_frame_path)
                    return JsonResponse({'success': False, 'message': f"Similar face already registered as {existing_user}. Skipping registration."})

        name = request.POST.get('name')
        contact = request.POST.get('contact')

        user_data[name] = {
            "contact": contact,
            "encoding": face_encoding.tolist()
        }

        save_user_data_csv(name, user_data)
        os.remove(captured_frame_path)

        return JsonResponse({'success': True, 'message': f"User {name} registered successfully!"})

    else:
        return render(request, 'home.html')






def delete_user_data(request):
    if request.method == 'POST':
        time.sleep(3)
        captured_frame_path = r"C:\Users\saite\Downloads\captured_frame.jpg"
        captured_frame = cv2.imread(captured_frame_path)

        if captured_frame is None:
            response_data = {
                'success': False,
                'error': 'Failed to load the captured frame.'
            }
            return JsonResponse(response_data)

        face_locations = face_recognition.face_locations(captured_frame)
        if not face_locations:
            response_data = {
                'success': False,
                'error': 'No face detected in the captured frame.'
            }
            return JsonResponse(response_data)

        face_encoding = face_recognition.face_encodings(captured_frame, face_locations)[0]

        recognized_user = None
        min_distance = 0.5
        user_data = load_user_data_csv()

        for name, user_info in user_data.items():
            registered_encoding = user_info["encoding"]
            distance = face_recognition.face_distance([registered_encoding], face_encoding)[0]

            if distance < min_distance:
                min_distance = distance
                recognized_user = name

        if recognized_user:
            if recognized_user in user_data:
                del user_data[recognized_user]
                save_user_data_csv1(user_data)
                with open(user_data_path, "w", newline="") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(["Name", "Contact Number", "Face Encodings"])
                    for name, user_info in user_data.items():
                        contact = user_info.get("contact")
                        face_encoding = json.dumps(user_info.get("encoding"))
                        csv_writer.writerow([name, contact, face_encoding])
                os.remove(captured_frame_path)

                return JsonResponse({'success': True, 'message': f"User {recognized_user}'s data has been deleted."})
            else:
                os.remove(captured_frame_path)
                return JsonResponse({'success': False, 'message': 'User not found in data.'})
        else:
            os.remove(captured_frame_path)
            return JsonResponse({'success': False, 'message': 'User not recognized.'})
    else:
        return HttpResponseBadRequest("Invalid request method.")
