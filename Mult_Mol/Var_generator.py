#!/home/ws/gt5111/testEnv/bin/python
import numpy as np
import yaml, sys, json
import shutil, os, tarfile

with open("rendered_wano.yml") as file:
    wano_file = yaml.full_load(file)

#args = sys.argv[1:]

var_begin = float(wano_file.get("Var_begin"))#float(args[0])
var_end = float(wano_file.get("Var_end"))#float(args[1])
var_npoints = int(wano_file.get("N_points"))#int(args[2])
var_1 = wano_file.get("Var_name")#args[3] # z_axis
var_2 = wano_file.get("Molecule_name")#args[4] # Molecule_name

z_0 = []
step = np.abs(var_end-var_begin)/var_npoints
for i in range(0,var_npoints):
    sc = var_begin + step*i
    sc = round(sc,2)
    z_0.append(sc)

destination = os.getcwd()
my_tar = tarfile.open('Molecules.tar.xz')
os.chdir('..')
my_tar.extractall(os.getcwd())
my_tar.close()

cpt = sum([len(files) for r, d, files in os.walk(os.getcwd()+"/Molecules")])

########## extend z_0 list ################
z_0 = cpt*z_0

os.chdir('Molecules')
files_mol = os.listdir()
os.chdir('..')

m_x_n = var_npoints*cpt

count_file = 0

input_dic = {}

for i in range (0,m_x_n):
       if(i != 0 and i % var_npoints == 0):
              count_file = count_file + 1

       var_mol = files_mol[count_file]
       file_var = "Input_data"+"_"+str(i)+".yml"
       with open(file_var, 'w') as file1:
              input_dic[var_1] = float(z_0[i])
              input_dic[var_2] = var_mol
              yaml.safe_dump(input_dic, file1)    
              
os.chdir(destination) 

### Writing the variable to create the directories.
outdict = {}
outdict["iter"] = []
for i in range(0,m_x_n ):
       outdict["iter"].append(i)

with open("output_dict.yml",'w') as out:
    yaml.safe_dump(outdict, out)
