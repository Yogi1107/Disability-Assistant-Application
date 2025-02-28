import tkinter as tk
from tkinter import messagebox
from tkhtmlview import HTMLLabel
import os
import json

class DisabilityAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disability Assistant Application")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize user profile system
        self.init_user_profile()
        
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
            'name': 'User    ',
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
    
    def create_main_ui(self):
        # Load HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Disability Assistant Application</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
            <style>
                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
                body {
                    font-family: 'Roboto', sans-serif;
                    background-color: #f0f0f0;
                    color: #333;
                }
                header {
                    background-color: #4a7abc;
                    padding: 20px;
                    text-align: center;
                    color: white;
                }
                h1 {
                    font-size: 2.5em;
                }
                main {
                    padding: 20px;
                }
                .feature-container {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 20px;
                }
                .feature-card {
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    text-align: center;
                    transition: transform 0.2s;
                }
                .feature-card:hover {
                    transform: translateY(-5px);
                }
                .feature-card h2 {
                    font-size: 1.5em;
                    margin-bottom: 10px;
                }
                .feature-card p {
                    font-size: 1em;
                    margin-bottom: 20px;
                }
                .feature-card button {
                    background-color: #4a7abc;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    cursor: pointer;
                    font-size: 1em;
                    transition: background-color 0.3s;
                }
                .feature-card button:hover {
                    background-color: #3a5a8c;
                }
                footer {
                    background-color: #333;
                    color: white;
                    text-align: center;
                    padding: 10px;
                    position: relative;
                    bottom: 0;
                    width: 100%;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Disability Assistant Application</h1>
            </header>
            <main>
                <div class="feature-container">
                    <div class="feature-card" onclick="openVoiceAssistant()">
                        <h2>Voice Assistance</h2>
                        <p>For visual impairment assistance</p>
                        <button>Launch</button>
                    </div>
                    <div class="feature-card" onclick="openLearningAssistant()">
                        <h2>AI Assistant</h2>
                        <p>For learning disability assistance</p>
                        <button>Launch</button>
                    </div>
                    <div class="feature-card" onclick="openSignDetection()">
                        <h2>Sign Detection</h2>
                        <p>For speech impairment assistance</p>
                        <button>Launch</button>
                    </div>
                    <div class="feature-card" onclick="openSettings()">
                        <h2>Settings</h2>
                        <p>Customize application preferences</p>
                        <button>Launch</button>
                    </div>
                </div>
            </main>
            <footer>
                <p>© 2025 Disability Assistant - Final Year Project</p>
            </footer>
        </body>
        <script>
            function openVoiceAssistant() {
                alert("Voice Assistant feature is not implemented yet.");
            }
            function openLearningAssistant() {
                alert("AI Assistant feature is not implemented yet.");
            }
            function openSignDetection() {
                alert("Sign Detection feature is not implemented yet.");
            }
            function openSettings() {
                alert("Settings feature is not implemented yet.");
            }
        </script>
        </html>
        """
        
        # Create HTML label
        self.html_label = HTMLLabel(self.root, html=html_content)
        self.html_label.pack(fill=tk.BOTH, expand=True)

    def open_voice_assistant(self):
        messagebox.showinfo("Voice Assistant", "Opening Voice Assistant...")

    def open_learning_assistant(self):
        messagebox.showinfo("AI Assistant", "Opening AI Assistant...")

    def open_sign_detection(self):
        messagebox.showinfo("Sign Detection", "Opening Sign Detection...")

    def open_settings(self):
        messagebox.showinfo("Settings", "Opening Settings...")

if __name__ == "__main__":
    root = tk.Tk()
    app = DisabilityAssistantApp(root)
    root.mainloop()
