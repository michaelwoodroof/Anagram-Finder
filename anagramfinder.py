#
# Tested and run on windows command line and windows powershell
#

# Imports
import unittest
import os.path
from os import path
import sys

class AnagramFinder():

    def __init__(self, filename = "", displayException = False):
        if filename and type(filename) == str:
            self.path = filename
            self.wordStorage = {}
            try:
                with open(self.path, "r") as f:
                    try:
                        for line in f:
                            word = line.rstrip()
                            length = len(word)
                            if self.wordStorage.get(length):
                                # Add to existing inner dictionary
                                existingDict = self.wordStorage.get(length)
                                # Prevents duplicate words
                                if not existingDict.get(word):
                                    existingDict[word] = self.deconstructWord(word)
                                    self.wordStorage[length] = existingDict
                            else:
                                # Create new entry for dictionary
                                innerDict = {}
                                innerDict[word] = self.deconstructWord(word)
                                self.wordStorage[length] = innerDict
                    except Exception as e:
                        if (displayException):
                            print(str(e))
            except IOError as e:
                if (displayException):
                    print(str(e))
        else:
            self.path = None
            self.wordStorage = None

    def deconstructWord(self, word = ""):
        if len(word) >= 1 and type(word) == str:
            deconstructed = [0] * 27
            for char in word:
                asciiValue = ord(char.upper()) - 65
                if asciiValue >= 0 and asciiValue <= 25:
                    deconstructed[asciiValue] += 1
                elif char == "\'":
                    deconstructed[26] += 1
                else:
                    return None
            return deconstructed
        return None

    def anagrams(self, word = ""):
        # Verify word exists
        if word and type(word) == str:
            decontruct = self.deconstructWord(word)
            # Get Partial Dictionary of Length of given word
            partialDict = self.wordStorage.get(len(word))
            # Verify that words of given length exist
            if partialDict:
                foundWords = []
                for key in partialDict:
                    if partialDict[key] == decontruct:
                        foundWords.append(key)
                return foundWords
            else:
                return []
        else:
            return []

class TestAnagramFinder(unittest.TestCase):

    # Series of tests to check words are deconstructed properly
    def testDeconstructions(self):
        # Set-up Variables
        af = AnagramFinder("")
        arr = [0] * 27

        testOne = af.deconstructWord("cheese")
        testOneArr = arr
        testOneArr[2] = 1
        testOneArr[4] = 3
        testOneArr[7] = 1
        testOneArr[18] = 1
        self.assertEqual(testOne, testOneArr)

        testTwo = af.deconstructWord("22")
        self.assertEqual(testTwo, None)

        testThree = af.deconstructWord("ZOO")
        testThreeArr = arr
        testThreeArr[25] = 1
        testThreeArr[14] = 2

        testFour = af.deconstructWord()
        self.assertEqual(testFour, None)

        testFive = af.deconstructWord("Olá")
        self.assertEqual(testFive, None)

        testSix = af.deconstructWord("")
        self.assertEqual(testSix, None)

        testSeven = af.deconstructWord([object])
        self.assertEqual(testSeven, None)

    # Series of tests to verify files are correctly read
    def testFiles(self):
        testOne = AnagramFinder("datasets/english.txt")
        self.assertEqual(testOne.path, "datasets/english.txt")
        self.assertIsNotNone(testOne.wordStorage)

        testTwo = AnagramFinder("")
        self.assertEqual(testTwo.path, None)
        self.assertEqual(testTwo.wordStorage, None)

        testThree = AnagramFinder("datasets/corrupted.txt")
        self.assertEqual(testThree.path, "datasets/corrupted.txt")
        self.assertEqual(testThree.wordStorage, {})

        testFour = AnagramFinder("datasets/foreign.txt")
        self.assertEqual(testFour.path, "datasets/foreign.txt")
        self.assertEqual(testFour.wordStorage, {})

        testFive = AnagramFinder("datasets/mixed.txt")
        self.assertEqual(testFive.path, "datasets/mixed.txt")
        self.assertIsNotNone(testFive.wordStorage)

        testSix = AnagramFinder()
        self.assertEqual(testSix.path, None)
        self.assertEqual(testSix.wordStorage, None)

        testSeven = AnagramFinder(None)
        self.assertEqual(testSeven.path, None)
        self.assertEqual(testSeven.wordStorage, None)

        testEight = AnagramFinder([object])
        self.assertEqual(testEight.path, None)
        self.assertEqual(testEight.wordStorage, None)


    def testAnagrams(self):
        af = AnagramFinder("datasets/english.txt")

        # @TODO Complete these Tests
        testOne = af.anagrams("evli")
        self.assertEqual(testOne, ['evil', 'levi', 'live', 'veil', 'vile'])

        testTwo = af.anagrams("madeupword")
        self.assertEqual(testTwo, [])

        testThree = af.anagrams("Olá")
        self.assertEqual(testThree, [])

        testFour = af.anagrams("[#;!""]")
        self.assertEqual(testFour, [])

        testFive = af.anagrams("adrarakv")
        self.assertEqual(testFive, ["aardvark"])

        testSix = af.anagrams("2242")
        self.assertEqual(testSix, [])

        testSeven = af.anagrams([object])
        self.assertEqual(testSeven, [])

        testEight = af.anagrams("disestablishmentarianims")
        self.assertEqual(testEight, ["disestablishmentarianism"])

def helper():
    print("                Anagram Finder               \n")
    print("[  Arg   Description                         ]")
    print("[   -f   file for anagrams to be found in    ]")
    print("[   -t   run tests on solution.py            ]")
    print("[   -h   run helper function                 ]\n")

    print("Example: python anagramfinder.py -f datasets/english.txt")
    print("Example: python anagramfinder -t")
    print("Example: python anagramfinder -h\n")

# Driver Code
if __name__ == "__main__":

    if len(sys.argv) - 1 == 2 or len(sys.argv) - 1 == 1:

        if sys.argv[1] == "-f":
            if path.exists(sys.argv[2]) and sys.argv[2].endswith(".txt"):
                af = AnagramFinder(sys.argv[2], False)
                # Start Input Loop
                newWord = True
                if len(af.wordStorage) >= 1:
                    while newWord:
                        word = input("Enter a string to find all possible anagrams (type exit to exit) > ")
                        if not word.upper() == "EXIT":
                            foundWords = af.anagrams(word)
                            if len(foundWords) == 0:
                                print("\nInput was: {word}\nNo found anagrams \n"
                                .format(word = word))
                            else:
                                print("\nInput was: {word}\nFound anagrams were : {foundWords} \n"
                                .format(word = word, foundWords = foundWords))
                        else:
                            newWord = False
                else:
                    print("Invalid content of file")
            else:
                print("Invalid file chosen")

        elif sys.argv[1] == "-h":
            helper()

        elif sys.argv[1] == "-t" and len(sys.argv) - 1 == 1:
            # Run Unit Tests
            unittest.main(argv=['anagramfinder.py'], exit=False)

        else:
            print("          Invalid arguments chosen\n")
            helper()

    else:
        print("          Invalid arguments chosen\n")
        helper()
