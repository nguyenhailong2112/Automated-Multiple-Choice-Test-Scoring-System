import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import support
from testform import questions, choices, answers

# Global variables

path = None
widthImg, heightImg = 480, 750


def load_image():
    global path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    img = cv2.imread(path)
    img = cv2.resize(img, (widthImg, heightImg))
    show_image(img, "Original Image")

def capture_from_camera():
    global path
    cap = cv2.VideoCapture(0)

    messagebox.showinfo("Camera", "Press 'Space' to capture the image and 'Esc' to cancel.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key
            break
        elif key == 32:  # Space key
            path = "camera_capture.jpg"
            cv2.imwrite(path, frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    if path:
        img = cv2.imread(path)
        img = cv2.resize(img, (widthImg, heightImg))
        show_image(img, "Captured Image")

def process_image():
    try:
        img = cv2.imread(path)
        img = cv2.resize(img, (widthImg, heightImg))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, 10, 50)

        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rectCon = support.rectContour(contours)

        if len(rectCon) < 2:
            messagebox.showerror("Error", "Could not detect the form or grading box.")
            return

        biggestContours = support.getCornerPoints(rectCon[0])
        gradePoints = support.getCornerPoints(rectCon[1])

        if biggestContours.size == 0 or gradePoints.size == 0:
            messagebox.showerror("Error", "Invalid contour detection.")
            return

        biggestContours = support.reorder(biggestContours)
        gradePoints = support.reorder(gradePoints)

        pt1 = np.float32(biggestContours)
        pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pt1, pt2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

        imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
        imgThresh = cv2.threshold(imgWarpGray, 150, 255, cv2.THRESH_BINARY_INV)[1]

        boxes = support.splitBoxes(imgThresh)

        myPixelVal = np.zeros((questions, choices))
        countC = 0
        countR = 0

        for image in boxes:
            totalPixels = cv2.countNonZero(image)
            myPixelVal[countR][countC] = totalPixels
            countC += 1
            if countC == choices:
                countR += 1
                countC = 0

        myIndex = [int(np.argmax(myPixelVal[x])) for x in range(questions)]

        grading = [1 if answers[x] == myIndex[x] else 0 for x in range(questions)]
        score = (sum(grading) / questions) * 10

        imgResult = support.showAnswers(imgWarpColored.copy(), myIndex, grading, answers, questions, choices)
        show_image(imgResult, f"Processed Image - Score: {score}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_image(img, title="Image"):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    top = tk.Toplevel()
    top.title(title)
    lbl = tk.Label(top, image=img)
    lbl.image = img
    lbl.pack()

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("PHẦN MỀM CHẤM THI TRẮC NGHIỆM")
root.geometry("1200x700")
root.configure(bg="#f0f0f0")

header_frame = tk.Frame(root, bg="#f0f0f0")
header_frame.pack(fill=tk.X, pady=10)

logo_img = Image.open("C:/Users/longn/PycharmProjects/BTL_CHAMTHITN/.venv/LogoUTC.jpg")
logo_img = logo_img.resize((200, 200), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(header_frame, image=logo_photo, bg="#f0f0f0")
logo_label.image = logo_photo
logo_label.pack(side=tk.LEFT, padx=10)

info_text = ("TRƯỜNG ĐẠI HỌC GIAO THÔNG VẬN TẢI\n\n"
             "KHOA ĐIỆN - ĐIỆN TỬ\n\n\n"
             "Họ và tên: Nguyễn Hải Long\n\n"
             "Mã sinh viên: 213330763\n\n"
             "Lớp chuyên ngành: Kỹ sư Kỹ thuật Robot và Trí tuệ Nhân tạo - K62\n\n"
             "Lớp học phần: Xử lý ảnh trong công nghiệp và giao thông (N02)")
info_label = tk.Label(header_frame, text=info_text, font=("Times New Roman", 13), bg="#f0f0f0", justify=tk.LEFT)
info_label.pack(side=tk.LEFT, padx=10)

title_label = tk.Label(root, text="\nBÁO CÁO BÀI TẬP LỚN\n_________________",
                       font=("Times New Roman", 28, "bold"), bg="#f0f0f0", fg="#333", justify=tk.CENTER)
title_label.pack(pady=20)
title_label = tk.Label(root, text="ĐỀ TÀI: ỨNG DỤNG CÔNG NGHỆ XỬ LÝ ẢNH ĐỂ CHẤM THI TRẮC NGHIỆM\n\nTHÔNG QUA PHIẾU TRẢ LỜI TRẮC NGHIỆM TỪ CAMERA\n",
                       font=("Times New Roman", 24, "bold"), bg="#f0f0f0", fg="#333", justify=tk.CENTER)
title_label.pack(pady=20)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=20)

btn_load = ttk.Button(frame_buttons, text="TẢI ẢNH", command=load_image)
btn_load.grid(row=0, column=0, padx=10, pady=5)

btn_camera = ttk.Button(frame_buttons, text="CAMERA", command=capture_from_camera)
btn_camera.grid(row=0, column=1, padx=10, pady=5)

btn_process = ttk.Button(frame_buttons, text="CHẤM BÀI", command=process_image)
btn_process.grid(row=0, column=2, padx=10, pady=5)

btn_exit = ttk.Button(frame_buttons, text="THOÁT", command=exit_app)
btn_exit.grid(row=0, column=3, padx=10, pady=5)

lbl_footer = tk.Label(root, text="Nguyễn Hải Long - 213330763", font=("Times New Roman", 10), bg="#f0f0f0", fg="#666")
lbl_footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()