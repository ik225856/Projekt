import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, simpledialog
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
            force_data.append(float(row[1]))  # Učitavamo sve vrijednosti, uključujući negativne
    return time_data, force_data

def plot_data(time_data1, force_data1, time_data2, force_data2, time_data3, force_data3, title, legend1, legend2, legend3, file_name):
    """Plots the time vs force graph with custom title and legend."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting the three datasets
    ax.plot(time_data1, force_data1, label=legend1, color='blue')
    ax.plot(time_data2, force_data2, label=legend2, color='red')
    ax.plot(time_data3, force_data3, label=legend3, color='darkgreen')  # Treća datoteka u tamno zelenoj boji
    
    # Setting labels and title with Times New Roman font
    ax.set_xlabel('Vrijeme, s', fontname='Times New Roman', fontsize=14)
    ax.set_ylabel('Aksijalna sila, N', fontname='Times New Roman', fontsize=14)
    ax.set_title(title, fontname='Times New Roman', fontsize=14)
    ax.grid(True)
    
    # Postavljanje vremenskih oznaka na x-osi svakih 1 sekundu
    ax.set_xticks(np.arange(min(min(time_data1), min(time_data2), min(time_data3)), max(max(time_data1), max(time_data2), max(time_data3))+1, 1))
    
    # Adjust the plot to ensure there is more space at the top for the legend
    fig.subplots_adjust(top=0.90)  # Increase space at the top of the plot for the legend
    
    # Create a draggable legend in the top-right corner
    legend = ax.legend(loc='upper right')
    legend.set_draggable(True)  # Allow the legend to be moved interactively
    
    # Save the plot as an image
    image_path = os.path.splitext(file_name)[0] + '_updated.png'
    plt.savefig(image_path)
    print(f"Grafikon spremljen kao {image_path}")
    
    plt.show()

def browse_and_load_file():
    """Opens a file dialog to let the user select .csv files and displays the plot."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Prompt for title and legend texts
    title = simpledialog.askstring("Naslov", "Unesite naslov grafa:")
    legend1 = simpledialog.askstring("Legenda", "Unesite tekst za prvu legendu:")
    legend2 = simpledialog.askstring("Legenda", "Unesite tekst za drugu legendu:")
    legend3 = simpledialog.askstring("Legenda", "Unesite tekst za treću legendu:")

    # Open a file dialog and let the user select the first file
    file_path1 = askopenfilename(
        title="Odaberite prvu .csv datoteku",
        filetypes=[("CSV files", "*.csv")],
        initialdir=r'C:\Users\Ivan\Desktop\NetFT-master\logiranje'
    )

    if file_path1:
        print(f"Odabrana prva datoteka: {file_path1}")
        time_data1, force_data1 = load_csv_data(file_path1)
        
        # Open a file dialog and let the user select the second file
        file_path2 = askopenfilename(
            title="Odaberite drugu .csv datoteku",
            filetypes=[("CSV files", "*.csv")],
            initialdir=r'C:\Users\Ivan\Desktop\NetFT-master\logiranje'
        )

        if file_path2:
            print(f"Odabrana druga datoteka: {file_path2}")
            time_data2, force_data2 = load_csv_data(file_path2)
            
            # Open a file dialog and let the user select the third file
            file_path3 = askopenfilename(
                title="Odaberite treću .csv datoteku",
                filetypes=[("CSV files", "*.csv")],
                initialdir=r'C:\Users\Ivan\Desktop\NetFT-master\logiranje'
            )

            if file_path3:
                print(f"Odabrana treća datoteka: {file_path3}")
                time_data3, force_data3 = load_csv_data(file_path3)

                plot_data(time_data1, force_data1, time_data2, force_data2, time_data3, force_data3, title, legend1, legend2, legend3, file_path1)
            else:
                print("Nije odabrana treća datoteka.")
        else:
            print("Nije odabrana druga datoteka.")
    else:
        print("Nije odabrana prva datoteka.")

if __name__ == '__main__':
    browse_and_load_file()
