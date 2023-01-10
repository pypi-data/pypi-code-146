from photonvision._photonvision import PhotonTrackedTarget
from robotpy_apriltag._apriltag import AprilTag, AprilTagFieldLayout
from wpimath.geometry._geometry import Pose3d, Translation3d, Rotation3d, Transform3d

from robotpy_toolkit_7407.sensors.gyro import PigeonIMUGyro_Wrapper
from robotpy_toolkit_7407.sensors.photonvision import PhotonCamera, PhotonTarget, PhotonOdometry

gyro = PigeonIMUGyro_Wrapper(13)

cam = PhotonCamera("hello", Pose3d(Translation3d(0, 1, 2), Rotation3d(roll=1, pitch=2, yaw=3)), height=1, pitch=1)

april_tag_1 = AprilTag()
april_tag_1.ID = 1
april_tag_1.pose = Pose3d(Translation3d(0, 0, 0), Rotation3d(roll=0, pitch=0, yaw=0))

target = PhotonTarget(PhotonTrackedTarget(1, 1, 1, 1, 1, Transform3d(Pose3d(1, 1, 1, Rotation3d(1, 1, 1)),
                                                                     Pose3d(1, 1, 1, Rotation3d(1, 1, 1))),
                                          Transform3d(Pose3d(1, 1, 1, Rotation3d(1, 1, 1)),
                                                      Pose3d(1, 1, 1, Rotation3d(1, 1, 1))), .1,
                                          [(1, 1), (1, 1), (1, 1), (1, 1)]))

odometry = PhotonOdometry(
    cam,
    AprilTagFieldLayout(
        apriltags=[
            april_tag_1
        ],
        fieldLength=50,
        fieldWidth=30
    ),
    gyro
)

odometry.refresh()
print(odometry.getRobotPose())
