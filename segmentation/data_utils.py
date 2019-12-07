import numpy as np
import json, csv
from PIL import Image
import cv2
import matplotlib.pyplot as plt


def crop_blacks(image):
    image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Crop black borders
    sums = np.sum(image_bw, axis=(1))
    where = np.where(np.sum(image_bw, axis=(1)) > 5000)
    image = image[where[0]]
    return image

# get rid of the black boundaries if it's a 16:9 movie trailer
def crop_frame(image, cropx=None, cropy=None):
    if image.shape[0] == 720 and image.shape[1] == 1280:
        image = image[100:600, ...]
    return image

# csv_path: cinematic-color/data/trailers.csv
# metadata_path: cinematic-color/data/movie_details.json
def load_json(metadata_path, csv_path):
    with open(metadata_path, 'r') as jsonfile:
        metadata_all = json.load(jsonfile)
    metadata = dict()
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
                try:
                    metadata['%s'%key] = metadata_all['%s'%key]
                except Exception as e:
                    print('cannot get key %s'%e)
                    continue
                metadata['%s'%key].update({'yt_filename': yt_filename})
    return metadata
  
# metadata_path = 'movie_details.json'
# csv_path = 'trailers.csv'
# meta = load_json(metadata_path, csv_path)
# # print(meta)

def resize_pil(image, ratio):
    image = Image.fromarray(image)
    image = image.resize((int(image.width*ratio),
                             int(image.height*ratio)),
                             Image.ANTIALIAS)
    return np.array(image)

def get_3d_dist(color_dist, ax):
    r, g, b = cv2.split(np.asarray(color_dist))
    pixel_colors = color_dist.reshape(
    (np.shape(color_dist)[0]*np.shape(color_dist)[1], 3)) / 255
    pixel_colors = pixel_colors.tolist()
    ax.scatter(r.flatten(),
               g.flatten(),
               b.flatten(),
               facecolors=pixel_colors, marker=".")
    ax.set_xlabel("Red")
    ax.set_ylabel("Green")
    ax.set_zlabel("Blue")
    return ax

# Histogram matching

def find_nearest_above(my_array, target):
    diff = my_array - target
    mask = np.ma.less_equal(diff, -1)
    # We need to mask the negative differences
    # since we are looking for values above
    if np.all(mask):
        c = np.abs(diff).argmin()
        return c # returns min index of the nearest if target is greater than any value
    masked_diff = np.ma.masked_array(diff, mask)
    return masked_diff.argmin()

def hist_match(source, target, plot=True):
    source_shape = source.shape
    source = source.ravel()
    target = target.ravel()
    s_values, bin_idx, s_counts = np.unique(source, return_inverse=True, return_counts=True)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_dist = s_quantiles / s_quantiles[-1]
    
    t_values, t_counts = np.unique(target, return_counts=True)
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_dist = t_quantiles / t_quantiles[-1]

    sour = np.around(s_quantiles)
    temp = np.around(t_quantiles)
    
    b = np.interp(s_quantiles, t_quantiles, t_values)
    
    interp_t_values, interp_t_bin, interp_t_counts = np.unique(b[bin_idx], return_inverse=True,return_counts=True)
    interp_t_quantiles = np.cumsum(interp_t_counts).astype(np.float64)
    interp_t_dist = interp_t_quantiles / interp_t_quantiles[-1]
    if plot:
        plt.figure(figsize=(12,4))
        ax = plt.subplot(1,3,1)
        ax.hist(s_dist)
        ax = plt.subplot(1,3,2)
        ax.hist(t_dist)
        ax = plt.subplot(1,3,3)
        ax.hist(interp_t_dist)
        plt.show()

    return b[bin_idx]