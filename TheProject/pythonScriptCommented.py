# We need to import the os and csv python modules for operating system and csv file operations, respectively.
# hashlib is for hashing the content of the file, which will be used for comparison
import os
import csv
import hashlib

# This function calculates a hash value (SHA-1) of the content of a file
def hash_file(filename):
    h = hashlib.sha1()  # create the hash object
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)  # read the file in chunks of 1024 bytes
            h.update(chunk)  # update the hash object
    return h.hexdigest()   # get the hexadecimal string of the hash

# The main function to delete duplicate files
def delete_duplicate_images():
    seen_files_dic = {}  # This will store a hash and the matching file's information (filename and line number)
    removed_files = {}   # This will store information about removed files

    # Open the CSV file that contains the file paths. Iterate over this file line by line (row by row)
    with open('files.csv', 'r') as f:
        csvreader = csv.reader(f)
        for i, row in enumerate(csvreader):
            file_name = row[0]
            
            # Check if the file exists. If it does not exist, the script skips to the next line of the CSV
            if not os.path.isfile(file_name):
                continue

            # If the file exists, the script calculates the file's hash.
            file_hash = hash_file(file_name)

            # If this hash has not been seen before, it is stored in the dictionary along with the file's line number
            if file_hash not in seen_files_dic:
                seen_files_dic[file_hash] = {file_name: i}
            # If this hash has been seen before, then it's a duplicate. The file is removed from the filesystem
            else:
                os.remove(file_name)
                # The removed file and its data are stored in another dictionary
                removed_files[file_name] = (file_hash, i)

    # After going through all files, the script writes down the removed files' data to a new csv file
    with open('deleted_files.csv', 'w') as out:
        csvwriter = csv.writer(out)
        csvwriter.writerow(['File Name', 'File Hash', 'Line Number'])
        for f_name, (f_hash, line_num) in removed_files.items():
            csvwriter.writerow([f_name, f_hash, line_num])

# We are calling our main function here
if __name__ =='__main__':
    delete_duplicate_images()

#The script takes all entries in `files.csv`, checks if they are genuine (existing) files, and then computes a hash of the file content using the `hash_file` function. If the hash is new, the file is considered unique and added to the `seen_files_dic`. If the hash has been seen before, the file is considered a duplicate and consequently removed from the system, and its data are stored in the `removed_files` dictionary. 