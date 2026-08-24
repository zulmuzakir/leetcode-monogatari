#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;

/**
 * Problem: Valid Anagram
 * Category: Arrays & Hashing
 * Difficulty: Easy
 */

class Solution {
public:
  bool isAnagram(string s, string t) {
    unordered_map<char, int> text1;
    unordered_map<char, int> text2;

    for (char c1 : s) {
      text1[c1]++;
    }

    for (char c2 : t) {
      text2[c2]++;
    }

    if (text1 == text2) {
      return true;
    }

    return false;
  }
};

int main() {
  Solution sol;

  // Test Case 1
  string s1 = "racecar";
  string t1 = "carrace";
  cout << "Test 1 (Expected: true): " << sol.isAnagram(s1, t1) << endl;

  // Test Case 2
  string s2 = "jar";
  string t2 = "jam";
  cout << "Test 2 (Expected: false): " << sol.isAnagram(s2, t2) << endl;

  return 0;
}
