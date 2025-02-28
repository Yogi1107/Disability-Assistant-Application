from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import datetime
import pywhatkit
import webbrowser

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Initialize user profile system
def init_user_profile():
    """Initialize user profile system"""
    if not os.path.exists('user_profiles'):
        os.makedirs('user_profiles')
    
    current_user_id = "default_user"
    user_profile = get_user_profile(current_user_id)
    return user_profile

def get_user_profile(user_id):
    profile_path = f'user_profiles/{user_id}.json'
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            return json.load(f)
    
    return {
        'user_id': user_id,
        'name': 'User  ',
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

@app.route('/')
def index():
    user_profile = init_user_profile()
    return render_template('index.html', user_profile=user_profile)

@app.route('/voice_assistant', methods=['GET', 'POST'])
def voice_assistant():
    if request.method == 'POST':
        command = request.form.get('command')
        response = process_voice_command(command)
        return render_template('voice_assistant.html', response=response)
    return render_template('voice_assistant.html')

@app.route('/learning_assistant')
def learning_assistant():
    return render_template('learning_assistant.html')

@app.route('/sign_detection')
def sign_detection():
    return render_template('sign_detection.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_profile = init_user_profile()
    if request.method == 'POST':
        user_profile['preferences']['voice_speed'] = float(request.form.get('voice_speed'))
        user_profile['preferences']['voice_volume'] = float(request.form.get('voice_volume'))
        user_profile['preferences']['theme'] = request.form.get('theme')
        user_profile['preferences']['font_size'] = request.form.get('font_size')
        
        # Save the updated profile
        save_user_profile(user_profile)
        flash('Settings have been saved successfully!')
        return redirect(url_for('settings'))
    
    return render_template('settings.html', user_profile=user_profile)

def save_user_profile(user_profile):
    with open(f'user_profiles/{user_profile["user_id"]}.json', 'w') as f:
        json.dump(user_profile, f)

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
        pywhatkit.playonyt(search_query)
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
        if user_profile['emergency_contacts']:
            contact = user_profile['emergency_contacts'][0]  # Just an example
            response = f"Calling {contact}."
            # Here you would implement the actual calling functionality
        else:
            response = "No emergency contacts found in your profile."
    
    return response

if __name__ == '__main__':
    app.run(debug=True)