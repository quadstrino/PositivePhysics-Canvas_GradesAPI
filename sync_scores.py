"""
This is the main program for the PositivePhysics to Canvas score sync tool.

This program will download scores from PositivePhysics, and then update scores to Canvas LMS.

The program will ask the user if they want to download scores, and if they want to update scores to Canvas.
"""
import pandas as pd                 # library for dataframe editing
from natsort import natsorted       # library for sorting properly
import os

from update_scores import update_scores
from download_and_relocate import download

# define necessary variables
path = os.getcwd()
directory_path = rf"{path}\files" #used in download and update_scores functions
grade_master = {}   #used in update_scores and determine_eligible functions

with open(rf"{directory_path}\config.txt") as f:
        lines = f.readlines()
        selected_term = lines[14].strip()

# import students.csv as dataframe
student_info = pd.read_csv(rf"{directory_path}\students.csv")    #used in update_scores and determine_eligible functions
# import assignments.csv as dataframe
assignment_info = pd.read_csv(rf"{directory_path}\assignments.csv")  #used in update_scores and term_selected functions
# define important lists from imported data
units_current = natsorted(list(set(assignment_info.loc[(assignment_info['Term'] == selected_term), 'PP Unit'].to_list())))


print("Beginning download...")
download(units_current, directory_path)
print("\nScore download complete!")

update_scores(units_current, assignment_info, student_info, directory_path, grade_master)
print("\nScore update complete!")