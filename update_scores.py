# function do update grade_master and save a .csv file for upload
def update_scores(units_all, assignment_info, student_info, directory_path, grade_master):
    """
    Updates the grade_master dictionary with student scores from PositivePhysics and prepares it for upload to Canvas.

    This function reads configuration settings, imports necessary data from CSV files, and processes scores for each
    course and student. It matches students' scores from PositivePhysics with Canvas assignments and organizes them
    in the grade_master dictionary for bulk upload to Canvas.

    Args:
        units_all (list): A list of all PositivePhysics units to process.
        assignment_info (DataFrame): DataFrame containing assignment metadata, including Canvas IDs and assignment names.
        student_info (DataFrame): DataFrame containing student details such as names and IDs.
        directory_path (str): The directory path where configuration and CSV files are located.
        grade_master (dict): A dictionary that gets updated with student scores for each course.

    Returns:
        None
    """
    import os
    import pandas as pd
    from canvasapi import Canvas

    # Your Canvas instance URL and API token
    with open(rf"{directory_path}\config.txt") as f:
        lines = f.readlines()
        BASE_URL = lines[9].strip()
        API_TOKEN = lines[11].strip()
        selected_term = lines[14].strip()

    scores = {}
    course_info = pd.read_csv(rf"{directory_path}\courses.csv") # imports course info from courses.csv
    courses = list(set(course_info['Course'].to_list()))

    for unit in units_all:    # iterates through +Phys units
        for fname in os.listdir(rf"{directory_path}\downloads"):    # iterates through directory to find +phys export files
            if unit in fname:
                scores[unit] = pd.read_html(rf"{directory_path}\downloads" + "\\" + fname, header=0)[0] #imports +phys export file, sets header to lesson name
                scores[unit].columns = scores[unit].columns.str.lower()

    # Initialize the Canvas API
    canvas = Canvas(BASE_URL, API_TOKEN)

    for current_course in courses:
        # create dataframe that contains all grades for each class
        grade_master[current_course] = student_info.loc[(student_info['Course'] == current_course), ['Student','ID']].copy().reset_index(drop=True) # creates new df with student info
        canvas_IDs = assignment_info.loc[(assignment_info['Course'] == current_course) & (assignment_info['Term'] == selected_term), 'Canvas ID'].to_list()
        assignment_names = assignment_info.loc[(assignment_info['Course'] == current_course) & (assignment_info['Term'] == selected_term), 'Assignment Name'].to_list()
        grade_master[current_course][canvas_IDs] = ''     # creates columns in df for all Canvas assignments
        # iterate through each student in grade_master
        for student in list(grade_master[current_course]['Student']):
            student_master_index = grade_master[current_course].loc[(grade_master[current_course]['Student'] == student)].index.to_list()[0]
            un = student_info.at[student_info.loc[(student_info['Student'] == student)].index.to_list()[0],'Username'] # gets student username based on name from students.csv
            # iterate through each assignment name in assignment_info
            for ASSIGNMENT_ID in canvas_IDs:
                lesson = assignment_info.loc[(assignment_info['Canvas ID'] == ASSIGNMENT_ID), 'PP Lesson'].to_list()[0].lower()
                unit = assignment_info.loc[(assignment_info['Canvas ID'] == ASSIGNMENT_ID), 'PP Unit'].to_list()[0]
                if unit in scores:
                    lesson_header = [col for col in scores[unit].columns if lesson in col][0]
                    student_score_index = scores[unit].loc[scores[unit]['student'] == un].index.to_list()[0]
                    grade_master[current_course].at[student_master_index,ASSIGNMENT_ID] = int(scores[unit].at[student_score_index, lesson_header][:-1])

                else:
                    continue

        print("\n" + "+" * len(f"Beginning grade update for {current_course}"))
        print(f"Beginning grade update for {current_course}")
        print("+" * len(f"Beginning grade update for {current_course}"))
        COURSE_ID = course_info.loc[(course_info['Course'] == current_course), 'CanvasID'].to_list()[0]
        course = canvas.get_course(COURSE_ID)

        for ASSIGNMENT_ID in canvas_IDs:
            
            assignment = course.get_assignment(ASSIGNMENT_ID)

            try:
                # Create the dictionary for submissions_bulk_update
                bulk_update_dict = grade_master[current_course].set_index("ID")[ASSIGNMENT_ID].apply(lambda x: {"posted_grade": x}).to_dict()
                assignment.submissions_bulk_update(grade_data=bulk_update_dict)
                print(f"Bulk grade update successful for assignment {assignment_names[canvas_IDs.index(ASSIGNMENT_ID)]}")
            
            except Exception as e:
                print(f"Failed to update grades: {e}")
