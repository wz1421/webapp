# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3

con = sqlite3.connect('babymonitordata.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS data
                    (time real PRIMARY KEY, skinconc real, bloodconc real)''')
cur.execute('''INSERT OR IGNORE INTO data VALUES
                    ('30','50','100')''')
con.commit()

for row in cur.execute('''SELECT * FROM data'''):
    print(row)


# Function to update the graph based on user input
def update_graph():
    # Get the user input
    x_values = [float(e) for e in entry_x.get().split(',')]
    y_values = [float(e) for e in entry_y.get().split(',')]

    # Clear the current plot
    subplot.clear()

    # Plot the new data
    subplot.plot(x_values, y_values)

    # Render the updated plot
    canvas.draw()


# Create a Tkinter window
window = tk.Tk()
window.title("Graph in UI")

# Create a figure for the plot
fig = Figure(figsize=(5, 4), dpi=100)
subplot = fig.add_subplot(111)

# Create the initial plot
subplot.plot([0], [0])  # Start with an empty plot

# Create a canvas and add the plot to the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
label_x1 = tk.Label(window, text="Enter time values for Graph 1:")
label_x1.pack(side=tk.TOP, fill=tk.X, expand=1)

# Create entry fields for user input
entry_x = tk.Entry(window)
entry_x.pack(side=tk.TOP, fill=tk.X, expand=1)

entry_x.insert(0, '0,1,2,3,4')  # Default values

label_y1 = tk.Label(window, text="Enter skin glucose concentration for Graph 1:")
label_y1.pack(side=tk.TOP, fill=tk.X, expand=1)

entry_y = tk.Entry(window)
entry_y.pack(side=tk.TOP, fill=tk.X, expand=1)
entry_y.insert(0, '0,2,4,6,8')  # Default values


# Create a button to update the plot
update_button = tk.Button(window, text="Update Graph", command=update_graph)
update_button.pack(side=tk.TOP)

# Run the application
window.mainloop()
