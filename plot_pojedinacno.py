import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Toplevel, Entry, Button, Label, StringVar
from tkinter.filedialog import askopenfilename

def load_csv_data(file_path):
    """Loads time and force data from a .csv file and returns two lists."""
    time_data = []
    force_data = []
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            time_data.append(float(row[0]))
            force_data.append(float(row[1]))  # Keep both positive and negative forces
    return time_data, force_data

def filter_low_force_periods(time_data, force_data, threshold=0.25, duration=2.0):
    """Filters out periods where the force is below the threshold for longer than the given duration."""
    filtered_time = []
    filtered_force = []
    
    i = 0
    while i < len(time_data):
        # Find the next period where the force is continuously below the threshold
        start_idx = i
        while i < len(force_data) and abs(force_data[i]) < threshold:
            i += 1
        
        # If this low-force period is longer than the duration, skip it
        if i - start_idx > 0:
            period_duration = time_data[i-1] - time_data[start_idx]
            if period_duration >= duration:
                print(f"Skipping period from {time_data[start_idx]}s to {time_data[i-1]}s (duration: {period_duration}s)")
            else:
                filtered_time.extend(time_data[start_idx:i])
                filtered_force.extend(force_data[start_idx:i])
        
        # Add the remaining data points (force above threshold)
        while i < len(force_data) and abs(force_data[i]) >= threshold:
            filtered_time.append(time_data[i])
            filtered_force.append(force_data[i])
            i += 1

    return filtered_time, filtered_force

def plot_data(root, time_data, force_data, file_name):
    """Plots the time vs force graph with interactive labels."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the data
    ax.plot(time_data, force_data, linestyle='-', marker='', color='b')
    
    # Set font properties
    font = {'fontname': 'Times New Roman'}

    # Set the labels without a title
    ax.set_xlabel('Vrijeme, s', fontsize=12, **font)
    ax.set_ylabel('Aksijalna sila, N', fontsize=12, **font)
    ax.grid(True)

    # Set time ticks on x-axis for every second
    ax.set_xticks(np.arange(min(time_data), max(time_data)+1, 1))

    # Integrate with Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Functions to update labels interactively
    def update_xlabel(event):
        def submit():
            new_label = label_var.get()
            ax.set_xlabel(new_label, fontsize=12, **font)
            canvas.draw()
            popup.destroy()
        popup = Toplevel()
        popup.title("Promijeni naziv x-osi")
        label_var = StringVar(value=ax.get_xlabel())
        Entry(popup, textvariable=label_var, width=50).pack()
        Button(popup, text="OK", command=submit).pack()

    def update_ylabel(event):
        def submit():
            new_label = label_var.get()
            ax.set_ylabel(new_label, fontsize=12, **font)
            canvas.draw()
            popup.destroy()
        popup = Toplevel()
        popup.title("Promijeni naziv y-osi")
        label_var = StringVar(value=ax.get_ylabel())
        Entry(popup, textvariable=label_var, width=50).pack()
        Button(popup, text="OK", command=submit).pack()

    # Connect events with mouse clicks
    def on_click(event):
        if event.inaxes == ax:
            if event.y < ax.get_position().y0:  # Click on x-axis
                update_xlabel(event)
            elif event.x < ax.get_position().x0:  # Click on y-axis
                update_ylabel(event)

    canvas.mpl_connect('button_press_event', on_click)

    # Button to save the plot
    def save_plot():
        image_path = os.path.splitext(file_name)[0] + '_updated.png'
        fig.savefig(image_path)
        print(f"Grafikon spremljen kao {image_path}")

    Button(root, text="Spremi graf", command=save_plot).pack()

def browse_and_load_file():
    """Opens a file dialog to let the user select a .csv file and displays the plot."""
    root = Tk()
    root.title("Interaktivni graf")

    # Open a file dialog and let the user select a file
    file_path = askopenfilename(
        title="Odaberite .csv datoteku",
        filetypes=[("CSV files", "*.csv")],
        initialdir=r'C:\Users\Ivan\Desktop\NetFT-master\logiranje'
    )

    if file_path:
        print(f"Odabrana datoteka: {file_path}")
        time_data, force_data = load_csv_data(file_path)
        # Apply the filtering function to remove low-force periods
        filtered_time_data, filtered_force_data = filter_low_force_periods(time_data, force_data)
        plot_data(root, filtered_time_data, filtered_force_data, file_path)
        root.mainloop()
    else:
        print("Nije odabrana nijedna datoteka.")

if __name__ == '__main__':
    browse_and_load_file()
