# Unsolvable Instances of the Missionaries and Cannibals Problem

This document outlines known conditions under which the Missionaries and Cannibals problem (with `n` missionaries and `n` cannibals, and a boat with capacity `k`) has no solution. The standard rules apply: missionaries cannot be outnumbered by cannibals on either bank at any time.

## General Conditions

The solvability of the problem depends significantly on the boat capacity `k` relative to the number of missionary/cannibal pairs `n`.

### Boat Capacity `k = 1`

*   If `n > 1` (e.g., 2 missionaries and 2 cannibals), the problem is generally considered unsolvable.
    *   **Reasoning (informal):** To move anyone to the other side, the boat must return. If only one person can be in the boat, to make progress, you'd send one person over. Then that person must row back to pick up others. If this person is a missionary, they might leave a missionary outnumbered on the starting bank. If a cannibal, similar issues arise, or no progress is made towards moving missionaries. For `n=1`, it is solvable in 3 moves (M C | ---, B  -> C | M, B  ->  --- | M C, B).

### Boat Capacity `k = 2`

*   The problem is solvable for `n=1, 2, 3`.
    *   `n=3` (3 missionaries, 3 cannibals) is the classic problem, solvable in 11 moves.
    *   `n=2` (2 missionaries, 2 cannibals) is solvable in 5 moves.
*   If `n >= 4` (e.g., 4 missionaries and 4 cannibals), the problem has no solution.
    *   **Source:** Wikipedia, citing various mathematical analyses of the problem. This is a well-established result.

### Boat Capacity `k = 3`

*   The problem is solvable for `n` up to 5 (i.e., `n=1, 2, 3, 4, 5`).
    *   For example, with 3 missionaries and 3 cannibals (`n=3`), a boat of capacity 3 makes the problem solvable in fewer moves than with `k=2`.
*   The exact point at which it becomes unsolvable for `k=3` (e.g., for `n=6` or higher) is not immediately clear from general summaries but is likely detailed in specialized publications (e.g., Pressman & Singmaster, 1989).
    *   *Further research might be needed for the specific `n` where `k=3` becomes unsolvable.*

### Boat Capacity `k = 4` (or more)

*   If the boat can hold 4 or more people (`k >= 4`), any number of missionary/cannibal pairs (`n`) can be safely transported.
    *   **Source:** Wikipedia, citing various mathematical analyses.
    *   **Reasoning (informal):** With a large enough boat, one can always ensure a safe ratio of missionaries to cannibals in the boat and on both banks during transfers. For example, sending 2 missionaries and 2 cannibals (if n >= 2) or a similar safe group.

## Summary Table

| Boat Capacity (k) | Number of M/C Pairs (n) | Solvable?                 | Notes                                       |
|-------------------|---------------------------|---------------------------|---------------------------------------------|
| 1                 | 1                         | Yes                       | 3 moves                                     |
| 1                 | `n > 1`                   | No (Generally)            | Cannot make progress without violations     |
| 2                 | 1, 2, 3                   | Yes                       | `n=3` is 11 moves; `n=2` is 5 moves       |
| 2                 | `n >= 4`                  | No                        | Established result                          |
| 3                 | 1, 2, 3, 4, 5             | Yes                       |                                             |
| 3                 | `n >= 6` (?)              | Needs Confirmation        | Unsolvable beyond a certain `n`             |
| `k >= 4`          | Any `n`                   | Yes                       | Sufficient capacity to maintain safe ratios |

**Note:** These conditions assume the standard problem where the number of missionaries equals the number of cannibals (`M=C=n`) and the goal is to move everyone from one bank to the other. Variations (like unequal numbers of M and C, or islands) change these conditions.
