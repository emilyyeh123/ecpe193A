# Project 5

## Overview
Write a Python program `cache.py` to simulate reading a direct-mapped cache or an n-way set associative cache. In this simulator, we are only interested in hits and misses, not in the word values being read. This program simulates the cache behavior (using the cache scheme selected by the user) for a sequence of memory accesses of 4-byte words, using 32-bit memory addresses.

 

## Input
Your program should use Argparse and support the following arguments:

`--type`:  The type of cache.  Valid options are `d` for direct-mapped and `s` for set associative cache. Note that the set associative cache must also specify the additional parameter `--nway` to configure the number of ways. 

`--cache_size`: The total cache size in bytes.  This value must be a power of 2. The cache size in bytes does not include the valid and tag bits.

`--block_size`: The size of a block in bytes. This value must be a power of 2. This block size does not include the valid and tag bits.

`--memfile`: The input text file that contains the sequence of memory accesses.  Each line of the input file is a memory address in hexadecimal format.

 

# Example usage: 

`python3 cache.py --type=d --cache_size=256 --block_size=64 --memfile=mem1.txt`

**Note**: When first launched, your program must verify if an input configuration is possible for a given cache type. If the input configuration is not possible, return an error and exit the program.

 

## Output
The program should produce a single output text file, cache.txt, containing the results of each memory address in a single line. For each memory access, a single line in the output text file should contain the following pipe (`|`) separated values:

`accessed memory address (hex) | tag bits (binary) | index bits (binary) |  hit (H) or miss (M) or unaligned (U)`

At the end of this output file, put a single line denoting the hit/miss rate:

`hit rate: calculated value`



## Provided Examples

Three demo input files are provided as examples: mem1.txt, mem2.txt, mem3.txt

Note that these text files contain addresses of 4-byte words. Therefore, the memory address must be divisible by 4. If this rule is broken, then it is unaligned access, which is costly. Mark it as unaligned (`U`) under the hit-or-miss section of the output.

One demo output file is provided:
- mem1out.txt: This represents the simulator run with a cache of size 128 bytes and 32 bytes per block on the input file mem1.txt. In other words:
`python3 cache.py --type=d --cache_size=128 --block_size=32 --memfile=mem1.txt`
