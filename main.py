import cv2
import argparse
import matplotlib.pyplot as plt
import numpy as np

# all function for detecting line segment and angle
from angleDetector import angleDetector

def main(img_path ):
    try: 
        img = cv2.imread(img_path, 0 )
        h,w = img.shape # needed to put text on image
    except Exception as e:
        print(f"Exception {e} raised, please check if you have given a valid image path: {img_path}")

    var = angleDetector(img)
    
    #find clusters
    var.find_coord()
    clusters = var.find_clusters()
    
    # group all clusters
    group = var.group_coords()

    # detect line in all the cluster
    var.line_detector()

    # find the line segment in cluster
    line_key = var.only_keep_line()

    # only for sanity check, draw back the line segment on image from slope and x corrdinates 
    sample_im = var.draw_coords_on_black_im(var.line_arr[line_key])
    
    # angle of line segment
    angle = round(var.find_angle_wrt_x_axis(line_key),2 )
    print(f"angle of line segment: {angle} degree")

    print("plotting line segment")
    while True:

        cv2.imshow( "original image", img)
        # line segmet drawn
        
        cv2.putText(sample_im,f"angle: {angle} degrees ", (10,h-10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1,2)

        cv2.imshow( "lines_segment drawn from slope", sample_im)
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break

        img_with_line = np.concatenate((img, np.ones([h,2])*255), axis=1)
        cv2.putText(img_with_line,f"original img ", (10,h-10), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1,2)

        out_im = np.concatenate((img_with_line, sample_im), axis=1)
        cv2.imwrite("out.jpg", out_im)

    return angle



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Find angle of a line segment in a image w.r.t x axis')
    parser.add_argument('--img_path', dest="img_path", type=str, help='image path with a line segment in it.')
    args = parser.parse_args()

    print(f"image_path: {args.img_path}")
    angle = main(args.img_path)
