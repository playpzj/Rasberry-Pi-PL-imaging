import pandas as pd
import numpy as np
import os
import re

path = r""  # select the folder containing the CSV files which have the RGB values

# Define a function to sort column with ageing hours and exposure time 
def extract_numeric_part(column_name):
    match_h = re.search(r'\d+(?=h)', column_name)
    match_ms = re.search(r'\d+(?=ms)', column_name)
    match_a = re.search(r'\d+(?=A)', column_name)
    
    if match_h and match_ms and match_a:
        return (int(match_h.group()), int(match_ms.group()), int(match_a.group()))
    elif match_h and match_ms:
        return (int(match_h.group()), int(match_ms.group()), float('inf'))
    elif match_h and match_a:
        return (int(match_h.group()), float('inf'), int(match_a.group()))
    elif match_ms and match_a:
        return (0, int(match_ms.group()), int(match_a.group()))
    elif match_h:
        return (int(match_h.group()), float('inf'), float('inf'))
    elif match_ms:
        return (0, int(match_ms.group()), float('inf'))
    elif match_a:
        return (0, float('inf'), int(match_a.group()))
    return (0, float('inf'), float('inf'))

# Calculate the QFLS = kBT * ln (PLQY * (JG/J0,rad)), 226.6, 125.9 and 50.4 A m-2 are JG under 0.9, 0.5 and 0.2 suns, 1 suns is 95% SQ limit = 25.175 mA cm-2
# J0,rad,25C is 4.64059E-20 A m-2 , J0,rad,85C is 1.28410E-15 A m-2
QFLS_25C_6A = lambda x: (8.617333E-5*298.15) * np.log((x/5828590) * (226.6/4.64059E-20))
QFLS_25C_3A = lambda x: (8.617333E-5*298.15) * np.log((x/3238106) * (125.9/4.64059E-20))
QFLS_25C_1A = lambda x: (8.617333E-5*298.15) * np.log((x/1295242) * (50.4/4.64059E-20))
QFLS_85C_6A = lambda x: (8.617333E-5*358.15) * np.log((x/5828590) * (226.6/1.28410E-15))
QFLS_85C_3A = lambda x: (8.617333E-5*358.15) * np.log((x/3238106) * (125.9/1.28410E-15))
QFLS_85C_1A = lambda x: (8.617333E-5*358.15) * np.log((x/1295242) * (50.4/1.28410E-15))

