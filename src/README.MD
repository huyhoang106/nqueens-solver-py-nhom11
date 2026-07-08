solve(row):
  if row == N:
    → Lưu nghiệm
  for col in 0..N-1:
    if is_safe(row, col):
      board[row] = col
      solve(row + 1)
      board[row] = -1   ← Backtrack
