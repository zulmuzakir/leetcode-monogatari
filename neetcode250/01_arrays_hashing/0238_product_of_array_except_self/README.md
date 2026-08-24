# [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/description/)
[NeetCode Link](https://neetcode.io/problems/products-of-array-discluding-self/)

## Problem Description
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in $O(N)$ time and without using the division operation.

## Example 1:
**Input:** nums = [1,2,4,6]
**Output:** [48,24,12,8]

## Example 2:
**Input:** nums = [-1,0,1,2,3]
**Output:** [0,-6,0,0,0]

## Constraints:
- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

## Intuition
To solve this without division and in $O(N)$ time, we can precalculate the product of all elements to the left of each element, and the product of all elements to the right of each element.

By multiplying the left product and the right product for each index, we get the product of all elements except the one at that index.

We can optimize the space complexity to $O(1)$ (excluding the output array) by using the output array to store the prefix products first, and then iterating backwards to multiply by the suffix products on the fly.

## Complexity Analysis
- **Time Complexity:** $O(N)$ - We iterate through the array twice: once from left-to-right and once from right-to-left.
- **Space Complexity:** $O(1)$ - Excluding the output array, we only use a single variable to track the running suffix product.
