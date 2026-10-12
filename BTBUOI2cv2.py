import os
import urllib.request
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# Lấy chính xác đường dẫn thư mục chứa file code hiện tại
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tạo sẵn các thư mục con nếu chưa tồn tại
FACE_DIR = os.path.join(BASE_DIR, 'face')
BIEN_SO_DIR = os.path.join(BASE_DIR, 'bien_so')

os.makedirs(FACE_DIR, exist_ok=True)
os.makedirs(BIEN_SO_DIR, exist_ok=True)

# --- HÀM TỰ ĐỘNG TẢI FILE MÔ HÌNH NHẬN DIỆN KHUÔN MẶT CHO BÀI 3 ---
def get_face_cascade():
    xml_filename = os.path.join(BASE_DIR, 'haarcascade_frontalface_default.xml')
    if not os.path.exists(xml_filename):
        try:
            print("Đang tải bộ nhận diện khuôn mặt...")
            url = 'https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml'
            urllib.request.urlretrieve(url, xml_filename)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file nhận diện: {e}")
            return None
    return cv2.CascadeClassifier(xml_filename)

# --- BÀI 2: CHỌN FILE VIDEO VÀ XOAY 90 ĐỘ (A / D) ---
def run_video_rotation():
    video_path = filedialog.askopenfilename(
        title="Chọn File Video cho Bài 2",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv")]
    )
    if not video_path:
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không thể mở file video này!")
        return

    rotation_mode = 0  
    window_name = 'Bai 2: Xoay Video (Phim A / D)'

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Đã phát xong video.")
            break

        if rotation_mode == 'CW':
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotation_mode == 'CCW':
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        cv2.putText(frame, "Nhan 'A': Quay nguoc 90 do | Nhan 'D': Quay thuan 90 do | 'Q': Thoat", 
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break

        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
        except:
            break

        if key == ord('a') or key == ord('A'):
            rotation_mode = 'CCW'
        elif key == ord('d') or key == ord('D'):
            rotation_mode = 'CW'

    cap.release()
    cv2.destroyWindow(window_name)

# --- BÀI 3: NHẬN DIỆN KHUÔN MẶT TỪ VIDEO, ĐẾM VÀ LƯU VÀO THƯ MỤC FACE ---
def run_face_detection_video():
    video_path = filedialog.askopenfilename(
        title="Chọn File Video cho Bài 3 (Nhận diện khuôn mặt)",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv")]
    )
    if not video_path:
        return

    face_cascade = get_face_cascade()
    if face_cascade is None or face_cascade.empty():
        messagebox.showerror("Lỗi", "Không thể khởi tạo bộ nhận diện khuôn mặt!")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Lỗi", "Không thể mở file video này cho Bài 3!")
        return

    window_name = 'Bai 3: Nhan dien khuon mat tu Video'

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Đã phát xong video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        face_count = len(faces)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame, f"So khuon mat: {face_count}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Nhan 'S' de luu anh khuon mat | 'Q' de thoat", (20, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break

        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
        except:
            break

        if key == ord('s') or key == ord('S'):
            if face_count > 0:
                for idx, (x, y, w, h) in enumerate(faces):
                    face_img = frame[y:y+h, x:x+w]
                    # Lưu trực tiếp vào thư mục con 'face'
                    save_path = os.path.join(FACE_DIR, f"face_{idx}.png")
                    cv2.imwrite(save_path, face_img)
                print(f"Đã lưu thành công {face_count} khuôn mặt vào thư mục 'face'!")
            else:
                print("Không tìm thấy khuôn mặt nào trong khung hình để lưu!")

    cap.release()
    cv2.destroyWindow(window_name)

# --- BÀI 4: ĐẾM VÀ IN RA SỐ BÓNG TRONG HÌNH ---
def run_count_balloons():
    img_path = filedialog.askopenfilename(
        title="Chọn Ảnh Bóng Bay cho Bài 4",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not img_path:
        return

    img = cv2.imread(img_path)
    if img is None:
        messagebox.showerror("Lỗi", "Không thể đọc ảnh bóng bay!")
        return

    h, w, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    balloon_count = 0
    for c in contours:
        area = cv2.contourArea(c)
        x, y, bw, bh = cv2.boundingRect(c)
        
        if 400 < area < 80000:
            if y > h * 0.35 and x > 5 and (x + bw) < (w - 5) and (y + bh) < (h - 5):
                balloon_count += 1
                cv2.drawContours(img, [c], -1, (0, 255, 0), 2)

    cv2.putText(img, f"So bong: {balloon_count}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    print(f"Tổng số bóng đếm được: {balloon_count}")

    cv2.imshow("Bai 4: Dem So Bong Bay", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- BÀI 5: ĐỌC ẢNH BIỂN SỐ XE VÀ CROP KÝ TỰ LƯU VÀO THƯ MỤC BIEN_SO ---
def run_crop_license_plate():
    img_path = filedialog.askopenfilename(
        title="Chọn Ảnh Biển Số Xe cho Bài 5",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not img_path:
        return

    img = cv2.imread(img_path)
    if img is None:
        messagebox.showerror("Lỗi", "Không thể đọc ảnh biển số xe!")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_h, img_w = gray.shape
    valid_boxes = []

    for c in contours:
        bx, by, bw, bh = cv2.boundingRect(c)
        if bw > img_w * 0.95 or bh > img_h * 0.95:
            continue
        
        if bh > img_h * 0.3 and bh < img_h * 0.95 and bw > 5 and bw < img_w * 0.15:
            valid_boxes.append((bx, by, bw, bh))

    valid_boxes = sorted(valid_boxes, key=lambda b: b[0])

    saved_count = 0
    for idx, (bx, by, bw, bh) in enumerate(valid_boxes):
        char_img = img[by:by+bh, bx:bx+bw]
        # Lưu trực tiếp vào thư mục con 'bien_so'
        save_path = os.path.join(BIEN_SO_DIR, f"char_{idx}.png")
        cv2.imwrite(save_path, char_img)
        cv2.rectangle(img, (bx, by), (bx+bw, by+bh), (0, 0, 255), 2)
        saved_count += 1

    print(f"Đã cắt và lưu thành công {saved_count} ký tự biển số vào thư mục 'bien_so'!")
    cv2.imshow("Bai 5: Crop Chu So Bien So Xe", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --- GIAO DIỆN TKINTER TỔNG HỢP ---
root = tk.Tk()
root.title("Thực Hành OpenCV - Bài 2, 3, 4 & 5")
root.geometry("440x300")
root.resizable(False, False)

lbl_title = tk.Label(root, text="CHƯƠNG TRÌNH XỬ LÝ ẢNH & VIDEO", font=("Arial", 11, "bold"))
lbl_title.pack(pady=12)

btn_video = tk.Button(root, text="Bài 2: Chọn Video & Xoay 90 Độ (A / D)", font=("Arial", 10, "bold"), command=run_video_rotation, bg="#009688", fg="white", width=40)
btn_video.pack(pady=6)

btn_face = tk.Button(root, text="Bài 3: Nhận Diện Khuôn Mặt Từ Video (Phím S)", font=("Arial", 10, "bold"), command=run_face_detection_video, bg="#E91E63", fg="white", width=40)
btn_face.pack(pady=6)

btn_balloon = tk.Button(root, text="Bài 4: Đếm Số Bóng Bay Trong Hình", font=("Arial", 10, "bold"), command=run_count_balloons, bg="#3F51B5", fg="white", width=40)
btn_balloon.pack(pady=6)

btn_plate = tk.Button(root, text="Bài 5: Cắt Ký Tự Biển Số Xe Ra File Ảnh", font=("Arial", 10, "bold"), command=run_crop_license_plate, bg="#FF9800", fg="white", width=40)
btn_plate.pack(pady=6)

root.mainloop()