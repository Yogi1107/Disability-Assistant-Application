from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import json
import datetime
import pywhatkit
import webbrowser
<<<<<<< HEAD
import speech_recognition as sr
import pyttsx3
=======
import secrets
>>>>>>> bee7e37dbce93766b3328cee2faf44ff6462d5de

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure secret key for flashing messages

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Global variable to keep track of the current question index
current_question_index = 0

# Initialize user profile system
def init_user_profile():
    """Initialize user profile system"""
    try:
        if not os.path.exists('user_profiles'):
            os.makedirs('user_profiles')
    except Exception as e:
        print(f"Error creating user_profiles directory: {e}")
        return None
    
    current_user_id = "default_user"
    user_profile = get_user_profile(current_user_id)
    return user_profile

def get_user_profile(user_id):
    profile_path = f'user_profiles/{user_id}.json'
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            return json.load(f)
    
    user_data = {
        'user_id': user_id,
<<<<<<< HEAD
        'name': 'User            ',
=======
        'name': 'User',
>>>>>>> bee7e37dbce93766b3328cee2faf44ff6462d5de
        'preferences': {
            'voice_speed': 1.0,
            'voice_volume': 1.0,
            'theme': 'light',
            'font_size': 'medium'
        },
        'history': [],
        'custom_gestures': {},
        'emergency_contacts': []
    }

    save_user_profile(user_data)  # Save profile if it doesn't exist
    return user_data

def save_user_profile(user_profile):
    """Save user profile to JSON file"""
    try:
        with open(f'user_profiles/{user_profile["user_id"]}.json', 'w') as f:
            json.dump(user_profile, f)
    except Exception as e:
        print(f"Error saving user profile: {e}")

@app.route('/')
def index():
    user_profile = init_user_profile()
    return render_template('index.html', user_profile=user_profile)

@app.route('/voice_assistant', methods=['GET', 'POST'])
def voice_assistant():
    if request.method == 'POST':
        command = request.form.get('command')
        response = process_voice_command(command)
        speak(response)  # Speak the response
        return render_template('voice_assistant.html', response=response)
    return render_template('voice_assistant.html')

@app.route('/learning_assistant', methods=['GET', 'POST'])
def learning_assistant():
    resources = [
        {
            'title': 'American Sign Language (ASL) Basics',
            'description': 'Learn the basics of American Sign Language.',
            'link': 'https://www.startasl.com/'
        },
        {
            'title': 'Sign Language Dictionary',
            'description': 'A comprehensive dictionary for sign language.',
            'link': 'https://www.signlanguage101.com/'
        },
        {
            'title': 'YouTube Sign Language Tutorials',
            'description': 'Watch tutorials on YouTube to learn sign language.',
            'link': 'https://www.youtube.com/results?search_query=sign+language+tutorials'
        },
        {
            'title': 'Communication Tips for Interacting with Disabled Individuals',
            'description': 'Learn how to effectively communicate with disabled individuals.',
            'link': 'https://www.nichd.nih.gov/health/topics/communication/conditioninfo/learning'
        }
    ]
    return render_template('learning_assistant.html', resources=resources)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        questions = request.form.getlist('question')
        options_list = request.form.getlist('options')
        
        if questions and options_list:
            # Load existing quizzes or create a new list
            if os.path.exists('quiz.json'):
                with open('quiz.json', 'r') as f:
                    quiz_data = json.load(f)
            else:
                quiz_data = []  # Initialize as an empty list

            # Append each question and its options
            for i in range(len(questions)):
                quiz_data.append({
                    'question': questions[i],
                    'options': options_list[i*4:(i+1)*4]  # Assuming 4 options per question
                })

            # Save the updated quiz data
            with open('quiz.json', 'w') as f:
                json.dump(quiz_data, f)

            flash('Quiz questions added successfully!')
            return redirect(url_for('quiz'))  # Redirect to the same page to show the quiz

    return render_template('quiz.html')

