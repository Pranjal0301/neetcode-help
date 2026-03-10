#!/usr/bin/env python3
"""
Transforms NeetCode 150 HTML to add multi-language code tabs.
Adds C++, Java, JavaScript alongside existing Python for all 150 problems.
"""
import re, json, html

# All solutions organized by leetcode problem number
# Each entry: { "cpp": "...", "java": "...", "js": "..." }
solutions = {}

# ============================================
# ARRAYS & HASHING
# ============================================

solutions["217"] = {
"cpp": """class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int num : nums) {
            if (seen.count(num)) return true;
            seen.insert(num);
        }
        return false;
    }
};""",
"java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (!seen.add(num)) return true;
        }
        return false;
    }
}""",
"js": """var containsDuplicate = function(nums) {
    const seen = new Set();
    for (const num of nums) {
        if (seen.has(num)) return true;
        seen.add(num);
    }
    return false;
};"""
}

solutions["242"] = {
"cpp": """class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.size() != t.size()) return false;
        int count[26] = {};
        for (int i = 0; i < s.size(); i++) {
            count[s[i] - 'a']++;
            count[t[i] - 'a']--;
        }
        for (int c : count) if (c != 0) return false;
        return true;
    }
};""",
"java": """class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) return false;
        int[] count = new int[26];
        for (int i = 0; i < s.length(); i++) {
            count[s.charAt(i) - 'a']++;
            count[t.charAt(i) - 'a']--;
        }
        for (int c : count) if (c != 0) return false;
        return true;
    }
}""",
"js": """var isAnagram = function(s, t) {
    if (s.length !== t.length) return false;
    const count = {};
    for (const c of s) count[c] = (count[c] || 0) + 1;
    for (const c of t) {
        if (!count[c]) return false;
        count[c]--;
    }
    return true;
};"""
}

solutions["1"] = {
"cpp": """class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> map;
        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];
            if (map.count(complement))
                return {map[complement], i};
            map[nums[i]] = i;
        }
        return {};
    }
};""",
"java": """class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement))
                return new int[]{map.get(complement), i};
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}""",
"js": """var twoSum = function(nums, target) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (map.has(complement))
            return [map.get(complement), i];
        map.set(nums[i], i);
    }
};"""
}

solutions["49"] = {
"cpp": """class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> map;
        for (string& s : strs) {
            string key = s;
            sort(key.begin(), key.end());
            map[key].push_back(s);
        }
        vector<vector<string>> result;
        for (auto& [k, v] : map) result.push_back(v);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] arr = s.toCharArray();
            Arrays.sort(arr);
            String key = new String(arr);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}""",
"js": """var groupAnagrams = function(strs) {
    const map = new Map();
    for (const s of strs) {
        const key = s.split('').sort().join('');
        if (!map.has(key)) map.set(key, []);
        map.get(key).push(s);
    }
    return Array.from(map.values());
};"""
}

solutions["347"] = {
"cpp": """class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> freq;
        for (int n : nums) freq[n]++;
        vector<vector<int>> bucket(nums.size() + 1);
        for (auto& [num, cnt] : freq) bucket[cnt].push_back(num);
        vector<int> result;
        for (int i = bucket.size() - 1; i >= 0 && result.size() < k; i--)
            for (int n : bucket[i]) {
                result.push_back(n);
                if (result.size() == k) break;
            }
        return result;
    }
};""",
"java": """class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int n : nums) freq.merge(n, 1, Integer::sum);
        List<Integer>[] bucket = new List[nums.length + 1];
        for (int i = 0; i < bucket.length; i++) bucket[i] = new ArrayList<>();
        for (var e : freq.entrySet()) bucket[e.getValue()].add(e.getKey());
        int[] result = new int[k];
        int idx = 0;
        for (int i = bucket.length - 1; i >= 0 && idx < k; i--)
            for (int n : bucket[i]) { result[idx++] = n; if (idx == k) break; }
        return result;
    }
}""",
"js": """var topKFrequent = function(nums, k) {
    const freq = new Map();
    for (const n of nums) freq.set(n, (freq.get(n) || 0) + 1);
    const bucket = Array.from({length: nums.length + 1}, () => []);
    for (const [num, cnt] of freq) bucket[cnt].push(num);
    const result = [];
    for (let i = bucket.length - 1; i >= 0 && result.length < k; i--)
        result.push(...bucket[i]);
    return result.slice(0, k);
};"""
}

solutions["271"] = {
"cpp": """class Codec {
public:
    string encode(vector<string>& strs) {
        string result;
        for (const string& s : strs)
            result += to_string(s.size()) + "#" + s;
        return result;
    }
    vector<string> decode(string s) {
        vector<string> result;
        int i = 0;
        while (i < s.size()) {
            int j = s.find('#', i);
            int len = stoi(s.substr(i, j - i));
            result.push_back(s.substr(j + 1, len));
            i = j + 1 + len;
        }
        return result;
    }
};""",
"java": """public class Codec {
    public String encode(List<String> strs) {
        StringBuilder sb = new StringBuilder();
        for (String s : strs) sb.append(s.length()).append('#').append(s);
        return sb.toString();
    }
    public List<String> decode(String s) {
        List<String> result = new ArrayList<>();
        int i = 0;
        while (i < s.length()) {
            int j = s.indexOf('#', i);
            int len = Integer.parseInt(s.substring(i, j));
            result.add(s.substring(j + 1, j + 1 + len));
            i = j + 1 + len;
        }
        return result;
    }
}""",
"js": """var encode = function(strs) {
    return strs.map(s => s.length + '#' + s).join('');
};
var decode = function(s) {
    const result = [];
    let i = 0;
    while (i < s.length) {
        let j = s.indexOf('#', i);
        const len = parseInt(s.substring(i, j));
        result.push(s.substring(j + 1, j + 1 + len));
        i = j + 1 + len;
    }
    return result;
};"""
}

solutions["238"] = {
"cpp": """class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, 1);
        int prefix = 1;
        for (int i = 0; i < n; i++) {
            result[i] = prefix;
            prefix *= nums[i];
        }
        int postfix = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] *= postfix;
            postfix *= nums[i];
        }
        return result;
    }
};""",
"java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        int prefix = 1;
        for (int i = 0; i < n; i++) {
            result[i] = prefix;
            prefix *= nums[i];
        }
        int postfix = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] *= postfix;
            postfix *= nums[i];
        }
        return result;
    }
}""",
"js": """var productExceptSelf = function(nums) {
    const n = nums.length, result = new Array(n).fill(1);
    let prefix = 1;
    for (let i = 0; i < n; i++) { result[i] = prefix; prefix *= nums[i]; }
    let postfix = 1;
    for (let i = n - 1; i >= 0; i--) { result[i] *= postfix; postfix *= nums[i]; }
    return result;
};"""
}

solutions["36"] = {
"cpp": """class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        unordered_set<string> seen;
        for (int i = 0; i < 9; i++)
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') continue;
                string d(1, board[i][j]);
                if (!seen.insert(d + "r" + to_string(i)).second ||
                    !seen.insert(d + "c" + to_string(j)).second ||
                    !seen.insert(d + "b" + to_string(i/3) + to_string(j/3)).second)
                    return false;
            }
        return true;
    }
};""",
"java": """class Solution {
    public boolean isValidSudoku(char[][] board) {
        Set<String> seen = new HashSet<>();
        for (int i = 0; i < 9; i++)
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') continue;
                String d = String.valueOf(board[i][j]);
                if (!seen.add(d + "r" + i) ||
                    !seen.add(d + "c" + j) ||
                    !seen.add(d + "b" + i/3 + j/3))
                    return false;
            }
        return true;
    }
}""",
"js": """var isValidSudoku = function(board) {
    const seen = new Set();
    for (let i = 0; i < 9; i++)
        for (let j = 0; j < 9; j++) {
            if (board[i][j] === '.') continue;
            const d = board[i][j];
            const row = d + 'r' + i, col = d + 'c' + j;
            const box = d + 'b' + Math.floor(i/3) + Math.floor(j/3);
            if (seen.has(row) || seen.has(col) || seen.has(box)) return false;
            seen.add(row); seen.add(col); seen.add(box);
        }
    return true;
};"""
}

solutions["128"] = {
"cpp": """class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> s(nums.begin(), nums.end());
        int longest = 0;
        for (int n : s) {
            if (!s.count(n - 1)) {
                int len = 1;
                while (s.count(n + len)) len++;
                longest = max(longest, len);
            }
        }
        return longest;
    }
};""",
"java": """class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int n : nums) set.add(n);
        int longest = 0;
        for (int n : set) {
            if (!set.contains(n - 1)) {
                int len = 1;
                while (set.contains(n + len)) len++;
                longest = Math.max(longest, len);
            }
        }
        return longest;
    }
}""",
"js": """var longestConsecutive = function(nums) {
    const set = new Set(nums);
    let longest = 0;
    for (const n of set) {
        if (!set.has(n - 1)) {
            let len = 1;
            while (set.has(n + len)) len++;
            longest = Math.max(longest, len);
        }
    }
    return longest;
};"""
}


# ============================================
# TWO POINTERS
# ============================================

solutions["125"] = {
"cpp": """class Solution {
public:
    bool isPalindrome(string s) {
        int l = 0, r = s.size() - 1;
        while (l < r) {
            while (l < r && !isalnum(s[l])) l++;
            while (l < r && !isalnum(s[r])) r--;
            if (tolower(s[l]) != tolower(s[r])) return false;
            l++; r--;
        }
        return true;
    }
};""",
"java": """class Solution {
    public boolean isPalindrome(String s) {
        int l = 0, r = s.length() - 1;
        while (l < r) {
            while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
            while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
            if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r)))
                return false;
            l++; r--;
        }
        return true;
    }
}""",
"js": """var isPalindrome = function(s) {
    const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');
    let l = 0, r = cleaned.length - 1;
    while (l < r) {
        if (cleaned[l] !== cleaned[r]) return false;
        l++; r--;
    }
    return true;
};"""
}

solutions["167"] = {
"cpp": """class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int l = 0, r = numbers.size() - 1;
        while (l < r) {
            int sum = numbers[l] + numbers[r];
            if (sum == target) return {l + 1, r + 1};
            else if (sum < target) l++;
            else r--;
        }
        return {};
    }
};""",
"java": """class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int l = 0, r = numbers.length - 1;
        while (l < r) {
            int sum = numbers[l] + numbers[r];
            if (sum == target) return new int[]{l + 1, r + 1};
            else if (sum < target) l++;
            else r--;
        }
        return new int[]{};
    }
}""",
"js": """var twoSum = function(numbers, target) {
    let l = 0, r = numbers.length - 1;
    while (l < r) {
        const sum = numbers[l] + numbers[r];
        if (sum === target) return [l + 1, r + 1];
        else if (sum < target) l++;
        else r--;
    }
};"""
}

