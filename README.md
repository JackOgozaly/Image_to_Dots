# Image to Dots

This is a repository that contains my work converting an image into 

# Example: 

### Boring, Old, Tired, Uninspiring Starry Night

<img src="https://github.com/JackOgozaly/Image_to_Dots/blob/main/Examples/starry_night.jpg" width="400" height="250">

### Interesting, New, Fresh, Inspiring Graphical Starry Night

<img src="https://github.com/JackOgozaly/Image_to_Dots/blob/main/Examples/starry_night_graph.png" width="400" height="250">


# What's different

I couldn't find any tool that did this in a satisfactory way. Plus, other methods online would result in long run times. This function allows you to customize how much you're downsampling the image, set a row cap, and what pixel brightness/dimness you want to select for. 


# How it Works

An image is provided, it is converted to black and white, and then the iamge is downsampled, the pixels are chosen based on the criteria provided, and this process is repeated until the row count of X, Y coordinates is beneath the cap set. 
