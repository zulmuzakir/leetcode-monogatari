#include <algorithm>
#include <iostream>
#include <unordered_set>
#include <vector>

using namespace std;

/**
 * Problem: Contains Duplicate
 * Category: Arrays & Hashing
 * Difficulty: Easy
 */

class Solution {
public:
  bool containsDuplicate(vector<int> &nums) {
    unordered_set<int> seen;
    for (int num : nums) {
      // if (seen.find(num) != seen.end()) {
      //     return true;
      // }

      // or like this
      if (seen.count(num)) {
        return true;
      }
      seen.insert(num);
    }
    return false;
  }
};

int main() {
  Solution sol;

  // Test Case 1
  vector<int> nums1 = {1, 2, 3, 1};
  cout << "Test 1 (Expected: 1): " << sol.containsDuplicate(nums1) << endl;

  // Test Case 2
  vector<int> nums2 = {1, 2, 3, 4};
  cout << "Test 2 (Expected: 0): " << sol.containsDuplicate(nums2) << endl;

  return 0;
}
