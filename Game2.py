import os
import sys
import random

class SudokuGame:
    def __init__(self):
        # Generate random Sudoku board
        self.board = self.generate_sudoku()
        
        # Store original board
        self.original_board = [row[:] for row in self.board]
        self.user_board = [row[:] for row in self.board]

    def generate_sudoku(self):
        """Generate a random valid Sudoku puzzle"""
        # Start with empty board
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the board with random valid numbers
        self.fill_board(board)
        
        # Store the completed board
        completed_board = [row[:] for row in board]
        
        # Remove numbers to create puzzle (remove about 50 numbers)
        cells_to_remove = 40
        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if board[row][col] != 0:
                board[row][col] = 0
                cells_to_remove -= 1
        
        return board

    def fill_board(self, board):
        """Fill board with random valid Sudoku numbers"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    # Get random numbers and shuffle them
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    
                    for num in numbers:
                        if self.is_safe(board, i, j, num):
                            board[i][j] = num
                            
                            # Recursively fill the rest
                            if self.fill_board(board):
                                return True
                            
                            # Backtrack if no solution found
                            board[i][j] = 0
                    
                    return False
        return True

    def is_safe(self, board, row, col, num):
        """Check if placing num at (row, col) is safe"""
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def display_board(self):
        self.clear_screen()
        print("\n" + "="*37)
        print("         PERMAINAN SUDOKU")
        print("="*37 + "\n")
        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 37)
            
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                
                num = self.user_board[i][j]
                if num == 0:
                    row_str += ". "
                else:
                    row_str += f"{num} "
            
            print(row_str)
        
        print("\n" + "="*37)

    def is_valid(self, row, col, num):
        # Check row
        if num in self.user_board[row]:
            return False, "Angka ini sudah ada di BARIS yang sama!"
        
        # Check column
        for i in range(9):
            if self.user_board[i][col] == num:
                return False, "Angka ini sudah ada di KOLOM yang sama!"
        
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.user_board[i][j] == num:
                    return False, "Angka ini sudah ada di KOTAK 3x3 yang sama!"
        
        return True, "Valid"

    def check_solution(self):
        # Check if all cells are filled
        for row in self.user_board:
            if 0 in row:
                return False, "Masih ada kotak kosong!"
        
        # Check if solution is valid
        for i in range(9):
            for j in range(9):
                num = self.user_board[i][j]
                self.user_board[i][j] = 0
                if not self.is_valid(i, j, num):
                    self.user_board[i][j] = num
                    return False, "Solusi tidak valid!"
                self.user_board[i][j] = num
        
        return True, "SELAMAT! Anda menang!"

    def play(self):
        while True:
            self.display_board()
            print("\nPerintah: (baris,kolom,angka) atau 'r' untuk reset atau 'c' untuk periksa atau 'q' untuk keluar")
            print("Contoh: 1,2,5 (untuk memasukkan 5 di baris 1, kolom 2)")
            
            user_input = input("\nMasukkan perintah: ").strip().lower()
            
            if user_input == 'q':
                print("\nTerima kasih telah bermain!")
                break
            
            if user_input == 'r':
                self.__init__()
                continue
            
            if user_input == 'c':
                valid, message = self.check_solution()
                print(f"\n{message}")
                if valid:
                    self.display_board()
                    input("Tekan Enter untuk keluar...")
                    break
                else:
                    input("Tekan Enter untuk melanjutkan...")
                continue
            
            # Parse input
            try:
                parts = user_input.split(',')
                if len(parts) != 3:
                    print("Format salah! Gunakan: baris,kolom,angka")
                    input("Tekan Enter untuk melanjutkan...")
                    continue
                
                row = int(parts[0].strip()) - 1  # Convert to 0-indexed
                col = int(parts[1].strip()) - 1
                num = int(parts[2].strip())
                
                # Validate input
                if not (0 <= row < 9 and 0 <= col < 9):
                    print("Baris dan kolom harus antara 1-9!")
                    input("Tekan Enter untuk melanjutkan...")
                    continue
                
                if num == 0:
                    # Hapus angka jika input 0
                    if self.original_board[row][col] == 0:
                        self.user_board[row][col] = 0
                        print("Angka dihapus!")
                    else:
                        print("Tidak bisa menghapus angka yang sudah ada!")
                    input("Tekan Enter untuk melanjutkan...")
                    continue
                
                if not (1 <= num <= 9):
                    print("Angka harus antara 1-9!")
                    input("Tekan Enter untuk melanjutkan...")
                    continue
                
                # Check if cell is locked
                if self.original_board[row][col] != 0:
                    print("Kotak ini sudah diisi dan tidak bisa diubah!")
                    input("Tekan Enter untuk melanjutkan...")
                    continue
                
                # Check validity
                is_valid, message = self.is_valid(row, col, num)
                if is_valid:
                    self.user_board[row][col] = num
                    print(f"Angka {num} dimasukkan di posisi ({row+1},{col+1})")
                else:
                    print(f"❌ {message}")
                
                input("Tekan Enter untuk melanjutkan...")
            
            except ValueError:
                print("Input tidak valid! Gunakan format: baris,kolom,angka")
                input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    game = SudokuGame()
    game.play()
