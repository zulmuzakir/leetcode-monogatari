#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

/**
 * Problem: Two Sum
 * Category: Arrays & Hashing
 * Difficulty: Easy
 */

class Solution {
public:
  vector<int> twoSum(vector<int> &nums, int target) {
    unordered_map<int, int> numMap;

    for (int i = 0; i < nums.size(); i++) {
      numMap[nums[i]] = i;
    }

    for (int i = 0; i < nums.size(); i++) {
      int diff = target - nums[i];

      if (numMap.count(diff) && numMap[diff] != i) {
        return {i, numMap[diff]};
      }
    }

    return {};
  }
};

int main() {
  Solution sol;

  // Test Case 1
  vector<int> nums1 = {3, 4, 5, 6};
  int target1 = 7;
  vector<int> res1 = sol.twoSum(nums1, target1);
  cout << "Test 1 (Expected: [0,1]): [";
  for (size_t i = 0; i < res1.size(); ++i) {
    if (i > 0) cout << ",";
    cout << res1[i];
  }
  cout << "]" << endl;

  // Test Case 2
  vector<int> nums2 = {4, 5, 6};
  int target2 = 10;
  vector<int> res2 = sol.twoSum(nums2, target2);
  cout << "Test 2 (Expected: [0,2]): [";
  for (size_t i = 0; i < res2.size(); ++i) {
    if (i > 0) cout << ",";
    cout << res2[i];
  }
  cout << "]" << endl;

  return 0;
}
