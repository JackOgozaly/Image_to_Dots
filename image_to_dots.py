# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 21:32:44 2022

@author: jogoz
"""

#Packages used
from PIL import Image             
import numpy as np                
import matplotlib.pyplot as plt   
import requests
from io import BytesIO
import pandas as pd 
import skimage


#image: image object that you want to convert
#max_length: sets a cap on how many rows the X,Y coordinates can take up
#pixel_cutoff: sets the threshold for the pixel briteness
#greater_than: If true selects pixels greater than pixel_cutoff value

def image_to_dots(image, max_length= 50000, pixel_cutoff=.4, greater_than=True): 
    #Convert to black and white
    I1 = image.convert('L')
    #Convert to array
    img_array = np.asarray(I1)
    #Convert pixels to 0-1 range
    img_array = img_array/255
    #Downsample more and more until desired row count is achieved
    for j in range(1,21):
        r = skimage.measure.block_reduce(img_array[:, :],
                                 (j, j),
                                 np.mean)
        #Rotate our array
        r = np.rot90(r, 3)
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
            return(image_df)
            break
        
        
        
#Example Image
#For this we have to use the io and requests package to convert image link to image
response = requests.get('https://www.moma.org/media/W1siZiIsIjQ2NzUxNyJdLFsicCIsImNvbnZlcnQiLCItcXVhbGl0eSA5MCAtcmVzaXplIDIwMDB4MTQ0MFx1MDAzZSJdXQ.jpg?sha=62618546638d742f')
example_image = Image.open(BytesIO(response.content))

#Calling our function
example_df = image_to_dots(example_image)

#Plottig the results
plt.plot(example_df['X'], example_df['Y'], 'o', color='black',  markersize=1)

