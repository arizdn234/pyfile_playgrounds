import sqlite3
import tkinter as tk
from tkinter import ttk

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('your_database_name.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a courses table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    courseName TEXT
                )""")

# Insert sample data into the courses table
cursor.execute("INSERT INTO courses (courseName) VALUES ('JavaScript Basics')")
cursor.execute("INSERT INTO courses (courseName) VALUES ('Python Fundamentals')")
cursor.execute("INSERT INTO courses (courseName) VALUES ('Web Development Bootcamp')")

# Commit the changes to the database
conn.commit()

# Execute a SELECT query to retrieve data from the "courses" table
cursor.execute("SELECT id, courseName FROM courses")

# Fetch all the rows of data returned by the query
rows = cursor.fetchall()

# Create a tkinter window
root = tk.Tk()

# Create a tkinter combobox widget
combo = ttk.Combobox(root, state="readonly")

# Populate the combobox with the data retrieved from the database
for row in rows:
    # Create a string with the course name and ID, separated by an underscore
    course_str = f"{row[1]}_{row[0]}"
    # Add the string to the combobox
    combo['values'] = (*combo['values'], course_str)

# Set the initial value of the combobox to the first item in the list
combo.current(0)

# Pack the combobox into the tkinter window
combo.pack()

# Define a function to save the selected value to the new table
def save_selection():
    # Extract the course ID from the selected value in the combobox
    course_id = combo.get().split('_')[1]
    print(course_id)

    # Create a selected_courses table if it doesn't exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS selected_courses (
                        id INTEGER PRIMARY KEY,
                        course_id INTEGER
                    )""")

    # Execute an INSERT INTO query to insert the selected course ID into the new table
    cursor.execute(f"INSERT INTO selected_courses (course_id) VALUES ({course_id})")

    # Commit the changes to the database
    conn.commit()

    # Display a message box to confirm that the selection was saved
    tk.messagebox.showinfo("Selection Saved", f"Course with ID {course_id} was saved to selected_courses table.")

# Create a tkinter button widget to save the selected value
save_button = ttk.Button(root, text="Save Selection", command=save_selection)
save_button.pack()

# Start the tkinter event loop
root.mainloop()

# Close the database connection
conn.close()
