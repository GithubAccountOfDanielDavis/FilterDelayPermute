# FilterDelayPermute

## What is this?
This repo is my testing and analysis of a hashing algorithm provided by [larsupilami73](https://www.reddit.com/user/larsupilami73) on Reddit. The original challenge can be found [here](https://www.reddit.com/r/codes/comments/e9uctm/challenge_delayfilterpermute/). If the included pastebin or original post go down, fdp_original.py is a mostly unaltered version of the code and includes the secret message to be decoded as proof of completing the challenge.

## Quickstart
If you wanna jump right in, you can run any of the .py files and check out their output. fdp_numpy.py and fdp_original.py give you an idea of the intended hashed output and run_tests.py will make sure the results are correct for our one measly case and do benchmarking as well.

## Optimizations
I've performed several rounds of optimizations on the original code in order to get to know it better. All in all, my version makes much better use of numpy's parallel computation features and is nearly an order of magnitude faster (4 vs 26 milliseconds on my machine). I've also written a few versions in c, but fairly benchmarking them would involve getting into the c apis or compiling via cython and I'm already in too deep, so I haven't included them here.

The biggest change I've made is in when the permutations happen. The first thing I did was remove the abstraction of the Delay class and inline the statements to replace its method calls. That made it much clearer that at the end of every loop, we were writing to the current index and reading from the next one. For conceptualization purposes, I preferred to do the reading at the beginning of each loop and write to the same index at the end of it. This lent itself to parallelization later, but it also moved the permutation step from the end to the beginning of the loop. So my version is not actually FilterDelayPermute, but PermuteFilterDelay. It also requires us to unpermute the first zero within the starting block for the sake of backwards compatibility as the original didn't permute index 0 (or index 40 in its case). The rest of the changes come down to optimizing for numpy.

## The algorithm
Every block has an array of echoes and its last encoding state. We get our initial block by putting our plaintext ascii secret at the end of a zeroed-out echoes array. The first index of that array can be unpermuted for backwards compatibility. Then we encode that block an arbitrary numbers of times, 20 by default.

Here's what moving from the current block to the next block (1 iteration) would look like for a block with a delay length of n:

```
current
block
 │ │
 │ └echoes → [   [0]           [1]     …   [n - 2]       [n - 1] ]
 │                ↓             ↓             ↓             ↓  
 │           ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
 │           │ PERMUTE │   │ PERMUTE │ … │ PERMUTE │   │ PERMUTE │
 │           └─────────┘   └─────────┘   └─────────┘   └─────────┘
 │                ↓             ↓             ↓             ↓
 │           ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
 └───state → │ FILTER  │ → │ FILTER  │ … │ FILTER  │ → │ FILTER  │ → state───┐
             └─────────┘   └─────────┘   └─────────┘   └─────────┘           │
                  ↓             ↓             ↓             ↓                │
             ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐           │
             │  DELAY  │   │  DELAY  │ … │  DELAY  │   │  DELAY  │           │
             └─────────┘   └─────────┘   └─────────┘   └─────────┘           │
                  ↓             ↓             ↓             ↓                │
             [   [0]           [1]     …   [n - 2]       [n - 1] ] → echoes┐ │
                                                                           │ │
                                                                           next
                                                                          block
```
