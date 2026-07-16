#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <stack>
#include <queue>
#include <cmath>
#include <numeric>
#include <cassert>

using namespace std;

/**
 * Problem: Product of Array Except Self
 * Category: Arrays & Hashing
 * Difficulty: Medium
 * Time Complexity: O(N)
 * Space Complexity: O(1) (excluding output array)
 */

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n, 1);
        
        // 1. Prefix product loop (left-to-right)
        int prefix = 1;
        for (int i = 0; i < n; i++) {
            res[i] = prefix;
            prefix *= nums[i];
        }
        
        // 2. Suffix product loop (right-to-left)
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            res[i] *= suffix;
            suffix *= nums[i];
        }
        
        return res;
    }
};

int main() {
    Solution sol;
    
    // Test Case 1
    vector<int> nums1 = {1, 2, 4, 6};
    vector<int> expected1 = {48, 24, 12, 8};
    assert(sol.productExceptSelf(nums1) == expected1);
    
    // Test Case 2
    vector<int> nums2 = {-1, 0, 1, 2, 3};
    vector<int> expected2 = {0, -6, 0, 0, 0};
    assert(sol.productExceptSelf(nums2) == expected2);
    
    // Test Case 3 (Smallest size constraint)
    vector<int> nums3 = {2, 3};
    vector<int> expected3 = {3, 2};
    assert(sol.productExceptSelf(nums3) == expected3);
    
    cout << "All tests passed successfully! 🎉" << endl;
    return 0;
}
