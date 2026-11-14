# The Drunken Mario Adventures

Flag: `SIGMOID_TANH`

## Solution

The level has 20 coins in one row at x = 7, 12, 17, 25, 32, 43, 61, 66, 73, 80, 93, 101, 110, 118, 130, 157, 172, 195, 201, 206.

A fully trained champion runs to the flagpole and takes exactly 7 of them: 7, 17, 80, 101, 110, 118, 172.
It walks past the other 13, even when they lie right on its path. This stays the same for 100+ generations after the first win, so it is the final behaviour.

Writing the coins left to right as 1 (taken) or 0 (skipped) and splitting them into groups of 5 bits (A=1 ... Z=26):

```
10100 00001 01110 01000
  20     1    14     8
   T     A     N     H
```

The word is TANH, so the flag is `SIGMOID_TANH`.

Why it happens: the fitness function in the program has a 1 or 0 for every coin. Coins with 1 are rewarded and coins with 0 are penalised, so evolution teaches the agent to take exactly those coins. The table read from the running program is `1 0 1 0 0 0 0 0 0 1 0 1 1 1 0 0 1 0 0 0`, the same bits.

## How to reproduce

1. Run `marathon-lab-linux-x86_64` (after `chmod +x`) or `marathon-lab-windows-x86_64.exe`.
2. Let it train until the best agent reaches the flagpole and keeps the same run for a while (a few minutes).
3. Press BEST ONLY and watch the run. For each of the 20 coins in the low row, left to right, note whether Mario takes it (1) or skips it (0).
4. Split the 20 bits into groups of 5 and convert each group to a letter (A=1 ... Z=26). The result is TANH.
