import os
import csv
import ntpath

def find_duplicates():

    # the folder path
    path = './images'

    seen_files_dic = {}   # {filename: line_num}
    duplicates_dic = {}   # {filename: line_num}

    with open('files.csv', 'r', newline='') as f:
        csvreader = csv.reader(f)
        all_rows = list(csvreader)

    # Loop to find the duplicate paths    
    for i, row in enumerate(all_rows):
        # assuming full directory with filename is in the first cell
        full_file_directory = row[0]

        # getting filename only without the prefix directory
        file_directory = ntpath.basename(full_file_directory)

        # check if file exists in the folder
        if not os.path.isfile(path + '/' + file_directory):
            continue
            
        # Check for duplicates
        if full_file_directory not in seen_files_dic:
            seen_files_dic[full_file_directory] = i
        else:
            duplicates_dic[full_file_directory] = i

    # Write duplicate paths and line numbers to 'duplicates.csv' 
    with open('duplicates.csv', 'w', newline='') as out:
        csvwriter = csv.writer(out)

        # headings
        csvwriter.writerow(['Duplicate File', 'Line Number'])

        for filename, line_num in duplicates_dic.items():
            csvwriter.writerow([filename, line_num])
            
    # Write non-duplicate rows to 'no_duplicates.csv'
    with open('no_duplicates.csv', 'w', newline='') as out:
        csvwriter = csv.writer(out)

        for i, row in enumerate(all_rows):
            if i not in duplicates_dic.values():
                csvwriter.writerow(row)


if __name__ =='__main__':
    find_duplicates()