solutions["15"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> result;
        for (int i = 0; i < (int)nums.size() - 2; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue;
            int l = i + 1, r = nums.size() - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    result.push_back({nums[i], nums[l], nums[r]});
                    while (l < r && nums[l] == nums[l+1]) l++;
                    while (l < r && nums[r] == nums[r-1]) r--;
                    l++; r--;
                } else if (sum < 0) l++;
                else r--;
            }
        }
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue;
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l+1]) l++;
                    while (l < r && nums[r] == nums[r-1]) r--;
                    l++; r--;
                } else if (sum < 0) l++;
                else r--;
            }
        }
        return result;
    }
}""",
"js": """var threeSum = function(nums) {
    nums.sort((a, b) => a - b);
    const result = [];
    for (let i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] === nums[i-1]) continue;
        let l = i + 1, r = nums.length - 1;
        while (l < r) {
            const sum = nums[i] + nums[l] + nums[r];
            if (sum === 0) {
                result.push([nums[i], nums[l], nums[r]]);
                while (l < r && nums[l] === nums[l+1]) l++;
                while (l < r && nums[r] === nums[r-1]) r--;
                l++; r--;
            } else if (sum < 0) l++;
            else r--;
        }
    }
    return result;
};"""
}

solutions["11"] = {
"cpp": """class Solution {
public:
    int maxArea(vector<int>& height) {
        int l = 0, r = height.size() - 1, maxWater = 0;
        while (l < r) {
            maxWater = max(maxWater, min(height[l], height[r]) * (r - l));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return maxWater;
    }
};""",
"java": """class Solution {
    public int maxArea(int[] height) {
        int l = 0, r = height.length - 1, maxWater = 0;
        while (l < r) {
            maxWater = Math.max(maxWater, Math.min(height[l], height[r]) * (r - l));
            if (height[l] < height[r]) l++;
            else r--;
        }
        return maxWater;
    }
}""",
"js": """var maxArea = function(height) {
    let l = 0, r = height.length - 1, maxWater = 0;
    while (l < r) {
        maxWater = Math.max(maxWater, Math.min(height[l], height[r]) * (r - l));
        if (height[l] < height[r]) l++;
        else r--;
    }
    return maxWater;
};"""
}

solutions["42"] = {
"cpp": """class Solution {
public:
    int trap(vector<int>& height) {
        int l = 0, r = height.size() - 1;
        int leftMax = 0, rightMax = 0, water = 0;
        while (l < r) {
            if (height[l] < height[r]) {
                leftMax = max(leftMax, height[l]);
                water += leftMax - height[l];
                l++;
            } else {
                rightMax = max(rightMax, height[r]);
                water += rightMax - height[r];
                r--;
            }
        }
        return water;
    }
};""",
"java": """class Solution {
    public int trap(int[] height) {
        int l = 0, r = height.length - 1;
        int leftMax = 0, rightMax = 0, water = 0;
        while (l < r) {
            if (height[l] < height[r]) {
                leftMax = Math.max(leftMax, height[l]);
                water += leftMax - height[l];
                l++;
            } else {
                rightMax = Math.max(rightMax, height[r]);
                water += rightMax - height[r];
                r--;
            }
        }
        return water;
    }
}""",
"js": """var trap = function(height) {
    let l = 0, r = height.length - 1;
    let leftMax = 0, rightMax = 0, water = 0;
    while (l < r) {
        if (height[l] < height[r]) {
            leftMax = Math.max(leftMax, height[l]);
            water += leftMax - height[l];
            l++;
        } else {
            rightMax = Math.max(rightMax, height[r]);
            water += rightMax - height[r];
            r--;
        }
    }
    return water;
};"""
}

# ============================================
# SLIDING WINDOW
# ============================================

solutions["121"] = {
"cpp": """class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int minPrice = INT_MAX, maxProfit = 0;
        for (int price : prices) {
            minPrice = min(minPrice, price);
            maxProfit = max(maxProfit, price - minPrice);
        }
        return maxProfit;
    }
};""",
"java": """class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE, maxProfit = 0;
        for (int price : prices) {
            minPrice = Math.min(minPrice, price);
            maxProfit = Math.max(maxProfit, price - minPrice);
        }
        return maxProfit;
    }
}""",
"js": """var maxProfit = function(prices) {
    let minPrice = Infinity, maxProfit = 0;
    for (const price of prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
};"""
}

solutions["3"] = {
"cpp": """class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> chars;
        int l = 0, result = 0;
        for (int r = 0; r < s.size(); r++) {
            while (chars.count(s[r])) {
                chars.erase(s[l]);
                l++;
            }
            chars.insert(s[r]);
            result = max(result, r - l + 1);
        }
        return result;
    }
};""",
"java": """class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> chars = new HashSet<>();
        int l = 0, result = 0;
        for (int r = 0; r < s.length(); r++) {
            while (chars.contains(s.charAt(r))) {
                chars.remove(s.charAt(l));
                l++;
            }
            chars.add(s.charAt(r));
            result = Math.max(result, r - l + 1);
        }
        return result;
    }
}""",
"js": """var lengthOfLongestSubstring = function(s) {
    const chars = new Set();
    let l = 0, result = 0;
    for (let r = 0; r < s.length; r++) {
        while (chars.has(s[r])) {
            chars.delete(s[l]);
            l++;
        }
        chars.add(s[r]);
        result = Math.max(result, r - l + 1);
    }
    return result;
};"""
}

solutions["424"] = {
"cpp": """class Solution {
public:
    int characterReplacement(string s, int k) {
        int count[26] = {}, l = 0, maxFreq = 0, result = 0;
        for (int r = 0; r < s.size(); r++) {
            maxFreq = max(maxFreq, ++count[s[r] - 'A']);
            while (r - l + 1 - maxFreq > k) {
                count[s[l] - 'A']--;
                l++;
            }
            result = max(result, r - l + 1);
        }
        return result;
    }
};""",
"java": """class Solution {
    public int characterReplacement(String s, int k) {
        int[] count = new int[26];
        int l = 0, maxFreq = 0, result = 0;
        for (int r = 0; r < s.length(); r++) {
            maxFreq = Math.max(maxFreq, ++count[s.charAt(r) - 'A']);
            while (r - l + 1 - maxFreq > k) {
                count[s.charAt(l) - 'A']--;
                l++;
            }
            result = Math.max(result, r - l + 1);
        }
        return result;
    }
}""",
"js": """var characterReplacement = function(s, k) {
    const count = {};
    let l = 0, maxFreq = 0, result = 0;
    for (let r = 0; r < s.length; r++) {
        count[s[r]] = (count[s[r]] || 0) + 1;
        maxFreq = Math.max(maxFreq, count[s[r]]);
        while (r - l + 1 - maxFreq > k) {
            count[s[l]]--;
            l++;
        }
        result = Math.max(result, r - l + 1);
    }
    return result;
};"""
}

solutions["567"] = {
"cpp": """class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        if (s1.size() > s2.size()) return false;
        int count[26] = {};
        for (char c : s1) count[c - 'a']++;
        for (int i = 0; i < s2.size(); i++) {
            count[s2[i] - 'a']--;
            if (i >= s1.size()) count[s2[i - s1.size()] - 'a']++;
            bool allZero = true;
            for (int j = 0; j < 26; j++) if (count[j]) { allZero = false; break; }
            if (allZero) return true;
        }
        return false;
    }
};""",
"java": """class Solution {
    public boolean checkInclusion(String s1, String s2) {
        if (s1.length() > s2.length()) return false;
        int[] count = new int[26];
        for (char c : s1.toCharArray()) count[c - 'a']++;
        int matches = 0;
        for (int i = 0; i < 26; i++) if (count[i] == 0) matches++;
        int l = 0;
        for (int r = 0; r < s2.length(); r++) {
            int idx = s2.charAt(r) - 'a';
            count[idx]--;
            if (count[idx] == 0) matches++;
            else if (count[idx] == -1) matches--;
            if (r >= s1.length()) {
                idx = s2.charAt(l) - 'a';
                count[idx]++;
                if (count[idx] == 0) matches++;
                else if (count[idx] == 1) matches--;
                l++;
            }
            if (matches == 26) return true;
        }
        return false;
    }
}""",
"js": """var checkInclusion = function(s1, s2) {
    if (s1.length > s2.length) return false;
    const count = new Array(26).fill(0);
    const a = 'a'.charCodeAt(0);
    for (const c of s1) count[c.charCodeAt(0) - a]++;
    for (let i = 0; i < s2.length; i++) {
        count[s2.charCodeAt(i) - a]--;
        if (i >= s1.length) count[s2.charCodeAt(i - s1.length) - a]++;
        if (count.every(c => c === 0)) return true;
    }
    return false;
};"""
}

solutions["76"] = {
"cpp": """class Solution {
public:
    string minWindow(string s, string t) {
        unordered_map<char, int> need, have;
        for (char c : t) need[c]++;
        int required = need.size(), formed = 0;
        int l = 0, minLen = INT_MAX, minL = 0;
        for (int r = 0; r < s.size(); r++) {
            have[s[r]]++;
            if (need.count(s[r]) && have[s[r]] == need[s[r]]) formed++;
            while (formed == required) {
                if (r - l + 1 < minLen) { minLen = r - l + 1; minL = l; }
                have[s[l]]--;
                if (need.count(s[l]) && have[s[l]] < need[s[l]]) formed--;
                l++;
            }
        }
        return minLen == INT_MAX ? "" : s.substr(minL, minLen);
    }
};""",
"java": """class Solution {
    public String minWindow(String s, String t) {
        Map<Character, Integer> need = new HashMap<>(), have = new HashMap<>();
        for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);
        int required = need.size(), formed = 0;
        int l = 0, minLen = Integer.MAX_VALUE, minL = 0;
        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            have.merge(c, 1, Integer::sum);
            if (need.containsKey(c) && have.get(c).intValue() == need.get(c).intValue())
                formed++;
            while (formed == required) {
                if (r - l + 1 < minLen) { minLen = r - l + 1; minL = l; }
                char lc = s.charAt(l);
                have.merge(lc, -1, Integer::sum);
                if (need.containsKey(lc) && have.get(lc) < need.get(lc)) formed--;
                l++;
            }
        }
        return minLen == Integer.MAX_VALUE ? "" : s.substring(minL, minL + minLen);
    }
}""",
"js": """var minWindow = function(s, t) {
    const need = {}, have = {};
    for (const c of t) need[c] = (need[c] || 0) + 1;
    let required = Object.keys(need).length, formed = 0;
    let l = 0, minLen = Infinity, minL = 0;
    for (let r = 0; r < s.length; r++) {
        have[s[r]] = (have[s[r]] || 0) + 1;
        if (need[s[r]] && have[s[r]] === need[s[r]]) formed++;
        while (formed === required) {
            if (r - l + 1 < minLen) { minLen = r - l + 1; minL = l; }
            have[s[l]]--;
            if (need[s[l]] && have[s[l]] < need[s[l]]) formed--;
            l++;
        }
    }
    return minLen === Infinity ? "" : s.substring(minL, minL + minLen);
};"""
}

solutions["239"] = {
"cpp": """class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq;
        vector<int> result;
        for (int i = 0; i < nums.size(); i++) {
            while (!dq.empty() && dq.front() < i - k + 1) dq.pop_front();
            while (!dq.empty() && nums[dq.back()] < nums[i]) dq.pop_back();
            dq.push_back(i);
            if (i >= k - 1) result.push_back(nums[dq.front()]);
        }
        return result;
    }
};""",
"java": """class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        Deque<Integer> dq = new ArrayDeque<>();
        int[] result = new int[nums.length - k + 1];
        int idx = 0;
        for (int i = 0; i < nums.length; i++) {
            while (!dq.isEmpty() && dq.peekFirst() < i - k + 1) dq.pollFirst();
            while (!dq.isEmpty() && nums[dq.peekLast()] < nums[i]) dq.pollLast();
            dq.offerLast(i);
            if (i >= k - 1) result[idx++] = nums[dq.peekFirst()];
        }
        return result;
    }
}""",
"js": """var maxSlidingWindow = function(nums, k) {
    const dq = [], result = [];
    for (let i = 0; i < nums.length; i++) {
        while (dq.length && dq[0] < i - k + 1) dq.shift();
        while (dq.length && nums[dq[dq.length - 1]] < nums[i]) dq.pop();
        dq.push(i);
        if (i >= k - 1) result.push(nums[dq[0]]);
    }
    return result;
};"""
}


# ============================================
# STACK
# ============================================

solutions["20"] = {
"cpp": """class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        unordered_map<char,char> m = {{')', '('}, {']', '['}, {'}', '{'}};
        for (char c : s) {
            if (m.count(c)) {
                if (st.empty() || st.top() != m[c]) return false;
                st.pop();
            } else st.push(c);
        }
        return st.empty();
    }
};""",
"java": """class Solution {
    public boolean isValid(String s) {
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '[') stack.push(']');
            else if (c == '{') stack.push('}');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }
        return stack.isEmpty();
    }
}""",
"js": """var isValid = function(s) {
    const stack = [], map = {')':'(', ']':'[', '}':'{'};
    for (const c of s) {
        if (map[c]) {
            if (!stack.length || stack.pop() !== map[c]) return false;
        } else stack.push(c);
    }
    return stack.length === 0;
};"""
}

solutions["155"] = {
"cpp": """class MinStack {
    stack<pair<int,int>> st; // {val, currentMin}
public:
    void push(int val) {
        int curMin = st.empty() ? val : min(val, st.top().second);
        st.push({val, curMin});
    }
    void pop() { st.pop(); }
    int top() { return st.top().first; }
    int getMin() { return st.top().second; }
};""",
"java": """class MinStack {
    private Stack<int[]> stack = new Stack<>();
    public void push(int val) {
        int min = stack.isEmpty() ? val : Math.min(val, stack.peek()[1]);
        stack.push(new int[]{val, min});
    }
    public void pop() { stack.pop(); }
    public int top() { return stack.peek()[0]; }
    public int getMin() { return stack.peek()[1]; }
}""",
"js": """var MinStack = function() { this.stack = []; };
MinStack.prototype.push = function(val) {
    const min = this.stack.length ? Math.min(val, this.getMin()) : val;
    this.stack.push([val, min]);
};
MinStack.prototype.pop = function() { this.stack.pop(); };
MinStack.prototype.top = function() { return this.stack[this.stack.length-1][0]; };
MinStack.prototype.getMin = function() { return this.stack[this.stack.length-1][1]; };"""
}

solutions["150"] = {
"cpp": """class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<int> st;
        for (const string& t : tokens) {
            if (t == "+" || t == "-" || t == "*" || t == "/") {
                int b = st.top(); st.pop();
                int a = st.top(); st.pop();
                if (t == "+") st.push(a + b);
                else if (t == "-") st.push(a - b);
                else if (t == "*") st.push(a * b);
                else st.push(a / b);
            } else st.push(stoi(t));
        }
        return st.top();
    }
};""",
"java": """class Solution {
    public int evalRPN(String[] tokens) {
        Stack<Integer> stack = new Stack<>();
        for (String t : tokens) {
            switch (t) {
                case "+": stack.push(stack.pop() + stack.pop()); break;
                case "-": int b = stack.pop(); stack.push(stack.pop() - b); break;
                case "*": stack.push(stack.pop() * stack.pop()); break;
                case "/": int d = stack.pop(); stack.push(stack.pop() / d); break;
                default: stack.push(Integer.parseInt(t));
            }
        }
        return stack.peek();
    }
}""",
"js": """var evalRPN = function(tokens) {
    const stack = [];
    for (const t of tokens) {
        if (['+','-','*','/'].includes(t)) {
            const b = stack.pop(), a = stack.pop();
            if (t === '+') stack.push(a + b);
            else if (t === '-') stack.push(a - b);
            else if (t === '*') stack.push(a * b);
            else stack.push(Math.trunc(a / b));
        } else stack.push(Number(t));
    }
    return stack[0];
};"""
}

solutions["22"] = {
"cpp": """class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        function<void(string&, int, int)> backtrack = [&](string& cur, int open, int close) {
            if (cur.size() == 2 * n) { result.push_back(cur); return; }
            if (open < n) { cur += '('; backtrack(cur, open+1, close); cur.pop_back(); }
            if (close < open) { cur += ')'; backtrack(cur, open, close+1); cur.pop_back(); }
        };
        string s;
        backtrack(s, 0, 0);
        return result;
    }
};""",
"java": """class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(result, new StringBuilder(), 0, 0, n);
        return result;
    }
    void backtrack(List<String> res, StringBuilder sb, int open, int close, int n) {
        if (sb.length() == 2 * n) { res.add(sb.toString()); return; }
        if (open < n) { sb.append('('); backtrack(res, sb, open+1, close, n); sb.deleteCharAt(sb.length()-1); }
        if (close < open) { sb.append(')'); backtrack(res, sb, open, close+1, n); sb.deleteCharAt(sb.length()-1); }
    }
}""",
"js": """var generateParenthesis = function(n) {
    const result = [];
    const backtrack = (cur, open, close) => {
        if (cur.length === 2 * n) { result.push(cur); return; }
        if (open < n) backtrack(cur + '(', open + 1, close);
        if (close < open) backtrack(cur + ')', open, close + 1);
    };
    backtrack('', 0, 0);
    return result;
};"""
}

solutions["739"] = {
"cpp": """class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> result(n, 0);
        stack<int> st;
        for (int i = 0; i < n; i++) {
            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {
                result[st.top()] = i - st.top();
                st.pop();
            }
            st.push(i);
        }
        return result;
    }
};""",
"java": """class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()])
                result[stack.peek()] = i - stack.pop();
            stack.push(i);
        }
        return result;
    }
}""",
"js": """var dailyTemperatures = function(temperatures) {
    const n = temperatures.length, result = new Array(n).fill(0);
    const stack = [];
    for (let i = 0; i < n; i++) {
        while (stack.length && temperatures[i] > temperatures[stack[stack.length-1]]) {
            const j = stack.pop();
            result[j] = i - j;
        }
        stack.push(i);
    }
    return result;
};"""
}

solutions["853"] = {
"cpp": """class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        vector<pair<int,double>> cars(n);
        for (int i = 0; i < n; i++)
            cars[i] = {position[i], (double)(target - position[i]) / speed[i]};
        sort(cars.begin(), cars.end());
        int fleets = 0;
        double curTime = 0;
        for (int i = n - 1; i >= 0; i--) {
            if (cars[i].second > curTime) {
                fleets++;
                curTime = cars[i].second;
            }
        }
        return fleets;
    }
};""",
"java": """class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        double[][] cars = new double[n][2];
        for (int i = 0; i < n; i++)
            cars[i] = new double[]{position[i], (double)(target - position[i]) / speed[i]};
        Arrays.sort(cars, (a, b) -> Double.compare(b[0], a[0]));
        int fleets = 0;
        double curTime = 0;
        for (double[] car : cars) {
            if (car[1] > curTime) { fleets++; curTime = car[1]; }
        }
        return fleets;
    }
}""",
"js": """var carFleet = function(target, position, speed) {
    const cars = position.map((p, i) => [p, (target - p) / speed[i]])
        .sort((a, b) => b[0] - a[0]);
    let fleets = 0, curTime = 0;
    for (const [_, time] of cars) {
        if (time > curTime) { fleets++; curTime = time; }
    }
    return fleets;
};"""
}

solutions["84"] = {
"cpp": """class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        stack<int> st;
        int maxArea = 0, n = heights.size();
        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!st.empty() && h < heights[st.top()]) {
                int height = heights[st.top()]; st.pop();
                int width = st.empty() ? i : i - st.top() - 1;
                maxArea = max(maxArea, height * width);
            }
            st.push(i);
        }
        return maxArea;
    }
};""",
"java": """class Solution {
    public int largestRectangleArea(int[] heights) {
        Stack<Integer> stack = new Stack<>();
        int maxArea = 0, n = heights.length;
        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && h < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }
}""",
"js": """var largestRectangleArea = function(heights) {
    const stack = [];
    let maxArea = 0;
    const n = heights.length;
    for (let i = 0; i <= n; i++) {
        const h = i === n ? 0 : heights[i];
        while (stack.length && h < heights[stack[stack.length-1]]) {
            const height = heights[stack.pop()];
            const width = stack.length ? i - stack[stack.length-1] - 1 : i;
            maxArea = Math.max(maxArea, height * width);
        }
        stack.push(i);
    }
    return maxArea;
};"""
}


# ============================================
# BINARY SEARCH
# ============================================

solutions["704"] = {
"cpp": """class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (nums[m] == target) return m;
            else if (nums[m] < target) l = m + 1;
            else r = m - 1;
        }
        return -1;
    }
};""",
"java": """class Solution {
    public int search(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (nums[m] == target) return m;
            else if (nums[m] < target) l = m + 1;
            else r = m - 1;
        }
        return -1;
    }
}""",
"js": """var search = function(nums, target) {
    let l = 0, r = nums.length - 1;
    while (l <= r) {
        const m = Math.floor((l + r) / 2);
        if (nums[m] === target) return m;
        else if (nums[m] < target) l = m + 1;
        else r = m - 1;
    }
    return -1;
};"""
}

solutions["74"] = {
"cpp": """class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int m = matrix.size(), n = matrix[0].size();
        int l = 0, r = m * n - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            int val = matrix[mid / n][mid % n];
            if (val == target) return true;
            else if (val < target) l = mid + 1;
            else r = mid - 1;
        }
        return false;
    }
};""",
"java": """class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int l = 0, r = m * n - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            int val = matrix[mid / n][mid % n];
            if (val == target) return true;
            else if (val < target) l = mid + 1;
            else r = mid - 1;
        }
        return false;
    }
}""",
"js": """var searchMatrix = function(matrix, target) {
    const m = matrix.length, n = matrix[0].length;
    let l = 0, r = m * n - 1;
    while (l <= r) {
        const mid = Math.floor((l + r) / 2);
        const val = matrix[Math.floor(mid / n)][mid % n];
        if (val === target) return true;
        else if (val < target) l = mid + 1;
        else r = mid - 1;
    }
    return false;
};"""
}

solutions["875"] = {
"cpp": """class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int l = 1, r = *max_element(piles.begin(), piles.end());
        while (l < r) {
            int m = l + (r - l) / 2;
            long hours = 0;
            for (int p : piles) hours += (p + m - 1) / m;
            if (hours <= h) r = m;
            else l = m + 1;
        }
        return l;
    }
};""",
"java": """class Solution {
    public int minEatingSpeed(int[] piles, int h) {
        int l = 1, r = Arrays.stream(piles).max().getAsInt();
        while (l < r) {
            int m = l + (r - l) / 2;
            long hours = 0;
            for (int p : piles) hours += (p + m - 1) / m;
            if (hours <= h) r = m;
            else l = m + 1;
        }
        return l;
    }
}""",
"js": """var minEatingSpeed = function(piles, h) {
    let l = 1, r = Math.max(...piles);
    while (l < r) {
        const m = Math.floor((l + r) / 2);
        const hours = piles.reduce((sum, p) => sum + Math.ceil(p / m), 0);
        if (hours <= h) r = m;
        else l = m + 1;
    }
    return l;
};"""
}

solutions["33"] = {
"cpp": """class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0, r = nums.size() - 1;
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (nums[m] == target) return m;
            if (nums[l] <= nums[m]) {
                if (nums[l] <= target && target < nums[m]) r = m - 1;
                else l = m + 1;
            } else {
                if (nums[m] < target && target <= nums[r]) l = m + 1;
                else r = m - 1;
            }
        }
        return -1;
    }
};""",
"java": """class Solution {
    public int search(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (nums[m] == target) return m;
            if (nums[l] <= nums[m]) {
                if (nums[l] <= target && target < nums[m]) r = m - 1;
                else l = m + 1;
            } else {
                if (nums[m] < target && target <= nums[r]) l = m + 1;
                else r = m - 1;
            }
        }
        return -1;
    }
}""",
"js": """var search = function(nums, target) {
    let l = 0, r = nums.length - 1;
    while (l <= r) {
        const m = Math.floor((l + r) / 2);
        if (nums[m] === target) return m;
        if (nums[l] <= nums[m]) {
            if (nums[l] <= target && target < nums[m]) r = m - 1;
            else l = m + 1;
        } else {
            if (nums[m] < target && target <= nums[r]) l = m + 1;
            else r = m - 1;
        }
    }
    return -1;
};"""
}

solutions["153"] = {
"cpp": """class Solution {
public:
    int findMin(vector<int>& nums) {
        int l = 0, r = nums.size() - 1;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] > nums[r]) l = m + 1;
            else r = m;
        }
        return nums[l];
    }
};""",
"java": """class Solution {
    public int findMin(int[] nums) {
        int l = 0, r = nums.length - 1;
        while (l < r) {
            int m = l + (r - l) / 2;
            if (nums[m] > nums[r]) l = m + 1;
            else r = m;
        }
        return nums[l];
    }
}""",
"js": """var findMin = function(nums) {
    let l = 0, r = nums.length - 1;
    while (l < r) {
        const m = Math.floor((l + r) / 2);
        if (nums[m] > nums[r]) l = m + 1;
        else r = m;
    }
    return nums[l];
};"""
}

solutions["981"] = {
"cpp": """class TimeMap {
    unordered_map<string, vector<pair<int, string>>> store;
public:
    void set(string key, string value, int timestamp) {
        store[key].push_back({timestamp, value});
    }
    string get(string key, int timestamp) {
        auto& arr = store[key];
        int l = 0, r = arr.size() - 1;
        string result = "";
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (arr[m].first <= timestamp) { result = arr[m].second; l = m + 1; }
            else r = m - 1;
        }
        return result;
    }
};""",
"java": """class TimeMap {
    Map<String, List<int[]>> store = new HashMap<>();
    Map<String, List<String>> vals = new HashMap<>();
    public void set(String key, String value, int timestamp) {
        store.computeIfAbsent(key, k -> new ArrayList<>()).add(new int[]{timestamp});
        vals.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    }
    public String get(String key, int timestamp) {
        if (!store.containsKey(key)) return "";
        List<int[]> times = store.get(key);
        List<String> values = vals.get(key);
        int l = 0, r = times.size() - 1;
        String result = "";
        while (l <= r) {
            int m = l + (r - l) / 2;
            if (times.get(m)[0] <= timestamp) { result = values.get(m); l = m + 1; }
            else r = m - 1;
        }
        return result;
    }
}""",
"js": """var TimeMap = function() { this.store = new Map(); };
TimeMap.prototype.set = function(key, value, timestamp) {
    if (!this.store.has(key)) this.store.set(key, []);
    this.store.get(key).push([timestamp, value]);
};
TimeMap.prototype.get = function(key, timestamp) {
    const arr = this.store.get(key) || [];
    let l = 0, r = arr.length - 1, result = '';
    while (l <= r) {
        const m = Math.floor((l + r) / 2);
        if (arr[m][0] <= timestamp) { result = arr[m][1]; l = m + 1; }
        else r = m - 1;
    }
    return result;
};"""
}

solutions["4"] = {
"cpp": """class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        if (nums1.size() > nums2.size()) swap(nums1, nums2);
        int m = nums1.size(), n = nums2.size(), half = (m + n + 1) / 2;
        int l = 0, r = m;
        while (l <= r) {
            int i = (l + r) / 2, j = half - i;
            int left1 = i > 0 ? nums1[i-1] : INT_MIN;
            int right1 = i < m ? nums1[i] : INT_MAX;
            int left2 = j > 0 ? nums2[j-1] : INT_MIN;
            int right2 = j < n ? nums2[j] : INT_MAX;
            if (left1 <= right2 && left2 <= right1) {
                if ((m + n) % 2) return max(left1, left2);
                return (max(left1, left2) + min(right1, right2)) / 2.0;
            } else if (left1 > right2) r = i - 1;
            else l = i + 1;
        }
        return 0;
    }
};""",
"java": """class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int m = nums1.length, n = nums2.length, half = (m + n + 1) / 2;
        int l = 0, r = m;
        while (l <= r) {
            int i = (l + r) / 2, j = half - i;
            int left1 = i > 0 ? nums1[i-1] : Integer.MIN_VALUE;
            int right1 = i < m ? nums1[i] : Integer.MAX_VALUE;
            int left2 = j > 0 ? nums2[j-1] : Integer.MIN_VALUE;
            int right2 = j < n ? nums2[j] : Integer.MAX_VALUE;
            if (left1 <= right2 && left2 <= right1) {
                if ((m + n) % 2 == 1) return Math.max(left1, left2);
                return (Math.max(left1, left2) + Math.min(right1, right2)) / 2.0;
            } else if (left1 > right2) r = i - 1;
            else l = i + 1;
        }
        return 0;
    }
}""",
"js": """var findMedianSortedArrays = function(nums1, nums2) {
    if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
    const m = nums1.length, n = nums2.length, half = Math.floor((m + n + 1) / 2);
    let l = 0, r = m;
    while (l <= r) {
        const i = Math.floor((l + r) / 2), j = half - i;
        const left1 = i > 0 ? nums1[i-1] : -Infinity;
        const right1 = i < m ? nums1[i] : Infinity;
        const left2 = j > 0 ? nums2[j-1] : -Infinity;
        const right2 = j < n ? nums2[j] : Infinity;
        if (left1 <= right2 && left2 <= right1) {
            if ((m + n) % 2) return Math.max(left1, left2);
            return (Math.max(left1, left2) + Math.min(right1, right2)) / 2;
        } else if (left1 > right2) r = i - 1;
        else l = i + 1;
    }
};"""
}

# ============================================
# LINKED LIST
# ============================================

solutions["206"] = {
"cpp": """class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        while (head) {
            ListNode* next = head->next;
            head->next = prev;
            prev = head;
            head = next;
        }
        return prev;
    }
};""",
"java": """class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        while (head != null) {
            ListNode next = head.next;
            head.next = prev;
            prev = head;
            head = next;
        }
        return prev;
    }
}""",
"js": """var reverseList = function(head) {
    let prev = null;
    while (head) {
        const next = head.next;
        head.next = prev;
        prev = head;
        head = next;
    }
    return prev;
};"""
}

solutions["21"] = {
"cpp": """class Solution {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode dummy(0), *cur = &dummy;
        while (l1 && l2) {
            if (l1->val <= l2->val) { cur->next = l1; l1 = l1->next; }
            else { cur->next = l2; l2 = l2->next; }
            cur = cur->next;
        }
        cur->next = l1 ? l1 : l2;
        return dummy.next;
    }
};""",
"java": """class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
            else { cur.next = l2; l2 = l2.next; }
            cur = cur.next;
        }
        cur.next = l1 != null ? l1 : l2;
        return dummy.next;
    }
}""",
"js": """var mergeTwoLists = function(l1, l2) {
    const dummy = new ListNode(0);
    let cur = dummy;
    while (l1 && l2) {
        if (l1.val <= l2.val) { cur.next = l1; l1 = l1.next; }
        else { cur.next = l2; l2 = l2.next; }
        cur = cur.next;
    }
    cur.next = l1 || l2;
    return dummy.next;
};"""
}

solutions["143"] = {
"cpp": """class Solution {
public:
    void reorderList(ListNode* head) {
        if (!head || !head->next) return;
        // Find middle
        ListNode *slow = head, *fast = head;
        while (fast->next && fast->next->next) { slow = slow->next; fast = fast->next->next; }
        // Reverse second half
        ListNode *prev = nullptr, *cur = slow->next;
        slow->next = nullptr;
        while (cur) { ListNode* next = cur->next; cur->next = prev; prev = cur; cur = next; }
        // Merge
        ListNode *l1 = head, *l2 = prev;
        while (l2) {
            ListNode *n1 = l1->next, *n2 = l2->next;
            l1->next = l2; l2->next = n1;
            l1 = n1; l2 = n2;
        }
    }
};""",
"java": """class Solution {
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) return;
        ListNode slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) { slow = slow.next; fast = fast.next.next; }
        ListNode prev = null, cur = slow.next;
        slow.next = null;
        while (cur != null) { ListNode next = cur.next; cur.next = prev; prev = cur; cur = next; }
        ListNode l1 = head, l2 = prev;
        while (l2 != null) {
            ListNode n1 = l1.next, n2 = l2.next;
            l1.next = l2; l2.next = n1;
            l1 = n1; l2 = n2;
        }
    }
}""",
"js": """var reorderList = function(head) {
    if (!head || !head.next) return;
    let slow = head, fast = head;
    while (fast.next && fast.next.next) { slow = slow.next; fast = fast.next.next; }
    let prev = null, cur = slow.next;
    slow.next = null;
    while (cur) { const next = cur.next; cur.next = prev; prev = cur; cur = next; }
    let l1 = head, l2 = prev;
    while (l2) {
        const n1 = l1.next, n2 = l2.next;
        l1.next = l2; l2.next = n1;
        l1 = n1; l2 = n2;
    }
};"""
}

solutions["19"] = {
"cpp": """class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0, head);
        ListNode *fast = &dummy, *slow = &dummy;
        for (int i = 0; i <= n; i++) fast = fast->next;
        while (fast) { slow = slow->next; fast = fast->next; }
        ListNode* del = slow->next;
        slow->next = slow->next->next;
        delete del;
        return dummy.next;
    }
};""",
"java": """class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0, head);
        ListNode fast = dummy, slow = dummy;
        for (int i = 0; i <= n; i++) fast = fast.next;
        while (fast != null) { slow = slow.next; fast = fast.next; }
        slow.next = slow.next.next;
        return dummy.next;
    }
}""",
"js": """var removeNthFromEnd = function(head, n) {
    const dummy = new ListNode(0, head);
    let fast = dummy, slow = dummy;
    for (let i = 0; i <= n; i++) fast = fast.next;
    while (fast) { slow = slow.next; fast = fast.next; }
    slow.next = slow.next.next;
    return dummy.next;
};"""
}

solutions["138"] = {
"cpp": """class Solution {
public:
    Node* copyRandomList(Node* head) {
        unordered_map<Node*, Node*> map;
        Node* cur = head;
        while (cur) { map[cur] = new Node(cur->val); cur = cur->next; }
        cur = head;
        while (cur) {
            map[cur]->next = map[cur->next];
            map[cur]->random = map[cur->random];
            cur = cur->next;
        }
        return map[head];
    }
};""",
"java": """class Solution {
    public Node copyRandomList(Node head) {
        Map<Node, Node> map = new HashMap<>();
        Node cur = head;
        while (cur != null) { map.put(cur, new Node(cur.val)); cur = cur.next; }
        cur = head;
        while (cur != null) {
            map.get(cur).next = map.get(cur.next);
            map.get(cur).random = map.get(cur.random);
            cur = cur.next;
        }
        return map.get(head);
    }
}""",
"js": """var copyRandomList = function(head) {
    const map = new Map();
    let cur = head;
    while (cur) { map.set(cur, new Node(cur.val)); cur = cur.next; }
    cur = head;
    while (cur) {
        map.get(cur).next = map.get(cur.next) || null;
        map.get(cur).random = map.get(cur.random) || null;
        cur = cur.next;
    }
    return map.get(head);
};"""
}

solutions["2"] = {
"cpp": """class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode dummy(0), *cur = &dummy;
        int carry = 0;
        while (l1 || l2 || carry) {
            int sum = carry + (l1 ? l1->val : 0) + (l2 ? l2->val : 0);
            carry = sum / 10;
            cur->next = new ListNode(sum % 10);
            cur = cur->next;
            if (l1) l1 = l1->next;
            if (l2) l2 = l2->next;
        }
        return dummy.next;
    }
};""",
"java": """class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int sum = carry + (l1 != null ? l1.val : 0) + (l2 != null ? l2.val : 0);
            carry = sum / 10;
            cur.next = new ListNode(sum % 10);
            cur = cur.next;
            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }
        return dummy.next;
    }
}""",
"js": """var addTwoNumbers = function(l1, l2) {
    const dummy = new ListNode(0);
    let cur = dummy, carry = 0;
    while (l1 || l2 || carry) {
        const sum = carry + (l1 ? l1.val : 0) + (l2 ? l2.val : 0);
        carry = Math.floor(sum / 10);
        cur.next = new ListNode(sum % 10);
        cur = cur.next;
        if (l1) l1 = l1.next;
        if (l2) l2 = l2.next;
    }
    return dummy.next;
};"""
}

solutions["141"] = {
"cpp": """class Solution {
public:
    bool hasCycle(ListNode *head) {
        ListNode *slow = head, *fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) return true;
        }
        return false;
    }
};""",
"java": """class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}""",
"js": """var hasCycle = function(head) {
    let slow = head, fast = head;
    while (fast && fast.next) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow === fast) return true;
    }
    return false;
};"""
}

solutions["287"] = {
"cpp": """class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0], fast = nums[0];
        do { slow = nums[slow]; fast = nums[nums[fast]]; } while (slow != fast);
        slow = nums[0];
        while (slow != fast) { slow = nums[slow]; fast = nums[fast]; }
        return slow;
    }
};""",
"java": """class Solution {
    public int findDuplicate(int[] nums) {
        int slow = nums[0], fast = nums[0];
        do { slow = nums[slow]; fast = nums[nums[fast]]; } while (slow != fast);
        slow = nums[0];
        while (slow != fast) { slow = nums[slow]; fast = nums[fast]; }
        return slow;
    }
}""",
"js": """var findDuplicate = function(nums) {
    let slow = nums[0], fast = nums[0];
    do { slow = nums[slow]; fast = nums[nums[fast]]; } while (slow !== fast);
    slow = nums[0];
    while (slow !== fast) { slow = nums[slow]; fast = nums[fast]; }
    return slow;
};"""
}

solutions["146"] = {
"cpp": """class LRUCache {
    int cap;
    list<pair<int,int>> cache;
    unordered_map<int, list<pair<int,int>>::iterator> map;
public:
    LRUCache(int capacity) : cap(capacity) {}
    int get(int key) {
        if (!map.count(key)) return -1;
        cache.splice(cache.begin(), cache, map[key]);
        return map[key]->second;
    }
    void put(int key, int value) {
        if (map.count(key)) {
            map[key]->second = value;
            cache.splice(cache.begin(), cache, map[key]);
        } else {
            if (cache.size() == cap) {
                map.erase(cache.back().first);
                cache.pop_back();
            }
            cache.push_front({key, value});
            map[key] = cache.begin();
        }
    }
};""",
"java": """class LRUCache extends LinkedHashMap<Integer, Integer> {
    private int capacity;
    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }
    public int get(int key) { return super.getOrDefault(key, -1); }
    public void put(int key, int value) { super.put(key, value); }
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > capacity;
    }
}""",
"js": """var LRUCache = function(capacity) {
    this.cap = capacity;
    this.cache = new Map();
};
LRUCache.prototype.get = function(key) {
    if (!this.cache.has(key)) return -1;
    const val = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, val);
    return val;
};
LRUCache.prototype.put = function(key, value) {
    this.cache.delete(key);
    this.cache.set(key, value);
    if (this.cache.size > this.cap) this.cache.delete(this.cache.keys().next().value);
};"""
}

solutions["23"] = {
"cpp": """class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
        for (auto* l : lists) if (l) pq.push(l);
        ListNode dummy(0), *cur = &dummy;
        while (!pq.empty()) {
            cur->next = pq.top(); pq.pop();
            cur = cur->next;
            if (cur->next) pq.push(cur->next);
        }
        return dummy.next;
    }
};""",
"java": """class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
        for (ListNode l : lists) if (l != null) pq.offer(l);
        ListNode dummy = new ListNode(0), cur = dummy;
        while (!pq.isEmpty()) {
            cur.next = pq.poll();
            cur = cur.next;
            if (cur.next != null) pq.offer(cur.next);
        }
        return dummy.next;
    }
}""",
"js": """var mergeKLists = function(lists) {
    // Simple approach: collect all values, sort, rebuild
    const vals = [];
    for (let l of lists) while (l) { vals.push(l.val); l = l.next; }
    vals.sort((a, b) => a - b);
    const dummy = new ListNode(0);
    let cur = dummy;
    for (const v of vals) { cur.next = new ListNode(v); cur = cur.next; }
    return dummy.next;
};"""
}

solutions["25"] = {
"cpp": """class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* cur = head;
        int count = 0;
        while (cur && count < k) { cur = cur->next; count++; }
        if (count < k) return head;
        ListNode* prev = reverseKGroup(cur, k);
        while (count-- > 0) {
            ListNode* next = head->next;
            head->next = prev;
            prev = head;
            head = next;
        }
        return prev;
    }
};""",
"java": """class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode cur = head;
        int count = 0;
        while (cur != null && count < k) { cur = cur.next; count++; }
        if (count < k) return head;
        ListNode prev = reverseKGroup(cur, k);
        while (count-- > 0) {
            ListNode next = head.next;
            head.next = prev;
            prev = head;
            head = next;
        }
        return prev;
    }
}""",
"js": """var reverseKGroup = function(head, k) {
    let cur = head, count = 0;
    while (cur && count < k) { cur = cur.next; count++; }
    if (count < k) return head;
    let prev = reverseKGroup(cur, k);
    while (count-- > 0) {
        const next = head.next;
        head.next = prev;
        prev = head;
        head = next;
    }
    return prev;
};"""
}


# ============================================
# TREES
# ============================================

solutions["226"] = {
"cpp": """class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (!root) return nullptr;
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};""",
"java": """class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        TreeNode tmp = root.left;
        root.left = invertTree(root.right);
        root.right = invertTree(tmp);
        return root;
    }
}""",
"js": """var invertTree = function(root) {
    if (!root) return null;
    [root.left, root.right] = [invertTree(root.right), invertTree(root.left)];
    return root;
};"""
}

solutions["104"] = {
"cpp": """class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root) return 0;
        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }
};""",
"java": """class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}""",
"js": """var maxDepth = function(root) {
    if (!root) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
};"""
}

solutions["543"] = {
"cpp": """class Solution {
    int result = 0;
    int dfs(TreeNode* node) {
        if (!node) return 0;
        int l = dfs(node->left), r = dfs(node->right);
        result = max(result, l + r);
        return 1 + max(l, r);
    }
public:
    int diameterOfBinaryTree(TreeNode* root) { dfs(root); return result; }
};""",
"java": """class Solution {
    int result = 0;
    public int diameterOfBinaryTree(TreeNode root) { dfs(root); return result; }
    int dfs(TreeNode node) {
        if (node == null) return 0;
        int l = dfs(node.left), r = dfs(node.right);
        result = Math.max(result, l + r);
        return 1 + Math.max(l, r);
    }
}""",
"js": """var diameterOfBinaryTree = function(root) {
    let result = 0;
    const dfs = (node) => {
        if (!node) return 0;
        const l = dfs(node.left), r = dfs(node.right);
        result = Math.max(result, l + r);
        return 1 + Math.max(l, r);
    };
    dfs(root);
    return result;
};"""
}

solutions["110"] = {
"cpp": """class Solution {
public:
    bool isBalanced(TreeNode* root) {
        return height(root) != -1;
    }
    int height(TreeNode* node) {
        if (!node) return 0;
        int l = height(node->left), r = height(node->right);
        if (l == -1 || r == -1 || abs(l - r) > 1) return -1;
        return 1 + max(l, r);
    }
};""",
"java": """class Solution {
    public boolean isBalanced(TreeNode root) { return height(root) != -1; }
    int height(TreeNode node) {
        if (node == null) return 0;
        int l = height(node.left), r = height(node.right);
        if (l == -1 || r == -1 || Math.abs(l - r) > 1) return -1;
        return 1 + Math.max(l, r);
    }
}""",
"js": """var isBalanced = function(root) {
    const height = (node) => {
        if (!node) return 0;
        const l = height(node.left), r = height(node.right);
        if (l === -1 || r === -1 || Math.abs(l - r) > 1) return -1;
        return 1 + Math.max(l, r);
    };
    return height(root) !== -1;
};"""
}

solutions["100"] = {
"cpp": """class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (!p && !q) return true;
        if (!p || !q || p->val != q->val) return false;
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};""",
"java": """class Solution {
    public boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null) return true;
        if (p == null || q == null || p.val != q.val) return false;
        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }
}""",
"js": """var isSameTree = function(p, q) {
    if (!p && !q) return true;
    if (!p || !q || p.val !== q.val) return false;
    return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
};"""
}

solutions["572"] = {
"cpp": """class Solution {
public:
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!root) return false;
        if (isSame(root, subRoot)) return true;
        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }
    bool isSame(TreeNode* a, TreeNode* b) {
        if (!a && !b) return true;
        if (!a || !b || a->val != b->val) return false;
        return isSame(a->left, b->left) && isSame(a->right, b->right);
    }
};""",
"java": """class Solution {
    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        if (root == null) return false;
        if (isSame(root, subRoot)) return true;
        return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
    }
    boolean isSame(TreeNode a, TreeNode b) {
        if (a == null && b == null) return true;
        if (a == null || b == null || a.val != b.val) return false;
        return isSame(a.left, b.left) && isSame(a.right, b.right);
    }
}""",
"js": """var isSubtree = function(root, subRoot) {
    if (!root) return false;
    const isSame = (a, b) => {
        if (!a && !b) return true;
        if (!a || !b || a.val !== b.val) return false;
        return isSame(a.left, b.left) && isSame(a.right, b.right);
    };
    if (isSame(root, subRoot)) return true;
    return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
};"""
}

solutions["235"] = {
"cpp": """class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        while (root) {
            if (p->val < root->val && q->val < root->val) root = root->left;
            else if (p->val > root->val && q->val > root->val) root = root->right;
            else return root;
        }
        return nullptr;
    }
};""",
"java": """class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        while (root != null) {
            if (p.val < root.val && q.val < root.val) root = root.left;
            else if (p.val > root.val && q.val > root.val) root = root.right;
            else return root;
        }
        return null;
    }
}""",
"js": """var lowestCommonAncestor = function(root, p, q) {
    while (root) {
        if (p.val < root.val && q.val < root.val) root = root.left;
        else if (p.val > root.val && q.val > root.val) root = root.right;
        else return root;
    }
};"""
}

solutions["102"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (!root) return result;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int sz = q.size();
            vector<int> level;
            while (sz--) {
                auto* node = q.front(); q.pop();
                level.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            result.push_back(level);
        }
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            int sz = q.size();
            List<Integer> level = new ArrayList<>();
            while (sz-- > 0) {
                TreeNode node = q.poll();
                level.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            result.add(level);
        }
        return result;
    }
}""",
"js": """var levelOrder = function(root) {
    if (!root) return [];
    const result = [], queue = [root];
    while (queue.length) {
        const level = [], sz = queue.length;
        for (let i = 0; i < sz; i++) {
            const node = queue.shift();
            level.push(node.val);
            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
        result.push(level);
    }
    return result;
};"""
}

