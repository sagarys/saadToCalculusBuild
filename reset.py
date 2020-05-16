#!/usr/bin/env python
import os 
import shutil
# Get the list of all files and directories 

path_build = "\\\\bawdfs01\\OUTBOX\\TO-FC\\Sustaining_Builds"
dir_list = os.listdir(path_build) 

print("Files and directories in '", path_build, "' :")  
  

for directory in dir_list:
    prod_name = os.path.join(path_build,directory)
    subdir_list = os.listdir(os.path.join(path_build,directory))
    for subdir_file in subdir_list :
        if "_configspec" in subdir_file :
            print(os.path.join(prod_name,subdir_file))
            configspec_path = os.path.join(prod_name,subdir_file)
            os.remove(configspec_path)