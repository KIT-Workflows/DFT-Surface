#!/home/ws/gt5111/testEnv/bin/python
import shutil
import os, yaml, sys
import numpy as np

args = sys.argv[1:]
temp_var = str(args[0])
var_1 = str(args[1])

# Source path 
destination = os.getcwd()
#print(os.getcwd())
os.chdir('..')
os.chdir(os.path.dirname('Molecules/'))
source_mol = os.getcwd()
#print(os.getcwd())
os.chdir('..')
source = os.getcwd()
os.chdir(destination)
# Move the content of source to destination
file_var = "Input_data_" + temp_var + ".yml"
shutil.move(source+'/' + file_var, destination+'/' + file_var)

with open(file_var) as f:
    input_dic = yaml.full_load(f)

line = input_dic[var_1]
shutil.copy(source_mol+'/' + line, destination+'/' + line)

file_number = int(''.join(char for char in line if char.isdigit()))


with open(file_var, 'w') as file1:
    input_dic["File_number"] = file_number
    yaml.safe_dump(input_dic, file1)



