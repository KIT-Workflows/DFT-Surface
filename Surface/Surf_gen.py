#!/home/ws/gt5111/testEnv/bin/python
import matplotlib.pyplot as plt
import numpy as np
import re, sys, os, subprocess, yaml

import pymatgen
import pymatgen.io.vasp.sets 
from pymatgen import Lattice
from pymatgen import Structure, Molecule
from pymatgen.core.surface import SlabGenerator
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.analysis.adsorption import plot_slab

def clean_num(srt_var):
    alphanumeric_filter = filter(str.isalnum, srt_var)
    alphanumeric_string = "".join(alphanumeric_filter)
    return alphanumeric_string
def clean_tuple(my_list):
    my_list = [clean_num(i) for i in my_list]
    my_list = list(filter(None, my_list))
    my_list = [int(i) for i in my_list]
    my_list =  tuple(my_list)
    return my_list


def surf_type(var_space_group):
    if var_space_group == "FCC":
        type_space_group = "Fm-3m" 
    elif var_space_group == "BCC":
        type_space_group = "Im-3m"
    elif var_space_group == "SC":
        type_space_group = "Pm-3m"
    elif var_space_group == "DC":
        type_space_group = "Fd-3m"
    elif var_space_group == "Graphene":
        type_space_group = "Graphene_C"    
    else:    
        type_space_group = None
    
    return type_space_group    
    
########### Inputs parameters ######################
args = sys.argv[1:]
type_space_group = surf_type(args[0])
type_element = args[1]
lattice_const = float(args[2])
Slab_size = float(args[3])
Vacuum_size = float(args[4])
Miller_index = clean_tuple(args[5:12])
Super_cell_size = clean_tuple(args[15:22])
Mol_flag = args[23]
Aux_var = str(args[26])
Mol_name = str(args[27])

file_var = "Input_data_" + Aux_var + ".yml"
print(file_var)
######## end of inputs parameters ###################

if type_space_group == "Graphene_C":
    Unit_cell = Structure.from_file("Graphene_POSCAR")
    supercell = Unit_cell*Super_cell_size
else:
    Unit_cell = Structure.from_spacegroup(type_space_group, Lattice.cubic(lattice_const),[type_element],[[0.0, 0.0, 0.0]])
    slabgen_Unit_cell = SlabGenerator(Unit_cell, Miller_index, Slab_size, Vacuum_size)
    slabs_Unit_cell = slabgen_Unit_cell.get_slabs()
    Unit_cell = slabs_Unit_cell[0]
    supercell = slabs_Unit_cell[0]*Super_cell_size


if Mol_flag == "True" and type_space_group != "Graphene_C":

    if os.path.exists("molecule.xyz"):
        file_mol = "molecule.xyz"
        Mol_surf_dist = float(args[24])
    elif os.path.exists(file_var):
        with open(file_var) as f:
            input_dic = yaml.full_load(f)
        
        file_mol = input_dic[Mol_name]
        Mol_surf_dist = args[24]
        Mol_surf_dist = input_dic[Mol_surf_dist]
    else:
        exit
 
    Mol_Mol_imag = float(args[25])
    asf = AdsorbateSiteFinder(Unit_cell)
    ads_sites = asf.find_adsorption_sites()
    ads_coord = ads_sites["ontop"][0]
    adsorbate1 = Molecule.from_file(file_mol)
    ads_structs = asf.generate_adsorption_structures(adsorbate1, min_lw=Mol_Mol_imag, find_args={"distance": Mol_surf_dist})
    ads_structs[0] = ads_structs[0].get_sorted_structure(reverse=True)
    ads_structs[0].to(filename=("POSCAR"))

elif Mol_flag == "True" and type_space_group == "Graphene_C":
    
    if os.path.exists("molecule.xyz"):
        file_mol = "molecule.xyz"
        Mol_surf_dist = float(args[24])
    elif os.path.exists(file_var):
        with open(file_var) as f:
            input_dic = yaml.full_load(f)
        
        file_mol = input_dic[Mol_name]
        Mol_surf_dist = args[24]
        Mol_surf_dist = input_dic[Mol_surf_dist]
    else:
        exit
    
    print(Mol_surf_dist)
    Mol_Mol_imag = float(args[25])
    asf = AdsorbateSiteFinder(Unit_cell)
    ads_sites = asf.find_adsorption_sites()
    ads_coord = ads_sites["ontop"][0]
    ads_coord = [ads_coord[0], ads_coord[1], Mol_surf_dist]
    adsorbate1 = Molecule.from_file(file_mol)
    ads_structs = asf.add_adsorbate(adsorbate1, ads_coord, repeat=Super_cell_size)
    ads_structs = ads_structs.get_sorted_structure(reverse=True)
    ads_structs.to(filename=("POSCAR"))
else:
    supercell.to(filename=("POSCAR"))

###################################################################################