Positive Physics to Canvas Score Sync
=====================================

Project Overview
----------------
This Python program automates the process of downloading student scores from PositivePhysics.org and uploading them to Canvas LMS using the Canvas API. It uses CSV files and a configuration file to streamline grade management and ensure accurate score reporting.

Features
--------
- Downloads student scores from Positive Physics.
- Uploads scores to Canvas LMS using the Canvas API.
- Configurable using a `config.txt` file.
- Processes CSV files for:
  - Student Information
  - Course Information
  - Assignment Information
  - Positive Physics Site Information
- Supports bulk updates for efficiency.

Requirements
------------
Software:
- Python 3.8+
- Canvas API access with a valid token.
- PositivePhysics.org account with instructor access.

Python Libraries:
- canvasapi
- datetime (standard library)
- glob (standard library)
- natsort
- os (standard library)
- pandas
- playwright
- tempfile (standard library)

Installation
------------
1. Clone the repository:
   git clone https://github.com/your-repository-url.git
   cd your-repository-folder

2. Install required libraries:
   pip install -r requirements.txt

3. Set up your files:
   - Update the following CSV files in the '/files' directory with the correct information (*see file descriptions below*):
     - `students.csv`: Contains student information.
     - `courses.csv`: Contains course details.
     - `assignments.csv`: Contains assignment information.
   - Create or update the `config.txt` file with:
     - Positive Physics login information:
       - Username, password, and class code
     - Canvas information:
       - Base URL and API token
     - Default term.

4. Run the program:
   python sync_scores.py

Usage
-----
1. Ensure required CSV files and `config.txt` are properly configured.
2. Run the program:
   python sync_scores.py
3. Monitor the console output for progress updates or errors.

File Descriptions (*including details on csv file requirements)
-----------------
- `config.txt`: Contains customizable program settings.
- `assignments.csv`: Maps Canvas assignment IDs to Positive Physics assignments.
	- Course: This is used to distinguish different courses. I have taught AP Physics 1, AP Physics 2, and Honors Physics at the same 		time, each with different homework assignments in Positive Physics. 
	- Assignment Name: I copy and paste the assignment name from Canvas for this column.
	- Canvas ID: This is the Canvas assignment ID, most easily found in the url when on the assignment page.
	- PP Unit: This is the unit that the assignment comes from in Positive Physics. This must match the `unit_name` column in the 			`posphys_urls.csv` file.
	- PP Lesson: This is the Lesson Name from PositivePhysics for the assignment.
	- Term: This is the Grade Term that the assignment will go on. My school has 4 terms, I use this so that I am only downloading and 		updating scores for the current term in Canvas.
- `courses.csv`: Maps course names to Canvas course IDs.
	- Course: Nickname for the different courses.
	- CanvasID: This is the Canvas course ID, most easily found in the url when on the course page.
- `posphys_urls.csv`: Maps Positive Physics units to the URL for their completion scores.
	- unit_name: These are the names of each unit from the default Physics course on Positive Physics.
	- url: These are the urls that are associated with the gradebook for the appropriate unit.
- `students.csv`: Includes student names, Canvas IDs, and Positive Physics IDs.
	- Student: Student's name.
	- ID: Student's Canvas ID.
	- Course: Which ever course the student is associated with.
	- Username: Student's positivephysics username.


Future Improvements
-------------------
- Use the canvas API to get assignment details.
- Add a graphical user interface (GUI).
  - I currently have a version that allows me to check if students have received a full `100%` on all assignments, and lists any that are incomplete. This is for me to check if students are eligible to do a retake. I haven't included it here because I don't like how it looks... maybe some day. 

Contributing
------------
Contributions are welcome! Submit a pull request or open an issue with suggestions or bug reports.

License
-------
This project is licensed under the MIT License. See the `LICENSE` file for details.

Acknowledgments
---------------
- PositivePhysics.org for educational resources. Jack is awesome!
- Canvas LMS for API integration.
