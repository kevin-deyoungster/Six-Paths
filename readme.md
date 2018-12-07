What Worked?

What Didn't Work?

Blob detection does not get the target objects

# Detect Colors

http://answers.opewhancv.org/question/90047/detecting-blue-color-in-this-image/

https://pythonprogramming.net/color-filter-python-opencv-tutorial/

OpenCV uses different system for representing HSV
https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv

https://solarianprogrammer.com/2015/05/08/detect-red-circles-image-using-opencv/

Nice code: Colored Ball Detections
https://pastebin.com/WVhfmphS

Good HSV Color Picker
https://alloyui.com/examples/color-picker/hsv

HSV Color Map
https://stackoverflow.com/questions/47483951/how-to-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-image

http://colorizer.org/

Noise Removal
https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python/

````python
        kernel = np.ones((5, 5), np.uint8)

 img_erosion = cv2.erode(warped, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)

        cv2.imshow("Scanned", warped)
        cv2.imshow("Erosion", img_erosion)
        cv2.imshow("Dilation", img_dilation)
        ```

```python

# from pathlib import Path
# pathlist = Path("images").glob('**/*.JPG')
# for path in pathlist:
#         getGrid(str(path))
````

````python
from pathlib import Path
pathlist = Path("images").glob('**/*.JPG')
for path in pathlist:
    detect_color(str(path), BLUE_LOWER,BLUE_UPPER)
    detect_color(str(path), RED_LOWER,RED_UPPER)
    ```


Optimal Canny Edge Detection
https://stackoverflow.com/questions/18194870/canny-edge-image-noise-removal
```

```
 # # Draw edges of the image
        # edged = get_edges(image, True)
        # cnts, found = get_contours(edged)
        # cv2.drawContours(image, cnts, 4, (0, 255, 0), 2)
        # cv2.imshow("Edges", edged)```
````

HSV Color Picker for OpenCV
https://github.com/alieldinayman/HSV-Color-Picker

Drawing Lines in OpenCV
https://stackoverflow.com/questions/44816682/drawing-grid-lines-across-the-image-uisng-openccv-python?rq=1

Check if point in in something
https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=pointpolygontest#pointpolygontest

https://stackoverflow.com/questions/50670326/how-to-check-if-point-is-placed-inside-contour

```
https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
```

```Detect Red Cirlces in an Image
https://solarianprogrammer.com/2015/05/08/detect-red-circles-image-using-opencv/
```
