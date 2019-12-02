from function_multi_layer import *
import img_gen as ig 

map_directory = 'maps'
files = read_map_directory(map_directory)
imgs_dic = ig.getAllTileImg("data/pics")
regions_map = code_map_regions(16, 11)
save_map("test" + str(1) + ".txt", read_file(files[0]))
#print(regions_map)
list_of_dependency = generate_dependency_matrix()
list_of_models = create_all_models(list_of_dependency, regions_map, files)
#inital_map = generat_initial_map(1,'D',1,'D',1,'D',0,'D')
#generated_map = generat_the_map(inital_map, regions_map, list_of_models, list_of_dependency)
#print(generated_map)
#ig.showRoom(generated_map ,imgs_dic)
for i in range(50):
	x = np.random.choice(2,4)
	while sum(x)==0:
		x = np.random.choice(2,4)
	inital_map = generat_initial_map(x[0],'D',x[1],'D',x[2],'D',x[3],'D')
	generated_map = generat_the_map(inital_map, regions_map, list_of_models, list_of_dependency)
	save_map("sample" + str(i) + ".txt", generated_map)
#	print(generated_map)
#	ig.showRoom(generated_map ,imgs_dic)

#for i in range(100000):
#	inital_map = generat_initial_map(1,'D',1,'D',1,'D',1,'D')
#	generat_the_map(inital_map, regions_map, list_of_models, list_of_dependency)
