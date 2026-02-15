# [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)
[NeetCode Link](https://neetcode.io/problems/top-k-elements-in-list)

## Problem Description
Given an integer array `nums` and an integer `k`, return *the `k` most frequent elements*. You may return the answer in **any order**.

## Example 1:
**Input:** nums = [1,1,1,2,2,3], k = 2
**Output:** [1,2]

## Example 2:
**Input:** nums = [1], k = 1
**Output:** [1]

## Constraints:
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `k` is in the range `[1, the number of unique elements in the array]`.
- It is guaranteed that the answer is **unique**.

## Intuition
- **Bucket Sort:**
  1. Count the frequency of each element using a hash map.
  2. Create an array of buckets (vectors) where the index represents the frequency.
  3. Iterate through the hash map and place each element in the bucket corresponding to its frequency.
  4. Iterate through the buckets from highest frequency to lowest and collect the first `k` elements.

## Complexity Analysis
- **Time Complexity:** $O(N)$ - We iterate through `nums` once to count frequencies, then through the hash map, and finally through the buckets. All these operations are linear with respect to the number of elements $N$.
- **Space Complexity:** $O(N)$ - We use a hash map to store frequencies and an array of buckets, both of which can store up to $N$ elements.
