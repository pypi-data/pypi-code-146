from pickletools import uint8
import numpy as np
import re
import warnings
import struct
import lzf
from tqdm import tqdm
import argparse
from PIL import Image
from pathlib import Path
import time
from functools import wraps
from numba import cuda
import os
import cv2
from math import *
import torch
from tqdm import tqdm
from multiprocessing import Process
import copy

numpy_pcd_type_mappings = [
    (np.dtype("float32"), ("F", 4)),
    (np.dtype("float64"), ("F", 8)),
    (np.dtype("uint8"), ("U", 1)),
    (np.dtype("uint16"), ("U", 2)),
    (np.dtype("uint32"), ("U", 4)),
    (np.dtype("uint64"), ("U", 8)),
    (np.dtype("int8"), ("I", 1)),
    (np.dtype("int16"), ("I", 2)),
    (np.dtype("int32"), ("I", 4)),
    (np.dtype("int64"), ("I", 8)),
]
numpy_type_to_pcd_type = dict(numpy_pcd_type_mappings)
pcd_type_to_numpy_type = dict((q, p) for (p, q) in numpy_pcd_type_mappings)


def _parse_binary_compressed_pc_data(f, dtype, metadata):
    fmt = "II"
    compressed_size, uncompressed_size = struct.unpack(
        fmt, f.read(struct.calcsize(fmt))
    )
    compressed_data = f.read(compressed_size)

    buf = lzf.decompress(compressed_data, uncompressed_size)
    if len(buf) != uncompressed_size:
        raise Exception("Error decompressing data")
    # the data is stored field-by-field
    pc_data = np.zeros(metadata["points"], dtype=dtype)
    ix = 0
    for dti in range(len(dtype)):
        dt = dtype[dti]
        bytes = dt.itemsize * metadata["points"]
        column = np.frombuffer(buf[ix : (ix + bytes)], dt)
        pc_data[dtype.names[dti]] = column
        ix += bytes
    return pc_data


def _parse_binary_pc_data(f, dtype, metadata):
    rowstep = metadata["points"] * dtype.itemsize
    # for some reason pcl adds empty space at the end of files
    buf = f.read(rowstep)
    return np.frombuffer(buf, dtype=dtype)


def _parse_ascii_pc_data(f, dtype, metadata):
    return np.loadtxt(f, dtype=dtype, delimiter=" ")


def _parse_header(lines):
    metadata = {}
    for ln in lines:
        if ln.startswith("#") or len(ln) < 2:
            continue
        match = re.match("(\w+)\s+([\w\s\.]+)", ln)
        if not match:
            warnings.warn("warning: can't understand line: %s" % ln)
            continue
        key, value = match.group(1).lower(), match.group(2)
        if key == "version":
            metadata[key] = value
        elif key in ("fields", "type"):
            metadata[key] = value.split()
        elif key in ("size", "count"):
            metadata[key] = list(map(int, value.split()))
        elif key in ("width", "height", "points"):
            metadata[key] = int(value)
        elif key == "viewpoint":
            metadata[key] = list(map(float, value.split()))
        elif key == "data":
            metadata[key] = value.strip().lower()

    # add some reasonable defaults
    if "count" not in metadata:
        metadata["count"] = [1] * len(metadata["fields"])
    if "viewpoint" not in metadata:
        metadata["viewpoint"] = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    if "version" not in metadata:
        metadata["version"] = ".7"
    return metadata


def _build_dtype(metadata):
    """build numpy structured array dtype from pcl metadata.
    note that fields with count > 1 are 'flattened' by creating multiple
    single-count fields.
    TODO: allow 'proper' multi-count fields.
    """
    fieldnames = []
    typenames = []
    for f, c, t, s in zip(
        metadata["fields"], metadata["count"], metadata["type"], metadata["size"]
    ):
        np_type = pcd_type_to_numpy_type[(t, s)]
        if c == 1:
            fieldnames.append(f)
            typenames.append(np_type)
        else:
            fieldnames.extend(["%s_%04d" % (f, i) for i in range(c)])
            typenames.extend([np_type] * c)
    dtype = np.dtype(list(zip(fieldnames, typenames)))
    return dtype


