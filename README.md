# Fitness AI Coach 🏋️‍♀️

Fitness AI Coach is an AI-based fitness application that can recognize exercises and automatically count repetitions using a webcam or uploaded video.

The project uses **Computer Vision, Pose Estimation, and Machine Learning** to track body movements and identify different exercises.

## Features

* 🎥 **Video Analysis** – Upload an exercise video and count repetitions.
* 📷 **Webcam Mode** – Perform exercises in front of your webcam and get real-time repetition counts.
* 🤖 **Auto Classify** – Automatically identifies the exercise and counts repetitions.
* 💬 **Fitness Chatbot** – Ask fitness-related questions and get basic guidance.
* 🧍 **Pose Detection** – Tracks body landmarks and joint movements to analyze exercise form.

## How It Works

The application uses **MediaPipe Pose** to detect body landmarks from video frames. These landmarks are used to calculate joint angles and movement patterns.

The exercise recognition model uses **LSTM/BiLSTM** to identify the exercise based on a sequence of body movements.

For repetition counting, the application checks the movement between different positions, such as the **up and down phases** of an exercise.

## Technologies Used

* Python
* OpenCV
* MediaPipe
* TensorFlow / Keras
* LSTM / BiLSTM
* Streamlit
* NumPy
* Pandas

## Project Structure

```text
├── main.py
├── ExerciseAiTrainer.py
├── AiTrainer_utils.py
├── PoseModule2.py
├── chatbot.py
├── extract_features.py
├── create_sequence_of_features.py
├── train_bidirectionallstm.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/FitnessAI-Coach.git
cd FitnessAI-Coach
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run main.py
```

The application will open in your browser.

## Dataset

We used exercise videos and datasets to train and test the exercise recognition model.

The main dataset used for this project is the **Real-Time Exercise Recognition Dataset** available on Kaggle.

## Project Goal

The main goal of this project is to create a simple AI fitness assistant that can help users track their workouts without manually counting repetitions.

It combines **pose detection, exercise recognition, and repetition counting** into one application.

## Future Improvements

Some features that can be added in the future:

* More exercise types
* Better exercise form correction
* Personalized workout plans
* Nutrition recommendations
* Improved repetition accuracy
* More detailed workout tracking
* Mobile application

## Team Project

This project was developed as a **college project** to explore Computer Vision, Machine Learning, and AI applications in fitness.

⭐ If you find this project useful, feel free to give it a star!
