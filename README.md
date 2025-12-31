# Automated-Multiple-Choice-Test-Scoring-System

Automated Multiple-Choice Test Scoring System with OpenCV

## FORM PHIẾU TRẮC NGHIỆM

<img width="1683" height="735" alt="image" src="https://github.com/user-attachments/assets/c1d7de04-e9a9-471c-b73c-6354389e23d0" />

## QUY TRÌNH XỬ LÝ

### Bước 1: Tiền xử lý ảnh

Ảnh gốc → Chuyển ảnh xám → Làm mờ Gauss → Phát hiện biên Canny

### Bước 2: Phát hiện form

Tìm contours trong ảnh

Lọc các hình chữ nhật (4 đỉnh)

Xác định form chính (bài thi) và form điểm

### Bước 3: Chỉnh sửa phối cảnh

Áp dụng perspective transform

Căn chỉnh form về góc nhìn thẳng đứng

Chuẩn hóa kích thước 480×750 pixel

### Bước 4: Phân tích ô trả lời

Form đã chỉnh → Chia thành 10×4 ô → Phân tích pixel mỗi ô → Xác định ô được tô (nhiều pixel đen nhất)

### Bước 5: Chấm điểm

So sánh với đáp án mẫu

Tính điểm: (số câu đúng/10)×10

Hiển thị kết quả trực quan

## Thuật toán chính

Contour Detection: Phát hiện đường viền form

Perspective Transform: Chỉnh sửa góc nghiêng

Pixel Counting: Đếm pixel đen để xác định ô tô

Thresholding: Phân ngưỡng nhị phân để tách đối tượng

## KẾT QUẢ

<img width="940" height="500" alt="image" src="https://github.com/user-attachments/assets/2baec06b-3452-4c2b-a908-963bb8d0ebd1" />

<img width="940" height="498" alt="image" src="https://github.com/user-attachments/assets/c106a2b8-44af-46a1-859f-f37b946cea46" />

## HẠN CHẾ - SAI SÓT

<img width="940" height="480" alt="image" src="https://github.com/user-attachments/assets/edccb188-f117-4446-a10b-60976b3550a3" />

<img width="940" height="481" alt="image" src="https://github.com/user-attachments/assets/ce260993-1c39-4c82-8c75-ad9ee3b56c2b" />
