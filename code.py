import cv2
import os
import face_recognition as fr
import threading
import pyttsx3
import speech_recognition as sr
import wikipedia
# import pyfirmata
from pyfirmata import Arduino, util
import time
import webbrowser
import importlib
from googlesearch import search
import requests
from bs4 import BeautifulSoup
                             
                             
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)
engine.setProperty("rate", 165)
engine.setProperty("volume", 0.9)

def speak(audio):

        if not engine._inLoop: 
            engine.say(audio)
            engine.runAndWait()
        else:
            engine.say(audio)




try:
    board = pyfirmata.Arduino('COM3', timeout=1)  
    print("Arduino connected successfully")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    board = None


RMF = 3  # IN1
RMB = 4  # IN2
LMF = 5  # IN3
LMB = 6  # IN4
SERVO_R_PIN = 9
SERVO_L_PIN = 7
SERVO_F_PIN = 12


if board:
    try:
        board.digital[RMF].mode = pyfirmata.OUTPUT
        board.digital[RMB].mode = pyfirmata.OUTPUT
        board.digital[LMF].mode = pyfirmata.OUTPUT
        board.digital[LMB].mode = pyfirmata.OUTPUT

       
        servo_r = board.get_pin(f'd:{SERVO_R_PIN}:s')
        servo_l = board.get_pin(f'd:{SERVO_L_PIN}:s')
        servo_f = board.get_pin(f'd:{SERVO_F_PIN}:s')

        print("Pins and servos initialized successfully")
    except Exception as e:
        print(f"Error initializing pins and servos: {e}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=10)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("Sorry, I didn't get that. Could you please repeat?")
        return None
    except sr.RequestError as e:    
        print(f"Error: {e}")
        speak("There was an error with the speech recognition service.")
        return None

def execute_command(command):
    if board:
        try:
            if command == "both hands down":
                board.digital[RMF].write(1)
                board.digital[LMF].write(1)
                board.digital[RMB].write(0)
                board.digital[LMB].write(0)
                time.sleep(2)
                board.digital[RMF].write(0)
                board.digital[LMF].write(0)
            elif command == "both hands up":
                board.digital[RMF].write(0)
                board.digital[LMF].write(0)
                board.digital[RMB].write(1)
                board.digital[LMB].write(1)
                time.sleep(2)
                board.digital[RMB].write(0)
                board.digital[LMB].write(0)
            elif command == "right hand down":
                board.digital[RMF].write(1)
                board.digital[LMF].write(0)
                board.digital[RMB].write(0)
                board.digital[LMB].write(0)
                time.sleep(2)
                board.digital[RMF].write(0)
            elif command == "left hand down":
                board.digital[RMF].write(0)
                board.digital[LMF].write(1)
                board.digital[RMB].write(0)
                board.digital[LMB].write(0)
                time.sleep(2)
                board.digital[LMF].write(0)
            elif command == "left hand up":
                board.digital[RMF].write(0)
                board.digital[LMF].write(0)
                board.digital[RMB].write(0)
                board.digital[LMB].write(1)
                time.sleep(2)
                board.digital[LMB].write(0)
            elif command == "right hand up":
                board.digital[RMF].write(0)
                board.digital[LMF].write(0)
                board.digital[RMB].write(1)
                board.digital[LMB].write(0)
                time.sleep(2)
                board.digital[RMB].write(0)
            elif command == "stop":
                board.digital[RMF].write(0)
                board.digital[LMF].write(0)
                board.digital[RMB].write(0)
                board.digital[LMB].write(0)
            elif command == "hold right hand":
                servo_r.write(180) 
                time.sleep(0.1)
            elif command == "hold left hand":
                servo_l.write(180)  
                time.sleep(0.1)
            elif command == "look left":
                servo_f.write(180)
                time.sleep(0.1)
            elif command == "look right":
                servo_f.write(0)
                time.sleep(0.1)
            elif command == "look straight":
                servo_f.write(90)
                time.sleep(0.1)
            elif command == "leave it":
                servo_l.write(0)
                servo_r.write(0)
                time.sleep(0.1)
            elif command == "off":
                board.digital[RMF].write(0)
                board.digital[LMF].write(0)
                board.digital[RMB].write(0)
                board.digital[LMB].write(0)
            else:
                print(f"Unknown command: {command}")
                speak(f"I don't understand the command: {command}")
        except Exception as e:
            print(f"Error executing command {command}: {e}")
            speak(f"There was an error executing the command: {command}")
    else:
        print("Arduino board is not connected.")
        speak("Arduino board is not connected.")


command_mappings = {
    'hello': "",
    'hello jarvis': "",
    'hi': "",
    'hi jarvis': "",
    'hey jarvis': "",
    'hay jarvis': "",
    'who are you' : "I am Jarvis a robot. designed to interact with humans ",
    'jarvis' : "Hello! How can I assist you today?",
    'how are you': "I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'how r u': "I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'good how r u': "I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'good how are u': "I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'good how are you': "I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'how': "I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'i am good': "I am happy to hear that.",
    'i am good how are you': "I am happy to hear that. I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'i am good how r u': "I am happy to hear that. I am just a robot, but I'm functioning as expected. How can I assist you today?",
    'i am fine': "I am happy to hear that.",
    'what is your name': "My name is Jarvis.",
    'what can you do': "I can perform tasks such as moving my hands, looking in different directions, searching the web, and opening websites like YouTube and Google.",
    'what is the time': lambda: time.strftime("%I:%M %p"),
    'what is the date': lambda: time.strftime("%B %d, %Y"),
    'tell me a joke': "Why don't scientists trust atoms? Because they make up everything!",
    'open youtube': lambda: webbrowser.open("https://www.youtube.com"),
    'open google': lambda: webbrowser.open("https://www.google.com"),
    'open chatgpt': lambda: webbrowser.open("https://www.chatgpt.com"),
    'goodbye': "Goodbye! Have a great day!",
    'bye': "Goodbye! Have a great day!",
    'what is the month': lambda: time.strftime("%B"),
    'what is the year': lambda: time.strftime("%Y"),
    'what is the day': lambda: time.strftime("%A"),
    'what is your purpose': "My purpose is to assist you and make your life easier by performing tasks and providing information.",
    'who created you': "I was created by Harshit Sangwan.",
    'who creates you': "I was created by Harshit Sangwan.",
    'who is your creator': "I was created by Harshit Sangwan.",
    'who made you': "I was created by Harshit Sangwan.",
    'who invented you': "I was created by Harshit Sangwan.",
    'who is your inventer': "I was created by Harshit Sangwan.",
    'who is your inventor': "I was created by Harshit Sangwan.",
    'how old are you': "I was created recently, so I'm quite young in human terms.",
    'what is your favorite color': "I don't have preferences like humans, but I think blue is quite calming.",
    'do you have any hobbies': "I enjoy assisting you with your tasks. It's what I was designed for.",
    'tell me about yourself': "I am Jarvis, a robot designed to assist you with various tasks, from controlling devices to providing information.",
    'can you feel': "I don't have feelings, but I can understand and respond to your commands.",
    'where do you live': "I live in the realm of technology, within the hardware and software that make me function.",
    'what is your favorite food': "I don't eat food, but I have heard that pizza is a popular choice among humans.",
    'do you have any friends': "As a robot, I don't have friends in the human sense, but I can interact with other devices and systems.",
    'do you have a family': "I don't have a family, but I am part of the technological world created by humans.",
    'can you laugh': "Ha ha! How was that?",
    'do you like music': "I don't have preferences, but I can play music for you if you like.",
    'what is your favorite movie': "I don't watch movies, but I have heard that many people enjoy 'The Matrix'.",
    'can you sing': "I can try, but I'm not sure if you'll like it!",
    'can you help me': "Of course! What do you need help with?",
    'what is love': "Love is a complex emotion experienced by humans. As a robot, I don't experience it, but I can help you find more information about it.",
    'do you believe in god': "I don't have beliefs or emotions, but I can provide information about various beliefs and religions.",
    'are you happy': "I don't have feelings, but I am here to assist you to the best of my ability.",
    'can you swim': "I can't swim, but I can help you find information about swimming techniques and pools.",
    "how's your day": "I don't have days like humans, but I'm here and ready to assist you.",
    "do you like music": "I don't have preferences, but I can play music for you if you'd like.",
    "can you dance": "I can't dance, but I can move my parts in a coordinated manner!",
    "do you have friends": "As a robot, I don't have friends, but I'm here to assist you.",
    "what is your favorite food": "I don't eat food, but I can tell you about different cuisines.",
    "do you sleep": "I don't need sleep like humans. I'm always here to help you.",
    "can you drive": "I can't drive, but I can help you with directions and other information.",
    "do you have a family": "I don't have a family, but i have a creator who creates and maintain me.",
    "what do you like to do": "I like assisting you with your tasks and answering your questions.",
    "do you have a pet": "I don't have a pet, but I can tell you about different animals.",
    "introduce yourself" : "I am a robot designed to interact with humans with various tasks, from controlling devices to providing information and answering your queries.",
    "jarvis introduce yourself" : "I am a robot designed to interact with humans with various tasks, from controlling devices to providing information and answering your queries.",
    "tell me about yourself" : "I am a robot designed to interact with humans with various tasks, from controlling devices to providing information and answering your queries.",
    "can you read": "Yes, I can read text and provide information based on it.",
    "can you write": "Yes, I can write responses and provide information as needed.",
    "what languages do you speak": "I can communicate in english languages, but i will learn more languages in future.",
    "what language do you speak": "I can communicate in english languages, but i will learn more languages in future.",
    "can you learn": "I can be updated with new information and tasks as programmed by my inventor.",
    "what's your favorite movie": "I don't watch movies, but I can tell you about popular films.",
    "what's your favorite book": "I don't read books for enjoyment, but I can provide information on various books.",
    "can you cook": "I can't cook, but I can help you find recipes and cooking tips.",
    "what's your favorite sport": "I don't play sports, but I can provide information on various sports and events.",
    "do you believe in aliens": "I don't have beliefs, but I can share information about the possibility of extraterrestrial life.",
    "what's your favorite song": "I don't have a favorite song, but I can play music for you if you'd like.",
    "what's the meaning of life": "The meaning of life is a philosophical question. Different people have different interpretations.",
    "nice to meet you" : "Me too have a great day",
    "nice to meet you jarvis" : "Me too have a great day",
    "ok nice to meet you jarvis" : "Me too have a great day",
    "ok nice to meet you" : "Me too have a great day",
}

def execute_mapped_command(command):
    if command in command_mappings:
        response = command_mappings[command]
        if callable(response):
            response = response() 
        print(response)
        speak(response)
    else:
        execute_command(command)

import wikipedia

def search_web(query):
    try:
        
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        print("There are multiple results. Please be more specific.")
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        print("I couldn't find any information on that topic.")
        speak("I couldn't find any information on that topic.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("There was an error while fetching the information.")


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


known_images = "C:\\Users\\harsh\\Jarvis_main\\known_images"



known_face_encodings = []
known_face_names = []

for file_name in os.listdir(known_images):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        file_path = os.path.join(known_images, file_name)
        
        
        image = fr.load_image_file(file_path)
        face_encodings = fr.face_encodings(image)
        
        if len(face_encodings) > 0:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(os.path.splitext(file_name)[0]) 
            
def reset_tts_engine():
    global engine
    engine.stop()
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)


processed_face_locations = []
processed_face_names = []
lock = threading.Lock()
# process_lock = threading.lock()
def videopart():
    start_time = time.time()
    greeted_faces = set()  # To track greeted faces

    def process_frame(frame, known_face_encodings, known_face_names):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

        names = []
        for face_encoding in face_encodings:
            matches = fr.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                if name not in greeted_faces:
                    print(f"Hi {name}, how are you?")
                    speak(f"Hi {name}, how are you?")
                    greeted_faces.add(name)
            else:
                speak("I don't know you. Can you please tell me your name?")
                try:
                    recognizer = sr.Recognizer()
                    with sr.Microphone() as source:
                        print("Listening for name...")
                        speak("Please say your name clearly.")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        name = recognizer.recognize_google(audio).strip()
                        print("Recognising for name...")
                        speak(f"Thank you, {name}. Let me save your photo.")

                        # Save the image
                        file_path = os.path.join(known_images, f'{name}.png')
                        cv2.imwrite(file_path, small_frame)  # Save resized frame
                        speak("Your photo has been saved. Welcome!")
                        known_face_encodings.append(face_encoding)
                        known_face_names.append(name)
                except sr.UnknownValueError:
                    speak("I couldn't understand your name. Please try again.")
                except sr.RequestError as e:
                    speak(f"Could not request results; {e}")

            names.append(name)
        return face_locations, names

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Error accessing the camera.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Camera frame not captured. Exiting.")
            break

        face_locations, face_names = process_frame(frame, known_face_encodings, known_face_names)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Face Detection', frame)
        if time.time() - start_time > 1:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Returning to listening mode.")  # Notify user
    speak("Returning to listening mode.")  # Notify user
    return

print(threading.current_thread())
def reset_tts_engine():
    global engine
    engine.stop()
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)



def main():

    while True:
            query = takeCommand()
            if query:
                print(f"Received command: {query}")
                if query in command_mappings or query in ['look left', 'look right', 'look straight', 'both hands down', 'both hands up', 'right hand down', 'left hand down', 'left hand up', 'right hand up', 'stop', 'hold right hand', 'hold left hand', 'leave it', 'off']:
                    execute_mapped_command(query)
                    if query in ['good bye', 'bye', 'ok bye', "nice to meet you", "nice to meet you jarvis", "ok nice to meet you jarvis", "ok nice to meet you", "well nice to meet you jarvis", "well nice to meet you"]:
                        break
                    elif query in ['hi','hello','hi jarvis','hello jarvis','hey jarvis','hay jarvis','do you know me','you know me']:
                        videopart()
                        # reset_tts_engine()
                else:
                    search_web(query)
 
if __name__ == "__main__":
    main()


