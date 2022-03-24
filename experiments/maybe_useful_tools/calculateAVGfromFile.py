# Windows
#   run in command line: python calculateAVGfromFile.py
#   then follow instructions
#
# source file must contain only numbers each on new line 

with open(input("Enter file name with extension. E.g. sample.txt :\n")) as fh:
    sum = 0
    numlines = 0
    for line in fh:
        sum += float(line)
        numlines += 1
    average = sum / numlines
print(average)