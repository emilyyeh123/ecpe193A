'''
PROJECT 5: PYTHON CACHE SIMULATOR
Write a Python program cache.py to simulate reading a direct-mapped cache or an n-way set associative cache.
In this simulator, we are only interested in hits and misses, not in the word values being read.
This program simulates the cache behavior (using the cache scheme selected by the user) for a sequence of memory accesses of 4-byte words, using 32-bit memory addresses.

COMMAND TO RUN THIS PROGRAM: 
python3 cache.py --type=d --cache_size=256 --block_size=64 --memfile=mem1.txt

*Valid Types:
> "d" for direct-mapped cache
> "s" for set associative cache
    > must have additional "--nway" parameter specifying number of ways

*Cache size is total cache size in bytes and MUST be a power of 2 (size does not include valid & tag bits)

*Block size is size of a block in bytes and MUST be a power of 2 (size does not include valid and tag bits)

*memfile is the input text file containing the sequence of memory accesses where each line is a memory address in hexadecimal
'''

import argparse
import math

def main():
    outStr = ""
    memAddress = 0 # store current address in binary
    addressSize = 32 # 32-bit memory addresses
    byteOffset = 2 # byte offset is assumed to be 2 bits
    wordOffset = 0
    numTagBits = 0
    numIndexBits = 0
    currTagBits = ""
    currIndexBits = ""
    cache = [] # list of dictionaries, each dictionary is an additional set
    hit = False # 0 if miss, 1 if hit
    hitCount = 0 # count number of hits
    addressCount = 0 # count number of addresses to use for hit rate

    parser = argparse.ArgumentParser(description = "Project 5: Python Cache Simulator")
    parser.add_argument("--type", required = True, help = "Valid Cache Types: d for direct-mapped and s for set associative")
    parser.add_argument("--nway", required = False, help = "specify number of ways if set associative cache")
    parser.add_argument("--cache_size", required = True, help = "cache size in bytes, must be power of 2 (does not include valid & tag bits)")
    parser.add_argument("--block_size", required = True, help = "block size in bytes, must be power of 2 (does not include valid & tag bits)")
    parser.add_argument("--memfile", required = True, help = "txt file containing sequence of memory accesses where each line is a memory address in hexadecimal")
    args = parser.parse_args()

    # program must first verify if an input configuration is possible based on cache type
    # return an error and exit program if invalid input arguments
    if args.type == "d" and args.nway is not None:
        print("INVALID ARGUMENTS!\n> Direct-Mapped cache should not have nway argument.")
        exit()
    elif args.type == "s":
        try:
            # if nway argument can convert to int, argument is valid
            args.nway = int(args.nway)
        except:
            pass
        if type(args.nway) is not int or args.nway <= 1:
            print("INVALID ARGUMENTS!\n> Set Associative cache should have an integer-type nway argument >= 2.")
            exit()

    # verify cache & block size are powers of 2
    # use bit manipulation: (n & (n-1) == 0) and n!=0
    #    >> True if n is a power of 2
    # Explanation:
    # - powers of 2 have exactly 1 bit set to 1
    # - subtract 1 from a power of 2 and all bits will flip
    # - AND the two inverse values to produce a 0
    # - only exception: zero
    try:
        # typecast sizes to int or throw error and exit if not possible
        args.cache_size = int(args.cache_size)
        args.block_size = int(args.block_size)
    except:
        print("INVALID ARGUMENTS!\n> Cache Size and Block Size must be integer values.")
        exit()
    if not( (args.cache_size & (args.cache_size-1) == 0) and args.cache_size!=0 ): # if cache size not a power of 2
        print("INVALID ARGUMENTS!\n> Cache Size must be a power of 2.")
        exit()
    if not( (args.block_size & (args.block_size-1) == 0) and args.block_size!=0 ): # if block size not a power of 2
        print("INVALID ARGUMENTS!\n> Block Size must be a power of 2.")
        exit()

    # get number of index, tag, and word bits
    numIndexBits = int( math.log2(args.cache_size) - math.log2(args.block_size) )
    wordOffset = int( math.log2(args.block_size/4) ) # number of words per block = block size / 4 bytes per word
    numTagBits = addressSize - numIndexBits -  wordOffset - byteOffset
    print(numTagBits, numIndexBits, wordOffset, "\n")

    # set up list of dictionaries
    if args.nway is None:
        cache.append({})
    else:
        for i in range(args.nway):
            cache.append({})

    # open file
    memFileIn = open(args.memfile, "r")

    for line in memFileIn:
        hit = False
        addressCount += 1
        outStr += line.strip() + "|"

        # convert memory address from hex to binary
        memAddress = int(line.strip(), 16) # convert hex to decimal
        memAddress = f'{memAddress:032b}' # convert decimal to 32-bit binary (string type)

        print(line.strip(), memAddress) #, end = " ")

        # print tag bits and index bits
        currTagBits = memAddress[0:numTagBits]
        currIndexBits = memAddress[numTagBits:numTagBits+numIndexBits]
        outStr += currTagBits + "|" + currIndexBits + "|"
        #print(line.strip(), currTagBits, currIndexBits, end = "  ||  ")

        for thisDict in cache: # iterate through all sets
            if currIndexBits in thisDict: # if index (key) exists,
                # check if tag bits match
                if currTagBits == thisDict[currIndexBits]: # if match, hit and exit loop
                    hit = True
                    #print("HIT!")
                    break
                # if no match, continue to next dictionary and repeat
                elif thisDict == cache[-1]:
                    # if no match, but this is the last possible set, 
                    # replace tag (value) at index (key), miss, and complete loop
                    thisDict = cache[0]
                    thisDict[currIndexBits] = currTagBits
                    #print("iterated through all dictionaries and no hits")
            else:
                # if index does not yet exist in current dictionary,
                # add index and tag as key, value pair, miss, and exit loop
                thisDict[currIndexBits] = currTagBits
                #print("index does not yet exist in current dict")
                break

        # print hit, miss, or unaligned
        if not (memAddress[-2:] == "00"): # if not divisible by 4
            # alignment: aligned if number is divisible by 4 (last two bits of address is 00)
            outStr += "U"
        elif hit:
            outStr += "HIT"
            hitCount += 1
        else:
            outStr += "MISS"

        outStr += "\n"

    memFileIn.close()

    # calculate hit rate
    hitRate = f'{(hitCount/addressCount):.1%}'
    outStr += "\nHit Rate: " + hitRate + "\n"

    # output to cache.txt file
    cacheOutFile = open("cache.txt", "w")
    cacheOutFile.write(outStr)
    cacheOutFile.close()

if __name__ == "__main__":
    main()
