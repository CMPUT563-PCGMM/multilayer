import numpy as np
from os import listdir, getcwd
import random 
import pickle
import itertools
import copy
import objects

possible_tiles = ['F', 'B', 'M', 'P', 'O', 'I', 'D', 'S', '-']

def read_map_directory(map_directory):
	path = map_directory
	files = listdir(path)
	for i in range(len(files)):
		files[i] = map_directory + '\\' + files[i]
	return files


def read_file(file_name):
    first_list = []
    with open(file_name) as file:
        for line in file.readlines():
            second_list = []
            for j in line:
                if not j == '\n':
                    second_list.append(j)
            first_list.append(second_list)
    return np.array(first_list, dtype='str')
 

def code_map_regions(row, column):
    regions_map = np.zeros([2, row, column])
    for i in range(row):
        if i < 2 or i > row-3:
            regions_map[0, i, :] = 1
        elif (i>1 and i<4) or (i < row -2 and i > row - 5):
            regions_map[0, i, :] = 2
        elif (i>3 and i<6) or (i < row -4 and i > row - 7):
            regions_map[0, i, :] = 3
        elif (i>5 and i<8) or (i < row -6 and i > row - 9):
            regions_map[0, i, :] = 4
    for j in range(column):
        if j < 2 or j > column-3:
            regions_map[1, :, j] = 1
        elif (j>1 and j<4) or (j < column -2 and j > column - 5):
            regions_map[1, :, j] = 2
        elif (j>3 and j<6) or (j < column -4 and j > column - 7):
            regions_map[1, :, j] = 3
    return regions_map


def config_extract(map_array,regions_map, depenndancy_matrix, model_dict):
    sub_matrix_height = depenndancy_matrix.shape[0]
    sub_matrix_width = depenndancy_matrix.shape[1]
    for i in range(map_array.shape[0]-sub_matrix_height + 1-2):
        for j in range(map_array.shape[1]-sub_matrix_width + 1-2):
            map_submatrix = map_array[i:i+sub_matrix_height, j:j+sub_matrix_width]
            regions_map_submatrix = regions_map[:, i:i+sub_matrix_height, j:j+sub_matrix_width]
            config, key = config_reshape(map_submatrix, regions_map_submatrix, depenndancy_matrix)
            #config = tuple(config)
            config = tuple(list(config.ravel()))
            if not config in model_dict:
                model_dict[config] = objects.tile_values(key)
            else:
                model_dict[config].add_tile(key)


def config_reshape(map_submatrix, regions_map_submatrix, depenndancy_matrix):
    conf_list = []
    config_element_cnt = np.count_nonzero(depenndancy_matrix) - 1
    config = np.empty([3, config_element_cnt], dtype='str')
    cntr = 0
    for i in range(depenndancy_matrix.shape[0]):
        for j in range(depenndancy_matrix.shape[1]):
            if depenndancy_matrix[i,j] == 1:
                conf_list.append( map_submatrix[i, j])
                config[0, cntr] = map_submatrix[i, j]
                config[1, cntr] = regions_map_submatrix[0, i, j]
                config[2, cntr] = regions_map_submatrix[1, i, j]
                cntr = cntr + 1
            elif depenndancy_matrix[i,j] == 2:
                conf_list.append(regions_map_submatrix[0, i, j])
                conf_list.append(regions_map_submatrix[1, i, j])
                desired_tile = map_submatrix[i,j]
    return config, desired_tile  


def fliper(config):
    list_of_conf = [config]
    t = np.flip(config, axis=1)
    list_of_conf.append(t)
    t = np.flip(t, axis=0)
    list_of_conf.append(t)
    t = np.flip(t, axis=1)
    list_of_conf.append(t)
    return list_of_conf


def generat_initial_map(left_door, left_door_symbol, upper_door, upper_door_symbol, buttom_door, buttom_door_symbol, right_door, right_door_symbol=None):
    initial_map = np.empty([16,11], dtype='str')
    for i in range(initial_map.shape[0]):
        for j in range(initial_map.shape[1]):
            if i < 2 or j < 2 or i > 13 or j > 8:
                initial_map[i,j] = 'W'
            else:
                initial_map[i][j] = '?'
    if left_door:
        initial_map[7:9,1] = left_door_symbol
    if right_door:
        initial_map[7:9,9] = right_door_symbol
    if upper_door:
        initial_map[1,4:7] = upper_door_symbol
    if buttom_door:
        initial_map[14,4:7] = buttom_door_symbol
    return initial_map



