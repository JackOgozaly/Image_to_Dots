# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 15:54:44 2022

@author: jogoz
"""

#Packages used
from PIL import Image             
import numpy as np                
import matplotlib.pyplot as plt   
import requests
from io import BytesIO
import pandas as pd 
import requests
import skimage



import cv2
from skimage.transform import resize

import skimage.transform as st

from numpy.linalg import norm
from scipy.spatial import distance
import math


#image: image object that you want to convert
#max_length: sets a cap on how many rows the X,Y coordinates can take up
#pixel_cutoff: sets the threshold for the pixel briteness
#greater_than: If true selects pixels greater than pixel_cutoff value

def image_to_dots(image, max_length= 10000, pixel_cutoff=.4, greater_than=False): 
    euclid_distance = np.sqrt(2)
    euclid_distance_margin = math.ceil(euclid_distance + 1)
    #Convert to black and white 
    I1 = image.convert('L')

    #Convert to array
    img_array = np.asarray(I1)
    
    #Convert pixels to 0-1 range
    img_array = img_array/255
    #Downsample more and more until desired row count is achieved
    for j in range(1,20):
        r = skimage.measure.block_reduce(img_array[:, :],
                                 (j, j),
                                 np.mean)

        r = np.rot90(r, 3)
        
        if np.mean(r) < pixel_cutoff: 
            pixel_cutoff = np.mean(r)
        
        #Create empty DF
        image_df = pd.DataFrame()
        if greater_than is True: 
            #Create a df and get indices for pixels greater than pixel_cutoff
            image_df['X'],image_df['Y']  = np.where(r > pixel_cutoff)
        else: 
            #Create a df and get indices for pixels less than pixel_cutoff
            image_df['X'],image_df['Y']  = np.where(r < pixel_cutoff)
        
        #Break loop if finally under max_length threshold
        if image_df.shape[0] <= max_length:
            print(np.mean(r))
            for a in range(len(image_df)):
                if a >= image_df.shape[0]:
                    continue
                x = image_df.iloc[a,0]
                y = image_df.iloc[a,1]
                x_min = x - euclid_distance_margin
                x_max = x + euclid_distance_margin
                y_min = y - euclid_distance_margin
                y_max = y + euclid_distance_margin
                #euclid_calc_df = test[test['X'] >= x_min and test['X'] <= x_max]
                euclid_calc_df = image_df[image_df['X'].between(x_min, x_max)]
                euclid_calc_df = euclid_calc_df[euclid_calc_df['Y'].between(y_min, y_max)]
                euclid_calc_df['euclid_dist'] = (np.sqrt(((euclid_calc_df['X'] - x)**2).astype(float) + ((euclid_calc_df['Y'] - y)**2).astype(float)))
                euclid_calc_df = euclid_calc_df['euclid_dist'].between(0.01, euclid_distance, inclusive = True)
                exclude_list = euclid_calc_df[euclid_calc_df == True].index.tolist()
                image_df = image_df.drop(image_df.index[exclude_list])
                image_df = image_df.reset_index(drop=True)
                
            
            return(image_df)
            break
        
MOMA_data = pd.read_csv(r'C:\Users\jogoz\OneDrive\Desktop\Iron Viz 2022\Moma_Data\MOMA_on_view.csv')
hyperlinks = MOMA_data['Image_Hyperlink'][MOMA_data['Image_Hyperlink'].notnull()]
hyperlinks = hyperlinks.reset_index(drop=True)
hyperlinks = list(hyperlinks[19:21])



#Pixel values are between 0 and 1. 0 being black, 1 being white. 


combined_pics = []
for i in range(len(hyperlinks)):
        #Get image from hyperlink
        response = requests.get(hyperlinks[i])
        I = Image.open(BytesIO(response.content))
        test_df = image_to_dots(I, max_length=30000, greater_than=False, pixel_cutoff=.65)
        test_df['URL'] = hyperlinks[i]
        combined_pics.append(test_df)

        

combined_pics = pd.concat(combined_pics)


for i in range(len(hyperlinks)): 
    response = requests.get(hyperlinks[i])
    I = Image.open(BytesIO(response.content))
    plt.imshow(np.asarray(I))
    plt.show()
    plot_data = combined_pics[combined_pics['URL'] == hyperlinks[i]]
    plt.plot(plot_data['X'], plot_data['Y'], 'o', color='black',  markersize=2)
    plt.show()

