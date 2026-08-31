#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

using namespace std;

/**
 * Problem: Remove Element
 * Category: Arrays & Hashing
 * Difficulty: Easy
 *
 * Given an integer array nums and an integer val, remove all occurrences of
 * val in-place and return the number of elements that remain.
 *
 * The first k elements of nums must contain the values not equal to val.
 * Values after the first k elements are not important, and their order may
 * be changed.
 *
 * Time Complexity: O(?)
 * Space Complexity: O(?)
 */

class Solution {
public:
  int removeElement(vector<int> &nums, int val) {
    int k = 0;

    for (int num : nums) {
      if (num != val) {
        nums[k] = num;
        k++;
      }
    }
    return k;
  }
};

int main() {
  Solution sol;

  // Test Case 1
  vector<int> nums1 = {3, 2, 2, 3};
  int k1 = sol.removeElement(nums1, 3);
  assert(k1 == 2);
  assert(nums1[0] == 2 && nums1[1] == 2);
  cout << "Test 1 passed." << endl;

  // Test Case 2
  vector<int> nums2 = {0, 1, 2, 2, 3, 0, 4, 2};
  int k2 = sol.removeElement(nums2, 2);
  assert(k2 == 5);
  // The order may change, so verify the first k elements after sorting.
  sort(nums2.begin(), nums2.begin() + k2);
  assert(vector<int>(nums2.begin(), nums2.begin() + k2) ==
         vector<int>({0, 0, 1, 3, 4}));
  cout << "Test 2 passed." << endl;

  return 0;
}
