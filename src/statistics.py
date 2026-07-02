"""
statistics.py - Module lưu thống kê quá trình giải N-Queens
"""
import time


class Statistics:
    def __init__(self):
        self.attempts = 0
        self.backtracks = 0
        self.solutions = 0
        self.start_time = None
        self.end_time = None

    def reset(self):
        self.attempts = 0
        self.backtracks = 0
        self.solutions = 0
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def add_attempt(self):
        self.attempts += 1

    def add_backtrack(self):
        self.backtracks += 1

    def add_solution(self):
        self.solutions += 1

    @property
    def runtime(self):
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.perf_counter()
        return end - self.start_time

    def runtime_str(self):
        return f"{self.runtime:.4f}s"

    def summary(self):
        return {
            'attempts': self.attempts,
            'backtracks': self.backtracks,
            'solutions': self.solutions,
            'runtime': self.runtime_str()
        }

    def __str__(self):
        return (
            f"Attempts:   {self.attempts}\n"
            f"Backtracks: {self.backtracks}\n"
            f"Solutions:  {self.solutions}\n"
            f"Time:       {self.runtime_str()}"
        )


def benchmark(n_values=None):
    """
    Chạy benchmark cho nhiều giá trị N.
    Đã sửa lỗi thời gian bằng cách đo đếm độc lập (Local Timer).
    """
    if n_values is None:
        n_values = [4, 6, 8, 10, 12]

    from solver import NQueensSolver
    results = []

    for n in n_values:
        stats = Statistics()
        solver = NQueensSolver(n, stats=stats)
        
        # 1. Bắt đầu đo thời gian ĐỘC LẬP bằng biến cục bộ
        t_start = time.perf_counter()
        
        # 2. Chạy thuật toán
        solutions = solver.solve()
        
        # 3. Kết thúc đo thời gian cục bộ
        t_end = time.perf_counter()
        elapsed_time = t_end - t_start
        
        # 4. Lưu kết quả
        results.append({
            'N': n,
            'solutions': len(solutions),
            'attempts': stats.attempts,
            'backtracks': stats.backtracks,
            # Format chuỗi thời gian dựa trên biến cục bộ, bỏ qua stats.runtime_str()
            'time': f"{elapsed_time:.4f}s" 
        })
        
    return results

