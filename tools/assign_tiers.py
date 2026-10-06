#!/usr/bin/env python3
"""
One-off migration: replace the boolean `core` flag with a priority `tier`.

Usage:  python tools/assign_tiers.py [--check]

The boolean was useless as a study filter — it ended up set on 128 of 150
problems, so the Sprint track filtered out only 22. A tier lets a plan of any
length take exactly as many problems as it has time for.

The inclusion rule, applied per category:

  tier 1  You cannot walk into an interview without it. Either it teaches a
          pattern no other problem in the list teaches, or it is the single
          most-asked instance of a very common pattern. Every category has at
          least one, so a tier-1-only plan still covers all 18 patterns.

  tier 2  Important reinforcement: a variant, a harder application, or a
          frequently-asked problem that is not pattern-unique.

  tier 3  Worth doing for depth, first to cut under time pressure. Mostly the
          rarely-asked hard problems and the pure design questions.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "dsa"

# problem id -> tier, grouped by category for reviewability
TIERS = {
    "arrays-hashing": {
        "217": 1,   # Contains Duplicate      - the simplest hash set
        "242": 1,   # Valid Anagram           - frequency counting
        "1":   1,   # Two Sum                 - complement lookup
        "49":  1,   # Group Anagrams          - canonical key / grouping
        "238": 1,   # Product Except Self     - prefix & suffix
        "347": 2,   # Top K Frequent          - bucket sort
        "128": 2,   # Longest Consecutive     - set membership trick
        "271": 3,   # Encode and Decode       - design, rarely asked
        "36":  3,   # Valid Sudoku            - constraint sets
    },
    "two-pointers": {
        "125": 1,   # Valid Palindrome        - converging pointers
        "15":  1,   # 3Sum                    - fix one + two pointers + dedupe
        "11":  1,   # Container With Most Water - the greedy discard argument
        "167": 2,   # Two Sum II              - good warm-up, subsumed by 3Sum
        "42":  2,   # Trapping Rain Water     - famous, hard
    },
    "sliding-window": {
        "121": 1,   # Best Time to Buy/Sell   - running minimum
        "3":   1,   # Longest Substring        - variable window
        "424": 2,   # Char Replacement        - window with a budget
        "567": 2,   # Permutation in String   - fixed window
        "76":  2,   # Minimum Window Substring - famous, hard
        "239": 3,   # Sliding Window Maximum  - monotonic deque, hard
    },
    "stack": {
        "20":  1,   # Valid Parentheses       - the canonical stack
        "739": 1,   # Daily Temperatures      - monotonic stack
        "155": 2,   # Min Stack               - design, common
        "150": 2,   # Evaluate RPN            - deferred operands
        "22":  2,   # Generate Parentheses    - pruned enumeration
        "853": 3,   # Car Fleet
        "84":  3,   # Largest Rectangle       - hard
    },
    "binary-search": {
        "704": 1,   # Binary Search           - the invariant
        "875": 1,   # Koko Eating Bananas     - search on the answer
        "153": 1,   # Find Minimum Rotated    - rotated arrays
        "33":  1,   # Search in Rotated       - rotated arrays, with a target
        "74":  2,   # Search a 2D Matrix      - flattening
        "981": 3,   # Time Based KV Store     - design
        "4":   3,   # Median of Two Sorted    - hard
    },
    "linked-list": {
        "206": 1,   # Reverse Linked List     - three-pointer rewiring
        "21":  1,   # Merge Two Sorted Lists  - dummy head
        "19":  1,   # Remove Nth From End     - fixed gap
        "141": 1,   # Linked List Cycle       - Floyd's
        "146": 1,   # LRU Cache               - very common design
        "143": 2,   # Reorder List            - composition of three techniques
        "138": 2,   # Copy List Random Pointer - map from original to copy
        "2":   2,   # Add Two Numbers         - carry simulation
        "23":  2,   # Merge K Sorted Lists    - pairwise merge
        "287": 3,   # Find the Duplicate      - the array-as-list reduction
        "25":  3,   # Reverse in k-Group      - hard bookkeeping
    },
    "trees": {
        "226": 1,   # Invert Binary Tree      - the simplest recursion
        "104": 1,   # Maximum Depth           - information flowing up
        "102": 1,   # Level Order             - BFS
        "98":  1,   # Validate BST            - information flowing down
        "235": 1,   # LCA of BST              - using the ordering
        "543": 2,   # Diameter                - return one thing, track another
        "110": 2,   # Balanced                - the sentinel trick
        "100": 2,   # Same Tree               - parallel traversal
        "199": 2,   # Right Side View         - per-level selection
        "230": 2,   # Kth Smallest in BST     - inorder with early exit
        "105": 2,   # Construct from Pre/In   - reconstruction
        "124": 2,   # Max Path Sum            - famous hard
        "572": 3,   # Subtree of Another Tree
        "1448": 3,  # Count Good Nodes
        "297": 3,   # Serialize/Deserialize   - design
    },
    "tries": {
        "208": 1,   # Implement Trie          - the structure itself
        "211": 2,   # Add and Search Words    - wildcard DFS
        "212": 3,   # Word Search II          - hard
    },
    "heap": {
        "215": 1,   # Kth Largest in Array    - quickselect vs size-k heap
        "295": 1,   # Median from Stream      - two heaps
        "703": 2,   # Kth Largest in Stream   - size-k heap
        "973": 2,   # K Closest Points        - max-heap of size k
        "621": 2,   # Task Scheduler          - greedy scheduling
        "1046": 3,  # Last Stone Weight
        "355": 3,   # Design Twitter          - design
    },
    "backtracking": {
        "78":  1,   # Subsets                 - the template
        "39":  1,   # Combination Sum         - reuse allowed
        "46":  1,   # Permutations            - used set
        "79":  1,   # Word Search             - grid backtracking
        "90":  2,   # Subsets II              - duplicate skip
        "40":  2,   # Combination Sum II      - both constraints at once
        "17":  2,   # Letter Combinations     - cartesian product
        "131": 3,   # Palindrome Partitioning
        "51":  3,   # N-Queens                - constraint backtracking
    },
    "graphs": {
        "200": 1,   # Number of Islands       - flood fill
        "133": 1,   # Clone Graph             - map from original to copy
        "994": 1,   # Rotting Oranges         - multi-source BFS
        "207": 1,   # Course Schedule         - cycle detection
        "323": 1,   # Connected Components    - union-find
        "695": 2,   # Max Area of Island      - flood fill returning a value
        "417": 2,   # Pacific Atlantic        - reverse the question
        "210": 2,   # Course Schedule II      - topological order
        "261": 2,   # Graph Valid Tree        - union-find properties
        "684": 2,   # Redundant Connection    - union-find on a stream
        "127": 2,   # Word Ladder             - implicit graph BFS
        "286": 3,   # Walls and Gates
        "130": 3,   # Surrounded Regions
    },
    "advanced-graphs": {
        "743": 1,   # Network Delay Time      - Dijkstra
        "1584": 2,  # Min Cost Connect Points - MST
        "787": 2,   # Cheapest Flights K Stops - Bellman-Ford
        "269": 2,   # Alien Dictionary        - inferred topological sort
        "332": 3,   # Reconstruct Itinerary   - Eulerian path
        "778": 3,   # Swim in Rising Water    - bottleneck Dijkstra
    },
    "1d-dp": {
        "70":  1,   # Climbing Stairs         - the first DP
        "198": 1,   # House Robber            - take or skip
        "322": 1,   # Coin Change             - unbounded knapsack
        "139": 1,   # Word Break              - boolean DP over prefixes
        "300": 1,   # LIS                     - very common
        "746": 2,   # Min Cost Climbing Stairs
        "213": 2,   # House Robber II         - circular reduction
        "5":   2,   # Longest Palindromic Substring
        "647": 2,   # Palindromic Substrings
        "91":  2,   # Decode Ways
        "152": 2,   # Max Product Subarray    - incomplete-state lesson
        "416": 2,   # Partition Equal Subset  - 0/1 knapsack
    },
    "2d-dp": {
        "62":  1,   # Unique Paths            - grid DP
        "1143": 1,  # LCS                     - the two-sequence template
        "72":  1,   # Edit Distance           - very common
        "518": 2,   # Coin Change II          - the loop-order lesson
        "309": 3,   # Stock with Cooldown     - state machine
        "494": 3,   # Target Sum              - the reduction
        "97":  3,   # Interleaving String
        "329": 3,   # Longest Increasing Path
        "115": 3,   # Distinct Subsequences
        "312": 3,   # Burst Balloons          - interval DP
        "10":  3,   # Regex Matching          - hard
    },
    "greedy": {
        "53":  1,   # Maximum Subarray        - Kadane's
        "55":  1,   # Jump Game               - reachability frontier
        "45":  2,   # Jump Game II            - greedy BFS layers
        "134": 2,   # Gas Station             - reset greedy
        "763": 2,   # Partition Labels        - last occurrence
        "846": 3,   # Hand of Straights
        "1899": 3,  # Merge Triplets
        "678": 3,   # Valid Parenthesis String - range tracking
    },
    "intervals": {
        "56":  1,   # Merge Intervals         - sort by start
        "253": 1,   # Meeting Rooms II        - concurrency
        "57":  2,   # Insert Interval
        "435": 2,   # Non-overlapping         - activity selection
        "252": 2,   # Meeting Rooms
        "1851": 3,  # Min Interval per Query  - offline queries
    },
    "math": {
        "48":  1,   # Rotate Image            - decomposition
        "54":  2,   # Spiral Matrix           - boundary shrinking
        "73":  2,   # Set Matrix Zeroes       - encode state in the input
        "50":  2,   # Pow(x, n)               - fast exponentiation
        "202": 3,   # Happy Number
        "66":  3,   # Plus One
        "43":  3,   # Multiply Strings
        "2013": 3,  # Detect Squares
    },
    "bit-manipulation": {
        "136": 1,   # Single Number           - XOR cancellation
        "191": 1,   # Number of 1 Bits        - n & (n-1)
        "338": 2,   # Counting Bits           - bit DP
        "268": 2,   # Missing Number          - XOR or sum
        "190": 3,   # Reverse Bits
        "371": 3,   # Sum of Two Integers
        "7":   3,   # Reverse Integer
    },
}


def main(argv):
    check_only = "--check" in argv
    index = json.loads((CONTENT / "_index.json").read_text(encoding="utf-8"))
    counts = {1: 0, 2: 0, 3: 0}
    per_cat = []
    errors = []

    for entry in sorted(index, key=lambda e: e["order"]):
        slug = entry["slug"]
        path = CONTENT / f"{slug}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        wanted = TIERS.get(slug)
        if wanted is None:
            errors.append(f"{slug}: no tier mapping")
            continue

        ids = {p["id"] for p in data["problems"]}
        missing = ids - set(wanted)
        extra = set(wanted) - ids
        if missing:
            errors.append(f"{slug}: no tier assigned for {sorted(missing)}")
        if extra:
            errors.append(f"{slug}: tier given for unknown ids {sorted(extra)}")

        local = {1: 0, 2: 0, 3: 0}
        for p in data["problems"]:
            tier = wanted.get(p["id"])
            if tier is None:
                continue
            p["tier"] = tier
            p.pop("core", None)          # retire the boolean
            counts[tier] += 1
            local[tier] += 1
        per_cat.append((slug, len(data["problems"]), local))

        if not check_only and not errors:
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    print(f"{'category':<20}{'probs':>6}{'T1':>5}{'T2':>5}{'T3':>5}")
    print("-" * 41)
    for slug, n, local in per_cat:
        print(f"{slug:<20}{n:>6}{local[1]:>5}{local[2]:>5}{local[3]:>5}")
    print("-" * 41)
    total = sum(counts.values())
    print(f"{'TOTAL':<20}{total:>6}{counts[1]:>5}{counts[2]:>5}{counts[3]:>5}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  {e}")
        return 1
    if total != 150:
        print(f"\nERROR: expected 150 problems, assigned {total}")
        return 1
    print("\nwrote tiers" if not check_only else "\ncheck only, nothing written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
