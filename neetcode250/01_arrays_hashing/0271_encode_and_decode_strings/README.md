# [659. Encode and Decode Strings (Premium)](https://leetcode.com/problems/encode-and-decode-strings/)
[NeetCode Link](https://neetcode.io/problems/string-encode-and-decode)

## Problem Description
Design an algorithm to encode *a list of strings* to *a string*. The encoded string is then sent over the network and is decoded back to the original list of strings.

Machine 1 (sender) has the function:
```cpp
string encode(vector<string> strs) {
    // ... your code
    return encoded_string;
}
```

Machine 2 (receiver) has the function;
```cpp
vector<string> decode(string s) {
    // ... your code
    return strs;
}
```

So Machine 1 does:
```cpp
string encoded_string = encode(strs);
```

and Machine 2 does:
```cpp
vector<string> strs2 = decode(encoded_string)
```

`strs2` in Machine 2 should be the same as `strs` in Machine 1.

Implement the `encode` and `decode` methods.

## Example 1:
*Input*: dummy_input = ["Hello","World"]

*Output*: ["Hello","World"]

*Explanation*:
Machine 1:
Codec encoder = new Codec();
String msg = encoder.encode(strs);
Machine 1 ---msg---> Machine 2

Machine 2:
Codec decoder = new Codec();
String[] strs = decoder.decode(msg);

## Example 2:
Input: dummy_input = [""]
Output: [""]

## Constraints:
- `0 <= strs.length < 100`
- `0 <= strs[i].length < 200`
- `strs[i]` contains any possible characters out of `256` valid ASCII characters.

## Intuition
To encode a list of strings into a single string, we need a way to distinguish where one string ends and the next begins. A simple delimiter (like `,`) isn't enough because that character might exist within the strings themselves.

The **Length Prefix** approach solves this:
1.  For each string, we prepend its length followed by a separator (e.g., `#`).
2.  An encoded string looks like: `[length1]#[string1][length2]#[string2]...`
3.  During decoding:
    - We read the numeric length until we hit the `#` separator.
    - We skip the `#` and read exactly the specified number of characters.
    - This allows us to handle any character (including `#`) within the original strings without ambiguity.

## Complexity Analysis
- **Time Complexity:** $O(N)$, where $N$ is the total number of characters in the input list. We iterate through each character once during both encoding and decoding.
- **Space Complexity:** $O(N)$ to store the encoded string and the resulting list of decoded strings. The extra space for length prefixes and delimiters is proportional to the number of strings.
