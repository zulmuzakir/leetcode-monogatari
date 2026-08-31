#include <cassert>
#include <iostream>
#include <vector>

using namespace std;

/**
 * Problem: Majority Element
 * Category: Arrays & Hashing
 * Difficulty: Easy
 *
 * Given an array nums of size n, return the majority element.
 * The majority element appears more than floor(n / 2) times.
 * You may assume that the majority element always exists in the array.
 *
 * Time Complexity: O(n)
 * Space Complexity: O(1)
 */

class Solution {
public:
  int majorityElement(vector<int> &nums) {

    int candidate, count = 0;

    for (int i = 0; i < size(nums); i++) {
      if (count == 0) {
        candidate = nums[i];
        count = 1;
      } else {
        if (nums[i] == candidate) {
          count++;
        } else {
          count--;
        }
      }
    }
    
    return candidate;
  }
};

int main() {
  Solution sol;

  // Test Case 1: nums = [3, 2, 3] -> 3
  vector<int> nums1 = {3, 2, 3};
  assert(sol.majorityElement(nums1) == 3);
  cout << "Test 1 passed." << endl;

  // Test Case 2: nums = [2, 2, 1, 1, 1, 2, 2] -> 2
  vector<int> nums2 = {2, 2, 1, 1, 1, 2, 2};
  assert(sol.majorityElement(nums2) == 2);
  cout << "Test 2 passed." << endl;

  // Test Case 3: nums = [1] -> 1
  vector<int> nums3 = {1};
  assert(sol.majorityElement(nums3) == 1);
  cout << "Test 3 passed." << endl;

  return 0;
}
