//requiring path and fs modules
const path = require('path');
const fs = require('fs');
//joining path of directory 

const selectedImagesPath = "./selected_images";
const outputJsonPath = "./selected_json";
const oldJsonPath = "../build/json";
const generatedJsonData = require('../build/json/_metadata.json'); 
const selected_json = "./selected_json";

// console.log(generatedJsonData[1]);


// readFilesSync reads files from a dir, and makes a list of all the filenames in the dir
function readFilesSync(dir) {
    let files = [];
    let fileNames = [];
    fs.readdirSync(dir).forEach(filename => {
      const name = path.parse(filename).name;
      const ext = path.parse(filename).ext;
      const filepath = path.resolve(dir, filename);
      const stat = fs.statSync(filepath);
      const isFile = stat.isFile();
  
      if (isFile) files.push({ filepath, name, ext, stat });
      if (isFile) fileNames.push(path.basename(filename));
    });
  
    files.sort((a, b) => {
      // natural sort alphanumeric strings
      // https://stackoverflow.com/a/38641281
      return a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' });
    });
  
    return fileNames 
}


// function copyMetaData(selectedImagesPath, modifiedJsonMetadataFilePath, fileName) {
    
//     const fileNamePath = path.join(selectedImagesPath,fileName);
//     const jsonFilePath = path.join(modifiedJsonMetadataFilePath,fileName);
//     // console.log(fileNamePath);
//     fs.copyFile(fileNamePath,jsonFilePath, (err) => {
//         if (err) throw err;
//         console.log(`${fileName} was copied to destination`);
//       });          
// }

// console.log(generatedJsonData.length)
// generatedJsonData.forEach(object => {
//     console.log(object.dna)
// })


async function moveMetadata(selectedImagesPath, outputJsonPath, oldJsonPath) {
  // This reads all the files in the dir where all the images I've selected
  // and poduces a list of their names
    const selectedImagesFileNames = readFilesSync(selectedImagesPath);
    const oldJsonFileNames        = readFilesSync(oldJsonPath);
    
    let newMetadataFile = [];

    // s.push('2')
    // console.log(s)
    oldJsonFileNames.forEach(fileName => {
        
        const dna = fileName.substring(0,fileName.length-5);
        
        if (selectedImagesFileNames.includes(dna+".png")) {
            fs.copyFile(path.join(oldJsonPath,fileName), path.join(outputJsonPath,fileName), (err) => {
                if (err) throw err;
                console.log(`${fileName} was moved!~`);
            });
            const data = fs.readFile(path.join(outputJsonPath,fileName), 'utf8' , (err, data) => {
                if (err) {
                  console.error(err)
                  return
                }
            const json = JSON.parse(data);
            console.log(json);
            newMetadataFile.push(json);
            console.log(newMetadataFile.length)
            })    
        }          
    })
    // console.log(newMetadataFile.length)
    
    // var jsonObj = JSON.parse(newMetadataFile);
    // var jsonContent = JSON.stringify(jsonObj);
    // fs.writeFile("./output.json", jsonContent, 'utf8', function (err) {
    //     if (err) {
    //         console.log("An error occured while writing JSON Object to File.");
    //         return console.log(err);
    //     }
    // })

    // fs.appendFileSync('metadata.json', newMetadataFile);
}


function readMetadatas(selected_json) {
  let metadatas = []
  
  
  fs.readdirSync(selected_json).forEach(filename => {
    console.log(filename)
    let rawdata= fs.readFileSync(selected_json+"/"+filename)
    // console.log(rawdata)
    let metadata = JSON.parse(rawdata);
    // console.log(metadata)
    metadatas.push(metadata)
    console.log(metadatas.length)
    
    // console.log(String("selected_json"+rawdata))
    // let metadata = JSON.parse(file);
    // console.log(metadata);
  });
  // console.log(metadatas)
  // return metadatas
  
  var jsonContent = JSON.stringify(metadatas, null, 4);
  // 
  // console.log(jsonContent)
  fs.writeFile("./aggregate_metadata.json", jsonContent, 'utf8', function (err) {
    if (err) {
        console.log("An error occured while writing JSON Object to File.");
        return console.log(err);
    }
  })
}

// async function makeAggregateMetadataFile(metadataFilesPath) {
//   let files = readFilesSync(metadataFilesPath)
//   let metadatas = [];
//   fs.readFileSync('')  

//     var jsonObj = JSON.parse(newMetadataFile);
//     var jsonContent = JSON.stringify(jsonObj);
//     fs.writeFile("./output.json", jsonContent, 'utf8', function (err) {
//         if (err) {
//             console.log("An error occured while writing JSON Object to File.");
//             return console.log(err);
//         }
//     })
// // 
//     fs.appendFileSync('metadata.json', newMetadataFile);
// }

async function moveAndMakeAggregateMetadata() {
  moveMetadata(selectedImagesPath, outputJsonPath, oldJsonPath).then(
    readMetadatas(selected_json)
  )
}

moveAndMakeAggregateMetadata()
// readMetadatas(selected_json)

// moveMetadata(selectedImagesPath, outputJsonPath, oldJsonPath) 
