import os
from pathlib import Path
from typing import Callable
from loguru import logger

import torch
from torch.utils.mobile_optimizer import optimize_for_mobile
from tepe.core.base_task import BaseTask

from tepe.utils.general import increment_path, file_size


class Exporter:
    def __init__(self, task, model=None, image_batcher=None):
        self.task: BaseTask = task

        if model is None:
            logger.info('Get model from task..')
            self.model = task.get_model(train=False)
        else:
            self.model = model
        assert self.model is not None
        setattr(self.model, 'export', True)

        self.input_size = task.input_size
        self.save_dir = task.output_dir
        out_file = task.out_file
        assert self.task.weights is not None
        self.save_name, _ = os.path.splitext(os.path.basename(self.task.weights))
        if out_file is not None:
            if os.path.isdir(out_file):  # file_dir
                self.save_dir = out_file
            elif os.path.isfile(out_file):  # file_path
                self.save_dir = os.path.abspath(os.path.dirname(out_file))
            else:  # file_name
                self.save_name = out_file

    def export(self, preprocessor=None):
        export_type = self.task.include
        if 'onnx' in export_type or 'tensorrt' in export_type:
            kwargs = dict(input_name=self.task.input_name, output_name=self.task.output_name,
                          opset=self.task.opset, dynamic=self.task.dynamic,
                          no_onnxsim=self.task.no_onnxsim)

            self.save_name = self.save_name.replace('.onnx', '')
            out_path = os.path.join(self.save_dir, f'{self.save_name}.onnx')
            self.export_onnx(self.model, self.input_size, out_path, **kwargs)

            self.task.set_post_info(onnx_path=out_path)

            if 'tensorrt' in export_type:
                onnx_file = out_path
                engine_file = out_path.replace('.onnx', '.engine')
                self.export_engine(
                    onnx_file, engine_file, self.task.precision, self.task.workspace,
                    self.task.calib_input, self.task.calib_cache, self.task.calib_num_images,
                    self.task.calib_batch_size, preprocessor
                )

    @staticmethod
    def export_onnx(model, input_size, out_path, input_name='images', output_name='output',
                    opset=11, dynamic=False, no_onnxsim=False):

        input_size = (input_size, input_size) if isinstance(input_size, int) else input_size
        dummy_input = torch.randn(1, 3, *input_size).type_as(next(model.parameters()))

        torch.onnx._export(
            model,
            dummy_input,
            out_path,
            input_names=[input_name],
            output_names=[output_name],
            dynamic_axes={input_name: {0: 'batch'},
                          output_name: {0: 'batch'}} if dynamic else None,
            opset_version=opset,
            do_constant_folding=True,
            training=torch.onnx.TrainingMode.EVAL,
        )

        if not no_onnxsim:
            import onnx
            from onnxsim import simplify

            input_shapes = {input_name: list(dummy_input.shape)} if dynamic else None

            # use onnxsimplify to reduce reduent model.
            onnx_model = onnx.load(out_path)
            model_simp, check = simplify(onnx_model,
                                         dynamic_input_shape=dynamic,
                                         input_shapes=input_shapes)
            assert check, "Simplified ONNX model could not be validated"
            onnx.save(model_simp, out_path)
        logger.info(f'onnx export success, saved as {out_path} ({file_size(out_path):.1f} MB)')

    def export_torchscript(self, model, im, file, optimize):
        # TorchScript model export
        try:
            out_path = os.path.join(self.save_dir, 'export.torchscript.pt')

            ts = torch.jit.trace(model, im, strict=False)
            (optimize_for_mobile(ts) if optimize else ts).save(out_path)

            logger.info(f'TorchScript: export success, saved as {out_path} ({file_size(out_path):.1f} MB)')
        except Exception as e:
            logger.info(f'TorchScript: export failure: {e}')

    def export_engine(
            self, onnx_file: str, engine_file: str, precision: str, workspace: int,
            calib_input: str, calib_cache: str, calib_num_images: int, calib_batch_size: int,
            preprocessor: Callable
    ) -> None:
        # TensorRT engine export
        try:
            from tepe.utils.tensorrt_utils import EngineBuilder
            builder = EngineBuilder(workspace=workspace, verbose=False)
            builder.create_network(onnx_file)
            builder.create_engine(engine_file, precision, calib_input, calib_cache, calib_num_images,
                                  calib_batch_size, preprocessor)
            logger.info(f'TensorRT: export sucess, saved as {engine_file} ({file_size(engine_file):.1f} MB')
        except Exception as e:
            logger.info(f'TensorRT: export failure: {e}')

    def export_ncnn(self):
        pass