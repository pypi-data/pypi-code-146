import numpy as np


def create_camera_matrix(fx,fy,u,v):
    return np.array([[fx,0,u],[0,fy,v], [0,0,1]])

def resize_camera_matrix(current_img_size, new_img_size, current_K):
    ratio = new_img_size*1.0/current_img_size
    new_K = current_K*ratio
    new_K[2,2] = 1.0
    return new_K




if __name__ == '__main__':
    pass
    K = create_camera_matrix(640,640,300,300)
    new_K = resize_camera_matrix(1000, 250, K)
    print(K)
    print(new_K)