solutions["199"] = {
"cpp": """class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> result;
        if (!root) return result;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                auto* node = q.front(); q.pop();
                if (i == sz - 1) result.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
        }
        return result;
    }
};""",
"java": """class Solution {
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                TreeNode node = q.poll();
                if (i == sz - 1) result.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
        }
        return result;
    }
}""",
"js": """var rightSideView = function(root) {
    if (!root) return [];
    const result = [], queue = [root];
    while (queue.length) {
        const sz = queue.length;
        for (let i = 0; i < sz; i++) {
            const node = queue.shift();
            if (i === sz - 1) result.push(node.val);
            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
    }
    return result;
};"""
}

solutions["1448"] = {
"cpp": """class Solution {
public:
    int goodNodes(TreeNode* root) {
        return dfs(root, root->val);
    }
    int dfs(TreeNode* node, int maxVal) {
        if (!node) return 0;
        int good = node->val >= maxVal ? 1 : 0;
        maxVal = max(maxVal, node->val);
        return good + dfs(node->left, maxVal) + dfs(node->right, maxVal);
    }
};""",
"java": """class Solution {
    public int goodNodes(TreeNode root) { return dfs(root, root.val); }
    int dfs(TreeNode node, int maxVal) {
        if (node == null) return 0;
        int good = node.val >= maxVal ? 1 : 0;
        maxVal = Math.max(maxVal, node.val);
        return good + dfs(node.left, maxVal) + dfs(node.right, maxVal);
    }
}""",
"js": """var goodNodes = function(root) {
    const dfs = (node, maxVal) => {
        if (!node) return 0;
        const good = node.val >= maxVal ? 1 : 0;
        const newMax = Math.max(maxVal, node.val);
        return good + dfs(node.left, newMax) + dfs(node.right, newMax);
    };
    return dfs(root, root.val);
};"""
}

solutions["98"] = {
"cpp": """class Solution {
public:
    bool isValidBST(TreeNode* root) {
        return validate(root, LONG_MIN, LONG_MAX);
    }
    bool validate(TreeNode* node, long lo, long hi) {
        if (!node) return true;
        if (node->val <= lo || node->val >= hi) return false;
        return validate(node->left, lo, node->val) && validate(node->right, node->val, hi);
    }
};""",
"java": """class Solution {
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    boolean validate(TreeNode node, long lo, long hi) {
        if (node == null) return true;
        if (node.val <= lo || node.val >= hi) return false;
        return validate(node.left, lo, node.val) && validate(node.right, node.val, hi);
    }
}""",
"js": """var isValidBST = function(root) {
    const validate = (node, lo, hi) => {
        if (!node) return true;
        if (node.val <= lo || node.val >= hi) return false;
        return validate(node.left, lo, node.val) && validate(node.right, node.val, hi);
    };
    return validate(root, -Infinity, Infinity);
};"""
}

solutions["230"] = {
"cpp": """class Solution {
public:
    int kthSmallest(TreeNode* root, int k) {
        stack<TreeNode*> st;
        while (root || !st.empty()) {
            while (root) { st.push(root); root = root->left; }
            root = st.top(); st.pop();
            if (--k == 0) return root->val;
            root = root->right;
        }
        return -1;
    }
};""",
"java": """class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Stack<TreeNode> stack = new Stack<>();
        while (root != null || !stack.isEmpty()) {
            while (root != null) { stack.push(root); root = root.left; }
            root = stack.pop();
            if (--k == 0) return root.val;
            root = root.right;
        }
        return -1;
    }
}""",
"js": """var kthSmallest = function(root, k) {
    const stack = [];
    while (root || stack.length) {
        while (root) { stack.push(root); root = root.left; }
        root = stack.pop();
        if (--k === 0) return root.val;
        root = root.right;
    }
};"""
}

solutions["105"] = {
"cpp": """class Solution {
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        unordered_map<int,int> map;
        for (int i = 0; i < inorder.size(); i++) map[inorder[i]] = i;
        int idx = 0;
        return build(preorder, map, idx, 0, inorder.size() - 1);
    }
    TreeNode* build(vector<int>& pre, unordered_map<int,int>& map, int& idx, int l, int r) {
        if (l > r) return nullptr;
        TreeNode* root = new TreeNode(pre[idx++]);
        int mid = map[root->val];
        root->left = build(pre, map, idx, l, mid - 1);
        root->right = build(pre, map, idx, mid + 1, r);
        return root;
    }
};""",
"java": """class Solution {
    int idx = 0;
    Map<Integer, Integer> map = new HashMap<>();
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        for (int i = 0; i < inorder.length; i++) map.put(inorder[i], i);
        return build(preorder, 0, inorder.length - 1);
    }
    TreeNode build(int[] pre, int l, int r) {
        if (l > r) return null;
        TreeNode root = new TreeNode(pre[idx++]);
        int mid = map.get(root.val);
        root.left = build(pre, l, mid - 1);
        root.right = build(pre, mid + 1, r);
        return root;
    }
}""",
"js": """var buildTree = function(preorder, inorder) {
    const map = new Map();
    inorder.forEach((v, i) => map.set(v, i));
    let idx = 0;
    const build = (l, r) => {
        if (l > r) return null;
        const root = new TreeNode(preorder[idx++]);
        const mid = map.get(root.val);
        root.left = build(l, mid - 1);
        root.right = build(mid + 1, r);
        return root;
    };
    return build(0, inorder.length - 1);
};"""
}

solutions["124"] = {
"cpp": """class Solution {
    int result = INT_MIN;
public:
    int maxPathSum(TreeNode* root) { dfs(root); return result; }
    int dfs(TreeNode* node) {
        if (!node) return 0;
        int l = max(0, dfs(node->left));
        int r = max(0, dfs(node->right));
        result = max(result, l + r + node->val);
        return max(l, r) + node->val;
    }
};""",
"java": """class Solution {
    int result = Integer.MIN_VALUE;
    public int maxPathSum(TreeNode root) { dfs(root); return result; }
    int dfs(TreeNode node) {
        if (node == null) return 0;
        int l = Math.max(0, dfs(node.left));
        int r = Math.max(0, dfs(node.right));
        result = Math.max(result, l + r + node.val);
        return Math.max(l, r) + node.val;
    }
}""",
"js": """var maxPathSum = function(root) {
    let result = -Infinity;
    const dfs = (node) => {
        if (!node) return 0;
        const l = Math.max(0, dfs(node.left));
        const r = Math.max(0, dfs(node.right));
        result = Math.max(result, l + r + node.val);
        return Math.max(l, r) + node.val;
    };
    dfs(root);
    return result;
};"""
}

solutions["297"] = {
"cpp": """class Codec {
public:
    string serialize(TreeNode* root) {
        if (!root) return "N";
        return to_string(root->val) + "," + serialize(root->left) + "," + serialize(root->right);
    }
    TreeNode* deserialize(string data) {
        queue<string> q;
        string token;
        istringstream ss(data);
        while (getline(ss, token, ',')) q.push(token);
        return build(q);
    }
    TreeNode* build(queue<string>& q) {
        string val = q.front(); q.pop();
        if (val == "N") return nullptr;
        TreeNode* node = new TreeNode(stoi(val));
        node->left = build(q);
        node->right = build(q);
        return node;
    }
};""",
"java": """public class Codec {
    public String serialize(TreeNode root) {
        if (root == null) return "N";
        return root.val + "," + serialize(root.left) + "," + serialize(root.right);
    }
    int idx = 0;
    public TreeNode deserialize(String data) {
        String[] tokens = data.split(",");
        idx = 0;
        return build(tokens);
    }
    TreeNode build(String[] tokens) {
        if (tokens[idx].equals("N")) { idx++; return null; }
        TreeNode node = new TreeNode(Integer.parseInt(tokens[idx++]));
        node.left = build(tokens);
        node.right = build(tokens);
        return node;
    }
}""",
"js": """var serialize = function(root) {
    if (!root) return 'N';
    return root.val + ',' + serialize(root.left) + ',' + serialize(root.right);
};
var deserialize = function(data) {
    const tokens = data.split(',');
    let idx = 0;
    const build = () => {
        if (tokens[idx] === 'N') { idx++; return null; }
        const node = new TreeNode(Number(tokens[idx++]));
        node.left = build();
        node.right = build();
        return node;
    };
    return build();
};"""
}


# ============================================
# TRIES
# ============================================

solutions["208"] = {
"cpp": """class Trie {
    struct TrieNode {
        TrieNode* children[26] = {};
        bool isEnd = false;
    };
    TrieNode* root = new TrieNode();
public:
    void insert(string word) {
        auto* node = root;
        for (char c : word) {
            if (!node->children[c-'a']) node->children[c-'a'] = new TrieNode();
            node = node->children[c-'a'];
        }
        node->isEnd = true;
    }
    bool search(string word) {
        auto* node = find(word);
        return node && node->isEnd;
    }
    bool startsWith(string prefix) {
        return find(prefix) != nullptr;
    }
    TrieNode* find(string& s) {
        auto* node = root;
        for (char c : s) {
            if (!node->children[c-'a']) return nullptr;
            node = node->children[c-'a'];
        }
        return node;
    }
};""",
"java": """class Trie {
    private Trie[] children = new Trie[26];
    private boolean isEnd = false;
    public void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            if (node.children[c-'a'] == null) node.children[c-'a'] = new Trie();
            node = node.children[c-'a'];
        }
        node.isEnd = true;
    }
    public boolean search(String word) {
        Trie node = find(word);
        return node != null && node.isEnd;
    }
    public boolean startsWith(String prefix) { return find(prefix) != null; }
    private Trie find(String s) {
        Trie node = this;
        for (char c : s.toCharArray()) {
            if (node.children[c-'a'] == null) return null;
            node = node.children[c-'a'];
        }
        return node;
    }
}""",
"js": """var Trie = function() { this.children = {}; this.isEnd = false; };
Trie.prototype.insert = function(word) {
    let node = this;
    for (const c of word) {
        if (!node.children[c]) node.children[c] = new Trie();
        node = node.children[c];
    }
    node.isEnd = true;
};
Trie.prototype.search = function(word) {
    const node = this._find(word);
    return node !== null && node.isEnd;
};
Trie.prototype.startsWith = function(prefix) { return this._find(prefix) !== null; };
Trie.prototype._find = function(s) {
    let node = this;
    for (const c of s) {
        if (!node.children[c]) return null;
        node = node.children[c];
    }
    return node;
};"""
}

solutions["211"] = {
"cpp": """class WordDictionary {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root = new Node();
public:
    void addWord(string word) {
        auto* node = root;
        for (char c : word) {
            if (!node->children[c-'a']) node->children[c-'a'] = new Node();
            node = node->children[c-'a'];
        }
        node->isEnd = true;
    }
    bool search(string word) { return dfs(word, 0, root); }
    bool dfs(string& word, int i, Node* node) {
        if (i == word.size()) return node->isEnd;
        if (word[i] == '.') {
            for (auto* ch : node->children)
                if (ch && dfs(word, i+1, ch)) return true;
            return false;
        }
        if (!node->children[word[i]-'a']) return false;
        return dfs(word, i+1, node->children[word[i]-'a']);
    }
};""",
"java": """class WordDictionary {
    WordDictionary[] children = new WordDictionary[26];
    boolean isEnd = false;
    public void addWord(String word) {
        WordDictionary node = this;
        for (char c : word.toCharArray()) {
            if (node.children[c-'a'] == null) node.children[c-'a'] = new WordDictionary();
            node = node.children[c-'a'];
        }
        node.isEnd = true;
    }
    public boolean search(String word) { return dfs(word, 0, this); }
    boolean dfs(String word, int i, WordDictionary node) {
        if (i == word.length()) return node.isEnd;
        if (word.charAt(i) == '.') {
            for (var ch : node.children) if (ch != null && dfs(word, i+1, ch)) return true;
            return false;
        }
        if (node.children[word.charAt(i)-'a'] == null) return false;
        return dfs(word, i+1, node.children[word.charAt(i)-'a']);
    }
}""",
"js": """var WordDictionary = function() { this.children = {}; this.isEnd = false; };
WordDictionary.prototype.addWord = function(word) {
    let node = this;
    for (const c of word) {
        if (!node.children[c]) node.children[c] = new WordDictionary();
        node = node.children[c];
    }
    node.isEnd = true;
};
WordDictionary.prototype.search = function(word) {
    const dfs = (i, node) => {
        if (i === word.length) return node.isEnd;
        if (word[i] === '.') {
            for (const ch of Object.values(node.children))
                if (dfs(i + 1, ch)) return true;
            return false;
        }
        if (!node.children[word[i]]) return false;
        return dfs(i + 1, node.children[word[i]]);
    };
    return dfs(0, this);
};"""
}

solutions["212"] = {
"cpp": """class Solution {
    struct TrieNode {
        TrieNode* children[26] = {};
        string word;
    };
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        TrieNode* root = new TrieNode();
        for (string& w : words) {
            auto* node = root;
            for (char c : w) {
                if (!node->children[c-'a']) node->children[c-'a'] = new TrieNode();
                node = node->children[c-'a'];
            }
            node->word = w;
        }
        vector<string> result;
        int m = board.size(), n = board[0].size();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                dfs(board, root, i, j, result);
        return result;
    }
    void dfs(vector<vector<char>>& board, TrieNode* node, int i, int j, vector<string>& result) {
        if (i < 0 || j < 0 || i >= board.size() || j >= board[0].size() || board[i][j] == '#') return;
        char c = board[i][j];
        if (!node->children[c-'a']) return;
        node = node->children[c-'a'];
        if (!node->word.empty()) { result.push_back(node->word); node->word.clear(); }
        board[i][j] = '#';
        dfs(board, node, i+1, j, result); dfs(board, node, i-1, j, result);
        dfs(board, node, i, j+1, result); dfs(board, node, i, j-1, result);
        board[i][j] = c;
    }
};""",
"java": """class Solution {
    class TrieNode { TrieNode[] ch = new TrieNode[26]; String word; }
    public List<String> findWords(char[][] board, String[] words) {
        TrieNode root = new TrieNode();
        for (String w : words) {
            TrieNode node = root;
            for (char c : w.toCharArray()) {
                if (node.ch[c-'a'] == null) node.ch[c-'a'] = new TrieNode();
                node = node.ch[c-'a'];
            }
            node.word = w;
        }
        List<String> result = new ArrayList<>();
        for (int i = 0; i < board.length; i++)
            for (int j = 0; j < board[0].length; j++)
                dfs(board, root, i, j, result);
        return result;
    }
    void dfs(char[][] board, TrieNode node, int i, int j, List<String> result) {
        if (i < 0 || j < 0 || i >= board.length || j >= board[0].length || board[i][j] == '#') return;
        char c = board[i][j];
        if (node.ch[c-'a'] == null) return;
        node = node.ch[c-'a'];
        if (node.word != null) { result.add(node.word); node.word = null; }
        board[i][j] = '#';
        dfs(board, node, i+1, j, result); dfs(board, node, i-1, j, result);
        dfs(board, node, i, j+1, result); dfs(board, node, i, j-1, result);
        board[i][j] = c;
    }
}""",
"js": """var findWords = function(board, words) {
    const root = {};
    for (const w of words) {
        let node = root;
        for (const c of w) { if (!node[c]) node[c] = {}; node = node[c]; }
        node.word = w;
    }
    const result = [], m = board.length, n = board[0].length;
    const dfs = (node, i, j) => {
        if (i < 0 || j < 0 || i >= m || j >= n || board[i][j] === '#') return;
        const c = board[i][j];
        if (!node[c]) return;
        node = node[c];
        if (node.word) { result.push(node.word); node.word = null; }
        board[i][j] = '#';
        dfs(node, i+1, j); dfs(node, i-1, j); dfs(node, i, j+1); dfs(node, i, j-1);
        board[i][j] = c;
    };
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) dfs(root, i, j);
    return result;
};"""
}

# ============================================
# HEAP / PRIORITY QUEUE
# ============================================

solutions["703"] = {
"cpp": """class KthLargest {
    priority_queue<int, vector<int>, greater<int>> pq;
    int k;
public:
    KthLargest(int k, vector<int>& nums) : k(k) {
        for (int n : nums) add(n);
    }
    int add(int val) {
        pq.push(val);
        if (pq.size() > k) pq.pop();
        return pq.top();
    }
};""",
"java": """class KthLargest {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    int k;
    public KthLargest(int k, int[] nums) {
        this.k = k;
        for (int n : nums) add(n);
    }
    public int add(int val) {
        pq.offer(val);
        if (pq.size() > k) pq.poll();
        return pq.peek();
    }
}""",
"js": """var KthLargest = function(k, nums) {
    this.k = k;
    this.nums = nums.sort((a, b) => a - b);
    while (this.nums.length > k) this.nums.shift();
};
KthLargest.prototype.add = function(val) {
    // Binary insert
    let l = 0, r = this.nums.length;
    while (l < r) { const m = (l + r) >> 1; this.nums[m] < val ? l = m + 1 : r = m; }
    this.nums.splice(l, 0, val);
    if (this.nums.length > this.k) this.nums.shift();
    return this.nums[0];
};"""
}

solutions["1046"] = {
"cpp": """class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        priority_queue<int> pq(stones.begin(), stones.end());
        while (pq.size() > 1) {
            int a = pq.top(); pq.pop();
            int b = pq.top(); pq.pop();
            if (a != b) pq.push(a - b);
        }
        return pq.empty() ? 0 : pq.top();
    }
};""",
"java": """class Solution {
    public int lastStoneWeight(int[] stones) {
        PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
        for (int s : stones) pq.offer(s);
        while (pq.size() > 1) {
            int a = pq.poll(), b = pq.poll();
            if (a != b) pq.offer(a - b);
        }
        return pq.isEmpty() ? 0 : pq.peek();
    }
}""",
"js": """var lastStoneWeight = function(stones) {
    while (stones.length > 1) {
        stones.sort((a, b) => b - a);
        const a = stones.shift(), b = stones.shift();
        if (a !== b) stones.push(a - b);
    }
    return stones.length ? stones[0] : 0;
};"""
}