def _point_cloud_from_fileobj(f):
    """parse pointcloud coming from file object f"""
    header = []
    while True:
        ln = f.readline().strip()
        if not isinstance(ln, str):
            ln = ln.decode("utf-8")
        header.append(ln)
        if ln.startswith("DATA"):
            metadata = _parse_header(header)
            dtype = _build_dtype(metadata)
            break
    if metadata["data"] == "ascii":
        pc_data = _parse_ascii_pc_data(f, dtype, metadata)
    elif metadata["data"] == "binary":
        pc_data = _parse_binary_pc_data(f, dtype, metadata)
    elif metadata["data"] == "binary_compressed":
        pc_data = _parse_binary_compressed_pc_data(f, dtype, metadata)
    else:
        print(
            'DATA field is neither "ascii" or "binary" or\
                "binary_compressed"'
        )
    return (metadata, pc_data)


def _write_header(metadata, rename_padding=False):
    """Given metadata as dictionary, return a string header."""
    template = """\
VERSION {version}
FIELDS {fields}
SIZE {size}
TYPE {type}
COUNT {count}
WIDTH {width}
HEIGHT {height}
VIEWPOINT {viewpoint}
POINTS {points}
DATA {data}
"""
    str_metadata = metadata.copy()

    if not rename_padding:
        str_metadata["fields"] = " ".join(metadata["fields"])
    else:
        new_fields = []
        for f in metadata["fields"]:
            if f == "_":
                new_fields.append("padding")
            else:
                new_fields.append(f)
        str_metadata["fields"] = " ".join(new_fields)
    str_metadata["size"] = " ".join(map(str, metadata["size"]))
    str_metadata["type"] = " ".join(metadata["type"])
    str_metadata["count"] = " ".join(map(str, metadata["count"]))
    str_metadata["width"] = str(metadata["width"])
    str_metadata["height"] = str(metadata["height"])
    str_metadata["viewpoint"] = " ".join(map(str, metadata["viewpoint"]))
    str_metadata["points"] = str(metadata["points"])
    tmpl = template.format(**str_metadata)
    return tmpl


def _build_ascii_fmtstr(pc):
    """Make a format string for printing to ascii.

    Note %.8f is minimum for rgb.
    """
    fmtstr = []
    for t, cnt in zip(pc.type, pc.count):
        if t == "F":
            fmtstr.extend(["%.10f"] * cnt)
        elif t == "I":
            fmtstr.extend(["%d"] * cnt)
        elif t == "U":
            fmtstr.extend(["%u"] * cnt)
        else:
            raise ValueError("don't know about type %s" % t)
    return fmtstr

    def save_point_cloud(self, pc, fname, mode="binary_compressed"):
        assert mode in ["ascii", "binary", "binary_compressed"]
        with open(fname, "w") as f:
            self.point_cloud_to_fileobj(pc, f, mode)


def point_cloud_to_fileobj(pc, fileobj, data_compression=None):
    """write pointcloud as .pcd to fileobj.
    if data_compression is not None it overrides pc.data.
    """
    metadata = pc.get_metadata()
    if data_compression is not None:
        data_compression = data_compression.lower()
        assert data_compression in ("ascii", "binary", "binary_compressed")
        metadata["data"] = data_compression

    header = _write_header(metadata).encode("utf-8")
    fileobj.write(header)
    if metadata["data"].lower() == "ascii":
        fmtstr = _build_ascii_fmtstr(pc)
        np.savetxt(fileobj, pc.pc_data, fmt=fmtstr)
    elif metadata["data"].lower() == "binary":
        fileobj.write(pc.pc_data.tobytes())
    elif metadata["data"].lower() == "binary_compressed":
        # TODO
        # a '_' field is ignored by pcl and breakes compressed point clouds.
        # changing '_' to '_padding' or other name fixes this.
        # admittedly padding shouldn't be compressed in the first place
        # reorder to column-by-column
        uncompressed_lst = []
        for fieldname in pc.pc_data.dtype.names:
            column = np.ascontiguousarray(pc.pc_data[fieldname]).tobytes()
            uncompressed_lst.append(column)
        uncompressed = b"".join(uncompressed_lst)
        uncompressed_size = len(uncompressed)
        # print("uncompressed_size = %r"%(uncompressed_size))
        buf = lzf.compress(uncompressed)
        if buf is None:
            # compression didn't shrink the file
            # TODO what do to do in this case when reading?
            buf = uncompressed
            compressed_size = uncompressed_size
        else:
            compressed_size = len(buf)
        fmt = "II"
        fileobj.write(struct.pack(fmt, compressed_size, uncompressed_size))
        fileobj.write(buf)
    else:
        raise ValueError("unknown DATA type")
    # we can't close because if it's stringio buf then we can't get value after


