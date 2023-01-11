from skimage import segmentation, morphology, color
import numpy as np
import cv2

START_LABEL = 1
BACKGROUND_PIXEL_COLOR = 255  # this value CANNOT be changed otherwise the masking algo wont work.


# TODO: test with a withe object.

class SlicPatchImageProcessor:
    def __init__(self, number_of_segmentss):
        self._number_of_segments = number_of_segmentss

    def _calculate_start_end_position(self, block, block_len, pixels_size):
        start = block * block_len
        if (pixels_size - start) < block_len:
            start = pixels_size - block_len
        end = start + block_len
        return start, end

    def _get_b_w_image_from_mask(self, patch_img, masked_p):
        ret = np.ndarray(shape=patch_img.shape, dtype=patch_img.dtype)
        ret[:] = (0, 0, 0)
        for x in range(patch_img.shape[0]):
            for y in range(patch_img.shape[1]):
                if masked_p[x][y]:
                    ret[x][y] = (255, 255, 255)
        return ret

    def _binarize_image(self, masked_p, patch_img):
        b_w_image = self._get_b_w_image_from_mask(patch_img, masked_p)
        gr = cv2.cvtColor(b_w_image, cv2.COLOR_BGR2GRAY)
        _, im = cv2.threshold(gr, 127, 255, cv2.THRESH_BINARY)
        return im

    def _get_slic_unique_values(self, slic_img, patch_img):
        vector = []
        for i in range(1, 40):
            mask = slic_img == i
            masked = patch_img[mask]
            if masked.size > 0:
                vector.append(np.mean(masked))
            else:
                vector.append(-1)
        return vector

    def _get_patch_vector(self, img, slic_superpixels_original_image, x_end, x_start, y_block, y_len, y_pixels_size):

        y_start, y_end = self._calculate_start_end_position(y_block, y_len, y_pixels_size)
        slic_img, patch_img, masked_p = self._get_patch_background_foreground(img,
                                                                              (x_start, x_end),
                                                                              (y_start, y_end),
                                                                              slic_superpixels_original_image)
        im = self._binarize_image(masked_p, patch_img)
        moments = cv2.moments(im)
        ordered_moments = dict(sorted(moments.items()))
        huMoments = cv2.HuMoments(moments)
        vector_p = []
        vector_p.extend(list(ordered_moments.values()))
        vector_p.extend(np.concatenate(huMoments).ravel().tolist())
        vector_p.extend(self._get_slic_unique_values(slic_img, patch_img))
        return vector_p

    def _get_dominant_superpixel(self, labeled_slice):
        return np.bincount(labeled_slice.ravel()).argmax()

    def _get_only_foregroung_of_dominant_pixel(self, img_patch, max_pixel, labeled_slice):
        masked_3d = np.broadcast_to(np.atleast_3d(labeled_slice == max_pixel), img_patch.shape)
        return np.where(masked_3d, img_patch, BACKGROUND_PIXEL_COLOR)

    def _get_patch_background_foreground(self, img, x_min_max, y_min_max, slic_superpixels_labels,
                                         start_label=START_LABEL):
        """
        separetares the foreground which is object being looked from the background.

        :param img: numpy array image 2D array pixels representation
        :param x_min_max: (xmin,xmax) tuple of the region in the image in which the
        :param y_min_max:(ymin,ymax) tuple of the region in the image in which the
        :return: labeled slic and the object detected with plain background
        """

        labeled_slice = slic_superpixels_labels[x_min_max[0]:x_min_max[1], y_min_max[0]:y_min_max[1]]

        max_pixel = self._get_dominant_superpixel(labeled_slice)
        img_patch = img[x_min_max[0]:x_min_max[1], y_min_max[0]:y_min_max[1], :]
        sliced_img_f_b = self._get_only_foregroung_of_dominant_pixel(img_patch, max_pixel, labeled_slice)
        masked_patch = self._compute_mask(sliced_img_f_b)

        values = np.unique(masked_patch)

        if len(values) > 1:
            slic_superpixels_labels_patch = segmentation.slic(sliced_img_f_b, n_segments=self._number_of_segments,
                                                              start_label=start_label, mask=masked_patch)
        else:
            slic_superpixels_labels_patch = segmentation.slic(sliced_img_f_b, n_segments=self._number_of_segments,
                                                              start_label=start_label)

        return slic_superpixels_labels_patch, sliced_img_f_b, masked_patch

    def _compute_mask(self, img):
        lum = color.rgb2gray(img)
        mask = morphology.remove_small_holes(
            morphology.remove_small_objects(lum < 0.7, 500), 500)
        mask = morphology.opening(mask, morphology.disk(3))
        return mask

    def process_image_patches(self, img, x_len, y_len, blocks_multiplier=1):
        """

        :param img: image to process the metrics based on a patch size
        :param patcth_size: the patch size tuple (Xlen,Ylen)
        :param blocks_multiplier: defines the multiplier of the blocks search based on the min blocks
        :return: an array of patches metrics vector
        """
        vector = []
        mask_general = self._compute_mask(img)
        slic_sp = segmentation.slic(img, n_segments=self._number_of_segments, start_label=START_LABEL,
                                    mask=mask_general)
        x_pixels_size = img.shape[0]
        y_pixels_size = img.shape[1]
        x_blocks_qty = int(x_pixels_size / x_len * blocks_multiplier)
        y_blocks_qty = int(y_pixels_size / y_len * blocks_multiplier)

        for x_block in range(x_blocks_qty):
            x_start, x_end = self._calculate_start_end_position(x_block, x_len, x_pixels_size)
            for y_block in range(y_blocks_qty):
                vector_p = self._get_patch_vector(img, slic_sp, x_end, x_start, y_block, y_len, y_pixels_size)
                vector.extend(vector_p)
        return vector
