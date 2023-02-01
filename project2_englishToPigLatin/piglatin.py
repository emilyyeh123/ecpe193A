'''
THIS PROGRAM IS DESIGNED TO BE AN ENGLISH TO PIG LATIN CONVERTER.
USE THE FOLLOWING COMMAND TO RUN THE PROGRAM:
python3 piglatin.py --input data.txt --output data_out.txt



PIG LATIN RULES
1. if a word starts with a consonant and a vowel, put the first letter of the word at the end of the word and add "ay" (EXAMPLE: happy = appyh + ay = appyhay)
2. If a word starts with two consonants, move the two consonants to the end of the word and add "ay" (EXAMPLE: Child = ildch + ay = ildchay)
3. If a word starts with a vowel, add the word "way" at the end of the word (EXAMPLE: Awesome = Awesome + way = awesomeway)
4. The output file must retain all of the punctuations used in the input text file

'''

import argparse
import re

vowels = ["a","e","i","o","u"]

# return the rule number to perform on the word
def ruleNum(word):
    word = word.lower()

    # test if first and second letters are vowels or consonants
    firstIsVowel = 0
    secondIsVowel = 0
    for v in vowels:
        if len(word) >= 1 and v == word[0]:
            firstIsVowel = 1
        if len(word) >= 2 and v == word[1]:
            secondIsVowel = 1
    print(word, " : ", firstIsVowel, ", ", secondIsVowel)

    if ((not firstIsVowel) and secondIsVowel):
        #print(word, ": perform rule 1")
        return 1
    elif ((not firstIsVowel) and (not secondIsVowel)):
        #print(word, ": perform rule 2")
        return 2
    elif firstIsVowel:
        #print(word, ": perform rule 3")
        return 3

    return 0

def performRule1(word):
# put the first letter of the word at the end of the word and add "ay" (EXAMPLE: happy = appyh + ay = appyhay)
    newWord = word[1:] + word[0] + "ay"
    return newWord

def performRule2(word):
# move the two consonants to the end of the word and add "ay" (EXAMPLE: Child = ildch + ay = ildchay)
    newWord = word[2:] + word[0:2] + "ay"
    return newWord

def performRule3(word):
# add the word "way" at the end of the word (EXAMPLE: Awesome = Awesome + way = awesomeway)
    newWord = word + "way"
    return newWord

def main():
    parser = argparse.ArgumentParser(description = "English to Pig Latin Converter")
    parser.add_argument("--input", required = True, help = "name of the input file")
    parser.add_argument("--output", required = True, help = "name of the output file")
    args = parser.parse_args()
    #print("file input: ", args.input)
    #print("file output: ", args.output)

    finalStr = ""

    fileIn = open(args.input, "r") # open in read and text mode
    for line in fileIn:
        for word in line.split():
            #strip punctuation from word
            wordNoPunc = re.sub("[^A-Za-z]","",word)

            # perform pig latin rules on current word
            rule = ruleNum(wordNoPunc)
            pigLat = ""
            if rule == 1:
                pigLat = performRule1(wordNoPunc)
            elif rule == 2:
                pigLat = performRule2(wordNoPunc)
            elif rule == 3:
                pigLat = performRule3(wordNoPunc)
            
            # add back any punctuation
            newWord = ""
            newWord = word.replace(wordNoPunc,pigLat)
            
            #print(word, " : ", newWord)
            finalStr = finalStr + newWord + " "
        finalStr = finalStr + "\n"
    fileIn.close()

    fileOut = open(args.output, "w")
    fileOut.write(finalStr)
    fileOut.close()

if __name__ == "__main__":
    main()