def _metadata_is_consistent(metadata):
    """Sanity check for metadata. Just some basic checks."""
    checks = []
    required = (
        "version",
        "fields",
        "size",
        "width",
        "height",
        "points",
        "viewpoint",
        "data",
    )
    for f in required:
        if f not in metadata:
            print("%s required" % f)
    checks.append((lambda m: all([k in m for k in required]), "missing field"))
    checks.append(
        (
            lambda m: len(m["type"]) == len(m["count"]) == len(m["fields"]),
            "length of type, count and fields must be equal",
        )
    )
    checks.append((lambda m: m["height"] > 0, "height must be greater than 0"))
    checks.append((lambda m: m["width"] > 0, "width must be greater than 0"))
    checks.append((lambda m: m["points"] > 0, "points must be greater than 0"))
    checks.append(
        (
            lambda m: m["data"].lower() in ("ascii", "binary", "binary_compressed"),
            "unknown data type:" "should be ascii/binary/binary_compressed",
        )
    )
    ok = True
    for check, msg in checks:
        if not check(metadata):
            print("error:", msg)
            ok = False
    return ok


def pc_from_path(fname):
    """load pcd and return a PointCloud instance"""
    with open(fname, "rb") as f:
        meta, pc = _point_cloud_from_fileobj(f)
        return PointCloud(meta, pc)


def pc_concat(pc_list):
    """concatenate multiple point clouds"""
    metas = [i.get_metadata() for i in pc_list]
    fields_unique = np.unique(np.array([i["fields"] for i in metas]), axis=0)
    size_unique = np.unique(np.array([i["size"] for i in metas]), axis=0)
    type_unique = np.unique(np.array([i["type"] for i in metas]), axis=0)
    points_list = [i["points"] for i in metas]
    width_list = [i["width"] for i in metas]
    height_list = [i["height"] for i in metas]
    data_list = [i["data"] for i in metas]
    # all concat pc has same fields, size and type
    try:
        assert (
        fields_unique.shape[0] == 1
        and size_unique.shape[0] == 1
        and type_unique.shape[0] == 1
        and len(set(data_list)) == 1
        # and len(set(width_list)) == 1
        # and len(set(height_list)) == 1
    )
    except:
        from IPython import embed; embed(colors='neutral')
    meta = pc_list[0].get_metadata()
    meta["points"] = np.sum(points_list)
    meta["width"] = meta["points"]
    meta["height"] = 1
    pc = np.concatenate([pc.pc_data for pc in pc_list])
    return PointCloud(meta, pc)


# def pc_transform(pc_array, extr_matr):
#     pc_trans = np.apply_along_axis(
#         homogene_transformation, axis=1, arr=pc_array, homo_matr=extr_matr
#     )
#     return pc_trans


# def homogene_transformation(self, arr, homo_matr):
#     arr_xyz_homo = np.append(arr[:3], 1)
#     arr_xyz_trans = np.matmul(homo_matr, arr_xyz_homo)
#     arr_rest = arr[3:]
#     arr_ret = np.append(arr_xyz_trans[:3], arr_rest)
#     return arr_ret


