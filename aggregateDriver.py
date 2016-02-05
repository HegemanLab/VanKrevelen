'''
Similar to the first driver class but handles multiple files of one type (either mzML or mzXML) Processes them
by dropping all duplicate m/z values to reduce clutter. Also opperates differently by starting with running the
script, then having you enter in the files one by one.
'''

import copy
import os
import webbrowser

# additional created classes/packages
from writeTxt import writeTxt
from process_mzs_mzML import process_mzs as ML_process

from MzXML import MzXML
from process_mzs import process_mzs as XML_process

print("\nWelcome to the Van Krevelen Aggregator.")
print("Please enter each file you would like to process one at at time.")
print("When you are done entering files, type 'done' and remember to include the file extensions (.mzXML or .mzML).\n")

files = []

# Get first file
print("Now enter your first file, then press return."
      "\nRemember to enter file names with extensions.\n")
new_file = raw_input("File Name: ")

# Continues to add as many files as the user wants.
while new_file.lower() != "done":
    # Makes sure file is accessible
    if not os.access(new_file, os.R_OK):
        print "%s is not accessible." % new_file
        print "Please try again. The files you use must be in the same file as this script."
    # Checks for one of the two desired file extensions and if the file is accessible and has the correct
    # ending then it is added to the list of the files.
    else:
        # This isn't a perfect error catching method but should catch enough.
        if ".mzXML" in new_file or ".mzML" in new_file:
            files.append(new_file)
        else:
            print("Incorrect file extension.")
    # Reprompt
    print("\nEnter another file with its extension, or enter 'done' and hit return.")
    new_file = raw_input("Enter Input: ")

print("\nNext this script will process your files. \nIt will do so by processing each file individually. \nTo do so "
      "it will look at the maximum intensity of a spectrum in the file and then assign a threshold to value that "
      "is some percentage of that maximum. \nThe threshold will be used to determine what values are significant and "
      "what values are just noise. \nWe recommend a threshold of 10% but you can set your own here. please enter your "
      "threshold percentage as a number with no percentage sign. \n(For example, if you wanted 15%, enter 15)")

threshold_input = raw_input("\nThreshold: ")
t_flag = False

while not t_flag:
    try:
        threshold = float(threshold_input) * .01
        t_flag = True
    except:
        threshold_input = raw_input("\nIncorrect input, please enter just a number.\nThreshold: ")

try:
    outputName = str(raw_input("What would you like to call this data set? (No spaces please.) Name: "))
except:
    outputName = raw_input("Enter name: ")

# Sets up book keeping lists and then processes it depending on if it's an mzXML file or mzML file .
neg_pos_mz_sets = [[], []]

# Use correct processing based on filetype
for f in files:
    if ".mzXML" in f:
        mzXML = MzXML()
        mzXML.parse_file(f)
        neg_pos_mz_sets_temp = XML_process(mzXML, threshold=threshold)
        neg_pos_mz_sets[0] = neg_pos_mz_sets[0] + neg_pos_mz_sets_temp[0]
        neg_pos_mz_sets[1] = neg_pos_mz_sets[1] + neg_pos_mz_sets_temp[1]
    elif ".mzML" in f:
        # Use ML processing
        print "Reading %s ..." % f
        neg_pos_mz_sets_temp = ML_process(f, threshold=threshold)
        neg_pos_mz_sets[0] = neg_pos_mz_sets[0] + neg_pos_mz_sets_temp[0]
        neg_pos_mz_sets[1] = neg_pos_mz_sets[1] + neg_pos_mz_sets_temp[1]

# Removes all duplicates from both neg and pos lists
neg_pos_mz_sets[0] = list(set(neg_pos_mz_sets[0]))
neg_pos_mz_sets[1] = list(set(neg_pos_mz_sets[1]))



# Fix for how writeTxt works - ugly code
name = outputName + "xxxxxx"

# Patch for bug when writing one file. Probably a better way to do this but this works.
if len(neg_pos_mz_sets[0]) > len(files):
    writeTxt(neg_pos_mz_sets[0], name, 0)
if len(neg_pos_mz_sets[1]) > len(files):
    writeTxt(neg_pos_mz_sets[1], name, 1)

# Automatically opens the web browser with the calculator page open
webbrowser.open('http://www.bmrb.wisc.edu/metabolomics/mass_query.php', new=1)

print('done')
