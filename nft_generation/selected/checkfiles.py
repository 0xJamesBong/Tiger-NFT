from os import listdir
from os.path import isfile, join

image_dir = "./selected_images"
json_dir = "./selected_json"

images  = [f[0:-3] for f in listdir(image_dir) if isfile(join(image_dir, f))]
jsons   = [j[0:-4] for j in listdir(json_dir) if isfile(join(json_dir, j))]

shared = set(images).intersection(set(jsons))

image_extras = [f not in shared for f in images]
json_extras  = [j not in shared for j in jsons]





print(set(images).difference(shared))
print(set(jsons).difference(shared))
print(len(images), len(jsons), len(shared), len(image_extras), len(json_extras))


