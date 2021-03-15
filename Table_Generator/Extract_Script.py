#!/home/ws/gt5111/testEnv/bin/python
import numpy as np
import matplotlib.pyplot as plt
import os, fnmatch
import sys, re, csv

def separate_string_number(string):
    previous_character = string[0]
    groups = []
    newword = string[0]
    for x, i in enumerate(string[1:]):
        if i.isalpha() and previous_character.isalpha():
            newword += i
        elif i.isnumeric() and previous_character.isnumeric():
            newword += i
        else:
            groups.append(newword)
            newword = i

        previous_character = i

        if x == len(string) - 2:
            groups.append(newword)
            newword = ''
    return groups

def find_parameter(file, Search_parameter):
    parameter_var = []
    nums = re.compile(r"[+-]?\d+(?:\.\d+)?")  # Regular expression
    with open(file, "r") as file1:
        for line in file1.readlines():
            if Search_parameter in line:
                idx1 = line.find('"')
                idx2 = line.find('"', idx1 + 1)
                field = line[idx1 + 1:idx2]
                array = nums.findall(field)
                # print(array)
                # print(Search_parameter)
                
                if len(array) > 0:
                    if Search_parameter == 'ENCUT':
                        parameter_var = np.around(float(array[0]), 3)
                    else:    
                        parameter_var = np.around(float(array[len(array)-1]), 3)
                else:
                    continue
        return parameter_var


def find_var1(file, Search_string):
    with open(file, "r") as file1:
        for line in file1.readlines():
            if Search_string in line:
                idx1 = line.find('"')
                idx2 = line.find('"', idx1 + 2)
                field = line[idx1 + 1:idx2 - 1]
        return str.strip(field.rpartition(' = ')[2])

def Filter(string, substr): 
	return[str1 for str1 in string if
			any(sub in str1 for sub in substr)] 

plt.rcParams['font.size'] = '14'
args = sys.argv[1:]
# print(args)
Search_file = args[0]  #"OUTCAR"
del_files = str(args[1])
#Plot_figure = str(args[2])

System_name = Search_file
Search_parameter_list = args[2:len(args)]   # "energy", "AL"
Search_file_list = []
Table_var = []

for file1 in os.listdir():
    if any(my_var in Search_file for my_var in separate_string_number(file1)):
        Search_file_list.append(file1)

for file in Search_file_list:
    for parameter_var in Search_parameter_list:
        temp_var1 = find_parameter(file, parameter_var)
        Table_var.append(temp_var1)

print(Search_parameter_list)
Table_var = np.array(Table_var)
Table_var = Table_var.reshape(len(Search_file_list), len(Search_parameter_list))
Sorted_Table = Table_var[np.argsort(Table_var[:, 1])]
#np.savetxt("Table_var", Sorted_Table, fmt="%s")

with open('Table_var', 'w') as f: 
    # using csv.writer method from CSV package 
    write = csv.writer(f) 
    # Columns label
    write.writerow(Search_parameter_list) 
    # Columns values
    write.writerows(Sorted_Table) 

if del_files == "True":
    for file in Search_file_list:
        os.remove(file)