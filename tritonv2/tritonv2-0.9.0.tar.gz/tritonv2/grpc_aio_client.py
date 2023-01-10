# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton aio grpc client
"""
import tritonclient.grpc.aio as grpc_client
from .client import TritonClient
from .utils import parse_model
from .exceptions import TritonClientException


class TritonAioGRPCClient(TritonClient):
    """
    Concrete implementation of TritonClient
    for GRPC AIO
    """

    def __init__(self,
                 server_url,
                 channel_args,
                 verbose=False,
                 ssl=False,
                 authority="",
                 root_certificates="",
                 private_key="",
                 certificate_chain="",
                 creds=None,
                 keepalive_options=None):
        """
        Parameters
        :param server_url:
        :param channel_args:
        :param ssl:
        :param root_certificates:
        :param private_key:
        :param certificate_chain:
        :param creds:
        :param keepalive_options:
        """

        super().__init__()

        if keepalive_options is None:
            keepalive_options = grpc_client.KeepAliveOptions()

        channel_args.append(("grpc.max_send_message_length", grpc_client.MAX_GRPC_MESSAGE_SIZE))
        channel_args.append(("grpc.max_receive_message_length", grpc_client.MAX_GRPC_MESSAGE_SIZE))
        channel_args.append(("grpc.keepalive_time_ms", keepalive_options.keepalive_time_ms))
        channel_args.append(("grpc.keepalive_timeout_ms", keepalive_options.keepalive_timeout_ms))
        channel_args.append(("grpc.keepalive_permit_without_calls",
                             keepalive_options.keepalive_permit_without_calls))
        channel_args.append(("grpc.http2.max_pings_without_data",
                             keepalive_options.http2_max_pings_without_data))

        if authority != "":
            channel_args.append(("grpc.default_authority", authority))

        self._client = grpc_client.InferenceServerClient(
            url=server_url,
            verbose=verbose,
            ssl=ssl,
            root_certificates=root_certificates,
            private_key=private_key,
            certificate_chain=certificate_chain,
            creds=creds,
            keepalive_options=keepalive_options,
            channel_args=channel_args,
        )

    async def close(self):
        """
        Close the client
        :return:
        """
        await self._client.close()

    async def __aenter__(self):
        """
        async context manager enter
        :return:
        """
        return self

    async def __aexit__(self, type, value, traceback):
        """
        async context manager exit
        :param type:
        :param value:
        :param traceback:
        :return:
        """
        await self.close()

    async def model_meta(self, model_name, model_version=""):
        """
        get model meta
        :param model_name:
        :param model_version:
        :return:
        """
        try:
            return await self._client.get_model_metadata(
                model_name=model_name,
                model_version=model_version,
                as_json=True)
        except Exception as e:
            raise TritonClientException('Failed to get model metadata: {}'.format(e)) from None

    async def model_config(self, model_name, model_version=""):
        """
       get model config
       :param model_name:
       :param model_version:
       :return:
       """
        try:
            model_config_dict = await self._client.get_model_config(
                model_name=model_name,
                model_version=model_version,
                as_json=True)
            return model_config_dict["config"]
        except Exception as e:
            raise TritonClientException('Failed to get model config: {}'.format(e)) from None

    async def model_ready(self, model_name, model_version=""):
        """
        check model ready
        :param model_name:
        :param model_version:
        :return:
        """
        try:
            return await self._client.is_model_ready(
                model_name=model_name,
                model_version=model_version)
        except Exception as e:
            raise TritonClientException('Failed to get model ready: {}'.format(e)) from None

    async def server_meta(self, headers=None):
        """
        get server metadata
        Returns
        :return:
        """
        try:
            return await self._client.get_server_metadata(headers=headers, as_json=True)
        except Exception as e:
            raise TritonClientException('Failed to get server meta: {}'.format(e)) from None

    async def server_live(self, headers=None):
        """
        check if the server live
        :param headers:
        :return:
        """
        try:
            return await self._client.is_server_live(headers=headers)
        except Exception as e:
            raise TritonClientException('Failed to check server live: {}'.format(e)) from None

    async def server_ready(self, headers=None):
        """
        check if the server is ready
        :param headers:
        :return:
        """
        try:
            return await self._client.is_server_ready(headers=headers)
        except Exception as e:
            raise TritonClientException(
                "Failed to check server ready: {}".format(e)) from None

    async def model_statistics(self, model_name, model_version="", headers=None):
        """
        get model statistics
        :param model_name:
        :param model_version:
        :param headers:
        :return:
        """
        try:
            return await self._client.get_inference_statistics(model_name, model_version, headers=headers,
                                                               as_json=True)
        except Exception as e:
            raise TritonClientException('Failed to get model statistics: {}'.format(e)) from None

    async def repository_index(self, headers=None):
        """
        get repository index
        :param headers:
        :return:
        """
        try:
            repository_index_dict = await self._client.get_model_repository_index(headers=headers, as_json=True)
            return repository_index_dict["models"]
        except Exception as e:
            raise TritonClientException('Failed to get repository index: {}'.format(e)) from None

    async def repository_model_load(self, model_name, headers=None, config="", files=None):
        """
        load model
        :param model_name:
        :param headers:
        :param config:
        :param files:
        :return:
        """
        try:
            return await self._client.load_model(model_name=model_name,
                                                 headers=headers,
                                                 config=config,
                                                 files=files)
        except Exception as e:
            raise TritonClientException('Failed to load model: {}'.format(e)) from None

    async def repository_model_unload(self, model_name, headers=None, unload_dependents=False):
        """
        unload model
        :param model_name:
        :param headers:
        :param unload_dependents:
        :return:
        """
        try:
            return await self._client.unload_model(model_name=model_name,
                                                   headers=headers,
                                                   unload_dependents=unload_dependents)
        except Exception as e:
            raise TritonClientException('Failed to unload model: {}'.format(e)) from None

    async def system_shared_memory_status(self, region_name="", headers=None):
        """
        get system shared memory status
        :param region_name:
        :param headers:
        :return:
        """
        try:
            return await self._client.get_system_shared_memory_status(region_name=region_name, headers=headers,
                                                                      as_json=True)
        except Exception as e:
            raise TritonClientException('Failed to get system shared memory status: {}'.format(e)) from None

    async def system_shared_memory_register(self, name, key, byte_size, offset=0, headers=None):
        """
        register system shared memory
        :param name:
        :param key:
        :param byte_size:
        :param offset:
        :param headers:
        :return:
        """
        try:
            return await self._client.register_system_shared_memory(name=name,
                                                                    key=key,
                                                                    byte_size=byte_size,
                                                                    offset=offset,
                                                                    headers=headers)
        except Exception as e:
            raise TritonClientException('Failed to register system shared memory: {}'.format(e)) from None

    async def system_shared_memory_unregister(self, name, headers=None):
        """
        unregister system shared memory
        :param name:
        :param headers:
        :return:
        """
        try:
            return await self._client.unregister_system_shared_memory(name=name,
                                                                      headers=headers)

        except Exception as e:
            raise TritonClientException('Failed to unregister system shared memory: {}'.format(e)) from None

    async def cuda_shared_memory_status(self, region_name="", headers=None):
        """
        get cuda shared memory status
        :param region_name:
        :param headers:
        :return:
        """
        try:
            return await self._client.get_cuda_shared_memory_status(region_name=region_name,
                                                                    headers=headers,
                                                                    as_json=True)
        except Exception as e:
            raise TritonClientException('Failed to get cuda shared memory status: {}'.format(e)) from None

    async def cuda_shared_memory_register(self, name, raw_handle, byte_size, device_id, headers=None):
        """
        register cuda shared memory
        :param name:
        :param raw_handle:
        :param byte_size:
        :param device_id:
        :param headers:
        :return:
        """
        try:
            return await self._client.register_cuda_shared_memory(name=name,
                                                                  raw_handle=raw_handle,
                                                                  device_id=device_id,
                                                                  byte_size=byte_size,
                                                                  headers=headers)

        except Exception as e:
            raise TritonClientException('Failed to register cuda shared memory: {}'.format(e)) from None

    async def cuda_shared_memory_unregister(self, name, headers=None):
        """
        unregister cuda shared memory
        :param name:
        :param headers:
        :return:
        """
        try:
            return await self._client.unregister_cuda_shared_memory(name=name,
                                                                    headers=headers)
        except Exception as e:
            raise TritonClientException('Failed to  unregister cuda shared memory: {}'.format(e)) from None

    async def trace_setting(self, model_name="", settings=None, headers=None):
        """
        update trace setting
        :param model_name:
        :param settings:
        :param headers:
        :return:
        """
        try:
            if settings is None:
                settings = {}
            return await self._client.update_trace_settings(model_name=model_name,
                                                            settings=settings,
                                                            headers=headers)
        except Exception as e:
            raise TritonClientException('Failed to update trace setting: {}'.format(e)) from None

    async def get_trace_settings(self, model_name="", headers=None):
        """
        get_trace_settings
        :param model_name:
        :param headers:
        :return:
        """
        try:
            return await self._client.get_trace_settings(model_name=model_name,
                                                         headers=headers,
                                                         as_json=True)
        except Exception as e:
            raise TritonClientException('Failed to get trace settings: {}'.format(e)) from None

    async def stream_infer(self,
                           inputs_iterator,
                           stream_timeout=None,
                           headers=None,
                           compression_algorithm=None):
        """
        stream infer
        :param inputs_iterator:
        :param stream_timeout:
        :param headers:
        :param compression_algorithm:
        :return:
        """
        try:
            return await self._client.stream_infer(inputs_iterator=inputs_iterator,
                                                   stream_timeout=stream_timeout,
                                                   headers=headers,
                                                   compression_algorithm=compression_algorithm)
        except Exception as e:
            raise TritonClientException('Failed to stream infer: {}'.format(e)) from None

    async def model_infer(self,
                          model_name,
                          inputs,
                          model_version="",
                          outputs=None,
                          request_id="",
                          sequence_id=0,
                          sequence_start=False,
                          sequence_end=False,
                          priority=0,
                          timeout=None,
                          client_timeout=None,
                          headers=None,
                          compression_algorithm=None
                          ):
        """
        model infer
        :param model_name:
        :param inputs:
        :param model_version:
        :param outputs:
        :param request_id:
        :param sequence_id:
        :param sequence_start:
        :param sequence_end:
        :param priority:
        :param timeout:
        :param client_timeout:
        :param headers:
        :param compression_algorithm:
        :return:
        """
        try:
            return await self._client.infer(model_name,
                                            inputs,
                                            model_version=model_version,
                                            outputs=outputs,
                                            request_id=request_id,
                                            sequence_id=sequence_id,
                                            sequence_start=sequence_start,
                                            sequence_end=sequence_end,
                                            priority=priority,
                                            timeout=timeout,
                                            client_timeout=client_timeout,
                                            headers=headers,
                                            compression_algorithm=compression_algorithm)
        except Exception as e:
            raise TritonClientException('Failed to model infer: {}'.format(e)) from None

    async def get_inputs_and_outputs_detail(self, model_name, model_version):
        """
        get inputs and outputs detail
        :param model_name:
        :param model_version:
        :return:
        """
        try:
            model_meta = await self.model_meta(model_name, model_version)
            model_config = await self.model_config(model_name, model_version)
            return parse_model(model_meta, model_config)
        except Exception as e:
            raise TritonClientException('Failed to get inputs and outputs detail: {}'.format(e)) from None
