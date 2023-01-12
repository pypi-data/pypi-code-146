from cv2 import aruco
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np

#A4_Y = 210
#A4_X = 297
A4_Y = 195.0 # printable area
A4_X = 276.0 # printable area

#A4_X = 420.0
#A4_Y = 297.0

A4_XY_RATIO = A4_X/A4_Y

def create_board(squares_x, squares_y, cb_sq_width, aruco_sq_width, aruco_dict_str, start_id):
    aruco_dict = aruco.Dictionary_get(getattr(aruco, aruco_dict_str))
    aruco_dict.bytesList=aruco_dict.bytesList[start_id:,:,:]
    board = aruco.CharucoBoard_create(squares_x,squares_y,cb_sq_width,aruco_sq_width,aruco_dict)
    return board


def create_printable_aruco_grid(aruco_dict_str, px_width, squares_x,squares_y, spacing_ratio, start_id, padding):
    #aruco_dict.bytesList=aruco_dict.bytesList[start_id:,:,:]
    squares_xy_ratio = squares_x/squares_y
    px_per_mm = px_width/A4_X
    print("px per mm", px_per_mm)
    #board = aruco.CharucoBoard_create(squares_x,squares_y,1,spacing_ratio,aruco_dict)
    board = create_board(squares_x, squares_y, 1, spacing_ratio, aruco_dict_str, start_id)
    px_height = np.round(px_width/A4_XY_RATIO, 0)



    if squares_xy_ratio > A4_XY_RATIO:
        norm_width = (squares_x*spacing_ratio+squares_x)
        #padding = px_width*1.0/norm_width*spacing_ratio/2
        img = board.draw((px_width,int(px_height)), marginSize=int(padding))
        ch_board_sq_size = ((px_width-2*padding)/squares_x)/px_per_mm
        aruko_size = spacing_ratio*ch_board_sq_size
        print("ch_board_size", ch_board_sq_size)
        print("aruko_size", aruko_size)

    else:
        norm_height = ((squares_y+1)*spacing_ratio+squares_y)
        #padding = px_height*1.0/norm_height*spacing_ratio
        img = board.draw((px_width,int(px_height)), marginSize=int(padding))
        ch_board_sq_size = ((px_height-2*padding)/squares_y)/px_per_mm
        aruko_size = spacing_ratio*ch_board_sq_size
        print("ch_board_size", ch_board_sq_size)
        print("aruko_size", aruko_size)


    label = "APRILTAG_16H5" + f' SZ_CH_SQ:{np.round(ch_board_sq_size, 3)}mm'
    label += f' AR_SZ:{np.round(aruko_size, 3)}mm' + f' start id: {str(start_id)}'
    imboard = cv2.putText(img, label, (100,100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=5, color=(0,0,0), thickness=5)
    img = img.T
    img = cv2.flip(img,1)
    return img

def detect_charuco():
    # open webcam
    cap = cv2.VideoCapture(0)
    # set zero focus
    # create camera matrix

    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    sq_x = 7
    sq_y = 6
    aruco_dict_str = "DICT_APRILTAG_16H5"
    start_id = 0
    spacing_ratio = 0.65
    board = create_board(sq_x, sq_y, 14.099, 9.164, aruco_dict_str, start_id)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, board.dictionary)
        if ids is not None:
            print(ids)
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if charuco_corners is not None:
                print(charuco_ids)
                aruco.drawDetectedCornersCharuco(frame, charuco_corners, charuco_ids, (0,255,0))
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def capture_and_calibrate():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    images = []
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',gray)
        c = cv2.waitKey(1)
        if c == ord('q'):
            cap.release()
            break
        if c == ord('s'):
            print("saving")
            images.append(gray)
    
    sq_x = 7
    sq_y = 6
    aruco_dict_str = "DICT_APRILTAG_16H5"
    start_id = 0
    spacing_ratio = 0.65
    board = create_board(sq_x, sq_y, 14.099, 9.164, aruco_dict_str, start_id)
    # calibrate using images
    print("calibrating")
    cal = aruco.CharucoBoard_create(sq_x, sq_y, 14.099, 9.164, aruco.Dictionary_get(aruco.DICT_APRILTAG_16H5))
    allCorners = []
    allIds = []
    decimator = 0
    for im in images:
        corners, ids, rejectedImgPoints = aruco.detectMarkers(im, board.dictionary)
        if ids is not None:
            print(len(ids))
        if ids is not None and len(ids) > 10:
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, im, board)
            aruco.drawDetectedCornersCharuco(im, charuco_corners, charuco_ids, (0,255,0))
            if charuco_corners is not None:
                allCorners.append(charuco_corners)
                allIds.append(charuco_ids)
    imsize = images[0].shape
    print("calibrating")
    rms, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(allCorners, allIds, cal, imsize, None, None)
    print("calibrated")
    print("rms", rms)
    print("cameraMatrix", cameraMatrix)
    print("distCoeffs", distCoeffs)
    print("rvecs", rvecs)
    print("tvecs", tvecs)
    # save calibration
    np.savez("calibration.npz", K=cameraMatrix, DC=distCoeffs)

