# N-Queens Solver

## Group Members

| Họ và tên | MSSV |
|------------|------------|
| Trịnh Đình Huy Hoàng (Leader) | 077206007861 |
| Đào Nguyễn Thiện Hiếu | 062206000126 |
| Trần Âu Đức | 077206002367 |
| Nguyễn Trần Đình Hiệu | 064206000109 |
| La Chí Hoàng | 089206004143 |
| Nguyễn Đặng Hoàng Danh | 082206014202 |

## Project Description

N-Queens Solver using Backtracking Algorithm.

## Features

- Solve N-Queens problem
- Visualization of queen placement
- Performance analysis
- Count number of solutions

## Technologies

- Python
- GitHub
- Visual Studio Code
## Flowchart
<img width="753" height="940" alt="image" src="https://github.com/user-attachments/assets/2b2abf59-3e92-4638-90b6-29ebf3e8388e" />
# ♛ N-Queens Solver

Ứng dụng minh họa thuật toán Backtracking giải bài toán N-Queens bằng Python + Tkinter.

## Cấu trúc dự án

```
NQueensSolver/
├── main.py        ← Entry point (chạy file này)
├── gui.py         ← Giao diện chính (Tkinter)
├── board.py       ← Vẽ bàn cờ bằng Canvas
├── solver.py      ← Thuật toán Backtracking
└── statistics.py  ← Thống kê attempts / backtracks / time
```

## Yêu cầu

- Python 3.8+
- Tkinter (có sẵn trong Python standard library)

## Cách chạy

```bash
cd NQueensSolver
python main.py
```

## Tính năng

| Tính năng | Mô tả |
|---|---|
| **Chọn N** | Nút nhanh 4/6/8/10/12 hoặc Spinbox tùy chỉnh 4-20 |
| **Solve Animation** | Hiển thị từng bước đặt hậu, có thể điều chỉnh tốc độ |
| **Step by Step** | Bấm Next để xem từng bước một |
| **Pause / Resume** | Tạm dừng và tiếp tục animation |
| **Highlight màu** | Xanh (đặt hậu), Đỏ (xung đột), Vàng (backtrack), Xanh dương (đang thử) |
| **Thống kê** | Attempts, Backtracks, Solutions, Time |
| **Benchmark** | So sánh N=4,6,8,10,12 một lúc |

## Màu sắc bàn cờ

| Màu | Ý nghĩa |
|---|---|
| 🟢 Xanh lá | Đặt hậu thành công |
| 🔴 Đỏ | Xung đột (tấn công nhau) |
| 🟠 Cam/Vàng | Backtrack |
| 🔵 Xanh dương | Đang thử ô này |
| 💚 Xanh sáng | Tìm được nghiệm |

## Thuật toán

```
solve(row):
  if row == N:
    → Lưu nghiệm
  for col in 0..N-1:
    if is_safe(row, col):
      board[row] = col
      solve(row + 1)
      board[row] = -1   ← Backtrack
```

