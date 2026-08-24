#include <algorithm>
#include <cassert>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

class Solution {
public:
  vector<vector<string>> groupAnagrams(vector<string> &strs) {
    unordered_map<string, vector<string>> res;

    for (const auto &str : strs) {
      vector<int> count(26, 0);
      for (char c : str) {
        count[c - 'a']++;
      }

      string key = to_string(count[0]);
      for (int i = 1; i < 26; ++i) {
        key += ',' + to_string(count[i]);
      }

      res[key].push_back(str);
    }

    vector<vector<string>> result;
    for (const auto &pair : res) {
      result.push_back(pair.second);
    }

    return result;
  }
};

bool containsGroup(const vector<vector<string>> &result,
                   const vector<string> &expected) {
  for (const auto &group : result) {
    if (group.size() != expected.size())
      continue;
    unordered_multiset<string> ms(expected.begin(), expected.end());
    unordered_multiset<string> ms2(group.begin(), group.end());
    if (ms == ms2)
      return true;
  }
  return false;
}

int main() {
  Solution sol;

  // Test Case 1
  vector<string> input1 = {"eat", "tea", "tan", "ate", "nat", "bat"};
  vector<vector<string>> result1 = sol.groupAnagrams(input1);
  assert(result1.size() == 3);
  assert(containsGroup(result1, {"eat", "tea", "ate"}));
  assert(containsGroup(result1, {"tan", "nat"}));
  assert(containsGroup(result1, {"bat"}));
  cout << "Test 1 passed" << endl;

  // Test Case 2
  vector<string> input2 = {""};
  vector<vector<string>> result2 = sol.groupAnagrams(input2);
  assert(result2.size() == 1);
  assert(result2[0].size() == 1 && result2[0][0] == "");
  cout << "Test 2 passed" << endl;

  // Test Case 3
  vector<string> input3 = {"a"};
  vector<vector<string>> result3 = sol.groupAnagrams(input3);
  assert(result3.size() == 1);
  assert(result3[0].size() == 1 && result3[0][0] == "a");
  cout << "Test 3 passed" << endl;

  // Test Case 4
  vector<string> input4 = {"abc", "bca", "cab", "xyz", "zyx"};
  vector<vector<string>> result4 = sol.groupAnagrams(input4);
  assert(result4.size() == 2);
  assert(containsGroup(result4, {"abc", "bca", "cab"}));
  assert(containsGroup(result4, {"xyz", "zyx"}));
  cout << "Test 4 passed" << endl;

  // Test Case 5
  vector<string> input5 = {};
  vector<vector<string>> result5 = sol.groupAnagrams(input5);
  assert(result5.size() == 0);
  cout << "Test 5 passed" << endl;

  cout << "All tests passed!" << endl;
  return 0;
}
