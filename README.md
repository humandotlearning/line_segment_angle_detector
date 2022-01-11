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


## process followed to get line segment:
1. read image in grayscale
2. find all points greater than 0
3. apply distance based hierarchical-clustering
4. sort all points into seperate groups based on clustering
5. assume all groups are line and find respective line equation for them.
6. find distance between line from line equuation and actual group.
7. the group with the smallest distance should be the line
8. find angle from slope using tan inverse.


references:
1. https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.single.html#scipy.cluster.hierarchy.single
2. https://www.analyticsvidhya.com/blog/2021/08/hierarchical-clustering-algorithm-python/ 
3. https://stackoverflow.com/questions/67387303/line-equation-of-every-two-consecutive-points-in-a-numpy-array

