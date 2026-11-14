# The Drunken Mario Adventures (Australia)

Flag: `SIGMOID_TANH`

There is no code to write. The program trains a Mario agent with evolution. We let it train until the best agent
reaches the flagpole and its run stops changing. Then we watched which of the 20 coins in the low row it takes.

It always takes the same 7 coins and skips the other 13, even ones right on its path. That is because the fitness
function holds a hidden 0/1 for each coin. Writing the coins left to right as 1 = taken, 0 = skipped, and reading
groups of 5 bits as letters (A = 1 ... Z = 26) gives TANH.

```
coins taken:  1 0 1 0 0 | 0 0 0 0 1 | 0 1 1 1 0 | 0 1 0 0 0
binary:          20     |     1     |    14     |     8
letter:           T     |     A     |     N     |     H        -> SIGMOID_TANH
```

Reproduce: run `marathon-lab-*`, wait for a stable winner, press BEST ONLY, note taken (1) / skipped (0) coins.
