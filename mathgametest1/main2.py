import pygame
import os
import cv2
import mediapipe as mp
from game import Game
import global_variables

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)

overlayList = [None] * len(myList)  # Create a list with the same size as myList
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')

    resized_image = cv2.resize(image, (200, 200))
    number = int(''.join(filter(str.isdigit, imPath)))
    overlayList[number] = resized_image
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Math Games")
done = False
clock = pygame.time.Clock()
game = Game()

while not done:
    done = game.process_events()
    game.run_logic()
    game.check_result()
    game.display_frame(screen)
    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        success, image = cap.read()
        if success:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            fingerCount = 0
            global_variables.fingerCount = fingerCount

            if results.multi_hand_landmarks:

                for hand_landmarks in results.multi_hand_landmarks:
                    # Get hand index to check label (left or right)
                    handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                    handLabel = results.multi_handedness[handIndex].classification[0].label

                    handLandmarks = []

                    for landmarks in hand_landmarks.landmark:
                        handLandmarks.append([landmarks.x, landmarks.y])

                    if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                        fingerCount = fingerCount + 1
                    elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                        fingerCount = fingerCount + 1
                    if handLandmarks[8][1] < handLandmarks[6][1]:
                        fingerCount = fingerCount + 1
                    if handLandmarks[12][1] < handLandmarks[10][1]:
                        fingerCount = fingerCount + 1
                    if handLandmarks[16][1] < handLandmarks[14][1]:
                        fingerCount = fingerCount + 1
                    if handLandmarks[20][1] < handLandmarks[18][1]:
                        fingerCount = fingerCount + 1

                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    resized_image = cv2.resize(overlayList[fingerCount], (200, 200))

                    image[0:200, 0:200] = resized_image
            global_variables.fingerCount = fingerCount
            print(global_variables.fingerCount)

            # Display image
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    clock.tick(30)
cap.release()
pygame.quit()


