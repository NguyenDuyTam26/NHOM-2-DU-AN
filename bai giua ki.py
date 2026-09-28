# ==============================================================================
# HỌC PHẦN: THỊ GIÁC MÁY TÍNH (COMPUTER VISION)
# BÀI KIỂM TRA GIỮA KỲ - TẤT CẢ ẢNH HIỂN THỊ TRONG CÙNG 1 CỬA SỔ
# ==============================================================================

import sys
import os

# Cấu hình in tiếng Việt trên console Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog


# --- Hàm tìm file mặc định dự phòng ---
def get_fallback_path(filename):
    candidates = [
        filename,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), filename),
        os.path.join("D:\\TGMT", filename),
        os.path.join("D:\\", filename)
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return filename


# --- Hộp thoại chọn ảnh từ máy tính ---
def choose_image_dialog(title="Chọn ảnh từ máy tính", default_filename="image1.jpg"):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Đưa hộp thoại lên trên cùng màn hình
    
    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=[
            ("Tệp hình ảnh", "*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff"),
            ("Tất cả tệp", "*.*")
        ]
    )
    root.destroy()

    if not file_path:
        fallback = get_fallback_path(default_filename)
        if os.path.exists(fallback):
            print(f"-> Chưa chọn ảnh, sử dụng ảnh mẫu: {fallback}")
            return fallback
        print("-> Đã hủy thao tác chọn ảnh.")
        return None
    
    print(f"-> Đã chọn: {file_path}")
    return file_path


# --- Hàm đọc ảnh hỗ trợ tiếng Việt có dấu (Unicode) ---
def read_image_safe(path):
    if not path or not os.path.exists(path):
        return None
    try:
        data = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Lỗi khi đọc file ảnh {path}: {e}")
        return None


# ==============================================================================
# HÀM HIỂN THỊ TẤT CẢ CÁC ẢNH TRONG CÙNG 1 CỬA SỔ DUY NHẤT
# ==============================================================================
def prepare_image_card(img, title, target_w=340, target_h=260):
    """
    Chuẩn hóa ảnh về 3 kênh màu, resize về kích thước chuẩn và thêm tiêu đề phía trên.
    """
    if img is None:
        return None
    # Nếu là ảnh 1 kênh (grayscale), chuyển sang 3 kênh BGR để ghép cùng ảnh màu
    if len(img.shape) == 2:
        img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    else:
        img_bgr = img.copy()

    # Resize về kích thước chuẩn của card
    resized = cv2.resize(img_bgr, (target_w, target_h), interpolation=cv2.INTER_AREA)

    # Tạo thanh tiêu đề màu xám đậm (cao 36px)
    banner_h = 36
    banner = np.zeros((banner_h, target_w, 3), dtype=np.uint8)
    banner[:] = (45, 45, 45)

    # Viết tên tiêu đề lên thanh
    cv2.putText(
        banner, 
        title, 
        (10, 24), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.55, 
        (255, 255, 255), 
        1, 
        cv2.LINE_AA
    )

    # Thêm đường viền mỏng quanh ảnh
    cv2.rectangle(resized, (0, 0), (target_w - 1, target_h - 1), (80, 80, 80), 1)

    # Ghép tiêu đề và ảnh lại theo chiều dọc
    return np.vstack([banner, resized])


