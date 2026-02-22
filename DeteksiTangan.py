import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

# Koneksi antar landmark untuk menggambar tangan
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),  # Jempol
    (0, 5), (5, 6), (6, 7), (7, 8),  # Telunjuk
    (0, 17), (5, 9), (9, 10), (10, 11), (11, 12),  # Jari tengah
    (9, 13), (13, 14), (14, 15), (15, 16),  # Jari manis
    (13, 17), (17, 18), (18, 19), (19, 20),  # Kelingking
]

# Setup untuk drawing
MARGIN = 10  # pixels
FONT_SIZE = 2  # Lebih besar biar jelas
FONT_THICKNESS = 2  # Lebih tebal
HANDEDNESS_TEXT_COLOR = (255, 255, 0)  # Cyan terang (lebih keliatan)
LANDMARK_COLOR = (0, 255, 0)  # hijau untuk titik
CONNECTION_COLOR = (255, 0, 0)  # biru untuk garis
GESTURE_TEXT_COLOR = (0, 255, 255)  # Yellow untuk gesture

def detect_gesture(hand_landmarks):
    """Deteksi gesture tangan berdasarkan posisi jari"""
    
    # ID landmark untuk ujung jari
    # 4: Jempol, 8: Telunjuk, 12: Tengah, 16: Manis, 20: Kelingking
    thumb_tip = hand_landmarks[4]
    index_tip = hand_landmarks[8]
    middle_tip = hand_landmarks[12]
    ring_tip = hand_landmarks[16]
    pinky_tip = hand_landmarks[20]
    
    # ID landmark untuk pangkal jari (MCP - Metacarpophalangeal)
    thumb_mcp = hand_landmarks[2]
    index_mcp = hand_landmarks[5]
    middle_mcp = hand_landmarks[9]
    ring_mcp = hand_landmarks[13]
    pinky_mcp = hand_landmarks[17]
    
    # Hitung jari yang terangkat (ujung jari lebih tinggi dari pangkal)
    fingers_up = []
    
    # Jempol (cek horizontal karena jempol ke samping)
    if thumb_tip.x < thumb_mcp.x:  # Jempol kiri
        fingers_up.append(1)
    else:
        fingers_up.append(0)
    
    # Jari lainnya (cek vertikal - y lebih kecil = lebih atas)
    if index_tip.y < index_mcp.y:
        fingers_up.append(1)
    else:
        fingers_up.append(0)
        
    if middle_tip.y < middle_mcp.y:
        fingers_up.append(1)
    else:
        fingers_up.append(0)
        
    if ring_tip.y < ring_mcp.y:
        fingers_up.append(1)
    else:
        fingers_up.append(0)
        
    if pinky_tip.y < pinky_mcp.y:
        fingers_up.append(1)
    else:
        fingers_up.append(0)
    
    total_fingers = sum(fingers_up)
    
    # Deteksi gesture berdasarkan jari yang terangkat
    if total_fingers == 0:
        return "KEPALAN! ✊"
    elif total_fingers == 5:
        return "TERBUKA! ✋"
    elif total_fingers == 1 and fingers_up[1] == 1:
        return "NUNJUK! 👆"
    elif total_fingers == 1 and fingers_up[0] == 1:
        return "JEMPOL! 👍"
    elif total_fingers == 2 and fingers_up[1] == 1 and fingers_up[2] == 1:
        return "PEACE! ✌️"
    elif total_fingers == 3:
        return f"3 JARI!"
    elif total_fingers == 4:
        return f"4 JARI!"
    else:
        return f"{total_fingers} JARI"


def draw_landmarks_on_image(rgb_image, detection_result):
    """Gambar landmarks tangan di image"""
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)
    height, width, _ = annotated_image.shape

    # Loop semua tangan yang kedeteksi
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Gambar koneksi antar landmark (garis)
        for connection in HAND_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            
            start_point = hand_landmarks[start_idx]
            end_point = hand_landmarks[end_idx]
            
            start_x = int(start_point.x * width)
            start_y = int(start_point.y * height)
            end_x = int(end_point.x * width)
            end_y = int(end_point.y * height)
            
            cv2.line(annotated_image, (start_x, start_y), (end_x, end_y), 
                    CONNECTION_COLOR, 2)

        # Gambar landmark (titik-titik)
        for landmark in hand_landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(annotated_image, (x, y), 5, LANDMARK_COLOR, -1)

        # Ambil koordinat untuk teks
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # ============================================
        # UBAH TEKS DI SINI!
        # ============================================
        # Cara 1: Bahasa Indonesia KEBALIK (Kanan jadi Kiri, Kiri jadi Kanan)
        text = "Kiri" if handedness[0].category_name == "Right" else "Kanan"
        
        # Cara 2: Pakai Emoji
        # text = "👉" if handedness[0].category_name == "Right" else "👈"
        
        # Cara 3: Bahasa Inggris (English)
        # text = handedness[0].category_name  # Langsung pakai "Right" atau "Left"
        
        # Cara 4: Custom text apapun
        # text = "Tangan Kanan" if handedness[0].category_name == "Right" else "Tangan Kiri"
        # text = "R" if handedness[0].category_name == "Right" else "L"
        # ============================================
        
        # Tulis teks dengan font yang lebih jelas
        cv2.putText(annotated_image, text,
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
        
        # --- DETEKSI GESTURE ---
        gesture = detect_gesture(hand_landmarks)
        
        # Tampilkan gesture di bawah teks tangan
        cv2.putText(annotated_image, gesture,
                    (text_x, text_y + 40), cv2.FONT_HERSHEY_DUPLEX,
                    FONT_SIZE - 0.5, GESTURE_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
        
        # --- LOGIKA SENSOR ---
        # Ambil koordinat ujung telunjuk (Index Finger Tip = id 8)
        telunjuk = hand_landmarks[8]
        print(f"Telunjuk {text} ada di: X={telunjuk.x:.2f}, Y={telunjuk.y:.2f} | Gesture: {gesture}")

    return annotated_image

# Setup opsi HandLandmarker
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,  # Deteksi maksimal 2 tangan
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5)

# Setup Webcam
cap = cv2.VideoCapture(0)
print("Kamera lagi dibuka, tunggu bentar...")

timestamp = 0  # Timestamp untuk video mode (dalam ms)

with vision.HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Waduh, frame kamera kosong/nggak kebaca.")
            continue

        # Flip dulu sebelum processing biar kayak cermin
        image = cv2.flip(image, 1)
        
        # Convert BGR to RGB (MediaPipe butuh RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Buat MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        # Deteksi tangan
        detection_result = landmarker.detect_for_video(mp_image, timestamp)
        timestamp += 1  # Increment timestamp

        # Gambar hasil deteksi
        annotated_image = draw_landmarks_on_image(rgb_image, detection_result)
        
        # Convert kembali ke BGR untuk ditampilkan OpenCV
        bgr_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        
        # Tampilkan langsung (sudah di-flip dari awal, jadi teks benar)
        cv2.imshow('Project Andre - Deteksi Tangan', bgr_image)

        # Tekan ESC atau 'q' buat keluar
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()