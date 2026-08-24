#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>

using namespace std;

// ============================================================================
//  INTERACTIVE VISUAL LEARNER: Valid Sudoku, one step at a time.
//
//  Run:  ./run neetcode250/01_arrays_hashing/0036_valid_sudoku/visual.cpp
//
//  YOU control the pace: press Enter to step to the next cell.
//  Type 'q' + Enter to quit. This board (Example 2) is INVALID and the
//  learner will FLASH RED on the duplicate inside box 0. Type 'r'+Enter to
//  jump straight to that moment.
// ============================================================================

const string RED = "\033[31m";
const string GREEN = "\033[32m";
const string YELLOW = "\033[33m";
const string MAGENTA = "\033[35m";
const string CYAN = "\033[36m";
const string BOLD = "\033[1m";
const string RESET = "\033[0m";

int boxOf(int r, int c) { return (r / 3) * 3 + (c / 3); }

string glyph(const vector<vector<char>> &b, int r, int c, int curR, int curC) {
  bool inRow = (r == curR);
  bool inCol = (c == curC);
  bool inBox = (boxOf(r, c) == boxOf(curR, curC));
  char ch = b[r][c];

  if (r == curR && c == curC)
    return BOLD + CYAN + "[" + string(1, ch) + "]" + RESET;
  if (ch == '.')
    return " . ";

  string col = RESET;
  if (inBox == false && inRow && inCol)
    col = YELLOW;
  else if (inBox)
    col = GREEN;       // box context is the one people miss
  else if (inRow)
    col = MAGENTA;
  else if (inCol)
    col = YELLOW;
  return " " + col + string(1, ch) + " " + RESET;
}

// Blocks until the user presses Enter. Returns 'q' if they typed q to quit.
char waitForStep(const string &prompt, bool urgent) {
  cout << "\n" << (urgent ? RED + BOLD : GREEN + BOLD) << prompt << RESET
       << "  [" << (urgent ? "ENTER" : "ENTER") << " = next | q = quit]\n> ";
  string line;
  getline(cin, line);
  if (!line.empty() && (line[0] == 'q' || line[0] == 'Q'))
    return 'q';
  if (!line.empty() && (line[0] == 'r' || line[0] == 'R'))
    return 'r';
  return ' ';
}

void sim(const vector<vector<char>> &board) {
  vector<unordered_set<char>> rows(9), cols(9), boxes(9);

  cout << "\033[H\033[2J" << BOLD
       << "INTERACTIVE SUDOKU — Example 2 (INVALID: duplicate inside box 0)."
       << RESET << "\n\n";
  cout << "Legend:  " << MAGENTA << "MAGENTA" << RESET << " = row context  "
       << YELLOW << "YELLOW" << RESET << " = column context  "
       << GREEN << "GREEN" << RESET << " = box context\n"
       << "The cursor is " << CYAN << BOLD << "[1]" << RESET
       << ". Press Enter to advance one cell.\n" << RESET;
  waitForStep("Start scanning.", false);

  for (int r = 0; r < 9; ++r) {
    for (int c = 0; c < 9; ++c) {
      char v = board[r][c];
      int b = boxOf(r, c);

      cout << "\033[H\033[2J";
      cout << "Cell (" << r << "," << c << ")  value '" << v
           << "'  box #" << b << "\n\n";
      for (int i = 0; i < 9; ++i) {
        cout << "r" << i << ": ";
        for (int j = 0; j < 9; ++j)
          cout << glyph(board, i, j, r, c);
        cout << "\n";
      }

      if (v == '.') {
        cout << "\n'" << v << "' is a blank -> " << BOLD << "SKIPPED, no check" << RESET
             << "\n";
        if (waitForStep("Move to next cell.", false) == 'q')
          return;
        continue;
      }

      bool dup = rows[r].count(v) || cols[c].count(v) || boxes[b].count(v);
      cout << "\nChecking the " << BOLD << v << RESET << ":\n"
           << "  in row " << r << "  already? "
           << (rows[r].count(v) ? RED + "YES" + RESET : "no") << "\n"
           << "  in col " << c << "  already? "
           << (cols[c].count(v) ? RED + "YES" + RESET : "no") << "\n"
           << "  in box " << b << "  already? "
           << (boxes[b].count(v) ? RED + "YES" + RESET : "no") << "\n";

      if (dup) {
        cout << "\n" << RED << BOLD
             << "  !! DUPLICATE FOUND -> this board is INVALID !!" << RESET
             << "\n";
        waitForStep("That's the whole point. Here's where it ends.", true);
        return;
      }

      rows[r].insert(v);
      cols[c].insert(v);
      boxes[b].insert(v);
      cout << GREEN << "\nFirst time seeing it -> remembered in row " << r
           << ", col " << c << ", box " << b << RESET << "\n";
      waitForStep("Next cell.", false);
    }
  }
  cout << GREEN << BOLD << "\nScanned all 81 clean -> board is VALID.\n" << RESET;
}

int main() {
  vector<vector<char>> board = {
      {'1', '2', '.', '.', '3', '.', '.', '.', '.'},
      {'4', '.', '.', '5', '.', '.', '.', '.', '.'},
      {'.', '9', '1', '.', '.', '.', '.', '.', '3'},
      {'5', '.', '.', '.', '6', '.', '.', '.', '4'},
      {'.', '.', '.', '8', '.', '3', '.', '.', '5'},
      {'7', '.', '.', '.', '2', '.', '.', '.', '6'},
      {'.', '.', '.', '.', '.', '.', '2', '.', '.'},
      {'.', '.', '.', '4', '1', '9', '.', '.', '8'},
      {'.', '.', '.', '.', '8', '.', '.', '7', '9'}};

  sim(board);
  return 0;
}