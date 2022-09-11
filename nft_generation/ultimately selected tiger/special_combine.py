
from copy import deepcopy

import os
import subprocess
import shutil
from distutils.dir_util import copy_tree

from numpy import eye

# define your paths
# path1 = './all_tigers/abyssBlue/centralComplex'
# path2 = './all_tigers/black/centralComplex'

# ## where to place the merged data
# merged_path = './combined'

# ## write an rsync commands to merge the directories
# rsync_cmd = 'rsync' + ' -avzh ' + path1 + ' ' + path2 + ' ' + merged_path

# ## run the rsync command
# subprocess.run(rsync_cmd, shell=True)

backgroundColours = [
    'black',
    'blue',
    'chinaRed',
    'deepPurple',
    'grass',
    'grey',
    'jade',
    'lavendar',
    'lemon',
    'cyan',
    'lightSky',
    'magenta',
    'mint',
    'rose',
    'greenYellow',
    'silentBlue',
    'abyssViolet',
    'darkGrey',
    'deepGrey'
]


def twoShades(lightColour, deepColour, leftEyeCross, rightEyeCross, irisColour):
    components_to_colours = {
        "leftNose":         [lightColour],
        "forehead":         [lightColour],
        "rightComplex":     [lightColour],
        "leftComplex":      [deepColour],
        "centralComplex":   [deepColour],
        "nose":             [deepColour],
        "sides":            [deepColour],
        "scatteredComplex": [lightColour, deepColour],
        "leftEar":          [lightColour],
        "rightEar":         [deepColour],
        "leftEye":          [lightColour],
        "rightEye":         [deepColour],
        "leftEyeCross":     [leftEyeCross],
        "rightEyeCross":    [rightEyeCross],
        "leftIris":         [irisColour],
        "rightIris":        [irisColour],
        "background":       backgroundColours,
    }

    return components_to_colours




def anime(lightColour, irisColour, eyeCrossColour):
    components_to_colours = {
        "leftNose":         [lightColour, 'black'],
        "forehead":         [lightColour, 'black'],
        "rightComplex":     [lightColour, 'black'],
        "leftComplex":      [lightColour, 'black'],
        "centralComplex":   [lightColour, 'black'],
        "nose":             [lightColour, 'black'],
        "sides":            [lightColour],
        "scatteredComplex": [lightColour],
        "leftEar":          [lightColour, 'black'],
        "rightEar":         [lightColour, 'black'],
        "leftEye":          [lightColour, 'black'],
        "rightEye":         [lightColour, 'black'],
        "leftEyeCross":     [eyeCrossColour],
        "rightEyeCross":    [eyeCrossColour],
        "leftIris":         [irisColour],
        "rightIris":        [irisColour],
        "background":       backgroundColours,
    }

    return components_to_colours
    


def specialCombineMultipleColours(components_to_colours):
    
    merged_path = './combined'
    # wipe the state clean
    shutil.rmtree(merged_path)
    shutil.rmtree("../layers")
    
    # ordinary components that are not irises 
    paths = []
    for component, colourList in components_to_colours.items():
        for colour in colourList: 
            path = f'./all_tigers/{colour}/{component}'
            paths.append(path)

    
    # print(paths)

    ## write an rsync commands to merge the directories
    sub_path = ' '.join(paths)
    # print(sub_path)
    rsync_cmd = 'rsync' + ' -avzh ' + sub_path + ' ' + merged_path

    ## run the rsync command
    subprocess.run(rsync_cmd, shell=True)

    
    # move background
    
    shutil.copytree("./components/background", merged_path+"/background")
    shutil.copytree("./combined", "../layers")


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
# 'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', "peach", "dirtyRose", "violetPink"

# 
colours = ['white','paleOrange','darkChocolate', 'swamp', 'woods', 'yellow', 'sky',
'emerald','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue'
'mint', 'jade', 'lemon', 'milkChocolate', 'lightBlue', 'cyan', 'deepForest'
'grey', 'dory', 'rice', 'emerald', 'rose', 'lavendar', 'forest', 'paleWhite', 'paleJade'
'greyBlue', 'gold', 'sapphire', 'strawberry', 'red', 'neonPurple'
'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', 'neonPink','violetPink', 'pencil']


simpleColours = ['darkChocolate', 'swamp', 'woods', 'sky',
'emerald','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue', 
'milkChocolate', 'lightBlue', 'cyan', 'deepForest'
'dory', 'emerald', 'silver', 'pencil','sapphire'
'greyBlue', 'gold', 'sapphire', 'strawberry', 'red', 'neonPurple'
'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', 'neonPink', 'violetPink', 'pencil','milktea','creamSeaweed']

darkColours = ['darkChocolate', 'emerald', 'royalBlue', 'purple', 'abyssBlue', 'black','red','blood','deepForest','leather']

# colours = ['white','paleOrange','darkChocolate', 'swamp', 'woods', 'yellow', 'sky',
# 'emerald','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue'
# 'mint', 'jade', 'lemon', 'milkChocolate', 'lightBlue', 'cyan', 'deepForest'
# 'grey', 'dory', 'rice', 'emerald', 'rose', 'lavendar', 'forest', 'paleWhite', 'paleJade'
# 'greyBlue', 'gold', 'lightSky', 'sapphire', 'strawberry', 'red', 'neonPurple'
# 'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', 'sunsetYellow', "peach"]

# possible colours for irises
# "emerald", "grass", "lavendar", "neonGreen", "paleJade", "paleOrange", "rice", "sky", "strawberry", "empty"

