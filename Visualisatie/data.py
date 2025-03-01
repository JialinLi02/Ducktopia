import csv
import random
import string

# Create a CSV file to store the data
filename = "Visualisatie/grid_data_3.csv"

# Open the file in write mode
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(["Location", "Value"])

    # Iterate over rows (A-Y) and columns (1-50)
    for row in string.ascii_uppercase[:25]:  # A-Y for 25 rows
        for col in range(1, 51):  # 1-50 for 50 columns
            location = f"{row}{col}"
            value = random.randint(10, 120)  # Random value between 10 and 120
            writer.writerow([location, value])

print(f"CSV file '{filename}' generated successfully.")