solutions["973"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
        sort(points.begin(), points.end(), [](auto& a, auto& b) {
            return a[0]*a[0] + a[1]*a[1] < b[0]*b[0] + b[1]*b[1];
        });
        points.resize(k);
        return points;
    }
};""",
"java": """class Solution {
    public int[][] kClosest(int[][] points, int k) {
        Arrays.sort(points, (a, b) -> a[0]*a[0] + a[1]*a[1] - b[0]*b[0] - b[1]*b[1]);
        return Arrays.copyOf(points, k);
    }
}""",
"js": """var kClosest = function(points, k) {
    return points.sort((a, b) => a[0]*a[0] + a[1]*a[1] - b[0]*b[0] - b[1]*b[1]).slice(0, k);
};"""
}

solutions["215"] = {
"cpp": """class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int>> pq;
        for (int n : nums) {
            pq.push(n);
            if (pq.size() > k) pq.pop();
        }
        return pq.top();
    }
};""",
"java": """class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        for (int n : nums) {
            pq.offer(n);
            if (pq.size() > k) pq.poll();
        }
        return pq.peek();
    }
}""",
"js": """var findKthLargest = function(nums, k) {
    nums.sort((a, b) => b - a);
    return nums[k - 1];
};"""
}

solutions["621"] = {
"cpp": """class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        int freq[26] = {};
        for (char c : tasks) freq[c - 'A']++;
        int maxFreq = *max_element(freq, freq + 26);
        int maxCount = count(freq, freq + 26, maxFreq);
        return max((int)tasks.size(), (maxFreq - 1) * (n + 1) + maxCount);
    }
};""",
"java": """class Solution {
    public int leastInterval(char[] tasks, int n) {
        int[] freq = new int[26];
        for (char c : tasks) freq[c - 'A']++;
        int maxFreq = Arrays.stream(freq).max().getAsInt();
        int maxCount = (int) Arrays.stream(freq).filter(f -> f == maxFreq).count();
        return Math.max(tasks.length, (maxFreq - 1) * (n + 1) + maxCount);
    }
}""",
"js": """var leastInterval = function(tasks, n) {
    const freq = new Array(26).fill(0);
    for (const c of tasks) freq[c.charCodeAt(0) - 65]++;
    const maxFreq = Math.max(...freq);
    const maxCount = freq.filter(f => f === maxFreq).length;
    return Math.max(tasks.length, (maxFreq - 1) * (n + 1) + maxCount);
};"""
}

solutions["355"] = {
"cpp": """class Twitter {
    int time = 0;
    unordered_map<int, unordered_set<int>> follows;
    unordered_map<int, vector<pair<int,int>>> tweets; // userId -> [{time, tweetId}]
public:
    void postTweet(int userId, int tweetId) { tweets[userId].push_back({time++, tweetId}); }
    vector<int> getNewsFeed(int userId) {
        auto cmp = [](auto& a, auto& b) { return a.first < b.first; };
        priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> pq(cmp);
        follows[userId].insert(userId);
        for (int uid : follows[userId])
            for (auto& t : tweets[uid]) pq.push(t);
        vector<int> result;
        while (!pq.empty() && result.size() < 10) { result.push_back(pq.top().second); pq.pop(); }
        return result;
    }
    void follow(int followerId, int followeeId) { follows[followerId].insert(followeeId); }
    void unfollow(int followerId, int followeeId) { follows[followerId].erase(followeeId); }
};""",
"java": """class Twitter {
    int time = 0;
    Map<Integer, Set<Integer>> follows = new HashMap<>();
    Map<Integer, List<int[]>> tweets = new HashMap<>();
    public void postTweet(int userId, int tweetId) {
        tweets.computeIfAbsent(userId, k -> new ArrayList<>()).add(new int[]{time++, tweetId});
    }
    public List<Integer> getNewsFeed(int userId) {
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[0] - a[0]);
        Set<Integer> users = follows.computeIfAbsent(userId, k -> new HashSet<>());
        users.add(userId);
        for (int uid : users)
            if (tweets.containsKey(uid)) for (int[] t : tweets.get(uid)) pq.offer(t);
        List<Integer> result = new ArrayList<>();
        while (!pq.isEmpty() && result.size() < 10) result.add(pq.poll()[1]);
        return result;
    }
    public void follow(int followerId, int followeeId) {
        follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);
    }
    public void unfollow(int followerId, int followeeId) {
        if (follows.containsKey(followerId)) follows.get(followerId).remove(followeeId);
    }
}""",
"js": """var Twitter = function() { this.time = 0; this.tweets = new Map(); this.follows = new Map(); };
Twitter.prototype.postTweet = function(userId, tweetId) {
    if (!this.tweets.has(userId)) this.tweets.set(userId, []);
    this.tweets.get(userId).push([this.time++, tweetId]);
};
Twitter.prototype.getNewsFeed = function(userId) {
    const users = this.follows.get(userId) || new Set();
    users.add(userId);
    const all = [];
    for (const uid of users)
        if (this.tweets.has(uid)) all.push(...this.tweets.get(uid));
    all.sort((a, b) => b[0] - a[0]);
    return all.slice(0, 10).map(t => t[1]);
};
Twitter.prototype.follow = function(ferId, feeId) {
    if (!this.follows.has(ferId)) this.follows.set(ferId, new Set());
    this.follows.get(ferId).add(feeId);
};
Twitter.prototype.unfollow = function(ferId, feeId) {
    if (this.follows.has(ferId)) this.follows.get(ferId).delete(feeId);
};"""
}

solutions["295"] = {
"cpp": """class MedianFinder {
    priority_queue<int> lo; // max heap
    priority_queue<int, vector<int>, greater<int>> hi; // min heap
public:
    void addNum(int num) {
        lo.push(num);
        hi.push(lo.top()); lo.pop();
        if (hi.size() > lo.size()) { lo.push(hi.top()); hi.pop(); }
    }
    double findMedian() {
        return lo.size() > hi.size() ? lo.top() : (lo.top() + hi.top()) / 2.0;
    }
};""",
"java": """class MedianFinder {
    PriorityQueue<Integer> lo = new PriorityQueue<>(Collections.reverseOrder());
    PriorityQueue<Integer> hi = new PriorityQueue<>();
    public void addNum(int num) {
        lo.offer(num);
        hi.offer(lo.poll());
        if (hi.size() > lo.size()) lo.offer(hi.poll());
    }
    public double findMedian() {
        return lo.size() > hi.size() ? lo.peek() : (lo.peek() + hi.peek()) / 2.0;
    }
}""",
"js": """var MedianFinder = function() { this.lo = []; this.hi = []; }; // simplified with sorted arrays
MedianFinder.prototype.addNum = function(num) {
    // Insert into sorted lo (descending) or hi (ascending)
    const insert = (arr, val, cmp) => {
        let l = 0, r = arr.length;
        while (l < r) { const m = (l + r) >> 1; cmp(arr[m], val) ? l = m + 1 : r = m; }
        arr.splice(l, 0, val);
    };
    insert(this.lo, num, (a, b) => a > b);
    this.hi.push(this.lo.shift());
    this.hi.sort((a, b) => a - b);
    if (this.hi.length > this.lo.length) this.lo.unshift(this.hi.shift());
};
MedianFinder.prototype.findMedian = function() {
    return this.lo.length > this.hi.length ? this.lo[0] : (this.lo[0] + this.hi[0]) / 2;
};"""
}


# ============================================
# BACKTRACKING
# ============================================

solutions["78"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> cur;
        function<void(int)> bt = [&](int i) {
            result.push_back(cur);
            for (int j = i; j < nums.size(); j++) {
                cur.push_back(nums[j]);
                bt(j + 1);
                cur.pop_back();
            }
        };
        bt(0);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }
    void backtrack(int[] nums, int i, List<Integer> cur, List<List<Integer>> result) {
        result.add(new ArrayList<>(cur));
        for (int j = i; j < nums.length; j++) {
            cur.add(nums[j]);
            backtrack(nums, j + 1, cur, result);
            cur.remove(cur.size() - 1);
        }
    }
}""",
"js": """var subsets = function(nums) {
    const result = [];
    const bt = (i, cur) => {
        result.push([...cur]);
        for (let j = i; j < nums.length; j++) {
            cur.push(nums[j]);
            bt(j + 1, cur);
            cur.pop();
        }
    };
    bt(0, []);
    return result;
};"""
}

solutions["39"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> result;
        vector<int> cur;
        function<void(int, int)> bt = [&](int i, int remain) {
            if (remain == 0) { result.push_back(cur); return; }
            if (remain < 0 || i >= candidates.size()) return;
            cur.push_back(candidates[i]);
            bt(i, remain - candidates[i]);
            cur.pop_back();
            bt(i + 1, remain);
        };
        bt(0, target);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(candidates, target, 0, new ArrayList<>(), result);
        return result;
    }
    void backtrack(int[] cands, int remain, int i, List<Integer> cur, List<List<Integer>> result) {
        if (remain == 0) { result.add(new ArrayList<>(cur)); return; }
        if (remain < 0 || i >= cands.length) return;
        cur.add(cands[i]);
        backtrack(cands, remain - cands[i], i, cur, result);
        cur.remove(cur.size() - 1);
        backtrack(cands, remain, i + 1, cur, result);
    }
}""",
"js": """var combinationSum = function(candidates, target) {
    const result = [];
    const bt = (i, remain, cur) => {
        if (remain === 0) { result.push([...cur]); return; }
        if (remain < 0 || i >= candidates.length) return;
        cur.push(candidates[i]);
        bt(i, remain - candidates[i], cur);
        cur.pop();
        bt(i + 1, remain, cur);
    };
    bt(0, target, []);
    return result;
};"""
}

solutions["46"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> result;
        function<void(int)> bt = [&](int start) {
            if (start == nums.size()) { result.push_back(nums); return; }
            for (int i = start; i < nums.size(); i++) {
                swap(nums[start], nums[i]);
                bt(start + 1);
                swap(nums[start], nums[i]);
            }
        };
        bt(0);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, result);
        return result;
    }
    void backtrack(int[] nums, int start, List<List<Integer>> result) {
        if (start == nums.length) {
            List<Integer> perm = new ArrayList<>();
            for (int n : nums) perm.add(n);
            result.add(perm);
            return;
        }
        for (int i = start; i < nums.length; i++) {
            int tmp = nums[start]; nums[start] = nums[i]; nums[i] = tmp;
            backtrack(nums, start + 1, result);
            tmp = nums[start]; nums[start] = nums[i]; nums[i] = tmp;
        }
    }
}""",
"js": """var permute = function(nums) {
    const result = [];
    const bt = (start) => {
        if (start === nums.length) { result.push([...nums]); return; }
        for (let i = start; i < nums.length; i++) {
            [nums[start], nums[i]] = [nums[i], nums[start]];
            bt(start + 1);
            [nums[start], nums[i]] = [nums[i], nums[start]];
        }
    };
    bt(0);
    return result;
};"""
}

solutions["90"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        vector<vector<int>> result;
        vector<int> cur;
        function<void(int)> bt = [&](int i) {
            result.push_back(cur);
            for (int j = i; j < nums.size(); j++) {
                if (j > i && nums[j] == nums[j-1]) continue;
                cur.push_back(nums[j]);
                bt(j + 1);
                cur.pop_back();
            }
        };
        bt(0);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }
    void backtrack(int[] nums, int i, List<Integer> cur, List<List<Integer>> result) {
        result.add(new ArrayList<>(cur));
        for (int j = i; j < nums.length; j++) {
            if (j > i && nums[j] == nums[j-1]) continue;
            cur.add(nums[j]);
            backtrack(nums, j + 1, cur, result);
            cur.remove(cur.size() - 1);
        }
    }
}""",
"js": """var subsetsWithDup = function(nums) {
    nums.sort((a, b) => a - b);
    const result = [];
    const bt = (i, cur) => {
        result.push([...cur]);
        for (let j = i; j < nums.length; j++) {
            if (j > i && nums[j] === nums[j-1]) continue;
            cur.push(nums[j]);
            bt(j + 1, cur);
            cur.pop();
        }
    };
    bt(0, []);
    return result;
};"""
}

solutions["40"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        vector<vector<int>> result;
        vector<int> cur;
        function<void(int, int)> bt = [&](int i, int remain) {
            if (remain == 0) { result.push_back(cur); return; }
            for (int j = i; j < candidates.size() && candidates[j] <= remain; j++) {
                if (j > i && candidates[j] == candidates[j-1]) continue;
                cur.push_back(candidates[j]);
                bt(j + 1, remain - candidates[j]);
                cur.pop_back();
            }
        };
        bt(0, target);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> result = new ArrayList<>();
        backtrack(candidates, target, 0, new ArrayList<>(), result);
        return result;
    }
    void backtrack(int[] cands, int remain, int i, List<Integer> cur, List<List<Integer>> result) {
        if (remain == 0) { result.add(new ArrayList<>(cur)); return; }
        for (int j = i; j < cands.length && cands[j] <= remain; j++) {
            if (j > i && cands[j] == cands[j-1]) continue;
            cur.add(cands[j]);
            backtrack(cands, remain - cands[j], j + 1, cur, result);
            cur.remove(cur.size() - 1);
        }
    }
}""",
"js": """var combinationSum2 = function(candidates, target) {
    candidates.sort((a, b) => a - b);
    const result = [];
    const bt = (i, remain, cur) => {
        if (remain === 0) { result.push([...cur]); return; }
        for (let j = i; j < candidates.length && candidates[j] <= remain; j++) {
            if (j > i && candidates[j] === candidates[j-1]) continue;
            cur.push(candidates[j]);
            bt(j + 1, remain - candidates[j], cur);
            cur.pop();
        }
    };
    bt(0, target, []);
    return result;
};"""
}

solutions["79"] = {
"cpp": """class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        int m = board.size(), n = board[0].size();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (dfs(board, word, i, j, 0)) return true;
        return false;
    }
    bool dfs(vector<vector<char>>& board, string& word, int i, int j, int k) {
        if (k == word.size()) return true;
        if (i < 0 || j < 0 || i >= board.size() || j >= board[0].size() || board[i][j] != word[k]) return false;
        char tmp = board[i][j]; board[i][j] = '#';
        bool found = dfs(board, word, i+1, j, k+1) || dfs(board, word, i-1, j, k+1)
                  || dfs(board, word, i, j+1, k+1) || dfs(board, word, i, j-1, k+1);
        board[i][j] = tmp;
        return found;
    }
};""",
"java": """class Solution {
    public boolean exist(char[][] board, String word) {
        for (int i = 0; i < board.length; i++)
            for (int j = 0; j < board[0].length; j++)
                if (dfs(board, word, i, j, 0)) return true;
        return false;
    }
    boolean dfs(char[][] board, String word, int i, int j, int k) {
        if (k == word.length()) return true;
        if (i < 0 || j < 0 || i >= board.length || j >= board[0].length || board[i][j] != word.charAt(k)) return false;
        char tmp = board[i][j]; board[i][j] = '#';
        boolean found = dfs(board, word, i+1, j, k+1) || dfs(board, word, i-1, j, k+1)
                     || dfs(board, word, i, j+1, k+1) || dfs(board, word, i, j-1, k+1);
        board[i][j] = tmp;
        return found;
    }
}""",
"js": """var exist = function(board, word) {
    const m = board.length, n = board[0].length;
    const dfs = (i, j, k) => {
        if (k === word.length) return true;
        if (i < 0 || j < 0 || i >= m || j >= n || board[i][j] !== word[k]) return false;
        const tmp = board[i][j]; board[i][j] = '#';
        const found = dfs(i+1,j,k+1) || dfs(i-1,j,k+1) || dfs(i,j+1,k+1) || dfs(i,j-1,k+1);
        board[i][j] = tmp;
        return found;
    };
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++)
            if (dfs(i, j, 0)) return true;
    return false;
};"""
}

solutions["131"] = {
"cpp": """class Solution {
public:
    vector<vector<string>> partition(string s) {
        vector<vector<string>> result;
        vector<string> cur;
        function<void(int)> bt = [&](int start) {
            if (start == s.size()) { result.push_back(cur); return; }
            for (int end = start; end < s.size(); end++) {
                if (isPalin(s, start, end)) {
                    cur.push_back(s.substr(start, end - start + 1));
                    bt(end + 1);
                    cur.pop_back();
                }
            }
        };
        bt(0);
        return result;
    }
    bool isPalin(string& s, int l, int r) {
        while (l < r) if (s[l++] != s[r--]) return false;
        return true;
    }
};""",
"java": """class Solution {
    public List<List<String>> partition(String s) {
        List<List<String>> result = new ArrayList<>();
        backtrack(s, 0, new ArrayList<>(), result);
        return result;
    }
    void backtrack(String s, int start, List<String> cur, List<List<String>> result) {
        if (start == s.length()) { result.add(new ArrayList<>(cur)); return; }
        for (int end = start; end < s.length(); end++) {
            if (isPalin(s, start, end)) {
                cur.add(s.substring(start, end + 1));
                backtrack(s, end + 1, cur, result);
                cur.remove(cur.size() - 1);
            }
        }
    }
    boolean isPalin(String s, int l, int r) {
        while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
        return true;
    }
}""",
"js": """var partition = function(s) {
    const result = [];
    const isPalin = (l, r) => { while (l < r) if (s[l++] !== s[r--]) return false; return true; };
    const bt = (start, cur) => {
        if (start === s.length) { result.push([...cur]); return; }
        for (let end = start; end < s.length; end++) {
            if (isPalin(start, end)) {
                cur.push(s.substring(start, end + 1));
                bt(end + 1, cur);
                cur.pop();
            }
        }
    };
    bt(0, []);
    return result;
};"""
}

solutions["17"] = {
"cpp": """class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        string map[] = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
        vector<string> result;
        function<void(int, string&)> bt = [&](int i, string& cur) {
            if (i == digits.size()) { result.push_back(cur); return; }
            for (char c : map[digits[i] - '0']) {
                cur += c; bt(i + 1, cur); cur.pop_back();
            }
        };
        string s;
        bt(0, s);
        return result;
    }
};""",
"java": """class Solution {
    String[] map = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    public List<String> letterCombinations(String digits) {
        if (digits.isEmpty()) return new ArrayList<>();
        List<String> result = new ArrayList<>();
        backtrack(digits, 0, new StringBuilder(), result);
        return result;
    }
    void backtrack(String digits, int i, StringBuilder sb, List<String> result) {
        if (i == digits.length()) { result.add(sb.toString()); return; }
        for (char c : map[digits.charAt(i) - '0'].toCharArray()) {
            sb.append(c); backtrack(digits, i + 1, sb, result); sb.deleteCharAt(sb.length() - 1);
        }
    }
}""",
"js": """var letterCombinations = function(digits) {
    if (!digits.length) return [];
    const map = ['','','abc','def','ghi','jkl','mno','pqrs','tuv','wxyz'];
    const result = [];
    const bt = (i, cur) => {
        if (i === digits.length) { result.push(cur); return; }
        for (const c of map[digits[i]]) bt(i + 1, cur + c);
    };
    bt(0, '');
    return result;
};"""
}

solutions["51"] = {
"cpp": """class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> result;
        vector<string> board(n, string(n, '.'));
        unordered_set<int> cols, diag1, diag2;
        function<void(int)> bt = [&](int row) {
            if (row == n) { result.push_back(board); return; }
            for (int col = 0; col < n; col++) {
                if (cols.count(col) || diag1.count(row-col) || diag2.count(row+col)) continue;
                board[row][col] = 'Q';
                cols.insert(col); diag1.insert(row-col); diag2.insert(row+col);
                bt(row + 1);
                board[row][col] = '.';
                cols.erase(col); diag1.erase(row-col); diag2.erase(row+col);
            }
        };
        bt(0);
        return result;
    }
};""",
"java": """class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        Set<Integer> cols = new HashSet<>(), d1 = new HashSet<>(), d2 = new HashSet<>();
        backtrack(board, 0, cols, d1, d2, result);
        return result;
    }
    void backtrack(char[][] board, int row, Set<Integer> cols, Set<Integer> d1, Set<Integer> d2, List<List<String>> result) {
        if (row == board.length) {
            List<String> copy = new ArrayList<>();
            for (char[] r : board) copy.add(new String(r));
            result.add(copy);
            return;
        }
        for (int col = 0; col < board.length; col++) {
            if (cols.contains(col) || d1.contains(row-col) || d2.contains(row+col)) continue;
            board[row][col] = 'Q';
            cols.add(col); d1.add(row-col); d2.add(row+col);
            backtrack(board, row+1, cols, d1, d2, result);
            board[row][col] = '.';
            cols.remove(col); d1.remove(row-col); d2.remove(row+col);
        }
    }
}""",
"js": """var solveNQueens = function(n) {
    const result = [], board = Array.from({length: n}, () => '.'.repeat(n));
    const cols = new Set(), d1 = new Set(), d2 = new Set();
    const bt = (row) => {
        if (row === n) { result.push([...board]); return; }
        for (let col = 0; col < n; col++) {
            if (cols.has(col) || d1.has(row-col) || d2.has(row+col)) continue;
            board[row] = board[row].substring(0,col) + 'Q' + board[row].substring(col+1);
            cols.add(col); d1.add(row-col); d2.add(row+col);
            bt(row + 1);
            board[row] = board[row].substring(0,col) + '.' + board[row].substring(col+1);
            cols.delete(col); d1.delete(row-col); d2.delete(row+col);
        }
    };
    bt(0);
    return result;
};"""
}


# ============================================
# GRAPHS
# ============================================

solutions["200"] = {
"cpp": """class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int count = 0, m = grid.size(), n = grid[0].size();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (grid[i][j] == '1') { dfs(grid, i, j); count++; }
        return count;
    }
    void dfs(vector<vector<char>>& grid, int i, int j) {
        if (i < 0 || j < 0 || i >= grid.size() || j >= grid[0].size() || grid[i][j] != '1') return;
        grid[i][j] = '0';
        dfs(grid, i+1, j); dfs(grid, i-1, j); dfs(grid, i, j+1); dfs(grid, i, j-1);
    }
};""",
"java": """class Solution {
    public int numIslands(char[][] grid) {
        int count = 0;
        for (int i = 0; i < grid.length; i++)
            for (int j = 0; j < grid[0].length; j++)
                if (grid[i][j] == '1') { dfs(grid, i, j); count++; }
        return count;
    }
    void dfs(char[][] grid, int i, int j) {
        if (i < 0 || j < 0 || i >= grid.length || j >= grid[0].length || grid[i][j] != '1') return;
        grid[i][j] = '0';
        dfs(grid, i+1, j); dfs(grid, i-1, j); dfs(grid, i, j+1); dfs(grid, i, j-1);
    }
}""",
"js": """var numIslands = function(grid) {
    let count = 0;
    const m = grid.length, n = grid[0].length;
    const dfs = (i, j) => {
        if (i < 0 || j < 0 || i >= m || j >= n || grid[i][j] !== '1') return;
        grid[i][j] = '0';
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1);
    };
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++)
            if (grid[i][j] === '1') { dfs(i, j); count++; }
    return count;
};"""
}

solutions["133"] = {
"cpp": """class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (!node) return nullptr;
        unordered_map<Node*, Node*> map;
        function<Node*(Node*)> dfs = [&](Node* n) -> Node* {
            if (map.count(n)) return map[n];
            map[n] = new Node(n->val);
            for (auto* nb : n->neighbors) map[n]->neighbors.push_back(dfs(nb));
            return map[n];
        };
        return dfs(node);
    }
};""",
"java": """class Solution {
    Map<Node, Node> map = new HashMap<>();
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        if (map.containsKey(node)) return map.get(node);
        Node clone = new Node(node.val);
        map.put(node, clone);
        for (Node nb : node.neighbors) clone.neighbors.add(cloneGraph(nb));
        return clone;
    }
}""",
"js": """var cloneGraph = function(node) {
    if (!node) return null;
    const map = new Map();
    const dfs = (n) => {
        if (map.has(n)) return map.get(n);
        const clone = new Node(n.val);
        map.set(n, clone);
        for (const nb of n.neighbors) clone.neighbors.push(dfs(nb));
        return clone;
    };
    return dfs(node);
};"""
}

solutions["695"] = {
"cpp": """class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int maxArea = 0, m = grid.size(), n = grid[0].size();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (grid[i][j]) maxArea = max(maxArea, dfs(grid, i, j));
        return maxArea;
    }
    int dfs(vector<vector<int>>& grid, int i, int j) {
        if (i < 0 || j < 0 || i >= grid.size() || j >= grid[0].size() || !grid[i][j]) return 0;
        grid[i][j] = 0;
        return 1 + dfs(grid,i+1,j) + dfs(grid,i-1,j) + dfs(grid,i,j+1) + dfs(grid,i,j-1);
    }
};""",
"java": """class Solution {
    public int maxAreaOfIsland(int[][] grid) {
        int maxArea = 0;
        for (int i = 0; i < grid.length; i++)
            for (int j = 0; j < grid[0].length; j++)
                if (grid[i][j] == 1) maxArea = Math.max(maxArea, dfs(grid, i, j));
        return maxArea;
    }
    int dfs(int[][] grid, int i, int j) {
        if (i < 0 || j < 0 || i >= grid.length || j >= grid[0].length || grid[i][j] == 0) return 0;
        grid[i][j] = 0;
        return 1 + dfs(grid,i+1,j) + dfs(grid,i-1,j) + dfs(grid,i,j+1) + dfs(grid,i,j-1);
    }
}""",
"js": """var maxAreaOfIsland = function(grid) {
    const m = grid.length, n = grid[0].length;
    const dfs = (i, j) => {
        if (i < 0 || j < 0 || i >= m || j >= n || !grid[i][j]) return 0;
        grid[i][j] = 0;
        return 1 + dfs(i+1,j) + dfs(i-1,j) + dfs(i,j+1) + dfs(i,j-1);
    };
    let max = 0;
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++)
            if (grid[i][j]) max = Math.max(max, dfs(i, j));
    return max;
};"""
}

