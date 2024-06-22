# Water Area Measurement for Wicking Video

Main.py calculate the area of water in each frame of the wicking video, an excel file storing the area data and a output video with drawn contour of water is saved in ./output.

### Output Video Demo

<p align="center"> 
    <img src="./info/demo.gif" alt="400" width="400">
</p>

### How it works?

1. Change all the frames to grayscale.
2. Compute the absolute difference of the first frame and each frame after the first frame.
3. Binary frame are produced from the result of 2. by applying threshold of 10 (default).
4. Draw the largest external contour.

### Requirements

- opencv-python
- numpy
- pandas

### Reference
- ChatGPT