class PointCloudVisualizer:
    def __init__(
        self,
        height=2400,
        width=1200,
        scale=10,
        world_trans=[0, 0, 0],
        point_scale=5,
        line_scale=2,
    ):
        self._set_canvas(
            height=height, width=width, scale=scale, world_trans=world_trans
        )
        # self.point_scale = point_scale
        # self.line_scale = line_scale
        self.FONT = cv2.FONT_HERSHEY_PLAIN
        self.color_dic = {
            "GT": [255, 255, 255],
            "FP": {
                "HIGH": [0, 0, 255],
                "MID": [144, 32, 208],
                "LOW": [203, 192, 255],
            },
            "FN": [0, 255, 255],
            "TP": [0, 255, 0],
            "FTP": [0, 255, 0],  # force tp
            "STP": [238, 229, 0],  # soft tp
            "DET": {
                "LOW": [205, 205, 150],
                # 'MID': [0,255,0],
                "HIGH": [0, 255, 0],
                "MID": [124, 205, 124],
            },
            "red": [255, 0, 0],
            "green": [0, 255, 0],
            "blue": [0, 0, 255],
            "yellow": [255, 255, 0],
            "purple": [255, 0, 255],
            "cyan": [0, 255, 255],
            "white": [255, 255, 255],
            "black": [0, 0, 0],
            "gray": [128, 128, 128],
        }

    def _maybe_tensor2numpy(self, data):
        if isinstance(data, torch.Tensor):
            data = data.detach().cpu().numpy()
        return data

    def _set_canvas(self, height=2000, width=1000, scale=10, world_trans=[0, 0, 0]):
        self.IM_H = height
        self.IM_W = width
        self.SCALE = scale
        self.WORLD_TRANS = world_trans
        self.IMAGE_TRANS = [self.IM_W / 2, self.IM_H / 2]

    def init_image(self):
        image = np.zeros((self.IM_H, self.IM_W, 3), np.uint8)
        return image

    def transfer_coor(self, pt):
        pt_trans = (np.array(pt) + np.array(self.WORLD_TRANS)) * self.SCALE
        pt_trans[0] = np.clip(-pt_trans[0] + self.IMAGE_TRANS[1], 0, self.IM_H)
        pt_trans[1] = np.clip(-pt_trans[1] + self.IMAGE_TRANS[0], 0, self.IM_W)
        return pt_trans.astype(np.int32)

    def transfer_coors(self, pts):
        pts_trans = np.array([self.transfer_coor(x) for x in pts])
        return pts_trans.astype(np.int32)

    def draw_pcloud(self, pcloud, color="gray", r=0, draw_distance_marker=True):
        """
        draw point cloud on image
        Args:
        image: [H, W, 3]
        pcloud: [N, 4] ndarray
        """
        image = self.init_image()

        for pt in pcloud:
            pt_draw = self.transfer_coor([pt[0], pt[1], 0])
            if (
                pt_draw[0] >= 0
                and pt_draw[0] < self.IM_H
                and pt_draw[1] >= 0
                and pt_draw[1] < self.IM_W
            ):
                image[
                    pt_draw[0] - r : pt_draw[0] + r + 1,
                    pt_draw[1] - r : pt_draw[1] + r + 1,
                ] = self.color_dic[color]
        if draw_distance_marker:
            self.draw_distance_marker(image)
        return image

    def draw_pc_overlay(self, pc_tuple, draw_distance_marker=True):
        """
        draw multiple point cloud class on image
        Args:
        image: [H, W, 3]
        pcloud: [N, 4] ndarray

        """
        image = self.init_image()
        for pcloud_color in pc_tuple:
            pcloud, color, r = pcloud_color
            for pt in pcloud.pc_data:
                pt_draw = self.transfer_coor([pt["x"], pt["y"], 0])
                if (
                    pt_draw[0] >= 0
                    and pt_draw[0] < self.IM_H
                    and pt_draw[1] >= 0
                    and pt_draw[1] < self.IM_W
                ):
                    image[
                        pt_draw[0] - r : pt_draw[0] + r + 1,
                        pt_draw[1] - r : pt_draw[1] + r + 1,
                    ] = self.color_dic[color]
        if draw_distance_marker:
            self.draw_distance_marker(image)
        return image

    def draw_pcloud_overlay(self, pc_tuple, draw_distance_marker=True):
        """
        draw multiple point cloud array on image
        TODO wait for refactor
        Args:
        image: [H, W, 3]
        pcloud: [N, 4] ndarray

        """
        image = self.init_image()
        for pcloud_color in pc_tuple:
            pcloud, color, r = pcloud_color
            for pt in pcloud:
                pt_draw = self.transfer_coor([pt[0], pt[1], 0])
                if (
                    pt_draw[0] >= 0
                    and pt_draw[0] < self.IM_H
                    and pt_draw[1] >= 0
                    and pt_draw[1] < self.IM_W
                ):
                    image[
                        pt_draw[0] - r : pt_draw[0] + r + 1,
                        pt_draw[1] - r : pt_draw[1] + r + 1,
                    ] = self.color_dic[color]
        if draw_distance_marker:
            self.draw_distance_marker(image)
        return image

    def draw_distance_marker(self, image, ranges_value=None):
        if not ranges_value:
            ranges_value = [40, 80, 120, 160, 200]
        color = (255, 255, 255)
        thickness = 1
        center_coordinates = tuple([int(self.IMAGE_TRANS[0]), int(self.IMAGE_TRANS[1])])

        for range_value in ranges_value:
            radius = int(range_value * self.SCALE)
            cv2.circle(image, center_coordinates, radius, color, thickness)

    def img_save(self, image, save_path, auto_rot=True):
        if auto_rot and image.shape[0] > image.shape[1]:
            img = np.rot90(image, -1)
        else:
            img = image
        path = os.path.join(save_path)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img_bgr)

    def draw_bbox(self, image, obj_corners, color=(255, 255, 255), line=1):
        b = obj_corners[:8].reshape([-1, 2])
        scor = obj_corners[-2] if obj_corners.shape[0] > 8 else 1.0
        clas = obj_corners[-1] if obj_corners.shape[0] > 8 else -1
        for k in range(0, 4):
            i, j = k, (k + 1) % 4
            pt0 = self.transfer_coor([b[i, 0], b[i, 1], 0])
            pt1 = self.transfer_coor([b[j, 0], b[j, 1], 0])
            cv2.line(image, (pt0[1], pt0[0]), (pt1[1], pt1[0]), color, line)

    def draw_cicle(self, image, obj, color=(0, 0, 255), r=4):
        center = obj[:3]
        pt = self.transfer_coor([center[0], center[1], 0])
        cv2.circle(image, (pt[1], pt[0]), r, color, -1)

    def draw_orientation(self, image, obj, color=(0, 255, 255)):
        center = obj[:3]
        theta = obj[6]
        vec = np.array([cos(theta), sin(theta), 0]) * obj[3]
        orientation = center + vec
        pt0 = self.transfer_coor([center[0], center[1], 0])
        pt1 = self.transfer_coor([orientation[0], orientation[1], 0])
        cv2.line(image, (pt0[1], pt0[0]), (pt1[1], pt1[0]), color, 1)

    def img_show(self, image, auto_rot=True):
        if auto_rot and image.shape[0] > image.shape[1]:
            img = np.rot90(image, -1)
        else:
            img = image
        img = Image.fromarray(img)
        img.show()

    def draw_str(self, image, center, class_name, color=(255, 255, 255)):
        pt0 = self.transfer_coor([center[0], center[1], 0])
        cv2.putText(
            image,
            class_name,
            (pt0[1] + 10 + 10, pt0[0] + 10),
            self.FONT,
            0.8,
            color,
            1,
            cv2.LINE_AA,
        )

    def draw_arrow(self, image, pixes1, pixes2, color=(0, 155, 155)):
        pixes1 = self._maybe_tensor2numpy(pixes1)
        pixes2 = self._maybe_tensor2numpy(pixes2)
        for pt1, pt2 in zip(pixes1, pixes2):
            pt1 = self.transfer_coor([pt1[0], pt1[1], 0])
            pt2 = self.transfer_coor([pt2[0], pt2[1], 0])
            cv2.arrowedLine(
                image,
                (int(pt1[1]), int(pt1[0])),
                (int(pt2[1]), int(pt2[0])),
                color,
                thickness=1,
                line_type=cv2.LINE_4,
                shift=0,
                tipLength=0.1,
            )
        return image