solutions["417"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int m = heights.size(), n = heights[0].size();
        vector<vector<bool>> pac(m, vector<bool>(n)), atl(m, vector<bool>(n));
        for (int i = 0; i < m; i++) { dfs(heights, pac, i, 0); dfs(heights, atl, i, n-1); }
        for (int j = 0; j < n; j++) { dfs(heights, pac, 0, j); dfs(heights, atl, m-1, j); }
        vector<vector<int>> result;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (pac[i][j] && atl[i][j]) result.push_back({i, j});
        return result;
    }
    void dfs(vector<vector<int>>& h, vector<vector<bool>>& v, int i, int j) {
        if (v[i][j]) return;
        v[i][j] = true;
        int dirs[] = {0,1,0,-1,0};
        for (int d = 0; d < 4; d++) {
            int ni = i+dirs[d], nj = j+dirs[d+1];
            if (ni >= 0 && nj >= 0 && ni < h.size() && nj < h[0].size() && h[ni][nj] >= h[i][j])
                dfs(h, v, ni, nj);
        }
    }
};""",
"java": """class Solution {
    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        int m = heights.length, n = heights[0].length;
        boolean[][] pac = new boolean[m][n], atl = new boolean[m][n];
        for (int i = 0; i < m; i++) { dfs(heights, pac, i, 0); dfs(heights, atl, i, n-1); }
        for (int j = 0; j < n; j++) { dfs(heights, pac, 0, j); dfs(heights, atl, m-1, j); }
        List<List<Integer>> result = new ArrayList<>();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (pac[i][j] && atl[i][j]) result.add(Arrays.asList(i, j));
        return result;
    }
    void dfs(int[][] h, boolean[][] v, int i, int j) {
        if (v[i][j]) return;
        v[i][j] = true;
        for (int[] d : dirs) {
            int ni = i+d[0], nj = j+d[1];
            if (ni >= 0 && nj >= 0 && ni < h.length && nj < h[0].length && h[ni][nj] >= h[i][j])
                dfs(h, v, ni, nj);
        }
    }
}""",
"js": """var pacificAtlantic = function(heights) {
    const m = heights.length, n = heights[0].length;
    const pac = Array.from({length:m}, () => new Array(n).fill(false));
    const atl = Array.from({length:m}, () => new Array(n).fill(false));
    const dfs = (vis, i, j) => {
        if (vis[i][j]) return;
        vis[i][j] = true;
        for (const [di,dj] of [[0,1],[0,-1],[1,0],[-1,0]]) {
            const ni = i+di, nj = j+dj;
            if (ni>=0 && nj>=0 && ni<m && nj<n && heights[ni][nj]>=heights[i][j]) dfs(vis,ni,nj);
        }
    };
    for (let i = 0; i < m; i++) { dfs(pac,i,0); dfs(atl,i,n-1); }
    for (let j = 0; j < n; j++) { dfs(pac,0,j); dfs(atl,m-1,j); }
    const result = [];
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) if (pac[i][j] && atl[i][j]) result.push([i,j]);
    return result;
};"""
}

solutions["130"] = {
"cpp": """class Solution {
public:
    void solve(vector<vector<char>>& board) {
        int m = board.size(), n = board[0].size();
        for (int i = 0; i < m; i++) { dfs(board, i, 0); dfs(board, i, n-1); }
        for (int j = 0; j < n; j++) { dfs(board, 0, j); dfs(board, m-1, j); }
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                board[i][j] = board[i][j] == 'T' ? 'O' : 'X';
    }
    void dfs(vector<vector<char>>& b, int i, int j) {
        if (i < 0 || j < 0 || i >= b.size() || j >= b[0].size() || b[i][j] != 'O') return;
        b[i][j] = 'T';
        dfs(b,i+1,j); dfs(b,i-1,j); dfs(b,i,j+1); dfs(b,i,j-1);
    }
};""",
"java": """class Solution {
    public void solve(char[][] board) {
        int m = board.length, n = board[0].length;
        for (int i = 0; i < m; i++) { dfs(board,i,0); dfs(board,i,n-1); }
        for (int j = 0; j < n; j++) { dfs(board,0,j); dfs(board,m-1,j); }
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                board[i][j] = board[i][j] == 'T' ? 'O' : 'X';
    }
    void dfs(char[][] b, int i, int j) {
        if (i < 0 || j < 0 || i >= b.length || j >= b[0].length || b[i][j] != 'O') return;
        b[i][j] = 'T';
        dfs(b,i+1,j); dfs(b,i-1,j); dfs(b,i,j+1); dfs(b,i,j-1);
    }
}""",
"js": """var solve = function(board) {
    const m = board.length, n = board[0].length;
    const dfs = (i, j) => {
        if (i < 0 || j < 0 || i >= m || j >= n || board[i][j] !== 'O') return;
        board[i][j] = 'T';
        dfs(i+1,j); dfs(i-1,j); dfs(i,j+1); dfs(i,j-1);
    };
    for (let i = 0; i < m; i++) { dfs(i,0); dfs(i,n-1); }
    for (let j = 0; j < n; j++) { dfs(0,j); dfs(m-1,j); }
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++)
            board[i][j] = board[i][j] === 'T' ? 'O' : 'X';
};"""
}

solutions["994"] = {
"cpp": """class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size(), fresh = 0, time = 0;
        queue<pair<int,int>> q;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) q.push({i, j});
                else if (grid[i][j] == 1) fresh++;
            }
        int dirs[] = {0,1,0,-1,0};
        while (!q.empty() && fresh > 0) {
            int sz = q.size();
            while (sz--) {
                auto [r, c] = q.front(); q.pop();
                for (int d = 0; d < 4; d++) {
                    int ni = r+dirs[d], nj = c+dirs[d+1];
                    if (ni>=0 && nj>=0 && ni<m && nj<n && grid[ni][nj]==1) {
                        grid[ni][nj] = 2; fresh--; q.push({ni, nj});
                    }
                }
            }
            time++;
        }
        return fresh == 0 ? time : -1;
    }
};""",
"java": """class Solution {
    public int orangesRotting(int[][] grid) {
        int m = grid.length, n = grid[0].length, fresh = 0, time = 0;
        Queue<int[]> q = new LinkedList<>();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 2) q.offer(new int[]{i,j});
                else if (grid[i][j] == 1) fresh++;
            }
        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
        while (!q.isEmpty() && fresh > 0) {
            int sz = q.size();
            while (sz-- > 0) {
                int[] cell = q.poll();
                for (int[] d : dirs) {
                    int ni = cell[0]+d[0], nj = cell[1]+d[1];
                    if (ni>=0 && nj>=0 && ni<m && nj<n && grid[ni][nj]==1) {
                        grid[ni][nj] = 2; fresh--; q.offer(new int[]{ni,nj});
                    }
                }
            }
            time++;
        }
        return fresh == 0 ? time : -1;
    }
}""",
"js": """var orangesRotting = function(grid) {
    const m = grid.length, n = grid[0].length, q = [];
    let fresh = 0, time = 0;
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === 2) q.push([i,j]);
            else if (grid[i][j] === 1) fresh++;
        }
    while (q.length && fresh > 0) {
        const sz = q.length;
        for (let s = 0; s < sz; s++) {
            const [r,c] = q.shift();
            for (const [di,dj] of [[0,1],[0,-1],[1,0],[-1,0]]) {
                const ni = r+di, nj = c+dj;
                if (ni>=0 && nj>=0 && ni<m && nj<n && grid[ni][nj]===1) {
                    grid[ni][nj] = 2; fresh--; q.push([ni,nj]);
                }
            }
        }
        time++;
    }
    return fresh === 0 ? time : -1;
};"""
}

solutions["286"] = {
"cpp": """class Solution {
public:
    void wallsAndGates(vector<vector<int>>& rooms) {
        int m = rooms.size(), n = rooms[0].size();
        queue<pair<int,int>> q;
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (rooms[i][j] == 0) q.push({i, j});
        int dirs[] = {0,1,0,-1,0};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int ni = r+dirs[d], nj = c+dirs[d+1];
                if (ni>=0 && nj>=0 && ni<m && nj<n && rooms[ni][nj] == INT_MAX) {
                    rooms[ni][nj] = rooms[r][c] + 1;
                    q.push({ni, nj});
                }
            }
        }
    }
};""",
"java": """class Solution {
    public void wallsAndGates(int[][] rooms) {
        int m = rooms.length, n = rooms[0].length;
        Queue<int[]> q = new LinkedList<>();
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (rooms[i][j] == 0) q.offer(new int[]{i,j});
        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
        while (!q.isEmpty()) {
            int[] cell = q.poll();
            for (int[] d : dirs) {
                int ni = cell[0]+d[0], nj = cell[1]+d[1];
                if (ni>=0 && nj>=0 && ni<m && nj<n && rooms[ni][nj] == Integer.MAX_VALUE) {
                    rooms[ni][nj] = rooms[cell[0]][cell[1]] + 1;
                    q.offer(new int[]{ni,nj});
                }
            }
        }
    }
}""",
"js": """var wallsAndGates = function(rooms) {
    const m = rooms.length, n = rooms[0].length, q = [];
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++)
            if (rooms[i][j] === 0) q.push([i,j]);
    while (q.length) {
        const [r,c] = q.shift();
        for (const [di,dj] of [[0,1],[0,-1],[1,0],[-1,0]]) {
            const ni = r+di, nj = c+dj;
            if (ni>=0 && nj>=0 && ni<m && nj<n && rooms[ni][nj] === 2147483647) {
                rooms[ni][nj] = rooms[r][c] + 1;
                q.push([ni,nj]);
            }
        }
    }
};"""
}

solutions["207"] = {
"cpp": """class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> graph(numCourses);
        vector<int> indegree(numCourses, 0);
        for (auto& p : prerequisites) { graph[p[1]].push_back(p[0]); indegree[p[0]]++; }
        queue<int> q;
        for (int i = 0; i < numCourses; i++) if (indegree[i] == 0) q.push(i);
        int count = 0;
        while (!q.empty()) {
            int cur = q.front(); q.pop(); count++;
            for (int next : graph[cur]) if (--indegree[next] == 0) q.push(next);
        }
        return count == numCourses;
    }
};""",
"java": """class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>();
        int[] indegree = new int[numCourses];
        for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
        for (int[] p : prerequisites) { graph.get(p[1]).add(p[0]); indegree[p[0]]++; }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) if (indegree[i] == 0) q.offer(i);
        int count = 0;
        while (!q.isEmpty()) {
            int cur = q.poll(); count++;
            for (int next : graph.get(cur)) if (--indegree[next] == 0) q.offer(next);
        }
        return count == numCourses;
    }
}""",
"js": """var canFinish = function(numCourses, prerequisites) {
    const graph = Array.from({length: numCourses}, () => []);
    const indegree = new Array(numCourses).fill(0);
    for (const [a, b] of prerequisites) { graph[b].push(a); indegree[a]++; }
    const q = [];
    for (let i = 0; i < numCourses; i++) if (indegree[i] === 0) q.push(i);
    let count = 0;
    while (q.length) {
        const cur = q.shift(); count++;
        for (const next of graph[cur]) if (--indegree[next] === 0) q.push(next);
    }
    return count === numCourses;
};"""
}

solutions["210"] = {
"cpp": """class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> graph(numCourses);
        vector<int> indegree(numCourses, 0);
        for (auto& p : prerequisites) { graph[p[1]].push_back(p[0]); indegree[p[0]]++; }
        queue<int> q;
        for (int i = 0; i < numCourses; i++) if (indegree[i] == 0) q.push(i);
        vector<int> order;
        while (!q.empty()) {
            int cur = q.front(); q.pop();
            order.push_back(cur);
            for (int next : graph[cur]) if (--indegree[next] == 0) q.push(next);
        }
        return order.size() == numCourses ? order : vector<int>();
    }
};""",
"java": """class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>();
        int[] indegree = new int[numCourses];
        for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
        for (int[] p : prerequisites) { graph.get(p[1]).add(p[0]); indegree[p[0]]++; }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) if (indegree[i] == 0) q.offer(i);
        int[] order = new int[numCourses];
        int idx = 0;
        while (!q.isEmpty()) {
            int cur = q.poll();
            order[idx++] = cur;
            for (int next : graph.get(cur)) if (--indegree[next] == 0) q.offer(next);
        }
        return idx == numCourses ? order : new int[]{};
    }
}""",
"js": """var findOrder = function(numCourses, prerequisites) {
    const graph = Array.from({length: numCourses}, () => []);
    const indegree = new Array(numCourses).fill(0);
    for (const [a, b] of prerequisites) { graph[b].push(a); indegree[a]++; }
    const q = [], order = [];
    for (let i = 0; i < numCourses; i++) if (indegree[i] === 0) q.push(i);
    while (q.length) {
        const cur = q.shift();
        order.push(cur);
        for (const next of graph[cur]) if (--indegree[next] === 0) q.push(next);
    }
    return order.length === numCourses ? order : [];
};"""
}

solutions["684"] = {
"cpp": """class Solution {
    vector<int> parent, rank_;
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        int n = edges.size();
        parent.resize(n + 1); rank_.resize(n + 1, 0);
        iota(parent.begin(), parent.end(), 0);
        for (auto& e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a == b) return e;
            if (rank_[a] < rank_[b]) swap(a, b);
            parent[b] = a;
            if (rank_[a] == rank_[b]) rank_[a]++;
        }
        return {};
    }
};""",
"java": """class Solution {
    int[] parent, rank;
    int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        parent = new int[n + 1]; rank = new int[n + 1];
        for (int i = 0; i <= n; i++) parent[i] = i;
        for (int[] e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a == b) return e;
            if (rank[a] < rank[b]) { int t = a; a = b; b = t; }
            parent[b] = a;
            if (rank[a] == rank[b]) rank[a]++;
        }
        return new int[]{};
    }
}""",
"js": """var findRedundantConnection = function(edges) {
    const n = edges.length, parent = Array.from({length: n+1}, (_, i) => i);
    const rank = new Array(n+1).fill(0);
    const find = (x) => parent[x] === x ? x : (parent[x] = find(parent[x]));
    for (const [a, b] of edges) {
        let pa = find(a), pb = find(b);
        if (pa === pb) return [a, b];
        if (rank[pa] < rank[pb]) [pa, pb] = [pb, pa];
        parent[pb] = pa;
        if (rank[pa] === rank[pb]) rank[pa]++;
    }
};"""
}

solutions["323"] = {
"cpp": """class Solution {
public:
    int countComponents(int n, vector<vector<int>>& edges) {
        vector<int> parent(n);
        iota(parent.begin(), parent.end(), 0);
        function<int(int)> find = [&](int x) {
            return parent[x] == x ? x : parent[x] = find(parent[x]);
        };
        int components = n;
        for (auto& e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a != b) { parent[a] = b; components--; }
        }
        return components;
    }
};""",
"java": """class Solution {
    int[] parent;
    int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
    public int countComponents(int n, int[][] edges) {
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int components = n;
        for (int[] e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a != b) { parent[a] = b; components--; }
        }
        return components;
    }
}""",
"js": """var countComponents = function(n, edges) {
    const parent = Array.from({length: n}, (_, i) => i);
    const find = (x) => parent[x] === x ? x : (parent[x] = find(parent[x]));
    let components = n;
    for (const [a, b] of edges) {
        const pa = find(a), pb = find(b);
        if (pa !== pb) { parent[pa] = pb; components--; }
    }
    return components;
};"""
}

solutions["261"] = {
"cpp": """class Solution {
public:
    bool validTree(int n, vector<vector<int>>& edges) {
        if (edges.size() != n - 1) return false;
        vector<int> parent(n);
        iota(parent.begin(), parent.end(), 0);
        function<int(int)> find = [&](int x) {
            return parent[x] == x ? x : parent[x] = find(parent[x]);
        };
        for (auto& e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a == b) return false;
            parent[a] = b;
        }
        return true;
    }
};""",
"java": """class Solution {
    int[] parent;
    int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
    public boolean validTree(int n, int[][] edges) {
        if (edges.length != n - 1) return false;
        parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] e : edges) {
            int a = find(e[0]), b = find(e[1]);
            if (a == b) return false;
            parent[a] = b;
        }
        return true;
    }
}""",
"js": """var validTree = function(n, edges) {
    if (edges.length !== n - 1) return false;
    const parent = Array.from({length: n}, (_, i) => i);
    const find = (x) => parent[x] === x ? x : (parent[x] = find(parent[x]));
    for (const [a, b] of edges) {
        const pa = find(a), pb = find(b);
        if (pa === pb) return false;
        parent[pa] = pb;
    }
    return true;
};"""
}

solutions["127"] = {
"cpp": """class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> dict(wordList.begin(), wordList.end());
        if (!dict.count(endWord)) return 0;
        queue<string> q;
        q.push(beginWord);
        int steps = 1;
        while (!q.empty()) {
            int sz = q.size();
            while (sz--) {
                string word = q.front(); q.pop();
                for (int i = 0; i < word.size(); i++) {
                    char orig = word[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        word[i] = c;
                        if (word == endWord) return steps + 1;
                        if (dict.count(word)) { q.push(word); dict.erase(word); }
                    }
                    word[i] = orig;
                }
            }
            steps++;
        }
        return 0;
    }
};""",
"java": """class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> dict = new HashSet<>(wordList);
        if (!dict.contains(endWord)) return 0;
        Queue<String> q = new LinkedList<>();
        q.offer(beginWord);
        int steps = 1;
        while (!q.isEmpty()) {
            int sz = q.size();
            while (sz-- > 0) {
                char[] word = q.poll().toCharArray();
                for (int i = 0; i < word.length; i++) {
                    char orig = word[i];
                    for (char c = 'a'; c <= 'z'; c++) {
                        word[i] = c;
                        String s = new String(word);
                        if (s.equals(endWord)) return steps + 1;
                        if (dict.contains(s)) { q.offer(s); dict.remove(s); }
                    }
                    word[i] = orig;
                }
            }
            steps++;
        }
        return 0;
    }
}""",
"js": """var ladderLength = function(beginWord, endWord, wordList) {
    const dict = new Set(wordList);
    if (!dict.has(endWord)) return 0;
    const q = [beginWord];
    let steps = 1;
    while (q.length) {
        const sz = q.length;
        for (let s = 0; s < sz; s++) {
            const word = q.shift().split('');
            for (let i = 0; i < word.length; i++) {
                const orig = word[i];
                for (let c = 97; c <= 122; c++) {
                    word[i] = String.fromCharCode(c);
                    const str = word.join('');
                    if (str === endWord) return steps + 1;
                    if (dict.has(str)) { q.push(str); dict.delete(str); }
                }
                word[i] = orig;
            }
        }
        steps++;
    }
    return 0;
};"""
}


# ============================================
# ADVANCED GRAPHS
# ============================================

solutions["332"] = {
"cpp": """class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, priority_queue<string, vector<string>, greater<string>>> graph;
        for (auto& t : tickets) graph[t[0]].push(t[1]);
        vector<string> result;
        function<void(string)> dfs = [&](string airport) {
            while (!graph[airport].empty()) {
                string next = graph[airport].top(); graph[airport].pop();
                dfs(next);
            }
            result.push_back(airport);
        };
        dfs("JFK");
        reverse(result.begin(), result.end());
        return result;
    }
};""",
"java": """class Solution {
    Map<String, PriorityQueue<String>> graph = new HashMap<>();
    List<String> result = new LinkedList<>();
    public List<String> findItinerary(List<List<String>> tickets) {
        for (var t : tickets) graph.computeIfAbsent(t.get(0), k -> new PriorityQueue<>()).offer(t.get(1));
        dfs("JFK");
        return result;
    }
    void dfs(String airport) {
        while (graph.containsKey(airport) && !graph.get(airport).isEmpty())
            dfs(graph.get(airport).poll());
        result.add(0, airport);
    }
}""",
"js": """var findItinerary = function(tickets) {
    const graph = {};
    for (const [from, to] of tickets) {
        if (!graph[from]) graph[from] = [];
        graph[from].push(to);
    }
    for (const key in graph) graph[key].sort();
    const result = [];
    const dfs = (airport) => {
        while (graph[airport] && graph[airport].length)
            dfs(graph[airport].shift());
        result.unshift(airport);
    };
    dfs('JFK');
    return result;
};"""
}

solutions["1584"] = {
"cpp": """class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        int n = points.size(), cost = 0, connected = 0;
        vector<int> minDist(n, INT_MAX);
        vector<bool> visited(n, false);
        minDist[0] = 0;
        while (connected < n) {
            int u = -1;
            for (int i = 0; i < n; i++)
                if (!visited[i] && (u == -1 || minDist[i] < minDist[u])) u = i;
            visited[u] = true;
            cost += minDist[u]; connected++;
            for (int v = 0; v < n; v++) {
                int d = abs(points[u][0]-points[v][0]) + abs(points[u][1]-points[v][1]);
                minDist[v] = min(minDist[v], d);
            }
        }
        return cost;
    }
};""",
"java": """class Solution {
    public int minCostConnectPoints(int[][] points) {
        int n = points.length, cost = 0;
        int[] minDist = new int[n];
        boolean[] visited = new boolean[n];
        Arrays.fill(minDist, Integer.MAX_VALUE);
        minDist[0] = 0;
        for (int i = 0; i < n; i++) {
            int u = -1;
            for (int j = 0; j < n; j++)
                if (!visited[j] && (u == -1 || minDist[j] < minDist[u])) u = j;
            visited[u] = true;
            cost += minDist[u];
            for (int v = 0; v < n; v++)
                minDist[v] = Math.min(minDist[v],
                    Math.abs(points[u][0]-points[v][0]) + Math.abs(points[u][1]-points[v][1]));
        }
        return cost;
    }
}""",
"js": """var minCostConnectPoints = function(points) {
    const n = points.length;
    const minDist = new Array(n).fill(Infinity);
    const visited = new Array(n).fill(false);
    minDist[0] = 0;
    let cost = 0;
    for (let i = 0; i < n; i++) {
        let u = -1;
        for (let j = 0; j < n; j++)
            if (!visited[j] && (u === -1 || minDist[j] < minDist[u])) u = j;
        visited[u] = true;
        cost += minDist[u];
        for (let v = 0; v < n; v++)
            minDist[v] = Math.min(minDist[v],
                Math.abs(points[u][0]-points[v][0]) + Math.abs(points[u][1]-points[v][1]));
    }
    return cost;
};"""
}

solutions["743"] = {
"cpp": """class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<vector<pair<int,int>>> graph(n + 1);
        for (auto& t : times) graph[t[0]].push_back({t[1], t[2]});
        vector<int> dist(n + 1, INT_MAX);
        dist[k] = 0;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
        pq.push({0, k});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d > dist[u]) continue;
            for (auto [v, w] : graph[u]) {
                if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push({dist[v], v}); }
            }
        }
        int result = *max_element(dist.begin() + 1, dist.end());
        return result == INT_MAX ? -1 : result;
    }
};""",
"java": """class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        List<int[]>[] graph = new List[n + 1];
        for (int i = 0; i <= n; i++) graph[i] = new ArrayList<>();
        for (int[] t : times) graph[t[0]].add(new int[]{t[1], t[2]});
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> a[0] - b[0]);
        pq.offer(new int[]{0, k});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            if (cur[0] > dist[cur[1]]) continue;
            for (int[] e : graph[cur[1]])
                if (dist[cur[1]] + e[1] < dist[e[0]]) {
                    dist[e[0]] = dist[cur[1]] + e[1];
                    pq.offer(new int[]{dist[e[0]], e[0]});
                }
        }
        int result = 0;
        for (int i = 1; i <= n; i++) result = Math.max(result, dist[i]);
        return result == Integer.MAX_VALUE ? -1 : result;
    }
}""",
"js": """var networkDelayTime = function(times, n, k) {
    const graph = Array.from({length: n+1}, () => []);
    for (const [u,v,w] of times) graph[u].push([v,w]);
    const dist = new Array(n+1).fill(Infinity);
    dist[k] = 0;
    const pq = [[0, k]]; // [dist, node]
    while (pq.length) {
        pq.sort((a,b) => a[0]-b[0]);
        const [d, u] = pq.shift();
        if (d > dist[u]) continue;
        for (const [v, w] of graph[u])
            if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.push([dist[v], v]); }
    }
    const result = Math.max(...dist.slice(1));
    return result === Infinity ? -1 : result;
};"""
}

solutions["787"] = {
"cpp": """class Solution {
public:
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<int> prices(n, INT_MAX);
        prices[src] = 0;
        for (int i = 0; i <= k; i++) {
            vector<int> tmp(prices);
            for (auto& f : flights) {
                if (prices[f[0]] == INT_MAX) continue;
                tmp[f[1]] = min(tmp[f[1]], prices[f[0]] + f[2]);
            }
            prices = tmp;
        }
        return prices[dst] == INT_MAX ? -1 : prices[dst];
    }
};""",
"java": """class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] prices = new int[n];
        Arrays.fill(prices, Integer.MAX_VALUE);
        prices[src] = 0;
        for (int i = 0; i <= k; i++) {
            int[] tmp = prices.clone();
            for (int[] f : flights) {
                if (prices[f[0]] == Integer.MAX_VALUE) continue;
                tmp[f[1]] = Math.min(tmp[f[1]], prices[f[0]] + f[2]);
            }
            prices = tmp;
        }
        return prices[dst] == Integer.MAX_VALUE ? -1 : prices[dst];
    }
}""",
"js": """var findCheapestPrice = function(n, flights, src, dst, k) {
    let prices = new Array(n).fill(Infinity);
    prices[src] = 0;
    for (let i = 0; i <= k; i++) {
        const tmp = [...prices];
        for (const [u, v, w] of flights)
            if (prices[u] !== Infinity) tmp[v] = Math.min(tmp[v], prices[u] + w);
        prices = tmp;
    }
    return prices[dst] === Infinity ? -1 : prices[dst];
};"""
}

solutions["269"] = {
"cpp": """class Solution {
public:
    string alienOrder(vector<string>& words) {
        unordered_map<char, unordered_set<char>> graph;
        unordered_map<char, int> indegree;
        for (auto& w : words) for (char c : w) indegree[c] = 0;
        for (int i = 0; i < words.size() - 1; i++) {
            string &w1 = words[i], &w2 = words[i+1];
            if (w1.size() > w2.size() && w1.substr(0, w2.size()) == w2) return "";
            for (int j = 0; j < min(w1.size(), w2.size()); j++) {
                if (w1[j] != w2[j]) {
                    if (!graph[w1[j]].count(w2[j])) {
                        graph[w1[j]].insert(w2[j]);
                        indegree[w2[j]]++;
                    }
                    break;
                }
            }
        }
        queue<char> q;
        for (auto& [c, d] : indegree) if (d == 0) q.push(c);
        string result;
        while (!q.empty()) {
            char c = q.front(); q.pop();
            result += c;
            for (char next : graph[c]) if (--indegree[next] == 0) q.push(next);
        }
        return result.size() == indegree.size() ? result : "";
    }
};""",
"java": """class Solution {
    public String alienOrder(String[] words) {
        Map<Character, Set<Character>> graph = new HashMap<>();
        Map<Character, Integer> indegree = new HashMap<>();
        for (String w : words) for (char c : w.toCharArray()) indegree.put(c, 0);
        for (int i = 0; i < words.length - 1; i++) {
            String w1 = words[i], w2 = words[i+1];
            if (w1.length() > w2.length() && w1.startsWith(w2)) return "";
            for (int j = 0; j < Math.min(w1.length(), w2.length()); j++) {
                if (w1.charAt(j) != w2.charAt(j)) {
                    graph.computeIfAbsent(w1.charAt(j), k -> new HashSet<>());
                    if (graph.get(w1.charAt(j)).add(w2.charAt(j)))
                        indegree.merge(w2.charAt(j), 1, Integer::sum);
                    break;
                }
            }
        }
        Queue<Character> q = new LinkedList<>();
        for (var e : indegree.entrySet()) if (e.getValue() == 0) q.offer(e.getKey());
        StringBuilder sb = new StringBuilder();
        while (!q.isEmpty()) {
            char c = q.poll(); sb.append(c);
            if (graph.containsKey(c))
                for (char next : graph.get(c)) if (indegree.merge(next, -1, Integer::sum) == 0) q.offer(next);
        }
        return sb.length() == indegree.size() ? sb.toString() : "";
    }
}""",
"js": """var alienOrder = function(words) {
    const graph = {}, indegree = {};
    for (const w of words) for (const c of w) indegree[c] = 0;
    for (let i = 0; i < words.length - 1; i++) {
        const w1 = words[i], w2 = words[i+1];
        if (w1.length > w2.length && w1.startsWith(w2)) return '';
        for (let j = 0; j < Math.min(w1.length, w2.length); j++) {
            if (w1[j] !== w2[j]) {
                if (!graph[w1[j]]) graph[w1[j]] = new Set();
                if (!graph[w1[j]].has(w2[j])) {
                    graph[w1[j]].add(w2[j]);
                    indegree[w2[j]]++;
                }
                break;
            }
        }
    }
    const q = Object.keys(indegree).filter(c => indegree[c] === 0);
    let result = '';
    while (q.length) {
        const c = q.shift(); result += c;
        if (graph[c]) for (const next of graph[c]) if (--indegree[next] === 0) q.push(next);
    }
    return result.length === Object.keys(indegree).length ? result : '';
};"""
}

solutions["778"] = {
"cpp": """class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        int n = grid.size();
        priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;
        pq.push({grid[0][0], 0, 0});
        vector<vector<bool>> visited(n, vector<bool>(n, false));
        visited[0][0] = true;
        int dirs[] = {0,1,0,-1,0};
        while (!pq.empty()) {
            auto [t, i, j] = pq.top(); pq.pop();
            if (i == n-1 && j == n-1) return t;
            for (int d = 0; d < 4; d++) {
                int ni = i+dirs[d], nj = j+dirs[d+1];
                if (ni>=0 && nj>=0 && ni<n && nj<n && !visited[ni][nj]) {
                    visited[ni][nj] = true;
                    pq.push({max(t, grid[ni][nj]), ni, nj});
                }
            }
        }
        return 0;
    }
};""",
"java": """class Solution {
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> a[0]-b[0]);
        pq.offer(new int[]{grid[0][0], 0, 0});
        boolean[][] visited = new boolean[n][n];
        visited[0][0] = true;
        int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            if (cur[1] == n-1 && cur[2] == n-1) return cur[0];
            for (int[] d : dirs) {
                int ni = cur[1]+d[0], nj = cur[2]+d[1];
                if (ni>=0 && nj>=0 && ni<n && nj<n && !visited[ni][nj]) {
                    visited[ni][nj] = true;
                    pq.offer(new int[]{Math.max(cur[0], grid[ni][nj]), ni, nj});
                }
            }
        }
        return 0;
    }
}""",
"js": """var swimInWater = function(grid) {
    const n = grid.length;
    const visited = Array.from({length:n}, () => new Array(n).fill(false));
    const pq = [[grid[0][0], 0, 0]];
    visited[0][0] = true;
    while (pq.length) {
        pq.sort((a,b) => a[0]-b[0]);
        const [t, i, j] = pq.shift();
        if (i === n-1 && j === n-1) return t;
        for (const [di,dj] of [[0,1],[0,-1],[1,0],[-1,0]]) {
            const ni = i+di, nj = j+dj;
            if (ni>=0 && nj>=0 && ni<n && nj<n && !visited[ni][nj]) {
                visited[ni][nj] = true;
                pq.push([Math.max(t, grid[ni][nj]), ni, nj]);
            }
        }
    }
};"""
}

# ============================================
# 1-D DYNAMIC PROGRAMMING
# ============================================

solutions["70"] = {
"cpp": """class Solution {
public:
    int climbStairs(int n) {
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) { int c = a + b; a = b; b = c; }
        return b;
    }
};""",
"java": """class Solution {
    public int climbStairs(int n) {
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) { int c = a + b; a = b; b = c; }
        return b;
    }
}""",
"js": """var climbStairs = function(n) {
    let a = 1, b = 1;
    for (let i = 2; i <= n; i++) { const c = a + b; a = b; b = c; }
    return b;
};"""
}

solutions["746"] = {
"cpp": """class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int a = 0, b = 0;
        for (int i = 2; i <= cost.size(); i++) {
            int c = min(a + cost[i-2], b + cost[i-1]);
            a = b; b = c;
        }
        return b;
    }
};""",
"java": """class Solution {
    public int minCostClimbingStairs(int[] cost) {
        int a = 0, b = 0;
        for (int i = 2; i <= cost.length; i++) {
            int c = Math.min(a + cost[i-2], b + cost[i-1]);
            a = b; b = c;
        }
        return b;
    }
}""",
"js": """var minCostClimbingStairs = function(cost) {
    let a = 0, b = 0;
    for (let i = 2; i <= cost.length; i++) {
        const c = Math.min(a + cost[i-2], b + cost[i-1]);
        a = b; b = c;
    }
    return b;
};"""
}

solutions["198"] = {
"cpp": """class Solution {
public:
    int rob(vector<int>& nums) {
        int prev2 = 0, prev1 = 0;
        for (int n : nums) { int cur = max(prev1, prev2 + n); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
};""",
"java": """class Solution {
    public int rob(int[] nums) {
        int prev2 = 0, prev1 = 0;
        for (int n : nums) { int cur = Math.max(prev1, prev2 + n); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
}""",
"js": """var rob = function(nums) {
    let prev2 = 0, prev1 = 0;
    for (const n of nums) { const cur = Math.max(prev1, prev2 + n); prev2 = prev1; prev1 = cur; }
    return prev1;
};"""
}

solutions["213"] = {
"cpp": """class Solution {
public:
    int rob(vector<int>& nums) {
        if (nums.size() == 1) return nums[0];
        return max(robRange(nums, 0, nums.size()-2), robRange(nums, 1, nums.size()-1));
    }
    int robRange(vector<int>& nums, int lo, int hi) {
        int prev2 = 0, prev1 = 0;
        for (int i = lo; i <= hi; i++) { int cur = max(prev1, prev2 + nums[i]); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
};""",
"java": """class Solution {
    public int rob(int[] nums) {
        if (nums.length == 1) return nums[0];
        return Math.max(robRange(nums, 0, nums.length-2), robRange(nums, 1, nums.length-1));
    }
    int robRange(int[] nums, int lo, int hi) {
        int prev2 = 0, prev1 = 0;
        for (int i = lo; i <= hi; i++) { int cur = Math.max(prev1, prev2 + nums[i]); prev2 = prev1; prev1 = cur; }
        return prev1;
    }
}""",
"js": """var rob = function(nums) {
    if (nums.length === 1) return nums[0];
    const robRange = (lo, hi) => {
        let prev2 = 0, prev1 = 0;
        for (let i = lo; i <= hi; i++) { const cur = Math.max(prev1, prev2 + nums[i]); prev2 = prev1; prev1 = cur; }
        return prev1;
    };
    return Math.max(robRange(0, nums.length-2), robRange(1, nums.length-1));
};"""
}

solutions["5"] = {
"cpp": """class Solution {
public:
    string longestPalindrome(string s) {
        int start = 0, maxLen = 0;
        for (int i = 0; i < s.size(); i++) {
            for (int d : {0, 1}) {
                int l = i, r = i + d;
                while (l >= 0 && r < s.size() && s[l] == s[r]) { l--; r++; }
                if (r - l - 1 > maxLen) { maxLen = r - l - 1; start = l + 1; }
            }
        }
        return s.substr(start, maxLen);
    }
};""",
"java": """class Solution {
    public String longestPalindrome(String s) {
        int start = 0, maxLen = 0;
        for (int i = 0; i < s.length(); i++) {
            for (int d = 0; d <= 1; d++) {
                int l = i, r = i + d;
                while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
                if (r - l - 1 > maxLen) { maxLen = r - l - 1; start = l + 1; }
            }
        }
        return s.substring(start, start + maxLen);
    }
}""",
"js": """var longestPalindrome = function(s) {
    let start = 0, maxLen = 0;
    for (let i = 0; i < s.length; i++) {
        for (const d of [0, 1]) {
            let l = i, r = i + d;
            while (l >= 0 && r < s.length && s[l] === s[r]) { l--; r++; }
            if (r - l - 1 > maxLen) { maxLen = r - l - 1; start = l + 1; }
        }
    }
    return s.substring(start, start + maxLen);
};"""
}

solutions["647"] = {
"cpp": """class Solution {
public:
    int countSubstrings(string s) {
        int count = 0;
        for (int i = 0; i < s.size(); i++)
            for (int d : {0, 1}) {
                int l = i, r = i + d;
                while (l >= 0 && r < s.size() && s[l] == s[r]) { count++; l--; r++; }
            }
        return count;
    }
};""",
"java": """class Solution {
    public int countSubstrings(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++)
            for (int d = 0; d <= 1; d++) {
                int l = i, r = i + d;
                while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { count++; l--; r++; }
            }
        return count;
    }
}""",
"js": """var countSubstrings = function(s) {
    let count = 0;
    for (let i = 0; i < s.length; i++)
        for (const d of [0, 1]) {
            let l = i, r = i + d;
            while (l >= 0 && r < s.length && s[l] === s[r]) { count++; l--; r++; }
        }
    return count;
};"""
}

solutions["91"] = {
"cpp": """class Solution {
public:
    int numDecodings(string s) {
        int n = s.size(), prev2 = 1, prev1 = s[0] != '0' ? 1 : 0;
        for (int i = 2; i <= n; i++) {
            int cur = 0;
            if (s[i-1] != '0') cur += prev1;
            int two = stoi(s.substr(i-2, 2));
            if (two >= 10 && two <= 26) cur += prev2;
            prev2 = prev1; prev1 = cur;
        }
        return prev1;
    }
};""",
"java": """class Solution {
    public int numDecodings(String s) {
        int prev2 = 1, prev1 = s.charAt(0) != '0' ? 1 : 0;
        for (int i = 2; i <= s.length(); i++) {
            int cur = 0;
            if (s.charAt(i-1) != '0') cur += prev1;
            int two = Integer.parseInt(s.substring(i-2, i));
            if (two >= 10 && two <= 26) cur += prev2;
            prev2 = prev1; prev1 = cur;
        }
        return prev1;
    }
}""",
"js": """var numDecodings = function(s) {
    let prev2 = 1, prev1 = s[0] !== '0' ? 1 : 0;
    for (let i = 2; i <= s.length; i++) {
        let cur = 0;
        if (s[i-1] !== '0') cur += prev1;
        const two = Number(s.substring(i-2, i));
        if (two >= 10 && two <= 26) cur += prev2;
        prev2 = prev1; prev1 = cur;
    }
    return prev1;
};"""
}

solutions["322"] = {
"cpp": """class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp(amount + 1, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++)
            for (int c : coins)
                if (c <= i) dp[i] = min(dp[i], dp[i - c] + 1);
        return dp[amount] > amount ? -1 : dp[amount];
    }
};""",
"java": """class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++)
            for (int c : coins)
                if (c <= i) dp[i] = Math.min(dp[i], dp[i - c] + 1);
        return dp[amount] > amount ? -1 : dp[amount];
    }
}""",
"js": """var coinChange = function(coins, amount) {
    const dp = new Array(amount + 1).fill(amount + 1);
    dp[0] = 0;
    for (let i = 1; i <= amount; i++)
        for (const c of coins)
            if (c <= i) dp[i] = Math.min(dp[i], dp[i - c] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
};"""
}

solutions["152"] = {
"cpp": """class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int result = nums[0], curMax = 1, curMin = 1;
        for (int n : nums) {
            int a = curMax * n, b = curMin * n;
            curMax = max({n, a, b});
            curMin = min({n, a, b});
            result = max(result, curMax);
        }
        return result;
    }
};""",
"java": """class Solution {
    public int maxProduct(int[] nums) {
        int result = nums[0], curMax = 1, curMin = 1;
        for (int n : nums) {
            int a = curMax * n, b = curMin * n;
            curMax = Math.max(n, Math.max(a, b));
            curMin = Math.min(n, Math.min(a, b));
            result = Math.max(result, curMax);
        }
        return result;
    }
}""",
"js": """var maxProduct = function(nums) {
    let result = nums[0], curMax = 1, curMin = 1;
    for (const n of nums) {
        const a = curMax * n, b = curMin * n;
        curMax = Math.max(n, a, b);
        curMin = Math.min(n, a, b);
        result = Math.max(result, curMax);
    }
    return result;
};"""
}

solutions["139"] = {
"cpp": """class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> dict(wordDict.begin(), wordDict.end());
        int n = s.size();
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int i = 1; i <= n; i++)
            for (int j = 0; j < i; j++)
                if (dp[j] && dict.count(s.substr(j, i - j))) { dp[i] = true; break; }
        return dp[n];
    }
};""",
"java": """class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> dict = new HashSet<>(wordDict);
        boolean[] dp = new boolean[s.length() + 1];
        dp[0] = true;
        for (int i = 1; i <= s.length(); i++)
            for (int j = 0; j < i; j++)
                if (dp[j] && dict.contains(s.substring(j, i))) { dp[i] = true; break; }
        return dp[s.length()];
    }
}""",
"js": """var wordBreak = function(s, wordDict) {
    const dict = new Set(wordDict);
    const dp = new Array(s.length + 1).fill(false);
    dp[0] = true;
    for (let i = 1; i <= s.length; i++)
        for (let j = 0; j < i; j++)
            if (dp[j] && dict.has(s.substring(j, i))) { dp[i] = true; break; }
    return dp[s.length];
};"""
}

solutions["300"] = {
"cpp": """class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tails;
        for (int n : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), n);
            if (it == tails.end()) tails.push_back(n);
            else *it = n;
        }
        return tails.size();
    }
};""",
"java": """class Solution {
    public int lengthOfLIS(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        for (int n : nums) {
            int pos = Collections.binarySearch(tails, n);
            if (pos < 0) pos = -(pos + 1);
            if (pos == tails.size()) tails.add(n);
            else tails.set(pos, n);
        }
        return tails.size();
    }
}""",
"js": """var lengthOfLIS = function(nums) {
    const tails = [];
    for (const n of nums) {
        let l = 0, r = tails.length;
        while (l < r) { const m = (l+r)>>1; tails[m] < n ? l = m+1 : r = m; }
        tails[l] = n;
    }
    return tails.length;
};"""
}

solutions["416"] = {
"cpp": """class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = accumulate(nums.begin(), nums.end(), 0);
        if (sum % 2) return false;
        int target = sum / 2;
        vector<bool> dp(target + 1, false);
        dp[0] = true;
        for (int n : nums)
            for (int j = target; j >= n; j--)
                dp[j] = dp[j] || dp[j - n];
        return dp[target];
    }
};""",
"java": """class Solution {
    public boolean canPartition(int[] nums) {
        int sum = Arrays.stream(nums).sum();
        if (sum % 2 != 0) return false;
        int target = sum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;
        for (int n : nums)
            for (int j = target; j >= n; j--)
                dp[j] = dp[j] || dp[j - n];
        return dp[target];
    }
}""",
"js": """var canPartition = function(nums) {
    const sum = nums.reduce((a, b) => a + b, 0);
    if (sum % 2) return false;
    const target = sum / 2;
    const dp = new Array(target + 1).fill(false);
    dp[0] = true;
    for (const n of nums)
        for (let j = target; j >= n; j--)
            dp[j] = dp[j] || dp[j - n];
    return dp[target];
};"""
}


# ============================================
# 2-D DYNAMIC PROGRAMMING
# ============================================

solutions["62"] = {
"cpp": """class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<int> dp(n, 1);
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++) dp[j] += dp[j-1];
        return dp[n-1];
    }
};""",
"java": """class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++) dp[j] += dp[j-1];
        return dp[n-1];
    }
}""",
"js": """var uniquePaths = function(m, n) {
    const dp = new Array(n).fill(1);
    for (let i = 1; i < m; i++)
        for (let j = 1; j < n; j++) dp[j] += dp[j-1];
    return dp[n-1];
};"""
}

solutions["1143"] = {
"cpp": """class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size(), n = text2.size();
        vector<int> dp(n + 1, 0);
        for (int i = 1; i <= m; i++) {
            int prev = 0;
            for (int j = 1; j <= n; j++) {
                int tmp = dp[j];
                dp[j] = text1[i-1] == text2[j-1] ? prev + 1 : max(dp[j], dp[j-1]);
                prev = tmp;
            }
        }
        return dp[n];
    }
};""",
"java": """class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[] dp = new int[n + 1];
        for (int i = 1; i <= m; i++) {
            int prev = 0;
            for (int j = 1; j <= n; j++) {
                int tmp = dp[j];
                dp[j] = text1.charAt(i-1) == text2.charAt(j-1) ? prev + 1 : Math.max(dp[j], dp[j-1]);
                prev = tmp;
            }
        }
        return dp[n];
    }
}""",
"js": """var longestCommonSubsequence = function(text1, text2) {
    const m = text1.length, n = text2.length;
    const dp = new Array(n + 1).fill(0);
    for (let i = 1; i <= m; i++) {
        let prev = 0;
        for (let j = 1; j <= n; j++) {
            const tmp = dp[j];
            dp[j] = text1[i-1] === text2[j-1] ? prev + 1 : Math.max(dp[j], dp[j-1]);
            prev = tmp;
        }
    }
    return dp[n];
};"""
}

solutions["309"] = {
"cpp": """class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int sold = 0, held = INT_MIN, rest = 0;
        for (int p : prices) {
            int prevSold = sold;
            sold = held + p;
            held = max(held, rest - p);
            rest = max(rest, prevSold);
        }
        return max(sold, rest);
    }
};""",
"java": """class Solution {
    public int maxProfit(int[] prices) {
        int sold = 0, held = Integer.MIN_VALUE, rest = 0;
        for (int p : prices) {
            int prevSold = sold;
            sold = held + p;
            held = Math.max(held, rest - p);
            rest = Math.max(rest, prevSold);
        }
        return Math.max(sold, rest);
    }
}""",
"js": """var maxProfit = function(prices) {
    let sold = 0, held = -Infinity, rest = 0;
    for (const p of prices) {
        const prevSold = sold;
        sold = held + p;
        held = Math.max(held, rest - p);
        rest = Math.max(rest, prevSold);
    }
    return Math.max(sold, rest);
};"""
}

solutions["518"] = {
"cpp": """class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<int> dp(amount + 1, 0);
        dp[0] = 1;
        for (int c : coins)
            for (int i = c; i <= amount; i++) dp[i] += dp[i - c];
        return dp[amount];
    }
};""",
"java": """class Solution {
    public int change(int amount, int[] coins) {
        int[] dp = new int[amount + 1];
        dp[0] = 1;
        for (int c : coins)
            for (int i = c; i <= amount; i++) dp[i] += dp[i - c];
        return dp[amount];
    }
}""",
"js": """var change = function(amount, coins) {
    const dp = new Array(amount + 1).fill(0);
    dp[0] = 1;
    for (const c of coins)
        for (let i = c; i <= amount; i++) dp[i] += dp[i - c];
    return dp[amount];
};"""
}

solutions["494"] = {
"cpp": """class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = accumulate(nums.begin(), nums.end(), 0);
        if ((sum + target) % 2 || abs(target) > sum) return 0;
        int t = (sum + target) / 2;
        vector<int> dp(t + 1, 0);
        dp[0] = 1;
        for (int n : nums)
            for (int j = t; j >= n; j--) dp[j] += dp[j - n];
        return dp[t];
    }
};""",
"java": """class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        int sum = Arrays.stream(nums).sum();
        if ((sum + target) % 2 != 0 || Math.abs(target) > sum) return 0;
        int t = (sum + target) / 2;
        int[] dp = new int[t + 1];
        dp[0] = 1;
        for (int n : nums)
            for (int j = t; j >= n; j--) dp[j] += dp[j - n];
        return dp[t];
    }
}""",
"js": """var findTargetSumWays = function(nums, target) {
    const sum = nums.reduce((a, b) => a + b, 0);
    if ((sum + target) % 2 || Math.abs(target) > sum) return 0;
    const t = (sum + target) / 2;
    const dp = new Array(t + 1).fill(0);
    dp[0] = 1;
    for (const n of nums)
        for (let j = t; j >= n; j--) dp[j] += dp[j - n];
    return dp[t];
};"""
}

solutions["97"] = {
"cpp": """class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        int m = s1.size(), n = s2.size();
        if (m + n != s3.size()) return false;
        vector<bool> dp(n + 1, false);
        for (int i = 0; i <= m; i++)
            for (int j = 0; j <= n; j++) {
                if (i == 0 && j == 0) dp[j] = true;
                else if (i == 0) dp[j] = dp[j-1] && s2[j-1] == s3[j-1];
                else if (j == 0) dp[j] = dp[j] && s1[i-1] == s3[i-1];
                else dp[j] = (dp[j] && s1[i-1] == s3[i+j-1]) || (dp[j-1] && s2[j-1] == s3[i+j-1]);
            }
        return dp[n];
    }
};""",
"java": """class Solution {
    public boolean isInterleave(String s1, String s2, String s3) {
        int m = s1.length(), n = s2.length();
        if (m + n != s3.length()) return false;
        boolean[] dp = new boolean[n + 1];
        for (int i = 0; i <= m; i++)
            for (int j = 0; j <= n; j++) {
                if (i == 0 && j == 0) dp[j] = true;
                else if (i == 0) dp[j] = dp[j-1] && s2.charAt(j-1) == s3.charAt(j-1);
                else if (j == 0) dp[j] = dp[j] && s1.charAt(i-1) == s3.charAt(i-1);
                else dp[j] = (dp[j] && s1.charAt(i-1) == s3.charAt(i+j-1)) || (dp[j-1] && s2.charAt(j-1) == s3.charAt(i+j-1));
            }
        return dp[n];
    }
}""",
"js": """var isInterleave = function(s1, s2, s3) {
    const m = s1.length, n = s2.length;
    if (m + n !== s3.length) return false;
    const dp = new Array(n + 1).fill(false);
    for (let i = 0; i <= m; i++)
        for (let j = 0; j <= n; j++) {
            if (i === 0 && j === 0) dp[j] = true;
            else if (i === 0) dp[j] = dp[j-1] && s2[j-1] === s3[j-1];
            else if (j === 0) dp[j] = dp[j] && s1[i-1] === s3[i-1];
            else dp[j] = (dp[j] && s1[i-1] === s3[i+j-1]) || (dp[j-1] && s2[j-1] === s3[i+j-1]);
        }
    return dp[n];
};"""
}

solutions["115"] = {
"cpp": """class Solution {
public:
    int numDistinct(string s, string t) {
        int m = s.size(), n = t.size();
        vector<unsigned long> dp(n + 1, 0);
        dp[0] = 1;
        for (int i = 1; i <= m; i++)
            for (int j = n; j >= 1; j--)
                if (s[i-1] == t[j-1]) dp[j] += dp[j-1];
        return dp[n];
    }
};""",
"java": """class Solution {
    public int numDistinct(String s, String t) {
        int m = s.length(), n = t.length();
        long[] dp = new long[n + 1];
        dp[0] = 1;
        for (int i = 1; i <= m; i++)
            for (int j = n; j >= 1; j--)
                if (s.charAt(i-1) == t.charAt(j-1)) dp[j] += dp[j-1];
        return (int)dp[n];
    }
}""",
"js": """var numDistinct = function(s, t) {
    const m = s.length, n = t.length;
    const dp = new Array(n + 1).fill(0);
    dp[0] = 1;
    for (let i = 1; i <= m; i++)
        for (let j = n; j >= 1; j--)
            if (s[i-1] === t[j-1]) dp[j] += dp[j-1];
    return dp[n];
};"""
}

solutions["72"] = {
"cpp": """class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        vector<int> dp(n + 1);
        iota(dp.begin(), dp.end(), 0);
        for (int i = 1; i <= m; i++) {
            int prev = dp[0]; dp[0] = i;
            for (int j = 1; j <= n; j++) {
                int tmp = dp[j];
                if (word1[i-1] == word2[j-1]) dp[j] = prev;
                else dp[j] = 1 + min({dp[j], dp[j-1], prev});
                prev = tmp;
            }
        }
        return dp[n];
    }
};""",
"java": """class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[] dp = new int[n + 1];
        for (int j = 0; j <= n; j++) dp[j] = j;
        for (int i = 1; i <= m; i++) {
            int prev = dp[0]; dp[0] = i;
            for (int j = 1; j <= n; j++) {
                int tmp = dp[j];
                if (word1.charAt(i-1) == word2.charAt(j-1)) dp[j] = prev;
                else dp[j] = 1 + Math.min(dp[j], Math.min(dp[j-1], prev));
                prev = tmp;
            }
        }
        return dp[n];
    }
}""",
"js": """var minDistance = function(word1, word2) {
    const m = word1.length, n = word2.length;
    const dp = Array.from({length: n+1}, (_, i) => i);
    for (let i = 1; i <= m; i++) {
        let prev = dp[0]; dp[0] = i;
        for (let j = 1; j <= n; j++) {
            const tmp = dp[j];
            if (word1[i-1] === word2[j-1]) dp[j] = prev;
            else dp[j] = 1 + Math.min(dp[j], dp[j-1], prev);
            prev = tmp;
        }
    }
    return dp[n];
};"""
}

solutions["312"] = {
"cpp": """class Solution {
public:
    int maxCoins(vector<int>& nums) {
        int n = nums.size();
        vector<int> a = {1};
        a.insert(a.end(), nums.begin(), nums.end());
        a.push_back(1);
        vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
        for (int len = 1; len <= n; len++)
            for (int l = 1; l <= n - len + 1; l++) {
                int r = l + len - 1;
                for (int k = l; k <= r; k++)
                    dp[l][r] = max(dp[l][r], dp[l][k-1] + a[l-1]*a[k]*a[r+1] + dp[k+1][r]);
            }
        return dp[1][n];
    }
};""",
"java": """class Solution {
    public int maxCoins(int[] nums) {
        int n = nums.length;
        int[] a = new int[n + 2];
        a[0] = a[n + 1] = 1;
        System.arraycopy(nums, 0, a, 1, n);
        int[][] dp = new int[n + 2][n + 2];
        for (int len = 1; len <= n; len++)
            for (int l = 1; l <= n - len + 1; l++) {
                int r = l + len - 1;
                for (int k = l; k <= r; k++)
                    dp[l][r] = Math.max(dp[l][r], dp[l][k-1] + a[l-1]*a[k]*a[r+1] + dp[k+1][r]);
            }
        return dp[1][n];
    }
}""",
"js": """var maxCoins = function(nums) {
    const n = nums.length;
    const a = [1, ...nums, 1];
    const dp = Array.from({length: n+2}, () => new Array(n+2).fill(0));
    for (let len = 1; len <= n; len++)
        for (let l = 1; l <= n - len + 1; l++) {
            const r = l + len - 1;
            for (let k = l; k <= r; k++)
                dp[l][r] = Math.max(dp[l][r], dp[l][k-1] + a[l-1]*a[k]*a[r+1] + dp[k+1][r]);
        }
    return dp[1][n];
};"""
}

solutions["10"] = {
"cpp": """class Solution {
public:
    bool isMatch(string s, string p) {
        int m = s.size(), n = p.size();
        vector<vector<bool>> dp(m+1, vector<bool>(n+1, false));
        dp[0][0] = true;
        for (int j = 2; j <= n; j++) if (p[j-1] == '*') dp[0][j] = dp[0][j-2];
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++) {
                if (p[j-1] == '*') {
                    dp[i][j] = dp[i][j-2] || ((p[j-2] == '.' || p[j-2] == s[i-1]) && dp[i-1][j]);
                } else {
                    dp[i][j] = dp[i-1][j-1] && (p[j-1] == '.' || p[j-1] == s[i-1]);
                }
            }
        return dp[m][n];
    }
};""",
"java": """class Solution {
    public boolean isMatch(String s, String p) {
        int m = s.length(), n = p.length();
        boolean[][] dp = new boolean[m+1][n+1];
        dp[0][0] = true;
        for (int j = 2; j <= n; j++) if (p.charAt(j-1) == '*') dp[0][j] = dp[0][j-2];
        for (int i = 1; i <= m; i++)
            for (int j = 1; j <= n; j++) {
                if (p.charAt(j-1) == '*')
                    dp[i][j] = dp[i][j-2] || ((p.charAt(j-2) == '.' || p.charAt(j-2) == s.charAt(i-1)) && dp[i-1][j]);
                else
                    dp[i][j] = dp[i-1][j-1] && (p.charAt(j-1) == '.' || p.charAt(j-1) == s.charAt(i-1));
            }
        return dp[m][n];
    }
}""",
"js": """var isMatch = function(s, p) {
    const m = s.length, n = p.length;
    const dp = Array.from({length: m+1}, () => new Array(n+1).fill(false));
    dp[0][0] = true;
    for (let j = 2; j <= n; j++) if (p[j-1] === '*') dp[0][j] = dp[0][j-2];
    for (let i = 1; i <= m; i++)
        for (let j = 1; j <= n; j++) {
            if (p[j-1] === '*')
                dp[i][j] = dp[i][j-2] || ((p[j-2] === '.' || p[j-2] === s[i-1]) && dp[i-1][j]);
            else
                dp[i][j] = dp[i-1][j-1] && (p[j-1] === '.' || p[j-1] === s[i-1]);
        }
    return dp[m][n];
};"""
}

solutions["329"] = {
"cpp": """class Solution {
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size(), result = 0;
        vector<vector<int>> memo(m, vector<int>(n, 0));
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                result = max(result, dfs(matrix, memo, i, j));
        return result;
    }
    int dfs(vector<vector<int>>& mat, vector<vector<int>>& memo, int i, int j) {
        if (memo[i][j]) return memo[i][j];
        int dirs[] = {0,1,0,-1,0};
        memo[i][j] = 1;
        for (int d = 0; d < 4; d++) {
            int ni = i+dirs[d], nj = j+dirs[d+1];
            if (ni>=0 && nj>=0 && ni<mat.size() && nj<mat[0].size() && mat[ni][nj] > mat[i][j])
                memo[i][j] = max(memo[i][j], 1 + dfs(mat, memo, ni, nj));
        }
        return memo[i][j];
    }
};""",
"java": """class Solution {
    int[][] memo;
    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
    public int longestIncreasingPath(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length, result = 0;
        memo = new int[m][n];
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                result = Math.max(result, dfs(matrix, i, j));
        return result;
    }
    int dfs(int[][] mat, int i, int j) {
        if (memo[i][j] != 0) return memo[i][j];
        memo[i][j] = 1;
        for (int[] d : dirs) {
            int ni = i+d[0], nj = j+d[1];
            if (ni>=0 && nj>=0 && ni<mat.length && nj<mat[0].length && mat[ni][nj] > mat[i][j])
                memo[i][j] = Math.max(memo[i][j], 1 + dfs(mat, ni, nj));
        }
        return memo[i][j];
    }
}""",
"js": """var longestIncreasingPath = function(matrix) {
    const m = matrix.length, n = matrix[0].length;
    const memo = Array.from({length: m}, () => new Array(n).fill(0));
    const dfs = (i, j) => {
        if (memo[i][j]) return memo[i][j];
        memo[i][j] = 1;
        for (const [di,dj] of [[0,1],[0,-1],[1,0],[-1,0]]) {
            const ni = i+di, nj = j+dj;
            if (ni>=0 && nj>=0 && ni<m && nj<n && matrix[ni][nj] > matrix[i][j])
                memo[i][j] = Math.max(memo[i][j], 1 + dfs(ni, nj));
        }
        return memo[i][j];
    };
    let result = 0;
    for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) result = Math.max(result, dfs(i, j));
    return result;
};"""
}


# ============================================
# GREEDY
# ============================================

solutions["53"] = {
"cpp": """class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int cur = 0, maxSum = nums[0];
        for (int n : nums) { cur = max(n, cur + n); maxSum = max(maxSum, cur); }
        return maxSum;
    }
};""",
"java": """class Solution {
    public int maxSubArray(int[] nums) {
        int cur = 0, maxSum = nums[0];
        for (int n : nums) { cur = Math.max(n, cur + n); maxSum = Math.max(maxSum, cur); }
        return maxSum;
    }
}""",
"js": """var maxSubArray = function(nums) {
    let cur = 0, maxSum = nums[0];
    for (const n of nums) { cur = Math.max(n, cur + n); maxSum = Math.max(maxSum, cur); }
    return maxSum;
};"""
}

solutions["55"] = {
"cpp": """class Solution {
public:
    bool canJump(vector<int>& nums) {
        int maxReach = 0;
        for (int i = 0; i <= maxReach && i < nums.size(); i++)
            maxReach = max(maxReach, i + nums[i]);
        return maxReach >= nums.size() - 1;
    }
};""",
"java": """class Solution {
    public boolean canJump(int[] nums) {
        int maxReach = 0;
        for (int i = 0; i <= maxReach && i < nums.length; i++)
            maxReach = Math.max(maxReach, i + nums[i]);
        return maxReach >= nums.length - 1;
    }
}""",
"js": """var canJump = function(nums) {
    let maxReach = 0;
    for (let i = 0; i <= maxReach && i < nums.length; i++)
        maxReach = Math.max(maxReach, i + nums[i]);
    return maxReach >= nums.length - 1;
};"""
}

solutions["45"] = {
"cpp": """class Solution {
public:
    int jump(vector<int>& nums) {
        int jumps = 0, curEnd = 0, farthest = 0;
        for (int i = 0; i < nums.size() - 1; i++) {
            farthest = max(farthest, i + nums[i]);
            if (i == curEnd) { jumps++; curEnd = farthest; }
        }
        return jumps;
    }
};""",
"java": """class Solution {
    public int jump(int[] nums) {
        int jumps = 0, curEnd = 0, farthest = 0;
        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == curEnd) { jumps++; curEnd = farthest; }
        }
        return jumps;
    }
}""",
"js": """var jump = function(nums) {
    let jumps = 0, curEnd = 0, farthest = 0;
    for (let i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        if (i === curEnd) { jumps++; curEnd = farthest; }
    }
    return jumps;
};"""
}

solutions["134"] = {
"cpp": """class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        int total = 0, tank = 0, start = 0;
        for (int i = 0; i < gas.size(); i++) {
            int diff = gas[i] - cost[i];
            total += diff; tank += diff;
            if (tank < 0) { start = i + 1; tank = 0; }
        }
        return total >= 0 ? start : -1;
    }
};""",
"java": """class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        int total = 0, tank = 0, start = 0;
        for (int i = 0; i < gas.length; i++) {
            int diff = gas[i] - cost[i];
            total += diff; tank += diff;
            if (tank < 0) { start = i + 1; tank = 0; }
        }
        return total >= 0 ? start : -1;
    }
}""",
"js": """var canCompleteCircuit = function(gas, cost) {
    let total = 0, tank = 0, start = 0;
    for (let i = 0; i < gas.length; i++) {
        const diff = gas[i] - cost[i];
        total += diff; tank += diff;
        if (tank < 0) { start = i + 1; tank = 0; }
    }
    return total >= 0 ? start : -1;
};"""
}

solutions["846"] = {
"cpp": """class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if (hand.size() % groupSize) return false;
        map<int, int> count;
        for (int h : hand) count[h]++;
        for (auto& [card, cnt] : count) {
            if (cnt > 0)
                for (int i = 0; i < groupSize; i++) {
                    count[card + i] -= cnt;
                    if (count[card + i] < 0) return false;
                }
        }
        return true;
    }
};""",
"java": """class Solution {
    public boolean isNStraightHand(int[] hand, int groupSize) {
        if (hand.length % groupSize != 0) return false;
        TreeMap<Integer, Integer> count = new TreeMap<>();
        for (int h : hand) count.merge(h, 1, Integer::sum);
        while (!count.isEmpty()) {
            int first = count.firstKey();
            for (int i = 0; i < groupSize; i++) {
                if (!count.containsKey(first + i)) return false;
                count.merge(first + i, -1, Integer::sum);
                if (count.get(first + i) == 0) count.remove(first + i);
            }
        }
        return true;
    }
}""",
"js": """var isNStraightHand = function(hand, groupSize) {
    if (hand.length % groupSize) return false;
    const count = new Map();
    for (const h of hand) count.set(h, (count.get(h) || 0) + 1);
    const sorted = [...count.keys()].sort((a,b) => a - b);
    for (const card of sorted) {
        const cnt = count.get(card);
        if (cnt > 0)
            for (let i = 0; i < groupSize; i++) {
                const c = count.get(card + i) || 0;
                if (c < cnt) return false;
                count.set(card + i, c - cnt);
            }
    }
    return true;
};"""
}

solutions["678"] = {
"cpp": """class Solution {
public:
    bool checkValidString(string s) {
        int lo = 0, hi = 0;
        for (char c : s) {
            lo += c == '(' ? 1 : -1;
            hi += c != ')' ? 1 : -1;
            if (hi < 0) return false;
            lo = max(lo, 0);
        }
        return lo == 0;
    }
};""",
"java": """class Solution {
    public boolean checkValidString(String s) {
        int lo = 0, hi = 0;
        for (char c : s.toCharArray()) {
            lo += c == '(' ? 1 : -1;
            hi += c != ')' ? 1 : -1;
            if (hi < 0) return false;
            lo = Math.max(lo, 0);
        }
        return lo == 0;
    }
}""",
"js": """var checkValidString = function(s) {
    let lo = 0, hi = 0;
    for (const c of s) {
        lo += c === '(' ? 1 : -1;
        hi += c !== ')' ? 1 : -1;
        if (hi < 0) return false;
        lo = Math.max(lo, 0);
    }
    return lo === 0;
};"""
}

solutions["1899"] = {
"cpp": """class Solution {
public:
    bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
        bool a = false, b = false, c = false;
        for (auto& t : triplets) {
            if (t[0] <= target[0] && t[1] <= target[1] && t[2] <= target[2]) {
                if (t[0] == target[0]) a = true;
                if (t[1] == target[1]) b = true;
                if (t[2] == target[2]) c = true;
            }
        }
        return a && b && c;
    }
};""",
"java": """class Solution {
    public boolean mergeTriplets(int[][] triplets, int[] target) {
        boolean a = false, b = false, c = false;
        for (int[] t : triplets) {
            if (t[0] <= target[0] && t[1] <= target[1] && t[2] <= target[2]) {
                if (t[0] == target[0]) a = true;
                if (t[1] == target[1]) b = true;
                if (t[2] == target[2]) c = true;
            }
        }
        return a && b && c;
    }
}""",
"js": """var mergeTriplets = function(triplets, target) {
    let a = false, b = false, c = false;
    for (const t of triplets) {
        if (t[0] <= target[0] && t[1] <= target[1] && t[2] <= target[2]) {
            if (t[0] === target[0]) a = true;
            if (t[1] === target[1]) b = true;
            if (t[2] === target[2]) c = true;
        }
    }
    return a && b && c;
};"""
}

solutions["763"] = {
"cpp": """class Solution {
public:
    vector<int> partitionLabels(string s) {
        int last[26] = {};
        for (int i = 0; i < s.size(); i++) last[s[i]-'a'] = i;
        vector<int> result;
        int start = 0, end = 0;
        for (int i = 0; i < s.size(); i++) {
            end = max(end, last[s[i]-'a']);
            if (i == end) { result.push_back(end - start + 1); start = i + 1; }
        }
        return result;
    }
};""",
"java": """class Solution {
    public List<Integer> partitionLabels(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i)-'a'] = i;
        List<Integer> result = new ArrayList<>();
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {
            end = Math.max(end, last[s.charAt(i)-'a']);
            if (i == end) { result.add(end - start + 1); start = i + 1; }
        }
        return result;
    }
}""",
"js": """var partitionLabels = function(s) {
    const last = {};
    for (let i = 0; i < s.length; i++) last[s[i]] = i;
    const result = [];
    let start = 0, end = 0;
    for (let i = 0; i < s.length; i++) {
        end = Math.max(end, last[s[i]]);
        if (i === end) { result.push(end - start + 1); start = i + 1; }
    }
    return result;
};"""
}

# ============================================
# INTERVALS
# ============================================

solutions["57"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> result;
        for (auto& i : intervals) {
            if (i[1] < newInterval[0]) result.push_back(i);
            else if (i[0] > newInterval[1]) { result.push_back(newInterval); newInterval = {INT_MAX, INT_MAX}; result.push_back(i); }
            else { newInterval[0] = min(newInterval[0], i[0]); newInterval[1] = max(newInterval[1], i[1]); }
        }
        if (newInterval[0] != INT_MAX) result.push_back(newInterval);
        return result;
    }
};""",
"java": """class Solution {
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> result = new ArrayList<>();
        for (int[] i : intervals) {
            if (i[1] < newInterval[0]) result.add(i);
            else if (i[0] > newInterval[1]) { result.add(newInterval); newInterval = new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE}; result.add(i); }
            else { newInterval[0] = Math.min(newInterval[0], i[0]); newInterval[1] = Math.max(newInterval[1], i[1]); }
        }
        if (newInterval[0] != Integer.MAX_VALUE) result.add(newInterval);
        return result.toArray(new int[0][]);
    }
}""",
"js": """var insert = function(intervals, newInterval) {
    const result = [];
    for (const i of intervals) {
        if (i[1] < newInterval[0]) result.push(i);
        else if (i[0] > newInterval[1]) { result.push(newInterval); newInterval = [Infinity, Infinity]; result.push(i); }
        else { newInterval[0] = Math.min(newInterval[0], i[0]); newInterval[1] = Math.max(newInterval[1], i[1]); }
    }
    if (newInterval[0] !== Infinity) result.push(newInterval);
    return result;
};"""
}

