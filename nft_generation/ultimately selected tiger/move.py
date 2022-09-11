import os 
import re 
import shutil
import pprint

from unittest.util import three_way_cmp

from numpy import short
tigers = [
        "tiger_abyss_blue.idraw",
        "tiger_blood.idraw",
        "tiger_cherry.idraw",
        "tiger_chocolate.idraw",
        "tiger_dark_chocolate.idraw",
        "tiger_deep_forest.idraw",
        "tiger_dory.idraw",
        "tiger_emerald.idraw",
        "tiger_gold.idraw",
        "tiger_grey_black.idraw",
        "tiger_grey_blue.idraw",
        "tiger_milk_chocolate.idraw",
        "tiger_neon_purple.idraw",
        "tiger_orange.idraw",
        "tiger_purple.idraw",
        "tiger_red.idraw",
        "tiger_royal_blue.idraw",
        "tiger_sapphire.idraw",
        "tiger_swamp.idraw",
        "tiger_white.idraw",
        "tiger_woods.idraw",
        "tiger_yellow.idraw"
        "tiger_black.idraw"
    ]

layers = [
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

colours = {
    'white',       
    'paleOrange', 
    'darkChocolate', 'swamp', 'woods', 'yellow', 'sky', 'paper',
    'emerald', 'black', 'peach',
    'pencil','blood', 'neonGreen', 'chocolate', 'purple', 'royalBlue', 'mint', 'jade', 'lemon', 'milkChocolate', 'cyan', 'deepForest', 'grey', 'dory', 'rice', 'emerald', 'rose', 'lavendar', 'forest', 'paleWhite', 'paleJade', 'greyBlue', 'gold', 'lightSky', 'sapphire', 'strawberry', 'red', 'neonPurple', 'grass', 'orange', 'black', 'abyssBlue', 'blue', 'magenta', 'cherry', "sunsetYellow", "yellow", "empty", 'neonPink', 'chinaRed',
    'greenYellow', 'silentBlue', 'abyssViolet', 'darkGrey', 'deepGrey', 'violetPink', 'dirtyRose', 'cream', 'silver',
    'leather','matcha','cappucino', 'creamSeaweed','milktea'

    
    }


motherDir = "./svg/"
svgDir = "./svg/"
tigerDir = './all_tigers/'

def mkdirs():
    
    dirs = []
    for colour in colours: 
        os.mkdir(f'./all_tigers/{colour}')

        # print(dir)

def makeComponentDirs():
    for layer in layers: 
        component = f"./components/{layer}" 
        # print(tiger_layered)
        os.mkdir(component)

def copySVGToComponents():
    for file in os.listdir(svgDir):
        # files.append(file)
        
        file = file.replace(".svg","")
        # print(file)
        colour = re.split("\_",file)[-1]
        # print(colour)
        component = re.split("\_",file)[0]
        # print(component)
        src = f"./svg/{file}.svg"
        dst = f'./components/{component}/{file}.svg'
        # print(src, dst)
        print(dst)

        if src != "./svg/.DS_Store.svg":
            shutil.copyfile(src, dst)


def makeLayerDirs(): 
    
    for colour in colours:
        for layer in layers: 
            if (layer != "background"):
                tiger_layered = f"./all_tigers/{colour}/{layer}/" 
                # print(tiger_layered)
                os.mkdir(tiger_layered)

    

    
def moveSvgIntoTiger():

    for file in os.listdir(svgDir):        
    
        file = file.replace(".svg","")
        # print(file)
        colour = re.split("\_",file)[-1]
        # print(colour)
        component = re.split("\_",file)[0]
        # print(component)
        src = f"./svg/{file}.svg"
        
        if component == "background":
            dst = f'./all_tigers/{component}/{file}.svg'    
        else:
            dst = f'./all_tigers/{colour}/{component}/{file}.svg'
        # print(src, dst)
        # print(dst)

        if ((src != "./svg/.DS_Store.svg") & (component != "background")):
            shutil.copyfile(src, dst)
            

    

# moveSvgIntoTiger()

def main(): 
    shutil.rmtree('./all_tigers')
    os.mkdir("./all_tigers")	
    shutil.rmtree('./components')
    os.mkdir("./components")	
    mkdirs()
    makeLayerDirs()
    moveSvgIntoTiger()
    makeComponentDirs()
    copySVGToComponents()

if __name__ == '__main__':
    main()


def checkColours():
    colours = []
    
    
    for file in os.listdir(svgDir):
        file = file.replace(".svg","")
        colour = re.split("\_",file)[-1]
        
        component = re.split("\_",file)[0]
        colours.append(colour)
        
    
    s = set(colours)
    print(s)
    return s
        
        
        
# checkColours()