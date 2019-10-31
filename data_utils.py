import numpy as np
import json
from PIL import Image

def crop_frame(image, cropx=None, cropy=None):
    if image.shape[0] == 720 and image.shape[1] == 1280:
        image = image[100:600, ...]
    return image

def load_json(metadata_path, csv_path):
    with open(metadata_path, 'r') as jsonfile:
        metadata_all = json.load(jsonfile)
    metadata = dict{}
    with open(csv_path, 'r') as csvfile: 
        yt_data = csv.reader(csvfile)
        line_count = 0
        for row in yt_data:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
                continue
            else:
                line_count += 1
                key = int(float(row[1]))
                yt_filename = row[4]
                metadata['%s'%key] = metadata_all['%s'%key]
                metadata['%s'%key].update('yt_filename': yt_filename)
    return metadata
  