class PointCloud:
    """Wrapper for point cloud data.

    The variable members of this class parallel the ones used by
    the PCD metadata (and similar to PCL and ROS PointCloud2 messages),

    ``pc_data`` holds the actual data as a structured numpy array.

    The other relevant metadata variables are:

    - ``version``: Version, usually .7
    - ``fields``: Field names, e.g. ``['x', 'y' 'z']``.
    - ``size.`: Field sizes in bytes, e.g. ``[4, 4, 4]``.
    - ``count``: Counts per field e.g. ``[1, 1, 1]``. NB: Multi-count field
      support is sketchy.
    - ``width``: Number of points, for unstructured point clouds (assumed by
      most operations).
    - ``height``: 1 for unstructured point clouds (again, what we assume most
      of the time.
    - ``viewpoint``: A pose for the viewpoint of the cloud, as
      x y z qw qx qy qz, e.g. ``[0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]``.
    - ``points``: Number of points.
    - ``type``: Data type of each field, e.g. ``[F, F, F]``.
    - ``data``: Data storage format. One of ``ascii``, ``binary`` or ``binary_compressed``.

    See `PCL docs <http://pointclouds.org/documentation/tutorials/pcd_file_format.php>`__
    for more information.
    """

    def __init__(self, metadata, pc_data):
        self.metadata_keys = metadata.keys()
        self.__dict__.update(metadata)
        self.pc_data = pc_data
        self.check_sanity()
        self.vis = PointCloudVisualizer()

    def get_metadata(self):
        """returns copy of metadata"""
        metadata = {}
        for k in self.metadata_keys:
            metadata[k] = copy.copy(getattr(self, k))
        return metadata

    def check_sanity(self):
        md = self.get_metadata()
        assert _metadata_is_consistent(md)
        assert len(self.pc_data) == self.points
        assert self.width * self.height == self.points
        assert len(self.fields) == len(self.count)
        assert len(self.fields) == len(self.type)

    def save_ascii(self, fname):
        self.save_pcd(fname, "ascii")

    def draw_pcloud(
        self,
        color="gray",
        r=0,
        show=True,
        save=False,
        save_path=None,
        draw_distance_marker=True,
    ):
        draw = self.vis.draw_pcloud(self.pc_data, color, r, draw_distance_marker)
        if show:
            self.vis.img_show(draw)
        if save:
            self.vis.img_save(draw, save_path)
        return draw

    def to_ndarray(self, fields=None):
        if not fields:
            fields = ["x", "y", "z"]
        assert set(fields).issubset(
            set(self.fields)
        ), f"Invalid fields, only support {str(self.fields)}"
        field_list = [self.pc_data[f].reshape(-1, 1) for f in fields]
        points = np.concatenate((field_list), axis=1)
        points = points[~np.isnan(points)[:, 0]]
        points.astype(np.float32)
        return points

    def to_lidar_ndarray(self):
        try:
            points = self.to_ndarray(fields=["x", "y", "z", "intensity"])
        except:
            points = self.to_ndarray(fields=["x", "y", "z"])
            print(points.shape)
            points = np.concatenate(
                [points, np.ones((points.shape[0], 1), dtype=np.float32)], axis=1
            )
        return points

    def to_radar_ndarray(self):
        try:
            points = self.to_ndarray(fields=["x", "y", "z", "rcs", "radial_vel"])
        except:
            points = self.to_ndarray(fields=["x", "y", "z"])
        return points

    def save_pcd(self, fname, compression=None, **kwargs):
        if "data_compression" in kwargs:
            warnings.warn("data_compression keyword is deprecated for" " compression")
            compression = kwargs["data_compression"]
        with open(fname, "wb") as f:
            point_cloud_to_fileobj(self, f, compression)

    def coor_trans(self, extr_mat):
        pc_data = self.pc_data.copy()
        assert "x" in self.fields and "y" in self.fields and "z" in self.fields

        x = pc_data["x"]
        y = pc_data["y"]
        z = pc_data["z"]
        xyz = np.stack((x, y, z)).T

        pc_trans = np.apply_along_axis(
            self.homogene_transformation, axis=1, arr=xyz, homo_matr=extr_mat
        )

        pc_data["x"] = pc_trans[:, 0]
        pc_data["y"] = pc_trans[:, 1]
        pc_data["z"] = pc_trans[:, 2]
        self.pc_data = pc_data
        return self

    def homogene_transformation(self, arr, homo_matr):
        arr_xyz_homo = np.append(arr[:3], 1)
        arr_xyz_trans = np.matmul(homo_matr, arr_xyz_homo)
        arr_rest = arr[3:]
        arr_ret = np.append(arr_xyz_trans[:3], arr_rest)
        return arr_ret

    def copy(self):
        new_pc_data = np.copy(self.pc_data)
        new_metadata = self.get_metadata()
        return PointCloud(new_metadata, new_pc_data)

    @staticmethod
    def from_path(fname):
        return pc_from_path(fname)

    @staticmethod
    def pc_concat(pc_list):
        return pc_concat(pc_list)

    # @staticmethod
    # def draw_pcloud_overlay(pc_tuple, draw_distance_marker=True):
    #     self.vis.draw_pcloud_overlay(pc_tuple, draw_distance_marker=True):



