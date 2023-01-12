

def pc_to_o3d(pc_np):
    assert pc_np.shape[1] == 3
    


def o3d_to_pc(pc_o3d):
    return np.array(pc_o3d.points)

def keep_overlap_pc(pc1_np, pc2_np, max_dist):
    # pc shape (n,3)
    assert pc1_np.shape[1] == 3 and pc2_np.shape[1] == 3
    pc1_o3d = o3d.geometry.PointCloud()
    pc2_o3d = o3d.geometry.PointCloud()
    pc1_o3d.points = o3d.utility.Vector3dVector(pc1_np)
    pc2_o3d.points = o3d.utility.Vector3dVector(pc2_np)
    result = o3d.pipelines.registration.evaluate_registration(pc1_o3d, pc2_o3d, max_dist, np.eye(4))
    corr = np.array(result.correspondence_set)
    kept_inds = corr[:,0]
    pc1_points = np.asarray(pc1_o3d.points)
    kept_points = pc1_points[pc1_keep_inds]
    return kept_points
    


    



if __name__ == '__main__':
    pass
