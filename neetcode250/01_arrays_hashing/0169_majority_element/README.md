# [169. Majority Element](https://neetcode.io/problems/majority-element/question)

## Problem Description

Given an array `nums` of size `n`, return the majority element.

The majority element is the element that appears more than `floor(n / 2)` times.
You may assume that the majority element always exists in the array.

## Examples

### Example 1

```text
Input: nums = [3, 2, 3]
Output: 3
```

### Example 2

```text
Input: nums = [2, 2, 1, 1, 1, 2, 2]
Output: 2
```

## Constraints

- `1 <= nums.length <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`
- The majority element always exists in the array.

## Intuition

The majority element appears more times than all other elements combined. Therefore, if we repeatedly cancel one occurrence of the current candidate with a different element, the majority element cannot be completely canceled.

The remaining candidate after all cancellations must be the majority element.

## Approach: Boyer-Moore Majority Vote

Maintain two variables:

- `candidate`: the current possible majority element.
- `count`: the candidate's unmatched vote count.

For each number:

1. If `count` is zero, choose the current number as the new candidate.
2. If the current number equals `candidate`, increment `count`.
3. Otherwise, decrement `count` because the two different values cancel each other out.
4. Return the final candidate.

## Complexity Analysis

- **Time Complexity:** `O(n)` because the array is traversed once.
- **Space Complexity:** `O(1)` because only a constant number of variables are used.