for CSVFile in os.listdir(path):
    if CSVFile.endswith('_name.csv'):
        csv_sum = os.path.join(path, CSVFile)
        sum = pd.read_csv(csv_sum)
        sum.index += 1

        # Select specific columns
        _25Clight = sum.loc[:, sum.columns.str.contains('SampleName') | (sum.columns.str.contains('25Clight') & sum.columns.str.contains('50ms') &  sum.columns.str.contains('Red'))]

        # Sort columns based on hours
        sorted_columns = sorted(_25Clight.columns[1:], key=extract_numeric_part)
        _25Clight = _25Clight[['SampleName'] + sorted_columns]

        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_25Clight_50ms_Red.csv'))
        _25Clight.to_csv(output_file, index=True)

        # To divide 5828590 [(Red_counts/s)/PLQY_100%] from all columns except the first one
        # 5828590 [(Red_counts/s)/PLQY_100%] is the reference red counts/s value for 100% PLQY
        # this value is obtained by calculating the red value from known PLQY perovskite film sample (PLQY ~ 20%) under the 1 sun, then multiple the red value with 5 (100/20)
        # 6A, 3A and 1A are the current of applied to the power source , making the light intensity 0.9, 0.5 and 0.2 suns respectively
        _25Clight_PLQY = _25Clight.copy()
        # _25Clight_PLQY.iloc[:, 1:] /= 5828590
        for column in _25Clight_PLQY.columns:
            if '6A' in column:
                _25Clight_PLQY[column] = _25Clight_PLQY[column]/5828590
            elif '3A' in column:
                _25Clight_PLQY[column] = _25Clight_PLQY[column]/3238106
            elif '1A' in column:
                _25Clight_PLQY[column] = _25Clight_PLQY[column]/1295242
        
        # Rename column with PLQY
        for column in _25Clight_PLQY.columns:
            if column.endswith('_Red(counts/s)'):
                new_column = column.replace('_Red(counts/s)', '_Red_PLQY')
                _25Clight_PLQY.rename(columns={column: new_column}, inplace=True)   
        
        # Export _25Clight_PLQY DataFrame to CSV
        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_25Clight_50ms_Red_PLQY.csv'))
        _25Clight_PLQY.to_csv(output_file, index=True)

        # Calculate the QFLS = kBT * ln (PLQY * (JG/J0,rad)), 226 A m-2 is JG under 0.9/1.0 suns, 4.64059E-20 A m-2 is J0,rad
        # Process the columns
        _25Clight_QFLS = _25Clight.copy()        
        for column in _25Clight_QFLS.columns:
            if '6A' in column:
                _25Clight_QFLS[column] = _25Clight_QFLS[column].apply(QFLS_25C_6A)
            elif '3A' in column:
                _25Clight_QFLS[column] = _25Clight_QFLS[column].apply(QFLS_25C_3A)
            elif '1A' in column:
                _25Clight_QFLS[column] = _25Clight_QFLS[column].apply(QFLS_25C_1A)

        # Rename column with QFLS
        for column in _25Clight_QFLS.columns:
            if column.endswith('_Red(counts/s)'):
                new_column = column.replace('_Red(counts/s)', '_Red_QFLS')
                _25Clight_QFLS.rename(columns={column: new_column}, inplace=True)   
        # _25Clight_QFLS = _25Clight.iloc[:, 1:].apply(QFLS_25C_6A)

        # # Combine the 0th column from _25Clight with _25Clight_QFLS DataFrame
        # _25Clight_QFLS.insert(0, _25Clight.columns[0], _25Clight.iloc[:, 0])

        # Export _25Clight_QFLS DataFrame to CSV
        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_25Clight_50ms_Red_QFLS.csv'))
        _25Clight_QFLS.to_csv(output_file, index=True)

############################
        # Select specific columns
        _85Cdark = sum.loc[:, sum.columns.str.contains('SampleName') | (sum.columns.str.contains('85Cdark') & sum.columns.str.contains('50ms') & sum.columns.str.contains('Red'))]

        # Sort columns based on hours
        sorted_columns = sorted(_85Cdark.columns[1:], key=extract_numeric_part)
        _85Cdark = _85Cdark[['SampleName'] + sorted_columns]

        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_85Cdark_50ms_Red.csv'))
        _85Cdark.to_csv(output_file, index=True)

        # To divide 5828590 [(Red_counts/s)/PLQY_100%] from all columns except the first one
        _85Cdark_PLQY = _85Cdark.copy()
        # _85Cdark_PLQY.iloc[:, 1:] /= 5828590
        for column in _85Cdark_PLQY.columns:
            if '6A' in column:
                _85Cdark_PLQY[column] = _85Cdark_PLQY[column]/5828590
            elif '3A' in column:
                _85Cdark_PLQY[column] = _85Cdark_PLQY[column]/3238106
            elif '1A' in column:
                _85Cdark_PLQY[column] = _85Cdark_PLQY[column]/1295242
        # Rename column with PLQY
        for column in _85Cdark_PLQY.columns:
            if column.endswith('_Red(counts/s)'):
                new_column = column.replace('_Red(counts/s)', '_Red_PLQY')
                _85Cdark_PLQY.rename(columns={column: new_column}, inplace=True)   
        # Export _85Cdark_PLQY DataFrame to CSV
        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_85Cdark_50ms_Red_PLQY.csv'))
        _85Cdark_PLQY.to_csv(output_file, index=True)
        
        # Calculate QFLS
        _85Cdark_QFLS = _85Cdark

        for column in _85Cdark_QFLS.columns:
            if '0h25C' in column or '317h25C' in column:
                if '6A' in column:
                    _85Cdark_QFLS[column] = _85Cdark_QFLS[column].apply(QFLS_25C_6A)
                elif '3A' in column:
                    _85Cdark_QFLS[column] = _85Cdark_QFLS[column].apply(QFLS_25C_3A)
                elif '1A' in column:
                    _85Cdark_QFLS[column] = _85Cdark_QFLS[column].apply(QFLS_25C_1A)
            else:
                if '6A' in column:
                    _85Cdark_QFLS[column] = _85Cdark_QFLS[column].apply(QFLS_85C_6A)
                elif '3A' in column:
                    _85Cdark_QFLS[column] = _85Cdark_QFLS[column].apply(QFLS_85C_3A)
                elif '1A' in column:
                    _85Cdark_QFLS[column] = _85Cdark_QFLS[column].apply(QFLS_85C_1A)
        # Rename column with QFLS
        for column in _85Cdark_QFLS.columns:
            if column.endswith('_Red(counts/s)'):
                new_column = column.replace('_Red(counts/s)', '_Red_QFLS')
                _85Cdark_QFLS.rename(columns={column: new_column}, inplace=True)   

        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_85Cdark_50ms_Red_QFLS.csv'))
        _85Cdark_QFLS.to_csv(output_file, index=True)

