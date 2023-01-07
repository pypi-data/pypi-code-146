# import platform
# import sys
# sys.path.append('build/lib.linux-%s-%s/' % (
#     platform.machine(), '.'.join(platform.python_version_tuple()[0:2])))
# import cModPyAlignment

import numpy as np
from vspscripts.alignment.utils.ann import Modification_ann


if __name__ == '__main__' :
    img_path = "./samples/gp4s___7663_18_16_5.jpg"
    cam_path = "./samples/gp4s___7663_18_16_5.png"
    ann_path = "./samples/gp4s___7663_18_16_5.json"
    # out_dir = "./samples"

    Mod = 'C'

    if Mod == 'C':
        from vspscripts.alignment.cModPyAlignment import ICpair_Aligning
        from vspscripts.alignment.utils.mat import Matrix_Sim_Generation
        Best = ICpair_Aligning(img_path, cam_path)
        matching_acc = Best['score']
        M_Sim = Matrix_Sim_Generation(theta=Best['theta'], s=Best['s'], t_x=Best['t_x'], t_y=Best['t_y'])
        print(matching_acc, M_Sim)
        Modification_ann(ann_path, M_Sim, matching_acc)
    elif Mod == 'P':
        from vspscripts.alignment.PyAlignment import ICpair_Aligning
        _, _, out_size, M_Sim, matching_acc = ICpair_Aligning(img_path, cam_path)
        print(matching_acc, M_Sim)
        Modification_ann(ann_path, M_Sim, matching_acc)