solutions["56"] = {
"cpp": """class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        vector<vector<int>> result = {intervals[0]};
        for (int i = 1; i < intervals.size(); i++) {
            if (intervals[i][0] <= result.back()[1])
                result.back()[1] = max(result.back()[1], intervals[i][1]);
            else result.push_back(intervals[i]);
        }
        return result;
    }
};""",
"java": """class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[0] - b[0]);
        List<int[]> result = new ArrayList<>();
        result.add(intervals[0]);
        for (int i = 1; i < intervals.length; i++) {
            int[] last = result.get(result.size()-1);
            if (intervals[i][0] <= last[1]) last[1] = Math.max(last[1], intervals[i][1]);
            else result.add(intervals[i]);
        }
        return result.toArray(new int[0][]);
    }
}""",
"js": """var merge = function(intervals) {
    intervals.sort((a,b) => a[0] - b[0]);
    const result = [intervals[0]];
    for (let i = 1; i < intervals.length; i++) {
        const last = result[result.length - 1];
        if (intervals[i][0] <= last[1]) last[1] = Math.max(last[1], intervals[i][1]);
        else result.push(intervals[i]);
    }
    return result;
};"""
}

solutions["435"] = {
"cpp": """class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), [](auto& a, auto& b) { return a[1] < b[1]; });
        int count = 0, prevEnd = INT_MIN;
        for (auto& i : intervals) {
            if (i[0] >= prevEnd) prevEnd = i[1];
            else count++;
        }
        return count;
    }
};""",
"java": """class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[1] - b[1]);
        int count = 0, prevEnd = Integer.MIN_VALUE;
        for (int[] i : intervals) {
            if (i[0] >= prevEnd) prevEnd = i[1];
            else count++;
        }
        return count;
    }
}""",
"js": """var eraseOverlapIntervals = function(intervals) {
    intervals.sort((a,b) => a[1] - b[1]);
    let count = 0, prevEnd = -Infinity;
    for (const i of intervals) {
        if (i[0] >= prevEnd) prevEnd = i[1];
        else count++;
    }
    return count;
};"""
}

