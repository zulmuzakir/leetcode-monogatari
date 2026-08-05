#include <iostream>
#include <unordered_set>
#include <vector>

using namespace std;

/**
 * Problem: Valid Sudoku
 * Category: Arrays & Hashing
 * Difficulty: Medium
 *
 * A board is valid if NO digit 1-9 repeats in any row, column, or 3x3 box.
 * Blank cells ('.') are ignored.
 *
 * Time Complexity:  O(81) = O(1)  (board is always 9x9)
 * Space Complexity: O(81) = O(1)
 */

class Solution {
public:
  bool isValidSudoku(vector<vector<char>> &board) {
    // 9 sets, one per row / column / box, tracking which digits we've seen.
    vector<unordered_set<char>> rows(9), cols(9), boxes(9);

    for (int r = 0; r < 9; ++r) {
      for (int c = 0; c < 9; ++c) {
        char v = board[r][c];
        if (v == '.')
          continue; // blanks don't participate in validation

        // Which of the 9 sub-boxes does (r, c) belong to?
        // row/3 -> band of rows (0..2), col/3 -> band of cols (0..2)
        int box = (r / 3) * 3 + (c / 3);

        // If this digit was already seen in its row, column, or box -> invalid.
        if (rows[r].count(v) || cols[c].count(v) || boxes[box].count(v))
          return false;

        // First time seeing it there -> remember it.
        rows[r].insert(v);
        cols[c].insert(v);
        boxes[box].insert(v);
      }
    }

    return true; // scanned everything, no repeats found
  }
};

int main() {
  Solution sol;

  // Test Case 1 — Example 1 (valid) -> expected true
  vector<vector<char>> board1 = {{'1', '2', '.', '.', '3', '.', '.', '.', '.'},
                                 {'4', '.', '.', '5', '.', '.', '.', '.', '.'},
                                 {'.', '9', '8', '.', '.', '.', '.', '.', '3'},
                                 {'5', '.', '.', '.', '6', '.', '.', '.', '4'},
                                 {'.', '.', '.', '8', '.', '3', '.', '.', '5'},
                                 {'7', '.', '.', '.', '2', '.', '.', '.', '6'},
                                 {'.', '.', '.', '.', '.', '.', '2', '.', '.'},
                                 {'.', '.', '.', '4', '1', '9', '.', '.', '8'},
                                 {'.', '.', '.', '.', '8', '.', '.', '7', '9'}};
  cout << "Test 1 (Expected: 1/true): " << (sol.isValidSudoku(board1) ? 1 : 0)
       << endl;

  // Test Case 2 — Example 2 (invalid: two 1s in top-left box) -> false
  vector<vector<char>> board2 = {{'1', '2', '.', '.', '3', '.', '.', '.', '.'},
                                 {'4', '.', '.', '5', '.', '.', '.', '.', '.'},
                                 {'.', '9', '1', '.', '.', '.', '.', '.', '3'},
                                 {'5', '.', '.', '.', '6', '.', '.', '.', '4'},
                                 {'.', '.', '.', '8', '.', '3', '.', '.', '5'},
                                 {'7', '.', '.', '.', '2', '.', '.', '.', '6'},
                                 {'.', '.', '.', '.', '.', '.', '2', '.', '.'},
                                 {'.', '.', '.', '4', '1', '9', '.', '.', '8'},
                                 {'.', '.', '.', '.', '8', '.', '.', '7', '9'}};
  cout << "Test 2 (Expected: 0/false): " << (sol.isValidSudoku(board2) ? 1 : 0)
       << endl;

  return 0;
}
