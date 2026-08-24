# [36. Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)

## Problem Description
Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to these rules:
1. Each row must contain the digits `1-9` without repetition.
2. Each column must contain the digits `1-9` without repetition.
3. Each of the nine `3 x 3` sub-boxes must contain the digits `1-9` without repetition.

## Intuition
- **Brute Force:** For every filled cell, rescan its entire row, column, and box for a duplicate. $O(9^3)$ time with no extra space — wasteful because each constraint is re-checked from scratch.
- **Hash Sets per Constraint:** Track seen digits in 9 row sets, 9 column sets, and 9 box sets during a single pass. The box index for cell `(r, c)` is `(r / 3) * 3 + (c / 3)`, mapping the three row bands and column bands to `0-8`. A duplicate in any of the three sets means the board is invalid.
- Blank cells (`'.'`) are skipped — they participate in no rule.

## Complexity Analysis
- **Time Complexity:** $O(9^2) = O(1)$ - The board is fixed at 9x9; we visit each cell once and do O(1) set lookups/inserts.
- **Space Complexity:** $O(9^2) = O(1)$ - 27 sets holding at most 9 digits each; constant for the fixed board size.
