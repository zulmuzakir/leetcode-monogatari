# [1. Two Sum](https://leetcode.com/problems/two-sum/)

## Problem Description
Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.

You may assume that each input would have **exactly one solution**, and you may not use the *same* element twice.

You can return the answer in any order.

## Example 1:
**Input:** nums = [2,7,11,15], target = 9
**Output:** [0,1]
**Explanation:** Because nums[0] + nums[1] == 9, we return [0, 1].

## Example 2:
**Input:** nums = [3,2,4], target = 6
**Output:** [1,2]

## Example 3:
**Input:** nums = [3,3], target = 6
**Output:** [0,1]

## Constraints:
- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- **Only one valid answer exists.**

## Intuition
- **Brute Force:** Check every pair of numbers. $O(N^2)$ time.
- **Two-Pass Hash Map:** First pass to populate map with values and indices, second pass to check for complement. $O(N)$ time.
- **One-Pass Hash Map:** While iterating, check if the complement already exists in the map. If not, add the current number to the map. $O(N)$ time.

## Complexity Analysis
- **Time Complexity:** $O(N)$ - We traverse the list containing $N$ elements only once. Each lookup in the table costs only $O(1)$ time.
- **Space Complexity:** $O(N)$ - The extra space required depends on the number of items stored in the hash table, which stores at most $N$ elements.
