Authors:
**Kevin de Youngster**, **Kofi Anamoa Mensah**, **David Edem Duamekpor**, **Kwamina Amoako**

# Install Instructions

1. To install dependencies, run:

```
pip install -r requirements.txt
```

2. To test run:

```
python six-paths.py
```

# External Tools Used

-   Python 3.7
-   @alieldinayman's [HSV Color Picker Tool](https://github.com/alieldinayman/HSV-Color-Picker) to extract the necessary color ranges of objects

# Project Info

## What Worked?

-   Processing image from drone camera into 2D grid map
-   Sending map to EV3

## What did not Work?

-   Making drone fly while taking images
    Blob detection does not get the target objects

### Links to Tutorial and Articles Used

-   [Connecting edges from canny edge with dilation](https://stackoverflow.com/questions/43009923/how-to-complete-close-a-contour-in-python-opencv)
-   [Detect Colors](http://answers.opewhancv.org/question/90047/detecting-blue-color-in-this-image/)
-   [Color Filter](https://pythonprogramming.net/color-filter-python-opencv-tutorial/)
-   [OpenCV uses different system for representing HSV](https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv)
-   [Color Filtering](https://stackoverflow.com/questions/47483951/how-to-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-image)
-   [Noise Removal](https://www.geeksforgeeks.org/erosion-dilation-images-using-opencv-python)
-   [Drawing Lines in OpenCV](https://stackoverflow.com/questions/44816682/drawing-grid-lines-across-the-image-uisng-openccv-python?rq=1)
-   [Check if point in in something](https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=pointpolygontest#pointpolygontest)
-   [Center of Contour](https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/)
