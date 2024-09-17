import os
import csv
import tkinter as tk
from tkinter import filedialog
import numpy as np

def choose_directory():
    """Funkcija koja omogućuje odabir mape s .csv datotekama."""
    root = tk.Tk()
    root.withdraw()  # Sakrij Tkinter glavni prozor
    folder_path = filedialog.askdirectory(title="Odaberite mapu s .csv datotekama")
    return folder_path

def process_csv_files(folder_path):
    """Učitaj sve .csv datoteke iz odabrane mape i pronađi maksimalni iznos iz 2. stupca."""
    max_values = []
    
    # Prođi kroz sve datoteke u odabranoj mapi
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            print(f"Procesiranje datoteke: {file_path}")
            
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Preskoči header
                
                second_column_values = []
                
                # Učitaj sve retke i pohrani vrijednosti iz 2. stupca
                for row in csv_reader:
                    if len(row) > 1:  # Provjera da li postoji 2. stupac
                        try:
                            value = float(row[1])  # Pretvori vrijednost u float
                            second_column_values.append(value)
                        except ValueError:
                            print(f"Nevaljana vrijednost u retku: {row}")
                
                if second_column_values:
                    max_value = max(second_column_values)
                    max_values.append(max_value)
                    print(f"Maksimalna vrijednost u 2. stupcu za {filename} je {max_value}")
    
    return max_values

def calculate_mean(max_values):
    """Izračunaj aritmetičku sredinu maksimalnih vrijednosti."""
    if max_values:
        mean_value = np.mean(max_values)
        print(f"Aritmetička sredina maksimalnih vrijednosti je: {mean_value}")
        return mean_value
    else:
        print("Nema maksimalnih vrijednosti za izračun.")
        return None

if __name__ == "__main__":
    folder_path = choose_directory()
    
    if folder_path:
        max_values = process_csv_files(folder_path)
        calculate_mean(max_values)
    else:
        print("Mapa nije odabrana.")