solutions["252"] = {
"cpp": """class Solution {
public:
    bool canAttendMeetings(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end());
        for (int i = 1; i < intervals.size(); i++)
            if (intervals[i][0] < intervals[i-1][1]) return false;
        return true;
    }
};""",
"java": """class Solution {
    public boolean canAttendMeetings(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[0] - b[0]);
        for (int i = 1; i < intervals.length; i++)
            if (intervals[i][0] < intervals[i-1][1]) return false;
        return true;
    }
}""",
"js": """var canAttendMeetings = function(intervals) {
    intervals.sort((a,b) => a[0] - b[0]);
    for (let i = 1; i < intervals.length; i++)
        if (intervals[i][0] < intervals[i-1][1]) return false;
    return true;
};"""
}

solutions["253"] = {
"cpp": """class Solution {
public:
    int minMeetingRooms(vector<vector<int>>& intervals) {
        vector<int> starts, ends;
        for (auto& i : intervals) { starts.push_back(i[0]); ends.push_back(i[1]); }
        sort(starts.begin(), starts.end());
        sort(ends.begin(), ends.end());
        int rooms = 0, endPtr = 0;
        for (int i = 0; i < starts.size(); i++) {
            if (starts[i] < ends[endPtr]) rooms++;
            else endPtr++;
        }
        return rooms;
    }
};""",
"java": """class Solution {
    public int minMeetingRooms(int[][] intervals) {
        int[] starts = new int[intervals.length], ends = new int[intervals.length];
        for (int i = 0; i < intervals.length; i++) { starts[i] = intervals[i][0]; ends[i] = intervals[i][1]; }
        Arrays.sort(starts); Arrays.sort(ends);
        int rooms = 0, endPtr = 0;
        for (int i = 0; i < starts.length; i++) {
            if (starts[i] < ends[endPtr]) rooms++;
            else endPtr++;
        }
        return rooms;
    }
}""",
"js": """var minMeetingRooms = function(intervals) {
    const starts = intervals.map(i => i[0]).sort((a,b) => a-b);
    const ends = intervals.map(i => i[1]).sort((a,b) => a-b);
    let rooms = 0, endPtr = 0;
    for (let i = 0; i < starts.length; i++) {
        if (starts[i] < ends[endPtr]) rooms++;
        else endPtr++;
    }
    return rooms;
};"""
}

solutions["1851"] = {
"cpp": """class Solution {
public:
    vector<int> minInterval(vector<vector<int>>& intervals, vector<int>& queries) {
        sort(intervals.begin(), intervals.end());
        vector<int> sortedQ = queries;
        sort(sortedQ.begin(), sortedQ.end());
        unordered_map<int, int> result;
        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
        int i = 0;
        for (int q : sortedQ) {
            while (i < intervals.size() && intervals[i][0] <= q)
                pq.push({intervals[i][1] - intervals[i][0] + 1, intervals[i][1]}), i++;
            while (!pq.empty() && pq.top().second < q) pq.pop();
            result[q] = pq.empty() ? -1 : pq.top().first;
        }
        vector<int> ans;
        for (int q : queries) ans.push_back(result[q]);
        return ans;
    }
};""",
"java": """class Solution {
    public int[] minInterval(int[][] intervals, int[] queries) {
        Arrays.sort(intervals, (a,b) -> a[0] - b[0]);
        int[] sortedQ = queries.clone();
        Arrays.sort(sortedQ);
        Map<Integer, Integer> result = new HashMap<>();
        PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> a[0] - b[0]);
        int i = 0;
        for (int q : sortedQ) {
            while (i < intervals.length && intervals[i][0] <= q)
                pq.offer(new int[]{intervals[i][1] - intervals[i][0] + 1, intervals[i++][1]});
            while (!pq.isEmpty() && pq.peek()[1] < q) pq.poll();
            result.put(q, pq.isEmpty() ? -1 : pq.peek()[0]);
        }
        int[] ans = new int[queries.length];
        for (int j = 0; j < queries.length; j++) ans[j] = result.get(queries[j]);
        return ans;
    }
}""",
"js": """var minInterval = function(intervals, queries) {
    intervals.sort((a,b) => a[0] - b[0]);
    const sortedQ = [...queries].sort((a,b) => a - b);
    const result = new Map();
    const pq = []; // [{size, end}]
    let i = 0;
    for (const q of sortedQ) {
        while (i < intervals.length && intervals[i][0] <= q) {
            pq.push([intervals[i][1] - intervals[i][0] + 1, intervals[i][1]]); i++;
        }
        pq.sort((a,b) => a[0] - b[0]);
        while (pq.length && pq[0][1] < q) pq.shift();
        result.set(q, pq.length ? pq[0][0] : -1);
    }
    return queries.map(q => result.get(q));
};"""
}