def show_in_single_window(window_title, items, max_cols=3):
    """
    Ghép các ảnh thành lưới và hiển thị trong DUY NHẤT 1 CỬA SỔ.
    items: danh sách các cặp (title, img)
    """
    cards = []
    for title, img in items:
        if img is not None:
            card = prepare_image_card(img, title)
            cards.append(card)

    if not cards:
        print("Không có ảnh để hiển thị!")
        return

    # Sắp xếp các card thành dạng lưới (rows x cols)
    rows = []
    for i in range(0, len(cards), max_cols):
        row_cards = cards[i : i + max_cols]
        # Nếu hàng cuối không đủ cột, bù bằng khung đen
        while len(row_cards) < min(len(cards), max_cols):
            placeholder = np.zeros_like(cards[0])
            placeholder[:] = (30, 30, 30)
            row_cards.append(placeholder)
        rows.append(np.hstack(row_cards))

    final_canvas = np.vstack(rows) if len(rows) > 1 else rows[0]

    # Hiển thị trên 1 cửa sổ duy nhất
    cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(window_title, final_canvas)
    print(f"\n[OK] Đang hiển thị kết quả trong CÙNG 1 CỬA SỔ: '{window_title}'")
    print("-> Nhấn phím bất kỳ trên cửa sổ ảnh để đóng...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ==============================================================================
# BÀI TẬP 1: Đọc và hiển thị ảnh bằng OpenCV và PIL (Cùng 1 cửa sổ)
# ==============================================================================
def bai_tap_1():
    print("\n" + "=" * 60)
    print("BÀI TẬP 1: Đọc và hiển thị ảnh bằng OpenCV và PIL")
    print("=" * 60)
    
    path = choose_image_dialog(title="Bài 1: Chọn ảnh để đọc và hiển thị", default_filename="image1.jpg")
    if not path:
        return

    # 1. Đọc bằng OpenCV (BGR)
    img_cv = read_image_safe(path)
    if img_cv is None:
        print("Không thể đọc ảnh bằng OpenCV!")
        return

    # 2. Đọc và hiển thị bằng Pillow (PIL)
    try:
        pil_img = Image.open(path)
        # Phương pháp 2 của Pillow: Hiển thị qua trình xem ảnh của hệ thống
        print("-> Đang mở ảnh bằng phương pháp hiển thị riêng của Pillow (pil_img.show())...")
        pil_img.show(title="Bai 1 - Pillow Native Viewer")
        
        # Chuyển ảnh Pillow RGB sang mảng NumPy BGR để hiển thị so sánh trong cùng cửa sổ OpenCV
        img_pil_rgb = np.array(pil_img)
        if len(img_pil_rgb.shape) == 3 and img_pil_rgb.shape[2] >= 3:
            img_pil_bgr = cv2.cvtColor(img_pil_rgb[:, :, :3], cv2.COLOR_RGB2BGR)
        else:
            img_pil_bgr = img_pil_rgb
    except Exception as e:
        print(f"Lỗi khi đọc qua Pillow: {e}")
        img_pil_bgr = img_cv

    # Hiển thị cả 2 trong CÙNG 1 CỬA SỔ
    show_in_single_window(
        "Bai 1 - So sanh OpenCV va Pillow (Chung 1 cua so)", 
        [
            ("1. Doc bang OpenCV (cv2.imread)", img_cv),
            ("2. Doc bang Pillow (Image.open)", img_pil_bgr)
        ],
        max_cols=2
    )
    print("Hoàn thành Bài tập 1!")


# ==============================================================================
# BÀI TẬP 2: Chuyển đổi RGB sang Grayscale và HSV (Cùng 1 cửa sổ)
# ==============================================================================
def bai_tap_2():
    print("\n" + "=" * 60)
    print("BÀI TẬP 2: Chuyển đổi ảnh sang Grayscale và HSV")
    print("=" * 60)
    
    path = choose_image_dialog(title="Bài 2: Chọn ảnh màu để chuyển đổi hệ màu", default_filename="image1.jpg")
    if not path:
        return

    img_bgr = read_image_safe(path)
    if img_bgr is None:
        print("Không thể đọc ảnh!")
        return

    # Chuyển đổi hệ màu
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Hiển thị CẢ 3 HỆ MÀU TRONG CÙNG 1 CỬA SỔ
    show_in_single_window(
        "Bai 2 - He mau: Goc, Grayscale va HSV (Chung 1 cua so)",
        [
            ("1. Anh goc (BGR)", img_bgr),
            ("2. Grayscale (Muc xam)", img_gray),
            ("3. He mau HSV", img_hsv)
        ],
        max_cols=3
    )
    print("Hoàn thành Bài tập 2!")


# ==============================================================================
# BÀI TẬP 3: Áp dụng phép toán Bitwise AND (Cùng 1 cửa sổ)
# ==============================================================================
def bai_tap_3():
    print("\n" + "=" * 60)
    print("BÀI TẬP 3: Áp dụng phép toán Bitwise AND trên 2 ảnh")
    print("=" * 60)
    
    print("Bước 1: Chọn ảnh thứ nhất...")
    path1 = choose_image_dialog(title="Bài 3 - Bước 1: Chọn ảnh thứ nhất", default_filename="image1.jpg")
    if not path1:
        return

    print("Bước 2: Chọn ảnh thứ hai...")
    path2 = choose_image_dialog(title="Bài 3 - Bước 2: Chọn ảnh thứ hai", default_filename="image2.jpg")
    if not path2:
        return

    img1 = read_image_safe(path1)
    img2 = read_image_safe(path2)

    if img1 is None or img2 is None:
        print("Không thể đọc đủ 2 ảnh đầu vào!")
        return

    # Đồng bộ kích thước 2 ảnh
    if img1.shape != img2.shape:
        print(f"Đang đồng bộ kích thước ảnh 2 {img2.shape[:2]} về cùng kích thước ảnh 1 {img1.shape[:2]}...")
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Áp dụng phép toán logic AND từng bit
    bitwise_res = cv2.bitwise_and(img1, img2)

    # Hiển thị CẢ 3 ẢNH TRONG CÙNG 1 CỬA SỔ
    show_in_single_window(
        "Bai 3 - Phep toan Bitwise AND (Chung 1 cua so)",
        [
            ("1. Anh 1 (Image 1)", img1),
            ("2. Anh 2 (Image 2)", img2),
            ("3. Ket qua Bitwise AND", bitwise_res)
        ],
        max_cols=3
    )
    print("Hoàn thành Bài tập 3!")


# ==============================================================================
# BÀI TẬP 4: Lưu ảnh dưới nhiều định dạng (Cùng 1 cửa sổ)
# ==============================================================================
def bai_tap_4():
    print("\n" + "=" * 60)
    print("BÀI TẬP 4: Lưu ảnh dưới nhiều định dạng PNG, JPEG, BMP")
    print("=" * 60)
    
    path = choose_image_dialog(title="Bài 4: Chọn ảnh để lưu sang các định dạng khác", default_filename="image1.jpg")
    if not path:
        return

    img = read_image_safe(path)
    if img is None:
        print("Không thể đọc ảnh!")
        return

    target_dir = os.path.dirname(path) if os.path.dirname(path) else "."
    out_png = os.path.join(target_dir, "output_image.png")
    out_jpg = os.path.join(target_dir, "output_image.jpg")
    out_bmp = os.path.join(target_dir, "output_image.bmp")

    cv2.imwrite(out_png, img)
    cv2.imwrite(out_jpg, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
    cv2.imwrite(out_bmp, img)

    size_png = os.path.getsize(out_png) / 1024 if os.path.exists(out_png) else 0
    size_jpg = os.path.getsize(out_jpg) / 1024 if os.path.exists(out_jpg) else 0
    size_bmp = os.path.getsize(out_bmp) / 1024 if os.path.exists(out_bmp) else 0

    print(f"1. Lưu PNG  ({out_png}): Thành công ({size_png:.1f} KB)")
    print(f"2. Lưu JPEG ({out_jpg}): Thành công ({size_jpg:.1f} KB)")
    print(f"3. Lưu BMP  ({out_bmp}): Thành công ({size_bmp:.1f} KB)")

    # Đọc lại các file đã lưu để hiển thị so sánh trong CÙNG 1 CỬA SỔ (lưới 2x2)
    read_png = read_image_safe(out_png)
    read_jpg = read_image_safe(out_jpg)
    read_bmp = read_image_safe(out_bmp)

    show_in_single_window(
        "Bai 4 - Cac dinh dang luu anh (Chung 1 cua so)",
        [
            ("1. Anh goc", img),
            (f"2. Dinh dang PNG ({size_png:.1f} KB)", read_png),
            (f"3. Dinh dang JPEG ({size_jpg:.1f} KB)", read_jpg),
            (f"4. Dinh dang BMP ({size_bmp:.1f} KB)", read_bmp)
        ],
        max_cols=2
    )
    print("Hoàn thành Bài tập 4!")


# ==============================================================================
# BÀI TẬP 5: Tăng cường độ sáng cho ảnh (Cùng 1 cửa sổ)
# ==============================================================================
def bai_tap_5():
    print("\n" + "=" * 60)
    print("BÀI TẬP 5: Tăng cường độ sáng cho ảnh với cv2.add()")
    print("=" * 60)
    
    path = choose_image_dialog(title="Bài 5: Chọn ảnh để tăng cường độ sáng", default_filename="image1.jpg")
    if not path:
        return

    img = read_image_safe(path)
    if img is None:
        print("Không thể đọc ảnh!")
        return

    # Tăng độ sáng với cv2.add() (tự động bão hòa ở 255)
    brightness_val = 50
    matrix = np.full(img.shape, brightness_val, dtype=np.uint8)
    bright_img = cv2.add(img, matrix)

    target_dir = os.path.dirname(path) if os.path.dirname(path) else "."
    out_file = os.path.join(target_dir, "output_bright.jpg")
    cv2.imwrite(out_file, bright_img)
    print(f"-> Đã lưu ảnh tăng sáng vào: {out_file}")

    # Hiển thị CẢ 2 ẢNH CẠNH NHAU TRONG CÙNG 1 CỬA SỔ
    show_in_single_window(
        "Bai 5 - So sanh anh goc va tang do sang (Chung 1 cua so)",
        [
            ("1. Anh goc", img),
            (f"2. Anh tang sang (+{brightness_val})", bright_img)
        ],
        max_cols=2
    )
    print("Hoàn thành Bài tập 5!")


# ==============================================================================
# BÀI TẬP 6: Phép biến đổi hình học (Cùng 1 cửa sổ)
# ==============================================================================
def bai_tap_6():
    print("\n" + "=" * 60)
    print("BÀI TẬP 6: Các phép biến đổi hình học")
    print("=" * 60)
    
    path = choose_image_dialog(title="Bài 6: Chọn ảnh để áp dụng biến đổi hình học", default_filename="image1.jpg")
    if not path:
        return

    img = read_image_safe(path)
    if img is None:
        print("Không thể đọc ảnh!")
        return

    h, w = img.shape[:2]

    # 1. Xoay ảnh 90 độ theo chiều kim đồng hồ
    rotated_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # 2. Dịch chuyển sang phải 50 pixel (tx=50, ty=0)
    M = np.float32([[1, 0, 50], [0, 1, 0]])
    shifted = cv2.warpAffine(img, M, (w, h))

    # 3. Thu phóng ảnh 1.5 lần
    resized_1_5x = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    target_dir = os.path.dirname(path) if os.path.dirname(path) else "."
    cv2.imwrite(os.path.join(target_dir, "output_rotated.jpg"), rotated_90)
    cv2.imwrite(os.path.join(target_dir, "output_shifted.jpg"), shifted)
    cv2.imwrite(os.path.join(target_dir, "output_resized.jpg"), resized_1_5x)

    # Hiển thị CẢ 4 ẢNH TRONG CÙNG 1 CỬA SỔ (lưới 2x2)
    show_in_single_window(
        "Bai 6 - Cac phep bien doi hinh hoc (Chung 1 cua so)",
        [
            ("1. Anh goc", img),
            ("2. Xoay 90 do", rotated_90),
            ("3. Dich phai 50px", shifted),
            ("4. Thu phong 1.5x", resized_1_5x)
        ],
        max_cols=2
    )
    print("Hoàn thành Bài tập 6!")


# ==============================================================================
# GIAO DIỆN CỬA SỔ ĐỒ HỌA (GUI) CÓ NÚT BẤM TRỰC QUAN
# ==============================================================================
def mo_giao_dien_gui():
    gui = tk.Tk()
    gui.title("Chương Trình Thị Giác Máy Tính - Bài Giữa Kỳ")
    gui.geometry("520x540")
    gui.resizable(False, False)

    title_label = tk.Label(
        gui, 
        text="BÀI TẬP THỊ GIÁC MÁY TÍNH (OPENCV)", 
        font=("Arial", 14, "bold"),
        fg="#1a73e8"
    )
    title_label.pack(pady=15)

    sub_label = tk.Label(
        gui, 
        text="Bấm vào nút bài tập bên dưới để chọn ảnh và xem kết quả chung 1 cửa sổ:", 
        font=("Arial", 10)
    )
    sub_label.pack(pady=5)

    btn_frame = tk.Frame(gui)
    btn_frame.pack(pady=10, padx=20, fill="both", expand=True)

    buttons = [
        ("Bài 1: Đọc & Hiển thị ảnh (OpenCV + PIL)", bai_tap_1, "#e8f0fe"),
        ("Bài 2: Chuyển đổi RGB sang Grayscale và HSV", bai_tap_2, "#e8f0fe"),
        ("Bài 3: Áp dụng phép toán Bitwise AND (2 ảnh)", bai_tap_3, "#e8f0fe"),
        ("Bài 4: Lưu ảnh dưới định dạng PNG, JPEG, BMP", bai_tap_4, "#e8f0fe"),
        ("Bài 5: Tăng cường độ sáng cho ảnh (cv2.add)", bai_tap_5, "#e8f0fe"),
        ("Bài 6: Biến đổi hình học (Xoay, Dịch, Phóng)", bai_tap_6, "#e8f0fe"),
    ]

    for text, cmd, bg_color in buttons:
        btn = tk.Button(
            btn_frame, 
            text=text, 
            command=cmd, 
            font=("Arial", 11),
            bg=bg_color,
            fg="#202124",
            relief="groove",
            height=2,
            anchor="w",
            padx=15
        )
        btn.pack(fill="x", pady=4)

    exit_btn = tk.Button(
        gui, 
        text="Thoát chương trình", 
        command=gui.destroy, 
        font=("Arial", 10, "bold"),
        bg="#fce8e6",
        fg="#c5221f",
        height=1
    )
    exit_btn.pack(pady=12, fill="x", padx=20)

    gui.mainloop()


# ==============================================================================
# MENU DÒNG LỆNH CHÍNH
# ==============================================================================
if __name__ == "__main__":
    menu = """
============================================================
      BÀI TẬP THỊ GIÁC MÁY TÍNH - BÀI GIỮA KỲ
       (TẤT CẢ KẾT QUẢ HIỂN THỊ CHUNG 1 CỬA SỔ)
============================================================
[1] Bài tập 1: Đọc & hiển thị ảnh bằng OpenCV và PIL
[2] Bài tập 2: Chuyển đổi RGB sang Grayscale và HSV
[3] Bài tập 3: Áp dụng phép toán Bitwise AND (Chọn 2 ảnh)
[4] Bài tập 4: Lưu ảnh dưới định dạng PNG, JPEG, BMP
[5] Bài tập 5: Tăng cường độ sáng cho ảnh với cv2.add()
[6] Bài tập 6: Biến đổi hình học (xoay 90°, dịch 50px, phóng 1.5x)
[7] Chạy lần lượt TẤT CẢ các bài tập (1 -> 6)
[8] MỞ GIAO DIỆN CỬA SỔ CÓ CÁC NÚT BẤM (GUI APP)
[0] Thoát
============================================================
"""
    while True:
        print(menu)
        choice = input("Nhập số bài tập bạn muốn chạy (0-8): ").strip()
        if choice == "1":
            bai_tap_1()
        elif choice == "2":
            bai_tap_2()
        elif choice == "3":
            bai_tap_3()
        elif choice == "4":
            bai_tap_4()
        elif choice == "5":
            bai_tap_5()
        elif choice == "6":
            bai_tap_6()
        elif choice == "7":
            bai_tap_1()
            bai_tap_2()
            bai_tap_3()
            bai_tap_4()
            bai_tap_5()
            bai_tap_6()
        elif choice == "8":
            mo_giao_dien_gui()
        elif choice == "0":
            print("Đã thoát chương trình!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 0 đến 8.")
