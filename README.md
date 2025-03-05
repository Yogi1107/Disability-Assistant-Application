# Disability Assistant Application

## Overview
The Disability Assistant Application is a comprehensive tool designed to assist individuals with disabilities. It integrates various features such as voice assistance, AI learning support, sign detection for speech impairment, and customizable user profiles. The application aims to enhance accessibility and provide support for users with different needs.

## Features
- **Voice Assistance**: A voice-controlled interface for visually impaired users, allowing them to interact with the application using voice commands.
- **AI Learning Assistant**: A dedicated section for users with learning disabilities, providing educational support and resources.
- **Sign Detection**: Utilizes computer vision to recognize hand gestures, aiding communication for users with speech impairments.
- **Customizable User Profiles**: Users can create profiles with personalized settings, including voice speed, volume, theme, and emergency contacts.
- **Emergency Contact Management**: Users can store and manage emergency contacts for quick access.
- **Voice Command Processing**: The application can respond to various voice commands, such as checking the time, opening websites, and more.

## Technologies Used
- **Python**: The programming language used for development.
- **Tkinter**: For creating the graphical user interface (GUI).
- **OpenCV**: For video processing and gesture recognition.
- **MediaPipe**: For hand tracking and gesture detection.
- **SpeechRecognition**: For processing voice commands.
- **pyttsx3**: For text-to-speech functionality.
- **pywhatkit**: For performing actions like searching on YouTube.
- **Pillow**: For image processing tasks.

## Installation
To run the Disability Assistant Application, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Yogi1107/Disability-Assistant-Application.git
   cd Disability-Assistant-Application
Install the required packages: Ensure you have Python installed, then install the necessary libraries using pip:

```bash
pip install opencv-python mediapipe pyttsx3 SpeechRecognition pywhatkit Pillow
```

Run the application: Execute the following command to start the application:
```bash
python main.py
```

##Usage
Upon launching the application, users will be greeted with a welcome message.
Users can navigate through the main features using the buttons provided.
The voice assistant can be activated to listen for commands, and users can interact with the application using their voice.
The sign detection feature will utilize the webcam to recognize hand gestures and provide feedback.
Customization
Users can customize their profiles by accessing the settings menu, where they can adjust voice speed, volume, theme, and manage emergency contacts.

##Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

##Acknowledgments
Thanks to the developers of the libraries used in this project, including OpenCV, MediaPipe, and others.
Special thanks to the community for their support and contributions to accessibility technologies.
