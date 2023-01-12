from copy import copy
from dataclasses import dataclass

import numpy

from nabu.stitching.overlap import ZStichOverlapKernel


@dataclass
class _FrameCompositionBase:
    def compose(self, output_frame: numpy.ndarray, input_frames: tuple):
        raise NotImplementedError("Base class")


@dataclass
class ZFrameComposition(_FrameCompositionBase):
    """
    class used to define intervals to know where to dump raw data or stitched data according to requested policy.
    The idea is to create this once for all for one stitching operation and reuse it for each frame.
    """

    local_start_y: tuple
    local_end_y: tuple
    global_start_y: tuple
    global_end_y: tuple

    def browse(self):
        for i in range(len(self.local_start_y)):
            yield (
                self.local_start_y[i],
                self.local_end_y[i],
                self.global_start_y[i],
                self.global_end_y[i],
            )

    def compose(self, output_frame: numpy.ndarray, input_frames: tuple):
        if not output_frame.ndim == 2:
            raise TypeError(f"output_frame is expected to be 2D and not {output_frame.ndim}")
        for (global_start_y, global_end_y, local_start_y, local_end_y, input_frame,) in zip(
            self.global_start_y,
            self.global_end_y,
            self.local_start_y,
            self.local_end_y,
            input_frames,
        ):
            if input_frame is not None:
                output_frame[global_start_y:global_end_y] = input_frame[local_start_y:local_end_y]

    @staticmethod
    def compute_raw_frame_compositions(frames: tuple, y_shifts: tuple, overlap_kernels: tuple):
        """
        compute frame composition for raw data
        """
        assert len(frames) == len(overlap_kernels) + 1 == len(y_shifts) + 1

        global_start_y = []
        local_start_y = []
        global_end_y = []
        local_end_y = []
        frame_height_sum = 0

        # extend shifts and kernels to have a first shift of 0 and two overlaps values at 0 to
        # generalize processing
        lower_shifts = [0]
        lower_shifts.extend(y_shifts)
        upper_shifts = list(copy(y_shifts))
        upper_shifts.append(0)
        overlaps = [kernel.overlap_height for kernel in overlap_kernels]
        overlaps.append(0)
        overlaps.insert(0, 0)

        for (
            frame,
            lower_shift,
            upper_shift,
            lower_overlap_kernel,
            upper_overlap_kernel,
        ) in zip(frames, lower_shifts, upper_shifts, overlaps[:-1], overlaps[1:]):
            if lower_shift > 0:
                raise ValueError(
                    "Unexpected shift value found; TODO: handle positive shift (this mean no overlap between frames"
                )
            lower_remaining = abs(lower_shift) - lower_overlap_kernel
            upper_o_s_diff = abs(upper_shift) - upper_overlap_kernel
            # policy with overlap that needs to take one more line on one side ((lower_remaining) % 2 == 1)
            # take this line on the lower frame side.
            new_local_start_y = lower_overlap_kernel + (lower_remaining) // 2 - (lower_remaining) % 2
            new_local_end_y = frame.shape[0] - (upper_overlap_kernel + (upper_o_s_diff) // 2)

            new_global_start_y = frame_height_sum + new_local_start_y
            new_global_end_y = frame_height_sum + new_local_end_y
            frame_height_sum += frame.shape[0] - abs(upper_shift)

            # check values are coherent
            if new_local_start_y < 0 or new_local_end_y < 0 or new_global_start_y < 0 or new_global_end_y < 0:
                raise ValueError(
                    "Incoherence found on the computing raw frame composition. Are you sure overlap height is no larger than frame height"
                )
            global_start_y.append(int(new_global_start_y))
            global_end_y.append(int(new_global_end_y))
            local_start_y.append(int(new_local_start_y))
            local_end_y.append(int(new_local_end_y))

        return ZFrameComposition(
            local_start_y=tuple(local_start_y),
            local_end_y=tuple(local_end_y),
            global_start_y=tuple(global_start_y),
            global_end_y=tuple(global_end_y),
        )

    @staticmethod
    def compute_stitch_frame_composition(frames, y_shifts: tuple, overlap_kernels: tuple):
        """
        compute frame composition for stiching.
        """
        assert len(frames) == len(overlap_kernels) + 1
        global_start_y = []
        global_end_y = []
        local_start_y = [0] * len(y_shifts)  # stiched is expected to be at the expected size already
        local_end_y = [kernel.overlap_height for kernel in overlap_kernels]

        frame_height_sum = 0
        for frame, kernel, y_shift in zip(frames[:-1], overlap_kernels, y_shifts):
            if y_shift > 0:
                raise ValueError(
                    "Unexpected shift value found; TODO: handle positive shift (this mean no overlap between frames"
                )

            assert isinstance(kernel, ZStichOverlapKernel)
            new_global_start_y = (
                frame_height_sum
                + frame.shape[0]
                - (kernel.overlap_height + (abs(y_shift) - kernel.overlap_height) // 2)
            )
            new_global_end_y = frame_height_sum + frame.shape[0] - (abs(y_shift) - kernel.overlap_height) // 2
            if new_global_start_y < 0 or new_global_end_y < 0:
                raise ValueError(
                    "Incoherence found on the computing raw frame composition. Are you sure overlap height is no larger than frame height"
                )
            global_start_y.append(int(new_global_start_y))
            global_end_y.append(int(new_global_end_y))
            frame_height_sum += frame.shape[0] + y_shift

        return ZFrameComposition(
            local_start_y=tuple(local_start_y),
            local_end_y=tuple(local_end_y),
            global_start_y=tuple(global_start_y),
            global_end_y=tuple(global_end_y),
        )

    @staticmethod
    def pprint_z_stitching(raw_composition, stitch_composition):
        """
        util to display what the output of the z stitch will looks like from composition
        """
        for i_frame, (raw_comp, stitch_comp) in enumerate(zip(raw_composition.browse(), stitch_composition.browse())):
            raw_local_start, raw_local_end, raw_global_start, raw_global_end = raw_comp

            print(
                f"stitch_frame[{raw_global_start}:{raw_global_end}] = frame_{i_frame}[{raw_local_start}:{raw_local_end}]"
            )

            (
                stitch_local_start,
                stitch_local_end,
                stitch_global_start,
                stitch_global_end,
            ) = stitch_comp

            print(
                f"stitch_frame[{stitch_global_start}:{stitch_global_end}] = stitched_frame_{i_frame}[{stitch_local_start}:{stitch_local_end}]"
            )
        else:
            i_frame += 1
            raw_local_start, raw_local_end, raw_global_start, raw_global_end = list(raw_composition.browse())[-1]
            print(
                f"stitch_frame[{raw_global_start}:{raw_global_end}] = frame_{i_frame}[{raw_local_start}:{raw_local_end}]"
            )
