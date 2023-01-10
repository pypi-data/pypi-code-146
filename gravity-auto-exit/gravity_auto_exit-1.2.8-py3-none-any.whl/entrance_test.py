from gravity_auto_exit.main import AutoExit

# left, upper, right, lower
# 2592*1944

if __name__ == '__main__':
    inst = AutoExit(  # 'http://172.16.6.176',
        'http://127.0.0.1',
        'admin',
        'Assa+123',
        debug=True,
        resize_photo=(10, 10, 1900, 1200),
        cam_port=83,
        neurocore_login="admin",
        neurocore_password="admin"
    )
    # inst.set_post_request_url('http://127.0.0.1:8080/start_auto_exit')
    #result = inst.try_recognise_plate()
    #print(result['result'])
    inst.start()
