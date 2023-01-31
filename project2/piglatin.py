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
import string

vowels = ["a","e","i","o","u"]

# return the rule number to perform on the word
def ruleNum(word):
    word.lower()

    # test if first and second letters are vowels or consonants
    firstIsVowel = 0
    secondIsVowel = 0
    for v in vowels:
        if v == word[0]:
            firstIsVowel = 1
        if v == word[1]:
            secondIsVowel = 1

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
    #print(word, " : ", newWord)
    return newWord

def performRule2(word):
# move the two consonants to the end of the word and add "ay" (EXAMPLE: Child = ildch + ay = ildchay)
    newWord = word[2:] + word[0:2] + "ay"
    #print(word, " : ", newWord)
    return newWord

def performRule3(word):
# add the word "way" at the end of the word (EXAMPLE: Awesome = Awesome + way = awesomeway)
    newWord = word + "way"
    #print(word, " : ", newWord)
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
            # perform pig latin rules on current word
            rule = ruleNum(word)

            punc = ""
            if word[-1] in string.punctuation:
                punc = word[-1]
                word = word[:-1]

            if rule == 1:
                newWord = performRule1(word)
            elif rule == 2:
                newWord = performRule2(word)
            elif rule == 3:
                newWord = performRule3(word)
            finalStr = finalStr + newWord + punc + " "
    fileIn.close()

    fileOut = open(args.output, "w")
    fileOut.write(finalStr)
    fileOut.close()

if __name__ == "__main__":
    main()
