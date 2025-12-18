import pandas as pd

# File path
file_path = r"C:\Users\agrawal-admin\Downloads\via_project_5Jul2025_1h32m_csv.csv" # Update with the correct path if needed

# Read the CSV file
df = pd.read_csv(file_path)

# Extract the folder number from the filename column
df["folder_number"] = df["filename"].str.split("/").str[0]

# Remove the folder number from the filename
df["filename"] = df["filename"].str.split("/").str[1]

# Generate separate CSV files for each folder number
for folder in df["folder_number"].unique():
    subset_df = df[df["folder_number"] == folder].drop(columns=["folder_number"])
    output_filename = f"via_export_csv_{folder}.csv"
    subset_df.to_csv(output_filename, index=False)
    print(f"Saved {output_filename}")