# def array2pcd(arr, field_names=None):
#     """create a PointCloud object from an np struct/array."""
#     pc_data = arr.copy()
#     md = {
#         "version": 0.7,
#         "fields": [],
#         "size": [],
#         "count": [],
#         "width": 0,
#         "height": 1,
#         "viewpoint": [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
#         "points": 0,
#         "type": [],
#         "data": "binary",
#     }
#     md["fields"] = field_names
#     assert len(field_names) == arr.shape[1]
#     for count, field in enumerate(md["fields"]):
#         type_, size_ = numpy_type_to_pcd_type[pc_data.dtype]
#         md["type"].append(type_)
#         md["size"].append(size_)
#         md["count"].append(1)
#     md["width"] = len(pc_data)
#     md["points"] = len(pc_data)
#     pc = PointCloud(md, pc_data)
#     return pc


def concat():
    pc_dict = {}
    path = Path("/Users/yuehao/Desktop/small_set_benz/output/9885806035")
    for folder in path.iterdir():
        if folder.is_dir() and "radar" in folder.name:

            for file in folder.iterdir():
                if file.suffix == ".pcd":
                    pc_dict[folder.name] = pc_from_path(file).to_radar_ndarray()
                    continue
                    pc = pc_from_path(file).to_lidar_ndarray()
                    print(pc.shape)
                    pc_concat = np.concatenate((pc_concat, pc), axis=0)
                    print(pc_concat.shape)
    print(pc_dict)