# ============================================
# MATH & GEOMETRY
# ============================================

solutions["48"] = {
"cpp": """class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) swap(matrix[i][j], matrix[j][i]);
        for (auto& row : matrix) reverse(row.begin(), row.end());
    }
};""",
"java": """class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) { int t = matrix[i][j]; matrix[i][j] = matrix[j][i]; matrix[j][i] = t; }
        for (int[] row : matrix) { int l = 0, r = n-1; while (l < r) { int t = row[l]; row[l++] = row[r]; row[r--] = t; } }
    }
}""",
"js": """var rotate = function(matrix) {
    const n = matrix.length;
    for (let i = 0; i < n; i++)
        for (let j = i + 1; j < n; j++) [matrix[i][j], matrix[j][i]] = [matrix[j][i], matrix[i][j]];
    for (const row of matrix) row.reverse();
};"""
}

solutions["54"] = {
"cpp": """class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> result;
        int top = 0, bottom = matrix.size()-1, left = 0, right = matrix[0].size()-1;
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) result.push_back(matrix[top][j]); top++;
            for (int i = top; i <= bottom; i++) result.push_back(matrix[i][right]); right--;
            if (top <= bottom) { for (int j = right; j >= left; j--) result.push_back(matrix[bottom][j]); bottom--; }
            if (left <= right) { for (int i = bottom; i >= top; i--) result.push_back(matrix[i][left]); left++; }
        }
        return result;
    }
};""",
"java": """class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        int top = 0, bottom = matrix.length-1, left = 0, right = matrix[0].length-1;
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) result.add(matrix[top][j]); top++;
            for (int i = top; i <= bottom; i++) result.add(matrix[i][right]); right--;
            if (top <= bottom) { for (int j = right; j >= left; j--) result.add(matrix[bottom][j]); bottom--; }
            if (left <= right) { for (int i = bottom; i >= top; i--) result.add(matrix[i][left]); left++; }
        }
        return result;
    }
}""",
"js": """var spiralOrder = function(matrix) {
    const result = [];
    let top = 0, bottom = matrix.length-1, left = 0, right = matrix[0].length-1;
    while (top <= bottom && left <= right) {
        for (let j = left; j <= right; j++) result.push(matrix[top][j]); top++;
        for (let i = top; i <= bottom; i++) result.push(matrix[i][right]); right--;
        if (top <= bottom) { for (let j = right; j >= left; j--) result.push(matrix[bottom][j]); bottom--; }
        if (left <= right) { for (let i = bottom; i >= top; i--) result.push(matrix[i][left]); left++; }
    }
    return result;
};"""
}

solutions["73"] = {
"cpp": """class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        bool firstRow = false, firstCol = false;
        for (int j = 0; j < n; j++) if (matrix[0][j] == 0) firstRow = true;
        for (int i = 0; i < m; i++) if (matrix[i][0] == 0) firstCol = true;
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                if (matrix[i][j] == 0) { matrix[i][0] = 0; matrix[0][j] = 0; }
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                if (matrix[i][0] == 0 || matrix[0][j] == 0) matrix[i][j] = 0;
        if (firstRow) for (int j = 0; j < n; j++) matrix[0][j] = 0;
        if (firstCol) for (int i = 0; i < m; i++) matrix[i][0] = 0;
    }
};""",
"java": """class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        boolean firstRow = false, firstCol = false;
        for (int j = 0; j < n; j++) if (matrix[0][j] == 0) firstRow = true;
        for (int i = 0; i < m; i++) if (matrix[i][0] == 0) firstCol = true;
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                if (matrix[i][j] == 0) { matrix[i][0] = 0; matrix[0][j] = 0; }
        for (int i = 1; i < m; i++)
            for (int j = 1; j < n; j++)
                if (matrix[i][0] == 0 || matrix[0][j] == 0) matrix[i][j] = 0;
        if (firstRow) for (int j = 0; j < n; j++) matrix[0][j] = 0;
        if (firstCol) for (int i = 0; i < m; i++) matrix[i][0] = 0;
    }
}""",
"js": """var setZeroes = function(matrix) {
    const m = matrix.length, n = matrix[0].length;
    let firstRow = false, firstCol = false;
    for (let j = 0; j < n; j++) if (matrix[0][j] === 0) firstRow = true;
    for (let i = 0; i < m; i++) if (matrix[i][0] === 0) firstCol = true;
    for (let i = 1; i < m; i++)
        for (let j = 1; j < n; j++)
            if (matrix[i][j] === 0) { matrix[i][0] = 0; matrix[0][j] = 0; }
    for (let i = 1; i < m; i++)
        for (let j = 1; j < n; j++)
            if (matrix[i][0] === 0 || matrix[0][j] === 0) matrix[i][j] = 0;
    if (firstRow) for (let j = 0; j < n; j++) matrix[0][j] = 0;
    if (firstCol) for (let i = 0; i < m; i++) matrix[i][0] = 0;
};"""
}

solutions["202"] = {
"cpp": """class Solution {
public:
    bool isHappy(int n) {
        int slow = n, fast = n;
        do {
            slow = next(slow);
            fast = next(next(fast));
        } while (slow != fast);
        return slow == 1;
    }
    int next(int n) {
        int sum = 0;
        while (n) { sum += (n % 10) * (n % 10); n /= 10; }
        return sum;
    }
};""",
"java": """class Solution {
    public boolean isHappy(int n) {
        int slow = n, fast = n;
        do { slow = next(slow); fast = next(next(fast)); } while (slow != fast);
        return slow == 1;
    }
    int next(int n) { int sum = 0; while (n > 0) { sum += (n%10)*(n%10); n /= 10; } return sum; }
}""",
"js": """var isHappy = function(n) {
    const next = (n) => { let sum = 0; while (n) { sum += (n%10)**2; n = Math.floor(n/10); } return sum; };
    let slow = n, fast = n;
    do { slow = next(slow); fast = next(next(fast)); } while (slow !== fast);
    return slow === 1;
};"""
}

solutions["66"] = {
"cpp": """class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] < 9) { digits[i]++; return digits; }
            digits[i] = 0;
        }
        digits.insert(digits.begin(), 1);
        return digits;
    }
};""",
"java": """class Solution {
    public int[] plusOne(int[] digits) {
        for (int i = digits.length - 1; i >= 0; i--) {
            if (digits[i] < 9) { digits[i]++; return digits; }
            digits[i] = 0;
        }
        int[] result = new int[digits.length + 1];
        result[0] = 1;
        return result;
    }
}""",
"js": """var plusOne = function(digits) {
    for (let i = digits.length - 1; i >= 0; i--) {
        if (digits[i] < 9) { digits[i]++; return digits; }
        digits[i] = 0;
    }
    return [1, ...digits];
};"""
}

solutions["50"] = {
"cpp": """class Solution {
public:
    double myPow(double x, int n) {
        long p = abs((long)n);
        double result = 1;
        while (p) {
            if (p & 1) result *= x;
            x *= x;
            p >>= 1;
        }
        return n < 0 ? 1.0 / result : result;
    }
};""",
"java": """class Solution {
    public double myPow(double x, int n) {
        long p = Math.abs((long)n);
        double result = 1;
        while (p > 0) {
            if ((p & 1) == 1) result *= x;
            x *= x;
            p >>= 1;
        }
        return n < 0 ? 1.0 / result : result;
    }
}""",
"js": """var myPow = function(x, n) {
    let p = Math.abs(n), result = 1;
    while (p > 0) {
        if (p & 1) result *= x;
        x *= x;
        p >>= 1;
    }
    return n < 0 ? 1 / result : result;
};"""
}

solutions["43"] = {
"cpp": """class Solution {
public:
    string multiply(string num1, string num2) {
        int m = num1.size(), n = num2.size();
        vector<int> result(m + n, 0);
        for (int i = m-1; i >= 0; i--)
            for (int j = n-1; j >= 0; j--) {
                int mul = (num1[i]-'0') * (num2[j]-'0');
                int p1 = i+j, p2 = i+j+1;
                int sum = mul + result[p2];
                result[p2] = sum % 10;
                result[p1] += sum / 10;
            }
        string s;
        for (int d : result) if (!(s.empty() && d == 0)) s += to_string(d);
        return s.empty() ? "0" : s;
    }
};""",
"java": """class Solution {
    public String multiply(String num1, String num2) {
        int m = num1.length(), n = num2.length();
        int[] result = new int[m + n];
        for (int i = m-1; i >= 0; i--)
            for (int j = n-1; j >= 0; j--) {
                int mul = (num1.charAt(i)-'0') * (num2.charAt(j)-'0');
                int sum = mul + result[i+j+1];
                result[i+j+1] = sum % 10;
                result[i+j] += sum / 10;
            }
        StringBuilder sb = new StringBuilder();
        for (int d : result) if (!(sb.length() == 0 && d == 0)) sb.append(d);
        return sb.length() == 0 ? "0" : sb.toString();
    }
}""",
"js": """var multiply = function(num1, num2) {
    const m = num1.length, n = num2.length;
    const result = new Array(m + n).fill(0);
    for (let i = m-1; i >= 0; i--)
        for (let j = n-1; j >= 0; j--) {
            const mul = (num1[i]-'0') * (num2[j]-'0');
            const sum = mul + result[i+j+1];
            result[i+j+1] = sum % 10;
            result[i+j] += Math.floor(sum / 10);
        }
    const s = result.join('').replace(/^0+/, '');
    return s || '0';
};"""
}

solutions["2013"] = {
"cpp": """class DetectSquares {
    unordered_map<long long, int> count;
    vector<pair<int,int>> points;
public:
    void add(vector<int> point) {
        count[(long long)point[0] << 32 | point[1]]++;
        points.push_back({point[0], point[1]});
    }
    int count_fn(vector<int> point) {
        int px = point[0], py = point[1], result = 0;
        for (auto& [x, y] : points) {
            if (abs(px-x) != abs(py-y) || px == x || py == y) continue;
            long long k1 = (long long)x << 32 | py;
            long long k2 = (long long)px << 32 | y;
            result += (count.count(k1) ? count[k1] : 0) * (count.count(k2) ? count[k2] : 0);
        }
        return result;
    }
};""",
"java": """class DetectSquares {
    Map<Long, Integer> count = new HashMap<>();
    List<int[]> points = new ArrayList<>();
    public void add(int[] point) {
        long key = (long)point[0] << 32 | (point[1] & 0xFFFFFFFFL);
        count.merge(key, 1, Integer::sum);
        points.add(point);
    }
    public int count(int[] point) {
        int px = point[0], py = point[1], result = 0;
        for (int[] p : points) {
            int x = p[0], y = p[1];
            if (Math.abs(px-x) != Math.abs(py-y) || px == x || py == y) continue;
            long k1 = (long)x << 32 | (py & 0xFFFFFFFFL);
            long k2 = (long)px << 32 | (y & 0xFFFFFFFFL);
            result += count.getOrDefault(k1, 0) * count.getOrDefault(k2, 0);
        }
        return result;
    }
}""",
"js": """var DetectSquares = function() { this.count = new Map(); this.points = []; };
DetectSquares.prototype.add = function(point) {
    const key = point[0] + ',' + point[1];
    this.count.set(key, (this.count.get(key) || 0) + 1);
    this.points.push(point);
};
DetectSquares.prototype.count = function(point) {
    const [px, py] = point;
    let result = 0;
    for (const [x, y] of this.points) {
        if (Math.abs(px-x) !== Math.abs(py-y) || px === x || py === y) continue;
        result += (this.count.get(x+','+py) || 0) * (this.count.get(px+','+y) || 0);
    }
    return result;
};"""
}

# ============================================
# BIT MANIPULATION
# ============================================

solutions["136"] = {
"cpp": """class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int result = 0;
        for (int n : nums) result ^= n;
        return result;
    }
};""",
"java": """class Solution {
    public int singleNumber(int[] nums) {
        int result = 0;
        for (int n : nums) result ^= n;
        return result;
    }
}""",
"js": """var singleNumber = function(nums) {
    return nums.reduce((a, b) => a ^ b, 0);
};"""
}

solutions["191"] = {
"cpp": """class Solution {
public:
    int hammingWeight(uint32_t n) {
        int count = 0;
        while (n) { count++; n &= n - 1; }
        return count;
    }
};""",
"java": """class Solution {
    public int hammingWeight(int n) {
        int count = 0;
        while (n != 0) { count++; n &= n - 1; }
        return count;
    }
}""",
"js": """var hammingWeight = function(n) {
    let count = 0;
    while (n) { count++; n &= n - 1; }
    return count;
};"""
}

solutions["338"] = {
"cpp": """class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> dp(n + 1, 0);
        for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
        return dp;
    }
};""",
"java": """class Solution {
    public int[] countBits(int n) {
        int[] dp = new int[n + 1];
        for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
        return dp;
    }
}""",
"js": """var countBits = function(n) {
    const dp = new Array(n + 1).fill(0);
    for (let i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
    return dp;
};"""
}

solutions["190"] = {
"cpp": """class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t result = 0;
        for (int i = 0; i < 32; i++) { result = (result << 1) | (n & 1); n >>= 1; }
        return result;
    }
};""",
"java": """class Solution {
    public int reverseBits(int n) {
        int result = 0;
        for (int i = 0; i < 32; i++) { result = (result << 1) | (n & 1); n >>>= 1; }
        return result;
    }
}""",
"js": """var reverseBits = function(n) {
    let result = 0;
    for (let i = 0; i < 32; i++) { result = (result << 1) | (n & 1); n >>>= 1; }
    return result >>> 0;
};"""
}

solutions["268"] = {
"cpp": """class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size(), result = n;
        for (int i = 0; i < n; i++) result ^= i ^ nums[i];
        return result;
    }
};""",
"java": """class Solution {
    public int missingNumber(int[] nums) {
        int n = nums.length, result = n;
        for (int i = 0; i < n; i++) result ^= i ^ nums[i];
        return result;
    }
}""",
"js": """var missingNumber = function(nums) {
    let result = nums.length;
    for (let i = 0; i < nums.length; i++) result ^= i ^ nums[i];
    return result;
};"""
}

solutions["371"] = {
"cpp": """class Solution {
public:
    int getSum(int a, int b) {
        while (b != 0) {
            int carry = a & b;
            a = a ^ b;
            b = carry << 1;
        }
        return a;
    }
};""",
"java": """class Solution {
    public int getSum(int a, int b) {
        while (b != 0) { int carry = a & b; a = a ^ b; b = carry << 1; }
        return a;
    }
}""",
"js": """var getSum = function(a, b) {
    while (b !== 0) { const carry = a & b; a = a ^ b; b = carry << 1; }
    return a;
};"""
}

solutions["7"] = {
"cpp": """class Solution {
public:
    int reverse(int x) {
        int result = 0;
        while (x) {
            if (result > INT_MAX/10 || result < INT_MIN/10) return 0;
            result = result * 10 + x % 10;
            x /= 10;
        }
        return result;
    }
};""",
"java": """class Solution {
    public int reverse(int x) {
        int result = 0;
        while (x != 0) {
            if (result > Integer.MAX_VALUE/10 || result < Integer.MIN_VALUE/10) return 0;
            result = result * 10 + x % 10;
            x /= 10;
        }
        return result;
    }
}""",
"js": """var reverse = function(x) {
    const sign = x < 0 ? -1 : 1;
    let result = 0;
    x = Math.abs(x);
    while (x) { result = result * 10 + x % 10; x = Math.floor(x / 10); }
    result *= sign;
    return result >= -(2**31) && result <= 2**31 - 1 ? result : 0;
};"""
}


# ============================================
# HTML TRANSFORMATION
# ============================================

print(f"Loaded {len(solutions)} problem solutions")

# Read the original HTML
with open('/home/pranjal/Downloads/dsa-plan/index.html', 'r') as f:
    html_content = f.read()

# CSS to inject for language tabs
lang_css = """
        /* Language Tabs */
        .lang-selector {
            display: flex;
            gap: 0;
            margin: 14px 0 0 0;
            border-bottom: 2px solid var(--border);
        }
        .lang-tab {
            padding: 8px 18px;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
            transition: all 0.2s;
        }
        .lang-tab:hover { color: var(--text); }
        .lang-tab.active {
            color: var(--accent-light);
            border-bottom-color: var(--accent);
            background: rgba(99,102,241,0.05);
        }
        .lang-panel { display: none; }
        .lang-panel.active { display: block; }
        .lang-panel pre { margin-top: 0; border-top-left-radius: 0; border-top-right-radius: 0; }
        .global-lang {
            display: inline-flex;
            gap: 4px;
            margin-left: auto;
        }
        .global-lang-btn {
            padding: 5px 12px;
            border-radius: 6px;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--text-muted);
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 600;
            transition: all 0.2s;
        }
        .global-lang-btn:hover { border-color: var(--accent); color: var(--text); }
        .global-lang-btn.active {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }
"""

# JS to inject for language switching
lang_js = """
// Global language selector
let currentLang = localStorage.getItem('neetcode_lang') || 'python';

function setGlobalLang(lang) {
    currentLang = lang;
    localStorage.setItem('neetcode_lang', lang);
    // Update global buttons
    document.querySelectorAll('.global-lang-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.lang === lang);
    });
    // Update all tab groups
    document.querySelectorAll('.lang-tabs').forEach(group => {
        const tabs = group.querySelectorAll('.lang-tab');
        const panels = group.querySelectorAll('.lang-panel');
        tabs.forEach(t => t.classList.toggle('active', t.dataset.lang === lang));
        panels.forEach(p => p.classList.toggle('active', p.dataset.lang === lang));
        // If this lang doesn't exist in this group, default to first
        const hasLang = group.querySelector(`.lang-tab[data-lang="${lang}"]`);
        if (!hasLang && tabs.length) {
            tabs[0].classList.add('active');
            panels[0].classList.add('active');
        }
    });
}

function switchLang(btn) {
    setGlobalLang(btn.dataset.lang);
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => setGlobalLang(currentLang));
"""

# Inject CSS before </style>
html_content = html_content.replace('    </style>', lang_css + '    </style>')

# Add global language selector in the search container
global_selector = """
    <div class="global-lang">
        <button class="global-lang-btn active" data-lang="python" onclick="setGlobalLang('python')">Python</button>
        <button class="global-lang-btn" data-lang="cpp" onclick="setGlobalLang('cpp')">C++</button>
        <button class="global-lang-btn" data-lang="java" onclick="setGlobalLang('java')">Java</button>
        <button class="global-lang-btn" data-lang="js" onclick="setGlobalLang('js')">JavaScript</button>
    </div>
"""
html_content = html_content.replace('</div>\n\n<div class="container"', global_selector + '</div>\n\n<div class="container"')

# Inject JS before </script>
html_content = html_content.replace('// Init\nloadChecked();', lang_js + '\n// Init\nloadChecked();')

def escape_html(code):
    """Escape HTML entities in code"""
    return (code
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;'))

# Now transform each problem's code block
# Strategy: Find each problem by data-id, find its <pre> solution block, wrap with tabs
import re

def add_lang_tabs(match_html, problem_id, pre_block):
    """Wrap existing Python pre block with language tabs and add other languages"""
    if problem_id not in solutions:
        return pre_block  # No other languages available, keep as-is

    sol = solutions[problem_id]

    tabs_html = f'''<div class="lang-tabs">
<div class="lang-selector">
<button class="lang-tab active" data-lang="python" onclick="switchLang(this)">Python</button>
<button class="lang-tab" data-lang="cpp" onclick="switchLang(this)">C++</button>
<button class="lang-tab" data-lang="java" onclick="switchLang(this)">Java</button>
<button class="lang-tab" data-lang="js" onclick="switchLang(this)">JavaScript</button>
</div>
<div class="lang-panel active" data-lang="python">
{pre_block}</div>
<div class="lang-panel" data-lang="cpp">
<pre>{escape_html(sol["cpp"])}</pre></div>
<div class="lang-panel" data-lang="java">
<pre>{escape_html(sol["java"])}</pre></div>
<div class="lang-panel" data-lang="js">
<pre>{escape_html(sol["js"])}</pre></div>
</div>'''

    return tabs_html

# Process each problem
# We need to find each problem's solution <pre> block (not the dry-run ones)
# Strategy: Split by problem blocks, find the first <pre> in the problem-body that's NOT inside a .dry-run

lines = html_content.split('\n')
result_lines = []
i = 0
current_problem_id = None
in_problem_body = False
in_dry_run = False
found_solution_pre = False
pre_buffer = []
collecting_pre = False

while i < len(lines):
    line = lines[i]

    # Detect problem check with data-id
    id_match = re.search(r'data-id="(\d+)"', line)
    if id_match and 'problem-check' in line:
        current_problem_id = id_match.group(1)
        found_solution_pre = False

    # Detect problem-body start
    if 'class="problem-body"' in line:
        in_problem_body = True

    # Detect dry-run start
    if 'class="dry-run"' in line:
        in_dry_run = True

    # Detect dry-run end (approximate: closing div after dry-run)
    if in_dry_run and '</div>' in line and 'dry-run' not in line:
        # Check if this closes the dry-run div
        pass  # We'll use a simpler approach

    # Detect <pre> tag - if we're in a problem body but NOT in a dry-run, this is the solution pre
    if '<pre>' in line and in_problem_body and not found_solution_pre and not in_dry_run:
        # Start collecting the pre block
        collecting_pre = True
        pre_buffer = [line]
        if '</pre>' in line:
            # Single-line pre
            collecting_pre = False
            pre_content = '\n'.join(pre_buffer)
            tabbed = add_lang_tabs(None, current_problem_id, pre_content)
            result_lines.append(tabbed)
            found_solution_pre = True
            i += 1
            continue
        else:
            i += 1
            continue

    if collecting_pre:
        pre_buffer.append(line)
        if '</pre>' in line:
            collecting_pre = False
            pre_content = '\n'.join(pre_buffer)
            tabbed = add_lang_tabs(None, current_problem_id, pre_content)
            result_lines.append(tabbed)
            found_solution_pre = True
            i += 1
            continue
        else:
            i += 1
            continue

    # Track dry-run state more carefully
    if 'class="dry-run"' in line:
        in_dry_run = True
    # Simple heuristic: dry-run ends when we hit complexity-box or another section
    if in_dry_run and ('class="complexity-box"' in line or ('</div>' in line and line.strip() == '</div>')):
        # Could be end of dry-run, but let's use a different approach
        pass

    # Reset states when we exit a problem
    if '</div>' in line and line.strip() == '</div>' and in_problem_body:
        # Multiple closing divs - can't easily track this way
        pass

    result_lines.append(line)
    i += 1

html_content = '\n'.join(result_lines)

# Simpler and more reliable approach: use regex
# Actually, the line-by-line approach above has issues with dry-run detection.
# Let me use a regex-based approach instead.

# Re-read original
with open('/home/pranjal/Downloads/dsa-plan/index.html', 'r') as f:
    html_content = f.read()

# Inject CSS
html_content = html_content.replace('    </style>', lang_css + '    </style>')

# Add global selector
html_content = html_content.replace('</div>\n\n<div class="container"', global_selector + '</div>\n\n<div class="container"')

# Inject JS
html_content = html_content.replace('// Init\nloadChecked();', lang_js + '\n// Init\nloadChecked();')

# Now use regex: find each problem-check with data-id, then find the FIRST <pre>...</pre>
# that comes after it but BEFORE any <div class="dry-run"> or <div class="complexity-box">

# Split content by problem check markers
parts = re.split(r'(data-id="\d+")', html_content)

result = parts[0]
for j in range(1, len(parts), 2):
    data_id_part = parts[j]  # e.g., data-id="217"
    pid = re.search(r'"(\d+)"', data_id_part).group(1)
    content_part = parts[j + 1] if j + 1 < len(parts) else ''

    # Find the first <pre>...</pre> that's a solution code (not in dry-run)
    # The solution <pre> comes before the complexity-box or dry-run
    # Find the first <pre>...</pre> block
    pre_pattern = re.compile(r'(<pre>.*?</pre>)', re.DOTALL)

    # Find position of first dry-run
    dry_run_pos = content_part.find('class="dry-run"')
    complexity_pos = content_part.find('class="complexity-box"')

    # The solution pre is the first pre before dry-run/complexity
    cutoff = len(content_part)
    if dry_run_pos != -1: cutoff = min(cutoff, dry_run_pos)
    if complexity_pos != -1: cutoff = min(cutoff, complexity_pos)

    before_cutoff = content_part[:cutoff]
    after_cutoff = content_part[cutoff:]

    pre_match = pre_pattern.search(before_cutoff)

    if pre_match and pid in solutions:
        pre_block = pre_match.group(1)
        tabbed = add_lang_tabs(None, pid, pre_block)
        before_cutoff = before_cutoff[:pre_match.start()] + tabbed + before_cutoff[pre_match.end():]

    result += data_id_part + before_cutoff + after_cutoff

html_content = result

# Write the output
with open('/home/pranjal/Downloads/dsa-plan/index.html', 'w') as f:
    f.write(html_content)

print(f"Transformation complete! Added multi-language tabs for {len(solutions)} problems.")
print(f"Output written to index.html")

