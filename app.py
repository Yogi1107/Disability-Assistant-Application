import tkinter as tk
from tkinter import Label, Button, Frame, scrolledtext, messagebox
import cv2
import mediapipe as mp
import pyttsx3
from PIL import Image, ImageTk
import speech_recognition as sr
import pywhatkit
import webbrowser
import time
import threading
import json
import os
import datetime

class DisabilityAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disability Person Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize user profile system
        self.init_user_profile()
        
        # Set up TTS engine
        self.engine = pyttsx3.init()
        
        # Create main UI
        self.create_main_ui()
    
    def init_user_profile(self):
        """Initialize user profile system"""
        if not os.path.exists('user_profiles'):
            os.makedirs('user_profiles')
        
        self.current_user_id = "default_user"
        self.user_profile = self.get_user_profile(self.current_user_id)
    
    def get_user_profile(self, user_id):
        profile_path = f'user_profiles/{user_id}.json'
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                return json.load(f)
        
        return {
            'user_id': user_id,
            'name': 'User ',
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
    
    def save_user_profile(self):
        with open(f'user_profiles/{self.user_profile["user_id"]}.json', 'w') as f:
            json.dump(self.user_profile, f)
    
    def create_main_ui(self):
        self.apply_theme()
        
        header_frame = Frame(self.root, bg="#4a7abc", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        welcome_label = Label(
            header_frame, 
            text="Disability Assistant Application", 
            font=("Helvetica", 24, "bold"),
            bg="#4a7abc",
            fg="white"
        )
        welcome_label.pack(pady=10)
        
        content_frame = Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_feature_buttons(content_frame)
        
        footer_frame = Frame(self.root, bg="#333333", padx=10, pady=5)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = Label(
            footer_frame,
            text="© 2025 Disability Assistant - Final Year Project",
            font=("Helvetica", 10),
            bg="#333333",
            fg="white"
        )
        footer_label.pack(pady=5)
        
        self.speak_welcome_message()

    def apply_theme(self):
        theme = self.user_profile['preferences']['theme']
        self.engine.setProperty('rate', 150 * self.user_profile['preferences']['voice_speed'])
        self.engine.setProperty('volume', self.user_profile['preferences']['voice_volume'])
        
        if theme == 'dark':
            self.root.configure(bg="#222222")
        else:
            self.root.configure(bg="#f0f0f0")

    def create_feature_buttons(self, parent):
        features_frame = Frame(parent, bg="#f0f0f0")
        features_frame.pack(pady=20)
        
        voice_card = self.create_feature_card(
            features_frame,
            "Voice Assistance",
            "For visual impairment assistance",
            "lightblue",
            self.open_voice_assistant
        )
        voice_card.grid(row=0, column=0, padx=20, pady=20)
        
        learning_card = self.create_feature_card(
            features_frame,
            "AI Assistant",
            "For learning disability assistance",
            "lightgreen",
            self.open_learning_assistant
        )
        learning_card.grid(row=0, column=1, padx=20, pady=20)
        
        sign_card = self.create_feature_card(
            features_frame,
            "Sign Detection",
            "For speech impairment assistance",
            "lightcoral",
            self.open_sign_detection
        )
        sign_card.grid(row=0, column=2, padx=20, pady=20)
        
        settings_card = self.create_feature_card(
            features_frame,
            "Settings",
            "Customize application preferences",
            "lightyellow",
            self.open_settings
        )
        settings_card.grid(row=1, column=1, padx=20, pady=20)

    def create_feature_card(self, parent, title, description, color, command):
        card = Frame(parent, bg="white", padx=10, pady=10, relief=tk.RAISED, bd=1)
        
        card_title = Label(
            card,
            text=title,
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        card_title.pack(pady=5)
        
        indicator = Frame(card, bg=color, height=5)
        indicator.pack(fill=tk.X, pady=5)
        
        card_desc = Label(
            card,
            text=description,
            font=("Helvetica", 12),
            bg="white",
            wraplength=200
        )
        card_desc.pack(pady=10)
        
        card_button = Button(
            card,
            text="Launch",
            font=("Helvetica", 12),
            bg="#4a7abc",
            fg="white",
            padx=10,
            pady=5,
            relief=tk.FLAT,
            command=command
        )
        card_button.pack(pady=10)
        
        return card

    def speak_welcome_message(self):
        welcome_text = f"Welcome to the Disability Assistant Application. How may I help you today?"
        threading.Thread(target=self.speak, args=(welcome_text,)).start()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # ===== SETTINGS MODULE ===== 
    def open_settings(self):
        """Open the settings window to customize application preferences"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("700x600")
        settings_window.configure(bg="#f0f0f0")
        
        # Header frame
        header_frame = Frame(settings_window, bg="#4a7abc", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        header_label = Label(
            header_frame,
            text="Settings",
            font=("Helvetica", 22, "bold"),
            bg="#4a7abc",
            fg="white"
        )
        header_label.pack(pady=5)
        
        # Main content
        content_frame = Frame(settings_window, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Voice settings section
        voice_frame = Frame(content_frame, bg="white", padx=15, pady=15, relief=tk.RAISED, bd=1)
        voice_frame.pack(fill=tk.X, pady=10)
        
        voice_title = Label(
            voice_frame,
            text="Voice Settings",
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        voice_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Voice speed slider
        speed_frame = Frame(voice_frame, bg="white")
        speed_frame.pack(fill=tk.X, pady=5)
        
        speed_label = Label(
            speed_frame,
            text="Voice Speed:",
            font=("Helvetica", 12),
            bg="white"
        )
        speed_label.pack(side=tk.LEFT, padx=5)
        
        self.speed_var = tk.DoubleVar(value=self.user_profile['preferences']['voice_speed'])
        speed_slider = tk.Scale(
            speed_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg="white",
            length=300
        )
        speed_slider.pack(side=tk.LEFT, padx=10)
        
        # Voice volume slider
        volume_frame = Frame(voice_frame, bg="white")
        volume_frame.pack(fill=tk.X, pady=5)
        
        volume_label = Label(
            volume_frame,
            text="Voice Volume:",
            font=("Helvetica", 12),
            bg="white"
        )
        volume_label.pack(side=tk.LEFT, padx=5)
        
        self.volume_var = tk.DoubleVar(value=self.user_profile['preferences']['voice_volume'])
        volume_slider = tk.Scale(
            volume_frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            bg="white",
            length=300
        )
        volume_slider.pack(side=tk.LEFT, padx=10)
        
        # Test voice button
        test_button = Button(
            voice_frame,
            text="Test Voice",
            command=lambda: self.test_voice_settings(self.speed_var.get(), self.volume_var.get()),
            font=("Helvetica", 12),
            bg="#4a7abc",
            fg="white",
            padx=10,
            pady=5
        )
        test_button.pack(pady=10)
        
        # Appearance settings section
        appearance_frame = Frame(content_frame, bg="white", padx=15, pady=15, relief=tk.RAISED, bd=1)
        appearance_frame.pack(fill=tk.X, pady=10)
        
        appearance_title = Label(
            appearance_frame,
            text="Appearance Settings",
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        appearance_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Theme selection
        theme_frame = Frame(appearance_frame, bg="white")
        theme_frame.pack(fill=tk.X, pady=5)
        
        theme_label = Label(
            theme_frame,
            text="Theme:",
            font=("Helvetica", 12),
            bg="white"
        )
        theme_label.pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value=self.user_profile['preferences']['theme'])
        
        theme_light = tk.Radiobutton(
            theme_frame,
            text="Light",
            variable=self.theme_var,
            value="light",
            bg="white",
            font=("Helvetica", 12)
        )
        theme_light.pack(side=tk.LEFT, padx=10)
        
        theme_dark = tk.Radiobutton(
            theme_frame,
            text="Dark",
            variable=self.theme_var,
            value="dark",
            bg="white",
            font=("Helvetica", 12)
        )
        theme_dark.pack(side=tk.LEFT, padx=10)
        
        # Font size selection
        font_frame = Frame(appearance_frame, bg="white")
        font_frame.pack(fill=tk.X, pady=5)
        
        font_label = Label(
            font_frame,
            text="Font Size:",
            font=("Helvetica", 12),
            bg="white"
        )
        font_label.pack(side=tk.LEFT, padx=5)
        
        self.font_var = tk.StringVar(value=self.user_profile['preferences']['font_size'])
        
        font_small = tk.Radiobutton(
            font_frame,
            text="Small",
            variable=self.font_var,
            value="small",
            bg="white",
            font=("Helvetica", 12)
        )
        font_small.pack(side=tk.LEFT, padx=10)
        
        font_medium = tk.Radiobutton(
            font_frame,
            text="Medium",
            variable=self.font_var,
            value="medium",
            bg="white",
            font=("Helvetica", 12)
        )
        font_medium.pack(side=tk.LEFT, padx=10)
        
        font_large = tk.Radiobutton(
            font_frame,
            text="Large",
            variable=self.font_var,
            value="large",
            bg="white",
            font=("Helvetica", 12)
        )
        font_large.pack(side=tk.LEFT, padx=10)
        
        # Emergency contacts section
        emergency_frame = Frame(content_frame, bg="white", padx=15, pady=15, relief=tk.RAISED, bd=1)
        emergency_frame.pack(fill=tk.X, pady=10)
        
        emergency_title = Label(
            emergency_frame,
            text="Emergency Contacts",
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        emergency_title.pack(anchor=tk.W, pady=(0, 10))
        
        # List of emergency contacts (simplified for this example)
        contacts_frame = Frame(emergency_frame, bg="white")
        contacts_frame.pack(fill=tk.X, pady=5)
        
        self.contacts_list = tk.Listbox(
            contacts_frame,
            height=4,
            width=50,
            font=("Helvetica", 12)
        )
        self.contacts_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Fill the listbox with contacts
        for contact in self.user_profile.get('emergency_contacts', []):
            self.contacts_list.insert(tk.END, contact)
        
        # Save and close buttons
        button_frame = Frame(settings_window, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=20)
        
        save_button = Button(
            button_frame,
            text="Save Settings",
            command=self.save_settings,
            font=("Helvetica", 14),
            bg="#28a745",
            fg="white",
            padx=20,
            pady=10
        )
        save_button.pack(side=tk.LEFT, padx=10)
        
        close_button = Button(
            button_frame,
            text="Close",
            command=settings_window.destroy,
            font=("Helvetica", 14),
            bg="red",
            fg="white",
            padx=20,
            pady=10
        )
        close_button.pack(side=tk.RIGHT, padx=10)

    def test_voice_settings(self, speed, volume):
        """Test the voice settings with the current settings"""
        # Save current settings
        current_speed = self.engine.getProperty('rate')
        current_volume = self.engine.getProperty('volume')
        
        # Apply test settings
        self.engine.setProperty('rate', 150 * speed)
        self.engine.setProperty('volume', volume)
        
        # Speak test message
        test_text = "This is a test of the voice settings."
        threading.Thread(target=self.speak, args=(test_text,)).start()
        
        # Restore original settings (will be changed later if user saves)
        self.engine.setProperty('rate', current_speed)
        self.engine.setProperty('volume', current_volume)

    def save_settings(self):
        """Save the user settings to the profile"""
        # Update user profile with the new settings
        self.user_profile['preferences']['voice_speed'] = self.speed_var.get()
        self.user_profile['preferences']['voice_volume'] = self.volume_var.get()
        self.user_profile['preferences']['theme'] = self.theme_var.get()
        self.user_profile['preferences']['font_size'] = self.font_var.get()
        
        # Save to disk
        self.save_user_profile()
        
        # Apply the settings
        self.apply_theme()
        
        messagebox.showinfo("Settings", "Settings have been saved successfully!")

    # ===== AI LEARNING ASSISTANT MODULE =====
    def open_learning_assistant(self):
        """Open the AI Learning Assistant window"""
        learning_window = tk.Toplevel(self.root)
        learning_window.title("AI Learning Assistant")
        learning_window.geometry("800x600")
        learning_window.configure(bg="#f0f0f0")
        
        # Header frame
        header_frame = Frame(learning_window, bg="#4a7abc", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        header_label = Label(
            header_frame,
            text="AI Learning Assistant",
            font=("Helvetica", 22, "bold"),
            bg="#4a7abc",
            fg="white"
        )
        header_label.pack(pady=5)
        
        # Main content
        content_frame = Frame(learning_window, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add your AI learning assistant features here
        info_label = Label(
            content_frame,
            text="This is where the AI Learning Assistant features will be implemented.",
            font=("Helvetica", 14),
            bg="#f0f0f0"
        )
        info_label.pack(pady=20)
        
        # Close button
        close_button = Button(
            learning_window,
            text="Close",
            command=learning_window.destroy,
            font=("Helvetica", 14),
            bg="red",
            fg="white",
            padx=20,
            pady=10
        )
        close_button.pack(pady=20)

    # ===== SIGN DETECTION MODULE =====
    def open_sign_detection(self):
        """Open the sign detection window"""
        sign_window = tk.Toplevel(self.root)
        sign_window.title("Sign Detection for Speech Impairment")
        sign_window.geometry("1000x800")
        sign_window.configure(bg="#f0f0f0")
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        
        # Welcome message
        self.engine.say("WELCOME TO SIGN GESTURE APPLICATION FOR COMMUNICATION. LET'S BEGIN.")
        self.engine.runAndWait()
        
        # Header frame
        header_frame = Frame(sign_window, bg="#4a7abc", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        header_label = Label(
            header_frame,
            text="Sign Detection",
            font=("Helvetica", 22, "bold"),
            bg="#4a7abc",
            fg="white"
        )
        header_label.pack(pady=5)
        
        # Main content
        content_frame = Frame(sign_window, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Video and detection frame
        top_frame = Frame(content_frame, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, pady=10)
        
        # Video frame
        video_frame = Frame(top_frame, bg="black", width=640, height=480)
        video_frame.pack(side=tk.LEFT, padx=10)
        
        # Make sure the frame keeps its size
        video_frame.pack_propagate(False)
        
        self.video_label = Label(video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        # Detection info frame
        detection_frame = Frame(top_frame, bg="white", padx=15, pady=15, relief=tk.RAISED, bd=1)
        detection_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Gesture detection label
        gesture_label_title = Label(
            detection_frame,
            text="Detected Gesture:",
            font=("Helvetica", 14, "bold"),
            bg="white"
        )
        gesture_label_title.pack(anchor=tk.W, pady=(0, 5))
        
        self.gesture_label = Label(
            detection_frame,
            text="DETECTING...",
            font=("Helvetica", 18),
            bg="white"
        )
        self.gesture_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Meaning label
        meaning_label_title = Label(
            detection_frame,
            text="Meaning:",
            font=("Helvetica", 14, "bold"),
            bg="white"
        )
        meaning_label_title.pack(anchor=tk.W, pady=(0, 5))
        
        self.sentence_label = Label(
            detection_frame,
            text="...",
            font=("Helvetica", 16),
            bg="white",
            wraplength=300,
            justify=tk.LEFT
        )
        self.sentence_label.pack(anchor=tk.W)
        
        # Sentence builder section
        sentence_frame = Frame(content_frame, bg="white", padx=15, pady=15, relief=tk.RAISED, bd=1)
        sentence_frame.pack(fill=tk.X, pady=20)
        
        sentence_title = Label(
            sentence_frame,
            text="Sentence Builder",
            font=("Helvetica", 16, "bold"),
            bg="white"
        )
        sentence_title.pack(anchor=tk.W, pady=(0, 10))
        
        self.current_sentence = scrolledtext.ScrolledText(
            sentence_frame,
            wrap=tk.WORD,
            height=3,
            font=("Helvetica", 14)
        )
        self.current_sentence.pack(fill=tk.X, pady=5)
        
        # Buttons frame
        buttons_frame = Frame(sentence_frame, bg="white")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Add to sentence button
        add_button = Button(
            buttons_frame,
            text="Add to Sentence",
            command=self.add_to_sentence,
            font=("Helvetica", 12),
            bg="#4a7abc",
            fg="white",
            padx=10,
            pady=5
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        # Speak sentence button
        speak_button = Button(
            buttons_frame,
            text="Speak Sentence",
            command=self.speak_current_sentence,
            font=("Helvetica", 12),
            bg="#28a745",
            fg="white",
            padx=10,
            pady=5
        )
        speak_button.pack(side=tk.LEFT, padx=5)
        
        # Clear sentence button
        clear_button = Button(
            buttons_frame,
            text="Clear Sentence",
            command=self.clear_sentence,
            font=("Helvetica", 12),
            bg="#dc3545",
            fg="white",
            padx=10,
            pady=5
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Gesture library section
        library_frame = Frame(content_frame, bg="#f0f0f0")
        library_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        library_title = Label(
            library_frame,
            text="Gesture Library",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0"
        )
        library_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Gesture library grid (showing available gestures)
        self.create_gesture_library(library_frame)
        
        # Close button at the bottom
        close_button = Button(
            sign_window,
            text="Close",
            command=lambda: self.close_sign_window(sign_window),
            font=("Helvetica", 14),
            bg="red",
            fg="white",
            padx=20,
            pady=10
        )
        close_button.pack(pady=20)
        
        # Start video capture
        self.cap = cv2.VideoCapture(0)
        self.last_spoken_gesture = None
        self.is_running = True
        
        # Start video stream in a separate thread
        threading.Thread(target=self.video_stream).start()

    def create_gesture_library(self, parent):
        """Create a grid showing available gestures"""
        gestures_frame = Frame(parent, bg="#f0f0f0")
        gestures_frame.pack(fill=tk.X)
        
        # Define some basic gestures
        gestures = [
            {"name": "Open Palm", "meaning": "Hello! How are you?"},
            {"name": "Pointing", "meaning": "Look there! What is that?"},
            {"name": "Thumbs Up", "meaning": "Yes! Good! Okay."},
            {"name": "Thumbs Down", "meaning": "No! Not Good."},
            {"name": "Victory/Peace", "meaning": "Victory! Everything is fine."}
        ]
        
        # Add any custom gestures from user profile
        for gesture_name, gesture_info in self.user_profile.get('custom_gestures', {}).items():
            gestures.append({
                "name": gesture_name,
                "meaning": gesture_info["meaning"]
            })
        
        # Create a card for each gesture
        for i, gesture in enumerate(gestures):
            frame = Frame(gestures_frame, bg="white", padx=10, pady=10, relief=tk.RAISED, bd=1)
            frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            # Placeholder for gesture image (in a real app, you'd have actual images)
            image_placeholder = Frame(frame, bg="lightgray", width=100, height=80)
            image_placeholder.pack(pady=5)
            image_placeholder.pack_propagate(False)
            
            Label(image_placeholder, text=gesture["name"], bg="lightgray").pack(pady=30)
            
            Label(
                frame,
                text=gesture["name"],
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(pady=5)
            
            Label(
                frame,
                text=gesture["meaning"],
                font=("Helvetica", 10),
                bg="white",
                wraplength=150
            ).pack(pady=5)

    def recognize_gesture(self, landmarks):
        """Recognize hand gesture from landmarks"""
        thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip = landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]
        thumb_ip, index_mcp, middle_mcp, ring_mcp, pinky_mcp = landmarks[3], landmarks[5], landmarks[9], landmarks[13], landmarks[17]
        
        # Check for custom gestures if available
        custom_gestures = self.user_profile.get('custom_gestures', {})
        if custom_gestures:
            # A real implementation would have more sophisticated pattern matching
            pass
        
        # Basic gesture recognition
        if index_tip[1] < index_mcp[1] and middle_tip[1] < middle_mcp[1] and ring_tip[1] < ring_mcp[1] and pinky_tip[1] < pinky_mcp[1]:
            return "Open Palm", "Hello! How are you?"
        elif index_tip[1] < index_mcp[1] and middle_tip[1] > middle_mcp[1] and ring_tip[1] > ring_mcp[1] and pinky_tip[1] > pinky_mcp[1]:
            return "Pointing", "Look there! What is that?"
        elif thumb_tip[0] < thumb_ip[0] and index_tip[0] < middle_tip[0] and middle_tip[0] < ring_tip[0] and ring_tip[0] < pinky_tip[0]:
            return "Thumbs Up", "Yes! Good! Okay."
        elif thumb_tip[0] > thumb_ip[0] and index_tip[0] > middle_tip[0] and middle_tip[0] > ring_tip[0] and ring_tip[0] > pinky_tip[0]:
            return "Thumbs Down", "No! Not Good."
        elif index_tip[1] < index_mcp[1] and thumb_tip[1] < thumb_ip[1] and middle_tip[1] < middle_mcp[1] and ring_tip[1] > ring_mcp[1] and pinky_tip[1] > pinky_mcp[1]:
            return "Victory (Peace)", "Victory! Everything is fine."
        
        return "DETECTING...", "..."

    def video_stream(self):
        """Process video frames for sign detection"""
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            gesture_text = "DETECTING..."
            sentence = "..."
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                    gesture_text, sentence = self.recognize_gesture(landmarks)
            
            # Update GUI (safely from the main thread)
            self.root.after(0, self.update_sign_detection_ui, frame, gesture_text, sentence)
            
            # Small delay to reduce CPU usage
            time.sleep(0.01)

    def update_sign_detection_ui(self, frame, gesture_text, sentence):
        """Update sign detection UI with new frame and detection"""
        # Convert the OpenCV frame to a format Tkinter can display
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        
        # Update detection labels
        self.gesture_label.config(text=gesture_text)
        self.sentence_label.config(text=sentence)
        
        # Speak the meaning if it's a new gesture
        if gesture_text != "DETECTING..." and gesture_text != self.last_spoken_gesture:
            self.last_spoken_gesture = gesture_text
            threading.Thread(target=self.speak, args=(sentence,)).start()

    def add_to_sentence(self):
        """Add current detected gesture meaning to the sentence builder"""
        current_meaning = self.sentence_label.cget("text")
        if current_meaning and current_meaning != "...":
            current_text = self.current_sentence.get("1.0", tk.END).strip()
            if current_text:
                new_text = f"{current_text} {current_meaning}"
            else:
                new_text = current_meaning
            
            self.current_sentence.delete("1.0", tk.END)
            self.current_sentence.insert("1.0", new_text)

    def speak_current_sentence(self):
        """Speak the text in the sentence builder"""
        sentence = self.current_sentence.get("1.0", tk.END).strip()
        if sentence:
            threading.Thread(target=self.speak, args=(sentence,)).start()

    def clear_sentence(self):
        """Clear the sentence builder"""
        self.current_sentence.delete("1.0", tk.END)

    def close_sign_window(self, window):
        """Close the sign detection window and clean up resources"""
        self.is_running = False
        time.sleep(0.2)  # Give time for video thread to stop
        if self.cap:
            self.cap.release()
        window.destroy()

    # ===== VOICE ASSISTANT MODULE =====
    def open_voice_assistant(self):
        """Open the voice assistant window for visually impaired users"""
        voice_window = tk.Toplevel(self.root)
        voice_window.title("Voice Assistant (for Blind)")
        voice_window.geometry("800x700")
        voice_window.configure(bg="#f0f0f0")
        
        # Header frame
        header_frame = Frame(voice_window, bg="#4a7abc", padx=20, pady=10)
        header_frame.pack(fill=tk.X)
        
        header_label = Label(
            header_frame,
            text="Voice Assistant",
            font=("Helvetica", 22, "bold"),
            bg="#4a7abc",
            fg="white"
        )
        header_label.pack(pady=5)
        
        # Main content
        content_frame = Frame(voice_window, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            state='disabled',
            height=20,
            bg="white",
            font=("Helvetica", 12)
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Control buttons frame
        controls_frame = Frame(content_frame, bg="#f0f0f0")
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Listen button
        listen_button = Button(
            controls_frame,
            text="Listen",
            command=self.start_listening,
            font=("Helvetica", 14),
            bg="#28a745",
            fg="white",
            padx=20,
            pady=10
        )
        listen_button.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        stop_button = Button(
            controls_frame,
            text="Stop",
            command=self.stop_listening,
            font=("Helvetica", 14),
            bg="#dc3545",
            fg="white",
            padx=20,
            pady=10
        )
        stop_button.pack(side=tk.LEFT, padx=10)
        
        # Help button
        help_button = Button(
            controls_frame,
            text="Help / Commands",
            command=self.show_voice_commands,
            font=("Helvetica", 14),
            bg="#17a2b8",
            fg="white",
            padx=20,
            pady=10
        )
        help_button.pack(side=tk.LEFT, padx=10)
        
        # Quick action buttons
        actions_frame = Frame(content_frame, bg="#f0f0f0")
        actions_frame.pack(fill=tk.X, pady=20)
        
        actions_label = Label(
            actions_frame,
            text="Quick Actions:",
            font=("Helvetica", 14, "bold"),
            bg="#f0f0f0"
        )
        actions_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create quick action buttons
        actions = [
            {"text": "What time is it?", "command": lambda: self.process_voice_command("what time is it")},
            {"text": "Open YouTube", "command": lambda: self.process_voice_command("open youtube")},
            {"text": "Read the news", "command": lambda: self.process_voice_command("read the news")},
            {"text": "Emergency contact", "command": lambda: self.process_voice_command("call emergency contact")}
        ]
        
        action_buttons_frame = Frame(actions_frame, bg="#f0f0f0")
        action_buttons_frame.pack(fill=tk.X)
        
        for i, action in enumerate(actions):
            action_btn = Button(
                action_buttons_frame,
                text=action["text"],
                command=action["command"],
                font=("Helvetica", 12),
                bg="#f8f9fa",
                padx=10,
                pady=5
            )
            action_btn.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
        
        # Make columns equal width
        action_buttons_frame.grid_columnconfigure(0, weight=1)
        action_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Close button
        close_button = Button(
            voice_window,
            text="Close",
            command=voice_window.destroy,
            font=("Helvetica", 14),
            bg="red",
            fg="white",
            padx=20,
            pady=10
        )
        close_button.pack(pady=20)
        
        # Initialize variables
        self.listening = False
        self.recognizer = sr.Recognizer()
        
        # Add initial message
        self.update_chat("Assistant", "Hello! I'm your voice assistant. How can I help you today?")
        threading.Thread(target=self.speak, args=("Hello! I'm your voice assistant. How can I help you today?",)).start()

    def update_chat(self, role, message):
        """Update the chat display with a new message"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{role}: {message}\n\n")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')

    def start_listening(self):
        """Start listening for voice commands"""
        if not self.listening:
            self.listening = True
            self.update_chat("Assistant", "Listening...")
            threading.Thread(target=self.listen_for_command).start()

    def stop_listening(self):
        """Stop listening for voice commands"""
        self.listening = False
        self.update_chat("Assistant", "Stopped listening.")

    def listen_for_command(self):
        """Listen for a voice command"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5)
        
            try:
                command = self.recognizer.recognize_google(audio).lower()
                self.root.after(0, lambda: self.update_chat("You", command))
                self.root.after(0, lambda: self.process_voice_command(command))
            except sr.UnknownValueError:
                self.root.after(0, lambda: self.update_chat("Assistant", "Sorry, I didn't understand that."))
                threading.Thread(target=self.speak, args=("Sorry, I didn't understand that.",)).start()
            except sr.RequestError:
                self.root.after(0, lambda: self.update_chat("Assistant", "Sorry, speech recognition service is unavailable."))
                threading.Thread(target=self.speak, args=("Sorry, speech recognition service is unavailable.",)).start()
        
        except Exception as e:
            self.root.after(0, lambda: self.update_chat("Assistant", f"Error: {str(e)}"))
        
        finally:
            self.listening = False

    def process_voice_command(self, command):
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
            self.update_chat("Assistant", response)
            threading.Thread(target=self.speak, args=(response,)).start()
            pywhatkit.playonyt(search_query)
            return
        
        elif "search" in command:
            search_query = command.replace("search", "").replace("for", "").strip()
            response = f"Searching for {search_query}."
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            
        elif "read" in command and "news" in command:
            response = "Here are the latest headlines. Opening a news website."
            webbrowser.open("https://news.google.com")
        
        elif "call emergency contact" in command:
            if self.user_profile['emergency_contacts']:
                contact = self.user_profile['emergency_contacts'][0]  # Just an example, you can implement a selection mechanism
                response = f"Calling {contact}."
                # Here you would implement the actual calling functionality
            else:
                response = "No emergency contacts found in your profile."
        
        # Update chat with the response
        self.update_chat("Assistant", response)
        threading.Thread(target=self.speak, args=(response,)).start()

    def show_voice_commands(self):
        """Show a message box with available voice commands"""
        commands = (
            "Available Commands:\n"
            "- What time is it?\n"
            "- Open YouTube\n"
            "- Read the news\n"
            "- Call emergency contact"
        )
        messagebox.showinfo("Voice Commands", commands)

if __name__ == "__main__":
    root = tk.Tk()
    app = DisabilityAssistantApp(root)
    root.mainloop()