backgroundColours = [
    'black',
    'blue',
    'greenYellow',
    'silentBlue',
    'abyssViolet',
    'darkGrey',
    'deepGrey'
]
# 
components_to_colours = {
    "leftNose":         ['orange','sunsetYellow','purple','greyblue','creamSeaweed','emerald','swamp'],
    "forehead":         ['orange','sunsetYellow','purple','greyblue','creamSeaweed','emerald','swamp'],
    "rightComplex":     ['orange','sunsetYellow','purple','pencil','neonPink','greyblue','creamSeaweed','swamp'],
    "leftComplex":      ['orange','sunsetYellow','purple','pencil','neonPink','greyblue','creamSeaweed','swamp'],
    "centralComplex":   ['orange','sunsetYellow','purple','greyblue','creamSeaweed','emerald','swamp','black'],
    "nose":             ['abyssBlue','emerald','black'],
    "sides":            ['orange','sunsetYellow','purple','emerald','black'],
    "scatteredComplex": ['orange','sunsetYellow','purple','emerald','black'],
    "leftEar":          ['orange','sunsetYellow','purple','greyblue','creamSeaweed','dirtyRose','swamp'],
    "rightEar":         ['orange','sunsetYellow','purple','greyblue','creamSeaweed','dirtyRose','swamp'],
    "leftEye":          ['black'],
    "rightEye":         ['black'],
    "leftEyeCross":     ['blood','orange','neonPurple'],
    "rightEyeCross":    ['sapphire','woods'],
    "leftIris":         ['strawberry','sky','emerald','paleOrange','gold'],
    "rightIris":        ['strawberry','sky','emerald','paleOrange','gold'],
    "background":       backgroundColours,
}

components_to_colours = {
    "leftNose":         ['darkChocolate','woods','abyssBlue','greyBlue','creamSeaweed','pencil'],
    "forehead":         ['darkChocolate','woods','abyssBlue','orange','sunsetYellow','greyBlue','creamSeaweed','pencil','dirtyRose'],
    "rightComplex":     ['darkChocolate','woods','abyssBlue','greyBlue','creamSeaweed','pencil','dirtyRose'],
    "leftComplex":      ['darkChocolate','woods','abyssBlue','greyBlue','creamSeaweed','dirtyRose'],
    "centralComplex":   ['darkChocolate','woods','abyssBlue','orange','sunsetYellow','greyBlue','creamSeaweed','pencil','dirtyRose', 'peach'],
    "nose":             ['greyBlue','black', 'darkchocolate','abyssBlue'],
    "sides":            ['magenta','black','yellow','sunsetYellow','greyBlue','creamSeaweed','pencil','dirtyRose','orange','sunsetYellow','greyBlue','creamSeaweed','pencil','neonPink'],
    "scatteredComplex": ['magenta','black','yellow','sunsetYellow','greyBlue','creamSeaweed','pencil','dirtyRose','orange','sunsetYellow','greyBlue','creamSeaweed','pencil','neonPink'],
    "leftEar":          ['magenta','black','orange','sunsetYellow','greyBlue','creamSeaweed','pencil','dirtyRose'],
    "rightEar":         ['magenta','black','orange','sunsetYellow','greyBlue','creamSeaweed','pencil','dirtyRose'],
    "leftEye":          ['black','black','abyssBlue'],
    "rightEye":         ['black','black','abyssBlue'],
    "leftEyeCross":     ['sunsetYellow','black','orange','neonPurple'],
    "rightEyeCross":    ['sunsetYellow','sapphire','woods'],
    "leftIris":         ['strawberry','sky','emerald','paleOrange','gold'],
    "rightIris":        ['strawberry','sky','emerald','paleOrange','gold'],
    "background":       backgroundColours,
}

components_to_colours = {
    "leftNose":         ['black','peach'],
    "forehead":         ['black','peach'],
    "rightComplex":     ['black','peach'],
    "leftComplex":      ['black','peach'],
    "centralComplex":   ['black','peach'],
    "nose":             ['black','peach'],
    "sides":            ['black','peach'],
    "scatteredComplex": ['black','peach'],
    "leftEar":          ['black','peach'],
    "rightEar":         ['black','peach'],
    "leftEye":          ['black','peach'],
    "rightEye":         ['black','peach'],
    "leftEyeCross":     ['black'],
    "rightEyeCross":    ['black'],
    "leftIris":         ['strawberry'],
    "rightIris":        ['strawberry'],
    "background":       backgroundColours,
}


    



# components_to_colours = {
#         "leftNose":         simpleColours,
#         "forehead":         colours,
#         "rightComplex":     simpleColours,
#         "leftComplex":      simpleColours,
#         "centralComplex":   colours,
#         "nose":             darkColours,
#         "sides":            simpleColours,
#         "scatteredComplex": colours,
#         "leftEar":          simpleColours,
#         "rightEar":         simpleColours,
#         "leftEye":          darkColours,
#         "rightEye":         darkColours,
#         "leftEyeCross":     darkColours,
#         "rightEyeCross":    darkColours,
#         "leftIris":         colours,
#         "rightIris":        colours,
#         "background":       colours,
#     }


# components_to_colours = twoShades('woods', 'black', 'neonGreen')

# anime(lightColour, irisColour, eyeCrossColour)
# components_to_colours = anime('violetPink', 'strawberry', 'blood')
# twoShades(lightColour, deepColour, leftEyeCross, rightEyeCross, irisColour):
# components_to_colours = twoShades('dirtyRose', 'creamSeaweed','sapphire', 'sapphire','strawberry')
specialCombineMultipleColours(components_to_colours)




