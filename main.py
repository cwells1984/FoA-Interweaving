import csv

# Constants
INPUT_FILE = 'input.csv'

# Global vars
global operationCount               # number of operations in the current execution

# Utility to read the input file
def readInput(inputFile):
    with open(inputFile, 'r') as csvfile:
        signals = list(csv.DictReader(csvfile))
    return signals


# Detects whether an input string s is an interweaving of strings x and y. Returns a proof certification if so and
# Nothing if not
# Return Object = an array of strings of the same langth as the input string s. Each position of the array gives the
# index of the matching character in the x or y string
def detectInterleaved(s, x, y):
    global operationCount
    proofCert = [''] * len(s)       # the proof cert array
    sIndex = 0                      # points to the current character in s
    xIndex = 0                      # points to the current character in x
    firstXFound = False             # Goes to true when the first character is found in string s that is a part of x
    yIndex = 0                      # points to the current character in y
    firstYFound = False             # Goes to true when the first character is found in string s that is a part of y
    sNonAdvanceCount = 0            # Count of unsuccessful attempts to match the current character in s to any
                                    # character in x or y

    # loop through every character in s - if no matching characters have been found in the x or y string the loop will
    # be terminated
    while sIndex < len(s) and sNonAdvanceCount < max(len(x), len(y)):
        operationCount += 1

        # if the current character in x matches the current character in s then we have matched. advance the s counter
        # and x counters by 1 (we will now be looking for the next character in the x string)
        operationCount += 1
        if s[sIndex] == x[xIndex % len(x)]:
            if not firstXFound: firstXFound = True
            proofCert[sIndex] = 'x[' + str(xIndex % len(x)) + ']'
            sIndex += 1
            xIndex += 1

        # if the current character in y matches the current character in s then we have matched. advance the s counter
        # and y counters by 1 (we will now be looking for the next character in the y string)
        elif s[sIndex] == y[yIndex % len(y)]:
            if not firstYFound: firstYFound = True
            proofCert[sIndex] = 'y[' + str(yIndex % len(x)) + ']'
            sIndex += 1
            yIndex += 1

        # if we don't find either x or y character we were expecting these special conditions are checked...
        else:

            # ... if we already have identified the repetition of characters from x and y this mismatch must be
            # something 'extra' in string s besides interweaving and we should return a failure
            operationCount += 1
            if firstXFound and firstYFound:return proofCert

            # ... if we had not yet identified any characters from x or y in s yet we may just need to look for the
            # next character in their strings, so advance their indexes by 1
            elif not firstXFound:
                xIndex += 1
            elif not firstYFound:
                yIndex += 1

            # ... but in any case we also increment the counter for s not advancing. if this matches the length of x
            # and y then there is no match with any of the characters in either and there is more going on than just
            # interweaving
            sNonAdvanceCount += 1

    return proofCert


# Main execution
print("=" * 100)

# Read the input and convert it to strings, S, X, and Y
signals = readInput(INPUT_FILE)

# For each signal...
for signal in signals:
    operationCount = 0

    # Detect whether it is interleaved and return the proof certificate (whether or not it is complete
    pc = detectInterleaved(signal['S'], signal['X'], signal['Y'])

    # Print the inputs
    print("S = " + signal['S'])
    print("x = " + signal['X'])
    print("y = " + signal['Y'])

    # Print the outputs
    operationCount += len(signal['S'])
    if '' not in pc:
        print("S is an interweaving of x and y")
        print(pc)
    else:
        print("S is NOT an interweaving of x and y")
        print(pc)
    print("# of operations: " + str(operationCount))
    print("=" * 100)