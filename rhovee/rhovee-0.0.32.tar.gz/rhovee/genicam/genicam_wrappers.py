from harvesters.core import Harvester
import os
import cv2

class GenicamWrapper():
    def __init__(self, cti_path, device_num, exposure_time=30000, width=2176, height=2176, offset=968, gray=False):
        print("Initializing GenicamWrapper")
        h = Harvester()
        h.add_file(cti_path)
        h.update()
        h.device_info_list[0]
        # set exposure time
        ia = h.create(device_num)
        ia.remote_device.node_map.ExposureTime.value = exposure_time
        ia.remote_device.node_map.Width.value = width
        ia.remote_device.node_map.Height.value = height
        ia.remote_device.node_map.OffsetX.value = offset
        ia.start()
        self.gray = gray
        self.ia = ia
    
    def read(self):
        with self.ia.fetch() as buffer:
            component = buffer.payload.components[0]
            _1d = component.data
            _2d = component.data.reshape(component.height, component.width)
            debayered = cv2.cvtColor(_2d, cv2.COLOR_BAYER_RG2RGB)
            resized = cv2.resize(debayered, (component.width//2, component.width//2))
            if gray:
                resized = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
        return resized

class GenicamStereo():
    def __init__(self, cti_path, d_num_left, d_num_right, exposure_time=30000, width=2176, offset=968, gray=False):
        h = Harvester()
        h.add_file(cti_path)
        h.update()
        h.device_info_list[0]
        ia_left = h.create(d_num_left)
        ia_right = h.create(d_num_right)
        ia_left.remote_device.node_map.ExposureTime.value = exposure_time
        ia_right.remote_device.node_map.ExposureTime.value = exposure_time
        ia_left.remote_device.node_map.Width.value = width
        ia_right.remote_device.node_map.Width.value = width
        ia_left.remote_device.node_map.Height.value = width
        ia_right.remote_device.node_map.Height.value = width
        ia_left.remote_device.node_map.OffsetX.value = offset
        ia_right.remote_device.node_map.OffsetX.value = offset
        ia_left.start()
        ia_right.start()
        self.left = ia_left
        self.right = ia_right
        self.gray = gray

    
    def read(self):
        with self.left.fetch() as buffer:
            component = buffer.payload.components[0]
            _1d = component.data
            _2d = component.data.reshape(component.height, component.width)
            debayered = cv2.cvtColor(_2d, cv2.COLOR_BAYER_RG2RGB)
            resized = cv2.resize(debayered, (component.width//2, component.width//2))
            if self.gray:
                resized = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
            left = resized
        with self.right.fetch() as buffer:
            component = buffer.payload.components[0]
            _1d = component.data
            _2d = component.data.reshape(component.height, component.width)
            debayered = cv2.cvtColor(_2d, cv2.COLOR_BAYER_RG2RGB)
            resized = cv2.resize(debayered, (component.width//2, component.width//2))
            if self.gray:
                resized = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
            right = resized
        return left, right




if __name__ == '__main__':
    cti_path = "/opt/cvb-13.04.005/drivers/genicam/libGevTL.cti.1.2309"
    exposure_time = 60000
    device_num_left = 0
    device_num_right = 1
    cap = GenicamStereo(cti_path, device_num_left, device_num_right, exposure_time, gray=True)
    while True:
        left, right = cap.read()
        cv2.imshow('left', left)
        cv2.imshow('right', right)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    


