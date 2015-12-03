import sys
import os
import webbrowser

#additional created classes/packages
from MzXML import MzXML
from writeTxt import writeTxt
from process_mzs import process_mzs

#Creates an MzXML object from the file provided
# filename_mzXML = '20150705_A8.mzXML' # Convert:  | Machine:   | Working:
# filename_mzXML = '1section.mzXML'   # Convert: MS_Convert  | Machine: Orbitrap | Working: No
# filename_mzXML = 'example.mzXML'  # Convert:  | Machine: | Working:
# filename_mzXML = '20150705_A11.mzXML' # Convert: MS Convert  | Machine: Waters  | Working:
# filename_mzXML = '20150705_A6.mzXML'    # Convert: MS Convert  | Machine: Waters  | Working: No
filename_mzXML = 'MRR_11-29-2011_Backexchange-Kinetics_trial4_C2_0hr.mzXML' # Convert: MM File Conversion | Machine: Dif Oribitrap | Working: Yes

'''
NOTES
############################################
'MRR_11-29-2011_Backexchange-Kinetics_trial4_C2_0hr.mzXML' # Convert: MS Convert | Machine: Dif Oribitrap | Working: No } Errors given and numbers nonsensical
'MRR_11-29-2011_Backexchange-Kinetics_trial4_C2_0hr.mzXML' # Convert: MM_File_conversion | Machine: Dif Orbitrap | Working: Yes

'20150705_A6.mzXML'                                        # Convert: MS Convert  | Machine: Waters  | Working: No

'1section.mzXML'                                           # Convert: MM_File_conversion  | Machine: Orbitrap | Working: Yes
'1section.mzXML'                                           # Convert: MS_Convert  | Machine: Orbitrap | Working: No
############################################
'''


mzXML = MzXML()
mzXML.parse_file(filename_mzXML)

#Takes in the mzXML object and processes all the data to extrac a list with both the positive and
#negative mz values extracted. Then writes those to two .txt files.
neg_pos_mz_sets = process_mzs(mzXML)
writeTxt(neg_pos_mz_sets[0], filename_mzXML, 0)
writeTxt(neg_pos_mz_sets[1], filename_mzXML, 1)

#Automatically opens the webbrowser with the calculator page open
webbrowser.open('http://www.bmrb.wisc.edu/metabolomics/mass_query.php', new = 1)

print('done')
