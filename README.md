# line_segment_angle_detector
the code detects angle for a line segment w.r.t x axis.

## setup
tested on python3.7 environment

```
pip install -r requirements.txt
```
## code execution
sample code 
```
python main.py --img_path ./test_images/image5.jpg
```
## output
![sample_img](https://github.com/humandotlearning/line_segment_angle_detector/blob/main/imgs/sample_output.png)

### time taken for output
average time taken to find angle of one image is: 1.5 seconds

## process followed to get line segment:
1. read image as grayscale 
    * for faster processing, as keeping all the channels didn't add to the accuracy of the solution.
2. find all points greater than 0.
    * to reduce processing overhead by only considering valid points.
3. apply Single Linkage based hierarchical-clustering
    * doesn't require to provide number of cluster beforehand.
    * Single Linkage — The distances between the most similar members are calculated for each pair of clusters, and the clusters are then merged based on the shortest distance. ( simple yet effective method for this problem statement)
4. sort all points into seperate groups based on class assigned by clustering algorithm (hierarchical-clustering)
5. assume all groups are line and find respective line equation for them.
    * find slope (m) and constant (b) for each cluster with an assumption that it could be a line.
6. find all y coordinates for each cluster based on the above calulated slope and constant.
    * fit all cluster to equation
    * > Y = m * X + b
7. find distance between line from line equation and actual coordinates.
8. the group with the smallest distance should be the line.
9. find angle from slope using tan inverse.


references:
1. https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.single.html#scipy.cluster.hierarchy.single
2. https://www.analyticsvidhya.com/blog/2021/08/hierarchical-clustering-algorithm-python/ 
3. https://stackoverflow.com/questions/67387303/line-equation-of-every-two-consecutive-points-in-a-numpy-array

