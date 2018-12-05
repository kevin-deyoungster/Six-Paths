Blob detection does not get the target objects

# Detect Colors 
http://answers.opencv.org/question/90047/detecting-blue-color-in-this-image/
https://pythonprogramming.net/color-filter-python-opencv-tutorial/


OpenCV uses different system for representing HSV
https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv


https://solarianprogrammer.com/2015/05/08/detect-red-circles-image-using-opencv/


Nice code: Colored Ball Detections
https://pastebin.com/WVhfmphS

Good HSV Color Picker 
https://alloyui.com/examples/color-picker/hsv

http://colorizer.org/


Noise Removal
https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/

```python
        kernel = np.ones((5, 5), np.uint8)

 img_erosion = cv2.erode(warped, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)

        cv2.imshow("Scanned", warped)
        cv2.imshow("Erosion", img_erosion)
        cv2.imshow("Dilation", img_dilation)
        ```