#############################
        # Select specific columns
        _85Clight = sum.loc[:, sum.columns.str.contains('SampleName') | (sum.columns.str.contains('85Clight')  & sum.columns.str.contains('50ms') & sum.columns.str.contains('Red'))]

        # Sort columns based on hours
        sorted_columns = sorted(_85Clight.columns[1:], key=extract_numeric_part)
        _85Clight = _85Clight[['SampleName'] + sorted_columns]

        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_85Clight_50ms_Red.csv'))
        _85Clight.to_csv(output_file, index=True)

        # To divide 5828590 [(Red_counts/s)/PLQY_100%] from all columns except the first one
        _85Clight_PLQY = _85Clight.copy()
        # _85Clight_PLQY.iloc[:, 1:] /= 5828590
        for column in _85Clight_PLQY.columns:
            if '6A' in column:
                _85Clight_PLQY[column] = _85Clight_PLQY[column]/5828590
            elif '3A' in column:
                _85Clight_PLQY[column] = _85Clight_PLQY[column]/3238106
            elif '1A' in column:
                _85Clight_PLQY[column] = _85Clight_PLQY[column]/1295242        
        # Rename column with PLQY
        for column in _85Clight_PLQY.columns:
            if column.endswith('_Red(counts/s)'):
                new_column = column.replace('_Red(counts/s)', '_Red_PLQY')
                _85Clight_PLQY.rename(columns={column: new_column}, inplace=True)  
        # Export _85Clight_PLQY DataFrame to CSV
        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_85Clight_50ms_Red_PLQY.csv'))
        _85Clight_PLQY.to_csv(output_file, index=True)
        
        # Calculate QFLS
        _85Clight_QFLS = _85Clight
        for column in _85Clight_QFLS.columns:
            if '0h25C' in column or '317h25C' in column:
                if '6A' in column:
                    _85Clight_QFLS[column] = _85Clight_QFLS[column].apply(QFLS_25C_6A)
                elif '3A' in column:
                    _85Clight_QFLS[column] = _85Clight_QFLS[column].apply(QFLS_25C_3A)
                elif '1A' in column:
                    _85Clight_QFLS[column] = _85Clight_QFLS[column].apply(QFLS_25C_1A)
            else:
                if '6A' in column:
                    _85Clight_QFLS[column] = _85Clight_QFLS[column].apply(QFLS_85C_6A)
                elif '3A' in column:
                    _85Clight_QFLS[column] = _85Clight_QFLS[column].apply(QFLS_85C_3A)
                elif '1A' in column:
                    _85Clight_QFLS[column] = _85Clight_QFLS[column].apply(QFLS_85C_1A)        
        # Rename QFLS
        for column in _85Clight_QFLS.columns:
            if column.endswith('_Red(counts/s)'):
                new_column = column.replace('_Red(counts/s)', '_Red_QFLS')
                _85Clight_QFLS.rename(columns={column: new_column}, inplace=True)           

        output_file = os.path.join(path, CSVFile.replace('_name.csv', '_85Clight_50ms_Red_QFLS.csv'))
        _85Clight_QFLS.to_csv(output_file, index=True)


print('Done')
