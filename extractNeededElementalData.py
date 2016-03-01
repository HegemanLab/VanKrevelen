'''
Combs through elemental data generated by http://www.bmrb.wisc.edu/metabolomics/mass_query.php, or found through
other databases, to pull out the numbers of Hydrogens, Carbons, Oxygens, and Nitrogens.
'''

import csv
import pandas as pd


def extract_needed_elemental_data(tab_separated_txt_file):

    '''
    If you wanted to run similar analysis with this script you could modify this list however additional work
    would need to be done if any of the additional desired elements are represented by more than a single
    uppercase letter.
    '''

    # List of compounds to be found and order they will be found in
    elements_to_find = ['C', 'H', 'O', 'N']

    compounds = []
    # open a text file
    with open(tab_separated_txt_file) as f:

        # Hard coded for number of characters each column has
        n = 16

        # Set up file reader
        reader = f.readlines()
        for line in reader:

            # Split line into columns
            new_line = [line[i:i+n] for i in range(0, len(line), n)]

            # If compound was not found by BMRB then 3 will be out of range, otherwise add that formula to the compounds
            try:
                compounds.append(new_line[3])
            except:
                pass

    # Process elemental data and close file
    elemental_list = find_elements_values(elements_to_find, compounds)
    f.close()

    return elemental_list



'''
Note, this current format only works for 1 letter elements which works fine for H, C, O, and N
which is what is needed for VanKrevelen Analysis. Also works for up to 3 digits (ie H999 works but H1000 would
not work).
'''


def find_elements_values(elements_to_find, compounds):
    # List to hold the lists of the counts of each element
    complete_element_counts = []

    # For each compound being searched
    for compound in compounds:

        # List to hold each lines element counts
        line_element_counts = []

        # For each element e in the elements to find list ['C', 'H', 'O', 'N']
        for e in elements_to_find:
            j = 0
            found = False

            # Looks through each character in each compound
            for c in compound:

                # If char is found, mark it
                if c == e:
                    found = True
                    location = j

                    # Checks if element found is the end of the compound
                    if location + 1 < len(compound):

                        # Sets element value equal to 1 because next char in compound is another element or end
                        # of the compound
                        if compound[location + 1].isupper() or compound[location + 1].isspace():
                            line_element_counts.append(1.0)
                            break

                        # Determines if the element found is actually a different element
                        elif compound[location + 1].islower():
                            found = False

                        # Has found a number value after the element
                        elif compound[location + 1].isdigit():

                            # If the value can be triple digits ...
                            if location + 3 < len(compound):

                                # If the value is triple digits
                                if compound[location + 2].isdigit() and compound[location + 3].isdigit():

                                    # set value to the three digit number
                                    line_element_counts.append(float(compound[location + 1: location + 4]))
                                    break

                                # If the value can be double digits
                                elif location + 2 < len(compound):

                                    # If the value is double digits
                                    if compound[location + 2].isdigit():

                                        # Set value to the two digit number
                                        line_element_counts.append(float(compound[location + 1: location + 3]))
                                        break

                                    else:

                                        # Sets value to one digit number
                                        line_element_counts.append(float(compound[location + 1: location + 2]))
                                        break

                                # Else it is determined to be a one digit number
                                else:
                                    line_element_counts.append(float(compound[location + 1: location + 2]))
                                    break

                            # If it can be a two digit number
                            elif location + 2 < len(compound):

                                # If it is a two digit number
                                if compound[location + 2].isdigit():

                                    # set value to the two digit number
                                    line_element_counts.append(float(compound[location + 1: location + 3]))
                                    break

                                # If it is a one digit number
                                else:
                                    line_element_counts.append(float(compound[location + 1: location + 2]))
                                    break

                            # It is a one digit number
                            else:
                                # set value equal to the first digit
                                line_element_counts.append(float(compound[location + 1]))
                                break

                    # If it is a single element
                    else:
                        line_element_counts.append(1.0)
                        break
                j += 1

            # If the element is not found, assign a value of zero
            if found == False:
                line_element_counts.append(0)

        # Add single compound's values to the overall list
        complete_element_counts.append(line_element_counts)

    return complete_element_counts



