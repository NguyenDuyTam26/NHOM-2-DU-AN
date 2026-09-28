import sys
import subprocess
import os

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

exercises = {
    "1": ("Bài tập 1: Đọc và hiển thị ảnh bằng OpenCV và PIL", "bai1.py"),
    "2": ("Bài tập 2: Chuyển đổi hệ màu RGB sang Grayscale và HSV", "bai2.py"),
    "3": ("Bài tập 3: Áp dụng phép toán Bitwise AND trên 2 ảnh", "bai3.py"),
    "4": ("Bài tập 4: Lưu ảnh dưới các định dạng PNG, JPEG, BMP", "bai4.py"),
    "5": ("Bài tập 5: Tăng cường độ sáng cho ảnh với cv2.add()", "bai5.py"),
    "6": ("Bài tập 6: Phép biến đổi hình học (xoay, dịch chuyển, thu phóng)", "bai6.py"),
}

def main():
    python_exec = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exec):
        python_exec = sys.executable

    while True:
        print("\n" + "=" * 60)
        print("          BÀI TẬP THỊ GIÁC MÁY TÍNH (OPENCV)")
        print("=" * 60)
        for k, v in exercises.items():
            print(f"[{k}] {v[0]}")
        print("[0] Thoát")
        print("=" * 60)
        
        choice = input("Chọn bài tập muốn chạy (0-6): ").strip()
        if choice == "0":
            print("Tạm biệt!")
            break
        elif choice in exercises:
            script_name = exercises[choice][1]
            print(f"\n--- Đang thực thi {exercises[choice][0]} ({script_name}) ---")
            subprocess.run([python_exec, script_name])
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn lại.")

if __name__ == "__main__":
    main()
