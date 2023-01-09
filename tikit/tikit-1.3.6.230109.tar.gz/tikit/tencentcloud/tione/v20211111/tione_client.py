# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tikit.tencentcloud.common.abstract_client import AbstractClient
from tikit.tencentcloud.tione.v20211111 import models


class TioneClient(AbstractClient):
    _apiVersion = '2021-11-11'
    _endpoint = 'tione.tencentcloudapi.com'
    _service = 'tione'


    def AddTencentLabWhitelist(self, request):
        """为腾学会上课的子用户添加白名单接口，仅供制定腾学会运营账号调用

        :param request: Request instance for AddTencentLabWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddTencentLabWhitelist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddTencentLabWhitelistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def AddTencentLabWhitelistTest(self, request):
        """为腾学会上课的子用户添加白名单接口，仅供制定腾学会运营账号调用，仅测试使用

        :param request: Request instance for AddTencentLabWhitelistTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.AddTencentLabWhitelistTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("AddTencentLabWhitelistTest", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AddTencentLabWhitelistTestResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckAutoMLTaskNameExist(self, request):
        """自动学习任务名称重名校验

        :param request: Request instance for CheckAutoMLTaskNameExist.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckAutoMLTaskNameExistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckAutoMLTaskNameExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckAutoMLTaskNameExist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckAutoMLTaskNameExistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckBillingOwnUin(self, request):
        """判断主账号是否是云梯在用账号

        :param request: Request instance for CheckBillingOwnUin.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckBillingOwnUinRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckBillingOwnUinResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckBillingOwnUin", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckBillingOwnUinResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckBillingWhitelist(self, request):
        """判断用户是否为白名单用户

        :param request: Request instance for CheckBillingWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckBillingWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckBillingWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckBillingWhitelist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckBillingWhitelistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckDatasetName(self, request):
        """数据集重名校验

        :param request: Request instance for CheckDatasetName.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckDatasetNameRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckDatasetNameResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckDatasetName", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckDatasetNameResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CheckModelAccTaskNameExist(self, request):
        """校验模型加速任务重名

        :param request: Request instance for CheckModelAccTaskNameExist.
        :type request: :class:`tencentcloud.tione.v20211111.models.CheckModelAccTaskNameExistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CheckModelAccTaskNameExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CheckModelAccTaskNameExist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CheckModelAccTaskNameExistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAnnotateTask(self, request):
        """创建任务

        :param request: Request instance for CreateAnnotateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAnnotateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAnnotateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAnnotateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAnnotateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAnnotationKey(self, request):
        """【OCR】 新建key名字典元素

        :param request: Request instance for CreateAnnotationKey.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAnnotationKeyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAnnotationKeyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAnnotationKey", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAnnotationKeyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAutoMLEMSTask(self, request):
        """创建自动学习模型服务发布任务

        :param request: Request instance for CreateAutoMLEMSTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLEMSTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLEMSTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAutoMLEMSTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAutoMLEMSTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAutoMLTask(self, request):
        """创建自动学习任务

        :param request: Request instance for CreateAutoMLTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAutoMLTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAutoMLTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateAutoMLTaskEvaluationConfusionMatrixUrl(self, request):
        """生成混淆矩阵下载链接

        :param request: Request instance for CreateAutoMLTaskEvaluationConfusionMatrixUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskEvaluationConfusionMatrixUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateAutoMLTaskEvaluationConfusionMatrixUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateAutoMLTaskEvaluationConfusionMatrixUrl", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateAutoMLTaskEvaluationConfusionMatrixUrlResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateBatchModelAccTasks(self, request):
        """批量创建模型加速任务

        :param request: Request instance for CreateBatchModelAccTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBatchModelAccTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBatchModelAccTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBatchModelAccTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateBatchModelAccTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateBatchTask(self, request):
        """创建跑批任务

        :param request: Request instance for CreateBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBatchTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateBillingResourceGroup(self, request):
        """创建资源组

        :param request: Request instance for CreateBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateBillingResourceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateBillingResourceInstance(self, request):
        """真实下单购买节点请至控制台！
        此接口仅用于校验子账号添加资源组节点资格(CAM鉴权)；
        支持场景(资源组添加节点);


        :param request: Request instance for CreateBillingResourceInstance.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceInstanceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateBillingResourceInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateBillingResourceInstance", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateBillingResourceInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCodeRepo(self, request):
        """创建代码仓库

        :param request: Request instance for CreateCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateCodeRepo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCodeRepoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDataset(self, request):
        """创建数据集

        :param request: Request instance for CreateDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDataset", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDatasetResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDatasetDetailText(self, request):
        """开启文本数据集详情

        :param request: Request instance for CreateDatasetDetailText.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDatasetDetailTextRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDatasetDetailTextResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDatasetDetailText", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDatasetDetailTextResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDatasetTextAnalyze(self, request):
        """开启文本数据透视

        :param request: Request instance for CreateDatasetTextAnalyze.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDatasetTextAnalyzeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDatasetTextAnalyzeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDatasetTextAnalyze", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDatasetTextAnalyzeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateDemoWhite(self, request):
        """动手实验室体验白名单

        :param request: Request instance for CreateDemoWhite.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateDemoWhiteRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateDemoWhiteResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateDemoWhite", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateDemoWhiteResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateExportAutoMLSDKTask(self, request):
        """创建自动学习模型导出SDK任务

        :param request: Request instance for CreateExportAutoMLSDKTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateExportAutoMLSDKTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateExportAutoMLSDKTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateExportAutoMLSDKTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateExportAutoMLSDKTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateInferGateway(self, request):
        """创建独立部署的推理服务用专享网关

        :param request: Request instance for CreateInferGateway.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateInferGatewayRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateInferGatewayResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateInferGateway", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateInferGatewayResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateLifecycleScript(self, request):
        """创建生命周期脚本

        :param request: Request instance for CreateLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateLifecycleScript", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateLifecycleScriptResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateModelAccelerateTask(self, request):
        """创建模型加速任务

        :param request: Request instance for CreateModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateModelService(self, request):
        """用于创建、发布一个新的模型服务

        :param request: Request instance for CreateModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateModelService", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateNotebook(self, request):
        """创建Notebook

        :param request: Request instance for CreateNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateNotebook", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateNotebookResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateOptimizedModel(self, request):
        """保存优化模型

        :param request: Request instance for CreateOptimizedModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateOptimizedModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateOptimizedModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateOptimizedModel", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateOptimizedModelResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreatePreSignedTensorBoardUrl(self, request):
        """创建TensorBoard授权Url

        :param request: Request instance for CreatePreSignedTensorBoardUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreatePreSignedTensorBoardUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreatePreSignedTensorBoardUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreatePreSignedTensorBoardUrl", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreatePreSignedTensorBoardUrlResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreatePresignedNotebookUrl(self, request):
        """生成Notebook访问链接

        :param request: Request instance for CreatePresignedNotebookUrl.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreatePresignedNotebookUrlRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreatePresignedNotebookUrlResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreatePresignedNotebookUrl", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreatePresignedNotebookUrlResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTensorBoardTask(self, request):
        """创建TensorBoard任务

        :param request: Request instance for CreateTensorBoardTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTensorBoardTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTensorBoardTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTensorBoardTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTensorBoardTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTrainingModel(self, request):
        """导入模型

        :param request: Request instance for CreateTrainingModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTrainingModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTrainingModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTrainingModel", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTrainingModelResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTrainingTask(self, request):
        """创建模型训练任务

        :param request: Request instance for CreateTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.CreateTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.CreateTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("CreateTrainingTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteAnnotatedTask(self, request):
        """本接口(DeleteAnnotatedTask)用于删除标注任务

        :param request: Request instance for DeleteAnnotatedTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAnnotatedTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAnnotatedTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAnnotatedTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAnnotatedTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteAutoMLNLPPredictRecord(self, request):
        """删除文本分类预测记录

        :param request: Request instance for DeleteAutoMLNLPPredictRecord.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLNLPPredictRecordRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLNLPPredictRecordResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAutoMLNLPPredictRecord", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAutoMLNLPPredictRecordResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteAutoMLTask(self, request):
        """删除自动学习任务

        :param request: Request instance for DeleteAutoMLTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteAutoMLTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteAutoMLTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteAutoMLTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteBatchTask(self, request):
        """删除跑批任务

        :param request: Request instance for DeleteBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteBatchTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteBillingResourceGroup(self, request):
        """删除资源组，支持场景：资源组下节点不存在部署中，运行中，释放中状态

        :param request: Request instance for DeleteBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteBillingResourceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteBillingResourceInstance(self, request):
        """删除资源组节点；支持场景：部署失败和已释放节点

        :param request: Request instance for DeleteBillingResourceInstance.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceInstanceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteBillingResourceInstanceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteBillingResourceInstance", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteBillingResourceInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCodeRepo(self, request):
        """删除代码仓库

        :param request: Request instance for DeleteCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteCodeRepo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCodeRepoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteDataset(self, request):
        """删除数据集

        :param request: Request instance for DeleteDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteDataset", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteDatasetResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteInferGateway(self, request):
        """删除推理服务使用的独立部署的专享网关及对应的

        :param request: Request instance for DeleteInferGateway.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteInferGatewayRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteInferGatewayResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteInferGateway", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteInferGatewayResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteLifecycleScript(self, request):
        """删除生命周期脚本

        :param request: Request instance for DeleteLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteLifecycleScript", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteLifecycleScriptResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteModelAccelerateTask(self, request):
        """删除模型加速任务

        :param request: Request instance for DeleteModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteModelService(self, request):
        """根据服务id删除模型服务

        :param request: Request instance for DeleteModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelService", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteModelServiceGroup(self, request):
        """根据服务组id删除服务组下所有模型服务

        :param request: Request instance for DeleteModelServiceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteModelServiceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteModelServiceGroup", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteModelServiceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteNotebook(self, request):
        """删除Notebook

        :param request: Request instance for DeleteNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteNotebook", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteNotebookResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTaskProcess(self, request):
        """删除任务进度

        :param request: Request instance for DeleteTaskProcess.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTaskProcessRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTaskProcessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTaskProcess", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTaskProcessResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTencentLabWhitelist(self, request):
        """为腾学会上课的子用户删除上课的子用户的白名单和资源的接口，仅供制定腾学会运营账号调用

        :param request: Request instance for DeleteTencentLabWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTencentLabWhitelist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTencentLabWhitelistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTencentLabWhitelistTest(self, request):
        """为腾学会上课的子用户删除上课的子用户的白名单和资源的接口，仅供制定腾学会运营账号调用，仅测试使用

        :param request: Request instance for DeleteTencentLabWhitelistTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTencentLabWhitelistTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTencentLabWhitelistTest", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTencentLabWhitelistTestResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingMetrics(self, request):
        """删除训练自定义指标

        :param request: Request instance for DeleteTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingModel(self, request):
        """删除模型

        :param request: Request instance for DeleteTrainingModel.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingModel", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingModelResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingModelVersion(self, request):
        """删除模型版本

        :param request: Request instance for DeleteTrainingModelVersion.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelVersionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingModelVersionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingModelVersion", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingModelVersionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTrainingTask(self, request):
        """删除训练任务

        :param request: Request instance for DeleteTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeleteTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeleteTrainingTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeliverBillingResource(self, request):
        """续费资源组节点

        :param request: Request instance for DeliverBillingResource.
        :type request: :class:`tencentcloud.tione.v20211111.models.DeliverBillingResourceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DeliverBillingResourceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DeliverBillingResource", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeliverBillingResourceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAPIConfigs(self, request):
        """列举API

        :param request: Request instance for DescribeAPIConfigs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAPIConfigsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAPIConfigsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAPIConfigs", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAPIConfigsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAnnotatedTaskList(self, request):
        """本接口（DescribeAnnotatedTaskList）用于查询用户标注任务详细信息列表；支持各种过滤条件；

        :param request: Request instance for DescribeAnnotatedTaskList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotatedTaskListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotatedTaskListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotatedTaskList", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAnnotatedTaskListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAnnotationKeys(self, request):
        """【OCR】查询数据集下的key名字典详情

        :param request: Request instance for DescribeAnnotationKeys.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotationKeysRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAnnotationKeysResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAnnotationKeys", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAnnotationKeysResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLEMSAPIInfo(self, request):
        """查询自动学习发布模型服务接口调用信息

        :param request: Request instance for DescribeAutoMLEMSAPIInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSAPIInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSAPIInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSAPIInfo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLEMSAPIInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLEMSTask(self, request):
        """查询自动学习发布模型服务任务详情

        :param request: Request instance for DescribeAutoMLEMSTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLEMSTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLEMSTasks(self, request):
        """查询自动学习模型服务任务列表

        :param request: Request instance for DescribeAutoMLEMSTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLEMSTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLEMSTasksTrainLabels(self, request):
        """获取当前发布任务所用到的训练集kv

        :param request: Request instance for DescribeAutoMLEMSTasksTrainLabels.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksTrainLabelsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEMSTasksTrainLabelsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEMSTasksTrainLabels", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLEMSTasksTrainLabelsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLEvaluationTaskStatus(self, request):
        """查询自动学习评测任务状态

        :param request: Request instance for DescribeAutoMLEvaluationTaskStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTaskStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTaskStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEvaluationTaskStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLEvaluationTaskStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLEvaluationTasks(self, request):
        """查询自动学习评测任务列表信息

        :param request: Request instance for DescribeAutoMLEvaluationTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLEvaluationTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLEvaluationTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLEvaluationTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLModelServiceInfo(self, request):
        """获取EMS正式发布所需信息

        :param request: Request instance for DescribeAutoMLModelServiceInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLModelServiceInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLModelServiceInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLModelServiceInfo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLModelServiceInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLNLPPredictRecords(self, request):
        """查询自动学习文本分类推理记录列表

        :param request: Request instance for DescribeAutoMLNLPPredictRecords.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLNLPPredictRecordsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLNLPPredictRecordsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLNLPPredictRecords", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLNLPPredictRecordsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskConfig(self, request):
        """查询自动学习任务配置

        :param request: Request instance for DescribeAutoMLTaskConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskEvaluationBadcases(self, request):
        """查询自动学习评测任务badcase详情

        :param request: Request instance for DescribeAutoMLTaskEvaluationBadcases.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBadcasesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBadcasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationBadcases", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskEvaluationBadcasesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskEvaluationBaseIndicators(self, request):
        """查询自动学习评测结果基础指标

        :param request: Request instance for DescribeAutoMLTaskEvaluationBaseIndicators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBaseIndicatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationBaseIndicatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationBaseIndicators", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskEvaluationBaseIndicatorsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskEvaluationDetail(self, request):
        """查询自动学习评测任务基本详情

        :param request: Request instance for DescribeAutoMLTaskEvaluationDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationDetail", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskEvaluationDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskEvaluationSeniorIndicators(self, request):
        """查询自动学习评测任务高阶指标信息

        :param request: Request instance for DescribeAutoMLTaskEvaluationSeniorIndicators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationSeniorIndicatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskEvaluationSeniorIndicatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskEvaluationSeniorIndicators", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskEvaluationSeniorIndicatorsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskNLPEvaluationBadcases(self, request):
        """查询自动学习NLP评测任务badcase详情

        :param request: Request instance for DescribeAutoMLTaskNLPEvaluationBadcases.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLPEvaluationBadcasesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskNLPEvaluationBadcasesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskNLPEvaluationBadcases", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskNLPEvaluationBadcasesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskTrainDetail(self, request):
        """查询训练任务详情

        :param request: Request instance for DescribeAutoMLTaskTrainDetail.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainDetailRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainDetailResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskTrainDetail", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskTrainDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTaskTrainIndicators(self, request):
        """查询训练任务指标

        :param request: Request instance for DescribeAutoMLTaskTrainIndicators.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainIndicatorsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTaskTrainIndicatorsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTaskTrainIndicators", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTaskTrainIndicatorsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoMLTrainTasks(self, request):
        """列举自动学习训练任务组列表

        :param request: Request instance for DescribeAutoMLTrainTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTrainTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoMLTrainTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoMLTrainTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoMLTrainTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeAutoOcrPrediction(self, request):
        """自动文字识别预测

        :param request: Request instance for DescribeAutoOcrPrediction.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeAutoOcrPredictionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeAutoOcrPredictionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeAutoOcrPrediction", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeAutoOcrPredictionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBadcasePreviewStatus(self, request):
        """查询自动学习badcase图片预览设置状态

        :param request: Request instance for DescribeBadcasePreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBadcasePreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBadcasePreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBadcasePreviewStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBadcasePreviewStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBatchTask(self, request):
        """查询跑批任务

        :param request: Request instance for DescribeBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBatchTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBatchTaskInstances(self, request):
        """查询跑批实例列表

        :param request: Request instance for DescribeBatchTaskInstances.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskInstancesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTaskInstancesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBatchTaskInstances", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchTaskInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBatchTasks(self, request):
        """批量预测任务列表信息

        :param request: Request instance for DescribeBatchTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBatchTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBatchTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBatchTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingResourceGroup(self, request):
        """查询资源组节点列表

        :param request: Request instance for DescribeBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingResourceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingResourceGroups(self, request):
        """查询资源组详情

        :param request: Request instance for DescribeBillingResourceGroups.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceGroups", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingResourceGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingResourceInstanceStatusStatistic(self, request):
        """查询资源组节点状态统计

        :param request: Request instance for DescribeBillingResourceInstanceStatusStatistic.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceStatusStatisticRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingResourceInstanceStatusStatisticResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingResourceInstanceStatusStatistic", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingResourceInstanceStatusStatisticResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingSpecs(self, request):
        """本接口(DescribeBillingSpecs)用于查询计费项列表

        :param request: Request instance for DescribeBillingSpecs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingSpecs", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingSpecsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingSpecsPrice(self, request):
        """本接口(DescribeBillingSpecsPrice)用于查询计费项价格。

        :param request: Request instance for DescribeBillingSpecsPrice.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsPriceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingSpecsPriceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingSpecsPrice", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingSpecsPriceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBillingUserList(self, request):
        """本接口(DescribeBillingUserList)查询并返回指定用户列表

        :param request: Request instance for DescribeBillingUserList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeBillingUserListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeBillingUserListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeBillingUserList", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBillingUserListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCodeRepo(self, request):
        """代码仓库详情

        :param request: Request instance for DescribeCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCodeRepo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCodeRepoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCodeRepos(self, request):
        """代码仓库列表

        :param request: Request instance for DescribeCodeRepos.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeCodeReposRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeCodeReposResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeCodeRepos", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCodeReposResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeContentByMD5(self, request):
        """根据MD5查询文本内容

        :param request: Request instance for DescribeContentByMD5.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeContentByMD5Request`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeContentByMD5Response`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeContentByMD5", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeContentByMD5Response()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDetailStructured(self, request):
        """查询结构化数据集详情

        :param request: Request instance for DescribeDatasetDetailStructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailStructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailStructured", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDetailStructuredResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDetailText(self, request):
        """查询文本数据集详情

        :param request: Request instance for DescribeDatasetDetailText.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailTextRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailTextResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailText", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDetailTextResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDetailUnstructured(self, request):
        """查询非结构化数据集详情

        :param request: Request instance for DescribeDatasetDetailUnstructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailUnstructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDetailUnstructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDetailUnstructured", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDetailUnstructuredResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDistributionStructured(self, request):
        """查询表格类数据集字段分布统计

        :param request: Request instance for DescribeDatasetDistributionStructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionStructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionStructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDistributionStructured", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDistributionStructuredResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetDistributionUnstructured(self, request):
        """查询非结构化标签分布详情

        :param request: Request instance for DescribeDatasetDistributionUnstructured.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionUnstructuredRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetDistributionUnstructuredResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetDistributionUnstructured", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetDistributionUnstructuredResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetFileList(self, request):
        """查询数据集文件列表详情

        :param request: Request instance for DescribeDatasetFileList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetFileListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetFileListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetFileList", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetFileListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetImageUrls(self, request):
        """查询数据集图片下载链接

        :param request: Request instance for DescribeDatasetImageUrls.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetImageUrlsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetImageUrlsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetImageUrls", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetImageUrlsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetOcrScene(self, request):
        """查询OCR场景数据集的标签子类别

        :param request: Request instance for DescribeDatasetOcrScene.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetOcrSceneRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetOcrSceneResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetOcrScene", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetOcrSceneResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetPerspectiveStatus(self, request):
        """查询文本数据集数据透视预览状态

        :param request: Request instance for DescribeDatasetPerspectiveStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPerspectiveStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPerspectiveStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetPerspectiveStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetPerspectiveStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetPreviewStatus(self, request):
        """查询数据集预览状态

        :param request: Request instance for DescribeDatasetPreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetPreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetPreviewStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetPreviewStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetSchema(self, request):
        """查询表格数据集头信息

        :param request: Request instance for DescribeDatasetSchema.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetSchemaResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetSchema", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetSchemaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasetTextAnalyze(self, request):
        """查询文本数据透视

        :param request: Request instance for DescribeDatasetTextAnalyze.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetTextAnalyzeRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetTextAnalyzeResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasetTextAnalyze", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetTextAnalyzeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeDatasets(self, request):
        """查询数据集列表

        :param request: Request instance for DescribeDatasets.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeDatasetsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeDatasets", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeDatasetsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeEvents(self, request):
        """获取训练，Notebook，推理服务的事件

        :param request: Request instance for DescribeEvents.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeEventsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeEventsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeEvents", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeEventsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeFixedPoint(self, request):
        """本接口(DescribeFixedPoint)用于获取固定点数

        :param request: Request instance for DescribeFixedPoint.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeFixedPointRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeFixedPointResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeFixedPoint", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeFixedPointResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeImagesInfo(self, request):
        """本接口(DescribeImagesInfo)用于获取图片及信息

        :param request: Request instance for DescribeImagesInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeImagesInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeImagesInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeImagesInfo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeImagesInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInferGatewayStatus(self, request):
        """查询推理专项网关的运行状态

        :param request: Request instance for DescribeInferGatewayStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInferGatewayStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInferGatewayStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInferGatewayStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInferGatewayStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInferTemplates(self, request):
        """查询推理镜像模板

        :param request: Request instance for DescribeInferTemplates.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInferTemplatesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInferTemplatesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInferTemplates", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInferTemplatesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInsideAction(self, request):
        """调用内网服务接口

        :param request: Request instance for DescribeInsideAction.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInsideActionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInsideActionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInsideAction", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInsideActionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeInstanceCredential(self, request):
        """获取实例内用户临时秘钥

        :param request: Request instance for DescribeInstanceCredential.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeInstanceCredentialRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeInstanceCredentialResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeInstanceCredential", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeInstanceCredentialResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeIsTaskNameExist(self, request):
        """本接口(DescribeIsTaskNameExist)用来查询新建标注任务时的名称是否重复

        :param request: Request instance for DescribeIsTaskNameExist.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeIsTaskNameExistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeIsTaskNameExistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeIsTaskNameExist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeIsTaskNameExistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLabelColor(self, request):
        """本接口(DescribeLabelColor)用于获取标签颜色

        :param request: Request instance for DescribeLabelColor.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLabelColorRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLabelColorResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLabelColor", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLabelColorResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLatestTrainingMetrics(self, request):
        """查询最近上报的训练自定义指标

        :param request: Request instance for DescribeLatestTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLatestTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLatestTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLatestTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLatestTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLifecycleScript(self, request):
        """查看生命周期脚本详情

        :param request: Request instance for DescribeLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLifecycleScript", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLifecycleScriptResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLifecycleScripts(self, request):
        """查看生命周期脚本列表

        :param request: Request instance for DescribeLifecycleScripts.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLifecycleScriptsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLifecycleScripts", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLifecycleScriptsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeLogs(self, request):
        """获取训练、推理、Notebook服务的日志

        :param request: Request instance for DescribeLogs.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeLogsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeLogsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeLogs", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeLogsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelAccEngineVersions(self, request):
        """查询模型加速引擎版本列表

        :param request: Request instance for DescribeModelAccEngineVersions.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccEngineVersionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccEngineVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccEngineVersions", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelAccEngineVersionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelAccOptimizedReport(self, request):
        """查询模型加速优化报告

        :param request: Request instance for DescribeModelAccOptimizedReport.
        :type request: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelAccOptimizedReportRequest`
        :rtype: :class:`tikit.tencentcloud.tione.v20211111.models.DescribeModelAccOptimizedReportResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccOptimizedReport", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelAccOptimizedReportResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelAccelerateTask(self, request):
        """查询模型优化任务详情

        :param request: Request instance for DescribeModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelAccelerateTasks(self, request):
        """查询模型加速任务列表

        :param request: Request instance for DescribeModelAccelerateTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccelerateTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelAccelerateTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelAccelerateVersions(self, request):
        """模型加速之后的模型版本列表

        :param request: Request instance for DescribeModelAccelerateVersions.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateVersionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelAccelerateVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelAccelerateVersions", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelAccelerateVersionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelService(self, request):
        """查询单个服务

        :param request: Request instance for DescribeModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelService", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceCallInfo(self, request):
        """展示服务的调用信息

        :param request: Request instance for DescribeModelServiceCallInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceCallInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceCallInfo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceCallInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceGroup(self, request):
        """查询单个服务组

        :param request: Request instance for DescribeModelServiceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceGroup", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceGroups(self, request):
        """列举在线推理服务组

        :param request: Request instance for DescribeModelServiceGroups.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceGroupsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceGroups", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceHistory(self, request):
        """展示服务的历史版本

        :param request: Request instance for DescribeModelServiceHistory.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHistoryRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHistoryResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceHistory", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceHistoryResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceHotUpdated(self, request):
        """用于查询模型服务能否开启热更新

        :param request: Request instance for DescribeModelServiceHotUpdated.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHotUpdatedRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceHotUpdatedResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceHotUpdated", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceHotUpdatedResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServiceUserInfo(self, request):
        """内部接口，用于查询部分白名单用户的特殊配额信息

        :param request: Request instance for DescribeModelServiceUserInfo.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceUserInfoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServiceUserInfoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServiceUserInfo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServiceUserInfoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeModelServices(self, request):
        """查询多个服务

        :param request: Request instance for DescribeModelServices.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeModelServicesRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeModelServicesResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeModelServices", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeModelServicesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeMonitorData(self, request):
        """查询监控数据

        :param request: Request instance for DescribeMonitorData.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeMonitorDataRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeMonitorDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeMonitorData", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeMonitorDataResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNLPDatasetContent(self, request):
        """根据datasetid和MD5获取文本内容

        :param request: Request instance for DescribeNLPDatasetContent.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNLPDatasetContentRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNLPDatasetContentResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNLPDatasetContent", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNLPDatasetContentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebook(self, request):
        """Notebook详情

        :param request: Request instance for DescribeNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebook", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNotebookResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebookStorageQuota(self, request):
        """获取notebook白名单存储配额

        :param request: Request instance for DescribeNotebookStorageQuota.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookStorageQuotaRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebookStorageQuotaResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebookStorageQuota", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNotebookStorageQuotaResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNotebooks(self, request):
        """Notebook列表

        :param request: Request instance for DescribeNotebooks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeNotebooksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeNotebooksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeNotebooks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNotebooksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSceneList(self, request):
        """获取自动学习场景列表

        :param request: Request instance for DescribeSceneList.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeSceneListRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeSceneListResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeSceneList", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSceneListResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTaskDisplayConfig(self, request):
        """本接口(DescribeTaskDisplayConfig)获取标注显示配置

        :param request: Request instance for DescribeTaskDisplayConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskDisplayConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskDisplayConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskDisplayConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTaskDisplayConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTaskProcess(self, request):
        """查询任务的进度

        :param request: Request instance for DescribeTaskProcess.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTaskProcessRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTaskProcessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTaskProcess", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTaskProcessResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTensorBoardTask(self, request):
        """TensorBoard任务详情

        :param request: Request instance for DescribeTensorBoardTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTensorBoardTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTensorBoardTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTensorBoardTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTensorBoardTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingFrameworks(self, request):
        """训练框架列表

        :param request: Request instance for DescribeTrainingFrameworks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingFrameworksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingFrameworks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingFrameworksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingMetrics(self, request):
        """查询训练自定义指标

        :param request: Request instance for DescribeTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingModelVersion(self, request):
        """查询模型版本

        :param request: Request instance for DescribeTrainingModelVersion.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingModelVersion", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingModelVersionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingModelVersions(self, request):
        """模型版本列表

        :param request: Request instance for DescribeTrainingModelVersions.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelVersionsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingModelVersions", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingModelVersionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingModels(self, request):
        """模型列表

        :param request: Request instance for DescribeTrainingModels.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingModelsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingModels", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingModelsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingTask(self, request):
        """训练任务详情

        :param request: Request instance for DescribeTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingTaskPods(self, request):
        """训练任务pod列表

        :param request: Request instance for DescribeTrainingTaskPods.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTaskPodsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTaskPods", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingTaskPodsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTrainingTasks(self, request):
        """训练任务列表

        :param request: Request instance for DescribeTrainingTasks.
        :type request: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTasksRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DescribeTrainingTasksResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DescribeTrainingTasks", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTrainingTasksResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DestroyBillingResource(self, request):
        """释放资源组节点; 适用场景：运行中和异常状态的节点

        :param request: Request instance for DestroyBillingResource.
        :type request: :class:`tencentcloud.tione.v20211111.models.DestroyBillingResourceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DestroyBillingResourceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DestroyBillingResource", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DestroyBillingResourceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DownloadTrainingMetrics(self, request):
        """下载训练自定义指标

        :param request: Request instance for DownloadTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.DownloadTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.DownloadTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("DownloadTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DownloadTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def EnableBatchTaskClsConfig(self, request):
        """开启或者关闭跑批任务 CLS日志投递

        :param request: Request instance for EnableBatchTaskClsConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.EnableBatchTaskClsConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.EnableBatchTaskClsConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("EnableBatchTaskClsConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.EnableBatchTaskClsConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def EnableNotebookClsConfig(self, request):
        """开启或者关闭Notebook CLS日志投递

        :param request: Request instance for EnableNotebookClsConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.EnableNotebookClsConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.EnableNotebookClsConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("EnableNotebookClsConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.EnableNotebookClsConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def EnableTrainingTaskClsConfig(self, request):
        """开启CLS日志投递

        :param request: Request instance for EnableTrainingTaskClsConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.EnableTrainingTaskClsConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.EnableTrainingTaskClsConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("EnableTrainingTaskClsConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.EnableTrainingTaskClsConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InferEMSProxy(self, request):
        """在线服务请求代理

        :param request: Request instance for InferEMSProxy.
        :type request: :class:`tencentcloud.tione.v20211111.models.InferEMSProxyRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.InferEMSProxyResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InferEMSProxy", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InferEMSProxyResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def InterfaceCallTest(self, request):
        """测试用户的接口调用

        :param request: Request instance for InterfaceCallTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.InterfaceCallTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.InterfaceCallTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("InterfaceCallTest", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.InterfaceCallTestResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAnnotateTaskReopen(self, request):
        """重新打开标注

        :param request: Request instance for ModifyAnnotateTaskReopen.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskReopenRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskReopenResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotateTaskReopen", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAnnotateTaskReopenResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAnnotateTaskTags(self, request):
        """本接口(ModifyTaskTags)用于更新任务绑定的标签

        :param request: Request instance for ModifyAnnotateTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotateTaskTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAnnotateTaskTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAnnotateTaskToSubmit(self, request):
        """提交标注任务结果

        :param request: Request instance for ModifyAnnotateTaskToSubmit.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskToSubmitRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotateTaskToSubmitResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotateTaskToSubmit", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAnnotateTaskToSubmitResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAnnotatedResult(self, request):
        """本及接口(ModifyAnnotatedResult)用于修改标注结果

        :param request: Request instance for ModifyAnnotatedResult.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotatedResultRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotatedResultResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotatedResult", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAnnotatedResultResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAnnotationKeys(self, request):
        """【OCR】 更新某数据集下的key名字典

        :param request: Request instance for ModifyAnnotationKeys.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotationKeysRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAnnotationKeysResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAnnotationKeys", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAnnotationKeysResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyAutoMLTaskTags(self, request):
        """修改自动学习任务标签

        :param request: Request instance for ModifyAutoMLTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyAutoMLTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyAutoMLTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyAutoMLTaskTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyAutoMLTaskTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyBadcasePreviewStatus(self, request):
        """修改自动学习badcase图片预览设置状态

        :param request: Request instance for ModifyBadcasePreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBadcasePreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBadcasePreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBadcasePreviewStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyBadcasePreviewStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyBatchTaskTags(self, request):
        """本接口(ModifyBatchTaskTags)用于更新跑批任务绑定的标签

        :param request: Request instance for ModifyBatchTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBatchTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBatchTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBatchTaskTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyBatchTaskTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyBillingResourceGroup(self, request):
        """更新资源组名称以及标签绑定

        :param request: Request instance for ModifyBillingResourceGroup.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyBillingResourceGroupRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyBillingResourceGroupResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyBillingResourceGroup", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyBillingResourceGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCodeRepo(self, request):
        """修改存储库

        :param request: Request instance for ModifyCodeRepo.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyCodeRepoRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyCodeRepoResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyCodeRepo", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCodeRepoResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDatasetAnnotationStatus(self, request):
        """修改数据集标注状态

        :param request: Request instance for ModifyDatasetAnnotationStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetAnnotationStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetAnnotationStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetAnnotationStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDatasetAnnotationStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDatasetPerspectiveStatus(self, request):
        """更新文本数据集数据透视预览状态

        :param request: Request instance for ModifyDatasetPerspectiveStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPerspectiveStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPerspectiveStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetPerspectiveStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDatasetPerspectiveStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDatasetPreviewStatus(self, request):
        """修改数据集预览状态

        :param request: Request instance for ModifyDatasetPreviewStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPreviewStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetPreviewStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetPreviewStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDatasetPreviewStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyDatasetTags(self, request):
        """修改数据集标签信息

        :param request: Request instance for ModifyDatasetTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyDatasetTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyDatasetTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyDatasetTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyFixedPoint(self, request):
        """本接口(ModifyFixedPoint)用于修改固定点数

        :param request: Request instance for ModifyFixedPoint.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyFixedPointRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyFixedPointResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyFixedPoint", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyFixedPointResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyLifecycleScript(self, request):
        """编辑生命周期脚本

        :param request: Request instance for ModifyLifecycleScript.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyLifecycleScriptRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyLifecycleScriptResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyLifecycleScript", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyLifecycleScriptResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyModelAccTaskTags(self, request):
        """修改模型加速任务标签

        :param request: Request instance for ModifyModelAccTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelAccTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelAccTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelAccTaskTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyModelAccTaskTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyModelService(self, request):
        """用于更新模型服务

        :param request: Request instance for ModifyModelService.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelServiceRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelServiceResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelService", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyModelServiceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyModelServicePartialConfig(self, request):
        """增量更新在线推理服务的部分配置，不更新的配置项不需要传入

        :param request: Request instance for ModifyModelServicePartialConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelServicePartialConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelServicePartialConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelServicePartialConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyModelServicePartialConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyModelTags(self, request):
        """编辑模型标签

        :param request: Request instance for ModifyModelTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyModelTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyModelTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyModelTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyModelTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyNotebook(self, request):
        """修改Notebook

        :param request: Request instance for ModifyNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyNotebook", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyNotebookResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyNotebookAutoStopping(self, request):
        """修改自动停止配置

        :param request: Request instance for ModifyNotebookAutoStopping.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookAutoStoppingRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookAutoStoppingResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyNotebookAutoStopping", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyNotebookAutoStoppingResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyNotebookTags(self, request):
        """修改Notebook标签

        :param request: Request instance for ModifyNotebookTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyNotebookTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyNotebookTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyNotebookTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyServiceGroupWeights(self, request):
        """更新推理服务组流量分配

        :param request: Request instance for ModifyServiceGroupWeights.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyServiceGroupWeightsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyServiceGroupWeights", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyServiceGroupWeightsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTags(self, request):
        """编辑模型服务的标签

        :param request: Request instance for ModifyTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTaskDisplayConfig(self, request):
        """本接口(ModifyTaskDisplayConfig)修改标注显示配置

        :param request: Request instance for ModifyTaskDisplayConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskDisplayConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskDisplayConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskDisplayConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTaskDisplayConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTaskLabelValue(self, request):
        """本接口(ModifyTaskLabelValue)修改任务标签值

        :param request: Request instance for ModifyTaskLabelValue.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskLabelValueRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskLabelValueResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskLabelValue", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTaskLabelValueResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTaskProcessingStatus(self, request):
        """本接口(ModifyTaskProcessingStatus)修改标注任务处理状态

        :param request: Request instance for ModifyTaskProcessingStatus.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskProcessingStatusRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskProcessingStatusResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskProcessingStatus", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTaskProcessingStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTaskTags(self, request):
        """本接口(ModifyTaskTags)用于更新任务绑定的标签

        :param request: Request instance for ModifyTaskTags.
        :type request: :class:`tencentcloud.tione.v20211111.models.ModifyTaskTagsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.ModifyTaskTagsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("ModifyTaskTags", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTaskTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PublishDataset(self, request):
        """发布数据集

        :param request: Request instance for PublishDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.PublishDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.PublishDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("PublishDataset", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PublishDatasetResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PushTaskProcess(self, request):
        """上报任务进度

        :param request: Request instance for PushTaskProcess.
        :type request: :class:`tencentcloud.tione.v20211111.models.PushTaskProcessRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.PushTaskProcessResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("PushTaskProcess", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PushTaskProcessResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PushTrainingMetrics(self, request):
        """上报训练自定义指标

        :param request: Request instance for PushTrainingMetrics.
        :type request: :class:`tencentcloud.tione.v20211111.models.PushTrainingMetricsRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.PushTrainingMetricsResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("PushTrainingMetrics", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PushTrainingMetricsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RenewTencentLabWhitelist(self, request):
        """为腾学会上课的子用户续期白名单接口，仅供制定腾学会运营账号调用

        :param request: Request instance for RenewTencentLabWhitelist.
        :type request: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewTencentLabWhitelist", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewTencentLabWhitelistResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RenewTencentLabWhitelistTest(self, request):
        """为腾学会上课的子用户续期白名单接口，仅供制定腾学会运营账号调用，仅测试使用

        :param request: Request instance for RenewTencentLabWhitelistTest.
        :type request: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistTestRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RenewTencentLabWhitelistTestResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RenewTencentLabWhitelistTest", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RenewTencentLabWhitelistTestResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RestartAutoMLModelAccelerateTask(self, request):
        """自动学习重启模型优化任务

        :param request: Request instance for RestartAutoMLModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.RestartAutoMLModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RestartAutoMLModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartAutoMLModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RestartAutoMLModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RestartModelAccelerateTask(self, request):
        """重启模型加速任务

        :param request: Request instance for RestartModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.RestartModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.RestartModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("RestartModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RestartModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SetRenewBillingResourceFlag(self, request):
        """设置资源组节点自动续费状态

        :param request: Request instance for SetRenewBillingResourceFlag.
        :type request: :class:`tencentcloud.tione.v20211111.models.SetRenewBillingResourceFlagRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SetRenewBillingResourceFlagResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SetRenewBillingResourceFlag", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetRenewBillingResourceFlagResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StartAutoMLEvaluationTask(self, request):
        """启动自动学习评测任务

        :param request: Request instance for StartAutoMLEvaluationTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartAutoMLEvaluationTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartAutoMLEvaluationTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartAutoMLEvaluationTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StartAutoMLEvaluationTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StartAutoMLTaskTrain(self, request):
        """开始训练任务

        :param request: Request instance for StartAutoMLTaskTrain.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartAutoMLTaskTrainRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartAutoMLTaskTrainResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartAutoMLTaskTrain", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StartAutoMLTaskTrainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StartNotebook(self, request):
        """启动Notebook


        :param request: Request instance for StartNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartNotebook", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StartNotebookResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StartTrainingTask(self, request):
        """启动模型训练任务

        :param request: Request instance for StartTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StartTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StartTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StartTrainingTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StartTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopAutoMLEMSTask(self, request):
        """停止自动学习发布的模型服务

        :param request: Request instance for StopAutoMLEMSTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEMSTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEMSTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLEMSTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopAutoMLEMSTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopAutoMLEvaluationTask(self, request):
        """停止自动学习评测任务

        :param request: Request instance for StopAutoMLEvaluationTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEvaluationTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLEvaluationTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLEvaluationTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopAutoMLEvaluationTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopAutoMLModelAccelerateTask(self, request):
        """停止自动学习模型优化任务

        :param request: Request instance for StopAutoMLModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopAutoMLModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopAutoMLTaskTrain(self, request):
        """停止训练任务

        :param request: Request instance for StopAutoMLTaskTrain.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopAutoMLTaskTrainRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopAutoMLTaskTrainResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopAutoMLTaskTrain", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopAutoMLTaskTrainResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopBatchTask(self, request):
        """停止跑批任务

        :param request: Request instance for StopBatchTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopBatchTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopBatchTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopBatchTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopBatchTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopModelAccelerateTask(self, request):
        """停止模型加速任务

        :param request: Request instance for StopModelAccelerateTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopModelAccelerateTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopModelAccelerateTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopModelAccelerateTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopModelAccelerateTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopNotebook(self, request):
        """停止Notebook

        :param request: Request instance for StopNotebook.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopNotebookRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopNotebookResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopNotebook", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopNotebookResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def StopTrainingTask(self, request):
        """停止模型训练任务

        :param request: Request instance for StopTrainingTask.
        :type request: :class:`tencentcloud.tione.v20211111.models.StopTrainingTaskRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.StopTrainingTaskResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("StopTrainingTask", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.StopTrainingTaskResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SyncDataset(self, request):
        """同步数据集

        :param request: Request instance for SyncDataset.
        :type request: :class:`tencentcloud.tione.v20211111.models.SyncDatasetRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.SyncDatasetResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("SyncDataset", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SyncDatasetResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateAutoMLCLSLogConfig(self, request):
        """更新训练任务CLS日志投递

        :param request: Request instance for UpdateAutoMLCLSLogConfig.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLCLSLogConfigRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLCLSLogConfigResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateAutoMLCLSLogConfig", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateAutoMLCLSLogConfigResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UpdateAutoMLTaskConfigReq(self, request):
        """更新自动学习任务配置

        :param request: Request instance for UpdateAutoMLTaskConfigReq.
        :type request: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLTaskConfigReqRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UpdateAutoMLTaskConfigReqResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UpdateAutoMLTaskConfigReq", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UpdateAutoMLTaskConfigReqResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UploadData(self, request):
        """上传数据

        :param request: Request instance for UploadData.
        :type request: :class:`tencentcloud.tione.v20211111.models.UploadDataRequest`
        :rtype: :class:`tencentcloud.tione.v20211111.models.UploadDataResponse`

        """
        try:
            params = request._serialize()
            headers = request.headers
            body = self.call("UploadData", params, headers=headers)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UploadDataResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)