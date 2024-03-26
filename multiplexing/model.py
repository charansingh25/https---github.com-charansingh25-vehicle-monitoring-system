# import os

# # List of cars
# cars = [
#     "INFINITI",
#     "HYUNDAI",
#     "RENAULT",
#     "FORD",
#     "TOYOTA",
#     "KIA",
#     "NISSAN",
#     "CHEVROLET",
#     "JEEP"
# ]

# # Display options to the user
# print("Select a vehicle from the list:")
# for i, car in enumerate(cars, start=1):
#     print(f"{i}. {car}")

# # Take user input for selecting a vehicle
# selected_option = int(input("\nEnter the number corresponding to your choice: "))

# # Validate user input
# if 1 <= selected_option <= len(cars):
#     vehicle_name = cars[selected_option - 1]
#     print(f"Selected vehicle: {vehicle_name}\n")
# else:
#     print("Invalid option. Please select a valid option.")

# # Take user input for the range of kilometers traveled
# km_traveled = float(input("Enter the range of kilometers traveled till now: "))

# # Display the user input
# print(f"Range of kilometers traveled: {km_traveled} km\n")

# # Allow the user to choose a directory
# directory_path = "E:\Coding\iot\smart-car-exhaust-new-new\modelfiles"

# # List all files in the specified directory
# try:
#     files = os.listdir(directory_path)
# except FileNotFoundError:
#     print(f"Error: Directory {directory_path} not found.")
#     exit()


# print(f"You are accessing file from directory : {directory_path}\n")


# # Display options to the user
# print("Select a file : ")
# for i, file in enumerate(files, start=1):
#     print(f"{i}. {file}")

# # Take user input for selecting a data file
# file_option = int(input("\nEnter the number corresponding to the file you want to read: "))
# selected_file = files[file_option - 1]
# file_path = os.path.join(directory_path, selected_file)

# # Read the sensor data from the selected text file
# try:
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
# except FileNotFoundError:
#     print(f"Error: File {file_path} not found.")
#     exit()

# # Extract data from the text file and calculate averages
# co2_percentage = sum(map(float, lines[0].split())) / len(lines[0].split())
# smoke_percentage = sum(map(float, lines[1].split())) / len(lines[1].split())
# co_percentage = sum(map(float, lines[2].split())) / len(lines[2].split())

# # Assuming coefficients a, b, and c
# a = 0.15
# b = 0.5
# c = 0.1
# d = 1

# # Calculate the estimated age using the linear formula
# estimated_age = int(a * (co2_percentage/10000) + b * smoke_percentage + c * co_percentage + d)

# print('\n')
# # Display the estimated age
# print(f"Estimated age for the vehicle: {estimated_age}")



import os
import tkinter as tk
from tkinter import ttk

def calculate_age():
    # Get user inputs from the UI
    selected_car = car_var.get()
    km_traveled = float(km_entry.get())
    selected_file = file_var.get()
    
    # Get the file path based on the selected directory and file
    file_path = os.path.join(directory_path, selected_file)
    
    # Read the sensor data from the selected text file
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        result_label.config(text=f"Error: File {file_path} not found.")
        return
    
    # Extract data from the text file and calculate averages
    co2_percentage = sum(map(float, lines[0].split())) / len(lines[0].split())
    smoke_percentage = sum(map(float, lines[1].split())) / len(lines[1].split())
    co_percentage = sum(map(float, lines[2].split())) / len(lines[2].split())


    print(f"CO2 percentage (mean) : {round(co2_percentage, 2)}%")
    print(f"smoke percentage (mean) : {round(smoke_percentage, 2)}%")
    print(f"CO percentage (mean) : {round(co_percentage, 2)}%\n")

    # Assuming coefficients a, b, and c
    a = 0.15
    b = 0.1
    c = 0.3
    d = 1

    # Calculate the estimated age using the linear formula
    estimated_age = (a * (co2_percentage) + b * smoke_percentage + c * co_percentage + d)

    # Display the estimated age in the UI
    result_label.config(text=f"Estimated age for {selected_car}: {estimated_age} years")

# Create the main window
window = tk.Tk()
window.title("Vehicle Age Estimation")

# Set the window size
window.geometry("600x400")

# List of cars
cars = [
    "INFINITI",
    "HYUNDAI",
    "RENAULT",
    "FORD",
    "TOYOTA",
    "KIA",
    "NISSAN",
    "CHEVROLET",
    "JEEP"
]

# Create variables to store user selections
car_var = tk.StringVar()
km_var = tk.StringVar()
file_var = tk.StringVar()

# Display options for car selection
car_label = tk.Label(window, text="Select a vehicle:", font=("Helvetica", 12))
car_label.grid(row=0, column=0, padx=80, pady=30)

car_dropdown = ttk.Combobox(window, textvariable=car_var, values=cars, state="readonly", font=("Helvetica", 12))
car_dropdown.grid(row=0, column=1, padx=70, pady=30)
car_dropdown.set("Select")

# Entry for entering kilometers traveled
km_label = tk.Label(window, text="Enter kilometers traveled:", font=("Helvetica", 12))
km_label.grid(row=1, column=0, padx=10, pady=10)

km_entry = tk.Entry(window, textvariable=km_var, font=("Helvetica", 13))
km_entry.grid(row=1, column=1, padx=10, pady=10)

# Display options for file selection
file_label = tk.Label(window, text="Select a file:", font=("Helvetica", 12))
file_label.grid(row=2, column=0, padx=10, pady=30)

# Allow the user to choose a directory
directory_path = "E:\\Coding\\iot\\smart-car-exhaust-new-new\\modelfiles"

# List all files in the specified directory
try:
    files = os.listdir(directory_path)
except FileNotFoundError:
    tk.messagebox.showerror("Error", f"Directory {directory_path} not found.")
    window.destroy()
    
file_dropdown = ttk.Combobox(window, textvariable=file_var, values=files, state="readonly", font=("Helvetica", 12))
file_dropdown.grid(row=2, column=1, padx=10, pady=10)
file_dropdown.set("Select")

# Button to calculate age
calculate_button = tk.Button(window, text="Calculate Age", command=calculate_age, font=("Helvetica", 14, "bold"))
calculate_button.grid(row=3, column=0, columnspan=2, pady=15)

# Label to display the result
result_label = tk.Label(window, text="", font=("Helvetica", 16, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()
