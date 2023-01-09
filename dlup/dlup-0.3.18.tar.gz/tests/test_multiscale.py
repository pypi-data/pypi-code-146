from dlup.annotations import WsiAnnotations

if __name__ == "__main__":
    annotations = WsiAnnotations.from_geojson(["/Users/jteuwen/annotations/867/wsong@ellogon.ai/88210/roi.json"])

    bbox = annotations.bounding_boxes
    pass

# import numpy as np
#
# from dlup.data.experimental.dataset import MultiScaleSlideImageDataset
#
# if __name__ == "__main__":
#     path = "/home/j.teuwen/dev/svg2svs/checkerboard.svs"
#     mpps = [0.0625, 0.85]
#     tile_size = (1600, 1600)
#     tile_overlap = (800, 800)
#     rois = None  # [[0, 0, 3200, 3200]]
#     ds = MultiScaleSlideImageDataset.multiscale_from_tiling(
#         path, mpps, tile_size, tile_overlap=tile_overlap, mask=None, rois=rois
#     )
#     #
#     # w = ds[0]
#     # z = ds[1]
#
#     images0 = [np.asarray(ds[idx][0]["image"]) for idx in (0, 1, 2)]
#     images1 = [np.asarray(ds[idx][1]["image"]) for idx in (0, 1, 2)]
#     # images2 = [np.asarray(ds[idx][2]["image"]) for idx in (0, 1, 2)]
#     # images3 = [np.asarray(ds[idx][3]["image"]) for idx in (0, 1, 2)]
#     # images4 = [np.asarray(ds[idx][4]["image"]) for idx in (0, 1, 2)]
#     # images5 = [np.asarray(ds[idx][5]["image"]) for idx in (0, 1, 2)]
#
#     pass
