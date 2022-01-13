import cv2
import matplotlib.pyplot as plt
import math
import numpy as np

# required for Hierarchical Clustering 
from scipy.cluster.hierarchy import single, fcluster
from scipy.spatial.distance import pdist

from collections import defaultdict

# to find angle from slope
from math import atan, degrees


class angleDetector():
  def __init__(self, img):
    self.im = img
    self.coords = 0
    self.cluster_dict = defaultdict(lambda: []) 

  def _sample_black_im(self):
    return np.zeros_like(self.im)    

  def find_coord(self):
    """
        groups all points in the image
    """
    np_arr = np.array(self.im) 
    self.coords = np.column_stack(np.where(np_arr > 0))
    return self.coords
  
  def draw_coords_on_black_im(self, coords):
    """
      draws an array of points on a plain black image. (useful for testing)
    """
    sample_im = self._sample_black_im()
    for coord in coords:
      sample_im = cv2.circle(sample_im, (int(coord[1]),int(coord[0])), radius=0, color=(255, 255, 255), thickness=-1)
    self.plot_im(sample_im)
    return sample_im

  def plot_im(self, im):
    plt.imshow(im, cmap="gray")
 
  def find_clusters(self):
    """
      finds clusters in a set of points. hierarchical clustering used.

      references: 
      1. https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.single.html#scipy.cluster.hierarchy.single
      2. https://www.analyticsvidhya.com/blog/2021/08/hierarchical-clustering-algorithm-python/ 
    """
    
    # generate the linkage matrix
    X = self.coords
    y = pdist(X)
    Z = single(y)
    self.clusters = fcluster(Z, 1, criterion='distance')
    self.clusters = np.expand_dims(self.clusters, axis=1)    
    # remove empty arrays
    self.clusters[self.clusters.astype(bool)]
    print(f" clusters.shape: {self.clusters.shape}")
    return self.clusters

  def group_coords(self):
    """
    group all points into their respective clusters.

    """
    # stack clusters and coordinates
    # group = np.hstack((self.clusters,self.coords))
    group = zip(self.clusters,self.coords)
    cluster_dict = defaultdict(lambda: []) 
    for k, v in group:
      cluster_dict[k[0]].append(v)
    
    # converting all dictionary to np arrays
    for k in cluster_dict:
      cluster_dict[k] = np.array(cluster_dict[k])
    
    # cleaning of cluster
    # number of points that should be present to consider it a valid cluster    
    tmp_dict = cluster_dict.copy()
    thresh = 100
    for k in tmp_dict:
      if len(cluster_dict[k]) < thresh: 
        del cluster_dict[k]

    self.cluster_dict = cluster_dict
    # print(f"cluster_dict: {cluster_dict}")

    return self.cluster_dict
    
  def arr_line_equation(self, arr):
    """
     finds the line equation of a numpy array

     references: 
     1. https://stackoverflow.com/questions/67387303/line-equation-of-every-two-consecutive-points-in-a-numpy-array
    """
    # x = arr[:,1]
    # y = arr[:,0]

    # dx = np.diff(x)  # Change in x
    # dy = np.diff(y)  # Change in y

    # (y1,x1),(y2,x2) = self.find_min_max_coord(arr)
    # # Amended for @Nan's
    # # If any dx is zero this will now return +-inf in m and c without raising a warning
    # # The code using m and c will need to handle this if it can occur.
    # with np.errstate( divide = 'ignore' ):
    #     m = dy/dx  # Gradient
    # c = y[1:] - m * x[1:]   # Constant

    (y1,x1),(y2,x2) = self.find_min_max_wrt_x_coord(arr)
    m = (y2 - y1)/(x2 - x1)
    c = y2 - m * x2

    # print(f" m:{m},c:{c}")
    return (m,c)

  def line_detector(self):
    """
      find the line cluster and its equation from all the clusters in the image 
    """
    group = self.group_coords()
    cluster_slope_dict = defaultdict(lambda: [])
    print("\n assuming all clusters are line and finding line equation for all:")
    for k in group:
      m, b = self.arr_line_equation(group[k])           # slope of each cluster
      cluster_slope_dict[k] = (m, b)

      print(f"key: {k}, m: {m}, b: {b}")

    print("\n")
    self.cluster_slope_dict = cluster_slope_dict
    
    # print(cluster_slope_dict)
    return cluster_slope_dict

  def find_min_max_coord(self, cluster):
    """
      find min max coordinates
    """
    y1, x1 = np.min(cluster, axis=0)
    y2, x2 = np.max(cluster, axis=0)
    return ((y1,x1),(y2,x2))


  def find_min_max_wrt_x_coord(self, cluster):
    """
      find min max w.r.t x coordinates
    """
    
    y1, x1 = cluster[np.argmin(cluster[:,1], axis=0)]
    y2, x2 = cluster[np.argmax(cluster[:,1], axis=0)]
    return ((y1,x1),(y2,x2))

  def find_distance(self,a, b):
    """Return distance between line a and b"""
    dist = np.linalg.norm(a-b)
    return dist

  def only_keep_line(self):
    """
      only keep line segment and removes all other cluster
    """
    group = self.group_coords()
    self.group = group
    self.line_arr = defaultdict(lambda: 0)
    line_dist = defaultdict(lambda: 0)
    for k in group:
      m,b = self.cluster_slope_dict[k]

      # assuming all cluster fit the line equation
      xarr = group[k][:,1]
      yarr = m * xarr + b
      arr = np.concatenate([yarr[:,None],xarr[:,None]], axis=1)
      self.line_arr[k] = arr 


      line_dist[k] = self.find_distance(group[k], arr)
      print(f"key: {k}, line distance from actual points: {line_dist[k]}")

    # find cluster with smallest distance ( that should be the line segment)
    temp = min(line_dist.values())
    is_line = [key for key in line_dist if line_dist[key] == temp][0]  
    self.is_line = is_line
    print(f"\nkey of line segment: {is_line}")
    
    return self.is_line
    # angle = self.find_angle_wrt_x_axis(is_line)
    # print(f"\n is_line: {is_line}, angle: {angle}\n\n")

  def find_angle_wrt_x_axis(self,k):
    """
      find angle of a cluster assuming it is a line
    """      
    # subtracted by 180 because the angle is given wrt to top line (x axis)
    m,c = self.cluster_slope_dict[k]
    if m > 0:
      angle = 180 - degrees(atan(m))
    else: 
      angle = abs(degrees(atan(m)))
    return angle


    