@app.route('/start_quiz', methods=['GET'])
def start_quiz():
    with open('quiz.json', 'r') as f:
        quiz_data = json.load(f)
    return jsonify(quiz_data)  # Return all quiz questions and options

@app.route('/quiz_command', methods=['POST'])
def quiz_command():
    global current_question_index
    command = request.json.get('command')

    # Load quiz data
    with open('quiz.json', 'r') as f:
        quiz_data = json.load(f)

    # Check if the command is to select an option
    if command.startswith("option "):
        selected_option = command.split(" ")[1].upper()
        option_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

        # Check if the selected option is valid
        if selected_option in option_map and option_map[selected_option] < len(quiz_data[current_question_index]['options']):
            # Here you can process the selected option (e.g., check if it's correct)
            correct_answer = "A"  # Replace with actual logic to determine the correct answer
            if selected_option == correct_answer:
                response = "Correct answer!"
            else:
                response = "Incorrect answer. The correct answer was " + correct_answer + "."

            # Move to the next question
            current_question_index += 1
            if current_question_index < len(quiz_data):
                # Speak the next question
                next_question = quiz_data[current_question_index]['question']
                options = quiz_data[current_question_index]['options']
                speak(next_question + " " + ", ".join(options))  # Speak the next question and options
                return jsonify({'response': response, 'next_question': next_question})
            else:
                response += " Quiz completed!"
                current_question_index = 0  # Reset for the next quiz
                return jsonify({'response': response})

        else:
            return jsonify({'response': 'Invalid option. Please select a valid option.'})

    return jsonify({'response': 'Command not recognized.'})

@app.route('/sign_detection')
def sign_detection():
    # Placeholder for the sign detection feature
    return render_template('sign_detection.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_profile = init_user_profile()
    if request.method == 'POST':
        try:
            user_profile['preferences']['voice_speed'] = float(request.form.get('voice_speed'))
            user_profile['preferences']['voice_volume'] = float(request.form.get('voice_volume'))
            user_profile['preferences']['theme'] = request.form.get('theme')
            user_profile['preferences']['font_size'] = request.form.get('font_size')

            save_user_profile(user_profile)
            flash('Settings have been saved successfully!')
        except Exception as e:
            flash(f"Error saving settings: {e}", 'error')
        return redirect(url_for('settings'))
    
    return render_template('settings.html', user_profile=user_profile)

def process_voice_command(command):
    """Process a voice command"""
    response = "I'm not sure how to help with that."
    
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}."
    
    elif "date" in command or "day" in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today is {current_date}."
    
    elif "open youtube" in command:
        response = "Opening YouTube."
        webbrowser.open("https://www.youtube.com")
    
    elif "search for" in command and "video" in command:
        search_query = command.replace("search for", "").replace("video", "").strip()
        response = f"Searching YouTube for {search_query}."
        try:
            pywhatkit.playonyt(search_query)
        except Exception as e:
            response = f"Could not search on YouTube: {e}"
        return response  # Return early since we are opening a new page
    
    elif "search" in command:
        search_query = command.replace("search", "").replace("for", "").strip()
        response = f"Searching for {search_query}."
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        
    elif "read" in command and "news" in command:
        response = "Here are the latest headlines. Opening a news website."
        webbrowser.open("https://news.google.com")
    
    elif "call emergency contact" in command:
        user_profile = init_user_profile()
        if user_profile and user_profile.get('emergency_contacts'):
            contact = user_profile['emergency_contacts'][0]  # Example: Call first contact
            response = f"Calling {contact}."
            # Here you would implement the actual calling functionality
        else:
            response = "No emergency contacts found in your profile."
    
    return response

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service."

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True, port='5001')
=======
    app.run(debug=True, port=5001)  # Run Flask on port 5001
>>>>>>> bee7e37dbce93766b3328cee2faf44ff6462d5de
