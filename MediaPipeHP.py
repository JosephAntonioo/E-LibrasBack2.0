import mediapipe

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
async def handPoseM(img):
    print(img)
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
        image = cv2.flip(cv2.imread(img), 1)
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        # print('Handedness:', results.multi_handedness)
        if not results.multi_hand_landmarks:
            return ''
        image_height, image_width, _ = image.shape
        pontos = []
        annotated_image = image.copy()
        # print(results.multi_hand_landmarks)
        for hand_landmarks in results.multi_hand_landmarks:
            # print('hand_landmarks:', hand_landmarks)
            # print(
            #     f'Index finger tip coordinates: (',
            #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
            #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
            # )
            for a in hand_landmarks.landmark:
                pontos.append(a)
        if not results.multi_hand_world_landmarks:
            return ''
        # print(pontos[0])
        # print(pontos[5])
        return pontos
        
