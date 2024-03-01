
# Gesture Recognition Application

This Python application utilizes the MediaPipe library for real-time gesture recognition using facial landmarks. Users can interact with the application by nodding for "YES" responses and shaking for "NO" responses.

## Installation

### Dependencies

Ensure you have the following dependencies installed:
To install dependencies from the project directory, run:

```bash
pip install -r requirements.txt
```

### Running the Application

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install dependencies using the command mentioned above.
4. Run the application by executing the Python script:

```bash
python main.py
```

## How It Works

1. The application captures video frames from the webcam in real-time., you are asked a question and based on your head movement the rsponse is logged.
2. Each frame is processed using the MediaPipe Face Mesh model to detect facial landmarks.
3. Chosen facial landmarks, are tracked across frames and basesd on their movment and velocity of this points certain threshold are set to detect two main gestures.
4. Two primary gestures are recognized:
   - Nodding: Up and down movements of the head indicate a "YES" response.
   - Shaking: Side-to-side movements of the head indicate a "NO" response.
5. The sensitivity of gesture recognition is adjusted dynamically based on the distance of facial landmarks from the screen.
6. Users have a limited time to respond to each question, after which the application moves to the next question.
7. Only one retry is allowed for users to respond correctly. If the response is still invalid after one retry, it will be logged as invalid.


## User Interaction Guidelines

- Ensure that your face is well-lit and clearly visible to the webcam.
- Respond to questions by nodding (up and down) for "YES" and shaking (side-to-side) for "NO".
- Keep your head movements clear and distinct to improve recognition accuracy.
- Respond within the specified time limit for each question to avoid invalidation.
- If your response is invalid, you will be prompted to retry. Only one retry is allowed.


## Points about the algorithm:
The current gesture detection algorithm employs traditional computer vision techniques, leveraging landmark tracking across frames to discern nods based on their movement patterns and velocity. While effective, a more sophisticated approach, such as employing deep learning techniques, could enhance accuracy significantly. These methods might include LSTM-based models or 3D CNNs, as described in this [paper](https://link.springer.com/article/10.1007/s12555-022-0051-6) which excel at extracting spatiotemporal features, particularly recognizing optical flows and motion characteristics.

Despite the potential benefits of deep learning, the implementation in this code opts for a more traditional thresholding-based approach. This decision stems from the significant requirements for training deep learning models, including extensive datasets of high-quality samples, which were not readily available for this project.

In summary, while acknowledging the potential of advanced deep learning techniques, the current implementation prioritizes simplicity and accessibility, ensuring effective gesture recognition without the need for extensive training datasets.