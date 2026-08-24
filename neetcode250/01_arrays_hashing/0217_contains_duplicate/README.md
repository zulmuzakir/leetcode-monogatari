# [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

## Problem Description
Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

## Intuition
- **Brute Force:** Compare every pair. $O(N^2)$ time.
- **Sorting:** Sort the array and check adjacent elements. $O(N \log N)$ time, $O(1)$ or $O(\log N)$ space.
- **Hash Set:** Use a set to track seen numbers. $O(N)$ time and space.

## Complexity Analysis
- **Time Complexity:** $O(N)$ - We traverse the array once.
- **Space Complexity:** $O(N)$ - In the worst case, we store all elements in the hash set.
