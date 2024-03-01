import cv2
import time
import numpy as np
import mediapipe as mp
from operator import attrgetter
from config import *
from utils import *
import datetime


#clear log file if it exists
with open("log.txt", "w") as file:
    pass

# Function to handle responses
def log_response(response, question_index):
    print(f"Question: {questions[question_index]}")
    print(f"Response: {response}")
    current_time = datetime.datetime.now()
    print("Current Time:", current_time)
    with open("log.txt", "a") as file:
        print(f"Question: {questions[question_index]}, Response: {response}, Current Time: {datetime.datetime.now()}", file=file)


def main():
    
    resp = None
    #initialzation
    response_display_countdown = 0
    point1_movements = []
    point2_movements = []
    nose_movements = []
    vel1 = []
    vel2 = []
    question_index = 0
    #meidpaipe
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    cap = cv2.VideoCapture(0)
    count = 0


    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

        start_time = time.time()

        while cap.isOpened() and question_index < len(questions):
            success, image = cap.read()
            if not success:
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)

    
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())

    
                    point_1 = face_landmarks.landmark[199]
                    point_2 = face_landmarks.landmark[447]
                    # Used to adjust the sensitivity constants based on distance to screen.
                    head_top = face_landmarks.landmark[10]
                    head_bottom = face_landmarks.landmark[152]
                    nose = face_landmarks.landmark[1]
                    distance_adjustment = (head_bottom.y - head_top.y) / 0.5

           
                    point1_movements.append(point_1)
                    point2_movements.append(point_2)
                    nose_movements.append(nose)

                    if len(point1_movements) > FRAMES_TO_ANALYZE and len(point2_movements) > FRAMES_TO_ANALYZE:
                        point1_movements.pop(0)
                        point2_movements.pop(0)

                        time_taken = 1 / cap.get(cv2.CAP_PROP_FPS) 

                        nose_movements.pop(0)
                        nose_velocity = calculate_velocity(nose_movements[-2], nose_movements[-1], time_taken)

                        vel1.append(nose_velocity)

                        
                        if resp == None and (direction_changes(point1_movements, "z",
                                            NODDING_SENSITIVITY * distance_adjustment) > 0
                            and direction_changes(point2_movements, "z",
                                                SHAKING_SENSITIVITY * distance_adjustment) == 0
                            and abs(max(point1_movements, key=attrgetter('y')).y - min(point1_movements,
                                                                                        key=attrgetter(
                                                                                            'y')).y) <= VERTICAL_ADJUSTMENT * distance_adjustment) \
                            and MIN_NODDING_VELOCITY < nose_velocity < 2.3:
        
                            if resp == None:
                                resp = "YES"
                                log_response(resp, question_index)
                            
                            response_display_countdown = RESPONSE_DISPLAY_DURATION
                            point1_movements = []
                            point2_movements = []
                            nose_movements = []
                            vel1 = []

                 
                        elif resp == None and (direction_changes(point2_movements, "z",
                                                SHAKING_SENSITIVITY * distance_adjustment) > 0
                            and direction_changes(point1_movements, "z",
                                                    NODDING_SENSITIVITY * distance_adjustment) == 0
                            and abs(max(point2_movements, key=attrgetter('x')).x - min(point2_movements,
                                                                                            key=attrgetter(
                                                                                                'x')).x) <= HORIZONTAL_ADJUSTMENT * distance_adjustment):
        
                            if resp == None:
                                resp = "NO"
                                log_response(resp, question_index)
                            point1_movements = []
                            point2_movements = []
                            nose_movements = []
                            response_display_countdown = RESPONSE_DISPLAY_DURATION

            if response_display_countdown > 0 or time.time() - start_time < RESPONSE_DURATION:
                response_display_countdown -= 1
                cv2.putText(image, resp, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            

            # Display the question in the OpenCV window
            cv2.putText(image, questions[question_index], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Calculate the remaining time to answer the question
            remaining_time = RESPONSE_DURATION - (time.time() - start_time)
            text = f"Time remaining: {round(remaining_time)} seconds"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = image.shape[1] - text_size[0] - 50  
            text_y = 50 + text_size[1]  
            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow('MediaPipe Face Mesh', image)

            if time.time() - start_time >= RESPONSE_DURATION:

                # Move to the next question
                if resp == None:
                    if count>=1:
                        log_response("invalid", question_index)
                        count = 0
                        cv2.putText(image, "Response recorded as invalid", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        cv2.imshow('MediaPipe Face Mesh', image)
                        cv2.waitKey(2000)
                    else:
                        count+=1
                        cv2.putText(image, "Invalid response try again", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        cv2.imshow('MediaPipe Face Mesh', image)
                        cv2.waitKey(2000)
                        start_time = time.time()
                        continue
                    
                question_index += 1
                count=0
                start_time = time.time()
                resp = None

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break 


    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
