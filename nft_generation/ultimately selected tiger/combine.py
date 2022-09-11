import os
import subprocess
import shutil
from distutils.dir_util import copy_tree

## define your paths
# path1 = './all_tigers/abyssBlue/centralComplex'
# path2 = './all_tigers/black/centralComplex'

# ## where to place the merged data
# merged_path = './combined'

# ## write an rsync commands to merge the directories
# rsync_cmd = 'rsync' + ' -avzh ' + path1 + ' ' + path2 + ' ' + merged_path

# ## run the rsync command
# subprocess.run(rsync_cmd, shell=True)

components = [
    "centralComplex",
    "forehead",
    "leftComplex",
    "leftEar",
    "leftEye",
    "leftEyeCross",
    "leftIris",
    "leftNose",
    "nose",
    "rightComplex",
    "rightEar",
    "rightEye",
    "rightEyeCross",
    "rightIris",
    "scatteredComplex",
    "sides",
    "background"
    ]
# possible colours 
# 'white','paleOrange','darkChocolate', 'swamp', 'woods', 'yellow', 'sky'
# 'emerald','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue'
# 'mint', 'jade', 'lemon', 'milkChocolate', 'lightBlue', 'cyan', 'deepForest'
# 'grey', 'dory', 'rice', 'emerald', 'rose', 'lavendar', 'forest', 'paleWhite', 'paleJade'
# 'greyBlue', 'gold', 'lightSky', 'sapphire', 'strawberry', 'red', 'neonPurple'
# 'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', "peach"

# 
colours = ['white','paleOrange','darkChocolate', 'swamp', 'woods', 'yellow', 'sky',
'emerald','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue'
'mint', 'jade', 'lemon', 'milkChocolate', 'cyan', 'deepForest'
'grey', 'dory', 'rice', 'emerald', 'rose', 'lavendar', 'forest', 'paleWhite', 'paleJade'
'greyBlue', 'gold', 'lightSky', 'sapphire', 'strawberry', 'red', 'neonPurple'
'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', "peach"]
# colours = ['white','paleOrange','darkChocolate', 'swamp', 'woods', 'yellow', 'sky',
# 'emerald','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue'
# 'mint', 'jade', 'lemon', 'milkChocolate', 'lightBlue', 'cyan', 'deepForest'
# 'grey', 'dory', 'rice', 'emerald', 'rose', 'lavendar', 'forest', 'paleWhite', 'paleJade'
# 'greyBlue', 'gold', 'lightSky', 'sapphire', 'strawberry', 'red', 'neonPurple'
# 'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', "peach"]

# possible colours for irises
# "emerald", "grass", "lavendar", "neonGreen", "paleJade", "paleOrange", "rice", "sky", "strawberry", "empty"

iris_colours = ["emerald", "grass", "lavendar", "neonGreen", "paleJade", "paleOrange", "rice", "sky", "strawberry", "empty"]





def combine(colours=list, iris_colours=list):
    
    merged_path = './combined'
    # wipe the state clean
    shutil.rmtree(merged_path)
    shutil.rmtree("../layers")
    
    # ordinary components that are not irises 
    paths = []
    for colour in colours: 
        for component in components: 
            path = f'./all_tigers/{colour}/{component}'
            paths.append(path)
    # print(paths)

    ## write an rsync commands to merge the directories
    sub_path = ' '.join(paths)
    # print(sub_path)
    rsync_cmd = 'rsync' + ' -avzh ' + sub_path + ' ' + merged_path

    ## run the rsync command
    subprocess.run(rsync_cmd, shell=True)

    iris_paths = []
    irises = ["rightIris", "leftIris"]
    for iris_colour in iris_colours:
        for iris in irises: 
            print(iris_colour, iris)
            iris_path = f'./all_tigers/{iris_colour}/{iris}'
            iris_paths.append(iris_path)
    print(iris_paths)
    sub_iris_path = ' '.join(iris_paths)
    # print(sub_iris_path)
    rsync_cmd_iris = 'rsync' + ' -avzh ' + sub_iris_path + ' ' + merged_path
    subprocess.run(rsync_cmd_iris, shell=True)


    # move background
    shutil.copytree("./components/background", merged_path+"/background")
    shutil.copytree("./combined", "../layers")



combine(colours, iris_colours)

