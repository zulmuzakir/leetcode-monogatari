#include <algorithm>
#include <cassert>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

/**
 * Problem: Top K Frequent Elements
 * Category: Arrays & Hashing
 * Difficulty: Medium
 */

class Solution {
public:
  vector<int> topKFrequent(vector<int> &nums, int k) {
    unordered_map<int, int> count;
    vector<vector<int>> freq(nums.size() + 1);

    for (int n : nums) {
      count[n] = 1 + count[n];
    }

    for (const auto &entry : count) {
      freq[entry.second].push_back(entry.first);
    }

    vector<int> res;
    for (int i = freq.size() - 1; i > 0; --i) {
      for (int n : freq[i]) {
        res.push_back(n);
        if (res.size() == k) {
          return res;
        }
      }
    }

    return res;
  }
};

int main() {
  Solution sol;

  // Test Case 1
  vector<int> nums1 = {1, 1, 1, 2, 2, 3};
  int k1 = 2;
  vector<int> res1 = sol.topKFrequent(nums1, k1);
  sort(res1.begin(), res1.end());
  assert(res1 == vector<int>({1, 2}));

  // Test Case 2
  vector<int> nums2 = {1};
  int k2 = 1;
  vector<int> res2 = sol.topKFrequent(nums2, k2);
  sort(res2.begin(), res2.end());
  assert(res2 == vector<int>({1}));

  // Test Case 3: Negative numbers
  vector<int> nums3 = {-1, -1, 2, 2, 2, 3};
  int k3 = 2;
  vector<int> res3 = sol.topKFrequent(nums3, k3);
  sort(res3.begin(), res3.end());
  vector<int> expected3 = {-1, 2};
  sort(expected3.begin(), expected3.end());
  assert(res3 == expected3);

  cout << "All test cases passed!" << endl;

  return 0;
}
