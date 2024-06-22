import os
import cv2
import numpy as np
import pandas as pd

# Open the video file
video_path = 'data/sample_wicking_video.avi'
video = cv2.VideoCapture(video_path)

# change accordingly
length_per_pixel = 1/38.6614
area_per_pixel = length_per_pixel*length_per_pixel

# Read the first frame
ret, first_frame = video.read()
if not ret:
    print("Failed to read video")
    video.release()
    exit()

# Convert the first frame to grayscale
first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

# DataFrame to store frame numbers and areas
df = pd.DataFrame(columns=['Frame Number', 'Area (mm^2)'])

output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)
output_xlsx = os.path.join(output_dir, 'areas.xlsx')
output_mp4 = os.path.join(output_dir, 'video.mp4')

# store processed frames
height, width = first_frame.shape
videow = cv2.VideoWriter(output_mp4, cv2.VideoWriter_fourcc(*'MP4V'), 30, (width, height))

frame_number = 1

while True:
    ret, frame = video.read()
    if not ret:
        break
    
    frame_number += 1

    # Convert current frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the absolute difference between the current frame and the first frame frame
    diff = cv2.absdiff(gray, first_frame)

    # Apply a binary threshold to create a binary image
    _, binary = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to track the largest contour
    largest_contour = None
    largest_area = 0

    # Iterate through contours to find the largest one
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            largest_area = area
            largest_contour = contour

    cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)  # Draw contour in green
    area_in_mm2 = largest_area * area_per_pixel
    area_in_mm2 = round(area_in_mm2, 6)  # Round to 6 decimal places
    print(f'Frame {frame_number}: {area_in_mm2} mm^2')

    # shows information on frame
    cv2.rectangle(frame, (width-510, 70), (width-80, 170), (255, 255, 255), -1)
    cv2.putText(frame, f'Frame {frame_number}', (width-500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, f'Area: {area_in_mm2} mm^2', (width-500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Append to DataFrame
    df = pd.concat([df, pd.DataFrame({'Frame Number': [frame_number], 'Area (mm^2)': [area_in_mm2]})], ignore_index=True)

    # Write frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    videow.write(frame)

    # display frame
    frame = cv2.resize(frame, (int(width*0.6), int(height*0.6)))
    cv2.imshow('Frame', frame)

    # stop program by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
videow.release()
cv2.destroyAllWindows()

# Save DataFrame to an Excel file
df.to_excel(output_xlsx, index=False)
print(f'Data saved to {output_xlsx}')
print(f'Video saved to {output_mp4}')
