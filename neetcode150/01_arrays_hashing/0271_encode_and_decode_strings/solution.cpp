#include <algorithm>
#include <cassert>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

/**
 * Problem: Encode and Decode Strings
 * Category: Arrays & Hashing
 * Difficulty: Medium
 */

class Solution {
public:
  string encode(vector<string> &strs) {
    string res;

    for (const string &str : strs) {
      res += to_string(str.size()) + "#" + str;
    }

    return res;
  }

  vector<string> decode(string s) {
    vector<string> res;
    int i = 0;

    while (i < s.size()) {
      int j = i;
      while (s[j] != '#') {
        j++;
      }

      int length = stoi(s.substr(i, j - i));
      i = j + 1;
      j = i + length;

      res.push_back((s.substr(i, length)));
      i = j;
    }

    return res;
  }
};

int main() {
  Solution sol;

  // Test Case 1: Standard words
  vector<string> input1 = {"hello", "world"};
  assert(sol.decode(sol.encode(input1)) == input1);

  // Test Case 2: Symbols inside the string
  vector<string> input2 = {"#", "##", "3#hi"};
  assert(sol.decode(sol.encode(input2)) == input2);

  // Test Case 3: Empty strings
  vector<string> input3 = {"", "", ""};
  assert(sol.decode(sol.encode(input3)) == input3);

  // Test Case 4: Numbers as strings
  vector<string> input4 = {"10", "5#apple"};
  assert(sol.decode(sol.encode(input4)) == input4);

  cout << "All test cases passed successfully! 🎉" << endl;

  return 0;
}
