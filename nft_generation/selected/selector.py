from select import select
import shutil
from os import listdir
from os.path import isfile, join


selectedImagesPath = "./selected_images";
selectedJsonPath = "./selected_json";
oldJsonPath = "../build/json";
orphanedPath = '../orphaned'

def distribution(selectedImagesPath, selectedJsonPath):
    selectedImages  = [f[0:-4] for f in listdir(selectedImagesPath) if isfile(join(selectedImagesPath, f))]
    selectedJsons   = [j[0:-5] for j in listdir(selectedJsonPath) if isfile(join(selectedJsonPath, j))]
    shared = set(selectedImages).intersection(set(selectedJsons))
    image_extras = [f not in shared for f in selectedImages]
    json_extras  = [j not in shared for j in selectedJsons ]    
    print("The number of images:", len(selectedImages), "the number of jsons:",len(selectedJsons), "shared:", len(shared), "extra images:", len(image_extras), "extra jsons:", len(json_extras))

def moveMetadata(selectedImagesPath, selectedJsonPath, oldJsonPath):
    selectedImages  = [f[0:-4] for f in listdir(selectedImagesPath) if isfile(join(selectedImagesPath, f))]
    selectedJsons   = [j[0:-5] for j in listdir(selectedJsonPath) if isfile(join(selectedJsonPath, j))]
    jsonInBuild = [j[0:-5] for j in listdir(oldJsonPath) if isfile(join(oldJsonPath, j))]
    # print(jsonInBuild)
    for image in selectedImages:
        src = f"../build/json/{image}.json"
        dst = f"./selected_json/{image}.json"
        
        if image in jsonInBuild:
            
            shutil.copyfile(src, dst)
            print(f"{image} was moved!")
        
        # print(json)


        # shutil.copyfile(src, dst)
    
    distribution(selectedImagesPath, selectedJsonPath)
    
    
def moveOrphaned(selectedImagesPath, selectedJsonPath, orphanedPath, oldJsonPath):
    moveMetadata(selectedImagesPath, selectedJsonPath, oldJsonPath)
    selectedImages  = [f[0:-4] for f in listdir(selectedImagesPath) if isfile(join(selectedImagesPath, f))]
    selectedJsons   = [j[0:-5] for j in listdir(selectedJsonPath) if isfile(join(selectedJsonPath, j))]

    for image in selectedImages:
        # if image != "aggregate_metadata.":
        if ((image not in selectedJsons) and image != "aggregate_metadata." and image !=".DS_S"): 
            src = f"./selected_images/{image}.png"
            dst = f"../orphaned/{image}.png"
            shutil.copyfile(src, dst)
    

# moveOrphaned(selectedImagesPath, selectedJsonPath, orphanedPath, oldJsonPath)

moveMetadata(selectedImagesPath, selectedJsonPath, oldJsonPath)
    
# async function moveMetadata(selectedImagesPath, outputJsonPath, oldJsonPath) {
  
# #   // This reads all the files in the dir where all the images I've selected
# #   // and poduces a list of their names
  
#     //  reads all the png files 
#     const selectedImagesFileNames = readFilesSync(selectedImagesPath);
#     //  reads all the json files 
#     const oldJsonFileNames        = readFilesSync(oldJsonPath);
    
#     let newMetadataFile = [];

#     // s.push('2')
#     // console.log(s)
#     oldJsonFileNames.forEach(fileName => {
        
#         const dna = fileName.substring(0,fileName.length-5);
        
#         if (selectedImagesFileNames.includes(dna+".png")) {
#             fs.copyFile(path.join(oldJsonPath,fileName), path.join(outputJsonPath,fileName), (err) => {
#                 if (err) throw err;
#                 console.log(`${fileName} was moved!~`);
#             });
#             const data = fs.readFile(path.join(outputJsonPath,fileName), 'utf8' , (err, data) => {
#                 if (err) {
#                   console.error(err)
#                   return
#                 }
#             const json = JSON.parse(data);
#             console.log(json);
#             newMetadataFile.push(json);
#             console.log(newMetadataFile.length)
#             })    
#         }          
#     })