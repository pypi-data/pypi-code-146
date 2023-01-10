import io
import time
import os
import shutil
import traceback
import uuid

import numpy as np
from PIL import Image
from algorithm_mic_sdk.algorithms.human_plus_classic import HumanPlusClassic
from algorithm_mic_sdk.auth import ClassicAuthInfo
from algorithm_mic_sdk.tools import FileInfo

host = 'http://mars.leqi.us:17012'  # 算法host地址
user_name = 'panso'
password = '0bdca2d8-4a3d-11eb-addb-0242c0a80006'
classic_password = 'rongsuo'
classic_user_name = 'pan'


cut_params = {
    'size': [1050, 1500],
    'head_height': [0.15, 0.3],
    'headtop_margin': [0.05, 0.1],
    'need_resize': False
}
cut_params = None
auth_info = ClassicAuthInfo(classic_user_name=classic_user_name, classic_password=classic_password, user_name=user_name,
                            password=password, host=host, gateway_cache=True, extranet=True)

beauty_level = {"coseye": 0, "facelift": 0, "skinsoft":0, "leyelarge": 0, "reyelarge": 0, "skinwhite": 0, "mouthlarge": 0}
# skinwhite 美白 skinsoft 美肤
root = 'src/多张人脸换底色/'
times = [[],[]]
for file in os.listdir(root):
    filename = root+file
    file_info = FileInfo.for_file_bytes(open(filename, 'rb').read()+str(uuid.uuid1()).encode())
    process = 'image/auto-orient,1/resize,m_lfit,w2000,h_2000/quality,q_90'
    process = None
    n = file.split('.')[0]

    save_name = f'src/save2/{file}.png'
    if os.path.exists(save_name):
        continue
    human_plus_classic = HumanPlusClassic(auth_info,
                                          file_info,
                                          # process=process,
                                          # beauty_level=beauty_level,
                                          # cut_params=cut_params,
                                          just_one_face=False,
                                          need_all_face=False,
                                          need_to_use_cache=True)
    t0 = time.time()
    try:
        resp = human_plus_classic.synchronous_request(timeout=500)
        if resp.code == 200:
            times[0].append(resp.algo_server_timing)
            result_im_oss_name = resp.json['result']['result_im_oss_name']
            print(time.time() - t0, human_plus_classic.get_classic_file_url(result_im_oss_name))
            t1 = time.time()
            files = resp.json['result']['files']
            res_image = None
            res_mask = None
            for i, file in enumerate(files):
                result_im_bytes = human_plus_classic.get_classic_file(file)
                image = Image.open(io.BytesIO(result_im_bytes))
                # image.save(f'src/save2/{i}.png')
                r,g,b,mask = image.split()
                rgb = Image.merge('RGB', (r,g,b))
                np_mask = np.array(mask)
                if not res_image:
                    res_image = rgb
                    res_mask = np_mask
                    continue
                res_image.paste(rgb, (0, 0), mask)
                res_mask = np.maximum(np_mask, res_mask)


                # res_image.paste(image, (0,0), image)
                # np_img = np.array(image)
                # if res_image is None:
                #     res_image=np_img
                #     continue
                # res_image = np.maximum(res_image, np_img)
            # Image.fromarray(res_mask).save(f'src/save2/{3}.png')
            res_mask = Image.fromarray(res_mask)
            res_image.putalpha(res_mask)
            model_image = res_image
            model_image.save(save_name, format='PNG')
            times[1].append(time.time()-t1)
            print('成功', save_name, time.time()-t1, len(files))
        else:
            print('失败', save_name, resp.json)
    except Exception as e:
        print('失败', save_name, e, traceback.format_exc())
        continue

print(sum(times[0])/len(times[0]))
print(sum(times[1])/len(times[1]))