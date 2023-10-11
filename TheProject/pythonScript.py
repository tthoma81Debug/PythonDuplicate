import os
import csv
import hashlib

def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""
    h = hashlib.sha1()
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest() 

def delete_duplicate_images():
    seen_files_dic = {}   # {hash: {name: filename}}
  
    removed_files = {}    # Track removed files and line numbers

    with open('files.csv', 'r') as f:
        csvreader = csv.reader(f)
        for i, row in enumerate(csvreader):
            file_name = row[0]
            if not os.path.isfile(file_name):
                continue
            file_hash = hash_file(file_name)
            if file_hash not in seen_files_dic:
                seen_files_dic[file_hash] = {file_name: i}
            else:
                os.remove(file_name)
                removed_files[file_name] = (file_hash, i) 

    # Write removed files hashes and line numbers
    with open('deleted_files.csv', 'w') as out:
        csvwriter = csv.writer(out)
        csvwriter.writerow(['File Name', 'File Hash', 'Line Number'])
        for f_name, (f_hash, line_num) in removed_files.items():
            csvwriter.writerow([f_name, f_hash, line_num])
   
if __name__ =='__main__':
    delete_duplicate_images()