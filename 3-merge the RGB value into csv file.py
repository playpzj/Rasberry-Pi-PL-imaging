import os
import re
import pandas as pd

# Define the directory where your CSV files are located
folder_path = r'' # Add the path to the directory containing output results from ImageJ

# Define the regular expression pattern to extract the numeric value
pattern = r'\d+(?=ms)'

# Create sample_name
sample_name = []
letters = ['con', 'PEAI', 'PEABr', 'PEASCN', 'FPEAI', 'BAI', 'OAI', 'BDAI', 'GuaI', '3-APAI', 'ImI', 'TOPO']
numbers = ['1mM', '10mM', '100mM']

# Generate sample names
for i, letter in enumerate(letters):
    if i == 0:
        for j in range(1, 4):
            sample_name.append(f"{letter}-{j}")
    else:
        for number in numbers:
            sample_name.append(f"{letter}-{number}")


# Create the DataFrame
samplename_column = pd.DataFrame({'SampleName': sample_name})

# Function to extract the filename before a specific extension
def extract_filename(file_path, extension):
    filename = os.path.basename(file_path)
    return filename[:-len(extension)]

# Create the selected_columns
selected_columns = []

# Iterate over the subfolders, files, and directories in the directory
for root, dirs, files in os.walk(folder_path):
    for csv_file in files:
        if csv_file.endswith('.tiff_RGB.csv'):
            # Extract the numeric value from the file name
            match = re.search(pattern, csv_file)
            if match:
                value = int(match.group())

                # Load the CSV file into a DataFrame
                file_path = os.path.join(root, csv_file)
                df = pd.read_csv(file_path)

                # Extract the filename before the extension
                sample_condition = extract_filename(csv_file, '.tiff_RGB.csv')

                # Rename the Mean to Red
                df.rename(columns={'Mean': f'{sample_condition}_Red'}, inplace=True)

                # Copy the green and blue values
                df[f'{sample_condition}_Green'] = df.iloc[36:72, 2].reset_index(drop=True)
                df[f'{sample_condition}_Blue'] = df.iloc[72:108, 2].reset_index(drop=True)

                # Paste the values to column 4 and 5
                df.iloc[0:35, 3] = df[f'{sample_condition}_Green'].values[0:35]
                df.iloc[0:35, 4] = df[f'{sample_condition}_Blue'].values[0:35]

                # Delete the row from 36 to 108
                df.drop(df.index[36:108], inplace=True)

                # Divide specific columns by the extracted value and store in new columns
                columns_to_divide = [f'{sample_condition}_Red', f'{sample_condition}_Green', f'{sample_condition}_Blue']
                RGB_counts = [f'{col}(counts/s)' for col in columns_to_divide]
                df[RGB_counts] = df[columns_to_divide] / (value * 0.001)

                # Calculate gray scale
                Gray_value = (df[f'{sample_condition}_Red(counts/s)'] +
                              df[f'{sample_condition}_Green(counts/s)'] +
                              df[f'{sample_condition}_Blue(counts/s)']) / 3
                df[f'{sample_condition}_Gray(counts/s)'] = Gray_value

                # Select columns 6, 7, and 8
                selected_columns.append(df.iloc[:, 5:9])

print('Counts/s is Done')

# Concatenate the selected columns from all CSV files
RGB_value = pd.concat(selected_columns, axis=1)

# Combine the sample_name dataframe and RGB value dataframe
sample_condition_RGB_value = pd.concat([samplename_column, RGB_value], axis=1)

# Start index from 1
sample_condition_RGB_value.index = sample_condition_RGB_value.index + 1

# Output file name
output_file = os.path.join(folder_path, '20230525_passi_merge_name.csv')

# Write the concatenated columns to a new CSV file
sample_condition_RGB_value.to_csv(output_file, index=True)

print('Merge is Done')
