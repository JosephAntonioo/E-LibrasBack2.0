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
        # Carrega img no cv2
        image = cv2.flip(cv2.imread(img), 1)
        # Processa img para pegar os pontos
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # Se não encontrar pontos na mão return
        if not results.multi_hand_landmarks:
            return 'Nao foi possivel identificar a mao!'
        image_height, image_width, _ = image.shape
        # print(results.multi_hand_landmarks)
        # Salva os pontos em um array 
        pontos = []
        for hand_landmarks in results.multi_hand_landmarks:
            for a in hand_landmarks.landmark:
                pontos.append(a)
        if not results.multi_hand_world_landmarks:
            return 'Nao foi possivel identificar a mao!'
        # print(pontos[0])
        # print(pontos[5])
        return pontos
        