def generat_the_map(initial_map, regions_map, model_dict_list, dependancy_matrix_list):
    map_height = initial_map.shape[0]
    map_width = initial_map.shape[1]
    model_index = len(model_dict_list) - 1
    for i,j in itertools.product(range(2,map_height-2), range(2,map_width-2)):
        generate_next_tile(initial_map, regions_map, model_dict_list, dependancy_matrix_list, model_index, i, j)
    return initial_map


    #dependancy_matrix_height = dependancy_matrix.shape[0]
    #dependancy_matrix_width = dependancy_matrix.shape[1]
    #for i, j in itertools.product(range(2,map_height-2), range(2,map_width-2)):
    #    sub_initial_map = initial_map[i-dependancy_matrix_height+1:i+1,j-dependancy_matrix_width+1:j+1]
    #    regions_map_sub_matrix = regions_map[:,i-dependancy_matrix_height+1:i+1,j-dependancy_matrix_width+1:j+1]
    #    config, key = config_reshape(sub_initial_map, regions_map_sub_matrix, dependancy_matrix)
    #    config = tuple(config)
    #    if config in model_dict:
            #print(config)
            #print(model_dict[config].print_object())
            #print(t)
    #        initial_map[i,j] = model_dict[config].generate_new_tile()
    #    else:
    #        print("failed")
    #        break
    #print(initial_map)


def generate_next_tile(initial_map, regions_map, model_dict_list, dependancy_matrix_list, model_index, i, j):
    model_dict = model_dict_list[model_index]
    dependancy_matrix = dependancy_matrix_list[model_index]
    dependancy_matrix_height = dependancy_matrix.shape[0]
    dependancy_matrix_width = dependancy_matrix.shape[1]
    sub_initial_map = initial_map[i-dependancy_matrix_height+1:i+1,j-dependancy_matrix_width+1:j+1]
    regions_map_sub_matrix = regions_map[:,i-dependancy_matrix_height+1:i+1,j-dependancy_matrix_width+1:j+1]
    config, key = config_reshape(sub_initial_map, regions_map_sub_matrix, dependancy_matrix)
    #config = tuple(config)
    config = tuple(list(config.ravel()))
    if config in model_dict:
        initial_map[i,j] = model_dict[config].generate_new_tile()
        print(model_index)
    elif model_index > 0:
        generate_next_tile(initial_map, regions_map, model_dict_list, dependancy_matrix_list, model_index-1, i, j)
    else:
        initial_map[i,j] = possible_tiles[int(np.random.choice(len(possible_tiles),1))]
        #print("bgaaaaa raftimmmmmm")

def generate_dependency_matrix():
    list_of_dependency_matrix = []
    d1 = np.ones([1,2])
    d1[0,1]=2
    list_of_dependency_matrix.append(d1)
    d2 = np.ones([2,2])
    d2[0,0]=0
    d2[1,1]=2
    list_of_dependency_matrix.append(d2)
    d3 = np.ones([1,3])
    d3[0,2] = 2
    list_of_dependency_matrix.append(d3)
    d4 = np.ones([2,2])
    d4[0,1] = 0
    d4[1,1] = 2
    list_of_dependency_matrix.append(d4)
    d5 = np.ones([2,2])
    d5[1,1] = 2
    list_of_dependency_matrix.append(d5)
    d6 = np.ones([2,3])
    d6[0,0:2]=0
    d6[1,2]=2
    list_of_dependency_matrix.append(d6)
    return(list_of_dependency_matrix)


def create_all_models(list_of_dependency_matrix, regions_map, files):
    list_of_models = []
    for each_dependancy_matrix in list_of_dependency_matrix:
        model_dict = {}
        for i in range(len(files)):
            sample = read_file(files[i])
            confs = fliper(sample)
            for each_conf in confs:
                config_extract(each_conf, regions_map, each_dependancy_matrix, model_dict)
        for i in model_dict:
            #print(i)
            model_dict[i].calculate_CPD()
        list_of_models.append(model_dict)
    return list_of_models


def save_map(file_name, gen_map):
    with open(file_name, 'w')as file:
        for i in range(gen_map.shape[0]):
            for j in range(gen_map.shape[1]):
                file.write(gen_map[i,j])
            file.write('\n')