def demo_pcdtrans_concat():
    # pcd1
    pcd1 = pc_from_path(
        "/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd"
    )
    # pcd2 with coor transformation
    pcd2 = pc_from_path(
        "/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd"
    ).coor_trans(np.array([[1, 0, 0, 10], [0, 1, 0, 10], [0, 0, 1, 0], [0, 0, 0, 1]]))
    pcd3 = pc_from_path(
        "/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd"
    ).coor_trans(np.array([[1, 0, 0, -10], [0, 1, 0, 10], [0, 0, 1, 0], [0, 0, 0, 1]]))
    # concat pcd1 and pcd2
    pcd_concat = pc_concat([pcd1, pcd2, pcd3])
    pcd_concat.save_pcd("pcd_concat.pcd")
    vis = PointCloudVisualizer()
    bev_concat = vis.draw_pc_overlay(((pcd1, "gray", 0), (pcd2, "red", 1)))
    vis.img_show(bev_concat)


def demo_load_vis_pcd():
    pcd1 = pc_from_path(
        "/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd"
    )
    bev = pcd1.draw_pcloud(show=True)


if __name__ == "__main__":

    pcd = PointCloud.from_path('test.pcd')
    pcd.save_ascii('test_ascii.pcd')


    # # concat()
    # # exit()
    # pch = PointCloudHelper()
    # vis = PointCloudVisualizer()
    # #pcl = pc_from_path("/Users/yuehao/Desktop/small_set_benz/top_lidar/9885804720.pcd")
    # #pcl2 = pc_from_path("/Users/yuehao/Desktop/small_set_benz/top_lidar/9885804720.pcd").coor_trans(np.array([[1, 0, 0, 110], [0, 1, 0, 100], [0, 0, 1, 0], [0, 0, 0, 1]]))
    # pcr1 = pc_from_path('/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd')
    # pcr2 = pc_from_path('/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd').coor_trans(np.array([[1, 0, 0, 10], [0, 1, 0, 10], [0, 0, 1, 0], [0, 0, 0, 1]]))
    # pcr3 = pc_from_path('/Users/yuehao/Momenta/labeltest/sampled_data/436fcc645714492c68b42b5dd3ba80aa/1656923753.220280.360lidar.pcd').coor_trans(np.array([[1, 0, 0, 10], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))

    # bev_lidar = vis.draw_pc_overlay(((pcr1, "gray", 0), (pcr2, "red", 1)))
    # vis.img_show(bev_lidar)
    # exit()
    # pc_con = pc_concat([pcr1,pcr2,pcr3])

    # draw = pc_con.draw_pcloud()
    # #pcl.save_pcd('test.pcd')
    # exit()

    # # draw_radar=vis.draw_pcloud(pcr,'red',1)
    # # vis.bev_show(draw_radar)

    # # #pc_concat=np.concatenate((pcl[:,0:3],pcr[:,0:3]))
    # # pc_concat = pc_from_path('/Users/yuehao/Desktop/small_set_benz/output/9885806035/merged_radar/9885806035.pcd').to_lidar_ndarray()
    # # draw_radar=vis.draw_pcloud(pc_concat,'red',1)
    # # vis.bev_show(draw_radar)
    # # pc_lidar = pc_from_path('/Users/yuehao/Desktop/small_set_benz/output/9885806035/top_lidar/9885804720.pcd').to_lidar_ndarray()
    # # pc_lidar_trans = pch.pc_transform(pc_lidar, np.array([[0.999894, 0.002756, -0.014267, 1.525952], [-0.002718, 0.999993, 0.002662, 1.031374], [0.014274, -0.002623, 0.999895,  2.37252], [0, 0, 0, 1]]))
    # # draw=vis.draw_pcloud_overlay(((pc_lidar_trans,'gray', 0),(pc_concat,'red', 1)))
    # # print(draw.shape)
    # # vis.bev_show(draw)
    # # exit()

    # # bev_radar = vis.draw_pcloud(pc_concat,'red', 1)
    # # bev_lidar = vis.draw_pcloud(pc_lidar,'gray', 0)
    # # vis.bev_show(bev_radar)

    # # pcr可以作为struct
    # pcd = array2pcd(pcr[:,:3],field_names=["x", "y", "z"])
    # pcd.save_pcd('save.pcd')

    # bev_lidar = vis.draw_pcloud_overlay(((pcl, "gray", 0), (pcr, "red", 1)))
    # vis.img_show(bev_lidar)

    # # lpt=lpt[110:120]
    # pc_trans = pch.pc_transform(pcl, np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))

    # draw = pch.draw_pcloud_single(pc_trans, "gray", 2)
    # vis.img_show(draw)
    # # dra_overlay = pch.draw_pcloud_overlay(((lpt, "gray", 0), (rpt, "red", 1)))
    # # pch.image_save("save.png", draw_overlay)
    # # pch.image_show(draw_overlay)
