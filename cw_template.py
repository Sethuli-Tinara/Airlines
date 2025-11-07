"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 
 4. Date: 
****************************************************************************

"""
from graphics import *
import csv
import math

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv_(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)



#************************************************************************************************************

#EDIT THE CODE BELOW TO COMPLETE YOUR SUBMISSION

selected_data_file="LHR2025.csv" #hard coded csv name to be replaced with your dynamically created filename
load_csv(selected_data_file)     #calls the function "load_csv" sending the variable 'selected_data_file" as a parameter

#Some Example code queries to be replaced with those required by the brief. Compare these outputs to the supplied CSV files

print (f"The current file name is {selected_data_file}")
print ("")
print (f"First row of data_list is data_list[0] -> {data_list[0]}")
print ("")
print (f"Second item of the first row is flight number, data_list[0][1]      -> {data_list[0][1]}")
print ("")
print (f"Third item of the second row is scheduled depature, data_list[1][2] -> {data_list[1][2]}")

  