def estimate_pose():
    calib = np.load("calibration.npz")
    K = calib["K"]
    dist_coeffs = calib["DC"]
    sq_x = 7
    sq_y = 6
    aruco_dict_str = "DICT_APRILTAG_16H5"
    start_id = 0
    spacing_ratio = 0.65
    board = create_board(sq_x, sq_y, 14.099, 9.164, aruco_dict_str, start_id)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, board.dictionary)
        if ids is not None:
            print(ids)
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if charuco_corners is not None:
                print(charuco_ids)
                aruco.drawDetectedCornersCharuco(frame, charuco_corners, charuco_ids, (0,255,0))
                retval, rvec, tvec = aruco.estimatePoseCharucoBoard(charuco_corners, charuco_ids, board, K, dist_coeffs, np.array([]), np.array([]))
                if retval:
                    print("pose", rvec, tvec)
                    cv2.drawFrameAxes(frame, K, dist_coeffs, rvec, tvec, 10)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



def calib_dir_charuco(img_dir):
    sq_x = 7
    sq_y = 6
    aruco_dict_str = "DICT_APRILTAG_16H5"
    start_id = 0
    spacing_ratio = 0.65
    board = create_board(sq_x, sq_y, 14.099, 9.164, aruco_dict_str, start_id)
    # calibrate using images
    print("calibrating")
    cal = aruco.CharucoBoard_create(sq_x, sq_y, 14.099, 9.164, aruco.Dictionary_get(aruco.DICT_APRILTAG_16H5))
    allCorners = []
    allIds = []
    decimator = 0
    for img_path in glob.glob(img_dir + "/*.png"):
        im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(im, board.dictionary)
        if ids is not None:
            print(len(ids))
        if ids is not None and len(ids) > 10:
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, im, board)
            aruco.drawDetectedCornersCharuco(im, charuco_corners, charuco_ids, (0,255,0))
            if charuco_corners is not None:
                allCorners.append(charuco_corners)
                allIds.append(charuco_ids)
    imsize = im.shape
    print("calibrating")
    rms, cameraMatrix, distCoeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(allCorners, allIds, cal, imsize, None, None)
    print("calibrated")
    print("rms", rms)
    print("cameraMatrix", cameraMatrix)
    print("distCoeffs", distCoeffs)
    print("rvecs", rvecs)
    print("tvecs", tvecs)
    # save calibration
    np.savez("calibration.npz", K=cameraMatrix, DC=distCoeffs)


def estimate_pose_dir(img_dir):
    calib = np.load("calibration.npz")
    K = calib["K"]
    dist_coeffs = calib["DC"]
    sq_x = 7
    sq_y = 6
    aruco_dict_str = "DICT_APRILTAG_16H5"
    start_id = 0
    spacing_ratio = 0.65
    board = create_board(sq_x, sq_y, 14.099, 9.164, aruco_dict_str, start_id)
    for img_path in glob.glob(img_dir + "/*.png"):
        im = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(im, board.dictionary)
        if ids is not None:
            print(ids)
            ret, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(corners, ids, im, board)
            if charuco_corners is not None:
                print(charuco_ids)
                aruco.drawDetectedCornersCharuco(im, charuco_corners, charuco_ids, (0,255,0))
                retval, rvec, tvec = aruco.estimatePoseCharucoBoard(charuco_corners, charuco_ids, board, K, dist_coeffs, np.array([]), np.array([]))
                if retval:
                    print("pose", rvec, tvec)
                    cv2.drawFrameAxes(im, K, dist_coeffs, rvec, tvec, 10)
        cv2.imshow('frame',im)
        cv2.waitKey(0)






    




if __name__ == '__main__':
    #detect_charuco()
    #capture_and_calibrate()
    #estimate_pose()
    calib_dir_charuco("polar_calib")
    estimate_pose_dir("polar_calib")



    """
    aruco_dict_str = "DICT_APRILTAG_16H5"
    px_width = 4000
    squares_x = 7
    squares_y = 6
    spacing_ratio = 0.65
    start_id = 0
    padding = 800
    img = create_printable_aruco_grid(aruco_dict_str, px_width, squares_x, squares_y, spacing_ratio, start_id, padding)
    img = np.where(img<128, 128, img)
    cv2.imwrite("board.png", img)
    """


