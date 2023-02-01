# Project 2: English to Pig Latin Converter

# Instructions
Implement a Python-based English text to Pig-Latin converter. The implementation should read in this text file, [data.txt](data.txt), and create a Pig-Latinized output text called out.txt. The converter must implement the following Pig-Latin rules:

1. If a word starts with a consonant and a vowel, put the first letter of the word at the end of the word and add "ay."
    1. Example: Happy = appyh + ay = appyhay

2. If a word starts with two consonants move the two consonants to the end of the word and add "ay."
    1. Example: Child = Ildch + ay = Ildchay

3. If a word starts with a vowel add the word "way" at the end of the word.
    1. Example: Awesome = Awesome +way = Awesomeway

4. The output file must retain all of the punctuations used in the input text file. 

# Coding Requirements
1. The code must use the [Python argparse](https://docs.python.org/3/library/argparse.html) to input the text file. Optionally, also include an argument for the user to name the output file. An example execution would be: `python3 piglatin.py --input data.txt --output data_out.txt`

2. The code must include a succinct description of the converter at the top of the file using triple quotes. Put appropriate code comments to promote readability.

3. The code must be modular using two or more functions.

