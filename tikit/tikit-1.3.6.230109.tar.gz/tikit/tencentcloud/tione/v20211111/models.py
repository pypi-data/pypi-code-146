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

import warnings

from tikit.tencentcloud.common.abstract_model import AbstractModel


class APIConfigDetail(AbstractModel):
    """接口描述信息

    """

    def __init__(self):
        r"""
        :param Id: 接口id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: str
        :param ServiceGroupId: 接口所属服务组id
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceGroupId: str
        :param Description: 接口描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Description: str
        :param RelativeUrl: 相对路径
注意：此字段可能返回 null，表示取不到有效值。
        :type RelativeUrl: str
        :param ServiceType: 服务类型 HTTP HTTPS
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceType: str
        :param HttpMethod: GET POST
注意：此字段可能返回 null，表示取不到有效值。
        :type HttpMethod: str
        :param HttpInputExample: 请求示例
注意：此字段可能返回 null，表示取不到有效值。
        :type HttpInputExample: str
        :param HttpOutputExample: 回包示例
注意：此字段可能返回 null，表示取不到有效值。
        :type HttpOutputExample: str
        :param UpdatedBy: 更新成员
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedBy: str
        :param UpdatedAt: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdatedAt: str
        :param Uin: 主账号uin
注意：此字段可能返回 null，表示取不到有效值。
        :type Uin: str
        :param SubUin: 子账号subuin
注意：此字段可能返回 null，表示取不到有效值。
        :type SubUin: str
        """
        self.Id = None
        self.ServiceGroupId = None
        self.Description = None
        self.RelativeUrl = None
        self.ServiceType = None
        self.HttpMethod = None
        self.HttpInputExample = None
        self.HttpOutputExample = None
        self.UpdatedBy = None
        self.UpdatedAt = None
        self.Uin = None
        self.SubUin = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.ServiceGroupId = params.get("ServiceGroupId")
        self.Description = params.get("Description")
        self.RelativeUrl = params.get("RelativeUrl")
        self.ServiceType = params.get("ServiceType")
        self.HttpMethod = params.get("HttpMethod")
        self.HttpInputExample = params.get("HttpInputExample")
        self.HttpOutputExample = params.get("HttpOutputExample")
        self.UpdatedBy = params.get("UpdatedBy")
        self.UpdatedAt = params.get("UpdatedAt")
        self.Uin = params.get("Uin")
        self.SubUin = params.get("SubUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddTencentLabWhitelistRequest(AbstractModel):
    """AddTencentLabWhitelist请求参数结构体

    """

    def __init__(self):
        r"""
        :param ClassUin: 需要增加白名单的主uin
        :type ClassUin: str
        :param ClassSubUin: 需要增加白名单的subUin
        :type ClassSubUin: str
        :param ResourceId: Tione 平台维护的资源 ID，对应腾学会的课程 ID
        :type ResourceId: str
        :param ExpireDurationSecond: 过期时长，以请求收到的时间向后延后 ExpireDurationSecond 计算过期时刻
        :type ExpireDurationSecond: int
        :param Description: 备注描述
        :type Description: str
        """
        self.ClassUin = None
        self.ClassSubUin = None
        self.ResourceId = None
        self.ExpireDurationSecond = None
        self.Description = None


    def _deserialize(self, params):
        self.ClassUin = params.get("ClassUin")
        self.ClassSubUin = params.get("ClassSubUin")
        self.ResourceId = params.get("ResourceId")
        self.ExpireDurationSecond = params.get("ExpireDurationSecond")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddTencentLabWhitelistResponse(AbstractModel):
    """AddTencentLabWhitelist返回参数结构体

    """

    def __init__(self):
        r"""
        :param ExtraCosSourcePathJson: json 格式。课程进行需要的额外 cos 信息。数据源路径信息。若为json 结构或空字符串则表示无额外信息。格式如下
  { 
   "bucket": string,
   "region": string,
   "paths": string array
   }
        :type ExtraCosSourcePathJson: str
        :param ExtraCosTargetPathJson: json 格式。课程进行需要的额外 cos 信息。数据目标路径信息。若为json 结构或空字符串则表示无额外信息。格式如下
   {
   "path": string
   }
        :type ExtraCosTargetPathJson: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ExtraCosSourcePathJson = None
        self.ExtraCosTargetPathJson = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ExtraCosSourcePathJson = params.get("ExtraCosSourcePathJson")
        self.ExtraCosTargetPathJson = params.get("ExtraCosTargetPathJson")
        self.RequestId = params.get("RequestId")


class AddTencentLabWhitelistTestRequest(AbstractModel):
    """AddTencentLabWhitelistTest请求参数结构体

    """

    def __init__(self):
        r"""
        :param ClassUin: 需要增加白名单的主uin
        :type ClassUin: str
        :param ClassSubUin: 需要增加白名单的subUin
        :type ClassSubUin: str
        :param ResourceId: Tione 平台维护的资源 ID，对应腾学会的课程 ID
        :type ResourceId: str
        :param ExpireDurationSecond: 过期时长，以请求收到的时间向后延后 ExpireDurationSecond 计算过期时刻
        :type ExpireDurationSecond: int
        :param Description: 备注描述
        :type Description: str
        """
        self.ClassUin = None
        self.ClassSubUin = None
        self.ResourceId = None
        self.ExpireDurationSecond = None
        self.Description = None


    def _deserialize(self, params):
        self.ClassUin = params.get("ClassUin")
        self.ClassSubUin = params.get("ClassSubUin")
        self.ResourceId = params.get("ResourceId")
        self.ExpireDurationSecond = params.get("ExpireDurationSecond")
        self.Description = params.get("Description")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class AddTencentLabWhitelistTestResponse(AbstractModel):
    """AddTencentLabWhitelistTest返回参数结构体

    """

    def __init__(self):
        r"""
        :param ExtraCosSourcePathJson: json 格式。课程进行需要的额外 cos 信息。数据源路径信息。若为json 结构或空字符串则表示无额外信息。格式如下
  { 
   "bucket": string,
   "region": string,
   "paths": string array
   }
        :type ExtraCosSourcePathJson: str
        :param ExtraCosTargetPathJson: json 格式。课程进行需要的额外 cos 信息。数据目标路径信息。若为json 结构或空字符串则表示无额外信息。格式如下
   {
   "path": string
   }
        :type ExtraCosTargetPathJson: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ExtraCosSourcePathJson = None
        self.ExtraCosTargetPathJson = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ExtraCosSourcePathJson = params.get("ExtraCosSourcePathJson")
        self.ExtraCosTargetPathJson = params.get("ExtraCosTargetPathJson")
        self.RequestId = params.get("RequestId")


class AnnotationTaskInfo(AbstractModel):
    """描述标注任务详细信息

    """

    def __init__(self):
        r"""
        :param TaskId: 标注任务id
        :type TaskId: str
        :param TaskName: 标注任务名称
        :type TaskName: str
        :param DatasetId: 数据集id
        :type DatasetId: str
        :param DatasetName: 数据集名称
        :type DatasetName: str
        :param SceneName: 标注场景名称
        :type SceneName: str
        :param LabelValueList: 标注任务的label信息数组
        :type LabelValueList: list of LabelValue
        :param CamTagList: tag详情数组
        :type CamTagList: list of CamTag
        :param Status: 任务状态
        :type Status: int
        :param AbnormalMsg: 创建任务失败原因说明
        :type AbnormalMsg: str
        :param IsSubmitting: 标注任务是否正在提交
        :type IsSubmitting: bool
        :param TaskNote: 任务详情描述
        :type TaskNote: str
        :param DataSetVersion: 数据集版本
        :type DataSetVersion: str
        :param NumAnnotated: 已经标注的图片数量
        :type NumAnnotated: int
        :param NumTotal: 标注的总图片数量
        :type NumTotal: int
        :param CreateTime: 创建任务的时间戳
        :type CreateTime: int
        :param OcrToolType: Ocr Tool Type
        :type OcrToolType: int
        :param OcrTextAttributeAnnotateEnable: Ocr Text Attribute Annotate Enable
        :type OcrTextAttributeAnnotateEnable: bool
        :param ExportFormat: 导出格式
        :type ExportFormat: str
        :param SubmittingErrorMsg: 提交错误说明
        :type SubmittingErrorMsg: str
        :param OcrAnnotationContentType: ocr任务类型：1-识别。2-智能结构化
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrAnnotationContentType: int
        :param EnableAuxiliaryAnnotation: OCR任务：是否启用辅助标注
注意：此字段可能返回 null，表示取不到有效值。
        :type EnableAuxiliaryAnnotation: bool
        """
        self.TaskId = None
        self.TaskName = None
        self.DatasetId = None
        self.DatasetName = None
        self.SceneName = None
        self.LabelValueList = None
        self.CamTagList = None
        self.Status = None
        self.AbnormalMsg = None
        self.IsSubmitting = None
        self.TaskNote = None
        self.DataSetVersion = None
        self.NumAnnotated = None
        self.NumTotal = None
        self.CreateTime = None
        self.OcrToolType = None
        self.OcrTextAttributeAnnotateEnable = None
        self.ExportFormat = None
        self.SubmittingErrorMsg = None
        self.OcrAnnotationContentType = None
        self.EnableAuxiliaryAnnotation = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.TaskName = params.get("TaskName")
        self.DatasetId = params.get("DatasetId")
        self.DatasetName = params.get("DatasetName")
        self.SceneName = params.get("SceneName")
        if params.get("LabelValueList") is not None:
            self.LabelValueList = []
            for item in params.get("LabelValueList"):
                obj = LabelValue()
                obj._deserialize(item)
                self.LabelValueList.append(obj)
        if params.get("CamTagList") is not None:
            self.CamTagList = []
            for item in params.get("CamTagList"):
                obj = CamTag()
                obj._deserialize(item)
                self.CamTagList.append(obj)
        self.Status = params.get("Status")
        self.AbnormalMsg = params.get("AbnormalMsg")
        self.IsSubmitting = params.get("IsSubmitting")
        self.TaskNote = params.get("TaskNote")
        self.DataSetVersion = params.get("DataSetVersion")
        self.NumAnnotated = params.get("NumAnnotated")
        self.NumTotal = params.get("NumTotal")
        self.CreateTime = params.get("CreateTime")
        self.OcrToolType = params.get("OcrToolType")
        self.OcrTextAttributeAnnotateEnable = params.get("OcrTextAttributeAnnotateEnable")
        self.ExportFormat = params.get("ExportFormat")
        self.SubmittingErrorMsg = params.get("SubmittingErrorMsg")
        self.OcrAnnotationContentType = params.get("OcrAnnotationContentType")
        self.EnableAuxiliaryAnnotation = params.get("EnableAuxiliaryAnnotation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BadcaseImageInfo(AbstractModel):
    """自动学习评测badcase图像信息

    """

    def __init__(self):
        r"""
        :param ImgThumbnailUrl: badcase图像缩略图地址
        :type ImgThumbnailUrl: str
        :param ImgOriginalUrl: badcase图像地址
        :type ImgOriginalUrl: str
        :param GroundTruthLabels: groundTrue标签信息
        :type GroundTruthLabels: list of LabelConfig
        :param PredictLabels: 推理结果标签信息
        :type PredictLabels: list of PredictConfig
        :param OcrGroundTruth: OCR GT json 字符串
        :type OcrGroundTruth: str
        :param OcrPrediction: OCR Pred json 字符串
        :type OcrPrediction: str
        """
        self.ImgThumbnailUrl = None
        self.ImgOriginalUrl = None
        self.GroundTruthLabels = None
        self.PredictLabels = None
        self.OcrGroundTruth = None
        self.OcrPrediction = None


    def _deserialize(self, params):
        self.ImgThumbnailUrl = params.get("ImgThumbnailUrl")
        self.ImgOriginalUrl = params.get("ImgOriginalUrl")
        if params.get("GroundTruthLabels") is not None:
            self.GroundTruthLabels = []
            for item in params.get("GroundTruthLabels"):
                obj = LabelConfig()
                obj._deserialize(item)
                self.GroundTruthLabels.append(obj)
        if params.get("PredictLabels") is not None:
            self.PredictLabels = []
            for item in params.get("PredictLabels"):
                obj = PredictConfig()
                obj._deserialize(item)
                self.PredictLabels.append(obj)
        self.OcrGroundTruth = params.get("OcrGroundTruth")
        self.OcrPrediction = params.get("OcrPrediction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BatchModelAccTask(AbstractModel):
    """批量模型加速任务

    """

    def __init__(self):
        r"""
        :param ModelId: 模型ID
        :type ModelId: str
        :param ModelVersion: 模型版本
        :type ModelVersion: str
        :param ModelSource: 模型来源(JOB/COS)
        :type ModelSource: str
        :param ModelFormat: 模型格式(TORCH_SCRIPT/DETECTRON2/SAVED_MODEL/FROZEN_GRAPH/MMDETECTION/ONNX/HUGGING_FACE)
        :type ModelFormat: str
        :param TensorInfos: 无
        :type TensorInfos: list of str
        :param AccEngineVersion: 加速引擎版本
        :type AccEngineVersion: str
        :param ModelInputPath: 无
        :type ModelInputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelName: 模型名称
        :type ModelName: str
        :param ModelSignature: SavedModel保存时配置的签名
        :type ModelSignature: str
        """
        self.ModelId = None
        self.ModelVersion = None
        self.ModelSource = None
        self.ModelFormat = None
        self.TensorInfos = None
        self.AccEngineVersion = None
        self.ModelInputPath = None
        self.ModelName = None
        self.ModelSignature = None


    def _deserialize(self, params):
        self.ModelId = params.get("ModelId")
        self.ModelVersion = params.get("ModelVersion")
        self.ModelSource = params.get("ModelSource")
        self.ModelFormat = params.get("ModelFormat")
        self.TensorInfos = params.get("TensorInfos")
        self.AccEngineVersion = params.get("AccEngineVersion")
        if params.get("ModelInputPath") is not None:
            self.ModelInputPath = CosPathInfo()
            self.ModelInputPath._deserialize(params.get("ModelInputPath"))
        self.ModelName = params.get("ModelName")
        self.ModelSignature = params.get("ModelSignature")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BatchTaskDetail(AbstractModel):
    """跑批任务详情

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        :param BatchTaskName: 跑批任务名称
        :type BatchTaskName: str
        :param Uin: 主账号uin
        :type Uin: str
        :param SubUin: 子账号uin
        :type SubUin: str
        :param Region: 地域
        :type Region: str
        :param ChargeType: 计费模式
        :type ChargeType: str
        :param ResourceGroupId: 预付费专用资源组id
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param ResourceGroupName: 预付费专用资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param ResourceConfigInfo: 资源配置
        :type ResourceConfigInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        :param Tags: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param ModelInfo: 服务对应的模型信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param ImageInfo: 自定义镜像信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param CodePackagePath: 代码包
注意：此字段可能返回 null，表示取不到有效值。
        :type CodePackagePath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StartCmd: 启动命令
注意：此字段可能返回 null，表示取不到有效值。
        :type StartCmd: str
        :param DataConfigs: 输入数据配置
注意：此字段可能返回 null，表示取不到有效值。
        :type DataConfigs: list of DataConfig
        :param Outputs: 输出数据配置
        :type Outputs: list of DataConfig
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param LogConfig: 日志配置
注意：此字段可能返回 null，表示取不到有效值。
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param VpcId: vpc id
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param SubnetId: 子网id
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: str
        :param Status: 任务状态
        :type Status: str
        :param RuntimeInSeconds: 运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param StartTime: 任务开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param EndTime: 任务结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param ChargeStatus: 计费状态，eg：BILLING计费中，ARREARS_STOP欠费停止，NOT_BILLING不在计费中
        :type ChargeStatus: str
        :param LatestInstanceId: 最近一次实例ID
注意：此字段可能返回 null，表示取不到有效值。
        :type LatestInstanceId: str
        :param Remark: 备注
注意：此字段可能返回 null，表示取不到有效值。
        :type Remark: str
        :param FailureReason: 失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailureReason: str
        :param BillingInfo: 计费金额信息，eg：2.00元/小时 (for后付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfo: str
        """
        self.BatchTaskId = None
        self.BatchTaskName = None
        self.Uin = None
        self.SubUin = None
        self.Region = None
        self.ChargeType = None
        self.ResourceGroupId = None
        self.ResourceGroupName = None
        self.ResourceConfigInfo = None
        self.Tags = None
        self.ModelInfo = None
        self.ImageInfo = None
        self.CodePackagePath = None
        self.StartCmd = None
        self.DataConfigs = None
        self.Outputs = None
        self.LogEnable = None
        self.LogConfig = None
        self.VpcId = None
        self.SubnetId = None
        self.Status = None
        self.RuntimeInSeconds = None
        self.CreateTime = None
        self.UpdateTime = None
        self.StartTime = None
        self.EndTime = None
        self.ChargeStatus = None
        self.LatestInstanceId = None
        self.Remark = None
        self.FailureReason = None
        self.BillingInfo = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        self.BatchTaskName = params.get("BatchTaskName")
        self.Uin = params.get("Uin")
        self.SubUin = params.get("SubUin")
        self.Region = params.get("Region")
        self.ChargeType = params.get("ChargeType")
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.ResourceGroupName = params.get("ResourceGroupName")
        if params.get("ResourceConfigInfo") is not None:
            self.ResourceConfigInfo = ResourceConfigInfo()
            self.ResourceConfigInfo._deserialize(params.get("ResourceConfigInfo"))
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        if params.get("CodePackagePath") is not None:
            self.CodePackagePath = CosPathInfo()
            self.CodePackagePath._deserialize(params.get("CodePackagePath"))
        self.StartCmd = params.get("StartCmd")
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        if params.get("Outputs") is not None:
            self.Outputs = []
            for item in params.get("Outputs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.Outputs.append(obj)
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Status = params.get("Status")
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.ChargeStatus = params.get("ChargeStatus")
        self.LatestInstanceId = params.get("LatestInstanceId")
        self.Remark = params.get("Remark")
        self.FailureReason = params.get("FailureReason")
        self.BillingInfo = params.get("BillingInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BatchTaskInstance(AbstractModel):
    """批处理任务实例

    """

    def __init__(self):
        r"""
        :param BatchTaskInstanceId: 任务实例id
        :type BatchTaskInstanceId: str
        :param StartTime: 开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param EndTime: 结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param Status: 任务状态
        :type Status: str
        :param RuntimeInSeconds: 运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        """
        self.BatchTaskInstanceId = None
        self.StartTime = None
        self.EndTime = None
        self.Status = None
        self.RuntimeInSeconds = None


    def _deserialize(self, params):
        self.BatchTaskInstanceId = params.get("BatchTaskInstanceId")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Status = params.get("Status")
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class BatchTaskSetItem(AbstractModel):
    """出参类型

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        :param BatchTaskName: 跑批任务名称
        :type BatchTaskName: str
        :param ModelInfo: 模型信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param ImageInfo: 镜像信息
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param ChargeType: 计费模式
        :type ChargeType: str
        :param ChargeStatus: 计费状态，eg：BILLING计费中，ARREARS_STOP欠费停止，NOT_BILLING不在计费中
        :type ChargeStatus: str
        :param ResourceGroupId: 预付费专用资源组
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param ResourceConfigInfo: 资源配置
        :type ResourceConfigInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        :param Tags: 标签配置
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param Status: 任务状态
        :type Status: str
        :param RuntimeInSeconds: 运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param StartTime: 开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param EndTime: 结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param Outputs: 输出
        :type Outputs: list of DataConfig
        :param ResourceGroupName: 预付费专用资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param FailureReason: 失败原因
        :type FailureReason: str
        :param BillingInfo: 计费金额信息，eg：2.00元/小时 (for后付费)
        :type BillingInfo: str
        """
        self.BatchTaskId = None
        self.BatchTaskName = None
        self.ModelInfo = None
        self.ImageInfo = None
        self.ChargeType = None
        self.ChargeStatus = None
        self.ResourceGroupId = None
        self.ResourceConfigInfo = None
        self.Tags = None
        self.Status = None
        self.RuntimeInSeconds = None
        self.CreateTime = None
        self.StartTime = None
        self.EndTime = None
        self.UpdateTime = None
        self.Outputs = None
        self.ResourceGroupName = None
        self.FailureReason = None
        self.BillingInfo = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        self.BatchTaskName = params.get("BatchTaskName")
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        self.ChargeType = params.get("ChargeType")
        self.ChargeStatus = params.get("ChargeStatus")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("ResourceConfigInfo") is not None:
            self.ResourceConfigInfo = ResourceConfigInfo()
            self.ResourceConfigInfo._deserialize(params.get("ResourceConfigInfo"))
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.Status = params.get("Status")
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.UpdateTime = params.get("UpdateTime")
        if params.get("Outputs") is not None:
            self.Outputs = []
            for item in params.get("Outputs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.Outputs.append(obj)
        self.ResourceGroupName = params.get("ResourceGroupName")
        self.FailureReason = params.get("FailureReason")
        self.BillingInfo = params.get("BillingInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CFSConfig(AbstractModel):
    """CFS存储的配置

    """

    def __init__(self):
        r"""
        :param Id: cfs的实例的ID
        :type Id: str
        :param Path: 存储的路径
        :type Path: str
        :param Ip: cfs的ip
注意：此字段可能返回 null，表示取不到有效值。
        :type Ip: str
        :param VpcId: cfs的vpcid
        :type VpcId: str
        :param SubnetId: cfs的子网id
        :type SubnetId: str
        """
        self.Id = None
        self.Path = None
        self.Ip = None
        self.VpcId = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Path = params.get("Path")
        self.Ip = params.get("Ip")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CamTag(AbstractModel):
    """cam详细信息

    """

    def __init__(self):
        r"""
        :param Key: tag键值
        :type Key: str
        :param Value: tag值
        :type Value: str
        """
        self.Key = None
        self.Value = None


    def _deserialize(self, params):
        self.Key = params.get("Key")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckAutoMLTaskNameExistRequest(AbstractModel):
    """CheckAutoMLTaskNameExist请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskName: 任务名称
        :type TaskName: str
        """
        self.TaskName = None


    def _deserialize(self, params):
        self.TaskName = params.get("TaskName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckAutoMLTaskNameExistResponse(AbstractModel):
    """CheckAutoMLTaskNameExist返回参数结构体

    """

    def __init__(self):
        r"""
        :param NameExist: 是否存在
        :type NameExist: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NameExist = None
        self.RequestId = None


    def _deserialize(self, params):
        self.NameExist = params.get("NameExist")
        self.RequestId = params.get("RequestId")


class CheckBillingOwnUinRequest(AbstractModel):
    """CheckBillingOwnUin请求参数结构体

    """


class CheckBillingOwnUinResponse(AbstractModel):
    """CheckBillingOwnUin返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsInternal: 是否是内部客户
        :type IsInternal: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsInternal = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsInternal = params.get("IsInternal")
        self.RequestId = params.get("RequestId")


class CheckBillingWhitelistRequest(AbstractModel):
    """CheckBillingWhitelist请求参数结构体

    """


class CheckBillingWhitelistResponse(AbstractModel):
    """CheckBillingWhitelist返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsWhitelist: 是否为白名单用户
        :type IsWhitelist: bool
        :param IsMiyingUser: 是否为觅影用户
        :type IsMiyingUser: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsWhitelist = None
        self.IsMiyingUser = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsWhitelist = params.get("IsWhitelist")
        self.IsMiyingUser = params.get("IsMiyingUser")
        self.RequestId = params.get("RequestId")


class CheckDatasetNameRequest(AbstractModel):
    """CheckDatasetName请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetName: 数据集名称，长度限制60字符
        :type DatasetName: str
        """
        self.DatasetName = None


    def _deserialize(self, params):
        self.DatasetName = params.get("DatasetName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckDatasetNameResponse(AbstractModel):
    """CheckDatasetName返回参数结构体

    """

    def __init__(self):
        r"""
        :param Exist: true or false
注意：此字段可能返回 null，表示取不到有效值。
        :type Exist: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Exist = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Exist = params.get("Exist")
        self.RequestId = params.get("RequestId")


class CheckModelAccTaskNameExistRequest(AbstractModel):
    """CheckModelAccTaskNameExist请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskName: 模型加速任务名称
        :type ModelAccTaskName: str
        """
        self.ModelAccTaskName = None


    def _deserialize(self, params):
        self.ModelAccTaskName = params.get("ModelAccTaskName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CheckModelAccTaskNameExistResponse(AbstractModel):
    """CheckModelAccTaskNameExist返回参数结构体

    """

    def __init__(self):
        r"""
        :param NameExist: 是否存在重名
注意：此字段可能返回 null，表示取不到有效值。
        :type NameExist: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NameExist = None
        self.RequestId = None


    def _deserialize(self, params):
        self.NameExist = params.get("NameExist")
        self.RequestId = params.get("RequestId")


class CodeRepoDetail(AbstractModel):
    """代码仓库详情

    """

    def __init__(self):
        r"""
        :param Id: 代码仓库ID
        :type Id: str
        :param Name: 代码仓库名称
        :type Name: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param NoSecret: 是否有密钥
        :type NoSecret: bool
        :param GitConfig: 配置
        :type GitConfig: :class:`tencentcloud.tione.v20211111.models.GitConfig`
        """
        self.Id = None
        self.Name = None
        self.CreateTime = None
        self.UpdateTime = None
        self.NoSecret = None
        self.GitConfig = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.NoSecret = params.get("NoSecret")
        if params.get("GitConfig") is not None:
            self.GitConfig = GitConfig()
            self.GitConfig._deserialize(params.get("GitConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CommonConfig(AbstractModel):
    """自动学习基础配置

    """

    def __init__(self):
        r"""
        :param SceneId: 场景ID
        :type SceneId: str
        :param TaskName: 任务名称
        :type TaskName: str
        :param TaskDescription: 任务描述
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskDescription: str
        :param Version: 任务版本，出参使用
        :type Version: str
        """
        self.SceneId = None
        self.TaskName = None
        self.TaskDescription = None
        self.Version = None


    def _deserialize(self, params):
        self.SceneId = params.get("SceneId")
        self.TaskName = params.get("TaskName")
        self.TaskDescription = params.get("TaskDescription")
        self.Version = params.get("Version")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ContentLengthCount(AbstractModel):
    """数据中心查询文本透视

    """

    def __init__(self):
        r"""
        :param LengthMin: 长度区间起点，闭区间
注意：此字段可能返回 null，表示取不到有效值。
        :type LengthMin: int
        :param LengthMax: 长度区间终点，开区间
注意：此字段可能返回 null，表示取不到有效值。
        :type LengthMax: int
        :param Count: 长度区间内样本出现的次数
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        """
        self.LengthMin = None
        self.LengthMax = None
        self.Count = None


    def _deserialize(self, params):
        self.LengthMin = params.get("LengthMin")
        self.LengthMax = params.get("LengthMax")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CosPathInfo(AbstractModel):
    """cos的路径信息

    """

    def __init__(self):
        r"""
        :param Bucket: 存储桶
注意：此字段可能返回 null，表示取不到有效值。
        :type Bucket: str
        :param Region: 所在地域
注意：此字段可能返回 null，表示取不到有效值。
        :type Region: str
        :param Paths: 路径列表，目前只支持单个
注意：此字段可能返回 null，表示取不到有效值。
        :type Paths: list of str
        :param Uin: 主用户Uin
注意：此字段可能返回 null，表示取不到有效值。
        :type Uin: str
        :param SubUin: 子用户UIN
注意：此字段可能返回 null，表示取不到有效值。
        :type SubUin: str
        """
        self.Bucket = None
        self.Region = None
        self.Paths = None
        self.Uin = None
        self.SubUin = None


    def _deserialize(self, params):
        self.Bucket = params.get("Bucket")
        self.Region = params.get("Region")
        self.Paths = params.get("Paths")
        self.Uin = params.get("Uin")
        self.SubUin = params.get("SubUin")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAnnotateTaskRequest(AbstractModel):
    """CreateAnnotateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param DataSetId: 数据集ID
        :type DataSetId: str
        :param DataSetName: 数据集名称
        :type DataSetName: str
        :param TaskName: 任务名称
        :type TaskName: str
        :param ExportFormat: 导出数据格式
        :type ExportFormat: str
        :param SceneName: 场景名称
        :type SceneName: str
        :param Labels: 标签配置
        :type Labels: list of PersonalLabel
        :param TaskNote: 任务备注
        :type TaskNote: str
        :param CamTags: camtag
        :type CamTags: list of CamTag
        :param OcrToolType: ocr标注工具类型 1 矩形 2 四点多边形
        :type OcrToolType: int
        :param OcrTextAttributeAnnotateEnable: ocr是否同时标注文本属性
        :type OcrTextAttributeAnnotateEnable: bool
        :param OcrAnnotationContentType: ocr任务类型：1-识别，2-智能结构化
        :type OcrAnnotationContentType: int
        :param EnableAuxiliaryAnnotation: OCR任务：是否启用辅助标注
        :type EnableAuxiliaryAnnotation: bool
        """
        self.DataSetId = None
        self.DataSetName = None
        self.TaskName = None
        self.ExportFormat = None
        self.SceneName = None
        self.Labels = None
        self.TaskNote = None
        self.CamTags = None
        self.OcrToolType = None
        self.OcrTextAttributeAnnotateEnable = None
        self.OcrAnnotationContentType = None
        self.EnableAuxiliaryAnnotation = None


    def _deserialize(self, params):
        self.DataSetId = params.get("DataSetId")
        self.DataSetName = params.get("DataSetName")
        self.TaskName = params.get("TaskName")
        self.ExportFormat = params.get("ExportFormat")
        self.SceneName = params.get("SceneName")
        if params.get("Labels") is not None:
            self.Labels = []
            for item in params.get("Labels"):
                obj = PersonalLabel()
                obj._deserialize(item)
                self.Labels.append(obj)
        self.TaskNote = params.get("TaskNote")
        if params.get("CamTags") is not None:
            self.CamTags = []
            for item in params.get("CamTags"):
                obj = CamTag()
                obj._deserialize(item)
                self.CamTags.append(obj)
        self.OcrToolType = params.get("OcrToolType")
        self.OcrTextAttributeAnnotateEnable = params.get("OcrTextAttributeAnnotateEnable")
        self.OcrAnnotationContentType = params.get("OcrAnnotationContentType")
        self.EnableAuxiliaryAnnotation = params.get("EnableAuxiliaryAnnotation")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAnnotateTaskResponse(AbstractModel):
    """CreateAnnotateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateAnnotationKeyRequest(AbstractModel):
    """CreateAnnotationKey请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param Key: keypair
        :type Key: :class:`tencentcloud.tione.v20211111.models.KeyPair`
        :param KeyType: 1	标准 key
2	附加key
        :type KeyType: int
        """
        self.DatasetId = None
        self.Key = None
        self.KeyType = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        if params.get("Key") is not None:
            self.Key = KeyPair()
            self.Key._deserialize(params.get("Key"))
        self.KeyType = params.get("KeyType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAnnotationKeyResponse(AbstractModel):
    """CreateAnnotationKey返回参数结构体

    """

    def __init__(self):
        r"""
        :param Key: keypari
        :type Key: :class:`tencentcloud.tione.v20211111.models.KeyPair`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Key = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Key") is not None:
            self.Key = KeyPair()
            self.Key._deserialize(params.get("Key"))
        self.RequestId = params.get("RequestId")


class CreateAutoMLEMSTaskRequest(AbstractModel):
    """CreateAutoMLEMSTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务创建任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param ChargeType: 付费模式，PREPAID(预付费), POSTPAID_BY_HOUR(后付费)
        :type ChargeType: str
        :param PublishResourceInfo: 发布模型服务资源分配信息
        :type PublishResourceInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        :param ResourceGroupId: 预付费资源组id
        :type ResourceGroupId: str
        :param MaxServiceHours: 模型服务最大运行小时，不填默认1小时，-1表示永久
        :type MaxServiceHours: int
        :param UserCosInfo: 用来保存用户测试时的图片
        :type UserCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        """
        self.AutoMLTaskId = None
        self.ChargeType = None
        self.PublishResourceInfo = None
        self.ResourceGroupId = None
        self.MaxServiceHours = None
        self.UserCosInfo = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.ChargeType = params.get("ChargeType")
        if params.get("PublishResourceInfo") is not None:
            self.PublishResourceInfo = ResourceConfigInfo()
            self.PublishResourceInfo._deserialize(params.get("PublishResourceInfo"))
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.MaxServiceHours = params.get("MaxServiceHours")
        if params.get("UserCosInfo") is not None:
            self.UserCosInfo = CosPathInfo()
            self.UserCosInfo._deserialize(params.get("UserCosInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAutoMLEMSTaskResponse(AbstractModel):
    """CreateAutoMLEMSTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务创建任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
        :type EMSTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.RequestId = params.get("RequestId")


class CreateAutoMLTaskEvaluationConfusionMatrixUrlRequest(AbstractModel):
    """CreateAutoMLTaskEvaluationConfusionMatrixUrl请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param Thresholds: 每个标签对应的阈值信息，不填默认所有标签用默认的0.5，填一个表示所有标签的阈值一样
        :type Thresholds: list of float
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Thresholds = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Thresholds = params.get("Thresholds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAutoMLTaskEvaluationConfusionMatrixUrlResponse(AbstractModel):
    """CreateAutoMLTaskEvaluationConfusionMatrixUrl返回参数结构体

    """

    def __init__(self):
        r"""
        :param ConfusionUrl: 混淆矩阵下载链接，有效期1分钟
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfusionUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ConfusionUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ConfusionUrl = params.get("ConfusionUrl")
        self.RequestId = params.get("RequestId")


class CreateAutoMLTaskRequest(AbstractModel):
    """CreateAutoMLTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param CommonConfig: 基础配置
        :type CommonConfig: :class:`tencentcloud.tione.v20211111.models.CommonConfig`
        :param DataConfig: 数据配置
        :type DataConfig: :class:`tencentcloud.tione.v20211111.models.MLDataConfig`
        :param ModelTrainConfig: 模型训练配置
        :type ModelTrainConfig: :class:`tencentcloud.tione.v20211111.models.ModelTrainConfig`
        :param ModelParamConfig: 模型训练超参数
        :type ModelParamConfig: str
        :param TrainResourceConfig: 训练资源配置
        :type TrainResourceConfig: :class:`tencentcloud.tione.v20211111.models.TrainResourceConfig`
        :param TaskSource: 任务来源
        :type TaskSource: str
        :param Tags: 标签
        :type Tags: list of Tag
        :param TaskOutputCosInfo: 任务输出路径
        :type TaskOutputCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param PublishAutoMLTaskId: 发布新版本任务来源ID
        :type PublishAutoMLTaskId: str
        :param ModelAccelerateConfig: 模型优化配置
        :type ModelAccelerateConfig: :class:`tencentcloud.tione.v20211111.models.ModelAccelerateConfig`
        """
        self.CommonConfig = None
        self.DataConfig = None
        self.ModelTrainConfig = None
        self.ModelParamConfig = None
        self.TrainResourceConfig = None
        self.TaskSource = None
        self.Tags = None
        self.TaskOutputCosInfo = None
        self.PublishAutoMLTaskId = None
        self.ModelAccelerateConfig = None


    def _deserialize(self, params):
        if params.get("CommonConfig") is not None:
            self.CommonConfig = CommonConfig()
            self.CommonConfig._deserialize(params.get("CommonConfig"))
        if params.get("DataConfig") is not None:
            self.DataConfig = MLDataConfig()
            self.DataConfig._deserialize(params.get("DataConfig"))
        if params.get("ModelTrainConfig") is not None:
            self.ModelTrainConfig = ModelTrainConfig()
            self.ModelTrainConfig._deserialize(params.get("ModelTrainConfig"))
        self.ModelParamConfig = params.get("ModelParamConfig")
        if params.get("TrainResourceConfig") is not None:
            self.TrainResourceConfig = TrainResourceConfig()
            self.TrainResourceConfig._deserialize(params.get("TrainResourceConfig"))
        self.TaskSource = params.get("TaskSource")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("TaskOutputCosInfo") is not None:
            self.TaskOutputCosInfo = CosPathInfo()
            self.TaskOutputCosInfo._deserialize(params.get("TaskOutputCosInfo"))
        self.PublishAutoMLTaskId = params.get("PublishAutoMLTaskId")
        if params.get("ModelAccelerateConfig") is not None:
            self.ModelAccelerateConfig = ModelAccelerateConfig()
            self.ModelAccelerateConfig._deserialize(params.get("ModelAccelerateConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateAutoMLTaskResponse(AbstractModel):
    """CreateAutoMLTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param Version: 任务版本
        :type Version: str
        :param AsyncTaskId: 异步任务ID
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.Version = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.Version = params.get("Version")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class CreateBatchModelAccTasksRequest(AbstractModel):
    """CreateBatchModelAccTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskName: 模型加速任务名称
        :type ModelAccTaskName: str
        :param BatchModelAccTasks: 批量模型加速任务
        :type BatchModelAccTasks: list of BatchModelAccTask
        :param ModelOutputPath: 模型加速保存路径
        :type ModelOutputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param Tags: 标签
        :type Tags: list of Tag
        :param OptimizationLevel: 优化级别(NO_LOSS/FP16/INT8)，默认FP16
        :type OptimizationLevel: str
        :param GPUType: GPU卡类型(T4/V100/A10)，默认T4
        :type GPUType: str
        :param HyperParameter: 专业参数设置
        :type HyperParameter: :class:`tencentcloud.tione.v20211111.models.HyperParameter`
        """
        self.ModelAccTaskName = None
        self.BatchModelAccTasks = None
        self.ModelOutputPath = None
        self.Tags = None
        self.OptimizationLevel = None
        self.GPUType = None
        self.HyperParameter = None


    def _deserialize(self, params):
        self.ModelAccTaskName = params.get("ModelAccTaskName")
        if params.get("BatchModelAccTasks") is not None:
            self.BatchModelAccTasks = []
            for item in params.get("BatchModelAccTasks"):
                obj = BatchModelAccTask()
                obj._deserialize(item)
                self.BatchModelAccTasks.append(obj)
        if params.get("ModelOutputPath") is not None:
            self.ModelOutputPath = CosPathInfo()
            self.ModelOutputPath._deserialize(params.get("ModelOutputPath"))
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.OptimizationLevel = params.get("OptimizationLevel")
        self.GPUType = params.get("GPUType")
        if params.get("HyperParameter") is not None:
            self.HyperParameter = HyperParameter()
            self.HyperParameter._deserialize(params.get("HyperParameter"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBatchModelAccTasksResponse(AbstractModel):
    """CreateBatchModelAccTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateBatchTaskRequest(AbstractModel):
    """CreateBatchTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskName: 跑批任务名称，不超过60个字符，仅支持中英文、数字、下划线"_"、短横"-"，只能以中英文、数字开头
        :type BatchTaskName: str
        :param ChargeType: 计费模式，eg：PREPAID预付费，即包年包月；POSTPAID_BY_HOUR按小时后付费
        :type ChargeType: str
        :param ResourceConfigInfo: 资源配置
        :type ResourceConfigInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        :param Outputs: 结果输出
        :type Outputs: list of DataConfig
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param JobType: 工作类型 1:单次 2:周期
        :type JobType: int
        :param CronInfo: 任务周期描述
        :type CronInfo: :class:`tencentcloud.tione.v20211111.models.CronInfo`
        :param ResourceGroupId: 预付费专用资源组
        :type ResourceGroupId: str
        :param Tags: 标签配置
        :type Tags: list of Tag
        :param ModelInfo: 服务对应的模型信息，有模型文件时需要填写
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param ImageInfo: 自定义镜像信息
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param CodePackage: 代码包
        :type CodePackage: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StartCmd: 启动命令
        :type StartCmd: str
        :param DataConfigs: 数据配置
        :type DataConfigs: list of DataConfig
        :param LogConfig: 日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param VpcId: VPC Id
        :type VpcId: str
        :param SubnetId: 子网Id
        :type SubnetId: str
        :param Remark: 备注
        :type Remark: str
        """
        self.BatchTaskName = None
        self.ChargeType = None
        self.ResourceConfigInfo = None
        self.Outputs = None
        self.LogEnable = None
        self.JobType = None
        self.CronInfo = None
        self.ResourceGroupId = None
        self.Tags = None
        self.ModelInfo = None
        self.ImageInfo = None
        self.CodePackage = None
        self.StartCmd = None
        self.DataConfigs = None
        self.LogConfig = None
        self.VpcId = None
        self.SubnetId = None
        self.Remark = None


    def _deserialize(self, params):
        self.BatchTaskName = params.get("BatchTaskName")
        self.ChargeType = params.get("ChargeType")
        if params.get("ResourceConfigInfo") is not None:
            self.ResourceConfigInfo = ResourceConfigInfo()
            self.ResourceConfigInfo._deserialize(params.get("ResourceConfigInfo"))
        if params.get("Outputs") is not None:
            self.Outputs = []
            for item in params.get("Outputs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.Outputs.append(obj)
        self.LogEnable = params.get("LogEnable")
        self.JobType = params.get("JobType")
        if params.get("CronInfo") is not None:
            self.CronInfo = CronInfo()
            self.CronInfo._deserialize(params.get("CronInfo"))
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        if params.get("CodePackage") is not None:
            self.CodePackage = CosPathInfo()
            self.CodePackage._deserialize(params.get("CodePackage"))
        self.StartCmd = params.get("StartCmd")
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Remark = params.get("Remark")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBatchTaskResponse(AbstractModel):
    """CreateBatchTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        self.RequestId = params.get("RequestId")


class CreateBillingResourceGroupRequest(AbstractModel):
    """CreateBillingResourceGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 资源组名称
注意：此字段仅支持英文、数字、下划线 _、短横 -，只能以英文、数字开头，长度为60个字
注意：此字段相同地域相同资源组类型下不可同名。
        :type Name: str
        :param Type: 资源组类型
注意：此字段为枚举值
说明：
TRAIN: 训练
 INFERENCE: 推理。
        :type Type: str
        :param TagSet: 资源组标签列表
注意：此字段从腾讯云标签服务获取。
        :type TagSet: list of Tag
        """
        self.Name = None
        self.Type = None
        self.TagSet = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBillingResourceGroupResponse(AbstractModel):
    """CreateBillingResourceGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id;
        :type ResourceGroupId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceGroupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.RequestId = params.get("RequestId")


class CreateBillingResourceInstanceRequest(AbstractModel):
    """CreateBillingResourceInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组节点id
        :type ResourceGroupId: str
        """
        self.ResourceGroupId = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateBillingResourceInstanceResponse(AbstractModel):
    """CreateBillingResourceInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param CheckResult: 校验结果 true: 有权限 false 无权限
注意：此字段可能返回 null，表示取不到有效值。
        :type CheckResult: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CheckResult = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CheckResult = params.get("CheckResult")
        self.RequestId = params.get("RequestId")


class CreateCodeRepoRequest(AbstractModel):
    """CreateCodeRepo请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 名称。不超过60个字符，仅支持中英文、数字、下划线"_"、短横"-"，只能以中英文、数字开头
        :type Name: str
        :param GitSecret: git的认证信息
        :type GitSecret: :class:`tencentcloud.tione.v20211111.models.GitSecret`
        :param GitConfig: git的配置信息
        :type GitConfig: :class:`tencentcloud.tione.v20211111.models.GitConfig`
        """
        self.Name = None
        self.GitSecret = None
        self.GitConfig = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        if params.get("GitSecret") is not None:
            self.GitSecret = GitSecret()
            self.GitSecret._deserialize(params.get("GitSecret"))
        if params.get("GitConfig") is not None:
            self.GitConfig = GitConfig()
            self.GitConfig._deserialize(params.get("GitConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateCodeRepoResponse(AbstractModel):
    """CreateCodeRepo返回参数结构体

    """

    def __init__(self):
        r"""
        :param Id: id值
        :type Id: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Id = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.RequestId = params.get("RequestId")


class CreateDatasetDetailTextRequest(AbstractModel):
    """CreateDatasetDetailText请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param FileId: 文件ID
        :type FileId: str
        """
        self.DatasetId = None
        self.FileId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.FileId = params.get("FileId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDatasetDetailTextResponse(AbstractModel):
    """CreateDatasetDetailText返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateDatasetRequest(AbstractModel):
    """CreateDataset请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetName: 数据集名称，不超过60个字符，仅支持中英文、数字、下划线"_"、短横"-"，只能以中英文、数字开头
        :type DatasetName: str
        :param DatasetType: 数据集类型:
TYPE_DATASET_TEXT，文本
TYPE_DATASET_IMAGE，图片
TYPE_DATASET_TABLE，表格
TYPE_DATASET_OTHER，其他
        :type DatasetType: str
        :param StorageDataPath: 数据源cos路径
        :type StorageDataPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StorageLabelPath: 数据集标签cos存储路径
        :type StorageLabelPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param DatasetTags: 数据集标签
        :type DatasetTags: list of Tag
        :param AnnotationStatus: 数据集标注状态:
STATUS_NON_ANNOTATED，未标注
STATUS_ANNOTATED，已标注
        :type AnnotationStatus: str
        :param AnnotationType: 标注类型:
ANNOTATION_TYPE_CLASSIFICATION，图片分类
ANNOTATION_TYPE_DETECTION，目标检测
ANNOTATION_TYPE_SEGMENTATION，图片分割
ANNOTATION_TYPE_TRACKING，目标跟踪
        :type AnnotationType: str
        :param AnnotationFormat: 标注格式:
ANNOTATION_FORMAT_TI，TI平台格式
ANNOTATION_FORMAT_PASCAL，Pascal Voc
ANNOTATION_FORMAT_COCO，COCO
ANNOTATION_FORMAT_FILE，文件目录结构
        :type AnnotationFormat: str
        :param SchemaInfos: 表头信息
        :type SchemaInfos: list of SchemaInfo
        :param IsSchemaExisted: 数据是否存在表头
        :type IsSchemaExisted: bool
        :param ContentType: 导入文件粒度，按行或者按文件
        :type ContentType: str
        """
        self.DatasetName = None
        self.DatasetType = None
        self.StorageDataPath = None
        self.StorageLabelPath = None
        self.DatasetTags = None
        self.AnnotationStatus = None
        self.AnnotationType = None
        self.AnnotationFormat = None
        self.SchemaInfos = None
        self.IsSchemaExisted = None
        self.ContentType = None


    def _deserialize(self, params):
        self.DatasetName = params.get("DatasetName")
        self.DatasetType = params.get("DatasetType")
        if params.get("StorageDataPath") is not None:
            self.StorageDataPath = CosPathInfo()
            self.StorageDataPath._deserialize(params.get("StorageDataPath"))
        if params.get("StorageLabelPath") is not None:
            self.StorageLabelPath = CosPathInfo()
            self.StorageLabelPath._deserialize(params.get("StorageLabelPath"))
        if params.get("DatasetTags") is not None:
            self.DatasetTags = []
            for item in params.get("DatasetTags"):
                obj = Tag()
                obj._deserialize(item)
                self.DatasetTags.append(obj)
        self.AnnotationStatus = params.get("AnnotationStatus")
        self.AnnotationType = params.get("AnnotationType")
        self.AnnotationFormat = params.get("AnnotationFormat")
        if params.get("SchemaInfos") is not None:
            self.SchemaInfos = []
            for item in params.get("SchemaInfos"):
                obj = SchemaInfo()
                obj._deserialize(item)
                self.SchemaInfos.append(obj)
        self.IsSchemaExisted = params.get("IsSchemaExisted")
        self.ContentType = params.get("ContentType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDatasetResponse(AbstractModel):
    """CreateDataset返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasetId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.RequestId = params.get("RequestId")


class CreateDatasetTextAnalyzeRequest(AbstractModel):
    """CreateDatasetTextAnalyze请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetIds: 数据集ID列表
        :type DatasetIds: list of str
        :param TextLanguage: 样本语言:
TEXT_LANGUAGE_ENGLISH 英文
TEXT_LANGUAGE_CHINESE 中文
        :type TextLanguage: str
        """
        self.DatasetIds = None
        self.TextLanguage = None


    def _deserialize(self, params):
        self.DatasetIds = params.get("DatasetIds")
        self.TextLanguage = params.get("TextLanguage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDatasetTextAnalyzeResponse(AbstractModel):
    """CreateDatasetTextAnalyze返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class CreateDemoWhiteRequest(AbstractModel):
    """CreateDemoWhite请求参数结构体

    """

    def __init__(self):
        r"""
        :param DemoUin: 要添加白名单用户的主账号uin
        :type DemoUin: str
        :param Type: 任务类型。1为Notebook+Tikit实验；2为自动学习实验
        :type Type: int
        """
        self.DemoUin = None
        self.Type = None


    def _deserialize(self, params):
        self.DemoUin = params.get("DemoUin")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateDemoWhiteResponse(AbstractModel):
    """CreateDemoWhite返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateExportAutoMLSDKTaskRequest(AbstractModel):
    """CreateExportAutoMLSDKTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        :param SDKLanguage: SDK语言
        :type SDKLanguage: str
        :param StorageCosInfo: 存储COS路径
        :type StorageCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.SDKLanguage = None
        self.StorageCosInfo = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.SDKLanguage = params.get("SDKLanguage")
        if params.get("StorageCosInfo") is not None:
            self.StorageCosInfo = CosPathInfo()
            self.StorageCosInfo._deserialize(params.get("StorageCosInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateExportAutoMLSDKTaskResponse(AbstractModel):
    """CreateExportAutoMLSDKTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param TrainId: 任务式建模ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainId: str
        :param StorageCosInfo: SDK输出COS路径
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.TrainId = None
        self.StorageCosInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.TrainId = params.get("TrainId")
        if params.get("StorageCosInfo") is not None:
            self.StorageCosInfo = CosPathInfo()
            self.StorageCosInfo._deserialize(params.get("StorageCosInfo"))
        self.RequestId = params.get("RequestId")


class CreateInferGatewayRequest(AbstractModel):
    """CreateInferGateway请求参数结构体

    """

    def __init__(self):
        r"""
        :param VpcId: 用户推理服务客户端服务所在的VpcId
        :type VpcId: str
        :param SubnetId: 用户推理服务客户端服务所在的SubnetId
        :type SubnetId: str
        """
        self.VpcId = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateInferGatewayResponse(AbstractModel):
    """CreateInferGateway返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class CreateLifecycleScriptRequest(AbstractModel):
    """CreateLifecycleScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 生命周期脚本名称。由中英文、数字、下划线"_"、短横"-"组成
        :type Name: str
        :param CreateScript: 创建脚本，需要base64编码，base64编码后的长度不能超过16384
        :type CreateScript: str
        :param StartScript: 动脚本, 需要base64编码，base64编码后的长度不能超过16384
        :type StartScript: str
        """
        self.Name = None
        self.CreateScript = None
        self.StartScript = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.CreateScript = params.get("CreateScript")
        self.StartScript = params.get("StartScript")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateLifecycleScriptResponse(AbstractModel):
    """CreateLifecycleScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param Id: id值
        :type Id: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Id = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.RequestId = params.get("RequestId")


class CreateModelAccelerateTaskRequest(AbstractModel):
    """CreateModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskName: 模型加速任务名称
        :type ModelAccTaskName: str
        :param ModelSource: 模型来源（JOB/COS）
        :type ModelSource: str
        :param ModelInputPath: 模型输入cos路径
        :type ModelInputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelOutputPath: 模型输出cos路径
        :type ModelOutputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param AlgorithmFramework: 算法框架（废弃）
        :type AlgorithmFramework: str
        :param ModelId: 模型ID
        :type ModelId: str
        :param ModelName: 模型名称
        :type ModelName: str
        :param ModelVersion: 模型版本
        :type ModelVersion: str
        :param OptimizationLevel: 优化级别 （NO_LOSS/FP16/INT8），默认FP16
        :type OptimizationLevel: str
        :param ModelInputNum: input节点个数（废弃）
        :type ModelInputNum: int
        :param ModelInputInfos: input节点信息（废弃）
        :type ModelInputInfos: list of ModelInputInfo
        :param ModelFormat: 模型格式 （TORCH_SCRIPT/DETECTRON2/SAVED_MODEL/FROZEN_GRAPH/MMDETECTION/ONNX/HUGGING_FACE）
        :type ModelFormat: str
        :param TensorInfos: 模型Tensor信息
        :type TensorInfos: list of str
        :param HyperParameter: 模型专业参数
        :type HyperParameter: :class:`tencentcloud.tione.v20211111.models.HyperParameter`
        :param GPUType: GPU类型（T4/V100/A10），默认T4
        :type GPUType: str
        :param AccEngineVersion: 加速引擎版本
        :type AccEngineVersion: str
        :param Tags: 标签
        :type Tags: list of Tag
        :param ModelSignature: SavedModel保存时配置的签名
        :type ModelSignature: str
        """
        self.ModelAccTaskName = None
        self.ModelSource = None
        self.ModelInputPath = None
        self.ModelOutputPath = None
        self.AlgorithmFramework = None
        self.ModelId = None
        self.ModelName = None
        self.ModelVersion = None
        self.OptimizationLevel = None
        self.ModelInputNum = None
        self.ModelInputInfos = None
        self.ModelFormat = None
        self.TensorInfos = None
        self.HyperParameter = None
        self.GPUType = None
        self.AccEngineVersion = None
        self.Tags = None
        self.ModelSignature = None


    def _deserialize(self, params):
        self.ModelAccTaskName = params.get("ModelAccTaskName")
        self.ModelSource = params.get("ModelSource")
        if params.get("ModelInputPath") is not None:
            self.ModelInputPath = CosPathInfo()
            self.ModelInputPath._deserialize(params.get("ModelInputPath"))
        if params.get("ModelOutputPath") is not None:
            self.ModelOutputPath = CosPathInfo()
            self.ModelOutputPath._deserialize(params.get("ModelOutputPath"))
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.ModelId = params.get("ModelId")
        self.ModelName = params.get("ModelName")
        self.ModelVersion = params.get("ModelVersion")
        self.OptimizationLevel = params.get("OptimizationLevel")
        self.ModelInputNum = params.get("ModelInputNum")
        if params.get("ModelInputInfos") is not None:
            self.ModelInputInfos = []
            for item in params.get("ModelInputInfos"):
                obj = ModelInputInfo()
                obj._deserialize(item)
                self.ModelInputInfos.append(obj)
        self.ModelFormat = params.get("ModelFormat")
        self.TensorInfos = params.get("TensorInfos")
        if params.get("HyperParameter") is not None:
            self.HyperParameter = HyperParameter()
            self.HyperParameter._deserialize(params.get("HyperParameter"))
        self.GPUType = params.get("GPUType")
        self.AccEngineVersion = params.get("AccEngineVersion")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.ModelSignature = params.get("ModelSignature")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateModelAccelerateTaskResponse(AbstractModel):
    """CreateModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskId: str
        :param AsyncTaskId: 异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ModelAccTaskId = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class CreateModelServiceRequest(AbstractModel):
    """CreateModelService请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageInfo: 镜像信息，配置服务运行所需的镜像地址等信息
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param ServiceGroupId: 新增版本时需要填写
        :type ServiceGroupId: str
        :param ServiceGroupName: 不超过60个字，仅支持英文、数字、下划线"_"、短横"-"，只能以英文、数字开头
        :type ServiceGroupName: str
        :param ServiceDescription: 模型服务的描述
        :type ServiceDescription: str
        :param ChargeType: 付费模式,有 PREPAID 、 POSTPAID_BY_HOUR 和 HYBRID_PAID 三种
        :type ChargeType: str
        :param ResourceGroupId: 预付费模式下所属的资源组id，同服务组下唯一
        :type ResourceGroupId: str
        :param ModelInfo: 模型信息，需要挂载模型时填写
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param Env: 环境变量，可选参数，用于配置容器中的环境变量
        :type Env: list of EnvVar
        :param Resources: 资源描述，指定预付费模式下的cpu,mem,gpu等信息，后付费无需填写
        :type Resources: :class:`tencentcloud.tione.v20211111.models.ResourceInfo`
        :param InstanceType: 使用DescribeBillingSpecs接口返回的规格列表中的值，或者参考实例列表:
TI.S.MEDIUM.POST	2C4G
TI.S.LARGE.POST	4C8G
TI.S.2XLARGE16.POST	8C16G
TI.S.2XLARGE32.POST	8C32G
TI.S.4XLARGE32.POST	16C32G
TI.S.4XLARGE64.POST	16C64G
TI.S.6XLARGE48.POST	24C48G
TI.S.6XLARGE96.POST	24C96G
TI.S.8XLARGE64.POST	32C64G
TI.S.8XLARGE128.POST 32C128G
TI.GN7.LARGE20.POST	4C20G T4*1/4
TI.GN7.2XLARGE40.POST	10C40G T4*1/2
TI.GN7.2XLARGE32.POST	8C32G T4*1
TI.GN7.5XLARGE80.POST	20C80G T4*1
TI.GN7.8XLARGE128.POST	32C128G T4*1
TI.GN7.10XLARGE160.POST	40C160G T4*2
TI.GN7.20XLARGE320.POST	80C320G T4*4
        :type InstanceType: str
        :param ScaleMode: 扩缩容类型 支持：自动 - "AUTO", 手动 - "MANUAL",默认为MANUAL
        :type ScaleMode: str
        :param Replicas: 实例数量, 不同计费模式和调节模式下对应关系如下
PREPAID 和 POSTPAID_BY_HOUR:
手动调节模式下对应 实例数量
自动调节模式下对应 基于时间的默认策略的实例数量
HYBRID_PAID:
后付费实例手动调节模式下对应 实例数量
后付费实例自动调节模式下对应 时间策略的默认策略的实例数量
        :type Replicas: int
        :param HorizontalPodAutoscaler: 自动伸缩信息
        :type HorizontalPodAutoscaler: :class:`tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param LogEnable: 是否开启日志投递，开启后需填写配置投递到指定cls
        :type LogEnable: bool
        :param LogConfig: 日志配置，需要投递服务日志到指定cls时填写
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param AuthorizationEnable: 是否开启接口鉴权，开启后自动生成token信息，访问需要token鉴权
        :type AuthorizationEnable: bool
        :param Tags: 腾讯云标签
        :type Tags: list of Tag
        :param NewVersion: 是否新增版本
        :type NewVersion: bool
        :param CronScaleJobs: 定时任务配置，使用定时策略时填写
        :type CronScaleJobs: list of CronScaleJob
        :param ScaleStrategy: 自动伸缩策略配置 HPA : 通过HPA进行弹性伸缩 CRON 通过定时任务进行伸缩
        :type ScaleStrategy: str
        :param HybridBillingPrepaidReplicas: 计费模式[HYBRID_PAID]时生效, 用于标识混合计费模式下的预付费实例数
        :type HybridBillingPrepaidReplicas: int
        :param CreateSource: [AUTO_ML 自动学习，自动学习正式发布 AUTO_ML_FORMAL, DEFAULT 默认]
        :type CreateSource: str
        :param ModelHotUpdateEnable: 是否开启模型的热更新。默认不开启
        :type ModelHotUpdateEnable: bool
        :param ScheduledAction: 定时停止配置
        :type ScheduledAction: :class:`tencentcloud.tione.v20211111.models.ScheduledAction`
        :param VolumeMount: 挂载配置，目前只支持CFS
        :type VolumeMount: :class:`tencentcloud.tione.v20211111.models.VolumeMount`
        :param ServiceLimit: 服务限速限流相关配置
        :type ServiceLimit: :class:`tencentcloud.tione.v20211111.models.ServiceLimit`
        """
        self.ImageInfo = None
        self.ServiceGroupId = None
        self.ServiceGroupName = None
        self.ServiceDescription = None
        self.ChargeType = None
        self.ResourceGroupId = None
        self.ModelInfo = None
        self.Env = None
        self.Resources = None
        self.InstanceType = None
        self.ScaleMode = None
        self.Replicas = None
        self.HorizontalPodAutoscaler = None
        self.LogEnable = None
        self.LogConfig = None
        self.AuthorizationEnable = None
        self.Tags = None
        self.NewVersion = None
        self.CronScaleJobs = None
        self.ScaleStrategy = None
        self.HybridBillingPrepaidReplicas = None
        self.CreateSource = None
        self.ModelHotUpdateEnable = None
        self.ScheduledAction = None
        self.VolumeMount = None
        self.ServiceLimit = None


    def _deserialize(self, params):
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        self.ServiceGroupId = params.get("ServiceGroupId")
        self.ServiceGroupName = params.get("ServiceGroupName")
        self.ServiceDescription = params.get("ServiceDescription")
        self.ChargeType = params.get("ChargeType")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        if params.get("Env") is not None:
            self.Env = []
            for item in params.get("Env"):
                obj = EnvVar()
                obj._deserialize(item)
                self.Env.append(obj)
        if params.get("Resources") is not None:
            self.Resources = ResourceInfo()
            self.Resources._deserialize(params.get("Resources"))
        self.InstanceType = params.get("InstanceType")
        self.ScaleMode = params.get("ScaleMode")
        self.Replicas = params.get("Replicas")
        if params.get("HorizontalPodAutoscaler") is not None:
            self.HorizontalPodAutoscaler = HorizontalPodAutoscaler()
            self.HorizontalPodAutoscaler._deserialize(params.get("HorizontalPodAutoscaler"))
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.AuthorizationEnable = params.get("AuthorizationEnable")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.NewVersion = params.get("NewVersion")
        if params.get("CronScaleJobs") is not None:
            self.CronScaleJobs = []
            for item in params.get("CronScaleJobs"):
                obj = CronScaleJob()
                obj._deserialize(item)
                self.CronScaleJobs.append(obj)
        self.ScaleStrategy = params.get("ScaleStrategy")
        self.HybridBillingPrepaidReplicas = params.get("HybridBillingPrepaidReplicas")
        self.CreateSource = params.get("CreateSource")
        self.ModelHotUpdateEnable = params.get("ModelHotUpdateEnable")
        if params.get("ScheduledAction") is not None:
            self.ScheduledAction = ScheduledAction()
            self.ScheduledAction._deserialize(params.get("ScheduledAction"))
        if params.get("VolumeMount") is not None:
            self.VolumeMount = VolumeMount()
            self.VolumeMount._deserialize(params.get("VolumeMount"))
        if params.get("ServiceLimit") is not None:
            self.ServiceLimit = ServiceLimit()
            self.ServiceLimit._deserialize(params.get("ServiceLimit"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateModelServiceResponse(AbstractModel):
    """CreateModelService返回参数结构体

    """

    def __init__(self):
        r"""
        :param Service: 生成的模型服务
注意：此字段可能返回 null，表示取不到有效值。
        :type Service: :class:`tencentcloud.tione.v20211111.models.Service`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Service = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Service") is not None:
            self.Service = Service()
            self.Service._deserialize(params.get("Service"))
        self.RequestId = params.get("RequestId")


class CreateNotebookRequest(AbstractModel):
    """CreateNotebook请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 名称。不超过60个字符，仅支持中英文、数字、下划线"_"、短横"-"，只能以中英文、数字开头
        :type Name: str
        :param ChargeType: 计算资源付费模式 ，可选值为：
PREPAID：预付费，即包年包月
POSTPAID_BY_HOUR：按小时后付费
        :type ChargeType: str
        :param ResourceConf: 计算资源配置
        :type ResourceConf: :class:`tencentcloud.tione.v20211111.models.ResourceConf`
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param RootAccess: 是否ROOT权限
        :type RootAccess: bool
        :param AutoStopping: 是否自动停止
        :type AutoStopping: bool
        :param DirectInternetAccess: 是否访问公网
        :type DirectInternetAccess: bool
        :param ResourceGroupId: 资源组ID(for预付费)
        :type ResourceGroupId: str
        :param VpcId: Vpc-Id
        :type VpcId: str
        :param SubnetId: 子网Id
        :type SubnetId: str
        :param VolumeSourceType: 存储的类型。取值包含： 
    FREE:    预付费的免费存储
    CLOUD_PREMIUM： 高性能云硬盘
    CLOUD_SSD： SSD云硬盘
    CFS:     CFS存储，包含NFS和turbo
        :type VolumeSourceType: str
        :param VolumeSizeInGB: 存储卷大小，单位GB
        :type VolumeSizeInGB: int
        :param VolumeSourceCFS: CFS存储的配置
        :type VolumeSourceCFS: :class:`tencentcloud.tione.v20211111.models.CFSConfig`
        :param LogConfig: 日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param LifecycleScriptId: 生命周期脚本的ID
        :type LifecycleScriptId: str
        :param DefaultCodeRepoId: 默认GIT存储库的ID
        :type DefaultCodeRepoId: str
        :param AdditionalCodeRepoIds: 其他GIT存储库的ID，最多3个
        :type AdditionalCodeRepoIds: list of str
        :param AutomaticStopTime: 自动停止时间，单位小时
        :type AutomaticStopTime: int
        :param Tags: 标签配置
        :type Tags: list of Tag
        :param DataConfigs: 数据配置
        :type DataConfigs: list of DataConfig
        """
        self.Name = None
        self.ChargeType = None
        self.ResourceConf = None
        self.LogEnable = None
        self.RootAccess = None
        self.AutoStopping = None
        self.DirectInternetAccess = None
        self.ResourceGroupId = None
        self.VpcId = None
        self.SubnetId = None
        self.VolumeSourceType = None
        self.VolumeSizeInGB = None
        self.VolumeSourceCFS = None
        self.LogConfig = None
        self.LifecycleScriptId = None
        self.DefaultCodeRepoId = None
        self.AdditionalCodeRepoIds = None
        self.AutomaticStopTime = None
        self.Tags = None
        self.DataConfigs = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.ChargeType = params.get("ChargeType")
        if params.get("ResourceConf") is not None:
            self.ResourceConf = ResourceConf()
            self.ResourceConf._deserialize(params.get("ResourceConf"))
        self.LogEnable = params.get("LogEnable")
        self.RootAccess = params.get("RootAccess")
        self.AutoStopping = params.get("AutoStopping")
        self.DirectInternetAccess = params.get("DirectInternetAccess")
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.VolumeSourceType = params.get("VolumeSourceType")
        self.VolumeSizeInGB = params.get("VolumeSizeInGB")
        if params.get("VolumeSourceCFS") is not None:
            self.VolumeSourceCFS = CFSConfig()
            self.VolumeSourceCFS._deserialize(params.get("VolumeSourceCFS"))
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.LifecycleScriptId = params.get("LifecycleScriptId")
        self.DefaultCodeRepoId = params.get("DefaultCodeRepoId")
        self.AdditionalCodeRepoIds = params.get("AdditionalCodeRepoIds")
        self.AutomaticStopTime = params.get("AutomaticStopTime")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateNotebookResponse(AbstractModel):
    """CreateNotebook返回参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook标志
        :type Id: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Id = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.RequestId = params.get("RequestId")


class CreateOptimizedModelRequest(AbstractModel):
    """CreateOptimizedModel请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        :param Tags: 标签
        :type Tags: list of Tag
        """
        self.ModelAccTaskId = None
        self.Tags = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateOptimizedModelResponse(AbstractModel):
    """CreateOptimizedModel返回参数结构体

    """

    def __init__(self):
        r"""
        :param ModelId: 模型ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelId: str
        :param ModelVersionId: 模型版本ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelVersionId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ModelId = None
        self.ModelVersionId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ModelId = params.get("ModelId")
        self.ModelVersionId = params.get("ModelVersionId")
        self.RequestId = params.get("RequestId")


class CreatePreSignedTensorBoardUrlRequest(AbstractModel):
    """CreatePreSignedTensorBoardUrl请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: TensorBoard ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePreSignedTensorBoardUrlResponse(AbstractModel):
    """CreatePreSignedTensorBoardUrl返回参数结构体

    """

    def __init__(self):
        r"""
        :param Url: TensorBoard Url
        :type Url: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Url = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Url = params.get("Url")
        self.RequestId = params.get("RequestId")


class CreatePresignedNotebookUrlRequest(AbstractModel):
    """CreatePresignedNotebookUrl请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: Notebook ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreatePresignedNotebookUrlResponse(AbstractModel):
    """CreatePresignedNotebookUrl返回参数结构体

    """

    def __init__(self):
        r"""
        :param AuthorizedUrl: 携带认证TOKEN的URL
        :type AuthorizedUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AuthorizedUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AuthorizedUrl = params.get("AuthorizedUrl")
        self.RequestId = params.get("RequestId")


class CreateTensorBoardTaskRequest(AbstractModel):
    """CreateTensorBoardTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 训练任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTensorBoardTaskResponse(AbstractModel):
    """CreateTensorBoardTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TensorBoardId: TensorBoard ID
        :type TensorBoardId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TensorBoardId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TensorBoardId = params.get("TensorBoardId")
        self.RequestId = params.get("RequestId")


class CreateTrainingModelRequest(AbstractModel):
    """CreateTrainingModel请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImportMethod: 导入方式
MODEL：导入新模型
VERSION：导入新版本
EXIST：导入现有版本
        :type ImportMethod: str
        :param TrainingModelCosPath: 模型来源cos目录，以/结尾
        :type TrainingModelCosPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ReasoningEnvironmentSource: 推理环境来源（SYSTEM/CUSTOM）
        :type ReasoningEnvironmentSource: str
        :param TrainingModelName: 模型名称，不超过60个字符，仅支持中英文、数字、下划线"_"、短横"-"，只能以中英文、数字开头
        :type TrainingModelName: str
        :param Tags: 标签配置
        :type Tags: list of Tag
        :param TrainingJobName: 训练任务名称
        :type TrainingJobName: str
        :param AlgorithmFramework: 算法框架 （PYTORCH/TENSORFLOW/DETECTRON2/PMML/MMDETECTION)
        :type AlgorithmFramework: str
        :param ReasoningEnvironment: 推理环境
        :type ReasoningEnvironment: str
        :param TrainingModelIndex: 训练指标，最多支持1000字符
        :type TrainingModelIndex: str
        :param TrainingModelVersion: 模型版本
        :type TrainingModelVersion: str
        :param ReasoningImageInfo: 自定义推理环境
        :type ReasoningImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param ModelMoveMode: 模型移动方式（CUT/COPY）
        :type ModelMoveMode: str
        :param TrainingJobId: 训练任务ID
        :type TrainingJobId: str
        :param TrainingModelId: 模型ID（导入新模型不需要，导入新版本需要）
        :type TrainingModelId: str
        :param ModelOutputPath: 模型存储cos目录
        :type ModelOutputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param TrainingModelSource: 模型来源 （JOB/COS）
        :type TrainingModelSource: str
        :param TrainingPreference: 模型偏好
        :type TrainingPreference: str
        :param AutoMLTaskId: 自动学习任务ID（已废弃）
        :type AutoMLTaskId: str
        :param TrainingJobVersion: 任务版本
        :type TrainingJobVersion: str
        :param ModelVersionType: 模型版本类型；
枚举值：NORMAL(通用)  ACCELERATE(加速)
注意:  默认为NORMAL
        :type ModelVersionType: str
        :param ModelFormat: 模型格式 （PYTORCH/TORCH_SCRIPT/DETECTRON2/SAVED_MODEL/FROZEN_GRAPH/PMML/MMDETECTION/ONNX/HUGGING_FACE）
        :type ModelFormat: str
        :param ReasoningEnvironmentId: 推理镜像ID
        :type ReasoningEnvironmentId: str
        :param AutoClean: 模型自动清理开关(true/false)，当前版本仅支持SAVED_MODEL格式模型
        :type AutoClean: str
        :param MaxReservedModels: 模型数量保留上限(默认值为24个，上限为24，下限为1，步长为1)
        :type MaxReservedModels: int
        :param ModelCleanPeriod: 模型清理周期(默认值为1分钟，上限为1440，下限为1分钟，步长为1)
        :type ModelCleanPeriod: int
        :param IsQAT: 是否QAT模型
        :type IsQAT: bool
        """
        self.ImportMethod = None
        self.TrainingModelCosPath = None
        self.ReasoningEnvironmentSource = None
        self.TrainingModelName = None
        self.Tags = None
        self.TrainingJobName = None
        self.AlgorithmFramework = None
        self.ReasoningEnvironment = None
        self.TrainingModelIndex = None
        self.TrainingModelVersion = None
        self.ReasoningImageInfo = None
        self.ModelMoveMode = None
        self.TrainingJobId = None
        self.TrainingModelId = None
        self.ModelOutputPath = None
        self.TrainingModelSource = None
        self.TrainingPreference = None
        self.AutoMLTaskId = None
        self.TrainingJobVersion = None
        self.ModelVersionType = None
        self.ModelFormat = None
        self.ReasoningEnvironmentId = None
        self.AutoClean = None
        self.MaxReservedModels = None
        self.ModelCleanPeriod = None
        self.IsQAT = None


    def _deserialize(self, params):
        self.ImportMethod = params.get("ImportMethod")
        if params.get("TrainingModelCosPath") is not None:
            self.TrainingModelCosPath = CosPathInfo()
            self.TrainingModelCosPath._deserialize(params.get("TrainingModelCosPath"))
        self.ReasoningEnvironmentSource = params.get("ReasoningEnvironmentSource")
        self.TrainingModelName = params.get("TrainingModelName")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.TrainingJobName = params.get("TrainingJobName")
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.ReasoningEnvironment = params.get("ReasoningEnvironment")
        self.TrainingModelIndex = params.get("TrainingModelIndex")
        self.TrainingModelVersion = params.get("TrainingModelVersion")
        if params.get("ReasoningImageInfo") is not None:
            self.ReasoningImageInfo = ImageInfo()
            self.ReasoningImageInfo._deserialize(params.get("ReasoningImageInfo"))
        self.ModelMoveMode = params.get("ModelMoveMode")
        self.TrainingJobId = params.get("TrainingJobId")
        self.TrainingModelId = params.get("TrainingModelId")
        if params.get("ModelOutputPath") is not None:
            self.ModelOutputPath = CosPathInfo()
            self.ModelOutputPath._deserialize(params.get("ModelOutputPath"))
        self.TrainingModelSource = params.get("TrainingModelSource")
        self.TrainingPreference = params.get("TrainingPreference")
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainingJobVersion = params.get("TrainingJobVersion")
        self.ModelVersionType = params.get("ModelVersionType")
        self.ModelFormat = params.get("ModelFormat")
        self.ReasoningEnvironmentId = params.get("ReasoningEnvironmentId")
        self.AutoClean = params.get("AutoClean")
        self.MaxReservedModels = params.get("MaxReservedModels")
        self.ModelCleanPeriod = params.get("ModelCleanPeriod")
        self.IsQAT = params.get("IsQAT")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTrainingModelResponse(AbstractModel):
    """CreateTrainingModel返回参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 模型ID，TrainingModel ID
        :type Id: str
        :param TrainingModelVersionId: 模型版本ID
        :type TrainingModelVersionId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Id = None
        self.TrainingModelVersionId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.TrainingModelVersionId = params.get("TrainingModelVersionId")
        self.RequestId = params.get("RequestId")


class CreateTrainingTaskRequest(AbstractModel):
    """CreateTrainingTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Name: 训练任务名称，不超过60个字符，仅支持中英文、数字、下划线"_"、短横"-"，只能以中英文、数字开头
        :type Name: str
        :param ChargeType: 计费模式，eg：PREPAID预付费，即包年包月；POSTPAID_BY_HOUR按小时后付费
        :type ChargeType: str
        :param ResourceConfigInfos: 资源配置，需填写对应算力规格ID和节点数量，算力规格ID查询接口为DescribeBillingSpecsPrice，eg：[{"Role":"WORKER", "InstanceType": "TI.S.MEDIUM.POST", "InstanceNum": 1}]
        :type ResourceConfigInfos: list of ResourceConfigInfo
        :param CodePackagePath: COS代码包路径
        :type CodePackagePath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param TrainingMode: 训练模式，通过DescribeTrainingFrameworks接口查询，eg：PS_WORKER、DDP、MPI、HOROVOD
        :type TrainingMode: str
        :param Output: COS训练输出路径
        :type Output: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param FrameworkName: 训练框架名称，通过DescribeTrainingFrameworks接口查询，eg：SPARK、PYSPARK、TENSORFLOW、PYTORCH
        :type FrameworkName: str
        :param FrameworkVersion: 训练框架版本，通过DescribeTrainingFrameworks接口查询，eg：1.15、1.9
        :type FrameworkVersion: str
        :param FrameworkEnvironment: 训练框架环境，通过DescribeTrainingFrameworks接口查询，eg：tf1.15-py3.7-cpu、torch1.9-py3.8-cuda11.1-gpu
        :type FrameworkEnvironment: str
        :param ResourceGroupId: 预付费专用资源组ID，通过DescribeBillingResourceGroups接口查询
        :type ResourceGroupId: str
        :param Tags: 标签配置
        :type Tags: list of Tag
        :param ImageInfo: 自定义镜像信息
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param StartCmdInfo: 启动命令信息，默认为sh start.sh
        :type StartCmdInfo: :class:`tencentcloud.tione.v20211111.models.StartCmdInfo`
        :param DataConfigs: 数据配置
        :type DataConfigs: list of DataConfig
        :param VpcId: VPC Id
        :type VpcId: str
        :param SubnetId: 子网Id
        :type SubnetId: str
        :param LogConfig: CLS日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param TuningParameters: 调优参数
        :type TuningParameters: str
        :param Remark: 备注，最多500个字
        :type Remark: str
        :param TaskType: 任务类型:请求方来自哪里,eg: AutoML-train、WeData
        :type TaskType: str
        :param TaskId: 请求方携带的主键ID，eg：14141341
        :type TaskId: str
        :param DataSource: 数据来源，eg：DATASET、COS、CFS、HDFS
        :type DataSource: str
        """
        self.Name = None
        self.ChargeType = None
        self.ResourceConfigInfos = None
        self.CodePackagePath = None
        self.TrainingMode = None
        self.Output = None
        self.LogEnable = None
        self.FrameworkName = None
        self.FrameworkVersion = None
        self.FrameworkEnvironment = None
        self.ResourceGroupId = None
        self.Tags = None
        self.ImageInfo = None
        self.StartCmdInfo = None
        self.DataConfigs = None
        self.VpcId = None
        self.SubnetId = None
        self.LogConfig = None
        self.TuningParameters = None
        self.Remark = None
        self.TaskType = None
        self.TaskId = None
        self.DataSource = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.ChargeType = params.get("ChargeType")
        if params.get("ResourceConfigInfos") is not None:
            self.ResourceConfigInfos = []
            for item in params.get("ResourceConfigInfos"):
                obj = ResourceConfigInfo()
                obj._deserialize(item)
                self.ResourceConfigInfos.append(obj)
        if params.get("CodePackagePath") is not None:
            self.CodePackagePath = CosPathInfo()
            self.CodePackagePath._deserialize(params.get("CodePackagePath"))
        self.TrainingMode = params.get("TrainingMode")
        if params.get("Output") is not None:
            self.Output = CosPathInfo()
            self.Output._deserialize(params.get("Output"))
        self.LogEnable = params.get("LogEnable")
        self.FrameworkName = params.get("FrameworkName")
        self.FrameworkVersion = params.get("FrameworkVersion")
        self.FrameworkEnvironment = params.get("FrameworkEnvironment")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        if params.get("StartCmdInfo") is not None:
            self.StartCmdInfo = StartCmdInfo()
            self.StartCmdInfo._deserialize(params.get("StartCmdInfo"))
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.TuningParameters = params.get("TuningParameters")
        self.Remark = params.get("Remark")
        self.TaskType = params.get("TaskType")
        self.TaskId = params.get("TaskId")
        self.DataSource = params.get("DataSource")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CreateTrainingTaskResponse(AbstractModel):
    """CreateTrainingTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Id = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.RequestId = params.get("RequestId")


class CronInfo(AbstractModel):
    """跑批任务周期描述

    """

    def __init__(self):
        r"""
        :param CronConfig: cron配置
        :type CronConfig: str
        :param StartTime: 周期开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param EndTime: 周期结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        """
        self.CronConfig = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.CronConfig = params.get("CronConfig")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CronScaleJob(AbstractModel):
    """定时扩缩任务

    """

    def __init__(self):
        r"""
        :param Schedule: Cron表达式，标识任务的执行时间，精确到分钟级
        :type Schedule: str
        :param Name: 定时任务名
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param TargetReplicas: 目标实例数
注意：此字段可能返回 null，表示取不到有效值。
        :type TargetReplicas: int
        :param MinReplicas: 目标min
注意：此字段可能返回 null，表示取不到有效值。
        :type MinReplicas: int
        :param MaxReplicas: 目标max
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxReplicas: int
        :param ExcludeDates: 例外时间，Cron表达式，在对应时间内不执行任务。最多支持3条。
注意：此字段可能返回 null，表示取不到有效值。
        :type ExcludeDates: list of str
        """
        self.Schedule = None
        self.Name = None
        self.TargetReplicas = None
        self.MinReplicas = None
        self.MaxReplicas = None
        self.ExcludeDates = None


    def _deserialize(self, params):
        self.Schedule = params.get("Schedule")
        self.Name = params.get("Name")
        self.TargetReplicas = params.get("TargetReplicas")
        self.MinReplicas = params.get("MinReplicas")
        self.MaxReplicas = params.get("MaxReplicas")
        self.ExcludeDates = params.get("ExcludeDates")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CustomTrainingData(AbstractModel):
    """自定义指标

    """

    def __init__(self):
        r"""
        :param MetricName: 指标名
注意：此字段可能返回 null，表示取不到有效值。
        :type MetricName: str
        :param Metrics: 指标
注意：此字段可能返回 null，表示取不到有效值。
        :type Metrics: list of CustomTrainingMetric
        """
        self.MetricName = None
        self.Metrics = None


    def _deserialize(self, params):
        self.MetricName = params.get("MetricName")
        if params.get("Metrics") is not None:
            self.Metrics = []
            for item in params.get("Metrics"):
                obj = CustomTrainingMetric()
                obj._deserialize(item)
                self.Metrics.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CustomTrainingMetric(AbstractModel):
    """自定义指标

    """

    def __init__(self):
        r"""
        :param XType: X轴数据类型: TIMESTAMP; EPOCH; STEP
        :type XType: str
        :param Points: 数据点
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of CustomTrainingPoint
        """
        self.XType = None
        self.Points = None


    def _deserialize(self, params):
        self.XType = params.get("XType")
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = CustomTrainingPoint()
                obj._deserialize(item)
                self.Points.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class CustomTrainingPoint(AbstractModel):
    """自定义训练指标数据点

    """

    def __init__(self):
        r"""
        :param XValue: X值
        :type XValue: float
        :param YValue: Y值
        :type YValue: float
        """
        self.XValue = None
        self.YValue = None


    def _deserialize(self, params):
        self.XValue = params.get("XValue")
        self.YValue = params.get("YValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataArray(AbstractModel):
    """数组信息

    """

    def __init__(self):
        r"""
        :param Values: 数组信息
        :type Values: list of float
        """
        self.Values = None


    def _deserialize(self, params):
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataConfig(AbstractModel):
    """数据配置

    """

    def __init__(self):
        r"""
        :param MappingPath: 映射路径
        :type MappingPath: str
        :param DataSourceType: DATASET、COS、CFS、HDFS、WEDATA_HDFS
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSourceType: str
        :param DataSetSource: 来自数据集的数据
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSetSource: :class:`tencentcloud.tione.v20211111.models.DataSetConfig`
        :param COSSource: 来自cos的数据
注意：此字段可能返回 null，表示取不到有效值。
        :type COSSource: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param CFSSource: 来自CFS的数据
注意：此字段可能返回 null，表示取不到有效值。
        :type CFSSource: :class:`tencentcloud.tione.v20211111.models.CFSConfig`
        :param HDFSSource: 来自HDFS的数据
注意：此字段可能返回 null，表示取不到有效值。
        :type HDFSSource: :class:`tencentcloud.tione.v20211111.models.HDFSConfig`
        :param WeDataHDFSSource: 来自WEDATA_HDFS的数据
注意：此字段可能返回 null，表示取不到有效值。
        :type WeDataHDFSSource: :class:`tencentcloud.tione.v20211111.models.WeDataHDFSConfig`
        """
        self.MappingPath = None
        self.DataSourceType = None
        self.DataSetSource = None
        self.COSSource = None
        self.CFSSource = None
        self.HDFSSource = None
        self.WeDataHDFSSource = None


    def _deserialize(self, params):
        self.MappingPath = params.get("MappingPath")
        self.DataSourceType = params.get("DataSourceType")
        if params.get("DataSetSource") is not None:
            self.DataSetSource = DataSetConfig()
            self.DataSetSource._deserialize(params.get("DataSetSource"))
        if params.get("COSSource") is not None:
            self.COSSource = CosPathInfo()
            self.COSSource._deserialize(params.get("COSSource"))
        if params.get("CFSSource") is not None:
            self.CFSSource = CFSConfig()
            self.CFSSource._deserialize(params.get("CFSSource"))
        if params.get("HDFSSource") is not None:
            self.HDFSSource = HDFSConfig()
            self.HDFSSource._deserialize(params.get("HDFSSource"))
        if params.get("WeDataHDFSSource") is not None:
            self.WeDataHDFSSource = WeDataHDFSConfig()
            self.WeDataHDFSSource._deserialize(params.get("WeDataHDFSSource"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataPoint(AbstractModel):
    """数据点

    """

    def __init__(self):
        r"""
        :param Name: 指标名字
        :type Name: str
        :param Value: 值
        :type Value: float
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DataSetConfig(AbstractModel):
    """数据集结构体

    """

    def __init__(self):
        r"""
        :param Id: 数据集ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasetConfigs(AbstractModel):
    """自动学习数据集配置信息

    """

    def __init__(self):
        r"""
        :param TrainDatasetId: 自动学习训练数据集id
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainDatasetId: str
        :param ValidationDatasetId: 自动学习验证数据集id
注意：此字段可能返回 null，表示取不到有效值。
        :type ValidationDatasetId: str
        :param TestDatasetId: 自动学习测试数据集id
注意：此字段可能返回 null，表示取不到有效值。
        :type TestDatasetId: str
        """
        self.TrainDatasetId = None
        self.ValidationDatasetId = None
        self.TestDatasetId = None


    def _deserialize(self, params):
        self.TrainDatasetId = params.get("TrainDatasetId")
        self.ValidationDatasetId = params.get("ValidationDatasetId")
        self.TestDatasetId = params.get("TestDatasetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasetFileInfo(AbstractModel):
    """数据集快照存储详情

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集id
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetId: str
        :param StorageDataPath: 数据源cos 信息
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageDataPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StorageLabelPath: 数据集存储cos信息
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageLabelPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param DatasetName: 数据集名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetName: str
        :param DatasetVersion: 数据集版本
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetVersion: str
        """
        self.DatasetId = None
        self.StorageDataPath = None
        self.StorageLabelPath = None
        self.DatasetName = None
        self.DatasetVersion = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        if params.get("StorageDataPath") is not None:
            self.StorageDataPath = CosPathInfo()
            self.StorageDataPath._deserialize(params.get("StorageDataPath"))
        if params.get("StorageLabelPath") is not None:
            self.StorageLabelPath = CosPathInfo()
            self.StorageLabelPath._deserialize(params.get("StorageLabelPath"))
        self.DatasetName = params.get("DatasetName")
        self.DatasetVersion = params.get("DatasetVersion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasetGroup(AbstractModel):
    """数据集组

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetId: str
        :param DatasetName: 数据集名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetName: str
        :param Creator: 创建者
注意：此字段可能返回 null，表示取不到有效值。
        :type Creator: str
        :param DatasetVersion: 数据集版本
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetVersion: str
        :param DatasetType: 数据集类型
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetType: str
        :param DatasetTags: 数据集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetTags: list of Tag
        :param DatasetAnnotationTaskName: 数据集标注任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetAnnotationTaskName: str
        :param DatasetAnnotationTaskId: 数据集标注任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetAnnotationTaskId: str
        :param Process: 处理进度
注意：此字段可能返回 null，表示取不到有效值。
        :type Process: int
        :param DatasetStatus: 数据集状态
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetStatus: str
        :param ErrorMsg: 错误详情
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param ExternalTaskType: 外部关联TASKType
注意：此字段可能返回 null，表示取不到有效值。
        :type ExternalTaskType: str
        :param DatasetSize: 数据集大小
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetSize: str
        :param FileNum: 数据集数据量
注意：此字段可能返回 null，表示取不到有效值。
        :type FileNum: int
        :param StorageDataPath: 数据集源COS路径
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageDataPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StorageLabelPath: 数据集标签存储路径
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageLabelPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param DatasetVersions: 数据集版本聚合详情
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetVersions: list of DatasetInfo
        :param AnnotationStatus: 数据集标注状态
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationStatus: str
        :param AnnotationType: 数据集类型
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationType: str
        :param AnnotationFormat: 数据集标注格式
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationFormat: str
        :param DatasetScope: 数据集范围
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetScope: str
        :param OcrScene: 数据集OCR子场景
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrScene: str
        :param AnnotationKeyStatus: 数据集字典修改状态
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationKeyStatus: str
        """
        self.DatasetId = None
        self.DatasetName = None
        self.Creator = None
        self.DatasetVersion = None
        self.DatasetType = None
        self.DatasetTags = None
        self.DatasetAnnotationTaskName = None
        self.DatasetAnnotationTaskId = None
        self.Process = None
        self.DatasetStatus = None
        self.ErrorMsg = None
        self.CreateTime = None
        self.UpdateTime = None
        self.ExternalTaskType = None
        self.DatasetSize = None
        self.FileNum = None
        self.StorageDataPath = None
        self.StorageLabelPath = None
        self.DatasetVersions = None
        self.AnnotationStatus = None
        self.AnnotationType = None
        self.AnnotationFormat = None
        self.DatasetScope = None
        self.OcrScene = None
        self.AnnotationKeyStatus = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.DatasetName = params.get("DatasetName")
        self.Creator = params.get("Creator")
        self.DatasetVersion = params.get("DatasetVersion")
        self.DatasetType = params.get("DatasetType")
        if params.get("DatasetTags") is not None:
            self.DatasetTags = []
            for item in params.get("DatasetTags"):
                obj = Tag()
                obj._deserialize(item)
                self.DatasetTags.append(obj)
        self.DatasetAnnotationTaskName = params.get("DatasetAnnotationTaskName")
        self.DatasetAnnotationTaskId = params.get("DatasetAnnotationTaskId")
        self.Process = params.get("Process")
        self.DatasetStatus = params.get("DatasetStatus")
        self.ErrorMsg = params.get("ErrorMsg")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.ExternalTaskType = params.get("ExternalTaskType")
        self.DatasetSize = params.get("DatasetSize")
        self.FileNum = params.get("FileNum")
        if params.get("StorageDataPath") is not None:
            self.StorageDataPath = CosPathInfo()
            self.StorageDataPath._deserialize(params.get("StorageDataPath"))
        if params.get("StorageLabelPath") is not None:
            self.StorageLabelPath = CosPathInfo()
            self.StorageLabelPath._deserialize(params.get("StorageLabelPath"))
        if params.get("DatasetVersions") is not None:
            self.DatasetVersions = []
            for item in params.get("DatasetVersions"):
                obj = DatasetInfo()
                obj._deserialize(item)
                self.DatasetVersions.append(obj)
        self.AnnotationStatus = params.get("AnnotationStatus")
        self.AnnotationType = params.get("AnnotationType")
        self.AnnotationFormat = params.get("AnnotationFormat")
        self.DatasetScope = params.get("DatasetScope")
        self.OcrScene = params.get("OcrScene")
        self.AnnotationKeyStatus = params.get("AnnotationKeyStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DatasetInfo(AbstractModel):
    """数据集详情

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集id
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetId: str
        :param DatasetName: 数据集名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetName: str
        :param Creator: 数据集创建者
注意：此字段可能返回 null，表示取不到有效值。
        :type Creator: str
        :param DatasetVersion: 数据集版本
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetVersion: str
        :param DatasetType: 数据集类型
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetType: str
        :param DatasetTags: 数据集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetTags: list of Tag
        :param DatasetAnnotationTaskName: 数据集对应标注任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetAnnotationTaskName: str
        :param DatasetAnnotationTaskId: 数据集对应标注任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetAnnotationTaskId: str
        :param Process: 处理进度
注意：此字段可能返回 null，表示取不到有效值。
        :type Process: int
        :param DatasetStatus: 数据集状态
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetStatus: str
        :param ErrorMsg: 错误详情
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param CreateTime: 数据集创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 数据集更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param ExternalTaskType: 外部任务类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ExternalTaskType: str
        :param DatasetSize: 数据集存储大小
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetSize: str
        :param FileNum: 数据集数据数量
注意：此字段可能返回 null，表示取不到有效值。
        :type FileNum: int
        :param StorageDataPath: 数据集源cos 路径
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageDataPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StorageLabelPath: 数据集输出cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type StorageLabelPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param AnnotationStatus: 数据集标注状态
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationStatus: str
        :param AnnotationType: 数据集类型
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationType: str
        :param AnnotationFormat: 数据集标注格式
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationFormat: str
        :param DatasetScope: 数据集范围
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetScope: str
        :param OcrScene: 数据集OCR子场景
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrScene: str
        :param AnnotationKeyStatus: 数据集字典修改状态
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationKeyStatus: str
        """
        self.DatasetId = None
        self.DatasetName = None
        self.Creator = None
        self.DatasetVersion = None
        self.DatasetType = None
        self.DatasetTags = None
        self.DatasetAnnotationTaskName = None
        self.DatasetAnnotationTaskId = None
        self.Process = None
        self.DatasetStatus = None
        self.ErrorMsg = None
        self.CreateTime = None
        self.UpdateTime = None
        self.ExternalTaskType = None
        self.DatasetSize = None
        self.FileNum = None
        self.StorageDataPath = None
        self.StorageLabelPath = None
        self.AnnotationStatus = None
        self.AnnotationType = None
        self.AnnotationFormat = None
        self.DatasetScope = None
        self.OcrScene = None
        self.AnnotationKeyStatus = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.DatasetName = params.get("DatasetName")
        self.Creator = params.get("Creator")
        self.DatasetVersion = params.get("DatasetVersion")
        self.DatasetType = params.get("DatasetType")
        if params.get("DatasetTags") is not None:
            self.DatasetTags = []
            for item in params.get("DatasetTags"):
                obj = Tag()
                obj._deserialize(item)
                self.DatasetTags.append(obj)
        self.DatasetAnnotationTaskName = params.get("DatasetAnnotationTaskName")
        self.DatasetAnnotationTaskId = params.get("DatasetAnnotationTaskId")
        self.Process = params.get("Process")
        self.DatasetStatus = params.get("DatasetStatus")
        self.ErrorMsg = params.get("ErrorMsg")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.ExternalTaskType = params.get("ExternalTaskType")
        self.DatasetSize = params.get("DatasetSize")
        self.FileNum = params.get("FileNum")
        if params.get("StorageDataPath") is not None:
            self.StorageDataPath = CosPathInfo()
            self.StorageDataPath._deserialize(params.get("StorageDataPath"))
        if params.get("StorageLabelPath") is not None:
            self.StorageLabelPath = CosPathInfo()
            self.StorageLabelPath._deserialize(params.get("StorageLabelPath"))
        self.AnnotationStatus = params.get("AnnotationStatus")
        self.AnnotationType = params.get("AnnotationType")
        self.AnnotationFormat = params.get("AnnotationFormat")
        self.DatasetScope = params.get("DatasetScope")
        self.OcrScene = params.get("OcrScene")
        self.AnnotationKeyStatus = params.get("AnnotationKeyStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAnnotatedTaskRequest(AbstractModel):
    """DeleteAnnotatedTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 删除的任务id
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAnnotatedTaskResponse(AbstractModel):
    """DeleteAnnotatedTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 删除的任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class DeleteAutoMLNLPPredictRecordRequest(AbstractModel):
    """DeleteAutoMLNLPPredictRecord请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务Id
        :type AutoMLTaskId: str
        :param RecordId: 预测记录Id
        :type RecordId: str
        :param EMSTaskId: 推理服务任务Id
        :type EMSTaskId: str
        """
        self.AutoMLTaskId = None
        self.RecordId = None
        self.EMSTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.RecordId = params.get("RecordId")
        self.EMSTaskId = params.get("EMSTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAutoMLNLPPredictRecordResponse(AbstractModel):
    """DeleteAutoMLNLPPredictRecord返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteAutoMLTaskRequest(AbstractModel):
    """DeleteAutoMLTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        """
        self.AutoMLTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteAutoMLTaskResponse(AbstractModel):
    """DeleteAutoMLTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param AsyncTaskId: 异步任务ID
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class DeleteBatchTaskRequest(AbstractModel):
    """DeleteBatchTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        """
        self.BatchTaskId = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBatchTaskResponse(AbstractModel):
    """DeleteBatchTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteBillingResourceGroupRequest(AbstractModel):
    """DeleteBillingResourceGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        """
        self.ResourceGroupId = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBillingResourceGroupResponse(AbstractModel):
    """DeleteBillingResourceGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceGroupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.RequestId = params.get("RequestId")


class DeleteBillingResourceInstanceRequest(AbstractModel):
    """DeleteBillingResourceInstance请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceInstanceId: 资源组节点id
        :type ResourceInstanceId: str
        """
        self.ResourceInstanceId = None


    def _deserialize(self, params):
        self.ResourceInstanceId = params.get("ResourceInstanceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteBillingResourceInstanceResponse(AbstractModel):
    """DeleteBillingResourceInstance返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceInstanceId: 资源组节点id
        :type ResourceInstanceId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceInstanceId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ResourceInstanceId = params.get("ResourceInstanceId")
        self.RequestId = params.get("RequestId")


class DeleteCodeRepoRequest(AbstractModel):
    """DeleteCodeRepo请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: id值
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteCodeRepoResponse(AbstractModel):
    """DeleteCodeRepo返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteDatasetRequest(AbstractModel):
    """DeleteDataset请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集id
        :type DatasetId: str
        :param DeleteLabelEnable: 是否删除cos标签文件
        :type DeleteLabelEnable: bool
        """
        self.DatasetId = None
        self.DeleteLabelEnable = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.DeleteLabelEnable = params.get("DeleteLabelEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteDatasetResponse(AbstractModel):
    """DeleteDataset返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 删除的datasetId
        :type DatasetId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasetId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.RequestId = params.get("RequestId")


class DeleteInferGatewayRequest(AbstractModel):
    """DeleteInferGateway请求参数结构体

    """


class DeleteInferGatewayResponse(AbstractModel):
    """DeleteInferGateway返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteLifecycleScriptRequest(AbstractModel):
    """DeleteLifecycleScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 生命周期脚本ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteLifecycleScriptResponse(AbstractModel):
    """DeleteLifecycleScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteModelAccelerateTaskRequest(AbstractModel):
    """DeleteModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        """
        self.ModelAccTaskId = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteModelAccelerateTaskResponse(AbstractModel):
    """DeleteModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteModelServiceGroupRequest(AbstractModel):
    """DeleteModelServiceGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 服务id
        :type ServiceGroupId: str
        """
        self.ServiceGroupId = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteModelServiceGroupResponse(AbstractModel):
    """DeleteModelServiceGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteModelServiceRequest(AbstractModel):
    """DeleteModelService请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceId: 服务id
        :type ServiceId: str
        """
        self.ServiceId = None


    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteModelServiceResponse(AbstractModel):
    """DeleteModelService返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteNotebookRequest(AbstractModel):
    """DeleteNotebook请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook id
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteNotebookResponse(AbstractModel):
    """DeleteNotebook返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTaskProcessRequest(AbstractModel):
    """DeleteTaskProcess请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskIds: 任务ID列表
        :type TaskIds: list of str
        """
        self.TaskIds = None


    def _deserialize(self, params):
        self.TaskIds = params.get("TaskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTaskProcessResponse(AbstractModel):
    """DeleteTaskProcess返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTencentLabWhitelistRequest(AbstractModel):
    """DeleteTencentLabWhitelist请求参数结构体

    """

    def __init__(self):
        r"""
        :param ClassUin: 需要增加白名单的主uin
        :type ClassUin: str
        :param ClassSubUin: 需要增加白名单的subUin
        :type ClassSubUin: str
        :param ResourceId: Tione 平台维护的资源 ID，对应腾学会的课程 ID
        :type ResourceId: str
        """
        self.ClassUin = None
        self.ClassSubUin = None
        self.ResourceId = None


    def _deserialize(self, params):
        self.ClassUin = params.get("ClassUin")
        self.ClassSubUin = params.get("ClassSubUin")
        self.ResourceId = params.get("ResourceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTencentLabWhitelistResponse(AbstractModel):
    """DeleteTencentLabWhitelist返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTencentLabWhitelistTestRequest(AbstractModel):
    """DeleteTencentLabWhitelistTest请求参数结构体

    """

    def __init__(self):
        r"""
        :param ClassUin: 需要增加白名单的主uin
        :type ClassUin: str
        :param ClassSubUin: 需要增加白名单的subUin
        :type ClassSubUin: str
        :param ResourceId: Tione 平台维护的资源 ID，对应腾学会的课程 ID
        :type ResourceId: str
        """
        self.ClassUin = None
        self.ClassSubUin = None
        self.ResourceId = None


    def _deserialize(self, params):
        self.ClassUin = params.get("ClassUin")
        self.ClassSubUin = params.get("ClassSubUin")
        self.ResourceId = params.get("ResourceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTencentLabWhitelistTestResponse(AbstractModel):
    """DeleteTencentLabWhitelistTest返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTrainingMetricsRequest(AbstractModel):
    """DeleteTrainingMetrics请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskIds: 训练任务Id列表
        :type TaskIds: list of str
        """
        self.TaskIds = None


    def _deserialize(self, params):
        self.TaskIds = params.get("TaskIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTrainingMetricsResponse(AbstractModel):
    """DeleteTrainingMetrics返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTrainingModelRequest(AbstractModel):
    """DeleteTrainingModel请求参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelId: 模型ID
        :type TrainingModelId: str
        :param EnableDeleteCos: 是否同步清理cos
        :type EnableDeleteCos: bool
        :param ModelVersionType: 删除模型类型，枚举值：NORMAL 普通，ACCELERATE 加速，不传则删除所有
        :type ModelVersionType: str
        """
        self.TrainingModelId = None
        self.EnableDeleteCos = None
        self.ModelVersionType = None


    def _deserialize(self, params):
        self.TrainingModelId = params.get("TrainingModelId")
        self.EnableDeleteCos = params.get("EnableDeleteCos")
        self.ModelVersionType = params.get("ModelVersionType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTrainingModelResponse(AbstractModel):
    """DeleteTrainingModel返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTrainingModelVersionRequest(AbstractModel):
    """DeleteTrainingModelVersion请求参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelVersionId: 模型版本ID
        :type TrainingModelVersionId: str
        :param EnableDeleteCos: 是否同步清理cos
        :type EnableDeleteCos: bool
        """
        self.TrainingModelVersionId = None
        self.EnableDeleteCos = None


    def _deserialize(self, params):
        self.TrainingModelVersionId = params.get("TrainingModelVersionId")
        self.EnableDeleteCos = params.get("EnableDeleteCos")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTrainingModelVersionResponse(AbstractModel):
    """DeleteTrainingModelVersion返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeleteTrainingTaskRequest(AbstractModel):
    """DeleteTrainingTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeleteTrainingTaskResponse(AbstractModel):
    """DeleteTrainingTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class DeliverBillingResourceRequest(AbstractModel):
    """DeliverBillingResource请求参数结构体

    """

    def __init__(self):
        r"""
        :param TimeUnit: 节点续费的时间单位(计费周期范围)
注意：此字段为枚举值
说明：m: 月  y: 年
        :type TimeUnit: str
        :param TimeSpan: 节点续费的时间大小
注意：节点续费最大支持2年; 因此当TimeUnit为m时，此字段取值不可大于24，TimeUnit为y时，此字段取值不可大于2
        :type TimeSpan: int
        :param ResourceIds: 资源组节点id列表
注意: 单次最多100个
        :type ResourceIds: list of str
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        """
        self.TimeUnit = None
        self.TimeSpan = None
        self.ResourceIds = None
        self.ResourceGroupId = None


    def _deserialize(self, params):
        self.TimeUnit = params.get("TimeUnit")
        self.TimeSpan = params.get("TimeSpan")
        self.ResourceIds = params.get("ResourceIds")
        self.ResourceGroupId = params.get("ResourceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DeliverBillingResourceResponse(AbstractModel):
    """DeliverBillingResource返回参数结构体

    """

    def __init__(self):
        r"""
        :param FailResources: 续费失败的节点及其失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailResources: list of FailResource
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FailResources = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FailResources") is not None:
            self.FailResources = []
            for item in params.get("FailResources"):
                obj = FailResource()
                obj._deserialize(item)
                self.FailResources.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAPIConfigsRequest(AbstractModel):
    """DescribeAPIConfigs请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列
        :type Order: str
        :param OrderField: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type OrderField: str
        :param Filters: 分页参数，支持的分页过滤Name包括：
["ClusterId", "ServiceId", "ServiceGroupName", "ServiceGroupId"]
        :type Filters: list of Filter
        """
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Filters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAPIConfigsResponse(AbstractModel):
    """DescribeAPIConfigs返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 接口数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param Details: 接口详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Details: list of APIConfigDetail
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Details = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Details") is not None:
            self.Details = []
            for item in params.get("Details"):
                obj = APIConfigDetail()
                obj._deserialize(item)
                self.Details.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAnnotatedTaskListRequest(AbstractModel):
    """DescribeAnnotatedTaskList请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 页面大小，默认为10
        :type Limit: int
        :param Filters: 过滤条件数组，支持数据集ID，标注场景、任务状态、数据集名称、人物名称的过滤，后面两个支持模糊查询
        :type Filters: list of Filter
        :param TagFilters: 标签过滤条件
        :type TagFilters: list of TagFilter
        :param Order: 排序方向：Asc Desc
        :type Order: str
        :param OrderField: 排序字段
        :type OrderField: str
        """
        self.Offset = None
        self.Limit = None
        self.Filters = None
        self.TagFilters = None
        self.Order = None
        self.OrderField = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAnnotatedTaskListResponse(AbstractModel):
    """DescribeAnnotatedTaskList返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 任务列表总数量
        :type TotalCount: int
        :param TaskList: 标注任务详情列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskList: list of AnnotationTaskInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.TaskList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("TaskList") is not None:
            self.TaskList = []
            for item in params.get("TaskList"):
                obj = AnnotationTaskInfo()
                obj._deserialize(item)
                self.TaskList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAnnotationKeysRequest(AbstractModel):
    """DescribeAnnotationKeys请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        """
        self.DatasetId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAnnotationKeysResponse(AbstractModel):
    """DescribeAnnotationKeys返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param InUpdating: 当前是否处于更新之中
注意：此字段可能返回 null，表示取不到有效值。
        :type InUpdating: bool
        :param LastUpdateStatus: 上一次更新的结果是否成功
注意：此字段可能返回 null，表示取不到有效值。
        :type LastUpdateStatus: bool
        :param LastUpdateMsg: 上一次更新的报错信息
注意：此字段可能返回 null，表示取不到有效值。
        :type LastUpdateMsg: str
        :param LastUpdateKeyType: 上一次更新的KeyType
注意：此字段可能返回 null，表示取不到有效值。
        :type LastUpdateKeyType: int
        :param Version: ver
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param StandardKeySet: 标注key名字典
注意：此字段可能返回 null，表示取不到有效值。
        :type StandardKeySet: :class:`tencentcloud.tione.v20211111.models.KeySetType`
        :param AdditionalKeySet: 标注key名字典
注意：此字段可能返回 null，表示取不到有效值。
        :type AdditionalKeySet: :class:`tencentcloud.tione.v20211111.models.KeySetType`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasetId = None
        self.InUpdating = None
        self.LastUpdateStatus = None
        self.LastUpdateMsg = None
        self.LastUpdateKeyType = None
        self.Version = None
        self.StandardKeySet = None
        self.AdditionalKeySet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.InUpdating = params.get("InUpdating")
        self.LastUpdateStatus = params.get("LastUpdateStatus")
        self.LastUpdateMsg = params.get("LastUpdateMsg")
        self.LastUpdateKeyType = params.get("LastUpdateKeyType")
        self.Version = params.get("Version")
        if params.get("StandardKeySet") is not None:
            self.StandardKeySet = KeySetType()
            self.StandardKeySet._deserialize(params.get("StandardKeySet"))
        if params.get("AdditionalKeySet") is not None:
            self.AdditionalKeySet = KeySetType()
            self.AdditionalKeySet._deserialize(params.get("AdditionalKeySet"))
        self.RequestId = params.get("RequestId")


class DescribeAutoMLEMSAPIInfoRequest(AbstractModel):
    """DescribeAutoMLEMSAPIInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务创建任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
        :type EMSTaskId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLEMSAPIInfoResponse(AbstractModel):
    """DescribeAutoMLEMSAPIInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务创建任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskId: str
        :param InnerUrl: 发布模型服务接口内网调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type InnerUrl: str
        :param OuterUrl: 发布模型服务接口外网调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type OuterUrl: str
        :param UrlInfo: 发布模型服务前端展示地址链接
注意：此字段可能返回 null，表示取不到有效值。
        :type UrlInfo: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.InnerUrl = None
        self.OuterUrl = None
        self.UrlInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.InnerUrl = params.get("InnerUrl")
        self.OuterUrl = params.get("OuterUrl")
        self.UrlInfo = params.get("UrlInfo")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLEMSTaskRequest(AbstractModel):
    """DescribeAutoMLEMSTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
        :type EMSTaskId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLEMSTaskResponse(AbstractModel):
    """DescribeAutoMLEMSTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskId: str
        :param EMSTaskBusinessStatus: 发布模型服务business状态，包括CREATING(创建中), CREATE_FAILED(创建失败), ARREARS_STOP(因欠费被强制停止)
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskBusinessStatus: str
        :param EMSTaskWorkloadStatus: 模型服务实例状态, Normal(运行中), Pending(启动中), Abnormal(服务异常), Stopping(服务停止中), Stopped(服务已停止)
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskWorkloadStatus: str
        :param Scene: 自动学习场景
注意：此字段可能返回 null，表示取不到有效值。
        :type Scene: :class:`tencentcloud.tione.v20211111.models.Scene`
        :param ChargeType: 付费模式，PREPAID(预付费), POSTPAID_BY_HOUR(后付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param MaxServiceHours: 模型服务最大运行时间，没设置则返回-1
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxServiceHours: int
        :param EMSServiceGroupId: 发布模型服务服务组id
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSServiceGroupId: str
        :param EMSServiceId: 发布模型服务服务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSServiceId: str
        :param ResourceGroupId: 预付费资源组id
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param PublishResourceInfo: 发布模型服务资源配置信息
注意：此字段可能返回 null，表示取不到有效值。
        :type PublishResourceInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        :param TaskOutputCosInfo: 自动学习任务模型输出cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskOutputCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ErrorMsg: 出现异常时错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param UserCosInfo: 保存文件的Cos信息
注意：此字段可能返回 null，表示取不到有效值。
        :type UserCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.EMSTaskBusinessStatus = None
        self.EMSTaskWorkloadStatus = None
        self.Scene = None
        self.ChargeType = None
        self.MaxServiceHours = None
        self.EMSServiceGroupId = None
        self.EMSServiceId = None
        self.ResourceGroupId = None
        self.PublishResourceInfo = None
        self.TaskOutputCosInfo = None
        self.ErrorMsg = None
        self.UserCosInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.EMSTaskBusinessStatus = params.get("EMSTaskBusinessStatus")
        self.EMSTaskWorkloadStatus = params.get("EMSTaskWorkloadStatus")
        if params.get("Scene") is not None:
            self.Scene = Scene()
            self.Scene._deserialize(params.get("Scene"))
        self.ChargeType = params.get("ChargeType")
        self.MaxServiceHours = params.get("MaxServiceHours")
        self.EMSServiceGroupId = params.get("EMSServiceGroupId")
        self.EMSServiceId = params.get("EMSServiceId")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("PublishResourceInfo") is not None:
            self.PublishResourceInfo = ResourceConfigInfo()
            self.PublishResourceInfo._deserialize(params.get("PublishResourceInfo"))
        if params.get("TaskOutputCosInfo") is not None:
            self.TaskOutputCosInfo = CosPathInfo()
            self.TaskOutputCosInfo._deserialize(params.get("TaskOutputCosInfo"))
        self.ErrorMsg = params.get("ErrorMsg")
        if params.get("UserCosInfo") is not None:
            self.UserCosInfo = CosPathInfo()
            self.UserCosInfo._deserialize(params.get("UserCosInfo"))
        self.RequestId = params.get("RequestId")


class DescribeAutoMLEMSTasksRequest(AbstractModel):
    """DescribeAutoMLEMSTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 业务关联过滤条件
        :type Filters: list of Filter
        :param TagFilters: 标签关联过滤条件
        :type TagFilters: list of TagFilter
        :param Offset: 偏移量，默认0
        :type Offset: int
        :param Limit: 结果限制数量，默认10
        :type Limit: int
        :param OrderField: 结果排序业务字段, 默认自动学习任务创建时间
        :type OrderField: str
        :param Order: 结果排序规则，ASC(升序), DESC(降序)
        :type Order: str
        """
        self.Filters = None
        self.TagFilters = None
        self.Offset = None
        self.Limit = None
        self.OrderField = None
        self.Order = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLEMSTasksResponse(AbstractModel):
    """DescribeAutoMLEMSTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 满足条件的模型发布任务总数量
        :type TotalCount: int
        :param EMSTaskGroups: 满足条件的模型服务列表
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskGroups: list of EMSTaskGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.EMSTaskGroups = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("EMSTaskGroups") is not None:
            self.EMSTaskGroups = []
            for item in params.get("EMSTaskGroups"):
                obj = EMSTaskGroup()
                obj._deserialize(item)
                self.EMSTaskGroups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAutoMLEMSTasksTrainLabelsRequest(AbstractModel):
    """DescribeAutoMLEMSTasksTrainLabels请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 推理任务任务id
        :type EMSTaskId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLEMSTasksTrainLabelsResponse(AbstractModel):
    """DescribeAutoMLEMSTasksTrainLabels返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 推理任务任务id
        :type EMSTaskId: str
        :param LabelResults: 标注的key数组
        :type LabelResults: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.LabelResults = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.LabelResults = params.get("LabelResults")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLEvaluationTaskStatusRequest(AbstractModel):
    """DescribeAutoMLEvaluationTaskStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLEvaluationTaskStatusResponse(AbstractModel):
    """DescribeAutoMLEvaluationTaskStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 查询评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 查询评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param TaskStatus: 评测任务当前状态，状态类型NOTSTART(未创建评测任务), WAITING(排队中),INIT(初始化中), STARTING(启动中), RUNNING(运行中), FAILED(异常), STOPPING(停止中), STOPPED(已停止), SUCCEED(已完成)
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskStatus: str
        :param TaskProgress: 评测任务进度百分比，范围为[0, 100]
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskProgress: int
        :param ErrorMsg: 任务异常信息，当TaskStatus为FAILED时返回
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param WaitNumber: 前面排队任务数量，当TaskStatus为WAITING时返回
注意：此字段可能返回 null，表示取不到有效值。
        :type WaitNumber: int
        :param InputTestDatasetIds: 输入评测数据集
注意：此字段可能返回 null，表示取不到有效值。
        :type InputTestDatasetIds: list of str
        :param InputTestDatasetLabels: 输入评测数据标签
注意：此字段可能返回 null，表示取不到有效值。
        :type InputTestDatasetLabels: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.TaskStatus = None
        self.TaskProgress = None
        self.ErrorMsg = None
        self.WaitNumber = None
        self.InputTestDatasetIds = None
        self.InputTestDatasetLabels = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.TaskStatus = params.get("TaskStatus")
        self.TaskProgress = params.get("TaskProgress")
        self.ErrorMsg = params.get("ErrorMsg")
        self.WaitNumber = params.get("WaitNumber")
        self.InputTestDatasetIds = params.get("InputTestDatasetIds")
        self.InputTestDatasetLabels = params.get("InputTestDatasetLabels")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLEvaluationTasksRequest(AbstractModel):
    """DescribeAutoMLEvaluationTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 业务关联过滤条件
        :type Filters: list of Filter
        :param TagFilters: 标签关联过滤条件
        :type TagFilters: list of TagFilter
        :param Offset: 偏移量，默认0
        :type Offset: int
        :param Limit: 结果限制数量，默认10
        :type Limit: int
        :param OrderField: 结果排序业务字段, 默认自动学习任务创建时间
        :type OrderField: str
        :param Order: 结果排序规则，ASC(升序), DESC(降序)
        :type Order: str
        """
        self.Filters = None
        self.TagFilters = None
        self.Offset = None
        self.Limit = None
        self.OrderField = None
        self.Order = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLEvaluationTasksResponse(AbstractModel):
    """DescribeAutoMLEvaluationTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 满足条件的评测任务总数量
        :type TotalCount: int
        :param EvaluationTaskGroups: 评测任务列表详情
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskGroups: list of EvaluationTaskGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.EvaluationTaskGroups = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("EvaluationTaskGroups") is not None:
            self.EvaluationTaskGroups = []
            for item in params.get("EvaluationTaskGroups"):
                obj = EvaluationTaskGroup()
                obj._deserialize(item)
                self.EvaluationTaskGroups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAutoMLModelServiceInfoRequest(AbstractModel):
    """DescribeAutoMLModelServiceInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        """
        self.AutoMLTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLModelServiceInfoResponse(AbstractModel):
    """DescribeAutoMLModelServiceInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        :param ModelId: 模型ID
        :type ModelId: str
        :param ModelVersionId: 模型版本ID
        :type ModelVersionId: str
        :param ModelName: 模型名称
        :type ModelName: str
        :param ModelVersion: 模型版本
        :type ModelVersion: str
        :param ImageInfo: GPU环境镜像
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.ModelId = None
        self.ModelVersionId = None
        self.ModelName = None
        self.ModelVersion = None
        self.ImageInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.ModelId = params.get("ModelId")
        self.ModelVersionId = params.get("ModelVersionId")
        self.ModelName = params.get("ModelName")
        self.ModelVersion = params.get("ModelVersion")
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        self.RequestId = params.get("RequestId")


class DescribeAutoMLNLPPredictRecordsRequest(AbstractModel):
    """DescribeAutoMLNLPPredictRecords请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务Id
        :type AutoMLTaskId: str
        :param EMSTaskId: 推理服务任务Id
        :type EMSTaskId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLNLPPredictRecordsResponse(AbstractModel):
    """DescribeAutoMLNLPPredictRecords返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务Id
        :type AutoMLTaskId: str
        :param EMSTaskId: 推理服务任务Id
        :type EMSTaskId: str
        :param PredictResults: 预测结果
        :type PredictResults: list of NLPSamplePredictResult
        :param InferUrl: 当前服务请求地址
        :type InferUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.PredictResults = None
        self.InferUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        if params.get("PredictResults") is not None:
            self.PredictResults = []
            for item in params.get("PredictResults"):
                obj = NLPSamplePredictResult()
                obj._deserialize(item)
                self.PredictResults.append(obj)
        self.InferUrl = params.get("InferUrl")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskConfigRequest(AbstractModel):
    """DescribeAutoMLTaskConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        """
        self.AutoMLTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskConfigResponse(AbstractModel):
    """DescribeAutoMLTaskConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param CommonConfig: 基础配置
注意：此字段可能返回 null，表示取不到有效值。
        :type CommonConfig: :class:`tencentcloud.tione.v20211111.models.CommonConfig`
        :param DataConfig: 数据配置
注意：此字段可能返回 null，表示取不到有效值。
        :type DataConfig: :class:`tencentcloud.tione.v20211111.models.MLDataConfig`
        :param TaskOutputCosInfo: 自动学习任务输出COS
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskOutputCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelTrainConfig: 模型训练参数配置
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelTrainConfig: :class:`tencentcloud.tione.v20211111.models.ModelTrainConfig`
        :param ModelParamConfig: 模型超参数
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelParamConfig: str
        :param TrainResourceConfig: 训练资源配置
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainResourceConfig: :class:`tencentcloud.tione.v20211111.models.TrainResourceConfig`
        :param Tags: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param TaskSource: 任务来源
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskSource: str
        :param AutoMLTaskId: 自动学习任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoMLTaskId: str
        :param AutoMLTaskGroupId: 任务组
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoMLTaskGroupId: str
        :param TrainTaskId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param EvaluationTaskId: 评测任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param EMSTaskId: 在线服务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CommonConfig = None
        self.DataConfig = None
        self.TaskOutputCosInfo = None
        self.ModelTrainConfig = None
        self.ModelParamConfig = None
        self.TrainResourceConfig = None
        self.Tags = None
        self.TaskSource = None
        self.AutoMLTaskId = None
        self.AutoMLTaskGroupId = None
        self.TrainTaskId = None
        self.EvaluationTaskId = None
        self.EMSTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CommonConfig") is not None:
            self.CommonConfig = CommonConfig()
            self.CommonConfig._deserialize(params.get("CommonConfig"))
        if params.get("DataConfig") is not None:
            self.DataConfig = MLDataConfig()
            self.DataConfig._deserialize(params.get("DataConfig"))
        if params.get("TaskOutputCosInfo") is not None:
            self.TaskOutputCosInfo = CosPathInfo()
            self.TaskOutputCosInfo._deserialize(params.get("TaskOutputCosInfo"))
        if params.get("ModelTrainConfig") is not None:
            self.ModelTrainConfig = ModelTrainConfig()
            self.ModelTrainConfig._deserialize(params.get("ModelTrainConfig"))
        self.ModelParamConfig = params.get("ModelParamConfig")
        if params.get("TrainResourceConfig") is not None:
            self.TrainResourceConfig = TrainResourceConfig()
            self.TrainResourceConfig._deserialize(params.get("TrainResourceConfig"))
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.TaskSource = params.get("TaskSource")
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.AutoMLTaskGroupId = params.get("AutoMLTaskGroupId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskEvaluationBadcasesRequest(AbstractModel):
    """DescribeAutoMLTaskEvaluationBadcases请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param Threshold: 阈值
        :type Threshold: float
        :param GroundTruthLabels: groundTruth标签过滤数组
        :type GroundTruthLabels: list of str
        :param PredictLabels: 模型推理结果标签过滤数据
        :type PredictLabels: list of str
        :param Offset: 偏移量，默认0
        :type Offset: int
        :param Limit: 结果大小限制，默认10
        :type Limit: int
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Threshold = None
        self.GroundTruthLabels = None
        self.PredictLabels = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Threshold = params.get("Threshold")
        self.GroundTruthLabels = params.get("GroundTruthLabels")
        self.PredictLabels = params.get("PredictLabels")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskEvaluationBadcasesResponse(AbstractModel):
    """DescribeAutoMLTaskEvaluationBadcases返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param Threshold: 阈值
注意：此字段可能返回 null，表示取不到有效值。
        :type Threshold: float
        :param TotalCount: 总的badcase数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param ImageInfos: badcase图像列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageInfos: list of BadcaseImageInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Threshold = None
        self.TotalCount = None
        self.ImageInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Threshold = params.get("Threshold")
        self.TotalCount = params.get("TotalCount")
        if params.get("ImageInfos") is not None:
            self.ImageInfos = []
            for item in params.get("ImageInfos"):
                obj = BadcaseImageInfo()
                obj._deserialize(item)
                self.ImageInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskEvaluationBaseIndicatorsRequest(AbstractModel):
    """DescribeAutoMLTaskEvaluationBaseIndicators请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param Threshold: 评测结果指标对应的阈值，不填默认0.5
        :type Threshold: float
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Threshold = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Threshold = params.get("Threshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskEvaluationBaseIndicatorsResponse(AbstractModel):
    """DescribeAutoMLTaskEvaluationBaseIndicators返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param EvaluationTaskStatus: 评测任务状态
        :type EvaluationTaskStatus: str
        :param Accuracy: 请求阈值下的精度
注意：此字段可能返回 null，表示取不到有效值。
        :type Accuracy: float
        :param Recall: 请求阈值下的召回率
注意：此字段可能返回 null，表示取不到有效值。
        :type Recall: float
        :param FScore: 请求阈值下的f1-score
注意：此字段可能返回 null，表示取不到有效值。
        :type FScore: float
        :param MAP: 请求阈值下的mAP
注意：此字段可能返回 null，表示取不到有效值。
        :type MAP: float
        :param Threshold: 请求阈值
注意：此字段可能返回 null，表示取不到有效值。
        :type Threshold: float
        :param NLPItems: NLP基础指标
注意：此字段可能返回 null，表示取不到有效值。
        :type NLPItems: list of NLPIndicatorItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.EvaluationTaskStatus = None
        self.Accuracy = None
        self.Recall = None
        self.FScore = None
        self.MAP = None
        self.Threshold = None
        self.NLPItems = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.EvaluationTaskStatus = params.get("EvaluationTaskStatus")
        self.Accuracy = params.get("Accuracy")
        self.Recall = params.get("Recall")
        self.FScore = params.get("FScore")
        self.MAP = params.get("MAP")
        self.Threshold = params.get("Threshold")
        if params.get("NLPItems") is not None:
            self.NLPItems = []
            for item in params.get("NLPItems"):
                obj = NLPIndicatorItem()
                obj._deserialize(item)
                self.NLPItems.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskEvaluationDetailRequest(AbstractModel):
    """DescribeAutoMLTaskEvaluationDetail请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param Threshold: 指定阈值，阈值范围为[0.05, 0.95]，步长为0.05
        :type Threshold: float
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Threshold = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Threshold = params.get("Threshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskEvaluationDetailResponse(AbstractModel):
    """DescribeAutoMLTaskEvaluationDetail返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param TestDatasetIds: 评测任务有效数据集列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TestDatasetIds: list of str
        :param TestDatasetLabels: 参与评测有效标签列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TestDatasetLabels: list of str
        :param ImgNums: 参与评测的有效图像数据量
注意：此字段可能返回 null，表示取不到有效值。
        :type ImgNums: int
        :param BadCaseNums: 查询阈值下的badcase数量
注意：此字段可能返回 null，表示取不到有效值。
        :type BadCaseNums: int
        :param Scene: 评测任务场景信息详情
注意：此字段可能返回 null，表示取不到有效值。
        :type Scene: :class:`tencentcloud.tione.v20211111.models.Scene`
        :param EvaluationCostSeconds: 评测任务运行时长，单位秒
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationCostSeconds: int
        :param TxtNums: 文本数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TxtNums: int
        :param NLPItems: “题目”查询参数扩展
注意：此字段可能返回 null，表示取不到有效值。
        :type NLPItems: list of NLPItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.TestDatasetIds = None
        self.TestDatasetLabels = None
        self.ImgNums = None
        self.BadCaseNums = None
        self.Scene = None
        self.EvaluationCostSeconds = None
        self.TxtNums = None
        self.NLPItems = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.TestDatasetIds = params.get("TestDatasetIds")
        self.TestDatasetLabels = params.get("TestDatasetLabels")
        self.ImgNums = params.get("ImgNums")
        self.BadCaseNums = params.get("BadCaseNums")
        if params.get("Scene") is not None:
            self.Scene = Scene()
            self.Scene._deserialize(params.get("Scene"))
        self.EvaluationCostSeconds = params.get("EvaluationCostSeconds")
        self.TxtNums = params.get("TxtNums")
        if params.get("NLPItems") is not None:
            self.NLPItems = []
            for item in params.get("NLPItems"):
                obj = NLPItem()
                obj._deserialize(item)
                self.NLPItems.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskEvaluationSeniorIndicatorsRequest(AbstractModel):
    """DescribeAutoMLTaskEvaluationSeniorIndicators请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param Thresholds: 每个标签对应的阈值信息，不填默认所有标签用默认的0.5，填一个表示所有标签的阈值一样
        :type Thresholds: list of float
        :param MaxConfusionMatrixSize: 返回的最大混淆矩阵大小，超过的则截断返回; 默认:0; 不截断，全部返回
        :type MaxConfusionMatrixSize: int
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Thresholds = None
        self.MaxConfusionMatrixSize = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Thresholds = params.get("Thresholds")
        self.MaxConfusionMatrixSize = params.get("MaxConfusionMatrixSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskEvaluationSeniorIndicatorsResponse(AbstractModel):
    """DescribeAutoMLTaskEvaluationSeniorIndicators返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param TestLabels: 评测标签列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TestLabels: list of str
        :param Thresholds: 评测结果每个标签对应的阈值列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Thresholds: list of float
        :param Precisions: 评测结果每个标签对应的精度信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Precisions: list of float
        :param Recalls: 评测结果每个标签对应的召回率信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Recalls: list of float
        :param FScores: 评测结果每个标签对应的f1-score信息
注意：此字段可能返回 null，表示取不到有效值。
        :type FScores: list of float
        :param MAP: 评测结果每个标签对应的mAP信息
注意：此字段可能返回 null，表示取不到有效值。
        :type MAP: list of float
        :param PRValues: pr曲线详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type PRValues: list of PRValue
        :param ConfusionMatrix: 混淆矩阵
注意：此字段可能返回 null，表示取不到有效值。
        :type ConfusionMatrix: list of DataArray
        :param MultiLabel: NLP是否为多标签
注意：此字段可能返回 null，表示取不到有效值。
        :type MultiLabel: bool
        :param Accuracies: NLP的分类别准确率
注意：此字段可能返回 null，表示取不到有效值。
        :type Accuracies: list of float
        :param MacroFScores: NLP的宏平均
注意：此字段可能返回 null，表示取不到有效值。
        :type MacroFScores: list of float
        :param MicroFScores: NLP的微平均
注意：此字段可能返回 null，表示取不到有效值。
        :type MicroFScores: list of float
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.TestLabels = None
        self.Thresholds = None
        self.Precisions = None
        self.Recalls = None
        self.FScores = None
        self.MAP = None
        self.PRValues = None
        self.ConfusionMatrix = None
        self.MultiLabel = None
        self.Accuracies = None
        self.MacroFScores = None
        self.MicroFScores = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.TestLabels = params.get("TestLabels")
        self.Thresholds = params.get("Thresholds")
        self.Precisions = params.get("Precisions")
        self.Recalls = params.get("Recalls")
        self.FScores = params.get("FScores")
        self.MAP = params.get("MAP")
        if params.get("PRValues") is not None:
            self.PRValues = []
            for item in params.get("PRValues"):
                obj = PRValue()
                obj._deserialize(item)
                self.PRValues.append(obj)
        if params.get("ConfusionMatrix") is not None:
            self.ConfusionMatrix = []
            for item in params.get("ConfusionMatrix"):
                obj = DataArray()
                obj._deserialize(item)
                self.ConfusionMatrix.append(obj)
        self.MultiLabel = params.get("MultiLabel")
        self.Accuracies = params.get("Accuracies")
        self.MacroFScores = params.get("MacroFScores")
        self.MicroFScores = params.get("MicroFScores")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskNLPEvaluationBadcasesRequest(AbstractModel):
    """DescribeAutoMLTaskNLPEvaluationBadcases请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: NLP评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        :param Topic: 题目
        :type Topic: str
        :param PreviewRange: 查询范围
        :type PreviewRange: str
        :param Offset: 偏移量，默认0
        :type Offset: int
        :param Limit: 结果大小限制，默认10
        :type Limit: int
        :param NLPTagFilters: 过滤
        :type NLPTagFilters: list of NLPTagFilter
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.Topic = None
        self.PreviewRange = None
        self.Offset = None
        self.Limit = None
        self.NLPTagFilters = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.Topic = params.get("Topic")
        self.PreviewRange = params.get("PreviewRange")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("NLPTagFilters") is not None:
            self.NLPTagFilters = []
            for item in params.get("NLPTagFilters"):
                obj = NLPTagFilter()
                obj._deserialize(item)
                self.NLPTagFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskNLPEvaluationBadcasesResponse(AbstractModel):
    """DescribeAutoMLTaskNLPEvaluationBadcases返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: NLP评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param TotalCount: 总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param NLPBadcaseItems: NLP badcase数组
注意：此字段可能返回 null，表示取不到有效值。
        :type NLPBadcaseItems: list of NLPBadcaseItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.TotalCount = None
        self.NLPBadcaseItems = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.TotalCount = params.get("TotalCount")
        if params.get("NLPBadcaseItems") is not None:
            self.NLPBadcaseItems = []
            for item in params.get("NLPBadcaseItems"):
                obj = NLPBadcaseItem()
                obj._deserialize(item)
                self.NLPBadcaseItems.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskTrainDetailRequest(AbstractModel):
    """DescribeAutoMLTaskTrainDetail请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskTrainDetailResponse(AbstractModel):
    """DescribeAutoMLTaskTrainDetail返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param TrainTimeUsedSecond: 训练耗时
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTimeUsedSecond: int
        :param TrainTimeExpectedSecond: 训练预估耗时
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTimeExpectedSecond: int
        :param TrainTimeMaxSecond: 训练最大时长
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTimeMaxSecond: int
        :param TrainProgress: 训练进度
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainProgress: int
        :param TrainTaskStatus: 训练任务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskStatus: str
        :param TrainErrorMessage: 训练失败时错误详情
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainErrorMessage: str
        :param TrainStartTime: 训练开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainStartTime: str
        :param TrainEndTime: 训练结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainEndTime: float
        :param TrainingTaskInfos: 任务式建模任务详情
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingTaskInfos: list of TrainingTaskInfo
        :param ModelAccTaskStatus: 模型优化任务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskStatus: str
        :param OptimizationResult: 模型优化任务报告
注意：此字段可能返回 null，表示取不到有效值。
        :type OptimizationResult: :class:`tencentcloud.tione.v20211111.models.OptimizationResult`
        :param ModelAccErrorMessage: 模型优化时错误详情
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccErrorMessage: str
        :param ModelAccTaskProgress: 模型优化任务进度
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskProgress: int
        :param ModelAccRunningSeconds: 模型优化耗时
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccRunningSeconds: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.TrainTimeUsedSecond = None
        self.TrainTimeExpectedSecond = None
        self.TrainTimeMaxSecond = None
        self.TrainProgress = None
        self.TrainTaskStatus = None
        self.TrainErrorMessage = None
        self.TrainStartTime = None
        self.TrainEndTime = None
        self.TrainingTaskInfos = None
        self.ModelAccTaskStatus = None
        self.OptimizationResult = None
        self.ModelAccErrorMessage = None
        self.ModelAccTaskProgress = None
        self.ModelAccRunningSeconds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.TrainTimeUsedSecond = params.get("TrainTimeUsedSecond")
        self.TrainTimeExpectedSecond = params.get("TrainTimeExpectedSecond")
        self.TrainTimeMaxSecond = params.get("TrainTimeMaxSecond")
        self.TrainProgress = params.get("TrainProgress")
        self.TrainTaskStatus = params.get("TrainTaskStatus")
        self.TrainErrorMessage = params.get("TrainErrorMessage")
        self.TrainStartTime = params.get("TrainStartTime")
        self.TrainEndTime = params.get("TrainEndTime")
        if params.get("TrainingTaskInfos") is not None:
            self.TrainingTaskInfos = []
            for item in params.get("TrainingTaskInfos"):
                obj = TrainingTaskInfo()
                obj._deserialize(item)
                self.TrainingTaskInfos.append(obj)
        self.ModelAccTaskStatus = params.get("ModelAccTaskStatus")
        if params.get("OptimizationResult") is not None:
            self.OptimizationResult = OptimizationResult()
            self.OptimizationResult._deserialize(params.get("OptimizationResult"))
        self.ModelAccErrorMessage = params.get("ModelAccErrorMessage")
        self.ModelAccTaskProgress = params.get("ModelAccTaskProgress")
        self.ModelAccRunningSeconds = params.get("ModelAccRunningSeconds")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTaskTrainIndicatorsRequest(AbstractModel):
    """DescribeAutoMLTaskTrainIndicators请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTaskTrainIndicatorsResponse(AbstractModel):
    """DescribeAutoMLTaskTrainIndicators返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param Scene: 场景
注意：此字段可能返回 null，表示取不到有效值。
        :type Scene: :class:`tencentcloud.tione.v20211111.models.Scene`
        :param Epochs: 迭代id
注意：此字段可能返回 null，表示取不到有效值。
        :type Epochs: list of int non-negative
        :param Accuracy: 准确率
注意：此字段可能返回 null，表示取不到有效值。
        :type Accuracy: list of float
        :param AccTop1: top1准确率
注意：此字段可能返回 null，表示取不到有效值。
        :type AccTop1: list of float
        :param AccTop5: top5准确率
注意：此字段可能返回 null，表示取不到有效值。
        :type AccTop5: list of float
        :param Loss: 损失值
注意：此字段可能返回 null，表示取不到有效值。
        :type Loss: list of float
        :param MAP: 检测mAP
注意：此字段可能返回 null，表示取不到有效值。
        :type MAP: list of float
        :param TrainTimeUsedSecond: 已运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTimeUsedSecond: int
        :param TrainTimeExpectedSecond: 预计运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTimeExpectedSecond: int
        :param TrainTimeMaxSecond: 最长运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTimeMaxSecond: int
        :param TrainProgress: 训练进度
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainProgress: int
        :param TrainTaskStatus: 任务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskStatus: str
        :param TrainErrorMessage: 错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainErrorMessage: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.Scene = None
        self.Epochs = None
        self.Accuracy = None
        self.AccTop1 = None
        self.AccTop5 = None
        self.Loss = None
        self.MAP = None
        self.TrainTimeUsedSecond = None
        self.TrainTimeExpectedSecond = None
        self.TrainTimeMaxSecond = None
        self.TrainProgress = None
        self.TrainTaskStatus = None
        self.TrainErrorMessage = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        if params.get("Scene") is not None:
            self.Scene = Scene()
            self.Scene._deserialize(params.get("Scene"))
        self.Epochs = params.get("Epochs")
        self.Accuracy = params.get("Accuracy")
        self.AccTop1 = params.get("AccTop1")
        self.AccTop5 = params.get("AccTop5")
        self.Loss = params.get("Loss")
        self.MAP = params.get("MAP")
        self.TrainTimeUsedSecond = params.get("TrainTimeUsedSecond")
        self.TrainTimeExpectedSecond = params.get("TrainTimeExpectedSecond")
        self.TrainTimeMaxSecond = params.get("TrainTimeMaxSecond")
        self.TrainProgress = params.get("TrainProgress")
        self.TrainTaskStatus = params.get("TrainTaskStatus")
        self.TrainErrorMessage = params.get("TrainErrorMessage")
        self.RequestId = params.get("RequestId")


class DescribeAutoMLTrainTasksRequest(AbstractModel):
    """DescribeAutoMLTrainTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤条件
        :type Filters: list of Filter
        :param TagFilters: 标签过滤条件
        :type TagFilters: list of TagFilter
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回个数
        :type Limit: int
        :param OrderField: 排序字段
        :type OrderField: str
        :param Order: 排序方式
        :type Order: str
        """
        self.Filters = None
        self.TagFilters = None
        self.Offset = None
        self.Limit = None
        self.OrderField = None
        self.Order = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoMLTrainTasksResponse(AbstractModel):
    """DescribeAutoMLTrainTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TrainTaskGroups: 训练任务组列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskGroups: list of TrainTaskGroup
        :param TotalCount: 总个数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrainTaskGroups = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TrainTaskGroups") is not None:
            self.TrainTaskGroups = []
            for item in params.get("TrainTaskGroups"):
                obj = TrainTaskGroup()
                obj._deserialize(item)
                self.TrainTaskGroups.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeAutoOcrPredictionRequest(AbstractModel):
    """DescribeAutoOcrPrediction请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param FileId: 文件id
        :type FileId: str
        :param Pts: 坐标
        :type Pts: list of Point
        :param RotateAngle: 旋转角度，支持0，90，180，270，360
        :type RotateAngle: int
        """
        self.TaskId = None
        self.FileId = None
        self.Pts = None
        self.RotateAngle = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.FileId = params.get("FileId")
        if params.get("Pts") is not None:
            self.Pts = []
            for item in params.get("Pts"):
                obj = Point()
                obj._deserialize(item)
                self.Pts.append(obj)
        self.RotateAngle = params.get("RotateAngle")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeAutoOcrPredictionResponse(AbstractModel):
    """DescribeAutoOcrPrediction返回参数结构体

    """

    def __init__(self):
        r"""
        :param Value: 预测结果
        :type Value: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Value = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Value = params.get("Value")
        self.RequestId = params.get("RequestId")


class DescribeBadcasePreviewStatusRequest(AbstractModel):
    """DescribeBadcasePreviewStatus请求参数结构体

    """


class DescribeBadcasePreviewStatusResponse(AbstractModel):
    """DescribeBadcasePreviewStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param PreviewStatus: 预览开关状态，有OFF(关闭), ON(开启)
注意：此字段可能返回 null，表示取不到有效值。
        :type PreviewStatus: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PreviewStatus = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PreviewStatus = params.get("PreviewStatus")
        self.RequestId = params.get("RequestId")


class DescribeBatchTaskInstancesRequest(AbstractModel):
    """DescribeBatchTaskInstances请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务id
        :type BatchTaskId: str
        """
        self.BatchTaskId = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBatchTaskInstancesResponse(AbstractModel):
    """DescribeBatchTaskInstances返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchInstances: 实例集
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchInstances: list of BatchTaskInstance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchInstances = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BatchInstances") is not None:
            self.BatchInstances = []
            for item in params.get("BatchInstances"):
                obj = BatchTaskInstance()
                obj._deserialize(item)
                self.BatchInstances.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBatchTaskRequest(AbstractModel):
    """DescribeBatchTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        """
        self.BatchTaskId = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBatchTaskResponse(AbstractModel):
    """DescribeBatchTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskDetail: 跑批任务详情
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchTaskDetail: :class:`tencentcloud.tione.v20211111.models.BatchTaskDetail`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BatchTaskDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("BatchTaskDetail") is not None:
            self.BatchTaskDetail = BatchTaskDetail()
            self.BatchTaskDetail._deserialize(params.get("BatchTaskDetail"))
        self.RequestId = params.get("RequestId")


class DescribeBatchTasksRequest(AbstractModel):
    """DescribeBatchTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤器，eg：[{ "Name": "Id", "Values": ["train-23091792777383936"] }]

取值范围：
Name（名称）：task1
Id（task ID）：train-23091792777383936
Status（状态）：STARTING / RUNNING / STOPPING / STOPPED / FAILED / SUCCEED / SUBMIT_FAILED
ChargeType（计费类型）：PREPAID（预付费）/ POSTPAID_BY_HOUR（后付费）
CHARGE_STATUS（计费状态）：NOT_BILLING（未开始计费）/ BILLING（计费中）/ ARREARS_STOP（欠费停止）
        :type Filters: list of Filter
        :param TagFilters: 标签过滤器，eg：[{ "TagKey": "TagKeyA", "TagValue": ["TagValueA"] }]
        :type TagFilters: list of TagFilter
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认为10，最大为50
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC（升序排列）/ DESC（降序排列），默认为DESC
        :type Order: str
        :param OrderField: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type OrderField: str
        """
        self.Filters = None
        self.TagFilters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBatchTasksResponse(AbstractModel):
    """DescribeBatchTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 数量
        :type TotalCount: int
        :param BatchTaskSet: 任务集
注意：此字段可能返回 null，表示取不到有效值。
        :type BatchTaskSet: list of BatchTaskSetItem
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.BatchTaskSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("BatchTaskSet") is not None:
            self.BatchTaskSet = []
            for item in params.get("BatchTaskSet"):
                obj = BatchTaskSetItem()
                obj._deserialize(item)
                self.BatchTaskSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillingResourceGroupRequest(AbstractModel):
    """DescribeBillingResourceGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id, 取值为创建资源组接口(CreateBillingResourceGroup)响应中的ResourceGroupId
        :type ResourceGroupId: str
        :param Filters: 过滤条件
注意: 
1. Filter.Name 只支持以下枚举值:
    InstanceId (资源组节点id)
    InstanceStatus (资源组节点状态)
2. Filter.Values: 长度为1且Filter.Fuzzy=true时，支持模糊查询; 不为1时，精确查询
3. 每次请求的Filters的上限为10，Filter.Values的上限为100
        :type Filters: list of Filter
        :param Offset: 分页查询起始位置，如：Limit为10，第一页Offset为0，第二页Offset为10....即每页左边为闭区间; 默认0
        :type Offset: int
        :param Limit: 分页查询每页大小，最大30; 默认20
        :type Limit: int
        :param Order: 排序方向; 枚举值: ASC | DESC；默认DESC
        :type Order: str
        :param OrderField: 排序字段; 枚举值: CreateTime (创建时间) ｜ ExpireTime (到期时间)；默认CreateTime
        :type OrderField: str
        """
        self.ResourceGroupId = None
        self.Filters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillingResourceGroupResponse(AbstractModel):
    """DescribeBillingResourceGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 资源组节点总数； 注意接口是分页拉取的，total是指资源组节点总数，不是本次返回中InstanceSet数组的大小
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param InstanceSet: 资源组节点信息
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceSet: list of Instance
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.InstanceSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = Instance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillingResourceGroupsRequest(AbstractModel):
    """DescribeBillingResourceGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param Type: 资源组类型; 枚举值 TRAIN:训练 INFERENCE:推理
        :type Type: str
        :param Filters: Filter.Name: 枚举值: ResourceGroupId (资源组id列表)
                    ResourceGroupName (资源组名称列表)
Filter.Values: 长度为1且Filter.Fuzzy=true时，支持模糊查询; 不为1时，精确查询
每次请求的Filters的上限为5，Filter.Values的上限为100
        :type Filters: list of Filter
        :param TagFilters: 标签过滤
        :type TagFilters: list of TagFilter
        :param Offset: 偏移量，默认为0；分页查询起始位置，如：Limit为100，第一页Offset为0，第二页OffSet为100....即每页左边为闭区间
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为30;
注意：小于0则默认为20；大于30则默认为30
        :type Limit: int
        :param SearchWord: 支持模糊查找资源组id和资源组名
        :type SearchWord: str
        :param DontShowInstanceSet: 是否不展示节点列表; 
true: 不展示，false 展示；
默认为false
        :type DontShowInstanceSet: bool
        """
        self.Type = None
        self.Filters = None
        self.TagFilters = None
        self.Offset = None
        self.Limit = None
        self.SearchWord = None
        self.DontShowInstanceSet = None


    def _deserialize(self, params):
        self.Type = params.get("Type")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.SearchWord = params.get("SearchWord")
        self.DontShowInstanceSet = params.get("DontShowInstanceSet")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillingResourceGroupsResponse(AbstractModel):
    """DescribeBillingResourceGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 资源组总数； 注意接口是分页拉取的，total是指资源组总数，不是本次返回中ResourceGroupSet数组的大小
        :type TotalCount: int
        :param ResourceGroupSet: 资源组详情
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupSet: list of ResourceGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ResourceGroupSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ResourceGroupSet") is not None:
            self.ResourceGroupSet = []
            for item in params.get("ResourceGroupSet"):
                obj = ResourceGroup()
                obj._deserialize(item)
                self.ResourceGroupSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillingResourceInstanceStatusStatisticRequest(AbstractModel):
    """DescribeBillingResourceInstanceStatusStatistic请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        """
        self.ResourceGroupId = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillingResourceInstanceStatusStatisticResponse(AbstractModel):
    """DescribeBillingResourceInstanceStatusStatistic返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupName: 资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param InstanceStatusSet: 资源组节点状态信息统计
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceStatusSet: list of InstanceStatusStatistic
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceGroupName = None
        self.InstanceStatusSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ResourceGroupName = params.get("ResourceGroupName")
        if params.get("InstanceStatusSet") is not None:
            self.InstanceStatusSet = []
            for item in params.get("InstanceStatusSet"):
                obj = InstanceStatusStatistic()
                obj._deserialize(item)
                self.InstanceStatusSet.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillingSpecsPriceRequest(AbstractModel):
    """DescribeBillingSpecsPrice请求参数结构体

    """

    def __init__(self):
        r"""
        :param SpecsParam: 询价参数，支持批量询价
        :type SpecsParam: list of SpecUnit
        """
        self.SpecsParam = None


    def _deserialize(self, params):
        if params.get("SpecsParam") is not None:
            self.SpecsParam = []
            for item in params.get("SpecsParam"):
                obj = SpecUnit()
                obj._deserialize(item)
                self.SpecsParam.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillingSpecsPriceResponse(AbstractModel):
    """DescribeBillingSpecsPrice返回参数结构体

    """

    def __init__(self):
        r"""
        :param SpecsPrice: 计费项价格，支持批量返回
        :type SpecsPrice: list of SpecPrice
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.SpecsPrice = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("SpecsPrice") is not None:
            self.SpecsPrice = []
            for item in params.get("SpecsPrice"):
                obj = SpecPrice()
                obj._deserialize(item)
                self.SpecsPrice.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillingSpecsRequest(AbstractModel):
    """DescribeBillingSpecs请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskType: 枚举值：TRAIN、NOTEBOOK、INFERENCE
        :type TaskType: str
        :param ChargeType: 付费模式：POSTPAID_BY_HOUR后付费、PREPAID预付费
        :type ChargeType: str
        :param ResourceType: 资源类型：CALC 计算资源、CPU CPU资源、GPU GPU资源、CBS云硬盘
        :type ResourceType: str
        """
        self.TaskType = None
        self.ChargeType = None
        self.ResourceType = None


    def _deserialize(self, params):
        self.TaskType = params.get("TaskType")
        self.ChargeType = params.get("ChargeType")
        self.ResourceType = params.get("ResourceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillingSpecsResponse(AbstractModel):
    """DescribeBillingSpecs返回参数结构体

    """

    def __init__(self):
        r"""
        :param Specs: 计费项列表
        :type Specs: list of Spec
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Specs = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Specs") is not None:
            self.Specs = []
            for item in params.get("Specs"):
                obj = Spec()
                obj._deserialize(item)
                self.Specs.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeBillingUserListRequest(AbstractModel):
    """DescribeBillingUserList请求参数结构体

    """

    def __init__(self):
        r"""
        :param UserType: 用户属性，比如WHITELIST、MIYING等。如果传空则不返回
        :type UserType: str
        """
        self.UserType = None


    def _deserialize(self, params):
        self.UserType = params.get("UserType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeBillingUserListResponse(AbstractModel):
    """DescribeBillingUserList返回参数结构体

    """

    def __init__(self):
        r"""
        :param UserType: 对应的用户属性
        :type UserType: str
        :param UserList: 用户主uin数组
        :type UserList: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.UserType = None
        self.UserList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.UserType = params.get("UserType")
        self.UserList = params.get("UserList")
        self.RequestId = params.get("RequestId")


class DescribeCodeRepoRequest(AbstractModel):
    """DescribeCodeRepo请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: id值
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCodeRepoResponse(AbstractModel):
    """DescribeCodeRepo返回参数结构体

    """

    def __init__(self):
        r"""
        :param CodeRepoDetail: 详情信息
        :type CodeRepoDetail: :class:`tencentcloud.tione.v20211111.models.CodeRepoDetail`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CodeRepoDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CodeRepoDetail") is not None:
            self.CodeRepoDetail = CodeRepoDetail()
            self.CodeRepoDetail._deserialize(params.get("CodeRepoDetail"))
        self.RequestId = params.get("RequestId")


class DescribeCodeReposRequest(AbstractModel):
    """DescribeCodeRepos请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 每页返回的实例数，默认为10
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列。默认为DESC
        :type Order: str
        :param OrderField: 根据哪个字段排序，如：CreateTime、UpdateTime，默认为UpdateTime
        :type OrderField: str
        :param Filters: 过滤器，eg：[{ "Name": "Name", "Values": ["myCodeRepoName"] }]
        :type Filters: list of Filter
        """
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Filters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeCodeReposResponse(AbstractModel):
    """DescribeCodeRepos返回参数结构体

    """

    def __init__(self):
        r"""
        :param CodeRepoSet: 详情信息
注意：此字段可能返回 null，表示取不到有效值。
        :type CodeRepoSet: list of CodeRepoDetail
        :param TotalCount: total count
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CodeRepoSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("CodeRepoSet") is not None:
            self.CodeRepoSet = []
            for item in params.get("CodeRepoSet"):
                obj = CodeRepoDetail()
                obj._deserialize(item)
                self.CodeRepoSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeContentByMD5Request(AbstractModel):
    """DescribeContentByMD5请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param MD5: 文件对象md5
        :type MD5: str
        """
        self.DatasetId = None
        self.MD5 = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.MD5 = params.get("MD5")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeContentByMD5Response(AbstractModel):
    """DescribeContentByMD5返回参数结构体

    """

    def __init__(self):
        r"""
        :param Content: 文本内容
注意：此字段可能返回 null，表示取不到有效值。
        :type Content: list of str
        :param ContentSummary: 文本内容摘要（前50个字符）
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentSummary: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Content = None
        self.ContentSummary = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Content = params.get("Content")
        self.ContentSummary = params.get("ContentSummary")
        self.RequestId = params.get("RequestId")


class DescribeDatasetDetailStructuredRequest(AbstractModel):
    """DescribeDatasetDetailStructured请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param Offset: 偏移值
        :type Offset: int
        :param Limit: 返回数据条数，默认20，目前最大支持2000条数据
        :type Limit: int
        """
        self.DatasetId = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetDetailStructuredResponse(AbstractModel):
    """DescribeDatasetDetailStructured返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 数据总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param ColumnNames: 表格头信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ColumnNames: list of str
        :param RowItems: 表格内容
注意：此字段可能返回 null，表示取不到有效值。
        :type RowItems: list of RowItem
        :param RowTexts: 文本内容
注意：此字段可能返回 null，表示取不到有效值。
        :type RowTexts: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ColumnNames = None
        self.RowItems = None
        self.RowTexts = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        self.ColumnNames = params.get("ColumnNames")
        if params.get("RowItems") is not None:
            self.RowItems = []
            for item in params.get("RowItems"):
                obj = RowItem()
                obj._deserialize(item)
                self.RowItems.append(obj)
        self.RowTexts = params.get("RowTexts")
        self.RequestId = params.get("RequestId")


class DescribeDatasetDetailTextRequest(AbstractModel):
    """DescribeDatasetDetailText请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param FileId: 文件ID
        :type FileId: str
        :param TaskId: 异步任务ID
        :type TaskId: str
        """
        self.DatasetId = None
        self.FileId = None
        self.TaskId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.FileId = params.get("FileId")
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetDetailTextResponse(AbstractModel):
    """DescribeDatasetDetailText返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskStatus: 数据透视任务状态
STATUS_PROCESSING，任务处理中
STATUS_SUCCESS, 任务成功
STATUS_FAIL，任务失败
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskStatus: str
        :param TaskProgress: 任务执行进度，取值范围[0, 100]
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskProgress: int
        :param RowSet: 文本行数据
        :type RowSet: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskStatus = None
        self.TaskProgress = None
        self.RowSet = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskStatus = params.get("TaskStatus")
        self.TaskProgress = params.get("TaskProgress")
        self.RowSet = params.get("RowSet")
        self.RequestId = params.get("RequestId")


class DescribeDatasetDetailUnstructuredRequest(AbstractModel):
    """DescribeDatasetDetailUnstructured请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回个数，默认20，目前最大支持2000条数据
        :type Limit: int
        :param LabelList: 标签过滤参数，对应标签值
        :type LabelList: list of str
        :param AnnotationStatus: 标注状态过滤参数:
STATUS_ANNOTATED，已标注
STATUS_NON_ANNOTATED，未标注
STATUS_ALL，全部
默认为STATUS_ALL
        :type AnnotationStatus: str
        :param DatasetIds: 数据集ID列表
        :type DatasetIds: list of str
        :param TextClassificationLabels: 要筛选的文本分类场景标签信息
        :type TextClassificationLabels: list of TextLabelDistributionInfo
        """
        self.DatasetId = None
        self.Offset = None
        self.Limit = None
        self.LabelList = None
        self.AnnotationStatus = None
        self.DatasetIds = None
        self.TextClassificationLabels = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.LabelList = params.get("LabelList")
        self.AnnotationStatus = params.get("AnnotationStatus")
        self.DatasetIds = params.get("DatasetIds")
        if params.get("TextClassificationLabels") is not None:
            self.TextClassificationLabels = []
            for item in params.get("TextClassificationLabels"):
                obj = TextLabelDistributionInfo()
                obj._deserialize(item)
                self.TextClassificationLabels.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetDetailUnstructuredResponse(AbstractModel):
    """DescribeDatasetDetailUnstructured返回参数结构体

    """

    def __init__(self):
        r"""
        :param AnnotatedTotalCount: 已标注数据量
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotatedTotalCount: int
        :param NonAnnotatedTotalCount: 没有标注数据量
注意：此字段可能返回 null，表示取不到有效值。
        :type NonAnnotatedTotalCount: int
        :param FilterTotalCount: 过滤数据总量
注意：此字段可能返回 null，表示取不到有效值。
        :type FilterTotalCount: int
        :param FilterLabelList: 过滤数据详情
注意：此字段可能返回 null，表示取不到有效值。
        :type FilterLabelList: list of FilterLabelInfo
        :param RowTexts: 数据文本行，默认返回前1000行
注意：此字段可能返回 null，表示取不到有效值。
        :type RowTexts: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AnnotatedTotalCount = None
        self.NonAnnotatedTotalCount = None
        self.FilterTotalCount = None
        self.FilterLabelList = None
        self.RowTexts = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AnnotatedTotalCount = params.get("AnnotatedTotalCount")
        self.NonAnnotatedTotalCount = params.get("NonAnnotatedTotalCount")
        self.FilterTotalCount = params.get("FilterTotalCount")
        if params.get("FilterLabelList") is not None:
            self.FilterLabelList = []
            for item in params.get("FilterLabelList"):
                obj = FilterLabelInfo()
                obj._deserialize(item)
                self.FilterLabelList.append(obj)
        self.RowTexts = params.get("RowTexts")
        self.RequestId = params.get("RequestId")


class DescribeDatasetDistributionStructuredRequest(AbstractModel):
    """DescribeDatasetDistributionStructured请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param FieldName: 字段名称
        :type FieldName: str
        """
        self.DatasetId = None
        self.FieldName = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.FieldName = params.get("FieldName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetDistributionStructuredResponse(AbstractModel):
    """DescribeDatasetDistributionStructured返回参数结构体

    """

    def __init__(self):
        r"""
        :param FieldName: 字段名称
注意：此字段可能返回 null，表示取不到有效值。
        :type FieldName: str
        :param FieldDistribution: 字段分布详情
注意：此字段可能返回 null，表示取不到有效值。
        :type FieldDistribution: list of FieldValueCount
        :param TotalCount: 数据总量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FieldName = None
        self.FieldDistribution = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FieldName = params.get("FieldName")
        if params.get("FieldDistribution") is not None:
            self.FieldDistribution = []
            for item in params.get("FieldDistribution"):
                obj = FieldValueCount()
                obj._deserialize(item)
                self.FieldDistribution.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeDatasetDistributionUnstructuredRequest(AbstractModel):
    """DescribeDatasetDistributionUnstructured请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param Order: Asc Desc 排序（废弃）
        :type Order: str
        :param OrderField: 排序字段（废弃）
        :type OrderField: str
        :param Offset: 偏移量（废弃）
        :type Offset: int
        :param Limit: 返回数据条数（废弃）
        :type Limit: int
        :param DatasetIds: 数据集ID列表
        :type DatasetIds: list of str
        :param Theme: 文本分类题目名称，文本分类场景不提供则返回该数据集下所有题目的标签分布信息
        :type Theme: str
        """
        self.DatasetId = None
        self.Order = None
        self.OrderField = None
        self.Offset = None
        self.Limit = None
        self.DatasetIds = None
        self.Theme = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.DatasetIds = params.get("DatasetIds")
        self.Theme = params.get("Theme")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetDistributionUnstructuredResponse(AbstractModel):
    """DescribeDatasetDistributionUnstructured返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 数据总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param LabelDistributionList: 标签分布
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelDistributionList: list of LabelDistributionInfo
        :param LabelTemplateType: 标签类型 分类、检测、分割
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelTemplateType: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.LabelDistributionList = None
        self.LabelTemplateType = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("LabelDistributionList") is not None:
            self.LabelDistributionList = []
            for item in params.get("LabelDistributionList"):
                obj = LabelDistributionInfo()
                obj._deserialize(item)
                self.LabelDistributionList.append(obj)
        self.LabelTemplateType = params.get("LabelTemplateType")
        self.RequestId = params.get("RequestId")


class DescribeDatasetFileListRequest(AbstractModel):
    """DescribeDatasetFileList请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetIds: 数据集id列表
        :type DatasetIds: list of str
        """
        self.DatasetIds = None


    def _deserialize(self, params):
        self.DatasetIds = params.get("DatasetIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetFileListResponse(AbstractModel):
    """DescribeDatasetFileList返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetFileInfos: 数据集文件列表详情
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetFileInfos: list of DatasetFileInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasetFileInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("DatasetFileInfos") is not None:
            self.DatasetFileInfos = []
            for item in params.get("DatasetFileInfos"):
                obj = DatasetFileInfo()
                obj._deserialize(item)
                self.DatasetFileInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatasetImageUrlsRequest(AbstractModel):
    """DescribeDatasetImageUrls请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param ImageIds: 图片id列表
        :type ImageIds: list of ImageId
        :param WithThumbnail: 是否返回缩略图
        :type WithThumbnail: bool
        """
        self.DatasetId = None
        self.ImageIds = None
        self.WithThumbnail = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        if params.get("ImageIds") is not None:
            self.ImageIds = []
            for item in params.get("ImageIds"):
                obj = ImageId()
                obj._deserialize(item)
                self.ImageIds.append(obj)
        self.WithThumbnail = params.get("WithThumbnail")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetImageUrlsResponse(AbstractModel):
    """DescribeDatasetImageUrls返回参数结构体

    """

    def __init__(self):
        r"""
        :param ImageUrlInfos: 图片URL连接
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageUrlInfos: list of ImageUrlInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ImageUrlInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ImageUrlInfos") is not None:
            self.ImageUrlInfos = []
            for item in params.get("ImageUrlInfos"):
                obj = ImageUrlInfo()
                obj._deserialize(item)
                self.ImageUrlInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatasetOcrSceneRequest(AbstractModel):
    """DescribeDatasetOcrScene请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetIds: 无
        :type DatasetIds: list of str
        """
        self.DatasetIds = None


    def _deserialize(self, params):
        self.DatasetIds = params.get("DatasetIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetOcrSceneResponse(AbstractModel):
    """DescribeDatasetOcrScene返回参数结构体

    """

    def __init__(self):
        r"""
        :param OcrSceneList: OCR场景信息
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrSceneList: list of OcrInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OcrSceneList = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("OcrSceneList") is not None:
            self.OcrSceneList = []
            for item in params.get("OcrSceneList"):
                obj = OcrInfo()
                obj._deserialize(item)
                self.OcrSceneList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatasetPerspectiveStatusRequest(AbstractModel):
    """DescribeDatasetPerspectiveStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetIds: 数据集Id
        :type DatasetIds: list of str
        """
        self.DatasetIds = None


    def _deserialize(self, params):
        self.DatasetIds = params.get("DatasetIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetPerspectiveStatusResponse(AbstractModel):
    """DescribeDatasetPerspectiveStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param PerspectiveStatus: true：开启，false：关闭
注意：此字段可能返回 null，表示取不到有效值。
        :type PerspectiveStatus: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PerspectiveStatus = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PerspectiveStatus = params.get("PerspectiveStatus")
        self.RequestId = params.get("RequestId")


class DescribeDatasetPreviewStatusRequest(AbstractModel):
    """DescribeDatasetPreviewStatus请求参数结构体

    """


class DescribeDatasetPreviewStatusResponse(AbstractModel):
    """DescribeDatasetPreviewStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param PreviewStatus: 数据集预览状态，true为开启，false为关闭
        :type PreviewStatus: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PreviewStatus = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PreviewStatus = params.get("PreviewStatus")
        self.RequestId = params.get("RequestId")


class DescribeDatasetSchemaRequest(AbstractModel):
    """DescribeDatasetSchema请求参数结构体

    """

    def __init__(self):
        r"""
        :param StorageDataPath: 表格文件cos存储路径
        :type StorageDataPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        """
        self.StorageDataPath = None


    def _deserialize(self, params):
        if params.get("StorageDataPath") is not None:
            self.StorageDataPath = CosPathInfo()
            self.StorageDataPath._deserialize(params.get("StorageDataPath"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetSchemaResponse(AbstractModel):
    """DescribeDatasetSchema返回参数结构体

    """

    def __init__(self):
        r"""
        :param Schema: 表格头信息列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Schema: list of SchemaInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Schema = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Schema") is not None:
            self.Schema = []
            for item in params.get("Schema"):
                obj = SchemaInfo()
                obj._deserialize(item)
                self.Schema.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeDatasetTextAnalyzeRequest(AbstractModel):
    """DescribeDatasetTextAnalyze请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetIds: 数据集ID列表
        :type DatasetIds: list of str
        :param TextLanguage: 样本语言:
TEXT_LANGUAGE_ENGLISH 英文
TEXT_LANGUAGE_CHINESE 中文
        :type TextLanguage: str
        :param TaskId: 异步任务ID
        :type TaskId: str
        """
        self.DatasetIds = None
        self.TextLanguage = None
        self.TaskId = None


    def _deserialize(self, params):
        self.DatasetIds = params.get("DatasetIds")
        self.TextLanguage = params.get("TextLanguage")
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetTextAnalyzeResponse(AbstractModel):
    """DescribeDatasetTextAnalyze返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskStatus: 数据透视任务状态
STATUS_PROCESSING，任务处理中
STATUS_SUCCESS, 任务成功
STATUS_FAIL，任务失败
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskStatus: str
        :param TaskProgress: 任务执行进度，取值范围[0, 100]
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskProgress: int
        :param TextAnalyzeResult: 数据透视结果
注意：此字段可能返回 null，表示取不到有效值。
        :type TextAnalyzeResult: :class:`tencentcloud.tione.v20211111.models.TextAnalyzeResult`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskStatus = None
        self.TaskProgress = None
        self.TextAnalyzeResult = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskStatus = params.get("TaskStatus")
        self.TaskProgress = params.get("TaskProgress")
        if params.get("TextAnalyzeResult") is not None:
            self.TextAnalyzeResult = TextAnalyzeResult()
            self.TextAnalyzeResult._deserialize(params.get("TextAnalyzeResult"))
        self.RequestId = params.get("RequestId")


class DescribeDatasetsRequest(AbstractModel):
    """DescribeDatasets请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetIds: 数据集id列表
        :type DatasetIds: list of str
        :param Filters: 数据集查询过滤条件，多个Filter之间的关系为逻辑与（AND）关系，过滤字段Filter.Name，类型为String
DatasetName，数据集名称
DatasetScope，数据集范围，SCOPE_DATASET_PRIVATE或SCOPE_DATASET_PUBLIC
        :type Filters: list of Filter
        :param TagFilters: 标签过滤条件
        :type TagFilters: list of TagFilter
        :param Order: 排序值，支持Asc或Desc，默认Desc
        :type Order: str
        :param OrderField: 排序字段，支持CreateTime或UpdateTime，默认CreateTime
        :type OrderField: str
        :param Offset: 偏移值
        :type Offset: int
        :param Limit: 返回数据个数，默认20，最大支持200
        :type Limit: int
        """
        self.DatasetIds = None
        self.Filters = None
        self.TagFilters = None
        self.Order = None
        self.OrderField = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.DatasetIds = params.get("DatasetIds")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeDatasetsResponse(AbstractModel):
    """DescribeDatasets返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 数据集总量（名称维度）
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param DatasetGroups: 数据集按照数据集名称聚合的分组
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetGroups: list of DatasetGroup
        :param DatasetIdNums: 数据集ID总量
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetIdNums: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.DatasetGroups = None
        self.DatasetIdNums = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("DatasetGroups") is not None:
            self.DatasetGroups = []
            for item in params.get("DatasetGroups"):
                obj = DatasetGroup()
                obj._deserialize(item)
                self.DatasetGroups.append(obj)
        self.DatasetIdNums = params.get("DatasetIdNums")
        self.RequestId = params.get("RequestId")


class DescribeEventsRequest(AbstractModel):
    """DescribeEvents请求参数结构体

    """

    def __init__(self):
        r"""
        :param Service: 查询哪个服务的事件（可选值为TRAIN, NOTEBOOK, INFER）
        :type Service: str
        :param ResourceName: 事件对应的k8s的资源的名称（支持结尾通配符*)
        :type ResourceName: str
        :param StartTime: 查询事件最早发生的时间（RFC3339格式的时间字符串），默认值为当前时间的前一天
        :type StartTime: str
        :param EndTime: 查询事件最晚发生的时间（RFC3339格式的时间字符串），默认值为当前时间
        :type EndTime: str
        :param Limit: 分页Limit，默认值为10
        :type Limit: int
        :param Offset: 分页Offset，默认值为0
        :type Offset: int
        :param Order: 排列顺序（可选值为ASC, DESC ），默认为DESC
        :type Order: str
        :param OrderField: 排序的依据字段（可选值为FirstTimestamp, LastTimestamp），默认值为LastTimestamp
        :type OrderField: str
        :param Filters: 过滤条件
注意: 
1. Filter.Name：目前支持ResourceKind（按事件关联的资源类型过滤）；Type（按事件类型过滤）
2. Filter.Values：
对于Name为ResourceKind，Values的可选取值为Deployment, Replicaset, Pod等K8S资源类型；
对于Name为Type，Values的可选取值仅为Normal或者Warning；
Values为多个的时候表示同时满足
3. Filter. Negative和Filter. Fuzzy没有使用
        :type Filters: list of Filter
        """
        self.Service = None
        self.ResourceName = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Offset = None
        self.Order = None
        self.OrderField = None
        self.Filters = None


    def _deserialize(self, params):
        self.Service = params.get("Service")
        self.ResourceName = params.get("ResourceName")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Offset = params.get("Offset")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEventsResponse(AbstractModel):
    """DescribeEvents返回参数结构体

    """

    def __init__(self):
        r"""
        :param Events: 事件的列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Events: list of Event
        :param TotalCount: 此次查询的事件的个数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Events = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Events") is not None:
            self.Events = []
            for item in params.get("Events"):
                obj = Event()
                obj._deserialize(item)
                self.Events.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeFixedPointRequest(AbstractModel):
    """DescribeFixedPoint请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeFixedPointResponse(AbstractModel):
    """DescribeFixedPoint返回参数结构体

    """

    def __init__(self):
        r"""
        :param FixedPoint: 固定点数
        :type FixedPoint: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FixedPoint = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FixedPoint = params.get("FixedPoint")
        self.RequestId = params.get("RequestId")


class DescribeImagesInfoRequest(AbstractModel):
    """DescribeImagesInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 请求的任务
        :type TaskId: str
        :param Offset: 查询的页数
        :type Offset: int
        :param Limit: 查询的大小
        :type Limit: int
        :param Filters: 过滤条件
        :type Filters: list of Filter
        :param OnlyResult: 是否只获取标注结果
        :type OnlyResult: bool
        :param BitShift: 指定位移量，与fileid使用
        :type BitShift: int
        """
        self.TaskId = None
        self.Offset = None
        self.Limit = None
        self.Filters = None
        self.OnlyResult = None
        self.BitShift = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.OnlyResult = params.get("OnlyResult")
        self.BitShift = params.get("BitShift")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeImagesInfoResponse(AbstractModel):
    """DescribeImagesInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 总数
        :type Total: int
        :param ImageList: 图片相关信息
        :type ImageList: list of Image
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.ImageList = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("ImageList") is not None:
            self.ImageList = []
            for item in params.get("ImageList"):
                obj = Image()
                obj._deserialize(item)
                self.ImageList.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInferGatewayStatusRequest(AbstractModel):
    """DescribeInferGatewayStatus请求参数结构体

    """


class DescribeInferGatewayStatusResponse(AbstractModel):
    """DescribeInferGatewayStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param GatewayStatus: 网关的状态
        :type GatewayStatus: str
        :param Description: 网关状态的详细描述
        :type Description: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.GatewayStatus = None
        self.Description = None
        self.RequestId = None


    def _deserialize(self, params):
        self.GatewayStatus = params.get("GatewayStatus")
        self.Description = params.get("Description")
        self.RequestId = params.get("RequestId")


class DescribeInferTemplatesRequest(AbstractModel):
    """DescribeInferTemplates请求参数结构体

    """


class DescribeInferTemplatesResponse(AbstractModel):
    """DescribeInferTemplates返回参数结构体

    """

    def __init__(self):
        r"""
        :param FrameworkTemplates: 模板列表
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkTemplates: list of InferTemplateGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FrameworkTemplates = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FrameworkTemplates") is not None:
            self.FrameworkTemplates = []
            for item in params.get("FrameworkTemplates"):
                obj = InferTemplateGroup()
                obj._deserialize(item)
                self.FrameworkTemplates.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeInsideActionRequest(AbstractModel):
    """DescribeInsideAction请求参数结构体

    """

    def __init__(self):
        r"""
        :param ActionParam: 内网接口名
        :type ActionParam: str
        :param HeadersParam: 请求头
        :type HeadersParam: str
        :param PayloadParam: 请求体
        :type PayloadParam: str
        """
        self.ActionParam = None
        self.HeadersParam = None
        self.PayloadParam = None


    def _deserialize(self, params):
        self.ActionParam = params.get("ActionParam")
        self.HeadersParam = params.get("HeadersParam")
        self.PayloadParam = params.get("PayloadParam")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInsideActionResponse(AbstractModel):
    """DescribeInsideAction返回参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 请求结果
注意：此字段可能返回 null，表示取不到有效值。
        :type Data: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.RequestId = params.get("RequestId")


class DescribeInstanceCredentialRequest(AbstractModel):
    """DescribeInstanceCredential请求参数结构体

    """

    def __init__(self):
        r"""
        :param AuthToken: 认证Token
        :type AuthToken: str
        :param Caller: 调用方地址
        :type Caller: str
        """
        self.AuthToken = None
        self.Caller = None


    def _deserialize(self, params):
        self.AuthToken = params.get("AuthToken")
        self.Caller = params.get("Caller")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeInstanceCredentialResponse(AbstractModel):
    """DescribeInstanceCredential返回参数结构体

    """

    def __init__(self):
        r"""
        :param TmpSecretId: 密钥ID
        :type TmpSecretId: str
        :param TmpSecretKey: 密钥Key
        :type TmpSecretKey: str
        :param Token: 密钥Token
        :type Token: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TmpSecretId = None
        self.TmpSecretKey = None
        self.Token = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TmpSecretId = params.get("TmpSecretId")
        self.TmpSecretKey = params.get("TmpSecretKey")
        self.Token = params.get("Token")
        self.RequestId = params.get("RequestId")


class DescribeIsTaskNameExistRequest(AbstractModel):
    """DescribeIsTaskNameExist请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskName: 新建标注任务的名称
        :type TaskName: str
        """
        self.TaskName = None


    def _deserialize(self, params):
        self.TaskName = params.get("TaskName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeIsTaskNameExistResponse(AbstractModel):
    """DescribeIsTaskNameExist返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsExist: true：重复；false：不重复
        :type IsExist: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsExist = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsExist = params.get("IsExist")
        self.RequestId = params.get("RequestId")


class DescribeLabelColorRequest(AbstractModel):
    """DescribeLabelColor请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 限制数
        :type Limit: int
        """
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLabelColorResponse(AbstractModel):
    """DescribeLabelColor返回参数结构体

    """

    def __init__(self):
        r"""
        :param Total: 总数
        :type Total: int
        :param Colors: 标签颜色
        :type Colors: list of LabelColor
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Total = None
        self.Colors = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Total = params.get("Total")
        if params.get("Colors") is not None:
            self.Colors = []
            for item in params.get("Colors"):
                obj = LabelColor()
                obj._deserialize(item)
                self.Colors.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLatestTrainingMetricsRequest(AbstractModel):
    """DescribeLatestTrainingMetrics请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLatestTrainingMetricsResponse(AbstractModel):
    """DescribeLatestTrainingMetrics返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param Metrics: 最近一次上报的训练指标.每个Metric中只有一个点的数据, 即len(Values) = len(Timestamps) = 1
注意：此字段可能返回 null，表示取不到有效值。
        :type Metrics: list of TrainingMetric
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.Metrics = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("Metrics") is not None:
            self.Metrics = []
            for item in params.get("Metrics"):
                obj = TrainingMetric()
                obj._deserialize(item)
                self.Metrics.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeLifecycleScriptRequest(AbstractModel):
    """DescribeLifecycleScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 生命周期脚本id
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLifecycleScriptResponse(AbstractModel):
    """DescribeLifecycleScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param LifecycleScript: 详情信息
        :type LifecycleScript: :class:`tencentcloud.tione.v20211111.models.LifecycleScript`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LifecycleScript = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LifecycleScript") is not None:
            self.LifecycleScript = LifecycleScript()
            self.LifecycleScript._deserialize(params.get("LifecycleScript"))
        self.RequestId = params.get("RequestId")


class DescribeLifecycleScriptsRequest(AbstractModel):
    """DescribeLifecycleScripts请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 每页返回的实例数，默认为10
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列。默认为DESC
        :type Order: str
        :param OrderField: 根据哪个字段排序，如：CreateTime、UpdateTime，默认为UpdateTime
        :type OrderField: str
        :param Filters: 过滤器，eg：[{ "Name": "Name", "Values": ["myLifecycleScriptName"] }]
        :type Filters: list of Filter
        """
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Filters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLifecycleScriptsResponse(AbstractModel):
    """DescribeLifecycleScripts返回参数结构体

    """

    def __init__(self):
        r"""
        :param LifecycleScriptSet: 详情信息
注意：此字段可能返回 null，表示取不到有效值。
        :type LifecycleScriptSet: list of LifecycleScriptItem
        :param TotalCount: total count
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LifecycleScriptSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("LifecycleScriptSet") is not None:
            self.LifecycleScriptSet = []
            for item in params.get("LifecycleScriptSet"):
                obj = LifecycleScriptItem()
                obj._deserialize(item)
                self.LifecycleScriptSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeLogsRequest(AbstractModel):
    """DescribeLogs请求参数结构体

    """

    def __init__(self):
        r"""
        :param Service: 查询哪个服务的事件（可选值为TRAIN, NOTEBOOK, INFER）
        :type Service: str
        :param PodName: 查询哪个Pod的日志（支持结尾通配符*)
        :type PodName: str
        :param StartTime: 日志查询开始时间（RFC3339格式的时间字符串），默认值为当前时间的前一个小时
        :type StartTime: str
        :param EndTime: 日志查询结束时间（RFC3339格式的时间字符串），默认值为当前时间
        :type EndTime: str
        :param Limit: 日志查询条数，默认值100，最大值100
        :type Limit: int
        :param Order: 排序方向（可选值为ASC, DESC ），默认为DESC
        :type Order: str
        :param OrderField: 按哪个字段排序（可选值为Timestamp），默认值为Timestamp
        :type OrderField: str
        :param Context: 日志查询上下文，查询下一页的时候需要回传这个字段，该字段来自本接口的返回
        :type Context: str
        :param Filters: 过滤条件
注意: 
1. Filter.Name：目前只支持Key（也就是按关键字过滤日志）
2. Filter.Values：表示过滤日志的关键字；Values为多个的时候表示同时满足
3. Filter. Negative和Filter. Fuzzy没有使用
        :type Filters: list of Filter
        """
        self.Service = None
        self.PodName = None
        self.StartTime = None
        self.EndTime = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Context = None
        self.Filters = None


    def _deserialize(self, params):
        self.Service = params.get("Service")
        self.PodName = params.get("PodName")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        self.Context = params.get("Context")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeLogsResponse(AbstractModel):
    """DescribeLogs返回参数结构体

    """

    def __init__(self):
        r"""
        :param Context: 分页的游标
注意：此字段可能返回 null，表示取不到有效值。
        :type Context: str
        :param Content: 日志数组
注意：此字段可能返回 null，表示取不到有效值。
        :type Content: list of LogIdentity
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Context = None
        self.Content = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Context = params.get("Context")
        if params.get("Content") is not None:
            self.Content = []
            for item in params.get("Content"):
                obj = LogIdentity()
                obj._deserialize(item)
                self.Content.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeModelAccEngineVersionsRequest(AbstractModel):
    """DescribeModelAccEngineVersions请求参数结构体

    """


class DescribeModelAccEngineVersionsResponse(AbstractModel):
    """DescribeModelAccEngineVersions返回参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccEngineVersions: 模型加速版本列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccEngineVersions: list of ModelAccEngineVersion
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ModelAccEngineVersions = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ModelAccEngineVersions") is not None:
            self.ModelAccEngineVersions = []
            for item in params.get("ModelAccEngineVersions"):
                obj = ModelAccEngineVersion()
                obj._deserialize(item)
                self.ModelAccEngineVersions.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeModelAccOptimizedReportRequest(AbstractModel):
    """DescribeModelAccOptimizedReport请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        """
        self.ModelAccTaskId = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelAccOptimizedReportResponse(AbstractModel):
    """DescribeModelAccOptimizedReport返回参数结构体

    """

    def __init__(self):
        r"""
        :param OptimizedReport: 模型加速优化报告
注意：此字段可能返回 null，表示取不到有效值。
        :type OptimizedReport: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.OptimizedReport = None
        self.RequestId = None


    def _deserialize(self, params):
        self.OptimizedReport = params.get("OptimizedReport")
        self.RequestId = params.get("RequestId")


class DescribeModelAccelerateTaskRequest(AbstractModel):
    """DescribeModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        """
        self.ModelAccTaskId = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelAccelerateTaskResponse(AbstractModel):
    """DescribeModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccelerateTask: 模型加速任务详情
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccelerateTask: :class:`tencentcloud.tione.v20211111.models.ModelAccelerateTask`
        :param ModelAccRuntimeInSecond: 模型加速时长，单位s
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccRuntimeInSecond: int
        :param ModelAccStartTime: 模型加速任务开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccStartTime: str
        :param ModelAccEndTime: 模型加速任务结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccEndTime: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ModelAccelerateTask = None
        self.ModelAccRuntimeInSecond = None
        self.ModelAccStartTime = None
        self.ModelAccEndTime = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ModelAccelerateTask") is not None:
            self.ModelAccelerateTask = ModelAccelerateTask()
            self.ModelAccelerateTask._deserialize(params.get("ModelAccelerateTask"))
        self.ModelAccRuntimeInSecond = params.get("ModelAccRuntimeInSecond")
        self.ModelAccStartTime = params.get("ModelAccStartTime")
        self.ModelAccEndTime = params.get("ModelAccEndTime")
        self.RequestId = params.get("RequestId")


class DescribeModelAccelerateTasksRequest(AbstractModel):
    """DescribeModelAccelerateTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤器
ModelAccTaskName 任务名称
        :type Filters: list of Filter
        :param OrderField: 排序字段，默认CreateTime
        :type OrderField: str
        :param Order: 排序方式：ASC/DESC，默认DESC
        :type Order: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回记录条数，默认20
        :type Limit: int
        :param TagFilters: 标签过滤
        :type TagFilters: list of TagFilter
        """
        self.Filters = None
        self.OrderField = None
        self.Order = None
        self.Offset = None
        self.Limit = None
        self.TagFilters = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelAccelerateTasksResponse(AbstractModel):
    """DescribeModelAccelerateTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccelerateTasks: 模型加速任务列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccelerateTasks: list of ModelAccelerateTask
        :param TotalCount: 任务总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ModelAccelerateTasks = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ModelAccelerateTasks") is not None:
            self.ModelAccelerateTasks = []
            for item in params.get("ModelAccelerateTasks"):
                obj = ModelAccelerateTask()
                obj._deserialize(item)
                self.ModelAccelerateTasks.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeModelAccelerateVersionsRequest(AbstractModel):
    """DescribeModelAccelerateVersions请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤条件
    Filter.Name: 枚举值: ModelJobName (任务名称)|TrainingModelVersionId (模型版本id)
    Filter.Values: 当长度为1时，支持模糊查询; 不为1时，精确查询
每次请求的Filters的上限为10，Filter.Values的上限为100
        :type Filters: list of Filter
        :param OrderField: 排序字段; 枚举值: CreateTime (创建时间) ；默认CreateTime
        :type OrderField: str
        :param Order: 排序方向; 枚举值: ASC | DESC；默认DESC
        :type Order: str
        :param Offset: 分页查询起始位置，如：Limit为100，第一页Offset为0，第二页Offset为100....即每页左边为闭区间; 默认0
        :type Offset: int
        :param Limit: 分页查询每页大小，最大20000; 默认20
        :type Limit: int
        :param TrainingModelId: 模型ID
        :type TrainingModelId: str
        """
        self.Filters = None
        self.OrderField = None
        self.Order = None
        self.Offset = None
        self.Limit = None
        self.TrainingModelId = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.TrainingModelId = params.get("TrainingModelId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelAccelerateVersionsResponse(AbstractModel):
    """DescribeModelAccelerateVersions返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 优化模型总数； 注意接口是分页拉取的，total是指优化模型节点总数，不是本次返回中ModelAccelerateVersions数组的大小
注意：此字段可能返回 null，表示取不到有效值。
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param ModelAccelerateVersions: 优化模型列表
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccelerateVersions: list of ModelAccelerateVersion
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ModelAccelerateVersions = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ModelAccelerateVersions") is not None:
            self.ModelAccelerateVersions = []
            for item in params.get("ModelAccelerateVersions"):
                obj = ModelAccelerateVersion()
                obj._deserialize(item)
                self.ModelAccelerateVersions.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeModelServiceCallInfoRequest(AbstractModel):
    """DescribeModelServiceCallInfo请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 服务组id
        :type ServiceGroupId: str
        """
        self.ServiceGroupId = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServiceCallInfoResponse(AbstractModel):
    """DescribeModelServiceCallInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceCallInfo: 服务调用信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceCallInfo: :class:`tencentcloud.tione.v20211111.models.ServiceCallInfo`
        :param InferGatewayCallInfo: 升级网关调用信息
注意：此字段可能返回 null，表示取不到有效值。
        :type InferGatewayCallInfo: :class:`tencentcloud.tione.v20211111.models.InferGatewayCallInfo`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceCallInfo = None
        self.InferGatewayCallInfo = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ServiceCallInfo") is not None:
            self.ServiceCallInfo = ServiceCallInfo()
            self.ServiceCallInfo._deserialize(params.get("ServiceCallInfo"))
        if params.get("InferGatewayCallInfo") is not None:
            self.InferGatewayCallInfo = InferGatewayCallInfo()
            self.InferGatewayCallInfo._deserialize(params.get("InferGatewayCallInfo"))
        self.RequestId = params.get("RequestId")


class DescribeModelServiceGroupRequest(AbstractModel):
    """DescribeModelServiceGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 无
        :type ServiceGroupId: str
        """
        self.ServiceGroupId = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServiceGroupResponse(AbstractModel):
    """DescribeModelServiceGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroup: 服务组信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceGroup: :class:`tencentcloud.tione.v20211111.models.ServiceGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceGroup = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ServiceGroup") is not None:
            self.ServiceGroup = ServiceGroup()
            self.ServiceGroup._deserialize(params.get("ServiceGroup"))
        self.RequestId = params.get("RequestId")


class DescribeModelServiceGroupsRequest(AbstractModel):
    """DescribeModelServiceGroups请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为100
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列
        :type Order: str
        :param OrderField: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type OrderField: str
        :param Filters: 分页参数，支持的分页过滤Name包括：
["ClusterId", "ServiceId", "ServiceGroupName", "ServiceGroupId","Status","CreatedBy","ModelVersionId"]
        :type Filters: list of Filter
        :param TagFilters: 标签过滤参数
        :type TagFilters: list of TagFilter
        """
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Filters = None
        self.TagFilters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServiceGroupsResponse(AbstractModel):
    """DescribeModelServiceGroups返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 推理服务组数量。
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param ServiceGroups: 服务组信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceGroups: list of ServiceGroup
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ServiceGroups = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ServiceGroups") is not None:
            self.ServiceGroups = []
            for item in params.get("ServiceGroups"):
                obj = ServiceGroup()
                obj._deserialize(item)
                self.ServiceGroups.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeModelServiceHistoryRequest(AbstractModel):
    """DescribeModelServiceHistory请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceId: 服务Id
        :type ServiceId: str
        """
        self.ServiceId = None


    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServiceHistoryResponse(AbstractModel):
    """DescribeModelServiceHistory返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 历史版本总数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param ServiceHistory: 服务版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceHistory: list of ServiceHistory
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.ServiceHistory = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("ServiceHistory") is not None:
            self.ServiceHistory = []
            for item in params.get("ServiceHistory"):
                obj = ServiceHistory()
                obj._deserialize(item)
                self.ServiceHistory.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeModelServiceHotUpdatedRequest(AbstractModel):
    """DescribeModelServiceHotUpdated请求参数结构体

    """

    def __init__(self):
        r"""
        :param ImageInfo: 镜像信息，配置服务运行所需的镜像地址等信息
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param ModelInfo: 模型信息，需要挂载模型时填写
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param VolumeMount: 挂载信息
        :type VolumeMount: :class:`tencentcloud.tione.v20211111.models.VolumeMount`
        """
        self.ImageInfo = None
        self.ModelInfo = None
        self.VolumeMount = None


    def _deserialize(self, params):
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        if params.get("VolumeMount") is not None:
            self.VolumeMount = VolumeMount()
            self.VolumeMount._deserialize(params.get("VolumeMount"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServiceHotUpdatedResponse(AbstractModel):
    """DescribeModelServiceHotUpdated返回参数结构体

    """

    def __init__(self):
        r"""
        :param HotUpdatedFlag: 热更新标志位. 
Allowed 允许开启热更新.
ForbiddenForEmptyModel 未选择模型，禁止开启热更新.
ForbiddenForIllegalModelType 模型来源非法（仅支持来自模型仓库的模型），禁止开启热更新.
ForbiddenForIllegalImage 镜像来源非法（仅支持tfserving镜像），禁止开启热更新.
ForbiddenForUnAutoCleanModel 模型未配置自动清理，禁止开启热更新.
        :type HotUpdatedFlag: str
        :param Reason: 热更新状态位的原因.
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.HotUpdatedFlag = None
        self.Reason = None
        self.RequestId = None


    def _deserialize(self, params):
        self.HotUpdatedFlag = params.get("HotUpdatedFlag")
        self.Reason = params.get("Reason")
        self.RequestId = params.get("RequestId")


class DescribeModelServiceRequest(AbstractModel):
    """DescribeModelService请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceId: 服务id
        :type ServiceId: str
        """
        self.ServiceId = None


    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServiceResponse(AbstractModel):
    """DescribeModelService返回参数结构体

    """

    def __init__(self):
        r"""
        :param Service: 服务信息
        :type Service: :class:`tencentcloud.tione.v20211111.models.Service`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Service = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Service") is not None:
            self.Service = Service()
            self.Service._deserialize(params.get("Service"))
        self.RequestId = params.get("RequestId")


class DescribeModelServiceUserInfoRequest(AbstractModel):
    """DescribeModelServiceUserInfo请求参数结构体

    """


class DescribeModelServiceUserInfoResponse(AbstractModel):
    """DescribeModelServiceUserInfo返回参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroupQuota: 服务组的数量配额, 默认为25，且 >=25
        :type ServiceGroupQuota: int
        :param ServiceGroupNumber: 服务组的当前数量
        :type ServiceGroupNumber: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceGroupQuota = None
        self.ServiceGroupNumber = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ServiceGroupQuota = params.get("ServiceGroupQuota")
        self.ServiceGroupNumber = params.get("ServiceGroupNumber")
        self.RequestId = params.get("RequestId")


class DescribeModelServicesRequest(AbstractModel):
    """DescribeModelServices请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认为20，最大值为20
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列
        :type Order: str
        :param OrderField: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type OrderField: str
        :param Filters: 分页参数，支持的分页过滤Name包括：
["ClusterId", "ServiceId", "ServiceGroupName", "ServiceGroupId","Status","CreatedBy","ModelId"]
        :type Filters: list of Filter
        :param TagFilters: 标签过滤参数
        :type TagFilters: list of TagFilter
        """
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Filters = None
        self.TagFilters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeModelServicesResponse(AbstractModel):
    """DescribeModelServices返回参数结构体

    """

    def __init__(self):
        r"""
        :param TotalCount: 服务数量
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param Services: 无
注意：此字段可能返回 null，表示取不到有效值。
        :type Services: list of Service
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TotalCount = None
        self.Services = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TotalCount = params.get("TotalCount")
        if params.get("Services") is not None:
            self.Services = []
            for item in params.get("Services"):
                obj = Service()
                obj._deserialize(item)
                self.Services.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeMonitorDataRequest(AbstractModel):
    """DescribeMonitorData请求参数结构体

    """

    def __init__(self):
        r"""
        :param Namespace: 空间
        :type Namespace: str
        :param MetricName: 指标名
        :type MetricName: str
        :param Instances: 实例
        :type Instances: list of FakeInstance
        :param Period: 周期
        :type Period: int
        :param StartTime: 开始时间
        :type StartTime: str
        :param EndTime: 结束时间
        :type EndTime: str
        """
        self.Namespace = None
        self.MetricName = None
        self.Instances = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None


    def _deserialize(self, params):
        self.Namespace = params.get("Namespace")
        self.MetricName = params.get("MetricName")
        if params.get("Instances") is not None:
            self.Instances = []
            for item in params.get("Instances"):
                obj = FakeInstance()
                obj._deserialize(item)
                self.Instances.append(obj)
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeMonitorDataResponse(AbstractModel):
    """DescribeMonitorData返回参数结构体

    """

    def __init__(self):
        r"""
        :param MetricName: 指标名
注意：此字段可能返回 null，表示取不到有效值。
        :type MetricName: str
        :param Period: 周期
注意：此字段可能返回 null，表示取不到有效值。
        :type Period: int
        :param StartTime: 开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param EndTime: 结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param DataPoints: 点
注意：此字段可能返回 null，表示取不到有效值。
        :type DataPoints: list of FakePoint
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.MetricName = None
        self.Period = None
        self.StartTime = None
        self.EndTime = None
        self.DataPoints = None
        self.RequestId = None


    def _deserialize(self, params):
        self.MetricName = params.get("MetricName")
        self.Period = params.get("Period")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("DataPoints") is not None:
            self.DataPoints = []
            for item in params.get("DataPoints"):
                obj = FakePoint()
                obj._deserialize(item)
                self.DataPoints.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeNLPDatasetContentRequest(AbstractModel):
    """DescribeNLPDatasetContent请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        :param DatasetId: 数据集id
        :type DatasetId: str
        :param SampleId: 文本md5
        :type SampleId: str
        :param EvaluationTaskId: 评测任务id
        :type EvaluationTaskId: str
        """
        self.AutoMLTaskId = None
        self.DatasetId = None
        self.SampleId = None
        self.EvaluationTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.DatasetId = params.get("DatasetId")
        self.SampleId = params.get("SampleId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNLPDatasetContentResponse(AbstractModel):
    """DescribeNLPDatasetContent返回参数结构体

    """

    def __init__(self):
        r"""
        :param Content: 文本内容
        :type Content: list of str
        :param ContentSummary: 文本摘要
        :type ContentSummary: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Content = None
        self.ContentSummary = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Content = params.get("Content")
        self.ContentSummary = params.get("ContentSummary")
        self.RequestId = params.get("RequestId")


class DescribeNotebookRequest(AbstractModel):
    """DescribeNotebook请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook id
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebookResponse(AbstractModel):
    """DescribeNotebook返回参数结构体

    """

    def __init__(self):
        r"""
        :param NotebookDetail: 详情
        :type NotebookDetail: :class:`tencentcloud.tione.v20211111.models.NotebookDetail`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NotebookDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NotebookDetail") is not None:
            self.NotebookDetail = NotebookDetail()
            self.NotebookDetail._deserialize(params.get("NotebookDetail"))
        self.RequestId = params.get("RequestId")


class DescribeNotebookStorageQuotaRequest(AbstractModel):
    """DescribeNotebookStorageQuota请求参数结构体

    """


class DescribeNotebookStorageQuotaResponse(AbstractModel):
    """DescribeNotebookStorageQuota返回参数结构体

    """

    def __init__(self):
        r"""
        :param IsWhitelist: 是否为配额白名单
        :type IsWhitelist: bool
        :param FreeCbs: 免费硬盘大小
        :type FreeCbs: int
        :param MaxCbs: 最大可购买硬盘大小
        :type MaxCbs: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.IsWhitelist = None
        self.FreeCbs = None
        self.MaxCbs = None
        self.RequestId = None


    def _deserialize(self, params):
        self.IsWhitelist = params.get("IsWhitelist")
        self.FreeCbs = params.get("FreeCbs")
        self.MaxCbs = params.get("MaxCbs")
        self.RequestId = params.get("RequestId")


class DescribeNotebooksRequest(AbstractModel):
    """DescribeNotebooks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 每页返回的实例数，默认为10
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC：升序排列 DESC：降序排列。默认为DESC
        :type Order: str
        :param OrderField: 根据哪个字段排序，如：CreateTime、UpdateTime，默认为UpdateTime
        :type OrderField: str
        :param Filters: 过滤器，eg：[{ "Name": "Id", "Values": ["nb-123456789"] }]

取值范围
Name（名称）：notebook1
Id（notebook ID）：nb-123456789
Status（状态）：Starting / Running / Stopped / Stopping / Failed / SubmitFailed
ChargeType（计费类型）：PREPAID（预付费）/ POSTPAID_BY_HOUR（后付费）
ChargeStatus（计费状态）：NOT_BILLING（未开始计费）/ BILLING（计费中）/ BILLING_STORAGE（存储计费中）/ARREARS_STOP（欠费停止）
DefaultCodeRepoId（默认代码仓库ID）：cr-123456789
AdditionalCodeRepoId（关联代码仓库ID）：cr-123456789
LifecycleScriptId（生命周期ID）：ls-12312312311312
        :type Filters: list of Filter
        :param TagFilters: 标签过滤器，eg：[{ "TagKey": "TagKeyA", "TagValue": ["TagValueA"] }]
        :type TagFilters: list of TagFilter
        """
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None
        self.Filters = None
        self.TagFilters = None


    def _deserialize(self, params):
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeNotebooksResponse(AbstractModel):
    """DescribeNotebooks返回参数结构体

    """

    def __init__(self):
        r"""
        :param NotebookSet: 详情
注意：此字段可能返回 null，表示取不到有效值。
        :type NotebookSet: list of NotebookSetItem
        :param TotalCount: 总条数
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.NotebookSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("NotebookSet") is not None:
            self.NotebookSet = []
            for item in params.get("NotebookSet"):
                obj = NotebookSetItem()
                obj._deserialize(item)
                self.NotebookSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeSceneListRequest(AbstractModel):
    """DescribeSceneList请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤项
        :type Filters: list of Filter
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 限制量
        :type Limit: int
        """
        self.Filters = None
        self.Offset = None
        self.Limit = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeSceneListResponse(AbstractModel):
    """DescribeSceneList返回参数结构体

    """

    def __init__(self):
        r"""
        :param Scenes: 场景列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Scenes: list of Scene
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Scenes = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Scenes") is not None:
            self.Scenes = []
            for item in params.get("Scenes"):
                obj = Scene()
                obj._deserialize(item)
                self.Scenes.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTaskDisplayConfigRequest(AbstractModel):
    """DescribeTaskDisplayConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTaskDisplayConfigResponse(AbstractModel):
    """DescribeTaskDisplayConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param BgColor: 背景颜色
        :type BgColor: str
        :param FontFamily: 字体系列
        :type FontFamily: str
        :param FontSize: 字体大小
        :type FontSize: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BgColor = None
        self.FontFamily = None
        self.FontSize = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BgColor = params.get("BgColor")
        self.FontFamily = params.get("FontFamily")
        self.FontSize = params.get("FontSize")
        self.RequestId = params.get("RequestId")


class DescribeTaskProcessRequest(AbstractModel):
    """DescribeTaskProcess请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTaskProcessResponse(AbstractModel):
    """DescribeTaskProcess返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param Total: 数量总计
        :type Total: int
        :param Finished: 已完成数量
        :type Finished: int
        :param Stage: 阶段
注意：此字段可能返回 null，表示取不到有效值。
        :type Stage: str
        :param CurrentTime: 上报时间（单位为）
注意：此字段可能返回 null，表示取不到有效值。
        :type CurrentTime: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.Total = None
        self.Finished = None
        self.Stage = None
        self.CurrentTime = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Total = params.get("Total")
        self.Finished = params.get("Finished")
        self.Stage = params.get("Stage")
        self.CurrentTime = params.get("CurrentTime")
        self.RequestId = params.get("RequestId")


class DescribeTensorBoardTaskRequest(AbstractModel):
    """DescribeTensorBoardTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTensorBoardTaskResponse(AbstractModel):
    """DescribeTensorBoardTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param Id: TensorBoard ID
        :type Id: str
        :param Status: TensorBoard状态
        :type Status: str
        :param Url: TensorBoard Url
注意：此字段可能返回 null，表示取不到有效值。
        :type Url: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Id = None
        self.Status = None
        self.Url = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Status = params.get("Status")
        self.Url = params.get("Url")
        self.RequestId = params.get("RequestId")


class DescribeTrainingFrameworksRequest(AbstractModel):
    """DescribeTrainingFrameworks请求参数结构体

    """


class DescribeTrainingFrameworksResponse(AbstractModel):
    """DescribeTrainingFrameworks返回参数结构体

    """

    def __init__(self):
        r"""
        :param FrameworkInfos: 框架信息列表
        :type FrameworkInfos: list of FrameworkInfo
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FrameworkInfos = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FrameworkInfos") is not None:
            self.FrameworkInfos = []
            for item in params.get("FrameworkInfos"):
                obj = FrameworkInfo()
                obj._deserialize(item)
                self.FrameworkInfos.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTrainingMetricsRequest(AbstractModel):
    """DescribeTrainingMetrics请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingMetricsResponse(AbstractModel):
    """DescribeTrainingMetrics返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param Data: 训练指标数据
注意：此字段可能返回 null，表示取不到有效值。
        :type Data: list of CustomTrainingData
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.Data = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = CustomTrainingData()
                obj._deserialize(item)
                self.Data.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTrainingModelVersionRequest(AbstractModel):
    """DescribeTrainingModelVersion请求参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelVersionId: 模型版本ID
        :type TrainingModelVersionId: str
        """
        self.TrainingModelVersionId = None


    def _deserialize(self, params):
        self.TrainingModelVersionId = params.get("TrainingModelVersionId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingModelVersionResponse(AbstractModel):
    """DescribeTrainingModelVersion返回参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelVersion: 模型版本
        :type TrainingModelVersion: :class:`tencentcloud.tione.v20211111.models.TrainingModelVersionDTO`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrainingModelVersion = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TrainingModelVersion") is not None:
            self.TrainingModelVersion = TrainingModelVersionDTO()
            self.TrainingModelVersion._deserialize(params.get("TrainingModelVersion"))
        self.RequestId = params.get("RequestId")


class DescribeTrainingModelVersionsRequest(AbstractModel):
    """DescribeTrainingModelVersions请求参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelId: 模型ID
        :type TrainingModelId: str
        :param Filters: 过滤条件
Filter.Name: 枚举值:
    TrainingModelVersionId (模型版本ID)
    ModelVersionType (模型版本类型) 其值支持: NORMAL(通用) ACCELERATE (加速)
    ModelFormat（模型格式）其值Filter.Values支持：
TORCH_SCRIPT/PYTORCH/DETECTRON2/SAVED_MODEL/FROZEN_GRAPH/PMML
    AlgorithmFramework (算法框架) 其值Filter.Values支持：TENSORFLOW/PYTORCH/DETECTRON2
Filter.Values: 当长度为1时，支持模糊查询; 不为1时，精确查询
每次请求的Filters的上限为10，Filter.Values的上限为100
        :type Filters: list of Filter
        """
        self.TrainingModelId = None
        self.Filters = None


    def _deserialize(self, params):
        self.TrainingModelId = params.get("TrainingModelId")
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingModelVersionsResponse(AbstractModel):
    """DescribeTrainingModelVersions返回参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelVersions: 模型版本列表
        :type TrainingModelVersions: list of TrainingModelVersionDTO
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrainingModelVersions = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TrainingModelVersions") is not None:
            self.TrainingModelVersions = []
            for item in params.get("TrainingModelVersions"):
                obj = TrainingModelVersionDTO()
                obj._deserialize(item)
                self.TrainingModelVersions.append(obj)
        self.RequestId = params.get("RequestId")


class DescribeTrainingModelsRequest(AbstractModel):
    """DescribeTrainingModels请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤器
Filter.Name: 枚举值:
    keyword (模型名称)
    TrainingModelId (模型ID)
    ModelVersionType (模型版本类型) 其值Filter.Values支持: NORMAL(通用) ACCELERATE (加速)
    TrainingModelSource (模型来源)  其值Filter.Values支持： JOB/COS
    AlgorithmFramework (算法框架) 其值Filter.Values支持：TENSORFLOW/PYTORCH/DETECTRON2
    ModelFormat（模型格式）其值Filter.Values支持：
TORCH_SCRIPT/PYTORCH/DETECTRON2/SAVED_MODEL/FROZEN_GRAPH/PMML
Filter.Values: 当长度为1时，支持模糊查询; 不为1时，精确查询
每次请求的Filters的上限为10，Filter.Values的上限为100
Filter.Fuzzy取值：true/false，是否支持模糊匹配
        :type Filters: list of Filter
        :param OrderField: 排序字段，默认CreateTime
        :type OrderField: str
        :param Order: 排序方式，ASC/DESC，默认DESC
        :type Order: str
        :param Offset: 偏移量
        :type Offset: int
        :param Limit: 返回结果数量
        :type Limit: int
        :param TagFilters: 标签过滤
        :type TagFilters: list of TagFilter
        """
        self.Filters = None
        self.OrderField = None
        self.Order = None
        self.Offset = None
        self.Limit = None
        self.TagFilters = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        self.OrderField = params.get("OrderField")
        self.Order = params.get("Order")
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingModelsResponse(AbstractModel):
    """DescribeTrainingModels返回参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModels: 模型列表
        :type TrainingModels: list of TrainingModelDTO
        :param TotalCount: 模型总数
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrainingModels = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TrainingModels") is not None:
            self.TrainingModels = []
            for item in params.get("TrainingModels"):
                obj = TrainingModelDTO()
                obj._deserialize(item)
                self.TrainingModels.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeTrainingTaskPodsRequest(AbstractModel):
    """DescribeTrainingTaskPods请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingTaskPodsResponse(AbstractModel):
    """DescribeTrainingTaskPods返回参数结构体

    """

    def __init__(self):
        r"""
        :param PodNames: pod名称列表
        :type PodNames: list of str
        :param TotalCount: 数量
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.PodNames = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        self.PodNames = params.get("PodNames")
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DescribeTrainingTaskRequest(AbstractModel):
    """DescribeTrainingTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingTaskResponse(AbstractModel):
    """DescribeTrainingTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingTaskDetail: 训练任务详情
        :type TrainingTaskDetail: :class:`tencentcloud.tione.v20211111.models.TrainingTaskDetail`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrainingTaskDetail = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TrainingTaskDetail") is not None:
            self.TrainingTaskDetail = TrainingTaskDetail()
            self.TrainingTaskDetail._deserialize(params.get("TrainingTaskDetail"))
        self.RequestId = params.get("RequestId")


class DescribeTrainingTasksRequest(AbstractModel):
    """DescribeTrainingTasks请求参数结构体

    """

    def __init__(self):
        r"""
        :param Filters: 过滤器，eg：[{ "Name": "Id", "Values": ["train-23091792777383936"] }]

取值范围：
Name（名称）：task1
Id（task ID）：train-23091792777383936
Status（状态）：STARTING / RUNNING / STOPPING / STOPPED / FAILED / SUCCEED / SUBMIT_FAILED
ChargeType（计费类型）：PREPAID（预付费）/ POSTPAID_BY_HOUR（后付费）
CHARGE_STATUS（计费状态）：NOT_BILLING（未开始计费）/ BILLING（计费中）/ ARREARS_STOP（欠费停止）
        :type Filters: list of Filter
        :param TagFilters: 标签过滤器，eg：[{ "TagKey": "TagKeyA", "TagValue": ["TagValueA"] }]
        :type TagFilters: list of TagFilter
        :param Offset: 偏移量，默认为0
        :type Offset: int
        :param Limit: 返回数量，默认为10，最大为50
        :type Limit: int
        :param Order: 输出列表的排列顺序。取值范围：ASC（升序排列）/ DESC（降序排列），默认为DESC
        :type Order: str
        :param OrderField: 排序的依据字段， 取值范围 "CreateTime" "UpdateTime"
        :type OrderField: str
        """
        self.Filters = None
        self.TagFilters = None
        self.Offset = None
        self.Limit = None
        self.Order = None
        self.OrderField = None


    def _deserialize(self, params):
        if params.get("Filters") is not None:
            self.Filters = []
            for item in params.get("Filters"):
                obj = Filter()
                obj._deserialize(item)
                self.Filters.append(obj)
        if params.get("TagFilters") is not None:
            self.TagFilters = []
            for item in params.get("TagFilters"):
                obj = TagFilter()
                obj._deserialize(item)
                self.TagFilters.append(obj)
        self.Offset = params.get("Offset")
        self.Limit = params.get("Limit")
        self.Order = params.get("Order")
        self.OrderField = params.get("OrderField")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeTrainingTasksResponse(AbstractModel):
    """DescribeTrainingTasks返回参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingTaskSet: 训练任务集
        :type TrainingTaskSet: list of TrainingTaskSetItem
        :param TotalCount: 数量
        :type TotalCount: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TrainingTaskSet = None
        self.TotalCount = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("TrainingTaskSet") is not None:
            self.TrainingTaskSet = []
            for item in params.get("TrainingTaskSet"):
                obj = TrainingTaskSetItem()
                obj._deserialize(item)
                self.TrainingTaskSet.append(obj)
        self.TotalCount = params.get("TotalCount")
        self.RequestId = params.get("RequestId")


class DestroyBillingResourceRequest(AbstractModel):
    """DestroyBillingResource请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceIds: 资源组节点id列表
注意: 单次最多100个
        :type ResourceIds: list of str
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        """
        self.ResourceIds = None
        self.ResourceGroupId = None


    def _deserialize(self, params):
        self.ResourceIds = params.get("ResourceIds")
        self.ResourceGroupId = params.get("ResourceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DestroyBillingResourceResponse(AbstractModel):
    """DestroyBillingResource返回参数结构体

    """

    def __init__(self):
        r"""
        :param FailResources: 节点失败详情
注意：此字段可能返回 null，表示取不到有效值。
        :type FailResources: list of FailResource
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FailResources = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FailResources") is not None:
            self.FailResources = []
            for item in params.get("FailResources"):
                obj = FailResource()
                obj._deserialize(item)
                self.FailResources.append(obj)
        self.RequestId = params.get("RequestId")


class DetectionLabelInfo(AbstractModel):
    """图像检测参数信息

    """

    def __init__(self):
        r"""
        :param Points: 点坐标列表
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of PointInfo
        :param Labels: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Labels: list of str
        :param FrameType: 类别
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameType: str
        """
        self.Points = None
        self.Labels = None
        self.FrameType = None


    def _deserialize(self, params):
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = PointInfo()
                obj._deserialize(item)
                self.Points.append(obj)
        self.Labels = params.get("Labels")
        self.FrameType = params.get("FrameType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Dimension(AbstractModel):
    """监控数据查询维度

    """

    def __init__(self):
        r"""
        :param Name: 名字
        :type Name: str
        :param Value: 值
        :type Value: str
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DownloadTrainingMetricsRequest(AbstractModel):
    """DownloadTrainingMetrics请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DownloadTrainingMetricsResponse(AbstractModel):
    """DownloadTrainingMetrics返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param URL: 任务指标数据文件资源定位符
注意：此字段可能返回 null，表示取不到有效值。
        :type URL: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.URL = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.URL = params.get("URL")
        self.RequestId = params.get("RequestId")


class EMSTask(AbstractModel):
    """模型服务任务详情

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoMLTaskId: str
        :param EMSTaskId: 模型服务任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskId: str
        :param TaskVersion: 自动学习任务版本
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskVersion: str
        :param Tags: 自动学习任务关联标签信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param TaskDescription: 自动学习任务描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskDescription: str
        :param SceneName: 自动学习任务场景名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneName: str
        :param Creator: 自动学习任务创建者信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Creator: str
        :param Updator: 自动学习任务更新者信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Updator: str
        :param EMSTaskStatus: 自动学习发布模型服务实例状态
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskStatus: str
        :param EMSTaskBusinessStatus: 自动学习发布模型服务business状态
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskBusinessStatus: str
        :param EMSTaskStartTime: 自动学习发布模型服务任务创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskStartTime: str
        :param ErrorMsg: 自动学习发布模型服务任务错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param ChargeType: 自动学习发布模型服务任务付费模式
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param ChargeStatus: 自动学习发布模型服务计费状态
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeStatus: str
        :param PublishResourceInfo: 自动学习发布模型服务资源配置情况
注意：此字段可能返回 null，表示取不到有效值。
        :type PublishResourceInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        :param MaxServiceHours: 自动学习发布模型服务运行最大小时， 0表示不限制时间
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxServiceHours: int
        :param ResourceGroupId: 预付费资源组id
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param SceneId: 场景ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneId: str
        :param SceneDomain: 场景领域
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneDomain: str
        :param BillingInfo: 自动学习发布模型服务计费情况
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfo: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.TaskVersion = None
        self.Tags = None
        self.TaskDescription = None
        self.SceneName = None
        self.Creator = None
        self.Updator = None
        self.EMSTaskStatus = None
        self.EMSTaskBusinessStatus = None
        self.EMSTaskStartTime = None
        self.ErrorMsg = None
        self.ChargeType = None
        self.ChargeStatus = None
        self.PublishResourceInfo = None
        self.MaxServiceHours = None
        self.ResourceGroupId = None
        self.SceneId = None
        self.SceneDomain = None
        self.BillingInfo = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.TaskVersion = params.get("TaskVersion")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.TaskDescription = params.get("TaskDescription")
        self.SceneName = params.get("SceneName")
        self.Creator = params.get("Creator")
        self.Updator = params.get("Updator")
        self.EMSTaskStatus = params.get("EMSTaskStatus")
        self.EMSTaskBusinessStatus = params.get("EMSTaskBusinessStatus")
        self.EMSTaskStartTime = params.get("EMSTaskStartTime")
        self.ErrorMsg = params.get("ErrorMsg")
        self.ChargeType = params.get("ChargeType")
        self.ChargeStatus = params.get("ChargeStatus")
        if params.get("PublishResourceInfo") is not None:
            self.PublishResourceInfo = ResourceConfigInfo()
            self.PublishResourceInfo._deserialize(params.get("PublishResourceInfo"))
        self.MaxServiceHours = params.get("MaxServiceHours")
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.SceneId = params.get("SceneId")
        self.SceneDomain = params.get("SceneDomain")
        self.BillingInfo = params.get("BillingInfo")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EMSTaskGroup(AbstractModel):
    """自动学习模型服务发布任务组信息

    """

    def __init__(self):
        r"""
        :param TaskGroupId: 自动学习任务组id
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskGroupId: str
        :param TaskName: 自动学习任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskName: str
        :param EMSTasks: 自动学习模型发布任务详情
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTasks: list of EMSTask
        """
        self.TaskGroupId = None
        self.TaskName = None
        self.EMSTasks = None


    def _deserialize(self, params):
        self.TaskGroupId = params.get("TaskGroupId")
        self.TaskName = params.get("TaskName")
        if params.get("EMSTasks") is not None:
            self.EMSTasks = []
            for item in params.get("EMSTasks"):
                obj = EMSTask()
                obj._deserialize(item)
                self.EMSTasks.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableBatchTaskClsConfigRequest(AbstractModel):
    """EnableBatchTaskClsConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        :param LogEnable: 是否开启CLS日志投递
        :type LogEnable: bool
        :param LogConfig: EnableCls为true时，填写日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        """
        self.BatchTaskId = None
        self.LogEnable = None
        self.LogConfig = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableBatchTaskClsConfigResponse(AbstractModel):
    """EnableBatchTaskClsConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EnableNotebookClsConfigRequest(AbstractModel):
    """EnableNotebookClsConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook ID
        :type Id: str
        :param LogEnable: 是否开启CLS日志投递
        :type LogEnable: bool
        :param LogConfig: EnableCls为true时，填写日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        """
        self.Id = None
        self.LogEnable = None
        self.LogConfig = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableNotebookClsConfigResponse(AbstractModel):
    """EnableNotebookClsConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EnableTrainingTaskClsConfigRequest(AbstractModel):
    """EnableTrainingTaskClsConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 训练任务ID
        :type TaskId: str
        :param LogEnable: 是否开启CLS日志投递
        :type LogEnable: bool
        :param LogConfig: 日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        """
        self.TaskId = None
        self.LogEnable = None
        self.LogConfig = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnableTrainingTaskClsConfigResponse(AbstractModel):
    """EnableTrainingTaskClsConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class EngineVersion(AbstractModel):
    """引擎版本

    """

    def __init__(self):
        r"""
        :param Version: 引擎版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param Image: 运行镜像
注意：此字段可能返回 null，表示取不到有效值。
        :type Image: str
        """
        self.Version = None
        self.Image = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.Image = params.get("Image")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EnvVar(AbstractModel):
    """环境变量

    """

    def __init__(self):
        r"""
        :param Name: 环境变量key
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Value: 环境变量value
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: str
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EvaluationTask(AbstractModel):
    """自动学习评测任务

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 自动学习评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param TaskVersion: 自动学习任务版本
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskVersion: str
        :param Tags: 关联标签信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param TaskDescription: 自动学习任务描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskDescription: str
        :param SceneName: 自动学习任务场景
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneName: str
        :param Creator: 自动学习任务创建者信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Creator: str
        :param Updator: 自动学习任务更新者信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Updator: str
        :param EvaluationTaskStatus: 自动学习评测任务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskStatus: str
        :param EvaluationTaskProgress: 自动学习评测任务进度百分比, 范围为[0, 100]
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskProgress: int
        :param EvaluationTaskStartTime: 自动学习评测任务创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskStartTime: str
        :param EvaluationTaskEndTime: 自动学习评测任务截止时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskEndTime: str
        :param ErrorMsg: 自动学习评测任务错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param ChargeType: 自动学习评测任务付费模式，当前为限时免费
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param ChargeStatus: 自动学习评测任务收费状态
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeStatus: str
        :param WaitNumber: 自动学习评测任务当前排队信息
注意：此字段可能返回 null，表示取不到有效值。
        :type WaitNumber: int
        :param SceneId: 场景ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneId: str
        :param SceneDomain: 场景领域
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneDomain: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.TaskVersion = None
        self.Tags = None
        self.TaskDescription = None
        self.SceneName = None
        self.Creator = None
        self.Updator = None
        self.EvaluationTaskStatus = None
        self.EvaluationTaskProgress = None
        self.EvaluationTaskStartTime = None
        self.EvaluationTaskEndTime = None
        self.ErrorMsg = None
        self.ChargeType = None
        self.ChargeStatus = None
        self.WaitNumber = None
        self.SceneId = None
        self.SceneDomain = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.TaskVersion = params.get("TaskVersion")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.TaskDescription = params.get("TaskDescription")
        self.SceneName = params.get("SceneName")
        self.Creator = params.get("Creator")
        self.Updator = params.get("Updator")
        self.EvaluationTaskStatus = params.get("EvaluationTaskStatus")
        self.EvaluationTaskProgress = params.get("EvaluationTaskProgress")
        self.EvaluationTaskStartTime = params.get("EvaluationTaskStartTime")
        self.EvaluationTaskEndTime = params.get("EvaluationTaskEndTime")
        self.ErrorMsg = params.get("ErrorMsg")
        self.ChargeType = params.get("ChargeType")
        self.ChargeStatus = params.get("ChargeStatus")
        self.WaitNumber = params.get("WaitNumber")
        self.SceneId = params.get("SceneId")
        self.SceneDomain = params.get("SceneDomain")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class EvaluationTaskGroup(AbstractModel):
    """自动学习评测任务组信息

    """

    def __init__(self):
        r"""
        :param TaskGroupId: 自动学习任务组id
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskGroupId: str
        :param TaskName: 自动学习任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskName: str
        :param EvaluationTasks: 评测任务详情
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTasks: list of EvaluationTask
        """
        self.TaskGroupId = None
        self.TaskName = None
        self.EvaluationTasks = None


    def _deserialize(self, params):
        self.TaskGroupId = params.get("TaskGroupId")
        self.TaskName = params.get("TaskName")
        if params.get("EvaluationTasks") is not None:
            self.EvaluationTasks = []
            for item in params.get("EvaluationTasks"):
                obj = EvaluationTask()
                obj._deserialize(item)
                self.EvaluationTasks.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Event(AbstractModel):
    """K8s的Event

    """

    def __init__(self):
        r"""
        :param Id: 事件的id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: str
        :param Message: 事件的具体信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param FirstTimestamp: 事件第一次发生的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type FirstTimestamp: str
        :param LastTimestamp: 事件最后一次发生的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastTimestamp: str
        :param Count: 事件发生的次数
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        :param Type: 事件的类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param ResourceKind: 事件关联的资源的类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceKind: str
        :param ResourceName: 事件关联的资源的名字
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceName: str
        """
        self.Id = None
        self.Message = None
        self.FirstTimestamp = None
        self.LastTimestamp = None
        self.Count = None
        self.Type = None
        self.ResourceKind = None
        self.ResourceName = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Message = params.get("Message")
        self.FirstTimestamp = params.get("FirstTimestamp")
        self.LastTimestamp = params.get("LastTimestamp")
        self.Count = params.get("Count")
        self.Type = params.get("Type")
        self.ResourceKind = params.get("ResourceKind")
        self.ResourceName = params.get("ResourceName")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FailResource(AbstractModel):
    """错误资源信息

    """

    def __init__(self):
        r"""
        :param ResourceId: 资源组节点id
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceId: str
        :param FailMsg: 失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailMsg: str
        """
        self.ResourceId = None
        self.FailMsg = None


    def _deserialize(self, params):
        self.ResourceId = params.get("ResourceId")
        self.FailMsg = params.get("FailMsg")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FakeInstance(AbstractModel):
    """监控数据查询实例

    """

    def __init__(self):
        r"""
        :param Dimensions: 无
注意：此字段可能返回 null，表示取不到有效值。
        :type Dimensions: list of Dimension
        """
        self.Dimensions = None


    def _deserialize(self, params):
        if params.get("Dimensions") is not None:
            self.Dimensions = []
            for item in params.get("Dimensions"):
                obj = Dimension()
                obj._deserialize(item)
                self.Dimensions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FakePoint(AbstractModel):
    """数据点

    """

    def __init__(self):
        r"""
        :param Dimensions: 维度
注意：此字段可能返回 null，表示取不到有效值。
        :type Dimensions: list of Dimension
        :param Timestamps: 时间戳
注意：此字段可能返回 null，表示取不到有效值。
        :type Timestamps: list of float
        :param Values: 值
注意：此字段可能返回 null，表示取不到有效值。
        :type Values: list of float
        """
        self.Dimensions = None
        self.Timestamps = None
        self.Values = None


    def _deserialize(self, params):
        if params.get("Dimensions") is not None:
            self.Dimensions = []
            for item in params.get("Dimensions"):
                obj = Dimension()
                obj._deserialize(item)
                self.Dimensions.append(obj)
        self.Timestamps = params.get("Timestamps")
        self.Values = params.get("Values")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FieldValueCount(AbstractModel):
    """统计信息详情

    """

    def __init__(self):
        r"""
        :param FieldValue: 字段名
        :type FieldValue: str
        :param FieldCount: 值个数
        :type FieldCount: int
        :param FieldPercentage: 值百分比
        :type FieldPercentage: float
        """
        self.FieldValue = None
        self.FieldCount = None
        self.FieldPercentage = None


    def _deserialize(self, params):
        self.FieldValue = params.get("FieldValue")
        self.FieldCount = params.get("FieldCount")
        self.FieldPercentage = params.get("FieldPercentage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Filter(AbstractModel):
    """过滤器

    """

    def __init__(self):
        r"""
        :param Name: 过滤字段名称
        :type Name: str
        :param Values: 过滤字段取值
        :type Values: list of str
        :param Negative: 是否开启反向查询
        :type Negative: bool
        :param Fuzzy: 是否开启模糊匹配
        :type Fuzzy: bool
        """
        self.Name = None
        self.Values = None
        self.Negative = None
        self.Fuzzy = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Values = params.get("Values")
        self.Negative = params.get("Negative")
        self.Fuzzy = params.get("Fuzzy")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FilterLabelInfo(AbstractModel):
    """图片列表查询结果详情

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集id
        :type DatasetId: str
        :param FileId: 文件ID
        :type FileId: str
        :param FileName: 文件路径
        :type FileName: str
        :param ClassificationLabels: 分类标签结果
注意：此字段可能返回 null，表示取不到有效值。
        :type ClassificationLabels: list of str
        :param DetectionLabels: 检测标签结果
注意：此字段可能返回 null，表示取不到有效值。
        :type DetectionLabels: list of DetectionLabelInfo
        :param SegmentationLabels: 分割标签结果
注意：此字段可能返回 null，表示取不到有效值。
        :type SegmentationLabels: list of SegmentationInfo
        :param RGBPath: RGB 图片路径
注意：此字段可能返回 null，表示取不到有效值。
        :type RGBPath: str
        :param LabelTemplateType: 标签模板类型
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelTemplateType: str
        :param DownloadUrl: 下载url链接
注意：此字段可能返回 null，表示取不到有效值。
        :type DownloadUrl: str
        :param DownloadThumbnailUrl: 缩略图下载链接
注意：此字段可能返回 null，表示取不到有效值。
        :type DownloadThumbnailUrl: str
        :param DownloadRGBUrl: 分割结果图片下载链接
注意：此字段可能返回 null，表示取不到有效值。
        :type DownloadRGBUrl: str
        :param OcrScene: OCR场景
IDENTITY：识别
STRUCTURE：智能结构化
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrScene: str
        :param OcrLabels: OCR场景标签列表
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrLabels: list of OcrLabelInfo
        :param OcrLabelInfo: OCR场景标签信息
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrLabelInfo: str
        :param TextClassificationLabelList: 文本分类场景标签结果，内容是json结构
注意：此字段可能返回 null，表示取不到有效值。
        :type TextClassificationLabelList: str
        :param RowText: 文本内容，返回50字符
注意：此字段可能返回 null，表示取不到有效值。
        :type RowText: str
        :param ContentOmit: 文本内容是否完全返回
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentOmit: bool
        """
        self.DatasetId = None
        self.FileId = None
        self.FileName = None
        self.ClassificationLabels = None
        self.DetectionLabels = None
        self.SegmentationLabels = None
        self.RGBPath = None
        self.LabelTemplateType = None
        self.DownloadUrl = None
        self.DownloadThumbnailUrl = None
        self.DownloadRGBUrl = None
        self.OcrScene = None
        self.OcrLabels = None
        self.OcrLabelInfo = None
        self.TextClassificationLabelList = None
        self.RowText = None
        self.ContentOmit = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.FileId = params.get("FileId")
        self.FileName = params.get("FileName")
        self.ClassificationLabels = params.get("ClassificationLabels")
        if params.get("DetectionLabels") is not None:
            self.DetectionLabels = []
            for item in params.get("DetectionLabels"):
                obj = DetectionLabelInfo()
                obj._deserialize(item)
                self.DetectionLabels.append(obj)
        if params.get("SegmentationLabels") is not None:
            self.SegmentationLabels = []
            for item in params.get("SegmentationLabels"):
                obj = SegmentationInfo()
                obj._deserialize(item)
                self.SegmentationLabels.append(obj)
        self.RGBPath = params.get("RGBPath")
        self.LabelTemplateType = params.get("LabelTemplateType")
        self.DownloadUrl = params.get("DownloadUrl")
        self.DownloadThumbnailUrl = params.get("DownloadThumbnailUrl")
        self.DownloadRGBUrl = params.get("DownloadRGBUrl")
        self.OcrScene = params.get("OcrScene")
        if params.get("OcrLabels") is not None:
            self.OcrLabels = []
            for item in params.get("OcrLabels"):
                obj = OcrLabelInfo()
                obj._deserialize(item)
                self.OcrLabels.append(obj)
        self.OcrLabelInfo = params.get("OcrLabelInfo")
        self.TextClassificationLabelList = params.get("TextClassificationLabelList")
        self.RowText = params.get("RowText")
        self.ContentOmit = params.get("ContentOmit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FrameworkInfo(AbstractModel):
    """框架信息列表

    """

    def __init__(self):
        r"""
        :param Name: 框架名称
        :type Name: str
        :param VersionInfos: 框架版本以及对应的训练模式
        :type VersionInfos: list of FrameworkVersion
        """
        self.Name = None
        self.VersionInfos = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        if params.get("VersionInfos") is not None:
            self.VersionInfos = []
            for item in params.get("VersionInfos"):
                obj = FrameworkVersion()
                obj._deserialize(item)
                self.VersionInfos.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class FrameworkVersion(AbstractModel):
    """框架版本以及对应的训练模式

    """

    def __init__(self):
        r"""
        :param Version: 框架版本
        :type Version: str
        :param TrainingModes: 训练模式
        :type TrainingModes: list of str
        :param Environment: 框架运行环境
        :type Environment: str
        """
        self.Version = None
        self.TrainingModes = None
        self.Environment = None


    def _deserialize(self, params):
        self.Version = params.get("Version")
        self.TrainingModes = params.get("TrainingModes")
        self.Environment = params.get("Environment")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GitConfig(AbstractModel):
    """存储库Git相关配置

    """

    def __init__(self):
        r"""
        :param RepositoryUrl: git地址
        :type RepositoryUrl: str
        :param Branch: 代码分支
注意：此字段可能返回 null，表示取不到有效值。
        :type Branch: str
        """
        self.RepositoryUrl = None
        self.Branch = None


    def _deserialize(self, params):
        self.RepositoryUrl = params.get("RepositoryUrl")
        self.Branch = params.get("Branch")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GitSecret(AbstractModel):
    """Git凭证

    """

    def __init__(self):
        r"""
        :param NoSecret: 无秘钥，默认选项
        :type NoSecret: bool
        :param Secret: Git用户名密码base64编码后的字符串
编码前的内容应为Json字符串，如
{"UserName": "用户名", "Password":"密码"}
        :type Secret: str
        """
        self.NoSecret = None
        self.Secret = None


    def _deserialize(self, params):
        self.NoSecret = params.get("NoSecret")
        self.Secret = params.get("Secret")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GpuDetail(AbstractModel):
    """gpu 详情

    """

    def __init__(self):
        r"""
        :param Name: GPU 显卡类型；枚举值: V100 A100 T4
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Value: GPU 显卡数；单位为1/100卡，比如100代表1卡
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: int
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class GroupResource(AbstractModel):
    """资源信息

    """

    def __init__(self):
        r"""
        :param Cpu: CPU核数; 单位为1/1000核，比如100表示0.1核
        :type Cpu: int
        :param Memory: 内存；单位为MB
        :type Memory: int
        :param Gpu: 总卡数；GPUDetail 显卡数之和；单位为1/100卡，比如100代表1卡
注意：此字段可能返回 null，表示取不到有效值。
        :type Gpu: int
        :param GpuDetailSet: Gpu详情
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuDetailSet: list of GpuDetail
        """
        self.Cpu = None
        self.Memory = None
        self.Gpu = None
        self.GpuDetailSet = None


    def _deserialize(self, params):
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Gpu = params.get("Gpu")
        if params.get("GpuDetailSet") is not None:
            self.GpuDetailSet = []
            for item in params.get("GpuDetailSet"):
                obj = GpuDetail()
                obj._deserialize(item)
                self.GpuDetailSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HDFSConfig(AbstractModel):
    """HDFS的参数配置

    """

    def __init__(self):
        r"""
        :param Id: 集群实例ID,实例ID形如: emr-xxxxxxxx
        :type Id: str
        :param Path: 路径
        :type Path: str
        """
        self.Id = None
        self.Path = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HorizontalPodAutoscaler(AbstractModel):
    """hpa的描述

    """

    def __init__(self):
        r"""
        :param MinReplicas: 最小实例数
注意：此字段可能返回 null，表示取不到有效值。
        :type MinReplicas: int
        :param MaxReplicas: 最大实例数
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxReplicas: int
        :param HpaMetrics: 扩缩容指标
注意：此字段可能返回 null，表示取不到有效值。
        :type HpaMetrics: list of Option
        """
        self.MinReplicas = None
        self.MaxReplicas = None
        self.HpaMetrics = None


    def _deserialize(self, params):
        self.MinReplicas = params.get("MinReplicas")
        self.MaxReplicas = params.get("MaxReplicas")
        if params.get("HpaMetrics") is not None:
            self.HpaMetrics = []
            for item in params.get("HpaMetrics"):
                obj = Option()
                obj._deserialize(item)
                self.HpaMetrics.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class HyperParameter(AbstractModel):
    """模型专业参数

    """

    def __init__(self):
        r"""
        :param MaxNNZ: 最大nnz数
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxNNZ: str
        :param SlotNum: slot数
注意：此字段可能返回 null，表示取不到有效值。
        :type SlotNum: str
        :param CpuCachePercentage: gpu cache 使用率
注意：此字段可能返回 null，表示取不到有效值。
        :type CpuCachePercentage: str
        :param GpuCachePercentage: cpu cache 使用率
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuCachePercentage: str
        :param EnableDistributed: 是否开启分布式模式
注意：此字段可能返回 null，表示取不到有效值。
        :type EnableDistributed: str
        :param MinBlockSizePt: TORCH_SCRIPT、MMDETECTION、DETECTRON2、HUGGINGFACE格式在进行优化时切分子图的最小算子数目，一般无需进行改动，默认为3
注意：此字段可能返回 null，表示取不到有效值。
        :type MinBlockSizePt: str
        :param MinBlockSizeTf: FROZEN_GRAPH、SAVED_MODEL格式在进行优化时切分子图的最小算子数目，一般无需进行改动，默认为10
注意：此字段可能返回 null，表示取不到有效值。
        :type MinBlockSizeTf: str
        """
        self.MaxNNZ = None
        self.SlotNum = None
        self.CpuCachePercentage = None
        self.GpuCachePercentage = None
        self.EnableDistributed = None
        self.MinBlockSizePt = None
        self.MinBlockSizeTf = None


    def _deserialize(self, params):
        self.MaxNNZ = params.get("MaxNNZ")
        self.SlotNum = params.get("SlotNum")
        self.CpuCachePercentage = params.get("CpuCachePercentage")
        self.GpuCachePercentage = params.get("GpuCachePercentage")
        self.EnableDistributed = params.get("EnableDistributed")
        self.MinBlockSizePt = params.get("MinBlockSizePt")
        self.MinBlockSizeTf = params.get("MinBlockSizeTf")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Image(AbstractModel):
    """图片相关信息

    """

    def __init__(self):
        r"""
        :param FileId: 文件id
        :type FileId: str
        :param FileName: 文件名称
        :type FileName: str
        :param FileUrl: 文件下载链接
        :type FileUrl: str
        :param FileStatus: 1=已标注；2=未标注；3=预标注
        :type FileStatus: int
        :param DataThumbnailUrl: 缩略图链接
        :type DataThumbnailUrl: str
        :param AnnotationResult: 标注结果
        :type AnnotationResult: str
        """
        self.FileId = None
        self.FileName = None
        self.FileUrl = None
        self.FileStatus = None
        self.DataThumbnailUrl = None
        self.AnnotationResult = None


    def _deserialize(self, params):
        self.FileId = params.get("FileId")
        self.FileName = params.get("FileName")
        self.FileUrl = params.get("FileUrl")
        self.FileStatus = params.get("FileStatus")
        self.DataThumbnailUrl = params.get("DataThumbnailUrl")
        self.AnnotationResult = params.get("AnnotationResult")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageId(AbstractModel):
    """图片id

    """

    def __init__(self):
        r"""
        :param FileId: 文件id
        :type FileId: str
        :param Path: 文件路径
        :type Path: str
        """
        self.FileId = None
        self.Path = None


    def _deserialize(self, params):
        self.FileId = params.get("FileId")
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageInfo(AbstractModel):
    """镜像描述信息

    """

    def __init__(self):
        r"""
        :param ImageType: 镜像类型：TCR为腾讯云TCR镜像; CCR为腾讯云TCR个人版镜像，PreSet为平台预置镜像
        :type ImageType: str
        :param ImageUrl: 镜像地址
        :type ImageUrl: str
        :param RegistryRegion: TCR镜像对应的地域
注意：此字段可能返回 null，表示取不到有效值。
        :type RegistryRegion: str
        :param RegistryId: TCR镜像对应的实例id
注意：此字段可能返回 null，表示取不到有效值。
        :type RegistryId: str
        """
        self.ImageType = None
        self.ImageUrl = None
        self.RegistryRegion = None
        self.RegistryId = None


    def _deserialize(self, params):
        self.ImageType = params.get("ImageType")
        self.ImageUrl = params.get("ImageUrl")
        self.RegistryRegion = params.get("RegistryRegion")
        self.RegistryId = params.get("RegistryId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ImageUrlInfo(AbstractModel):
    """图像url 链接

    """

    def __init__(self):
        r"""
        :param FileId: 文件id
注意：此字段可能返回 null，表示取不到有效值。
        :type FileId: str
        :param ImageUrl: 图片下载URL
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageUrl: str
        :param ThumbnailUrl: 图片缩略图url
注意：此字段可能返回 null，表示取不到有效值。
        :type ThumbnailUrl: str
        """
        self.FileId = None
        self.ImageUrl = None
        self.ThumbnailUrl = None


    def _deserialize(self, params):
        self.FileId = params.get("FileId")
        self.ImageUrl = params.get("ImageUrl")
        self.ThumbnailUrl = params.get("ThumbnailUrl")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferEMSProxyRequest(AbstractModel):
    """InferEMSProxy请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param ImageCosPaths: 图片列表
        :type ImageCosPaths: list of str
        :param EMSTaskId: 在线服务ID
        :type EMSTaskId: str
        :param OcrKeys: OCR 结构化key列表
        :type OcrKeys: list of str
        :param NLPSamples: 文本分类的样本列表
        :type NLPSamples: list of NLPSample
        """
        self.AutoMLTaskId = None
        self.ImageCosPaths = None
        self.EMSTaskId = None
        self.OcrKeys = None
        self.NLPSamples = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.ImageCosPaths = params.get("ImageCosPaths")
        self.EMSTaskId = params.get("EMSTaskId")
        self.OcrKeys = params.get("OcrKeys")
        if params.get("NLPSamples") is not None:
            self.NLPSamples = []
            for item in params.get("NLPSamples"):
                obj = NLPSample()
                obj._deserialize(item)
                self.NLPSamples.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferEMSProxyResponse(AbstractModel):
    """InferEMSProxy返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param EMSTaskId: 在线学习任务ID
        :type EMSTaskId: str
        :param SceneType: 场景类型
        :type SceneType: str
        :param InferenceResults: 推理结果
注意：此字段可能返回 null，表示取不到有效值。
        :type InferenceResults: list of str
        :param InferUrl: 在线服务调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type InferUrl: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.SceneType = None
        self.InferenceResults = None
        self.InferUrl = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.SceneType = params.get("SceneType")
        self.InferenceResults = params.get("InferenceResults")
        self.InferUrl = params.get("InferUrl")
        self.RequestId = params.get("RequestId")


class InferGatewayCallInfo(AbstractModel):
    """服务的调用信息，服务组下唯一

    """

    def __init__(self):
        r"""
        :param VpcHttpAddr: 内网http调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcHttpAddr: str
        :param VpcHttpsAddr: 内网https调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcHttpsAddr: str
        :param VpcGrpcTlsAddr: 内网grpc调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcGrpcTlsAddr: str
        :param VpcId: 可访问的vpcid
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param SubnetId: 后端ip对应的子网
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: str
        """
        self.VpcHttpAddr = None
        self.VpcHttpsAddr = None
        self.VpcGrpcTlsAddr = None
        self.VpcId = None
        self.SubnetId = None


    def _deserialize(self, params):
        self.VpcHttpAddr = params.get("VpcHttpAddr")
        self.VpcHttpsAddr = params.get("VpcHttpsAddr")
        self.VpcGrpcTlsAddr = params.get("VpcGrpcTlsAddr")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferTemplate(AbstractModel):
    """推理镜像详情

    """

    def __init__(self):
        r"""
        :param InferTemplateId: 模板ID
        :type InferTemplateId: str
        :param InferTemplateImage: 模板镜像
        :type InferTemplateImage: str
        """
        self.InferTemplateId = None
        self.InferTemplateImage = None


    def _deserialize(self, params):
        self.InferTemplateId = params.get("InferTemplateId")
        self.InferTemplateImage = params.get("InferTemplateImage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InferTemplateGroup(AbstractModel):
    """推理镜像组

    """

    def __init__(self):
        r"""
        :param Framework: 算法框架
注意：此字段可能返回 null，表示取不到有效值。
        :type Framework: str
        :param FrameworkVersion: 版本号
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkVersion: str
        :param Groups: 支持的训练框架集合
注意：此字段可能返回 null，表示取不到有效值。
        :type Groups: list of str
        :param InferTemplates: 镜像模板参数列表
注意：此字段可能返回 null，表示取不到有效值。
        :type InferTemplates: list of InferTemplate
        """
        self.Framework = None
        self.FrameworkVersion = None
        self.Groups = None
        self.InferTemplates = None


    def _deserialize(self, params):
        self.Framework = params.get("Framework")
        self.FrameworkVersion = params.get("FrameworkVersion")
        self.Groups = params.get("Groups")
        if params.get("InferTemplates") is not None:
            self.InferTemplates = []
            for item in params.get("InferTemplates"):
                obj = InferTemplate()
                obj._deserialize(item)
                self.InferTemplates.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Instance(AbstractModel):
    """资源组节点信息

    """

    def __init__(self):
        r"""
        :param InstanceId: 资源组节点id
        :type InstanceId: str
        :param UsedResource: 节点已用资源
注意：此字段可能返回 null，表示取不到有效值。
        :type UsedResource: :class:`tencentcloud.tione.v20211111.models.ResourceInfo`
        :param TotalResource: 节点总资源
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalResource: :class:`tencentcloud.tione.v20211111.models.ResourceInfo`
        :param InstanceStatus: 节点状态 
注意：此字段为枚举值
说明: 
DEPLOYING: 部署中
RUNNING: 运行中 
DEPLOY_FAILED: 部署失败
 RELEASING 释放中 
RELEASED：已释放 
EXCEPTION：异常
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceStatus: str
        :param SubUin: 创建人
        :type SubUin: str
        :param CreateTime: 创建时间: 
注意：北京时间，比如: 2021-12-01 12:00:00
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param ExpireTime: 到期时间
注意：北京时间，比如：2021-12-11 12:00:00
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpireTime: str
        :param AutoRenewFlag: 自动续费标识
注意：此字段为枚举值
说明：
NOTIFY_AND_MANUAL_RENEW：手动续费(取消自动续费)且到期通知
NOTIFY_AND_AUTO_RENEW：自动续费且到期通知
DISABLE_NOTIFY_AND_MANUAL_RENEW：手动续费(取消自动续费)且到期不通知
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoRenewFlag: str
        :param SpecId: 计费项ID
        :type SpecId: str
        :param SpecAlias: 计费项别名
        :type SpecAlias: str
        """
        self.InstanceId = None
        self.UsedResource = None
        self.TotalResource = None
        self.InstanceStatus = None
        self.SubUin = None
        self.CreateTime = None
        self.ExpireTime = None
        self.AutoRenewFlag = None
        self.SpecId = None
        self.SpecAlias = None


    def _deserialize(self, params):
        self.InstanceId = params.get("InstanceId")
        if params.get("UsedResource") is not None:
            self.UsedResource = ResourceInfo()
            self.UsedResource._deserialize(params.get("UsedResource"))
        if params.get("TotalResource") is not None:
            self.TotalResource = ResourceInfo()
            self.TotalResource._deserialize(params.get("TotalResource"))
        self.InstanceStatus = params.get("InstanceStatus")
        self.SubUin = params.get("SubUin")
        self.CreateTime = params.get("CreateTime")
        self.ExpireTime = params.get("ExpireTime")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.SpecId = params.get("SpecId")
        self.SpecAlias = params.get("SpecAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InstanceStatusStatistic(AbstractModel):
    """资源组节点状态统计

    """

    def __init__(self):
        r"""
        :param InstanceStatus: 节点状态
注意：枚举值
RUNNING (运行中)
DEPLOYING （部署中）
DEPLOY_FAILED （部署失败）
RELEASED （已经释放）
EXCEPTION （异常）
RELEASING （释放中）
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceStatus: str
        :param Count: 此状态节点总数
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        """
        self.InstanceStatus = None
        self.Count = None


    def _deserialize(self, params):
        self.InstanceStatus = params.get("InstanceStatus")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InterfaceCallTestRequest(AbstractModel):
    """InterfaceCallTest请求参数结构体

    """

    def __init__(self):
        r"""
        :param ApiId: 测试时对应的api-id
        :type ApiId: str
        :param CurlData: 请求的body
        :type CurlData: str
        """
        self.ApiId = None
        self.CurlData = None


    def _deserialize(self, params):
        self.ApiId = params.get("ApiId")
        self.CurlData = params.get("CurlData")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class InterfaceCallTestResponse(AbstractModel):
    """InterfaceCallTest返回参数结构体

    """

    def __init__(self):
        r"""
        :param CurlResponseRaw: 请求序列化后的回包
注意：此字段可能返回 null，表示取不到有效值。
        :type CurlResponseRaw: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.CurlResponseRaw = None
        self.RequestId = None


    def _deserialize(self, params):
        self.CurlResponseRaw = params.get("CurlResponseRaw")
        self.RequestId = params.get("RequestId")


class KeyPair(AbstractModel):
    """KeyPair 映射后的key（附加key或者标准key）

    """

    def __init__(self):
        r"""
        :param Raw: 原始字段
        :type Raw: str
        :param Key: 映射后的key（附加key或者标准key）
        :type Key: str
        :param Idx: 索引
注意：此字段可能返回 null，表示取不到有效值。
        :type Idx: str
        """
        self.Raw = None
        self.Key = None
        self.Idx = None


    def _deserialize(self, params):
        self.Raw = params.get("Raw")
        self.Key = params.get("Key")
        self.Idx = params.get("Idx")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class KeySetType(AbstractModel):
    """keypair set

    """

    def __init__(self):
        r"""
        :param Keys: keyset
        :type Keys: list of KeyPair
        """
        self.Keys = None


    def _deserialize(self, params):
        if params.get("Keys") is not None:
            self.Keys = []
            for item in params.get("Keys"):
                obj = KeyPair()
                obj._deserialize(item)
                self.Keys.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LabelColor(AbstractModel):
    """标签颜色

    """

    def __init__(self):
        r"""
        :param Num: 顺序数
        :type Num: int
        :param Hex: hex颜色
        :type Hex: str
        """
        self.Num = None
        self.Hex = None


    def _deserialize(self, params):
        self.Num = params.get("Num")
        self.Hex = params.get("Hex")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LabelConfig(AbstractModel):
    """标签信息

    """

    def __init__(self):
        r"""
        :param LabelName: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelName: str
        :param LabelId: 标签id
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelId: int
        :param Points: 标签在图像坐标点信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of Point
        :param Blocks: OCR块结果
注意：此字段可能返回 null，表示取不到有效值。
        :type Blocks: list of OcrBlock
        """
        self.LabelName = None
        self.LabelId = None
        self.Points = None
        self.Blocks = None


    def _deserialize(self, params):
        self.LabelName = params.get("LabelName")
        self.LabelId = params.get("LabelId")
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = Point()
                obj._deserialize(item)
                self.Points.append(obj)
        if params.get("Blocks") is not None:
            self.Blocks = []
            for item in params.get("Blocks"):
                obj = OcrBlock()
                obj._deserialize(item)
                self.Blocks.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LabelDistributionInfo(AbstractModel):
    """标签分布

    """

    def __init__(self):
        r"""
        :param FirstClassLabelValue: 一级标签名
        :type FirstClassLabelValue: str
        :param FirstClassLabelCount: 标签个数
        :type FirstClassLabelCount: int
        :param FirstClassLabelPercentage: 标签百分比
        :type FirstClassLabelPercentage: float
        :param Choice: 文本分类题目属性(1.2.8新增)
SINGLE\MULTIPLE\MIX
描述题目是单选 还是多选；
注意：此字段可能返回 null，表示取不到有效值。
        :type Choice: str
        :param TextClassLabelInfo: 文本数据标签分布信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TextClassLabelInfo: :class:`tencentcloud.tione.v20211111.models.TextLabelDistributionInfo`
        """
        self.FirstClassLabelValue = None
        self.FirstClassLabelCount = None
        self.FirstClassLabelPercentage = None
        self.Choice = None
        self.TextClassLabelInfo = None


    def _deserialize(self, params):
        self.FirstClassLabelValue = params.get("FirstClassLabelValue")
        self.FirstClassLabelCount = params.get("FirstClassLabelCount")
        self.FirstClassLabelPercentage = params.get("FirstClassLabelPercentage")
        self.Choice = params.get("Choice")
        if params.get("TextClassLabelInfo") is not None:
            self.TextClassLabelInfo = TextLabelDistributionInfo()
            self.TextClassLabelInfo._deserialize(params.get("TextClassLabelInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LabelValue(AbstractModel):
    """描述label详细信息

    """

    def __init__(self):
        r"""
        :param LabelName: 标签名称
        :type LabelName: str
        :param LabelColor: 标签的颜色
        :type LabelColor: str
        """
        self.LabelName = None
        self.LabelColor = None


    def _deserialize(self, params):
        self.LabelName = params.get("LabelName")
        self.LabelColor = params.get("LabelColor")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LifecycleScript(AbstractModel):
    """生命周期脚本信息

    """

    def __init__(self):
        r"""
        :param Id: 生命周期脚本ID
        :type Id: str
        :param Name: 生命周期脚本名称
        :type Name: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param CreateScript: 创建脚本内容 (base64编码)
        :type CreateScript: str
        :param StartScript: 启动脚本内容（base64编码）
        :type StartScript: str
        """
        self.Id = None
        self.Name = None
        self.CreateTime = None
        self.UpdateTime = None
        self.CreateScript = None
        self.StartScript = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.CreateScript = params.get("CreateScript")
        self.StartScript = params.get("StartScript")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LifecycleScriptItem(AbstractModel):
    """生命周期脚本列表ITEM

    """

    def __init__(self):
        r"""
        :param Id: 生命周期脚本ID
        :type Id: str
        :param Name: 生命周期脚本名称
        :type Name: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        """
        self.Id = None
        self.Name = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LogConfig(AbstractModel):
    """日志配置

    """

    def __init__(self):
        r"""
        :param LogsetId: 日志需要投递到cls的日志集
注意：此字段可能返回 null，表示取不到有效值。
        :type LogsetId: str
        :param TopicId: 日志需要投递到cls的主题
注意：此字段可能返回 null，表示取不到有效值。
        :type TopicId: str
        """
        self.LogsetId = None
        self.TopicId = None


    def _deserialize(self, params):
        self.LogsetId = params.get("LogsetId")
        self.TopicId = params.get("TopicId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class LogIdentity(AbstractModel):
    """单条日志数据结构

    """

    def __init__(self):
        r"""
        :param Id: 单条日志的ID
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: str
        :param Message: 单条日志的内容
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param PodName: 这条日志对应的Pod名称
注意：此字段可能返回 null，表示取不到有效值。
        :type PodName: str
        :param Timestamp: 日志的时间戳（RFC3339格式的时间字符串）
注意：此字段可能返回 null，表示取不到有效值。
        :type Timestamp: str
        """
        self.Id = None
        self.Message = None
        self.PodName = None
        self.Timestamp = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Message = params.get("Message")
        self.PodName = params.get("PodName")
        self.Timestamp = params.get("Timestamp")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MLDataConfig(AbstractModel):
    """自动学习数据配置

    """

    def __init__(self):
        r"""
        :param DataSource: 数据来源
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSource: str
        :param TrainDatasetIds: 训练数据集
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainDatasetIds: list of str
        :param TrainDatasetLabels: 训练集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainDatasetLabels: list of str
        :param ValidationDatasetIds: 验证数据集
注意：此字段可能返回 null，表示取不到有效值。
        :type ValidationDatasetIds: list of str
        :param ValidationDatasetLabels: 验证集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type ValidationDatasetLabels: list of str
        :param ValidationPercent: 验证集百分比
注意：此字段可能返回 null，表示取不到有效值。
        :type ValidationPercent: int
        :param TestDatasetIds: 测试数据集
注意：此字段可能返回 null，表示取不到有效值。
        :type TestDatasetIds: list of str
        :param TestDatasetLabels: 测试数据标签
注意：此字段可能返回 null，表示取不到有效值。
        :type TestDatasetLabels: list of str
        :param LogEnable: 是否开启日志投递
注意：此字段可能返回 null，表示取不到有效值。
        :type LogEnable: bool
        :param LogConfig: 日志投递配置
注意：此字段可能返回 null，表示取不到有效值。
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param TrainDatasetLabelsMap: 训练数据集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainDatasetLabelsMap: str
        :param TestDatasetLabelsMap: 测试数据集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type TestDatasetLabelsMap: str
        :param ValidationDatasetLabelsMap: 验证数据集标签
注意：此字段可能返回 null，表示取不到有效值。
        :type ValidationDatasetLabelsMap: str
        """
        self.DataSource = None
        self.TrainDatasetIds = None
        self.TrainDatasetLabels = None
        self.ValidationDatasetIds = None
        self.ValidationDatasetLabels = None
        self.ValidationPercent = None
        self.TestDatasetIds = None
        self.TestDatasetLabels = None
        self.LogEnable = None
        self.LogConfig = None
        self.TrainDatasetLabelsMap = None
        self.TestDatasetLabelsMap = None
        self.ValidationDatasetLabelsMap = None


    def _deserialize(self, params):
        self.DataSource = params.get("DataSource")
        self.TrainDatasetIds = params.get("TrainDatasetIds")
        self.TrainDatasetLabels = params.get("TrainDatasetLabels")
        self.ValidationDatasetIds = params.get("ValidationDatasetIds")
        self.ValidationDatasetLabels = params.get("ValidationDatasetLabels")
        self.ValidationPercent = params.get("ValidationPercent")
        self.TestDatasetIds = params.get("TestDatasetIds")
        self.TestDatasetLabels = params.get("TestDatasetLabels")
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.TrainDatasetLabelsMap = params.get("TrainDatasetLabelsMap")
        self.TestDatasetLabelsMap = params.get("TestDatasetLabelsMap")
        self.ValidationDatasetLabelsMap = params.get("ValidationDatasetLabelsMap")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class MetricData(AbstractModel):
    """指标数据

    """

    def __init__(self):
        r"""
        :param TaskId: 训练任务id
        :type TaskId: str
        :param Timestamp: 时间戳.unix timestamp,单位为秒
注意：此字段可能返回 null，表示取不到有效值。
        :type Timestamp: int
        :param Uin: 用户uin
注意：此字段可能返回 null，表示取不到有效值。
        :type Uin: str
        :param Epoch: 本次上报数据所处的训练周期数。
注意：此字段可能返回 null，表示取不到有效值。
        :type Epoch: int
        :param Step: 本次上报数据所处的训练迭代次数。
注意：此字段可能返回 null，表示取不到有效值。
        :type Step: int
        :param TotalSteps: 训练停止所需的迭代总数。
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalSteps: int
        :param Points: 数据点。数组元素为不同指标的数据。数组长度不超过10。
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of DataPoint
        """
        self.TaskId = None
        self.Timestamp = None
        self.Uin = None
        self.Epoch = None
        self.Step = None
        self.TotalSteps = None
        self.Points = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Timestamp = params.get("Timestamp")
        self.Uin = params.get("Uin")
        self.Epoch = params.get("Epoch")
        self.Step = params.get("Step")
        self.TotalSteps = params.get("TotalSteps")
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = DataPoint()
                obj._deserialize(item)
                self.Points.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelAccEngineVersion(AbstractModel):
    """模型加速引擎版本

    """

    def __init__(self):
        r"""
        :param ModelFormat: 模型格式
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelFormat: str
        :param EngineVersions: 引擎版本信息
注意：此字段可能返回 null，表示取不到有效值。
        :type EngineVersions: list of EngineVersion
        """
        self.ModelFormat = None
        self.EngineVersions = None


    def _deserialize(self, params):
        self.ModelFormat = params.get("ModelFormat")
        if params.get("EngineVersions") is not None:
            self.EngineVersions = []
            for item in params.get("EngineVersions"):
                obj = EngineVersion()
                obj._deserialize(item)
                self.EngineVersions.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelAccelerateConfig(AbstractModel):
    """模型优化配置

    """

    def __init__(self):
        r"""
        :param OptimizeEnable: 是否开启优化开关
        :type OptimizeEnable: bool
        :param OptimizationLevel: 优化级别
        :type OptimizationLevel: str
        :param GpuType: gpu 卡类型
        :type GpuType: str
        """
        self.OptimizeEnable = None
        self.OptimizationLevel = None
        self.GpuType = None


    def _deserialize(self, params):
        self.OptimizeEnable = params.get("OptimizeEnable")
        self.OptimizationLevel = params.get("OptimizationLevel")
        self.GpuType = params.get("GpuType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelAccelerateTask(AbstractModel):
    """模型加速任务

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskId: str
        :param ModelAccTaskName: 模型加速任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskName: str
        :param ModelId: 模型ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelId: str
        :param ModelName: 模型名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelName: str
        :param ModelVersion: 模型版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelVersion: str
        :param ModelSource: 模型来源
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelSource: str
        :param OptimizationLevel: 优化级别
注意：此字段可能返回 null，表示取不到有效值。
        :type OptimizationLevel: str
        :param TaskStatus: 任务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskStatus: str
        :param ModelInputNum: input节点个数
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInputNum: int
        :param ModelInputInfos: input节点信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInputInfos: list of ModelInputInfo
        :param GPUType: GPU型号
注意：此字段可能返回 null，表示取不到有效值。
        :type GPUType: str
        :param ChargeType: 计费模式
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param Speedup: 加速比
注意：此字段可能返回 null，表示取不到有效值。
        :type Speedup: str
        :param ModelInputPath: 模型输入cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelOutputPath: 模型输出cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelOutputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ErrorMsg: 错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param AlgorithmFramework: 算法框架
注意：此字段可能返回 null，表示取不到有效值。
        :type AlgorithmFramework: str
        :param WaitNumber: 排队个数
注意：此字段可能返回 null，表示取不到有效值。
        :type WaitNumber: int
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param TaskProgress: 任务进度
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskProgress: int
        :param ModelFormat: 模型格式
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelFormat: str
        :param TensorInfos: 模型Tensor信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TensorInfos: list of str
        :param HyperParameter: 模型专业参数
注意：此字段可能返回 null，表示取不到有效值。
        :type HyperParameter: :class:`tencentcloud.tione.v20211111.models.HyperParameter`
        :param AccEngineVersion: 加速引擎版本
注意：此字段可能返回 null，表示取不到有效值。
        :type AccEngineVersion: str
        :param Tags: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param IsSaved: 优化模型是否已保存到模型仓库
注意：此字段可能返回 null，表示取不到有效值。
        :type IsSaved: bool
        :param ModelSignature: SAVED_MODEL保存时配置的签名
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelSignature: str
        :param QATModel: 是否是QAT模型
注意：此字段可能返回 null，表示取不到有效值。
        :type QATModel: bool
        """
        self.ModelAccTaskId = None
        self.ModelAccTaskName = None
        self.ModelId = None
        self.ModelName = None
        self.ModelVersion = None
        self.ModelSource = None
        self.OptimizationLevel = None
        self.TaskStatus = None
        self.ModelInputNum = None
        self.ModelInputInfos = None
        self.GPUType = None
        self.ChargeType = None
        self.Speedup = None
        self.ModelInputPath = None
        self.ModelOutputPath = None
        self.ErrorMsg = None
        self.AlgorithmFramework = None
        self.WaitNumber = None
        self.CreateTime = None
        self.TaskProgress = None
        self.ModelFormat = None
        self.TensorInfos = None
        self.HyperParameter = None
        self.AccEngineVersion = None
        self.Tags = None
        self.IsSaved = None
        self.ModelSignature = None
        self.QATModel = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        self.ModelAccTaskName = params.get("ModelAccTaskName")
        self.ModelId = params.get("ModelId")
        self.ModelName = params.get("ModelName")
        self.ModelVersion = params.get("ModelVersion")
        self.ModelSource = params.get("ModelSource")
        self.OptimizationLevel = params.get("OptimizationLevel")
        self.TaskStatus = params.get("TaskStatus")
        self.ModelInputNum = params.get("ModelInputNum")
        if params.get("ModelInputInfos") is not None:
            self.ModelInputInfos = []
            for item in params.get("ModelInputInfos"):
                obj = ModelInputInfo()
                obj._deserialize(item)
                self.ModelInputInfos.append(obj)
        self.GPUType = params.get("GPUType")
        self.ChargeType = params.get("ChargeType")
        self.Speedup = params.get("Speedup")
        if params.get("ModelInputPath") is not None:
            self.ModelInputPath = CosPathInfo()
            self.ModelInputPath._deserialize(params.get("ModelInputPath"))
        if params.get("ModelOutputPath") is not None:
            self.ModelOutputPath = CosPathInfo()
            self.ModelOutputPath._deserialize(params.get("ModelOutputPath"))
        self.ErrorMsg = params.get("ErrorMsg")
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.WaitNumber = params.get("WaitNumber")
        self.CreateTime = params.get("CreateTime")
        self.TaskProgress = params.get("TaskProgress")
        self.ModelFormat = params.get("ModelFormat")
        self.TensorInfos = params.get("TensorInfos")
        if params.get("HyperParameter") is not None:
            self.HyperParameter = HyperParameter()
            self.HyperParameter._deserialize(params.get("HyperParameter"))
        self.AccEngineVersion = params.get("AccEngineVersion")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.IsSaved = params.get("IsSaved")
        self.ModelSignature = params.get("ModelSignature")
        self.QATModel = params.get("QATModel")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelAccelerateVersion(AbstractModel):
    """优化模型版本列表

    """

    def __init__(self):
        r"""
        :param ModelId: 模型id
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelId: str
        :param ModelVersionId: 优化模型版本id
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelVersionId: str
        :param ModelJobId: 优化任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelJobId: str
        :param ModelJobName: 优化任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelJobName: str
        :param ModelVersion: 优化后模型版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelVersion: str
        :param SpeedUp: 加速比
注意：此字段可能返回 null，表示取不到有效值。
        :type SpeedUp: str
        :param ModelSource: 模型来源/任务名称/任务版本
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelSource: :class:`tencentcloud.tione.v20211111.models.ModelSource`
        :param CosPathInfo: 模型cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type CosPathInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param ModelFormat: 模型规范
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelFormat: str
        :param Status: 状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param Progress: 进度
注意：此字段可能返回 null，表示取不到有效值。
        :type Progress: int
        :param ErrorMsg: 错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param GPUType: GPU类型
注意：此字段可能返回 null，表示取不到有效值。
        :type GPUType: str
        :param ModelCosPath: 模型cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelCosPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        """
        self.ModelId = None
        self.ModelVersionId = None
        self.ModelJobId = None
        self.ModelJobName = None
        self.ModelVersion = None
        self.SpeedUp = None
        self.ModelSource = None
        self.CosPathInfo = None
        self.CreateTime = None
        self.ModelFormat = None
        self.Status = None
        self.Progress = None
        self.ErrorMsg = None
        self.GPUType = None
        self.ModelCosPath = None


    def _deserialize(self, params):
        self.ModelId = params.get("ModelId")
        self.ModelVersionId = params.get("ModelVersionId")
        self.ModelJobId = params.get("ModelJobId")
        self.ModelJobName = params.get("ModelJobName")
        self.ModelVersion = params.get("ModelVersion")
        self.SpeedUp = params.get("SpeedUp")
        if params.get("ModelSource") is not None:
            self.ModelSource = ModelSource()
            self.ModelSource._deserialize(params.get("ModelSource"))
        if params.get("CosPathInfo") is not None:
            self.CosPathInfo = CosPathInfo()
            self.CosPathInfo._deserialize(params.get("CosPathInfo"))
        self.CreateTime = params.get("CreateTime")
        self.ModelFormat = params.get("ModelFormat")
        self.Status = params.get("Status")
        self.Progress = params.get("Progress")
        self.ErrorMsg = params.get("ErrorMsg")
        self.GPUType = params.get("GPUType")
        if params.get("ModelCosPath") is not None:
            self.ModelCosPath = CosPathInfo()
            self.ModelCosPath._deserialize(params.get("ModelCosPath"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelInfo(AbstractModel):
    """模型描述信息

    """

    def __init__(self):
        r"""
        :param ModelVersionId: 模型版本id, DescribeTrainingModelVersion查询模型接口时的id
自动学习类型的模型填写自动学习的任务id
        :type ModelVersionId: str
        :param ModelId: 模型id
        :type ModelId: str
        :param ModelName: 模型名
        :type ModelName: str
        :param ModelVersion: 模型版本
        :type ModelVersion: str
        :param ModelSource: 模型来源
        :type ModelSource: str
        :param CosPathInfo: cos路径信息
        :type CosPathInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param AlgorithmFramework: 模型对应的算法框架，预留
注意：此字段可能返回 null，表示取不到有效值。
        :type AlgorithmFramework: str
        :param ModelType: 默认为 NORMAL, 已加速模型: ACCELERATE, 自动学习模型 AUTO_ML
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelType: str
        :param GpuType: 模型的GPU类型，仅ModelType为ACCELERATE时有效，标识加速后的模型需要运行的GPU类型
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuType: str
        """
        self.ModelVersionId = None
        self.ModelId = None
        self.ModelName = None
        self.ModelVersion = None
        self.ModelSource = None
        self.CosPathInfo = None
        self.AlgorithmFramework = None
        self.ModelType = None
        self.GpuType = None


    def _deserialize(self, params):
        self.ModelVersionId = params.get("ModelVersionId")
        self.ModelId = params.get("ModelId")
        self.ModelName = params.get("ModelName")
        self.ModelVersion = params.get("ModelVersion")
        self.ModelSource = params.get("ModelSource")
        if params.get("CosPathInfo") is not None:
            self.CosPathInfo = CosPathInfo()
            self.CosPathInfo._deserialize(params.get("CosPathInfo"))
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.ModelType = params.get("ModelType")
        self.GpuType = params.get("GpuType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelInputInfo(AbstractModel):
    """模型输入信息

    """

    def __init__(self):
        r"""
        :param ModelInputType: input数据类型
FIXED：固定
RANGE：浮动
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInputType: str
        :param ModelInputDimension: input数据尺寸
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInputDimension: list of str
        """
        self.ModelInputType = None
        self.ModelInputDimension = None


    def _deserialize(self, params):
        self.ModelInputType = params.get("ModelInputType")
        self.ModelInputDimension = params.get("ModelInputDimension")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelSource(AbstractModel):
    """模型来源

    """

    def __init__(self):
        r"""
        :param Source: 来源
注意：此字段可能返回 null，表示取不到有效值。
        :type Source: str
        :param JobName: 来源任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type JobName: str
        :param JobVersion: 来源任务版本
注意：此字段可能返回 null，表示取不到有效值。
        :type JobVersion: str
        :param JobId: 来源任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type JobId: str
        :param ModelName: 模型名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelName: str
        :param AlgorithmFramework: 算法框架
注意：此字段可能返回 null，表示取不到有效值。
        :type AlgorithmFramework: str
        :param TrainingPreference: 训练偏好
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingPreference: str
        :param ReasoningEnvironmentSource: 推理环境来源，SYSTEM/CUSTOM
注意：此字段可能返回 null，表示取不到有效值。
        :type ReasoningEnvironmentSource: str
        :param ReasoningEnvironment: 推理环境
注意：此字段可能返回 null，表示取不到有效值。
        :type ReasoningEnvironment: str
        :param ReasoningEnvironmentId: 推理环境id
注意：此字段可能返回 null，表示取不到有效值。
        :type ReasoningEnvironmentId: str
        :param ReasoningImageInfo: 自定义推理环境
注意：此字段可能返回 null，表示取不到有效值。
        :type ReasoningImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        """
        self.Source = None
        self.JobName = None
        self.JobVersion = None
        self.JobId = None
        self.ModelName = None
        self.AlgorithmFramework = None
        self.TrainingPreference = None
        self.ReasoningEnvironmentSource = None
        self.ReasoningEnvironment = None
        self.ReasoningEnvironmentId = None
        self.ReasoningImageInfo = None


    def _deserialize(self, params):
        self.Source = params.get("Source")
        self.JobName = params.get("JobName")
        self.JobVersion = params.get("JobVersion")
        self.JobId = params.get("JobId")
        self.ModelName = params.get("ModelName")
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.TrainingPreference = params.get("TrainingPreference")
        self.ReasoningEnvironmentSource = params.get("ReasoningEnvironmentSource")
        self.ReasoningEnvironment = params.get("ReasoningEnvironment")
        self.ReasoningEnvironmentId = params.get("ReasoningEnvironmentId")
        if params.get("ReasoningImageInfo") is not None:
            self.ReasoningImageInfo = ImageInfo()
            self.ReasoningImageInfo._deserialize(params.get("ReasoningImageInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModelTrainConfig(AbstractModel):
    """模型训练配置

    """

    def __init__(self):
        r"""
        :param ModelType: 模型偏好设置
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelType: str
        :param IsIncrementalLearning: 是否开启增量训练
注意：此字段可能返回 null，表示取不到有效值。
        :type IsIncrementalLearning: bool
        :param AutoMLTaskId: 增量训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoMLTaskId: str
        :param ExpectedAccuracy: 期望准确率
注意：此字段可能返回 null，表示取不到有效值。
        :type ExpectedAccuracy: int
        :param EnableMaxTrainHours: 是否开启最长时长限制
注意：此字段可能返回 null，表示取不到有效值。
        :type EnableMaxTrainHours: bool
        :param MaxTrainHours: 最长训练时长
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxTrainHours: int
        """
        self.ModelType = None
        self.IsIncrementalLearning = None
        self.AutoMLTaskId = None
        self.ExpectedAccuracy = None
        self.EnableMaxTrainHours = None
        self.MaxTrainHours = None


    def _deserialize(self, params):
        self.ModelType = params.get("ModelType")
        self.IsIncrementalLearning = params.get("IsIncrementalLearning")
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.ExpectedAccuracy = params.get("ExpectedAccuracy")
        self.EnableMaxTrainHours = params.get("EnableMaxTrainHours")
        self.MaxTrainHours = params.get("MaxTrainHours")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAnnotateTaskReopenRequest(AbstractModel):
    """ModifyAnnotateTaskReopen请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param DataSetId: 数据集ID
        :type DataSetId: str
        """
        self.TaskId = None
        self.DataSetId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.DataSetId = params.get("DataSetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAnnotateTaskReopenResponse(AbstractModel):
    """ModifyAnnotateTaskReopen返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAnnotateTaskTagsRequest(AbstractModel):
    """ModifyAnnotateTaskTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param Tags: 需要修改的标签
        :type Tags: list of Tag
        """
        self.TaskId = None
        self.Tags = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAnnotateTaskTagsResponse(AbstractModel):
    """ModifyAnnotateTaskTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class ModifyAnnotateTaskToSubmitRequest(AbstractModel):
    """ModifyAnnotateTaskToSubmit请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 标注任务ID
        :type TaskId: str
        """
        self.TaskId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAnnotateTaskToSubmitResponse(AbstractModel):
    """ModifyAnnotateTaskToSubmit返回参数结构体

    """

    def __init__(self):
        r"""
        :param Success: 是否成功
        :type Success: bool
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Success = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Success = params.get("Success")
        self.RequestId = params.get("RequestId")


class ModifyAnnotatedResultRequest(AbstractModel):
    """ModifyAnnotatedResult请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 修改的任务
        :type TaskId: str
        :param FileIds: 修改的文件id
        :type FileIds: list of str
        :param AnnotationResult: 标注结果
        :type AnnotationResult: str
        """
        self.TaskId = None
        self.FileIds = None
        self.AnnotationResult = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.FileIds = params.get("FileIds")
        self.AnnotationResult = params.get("AnnotationResult")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAnnotatedResultResponse(AbstractModel):
    """ModifyAnnotatedResult返回参数结构体

    """

    def __init__(self):
        r"""
        :param FileIds: 修改成功的文件id
        :type FileIds: list of str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FileIds = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FileIds = params.get("FileIds")
        self.RequestId = params.get("RequestId")


class ModifyAnnotationKeysRequest(AbstractModel):
    """ModifyAnnotationKeys请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param KeyType: key类型
        :type KeyType: int
        :param KeySet: keypair set
        :type KeySet: :class:`tencentcloud.tione.v20211111.models.KeySetType`
        """
        self.DatasetId = None
        self.KeyType = None
        self.KeySet = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.KeyType = params.get("KeyType")
        if params.get("KeySet") is not None:
            self.KeySet = KeySetType()
            self.KeySet._deserialize(params.get("KeySet"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAnnotationKeysResponse(AbstractModel):
    """ModifyAnnotationKeys返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyAutoMLTaskTagsRequest(AbstractModel):
    """ModifyAutoMLTaskTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务id
        :type AutoMLTaskId: str
        :param Tags: 修改后的标签组
        :type Tags: list of Tag
        """
        self.AutoMLTaskId = None
        self.Tags = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyAutoMLTaskTagsResponse(AbstractModel):
    """ModifyAutoMLTaskTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param ErrorMsg: 出现异常时错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ErrorMsg = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ErrorMsg = params.get("ErrorMsg")
        self.RequestId = params.get("RequestId")


class ModifyBadcasePreviewStatusRequest(AbstractModel):
    """ModifyBadcasePreviewStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param PreviewStatus: badcase预览状态，OFF(关闭), ON(开启)
        :type PreviewStatus: str
        """
        self.PreviewStatus = None


    def _deserialize(self, params):
        self.PreviewStatus = params.get("PreviewStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBadcasePreviewStatusResponse(AbstractModel):
    """ModifyBadcasePreviewStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBatchTaskTagsRequest(AbstractModel):
    """ModifyBatchTaskTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 任务id
        :type BatchTaskId: str
        :param Tags: 标签列表
        :type Tags: list of Tag
        """
        self.BatchTaskId = None
        self.Tags = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBatchTaskTagsResponse(AbstractModel):
    """ModifyBatchTaskTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyBillingResourceGroupRequest(AbstractModel):
    """ModifyBillingResourceGroup请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        :param Name: 资源组名称
注意：此字段仅支持英文、数字、下划线 _、短横 -，只能以英文、数字开头，长度为60个字
注意：此字段相同地域相同资源组类型下不可同名。
        :type Name: str
        :param Type: 资源组类型;
枚举值: TRAIN: 训练, INFERENCE: 推理
        :type Type: str
        :param TagSet: 资源组标签列表
        :type TagSet: list of Tag
        """
        self.ResourceGroupId = None
        self.Name = None
        self.Type = None
        self.TagSet = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyBillingResourceGroupResponse(AbstractModel):
    """ModifyBillingResourceGroup返回参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ResourceGroupId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.RequestId = params.get("RequestId")


class ModifyCodeRepoRequest(AbstractModel):
    """ModifyCodeRepo请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 存储库id
        :type Id: str
        :param GitSecret: Git的认证信息
        :type GitSecret: :class:`tencentcloud.tione.v20211111.models.GitSecret`
        """
        self.Id = None
        self.GitSecret = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        if params.get("GitSecret") is not None:
            self.GitSecret = GitSecret()
            self.GitSecret._deserialize(params.get("GitSecret"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyCodeRepoResponse(AbstractModel):
    """ModifyCodeRepo返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDatasetAnnotationStatusRequest(AbstractModel):
    """ModifyDatasetAnnotationStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param AnnotationType: 标注类型：
ANNOTATION_TYPE_CLASSIFICATION，图片分类
ANNOTATION_TYPE_DETECTION，目标检测
ANNOTATION_TYPE_SEGMENTATION，图片分割
ANNOTATION_TYPE_TRACKING，目标跟踪
ANNOTATION_TYPE_OCR，OCR识别
        :type AnnotationType: str
        :param AnnotationStatus: 标注格式：
ANNOTATION_FORMAT_TI，TI平台格式
ANNOTATION_FORMAT_PASCAL，Pascal Voc
ANNOTATION_FORMAT_COCO，COCO
ANNOTATION_FORMAT_FILE，文件目录结构
        :type AnnotationStatus: str
        """
        self.DatasetId = None
        self.AnnotationType = None
        self.AnnotationStatus = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.AnnotationType = params.get("AnnotationType")
        self.AnnotationStatus = params.get("AnnotationStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDatasetAnnotationStatusResponse(AbstractModel):
    """ModifyDatasetAnnotationStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDatasetPerspectiveStatusRequest(AbstractModel):
    """ModifyDatasetPerspectiveStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param PerspectiveStatus: true：开启，false：关闭
        :type PerspectiveStatus: bool
        :param DatasetIds: 数据集Id数组
        :type DatasetIds: list of str
        """
        self.PerspectiveStatus = None
        self.DatasetIds = None


    def _deserialize(self, params):
        self.PerspectiveStatus = params.get("PerspectiveStatus")
        self.DatasetIds = params.get("DatasetIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDatasetPerspectiveStatusResponse(AbstractModel):
    """ModifyDatasetPerspectiveStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDatasetPreviewStatusRequest(AbstractModel):
    """ModifyDatasetPreviewStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param PreviewStatus: 数据集预览状态，true为开启，false为关闭
        :type PreviewStatus: bool
        """
        self.PreviewStatus = None


    def _deserialize(self, params):
        self.PreviewStatus = params.get("PreviewStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDatasetPreviewStatusResponse(AbstractModel):
    """ModifyDatasetPreviewStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyDatasetTagsRequest(AbstractModel):
    """ModifyDatasetTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param DatasetTags: 标签列表
        :type DatasetTags: list of Tag
        """
        self.DatasetId = None
        self.DatasetTags = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        if params.get("DatasetTags") is not None:
            self.DatasetTags = []
            for item in params.get("DatasetTags"):
                obj = Tag()
                obj._deserialize(item)
                self.DatasetTags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyDatasetTagsResponse(AbstractModel):
    """ModifyDatasetTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasetId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.RequestId = params.get("RequestId")


class ModifyFixedPointRequest(AbstractModel):
    """ModifyFixedPoint请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param FixedPoint: 需要固定的点数
        :type FixedPoint: int
        """
        self.TaskId = None
        self.FixedPoint = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.FixedPoint = params.get("FixedPoint")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyFixedPointResponse(AbstractModel):
    """ModifyFixedPoint返回参数结构体

    """

    def __init__(self):
        r"""
        :param FixedPoint: 修改后的点数
        :type FixedPoint: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FixedPoint = None
        self.RequestId = None


    def _deserialize(self, params):
        self.FixedPoint = params.get("FixedPoint")
        self.RequestId = params.get("RequestId")


class ModifyLifecycleScriptRequest(AbstractModel):
    """ModifyLifecycleScript请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 生命周期脚本Id
        :type Id: str
        :param CreateScript: 创建脚本，需要base64编码，base64编码后的长度不能超过16384
        :type CreateScript: str
        :param StartScript: 动脚本, 需要base64编码，base64编码后的长度不能超过16384
        :type StartScript: str
        """
        self.Id = None
        self.CreateScript = None
        self.StartScript = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.CreateScript = params.get("CreateScript")
        self.StartScript = params.get("StartScript")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyLifecycleScriptResponse(AbstractModel):
    """ModifyLifecycleScript返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyModelAccTaskTagsRequest(AbstractModel):
    """ModifyModelAccTaskTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        :param Tags: 标签
        :type Tags: list of Tag
        """
        self.ModelAccTaskId = None
        self.Tags = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyModelAccTaskTagsResponse(AbstractModel):
    """ModifyModelAccTaskTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyModelServicePartialConfigRequest(AbstractModel):
    """ModifyModelServicePartialConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceId: 在线推理服务Id，需已存在
        :type ServiceId: str
        :param ScheduledAction: 更新后服务不重启，定时停止的配置
        :type ScheduledAction: :class:`tencentcloud.tione.v20211111.models.ScheduledAction`
        :param ServiceLimit: 更新后服务不重启，服务对应限流限频配置
        :type ServiceLimit: :class:`tencentcloud.tione.v20211111.models.ServiceLimit`
        """
        self.ServiceId = None
        self.ScheduledAction = None
        self.ServiceLimit = None


    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        if params.get("ScheduledAction") is not None:
            self.ScheduledAction = ScheduledAction()
            self.ScheduledAction._deserialize(params.get("ScheduledAction"))
        if params.get("ServiceLimit") is not None:
            self.ServiceLimit = ServiceLimit()
            self.ServiceLimit._deserialize(params.get("ServiceLimit"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyModelServicePartialConfigResponse(AbstractModel):
    """ModifyModelServicePartialConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param Service: 被修改后的服务配置
        :type Service: :class:`tencentcloud.tione.v20211111.models.Service`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Service = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Service") is not None:
            self.Service = Service()
            self.Service._deserialize(params.get("Service"))
        self.RequestId = params.get("RequestId")


class ModifyModelServiceRequest(AbstractModel):
    """ModifyModelService请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceId: 服务id
        :type ServiceId: str
        :param ModelInfo: 模型信息，需要挂载模型时填写
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param ImageInfo: 镜像信息，配置服务运行所需的镜像地址等信息
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param Env: 环境变量，可选参数，用于配置容器中的环境变量
        :type Env: list of EnvVar
        :param Resources: 资源描述，指定预付费模式下的cpu,mem,gpu等信息，后付费无需填写
        :type Resources: :class:`tencentcloud.tione.v20211111.models.ResourceInfo`
        :param InstanceType: 使用DescribeBillingSpecs接口返回的规格列表中的值，或者参考实例列表:
TI.S.MEDIUM.POST	2C4G
TI.S.LARGE.POST	4C8G
TI.S.2XLARGE16.POST	8C16G
TI.S.2XLARGE32.POST	8C32G
TI.S.4XLARGE32.POST	16C32G
TI.S.4XLARGE64.POST	16C64G
TI.S.6XLARGE48.POST	24C48G
TI.S.6XLARGE96.POST	24C96G
TI.S.8XLARGE64.POST	32C64G
TI.S.8XLARGE128.POST 32C128G
TI.GN7.LARGE20.POST	4C20G T4*1/4
TI.GN7.2XLARGE40.POST	10C40G T4*1/2
TI.GN7.2XLARGE32.POST	8C32G T4*1
TI.GN7.5XLARGE80.POST	20C80G T4*1
TI.GN7.8XLARGE128.POST	32C128G T4*1
TI.GN7.10XLARGE160.POST	40C160G T4*2
TI.GN7.20XLARGE320.POST	80C320G T4*4
        :type InstanceType: str
        :param ScaleMode: 扩缩容类型 支持：自动 - "AUTO", 手动 - "MANUAL"
        :type ScaleMode: str
        :param Replicas: 实例数量, 不同计费模式和调节模式下对应关系如下
PREPAID 和 POSTPAID_BY_HOUR:
手动调节模式下对应 实例数量
自动调节模式下对应 基于时间的默认策略的实例数量
HYBRID_PAID:
后付费实例手动调节模式下对应 实例数量
后付费实例自动调节模式下对应 时间策略的默认策略的实例数量
        :type Replicas: int
        :param HorizontalPodAutoscaler: 自动伸缩信息
        :type HorizontalPodAutoscaler: :class:`tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param LogEnable: 是否开启日志投递，开启后需填写配置投递到指定cls
        :type LogEnable: bool
        :param LogConfig: 日志配置，需要投递服务日志到指定cls时填写
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param ServiceAction: 特殊更新行为： "STOP": 停止, "RESUME": 重启, "SCALE": 扩缩容, 存在这些特殊更新行为时，会忽略其他更新字段
        :type ServiceAction: str
        :param ServiceDescription: 服务的描述
        :type ServiceDescription: str
        :param ScaleStrategy: 自动伸缩策略
        :type ScaleStrategy: str
        :param CronScaleJobs: 自动伸缩策略配置 HPA : 通过HPA进行弹性伸缩 CRON 通过定时任务进行伸缩
        :type CronScaleJobs: list of CronScaleJob
        :param HybridBillingPrepaidReplicas: 计费模式[HYBRID_PAID]时生效, 用于标识混合计费模式下的预付费实例数, 若不填则默认为1
        :type HybridBillingPrepaidReplicas: int
        :param ModelHotUpdateEnable: 是否开启模型的热更新。默认不开启
        :type ModelHotUpdateEnable: bool
        :param ScheduledAction: 定时停止配置
        :type ScheduledAction: :class:`tencentcloud.tione.v20211111.models.ScheduledAction`
        :param ServiceLimit: 服务限速限流相关配置
        :type ServiceLimit: :class:`tencentcloud.tione.v20211111.models.ServiceLimit`
        :param VolumeMount: 挂载配置，目前只支持CFS
        :type VolumeMount: :class:`tencentcloud.tione.v20211111.models.VolumeMount`
        :param AuthorizationEnable: 是否开启鉴权、目前更新时不支持更新，仅用于方便前端提交参数，不做任何处理，且参数不展示
        :type AuthorizationEnable: bool
        """
        self.ServiceId = None
        self.ModelInfo = None
        self.ImageInfo = None
        self.Env = None
        self.Resources = None
        self.InstanceType = None
        self.ScaleMode = None
        self.Replicas = None
        self.HorizontalPodAutoscaler = None
        self.LogEnable = None
        self.LogConfig = None
        self.ServiceAction = None
        self.ServiceDescription = None
        self.ScaleStrategy = None
        self.CronScaleJobs = None
        self.HybridBillingPrepaidReplicas = None
        self.ModelHotUpdateEnable = None
        self.ScheduledAction = None
        self.ServiceLimit = None
        self.VolumeMount = None
        self.AuthorizationEnable = None


    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        if params.get("Env") is not None:
            self.Env = []
            for item in params.get("Env"):
                obj = EnvVar()
                obj._deserialize(item)
                self.Env.append(obj)
        if params.get("Resources") is not None:
            self.Resources = ResourceInfo()
            self.Resources._deserialize(params.get("Resources"))
        self.InstanceType = params.get("InstanceType")
        self.ScaleMode = params.get("ScaleMode")
        self.Replicas = params.get("Replicas")
        if params.get("HorizontalPodAutoscaler") is not None:
            self.HorizontalPodAutoscaler = HorizontalPodAutoscaler()
            self.HorizontalPodAutoscaler._deserialize(params.get("HorizontalPodAutoscaler"))
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.ServiceAction = params.get("ServiceAction")
        self.ServiceDescription = params.get("ServiceDescription")
        self.ScaleStrategy = params.get("ScaleStrategy")
        if params.get("CronScaleJobs") is not None:
            self.CronScaleJobs = []
            for item in params.get("CronScaleJobs"):
                obj = CronScaleJob()
                obj._deserialize(item)
                self.CronScaleJobs.append(obj)
        self.HybridBillingPrepaidReplicas = params.get("HybridBillingPrepaidReplicas")
        self.ModelHotUpdateEnable = params.get("ModelHotUpdateEnable")
        if params.get("ScheduledAction") is not None:
            self.ScheduledAction = ScheduledAction()
            self.ScheduledAction._deserialize(params.get("ScheduledAction"))
        if params.get("ServiceLimit") is not None:
            self.ServiceLimit = ServiceLimit()
            self.ServiceLimit._deserialize(params.get("ServiceLimit"))
        if params.get("VolumeMount") is not None:
            self.VolumeMount = VolumeMount()
            self.VolumeMount._deserialize(params.get("VolumeMount"))
        self.AuthorizationEnable = params.get("AuthorizationEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyModelServiceResponse(AbstractModel):
    """ModifyModelService返回参数结构体

    """

    def __init__(self):
        r"""
        :param Service: 生成的模型服务
注意：此字段可能返回 null，表示取不到有效值。
        :type Service: :class:`tencentcloud.tione.v20211111.models.Service`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Service = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("Service") is not None:
            self.Service = Service()
            self.Service._deserialize(params.get("Service"))
        self.RequestId = params.get("RequestId")


class ModifyModelTagsRequest(AbstractModel):
    """ModifyModelTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param TrainingModelId: 模型ID
        :type TrainingModelId: str
        :param Tags: 标签
        :type Tags: list of Tag
        """
        self.TrainingModelId = None
        self.Tags = None


    def _deserialize(self, params):
        self.TrainingModelId = params.get("TrainingModelId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyModelTagsResponse(AbstractModel):
    """ModifyModelTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNotebookAutoStoppingRequest(AbstractModel):
    """ModifyNotebookAutoStopping请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: id值
        :type Id: str
        :param AutoStopping: 是否自动停止
        :type AutoStopping: bool
        :param AutomaticStopTime: 自动停止时间，单位小时
        :type AutomaticStopTime: int
        """
        self.Id = None
        self.AutoStopping = None
        self.AutomaticStopTime = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.AutoStopping = params.get("AutoStopping")
        self.AutomaticStopTime = params.get("AutomaticStopTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNotebookAutoStoppingResponse(AbstractModel):
    """ModifyNotebookAutoStopping返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNotebookRequest(AbstractModel):
    """ModifyNotebook请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook id
        :type Id: str
        :param Name: 名称
        :type Name: str
        :param ChargeType: 计算资源付费模式 ，可选值为：
PREPAID：预付费，即包年包月
POSTPAID_BY_HOUR：按小时后付费
        :type ChargeType: str
        :param ResourceConf: 计算资源配置
        :type ResourceConf: :class:`tencentcloud.tione.v20211111.models.ResourceConf`
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param AutoStopping: 是否自动停止
        :type AutoStopping: bool
        :param DirectInternetAccess: 是否访问公网
        :type DirectInternetAccess: bool
        :param RootAccess: 是否ROOT权限
        :type RootAccess: bool
        :param ResourceGroupId: 资源组ID(for预付费)
        :type ResourceGroupId: str
        :param VpcId: Vpc-Id
        :type VpcId: str
        :param SubnetId: 子网Id
        :type SubnetId: str
        :param VolumeSizeInGB: 存储卷大小，单位GB
        :type VolumeSizeInGB: int
        :param VolumeSourceType: 存储的类型。取值包含： 
    FREE:    预付费的免费存储
    CLOUD_PREMIUM： 高性能云硬盘
    CLOUD_SSD： SSD云硬盘
    CFS:     CFS存储，包含NFS和turbo
        :type VolumeSourceType: str
        :param VolumeSourceCFS: CFS存储的配置
        :type VolumeSourceCFS: :class:`tencentcloud.tione.v20211111.models.CFSConfig`
        :param LogConfig: 日志配置
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param LifecycleScriptId: 生命周期脚本的ID
        :type LifecycleScriptId: str
        :param DefaultCodeRepoId: 默认GIT存储库的ID
        :type DefaultCodeRepoId: str
        :param AdditionalCodeRepoIds: 其他GIT存储库的ID，最多3个
        :type AdditionalCodeRepoIds: list of str
        :param AutomaticStopTime: 自动停止时间，单位小时
        :type AutomaticStopTime: int
        :param Tags: 标签配置
        :type Tags: list of Tag
        :param DataConfigs: 数据配置
        :type DataConfigs: list of DataConfig
        """
        self.Id = None
        self.Name = None
        self.ChargeType = None
        self.ResourceConf = None
        self.LogEnable = None
        self.AutoStopping = None
        self.DirectInternetAccess = None
        self.RootAccess = None
        self.ResourceGroupId = None
        self.VpcId = None
        self.SubnetId = None
        self.VolumeSizeInGB = None
        self.VolumeSourceType = None
        self.VolumeSourceCFS = None
        self.LogConfig = None
        self.LifecycleScriptId = None
        self.DefaultCodeRepoId = None
        self.AdditionalCodeRepoIds = None
        self.AutomaticStopTime = None
        self.Tags = None
        self.DataConfigs = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.ChargeType = params.get("ChargeType")
        if params.get("ResourceConf") is not None:
            self.ResourceConf = ResourceConf()
            self.ResourceConf._deserialize(params.get("ResourceConf"))
        self.LogEnable = params.get("LogEnable")
        self.AutoStopping = params.get("AutoStopping")
        self.DirectInternetAccess = params.get("DirectInternetAccess")
        self.RootAccess = params.get("RootAccess")
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.VolumeSizeInGB = params.get("VolumeSizeInGB")
        self.VolumeSourceType = params.get("VolumeSourceType")
        if params.get("VolumeSourceCFS") is not None:
            self.VolumeSourceCFS = CFSConfig()
            self.VolumeSourceCFS._deserialize(params.get("VolumeSourceCFS"))
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.LifecycleScriptId = params.get("LifecycleScriptId")
        self.DefaultCodeRepoId = params.get("DefaultCodeRepoId")
        self.AdditionalCodeRepoIds = params.get("AdditionalCodeRepoIds")
        self.AutomaticStopTime = params.get("AutomaticStopTime")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNotebookResponse(AbstractModel):
    """ModifyNotebook返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyNotebookTagsRequest(AbstractModel):
    """ModifyNotebookTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: Notebook Id
        :type Id: str
        :param Tags: Notebook修改标签集合
        :type Tags: list of Tag
        """
        self.Id = None
        self.Tags = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyNotebookTagsResponse(AbstractModel):
    """ModifyNotebookTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyServiceGroupWeightsRequest(AbstractModel):
    """ModifyServiceGroupWeights请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 服务组id
        :type ServiceGroupId: str
        :param Weights: 权重设置
        :type Weights: list of WeightEntry
        """
        self.ServiceGroupId = None
        self.Weights = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        if params.get("Weights") is not None:
            self.Weights = []
            for item in params.get("Weights"):
                obj = WeightEntry()
                obj._deserialize(item)
                self.Weights.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyServiceGroupWeightsResponse(AbstractModel):
    """ModifyServiceGroupWeights返回参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroup: 更新权重后的服务组信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceGroup: :class:`tencentcloud.tione.v20211111.models.ServiceGroup`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ServiceGroup = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("ServiceGroup") is not None:
            self.ServiceGroup = ServiceGroup()
            self.ServiceGroup._deserialize(params.get("ServiceGroup"))
        self.RequestId = params.get("RequestId")


class ModifyTagsRequest(AbstractModel):
    """ModifyTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 模型服务的服务组id
        :type ServiceGroupId: str
        :param Tags: 标签数组
        :type Tags: list of Tag
        """
        self.ServiceGroupId = None
        self.Tags = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyTagsResponse(AbstractModel):
    """ModifyTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ModifyTaskDisplayConfigRequest(AbstractModel):
    """ModifyTaskDisplayConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务id
        :type TaskId: str
        :param BgColor: 背景颜色
        :type BgColor: str
        :param FontFamily: 字体系列
        :type FontFamily: str
        :param FontSize: 字体大小
        :type FontSize: str
        """
        self.TaskId = None
        self.BgColor = None
        self.FontFamily = None
        self.FontSize = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.BgColor = params.get("BgColor")
        self.FontFamily = params.get("FontFamily")
        self.FontSize = params.get("FontSize")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyTaskDisplayConfigResponse(AbstractModel):
    """ModifyTaskDisplayConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param BgColor: 背景颜色
        :type BgColor: str
        :param FontFamily: 字体系列
        :type FontFamily: str
        :param FontSize: 字体大小
        :type FontSize: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.BgColor = None
        self.FontFamily = None
        self.FontSize = None
        self.RequestId = None


    def _deserialize(self, params):
        self.BgColor = params.get("BgColor")
        self.FontFamily = params.get("FontFamily")
        self.FontSize = params.get("FontSize")
        self.RequestId = params.get("RequestId")


class ModifyTaskLabelValueRequest(AbstractModel):
    """ModifyTaskLabelValue请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param LabelName: 标签名
        :type LabelName: str
        :param LabelColor: 标签颜色(分类场景无需)
        :type LabelColor: str
        """
        self.TaskId = None
        self.LabelName = None
        self.LabelColor = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.LabelName = params.get("LabelName")
        self.LabelColor = params.get("LabelColor")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyTaskLabelValueResponse(AbstractModel):
    """ModifyTaskLabelValue返回参数结构体

    """

    def __init__(self):
        r"""
        :param LabelName: 标签名
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelName: str
        :param LabelColor: 标签颜色(分类场景无需)
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelColor: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.LabelName = None
        self.LabelColor = None
        self.RequestId = None


    def _deserialize(self, params):
        self.LabelName = params.get("LabelName")
        self.LabelColor = params.get("LabelColor")
        self.RequestId = params.get("RequestId")


class ModifyTaskProcessingStatusRequest(AbstractModel):
    """ModifyTaskProcessingStatus请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param ProcessingStatus: 状态取值范围0-2
        :type ProcessingStatus: int
        """
        self.TaskId = None
        self.ProcessingStatus = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.ProcessingStatus = params.get("ProcessingStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyTaskProcessingStatusResponse(AbstractModel):
    """ModifyTaskProcessingStatus返回参数结构体

    """

    def __init__(self):
        r"""
        :param ProcessingStatus: 状态取值范围0-2
        :type ProcessingStatus: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ProcessingStatus = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ProcessingStatus = params.get("ProcessingStatus")
        self.RequestId = params.get("RequestId")


class ModifyTaskTagsRequest(AbstractModel):
    """ModifyTaskTags请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        :param Tags: 标签列表
        :type Tags: list of Tag
        """
        self.Id = None
        self.Tags = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ModifyTaskTagsResponse(AbstractModel):
    """ModifyTaskTags返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class NLPBadcaseItem(AbstractModel):
    """NLPBadcase项

    """

    def __init__(self):
        r"""
        :param Topic: 题目
        :type Topic: str
        :param GroundTruthLabels: gt标签
        :type GroundTruthLabels: list of str
        :param PredictLabels: pred标签
        :type PredictLabels: list of str
        :param DatasetId: 数据集id
        :type DatasetId: str
        :param SampleId: 文本id
        :type SampleId: str
        :param Summary: 文本摘要
        :type Summary: str
        :param IsBadCase: 是否为badcase
        :type IsBadCase: bool
        """
        self.Topic = None
        self.GroundTruthLabels = None
        self.PredictLabels = None
        self.DatasetId = None
        self.SampleId = None
        self.Summary = None
        self.IsBadCase = None


    def _deserialize(self, params):
        self.Topic = params.get("Topic")
        self.GroundTruthLabels = params.get("GroundTruthLabels")
        self.PredictLabels = params.get("PredictLabels")
        self.DatasetId = params.get("DatasetId")
        self.SampleId = params.get("SampleId")
        self.Summary = params.get("Summary")
        self.IsBadCase = params.get("IsBadCase")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NLPIndicatorItem(AbstractModel):
    """NLP基础指标

    """

    def __init__(self):
        r"""
        :param Topic: 题目
        :type Topic: str
        :param MultiLabel: 是否为多标签
        :type MultiLabel: bool
        :param Accuracy: 准确率
        :type Accuracy: float
        :param Precision: 精确率
        :type Precision: float
        :param Recall: 召回率
        :type Recall: float
        :param MacroFScore: 宏平均
        :type MacroFScore: float
        :param MicroFScore: 微平均
        :type MicroFScore: float
        """
        self.Topic = None
        self.MultiLabel = None
        self.Accuracy = None
        self.Precision = None
        self.Recall = None
        self.MacroFScore = None
        self.MicroFScore = None


    def _deserialize(self, params):
        self.Topic = params.get("Topic")
        self.MultiLabel = params.get("MultiLabel")
        self.Accuracy = params.get("Accuracy")
        self.Precision = params.get("Precision")
        self.Recall = params.get("Recall")
        self.MacroFScore = params.get("MacroFScore")
        self.MicroFScore = params.get("MicroFScore")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NLPItem(AbstractModel):
    """NlpItem项

    """

    def __init__(self):
        r"""
        :param Topic: 题目
        :type Topic: str
        :param GtLabels: gt标签
        :type GtLabels: list of str
        :param PredictionLabels: pred标签
        :type PredictionLabels: list of str
        """
        self.Topic = None
        self.GtLabels = None
        self.PredictionLabels = None


    def _deserialize(self, params):
        self.Topic = params.get("Topic")
        self.GtLabels = params.get("GtLabels")
        self.PredictionLabels = params.get("PredictionLabels")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NLPPredictResult(AbstractModel):
    """文本分类预测结果

    """

    def __init__(self):
        r"""
        :param Topic: 问题类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Topic: str
        :param Category: 文本类别
        :type Category: list of str
        :param Score: 置信度
        :type Score: float
        """
        self.Topic = None
        self.Category = None
        self.Score = None


    def _deserialize(self, params):
        self.Topic = params.get("Topic")
        self.Category = params.get("Category")
        self.Score = params.get("Score")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NLPSample(AbstractModel):
    """自动学习文本分类样本

    """

    def __init__(self):
        r"""
        :param Text: 样本内容
        :type Text: str
        :param RecordId: 样本id
        :type RecordId: str
        """
        self.Text = None
        self.RecordId = None


    def _deserialize(self, params):
        self.Text = params.get("Text")
        self.RecordId = params.get("RecordId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NLPSamplePredictResult(AbstractModel):
    """文本分类预测结果

    """

    def __init__(self):
        r"""
        :param RecordId: 缓存记录ID
        :type RecordId: str
        :param SampleMD5: 文本内容的MD5值
        :type SampleMD5: str
        :param Content: 文本内容
        :type Content: str
        :param PredictResult: 预测结果
        :type PredictResult: list of NLPPredictResult
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 最近更新时间
        :type UpdateTime: str
        """
        self.RecordId = None
        self.SampleMD5 = None
        self.Content = None
        self.PredictResult = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.RecordId = params.get("RecordId")
        self.SampleMD5 = params.get("SampleMD5")
        self.Content = params.get("Content")
        if params.get("PredictResult") is not None:
            self.PredictResult = []
            for item in params.get("PredictResult"):
                obj = NLPPredictResult()
                obj._deserialize(item)
                self.PredictResult.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NLPTagFilter(AbstractModel):
    """NLP查询条件

    """

    def __init__(self):
        r"""
        :param Name: 查询的名称
        :type Name: str
        :param Predicate: 查询的类型
        :type Predicate: str
        :param NumberValue: 需要查询的数字类型的内容
        :type NumberValue: float
        :param SearchTerm: 用于SEARCH的词
        :type SearchTerm: str
        :param Checked: 用于CHECK的词
        :type Checked: list of str
        """
        self.Name = None
        self.Predicate = None
        self.NumberValue = None
        self.SearchTerm = None
        self.Checked = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Predicate = params.get("Predicate")
        self.NumberValue = params.get("NumberValue")
        self.SearchTerm = params.get("SearchTerm")
        self.Checked = params.get("Checked")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NotebookDetail(AbstractModel):
    """类型NotebookDetail

    """

    def __init__(self):
        r"""
        :param Id: notebook  ID
        :type Id: str
        :param Name: notebook 名称
        :type Name: str
        :param LifecycleScriptId: 生命周期脚本
注意：此字段可能返回 null，表示取不到有效值。
        :type LifecycleScriptId: str
        :param PodName: Pod-Name
注意：此字段可能返回 null，表示取不到有效值。
        :type PodName: str
        :param UpdateTime: Update-Time
        :type UpdateTime: str
        :param DirectInternetAccess: 是否访问公网
        :type DirectInternetAccess: bool
        :param ResourceGroupId: 预付费专用资源组
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param Tags: 标签配置
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param AutoStopping: 是否自动停止
        :type AutoStopping: bool
        :param AdditionalCodeRepoIds: 其他GIT存储库，最多3个，单个
长度不超过512字符
注意：此字段可能返回 null，表示取不到有效值。
        :type AdditionalCodeRepoIds: list of str
        :param AutomaticStopTime: 自动停止时间，单位小时
注意：此字段可能返回 null，表示取不到有效值。
        :type AutomaticStopTime: int
        :param ResourceConf: 资源配置
        :type ResourceConf: :class:`tencentcloud.tione.v20211111.models.ResourceConf`
        :param DefaultCodeRepoId: 默认GIT存储库，长度不超过512字符
        :type DefaultCodeRepoId: str
        :param EndTime: 训练输出
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param LogConfig: 日志配置
注意：此字段可能返回 null，表示取不到有效值。
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param VpcId: VPC ID
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param SubnetId: 子网ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: str
        :param Status: 任务状态
        :type Status: str
        :param RuntimeInSeconds: 运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param StartTime: 训练开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param ChargeStatus: 计费状态，eg：BILLING计费中，ARREARS_STOP欠费停止，NOT_BILLING不在计费中
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeStatus: str
        :param RootAccess: 是否ROOT权限
        :type RootAccess: bool
        :param BillingInfos: 计贺金额信息，eg:2.00元/小时
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfos: list of str
        :param VolumeSizeInGB: 存储卷大小 （单位时GB，最小10GB，必须是10G的倍数）
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeSizeInGB: int
        :param FailureReason: 失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailureReason: str
        :param ChargeType: 计算资源付费模式 (- PREPAID：预付费，即包年包月 - POSTPAID_BY_HOUR：按小时后付费)
        :type ChargeType: str
        :param InstanceTypeAlias: 后付费资源规格说明
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceTypeAlias: str
        :param ResourceGroupName: 预付费资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param VolumeSourceType: 存储的类型。取值包含： 
    FREE:        预付费的免费存储
    CLOUD_PREMIUM： 高性能云硬盘
    CLOUD_SSD： SSD云硬盘
    CFS:     CFS存储，包含NFS和turbo
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeSourceType: str
        :param VolumeSourceCFS: CFS存储的配置
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeSourceCFS: :class:`tencentcloud.tione.v20211111.models.CFSConfig`
        :param DataConfigs: 数据配置
注意：此字段可能返回 null，表示取不到有效值。
        :type DataConfigs: list of DataConfig
        :param Message: notebook 信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param DataSource: 数据源来源，eg：WeData_HDFS
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSource: str
        """
        self.Id = None
        self.Name = None
        self.LifecycleScriptId = None
        self.PodName = None
        self.UpdateTime = None
        self.DirectInternetAccess = None
        self.ResourceGroupId = None
        self.Tags = None
        self.AutoStopping = None
        self.AdditionalCodeRepoIds = None
        self.AutomaticStopTime = None
        self.ResourceConf = None
        self.DefaultCodeRepoId = None
        self.EndTime = None
        self.LogEnable = None
        self.LogConfig = None
        self.VpcId = None
        self.SubnetId = None
        self.Status = None
        self.RuntimeInSeconds = None
        self.CreateTime = None
        self.StartTime = None
        self.ChargeStatus = None
        self.RootAccess = None
        self.BillingInfos = None
        self.VolumeSizeInGB = None
        self.FailureReason = None
        self.ChargeType = None
        self.InstanceTypeAlias = None
        self.ResourceGroupName = None
        self.VolumeSourceType = None
        self.VolumeSourceCFS = None
        self.DataConfigs = None
        self.Message = None
        self.DataSource = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.LifecycleScriptId = params.get("LifecycleScriptId")
        self.PodName = params.get("PodName")
        self.UpdateTime = params.get("UpdateTime")
        self.DirectInternetAccess = params.get("DirectInternetAccess")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AutoStopping = params.get("AutoStopping")
        self.AdditionalCodeRepoIds = params.get("AdditionalCodeRepoIds")
        self.AutomaticStopTime = params.get("AutomaticStopTime")
        if params.get("ResourceConf") is not None:
            self.ResourceConf = ResourceConf()
            self.ResourceConf._deserialize(params.get("ResourceConf"))
        self.DefaultCodeRepoId = params.get("DefaultCodeRepoId")
        self.EndTime = params.get("EndTime")
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        self.Status = params.get("Status")
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.ChargeStatus = params.get("ChargeStatus")
        self.RootAccess = params.get("RootAccess")
        self.BillingInfos = params.get("BillingInfos")
        self.VolumeSizeInGB = params.get("VolumeSizeInGB")
        self.FailureReason = params.get("FailureReason")
        self.ChargeType = params.get("ChargeType")
        self.InstanceTypeAlias = params.get("InstanceTypeAlias")
        self.ResourceGroupName = params.get("ResourceGroupName")
        self.VolumeSourceType = params.get("VolumeSourceType")
        if params.get("VolumeSourceCFS") is not None:
            self.VolumeSourceCFS = CFSConfig()
            self.VolumeSourceCFS._deserialize(params.get("VolumeSourceCFS"))
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        self.Message = params.get("Message")
        self.DataSource = params.get("DataSource")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class NotebookSetItem(AbstractModel):
    """Notebook列表元素

    """

    def __init__(self):
        r"""
        :param Id: notebook ID
        :type Id: str
        :param Name: notebook 名称
        :type Name: str
        :param ChargeType: 计费模式
        :type ChargeType: str
        :param ResourceConf: 资源配置
        :type ResourceConf: :class:`tencentcloud.tione.v20211111.models.ResourceConf`
        :param ResourceGroupId: 预付费资源组
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param VolumeSizeInGB: 存储卷大小
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeSizeInGB: int
        :param BillingInfos: 计费金额信息，eg：2.00元/小时 (for后付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfos: list of str
        :param Tags: 标签配置
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param StartTime: 启动时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param RuntimeInSeconds: 运行时间
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        :param ChargeStatus: 计费状态
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeStatus: str
        :param Status: 状态
        :type Status: str
        :param FailureReason: 错误原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailureReason: str
        :param EndTime: 结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param PodName: Pod名称
注意：此字段可能返回 null，表示取不到有效值。
        :type PodName: str
        :param InstanceTypeAlias: 后付费资源规格名称
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceTypeAlias: str
        :param ResourceGroupName: 预付费资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param AutoStopping: 是否自动终止
        :type AutoStopping: bool
        :param AutomaticStopTime: 自动停止时间
注意：此字段可能返回 null，表示取不到有效值。
        :type AutomaticStopTime: int
        :param VolumeSourceType: 存储的类型。取值包含： 
    FREE:        预付费的免费存储
    CLOUD_PREMIUM： 高性能云硬盘
    CLOUD_SSD： SSD云硬盘
    CFS:     CFS存储，包含NFS和turbo
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeSourceType: str
        :param VolumeSourceCFS: CFS存储的配置
注意：此字段可能返回 null，表示取不到有效值。
        :type VolumeSourceCFS: :class:`tencentcloud.tione.v20211111.models.CFSConfig`
        :param Message: notebook 信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        """
        self.Id = None
        self.Name = None
        self.ChargeType = None
        self.ResourceConf = None
        self.ResourceGroupId = None
        self.VolumeSizeInGB = None
        self.BillingInfos = None
        self.Tags = None
        self.CreateTime = None
        self.StartTime = None
        self.UpdateTime = None
        self.RuntimeInSeconds = None
        self.ChargeStatus = None
        self.Status = None
        self.FailureReason = None
        self.EndTime = None
        self.PodName = None
        self.InstanceTypeAlias = None
        self.ResourceGroupName = None
        self.AutoStopping = None
        self.AutomaticStopTime = None
        self.VolumeSourceType = None
        self.VolumeSourceCFS = None
        self.Message = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.ChargeType = params.get("ChargeType")
        if params.get("ResourceConf") is not None:
            self.ResourceConf = ResourceConf()
            self.ResourceConf._deserialize(params.get("ResourceConf"))
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.VolumeSizeInGB = params.get("VolumeSizeInGB")
        self.BillingInfos = params.get("BillingInfos")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.UpdateTime = params.get("UpdateTime")
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        self.ChargeStatus = params.get("ChargeStatus")
        self.Status = params.get("Status")
        self.FailureReason = params.get("FailureReason")
        self.EndTime = params.get("EndTime")
        self.PodName = params.get("PodName")
        self.InstanceTypeAlias = params.get("InstanceTypeAlias")
        self.ResourceGroupName = params.get("ResourceGroupName")
        self.AutoStopping = params.get("AutoStopping")
        self.AutomaticStopTime = params.get("AutomaticStopTime")
        self.VolumeSourceType = params.get("VolumeSourceType")
        if params.get("VolumeSourceCFS") is not None:
            self.VolumeSourceCFS = CFSConfig()
            self.VolumeSourceCFS._deserialize(params.get("VolumeSourceCFS"))
        self.Message = params.get("Message")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OcrBlock(AbstractModel):
    """自动学习ocr评测结果块内容

    """

    def __init__(self):
        r"""
        :param Bgs: 背景字段
注意：此字段可能返回 null，表示取不到有效值。
        :type Bgs: list of OcrBlockItem
        :param Keys: 识别key字段结果
注意：此字段可能返回 null，表示取不到有效值。
        :type Keys: list of OcrBlockItem
        :param Values: 识别key对应的value结果
注意：此字段可能返回 null，表示取不到有效值。
        :type Values: list of OcrBlockItem
        :param IsCorrect: 识别块内容结果是否正确
注意：此字段可能返回 null，表示取不到有效值。
        :type IsCorrect: bool
        """
        self.Bgs = None
        self.Keys = None
        self.Values = None
        self.IsCorrect = None


    def _deserialize(self, params):
        if params.get("Bgs") is not None:
            self.Bgs = []
            for item in params.get("Bgs"):
                obj = OcrBlockItem()
                obj._deserialize(item)
                self.Bgs.append(obj)
        if params.get("Keys") is not None:
            self.Keys = []
            for item in params.get("Keys"):
                obj = OcrBlockItem()
                obj._deserialize(item)
                self.Keys.append(obj)
        if params.get("Values") is not None:
            self.Values = []
            for item in params.get("Values"):
                obj = OcrBlockItem()
                obj._deserialize(item)
                self.Values.append(obj)
        self.IsCorrect = params.get("IsCorrect")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OcrBlockItem(AbstractModel):
    """自动学习ocr块内容项

    """

    def __init__(self):
        r"""
        :param Coords: 四边形四个定点坐标，顺序为左上，右上，右下，左下
注意：此字段可能返回 null，表示取不到有效值。
        :type Coords: list of float
        :param Content: 识别文字内容
注意：此字段可能返回 null，表示取不到有效值。
        :type Content: str
        :param IsComplement: 是否为补充key
注意：此字段可能返回 null，表示取不到有效值。
        :type IsComplement: bool
        :param IsCorrect: 推理值是否正确
注意：此字段可能返回 null，表示取不到有效值。
        :type IsCorrect: bool
        """
        self.Coords = None
        self.Content = None
        self.IsComplement = None
        self.IsCorrect = None


    def _deserialize(self, params):
        self.Coords = params.get("Coords")
        self.Content = params.get("Content")
        self.IsComplement = params.get("IsComplement")
        self.IsCorrect = params.get("IsCorrect")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OcrInfo(AbstractModel):
    """OCR场景信息

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetId: str
        :param OcrScene: OCR 场景：
IDENTITY，识别
STRUCTURE， 智能结构化
如果改数据集非OCR场景，该字段为空
注意：此字段可能返回 null，表示取不到有效值。
        :type OcrScene: str
        """
        self.DatasetId = None
        self.OcrScene = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.OcrScene = params.get("OcrScene")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OcrLabelInfo(AbstractModel):
    """OCR场景标签列表

    """

    def __init__(self):
        r"""
        :param Points: 坐标点围起来的框
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of PointInfo
        :param FrameType: 框的形状：
FRAME_TYPE_RECTANGLE
FRAME_TYPE_POLYGON
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameType: str
        :param Key: 智能结构化：key区域对应的内容
注意：此字段可能返回 null，表示取不到有效值。
        :type Key: str
        :param KeyId: 智能结构化：上述key的ID
注意：此字段可能返回 null，表示取不到有效值。
        :type KeyId: str
        :param Value: 识别：框区域的内容
智能结构化：value区域对应的内容
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: str
        :param KeyIdsForValue: 智能结构化：value区域所关联的key 区域的keyID的集合
注意：此字段可能返回 null，表示取不到有效值。
        :type KeyIdsForValue: list of str
        :param Direction: key或者value区域内容的方向：
DIRECTION_VERTICAL
DIRECTION_HORIZONTAL
注意：此字段可能返回 null，表示取不到有效值。
        :type Direction: str
        """
        self.Points = None
        self.FrameType = None
        self.Key = None
        self.KeyId = None
        self.Value = None
        self.KeyIdsForValue = None
        self.Direction = None


    def _deserialize(self, params):
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = PointInfo()
                obj._deserialize(item)
                self.Points.append(obj)
        self.FrameType = params.get("FrameType")
        self.Key = params.get("Key")
        self.KeyId = params.get("KeyId")
        self.Value = params.get("Value")
        self.KeyIdsForValue = params.get("KeyIdsForValue")
        self.Direction = params.get("Direction")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class OptimizationResult(AbstractModel):
    """自动学习模型优化报告

    """

    def __init__(self):
        r"""
        :param BaselineTime: 优化前时延
注意：此字段可能返回 null，表示取不到有效值。
        :type BaselineTime: str
        :param OptimizedTime: 优化后时延
注意：此字段可能返回 null，表示取不到有效值。
        :type OptimizedTime: str
        :param Speedup: 加速比
        :type Speedup: str
        """
        self.BaselineTime = None
        self.OptimizedTime = None
        self.Speedup = None


    def _deserialize(self, params):
        self.BaselineTime = params.get("BaselineTime")
        self.OptimizedTime = params.get("OptimizedTime")
        self.Speedup = params.get("Speedup")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Option(AbstractModel):
    """键值对

    """

    def __init__(self):
        r"""
        :param Name: 指标名
        :type Name: str
        :param Value: 指标值
        :type Value: int
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PRValue(AbstractModel):
    """评测指标pr曲线值

    """

    def __init__(self):
        r"""
        :param Precision: 精度信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Precision: list of float
        :param Recall: 召回率信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Recall: list of float
        :param Threshold: 阈值信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Threshold: list of float
        """
        self.Precision = None
        self.Recall = None
        self.Threshold = None


    def _deserialize(self, params):
        self.Precision = params.get("Precision")
        self.Recall = params.get("Recall")
        self.Threshold = params.get("Threshold")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PersonalLabel(AbstractModel):
    """用于创建标注任务时，表示个人标签信息

    """

    def __init__(self):
        r"""
        :param LabelName: label name
        :type LabelName: str
        :param Color: label color
        :type Color: str
        :param ID: label id
        :type ID: int
        :param CreateTime: 创建时间
        :type CreateTime: int
        :param UpdateTime: 更新时间
        :type UpdateTime: int
        """
        self.LabelName = None
        self.Color = None
        self.ID = None
        self.CreateTime = None
        self.UpdateTime = None


    def _deserialize(self, params):
        self.LabelName = params.get("LabelName")
        self.Color = params.get("Color")
        self.ID = params.get("ID")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Point(AbstractModel):
    """图像坐标点信息

    """

    def __init__(self):
        r"""
        :param X: x坐标值
        :type X: float
        :param Y: y坐标值
        :type Y: float
        """
        self.X = None
        self.Y = None


    def _deserialize(self, params):
        self.X = params.get("X")
        self.Y = params.get("Y")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PointInfo(AbstractModel):
    """点信息描述

    """

    def __init__(self):
        r"""
        :param X: X坐标值
注意：此字段可能返回 null，表示取不到有效值。
        :type X: float
        :param Y: Y坐标值
注意：此字段可能返回 null，表示取不到有效值。
        :type Y: float
        """
        self.X = None
        self.Y = None


    def _deserialize(self, params):
        self.X = params.get("X")
        self.Y = params.get("Y")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PredictConfig(AbstractModel):
    """推理标签信息

    """

    def __init__(self):
        r"""
        :param LabelName: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelName: str
        :param LabelId: 标签id
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelId: int
        :param IsCorrect: 推理结果是否正确
注意：此字段可能返回 null，表示取不到有效值。
        :type IsCorrect: bool
        :param Points: 标签在图像坐标点信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of Point
        :param Blocks: ocr块结果
注意：此字段可能返回 null，表示取不到有效值。
        :type Blocks: list of OcrBlock
        """
        self.LabelName = None
        self.LabelId = None
        self.IsCorrect = None
        self.Points = None
        self.Blocks = None


    def _deserialize(self, params):
        self.LabelName = params.get("LabelName")
        self.LabelId = params.get("LabelId")
        self.IsCorrect = params.get("IsCorrect")
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = Point()
                obj._deserialize(item)
                self.Points.append(obj)
        if params.get("Blocks") is not None:
            self.Blocks = []
            for item in params.get("Blocks"):
                obj = OcrBlock()
                obj._deserialize(item)
                self.Blocks.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PublishDatasetRequest(AbstractModel):
    """PublishDataset请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        """
        self.DatasetId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PublishDatasetResponse(AbstractModel):
    """PublishDataset返回参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 新的数据集ID
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetId: str
        :param DatasetVersion: 数据集版本号
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetVersion: str
        :param TaskId: 后台异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.DatasetId = None
        self.DatasetVersion = None
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        self.DatasetVersion = params.get("DatasetVersion")
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class PushTaskProcessRequest(AbstractModel):
    """PushTaskProcess请求参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 任务ID
        :type TaskId: str
        :param Total: 数量总计
        :type Total: int
        :param Finished: 已完成数量
        :type Finished: int
        :param Stage: 阶段。字节数不大于10字节
        :type Stage: str
        :param CurrentTime: 上报时间（单位为s)。如果为0，系统会填上收到的时间
        :type CurrentTime: int
        """
        self.TaskId = None
        self.Total = None
        self.Finished = None
        self.Stage = None
        self.CurrentTime = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.Total = params.get("Total")
        self.Finished = params.get("Finished")
        self.Stage = params.get("Stage")
        self.CurrentTime = params.get("CurrentTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PushTaskProcessResponse(AbstractModel):
    """PushTaskProcess返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class PushTrainingMetricsRequest(AbstractModel):
    """PushTrainingMetrics请求参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 指标数据
        :type Data: list of MetricData
        """
        self.Data = None


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self.Data = []
            for item in params.get("Data"):
                obj = MetricData()
                obj._deserialize(item)
                self.Data.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class PushTrainingMetricsResponse(AbstractModel):
    """PushTrainingMetrics返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewTencentLabWhitelistRequest(AbstractModel):
    """RenewTencentLabWhitelist请求参数结构体

    """

    def __init__(self):
        r"""
        :param ClassUin: 需要增加白名单的主uin
        :type ClassUin: str
        :param ClassSubUin: 需要增加白名单的subUin
        :type ClassSubUin: str
        :param ResourceId: Tione 平台维护的资源 ID，对应腾学会的课程 ID
        :type ResourceId: str
        :param ExtendDurationSecond: 续期时长，从过期时间向后续期 ExtendDurationSecond
        :type ExtendDurationSecond: int
        """
        self.ClassUin = None
        self.ClassSubUin = None
        self.ResourceId = None
        self.ExtendDurationSecond = None


    def _deserialize(self, params):
        self.ClassUin = params.get("ClassUin")
        self.ClassSubUin = params.get("ClassSubUin")
        self.ResourceId = params.get("ResourceId")
        self.ExtendDurationSecond = params.get("ExtendDurationSecond")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewTencentLabWhitelistResponse(AbstractModel):
    """RenewTencentLabWhitelist返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RenewTencentLabWhitelistTestRequest(AbstractModel):
    """RenewTencentLabWhitelistTest请求参数结构体

    """

    def __init__(self):
        r"""
        :param ClassUin: 需要增加白名单的主uin
        :type ClassUin: str
        :param ClassSubUin: 需要增加白名单的subUin
        :type ClassSubUin: str
        :param ResourceId: Tione 平台维护的资源 ID，对应腾学会的课程 ID
        :type ResourceId: str
        :param ExtendDurationSecond: 续期时长，从过期时间向后续期 ExtendDurationSecond
        :type ExtendDurationSecond: int
        """
        self.ClassUin = None
        self.ClassSubUin = None
        self.ResourceId = None
        self.ExtendDurationSecond = None


    def _deserialize(self, params):
        self.ClassUin = params.get("ClassUin")
        self.ClassSubUin = params.get("ClassSubUin")
        self.ResourceId = params.get("ResourceId")
        self.ExtendDurationSecond = params.get("ExtendDurationSecond")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RenewTencentLabWhitelistTestResponse(AbstractModel):
    """RenewTencentLabWhitelistTest返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class ResourceConf(AbstractModel):
    """Notebook资源参数

    """

    def __init__(self):
        r"""
        :param Cpu: cpu 处理器资源, 单位为1/1000核 (for预付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type Cpu: int
        :param Memory: memory 内存资源, 单位为1M (for预付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type Memory: int
        :param Gpu: gpu Gpu卡资源，单位为1单位的GpuType，例如GpuType=T4时，1 Gpu = 1/100 T4卡，GpuType=vcuda时，1 Gpu = 1/100 vcuda-core (for预付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type Gpu: int
        :param GpuType: GpuType 卡类型 vcuda, T4,P4,V100等 (for预付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuType: str
        :param InstanceType: 计算规格 (for后付费)，可选值如下：
TI.S.LARGE.POST: 4C8G 
TI.S.2XLARGE16.POST:  8C16G 
TI.S.2XLARGE32.POST:  8C32G 
TI.S.4XLARGE32.POST:  16C32G
TI.S.4XLARGE64.POST:  16C64G
TI.S.6XLARGE48.POST:  24C48G
TI.S.6XLARGE96.POST:  24C96G
TI.S.8XLARGE64.POST:  32C64G
TI.S.8XLARGE128.POST : 32C128G
TI.GN10.2XLARGE40.POST: 8C40G V100*1 
TI.GN10.5XLARGE80.POST:  18C80G V100*2 
TI.GN10.10XLARGE160.POST :  32C160G V100*4
TI.GN10.20XLARGE320.POST :  72C320G V100*8
TI.GN7.8XLARGE128.POST: 32C128G T4*1 
TI.GN7.10XLARGE160.POST: 40C160G T4*2 
TI.GN7.20XLARGE320.POST: 80C320G T4*4
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceType: str
        """
        self.Cpu = None
        self.Memory = None
        self.Gpu = None
        self.GpuType = None
        self.InstanceType = None


    def _deserialize(self, params):
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Gpu = params.get("Gpu")
        self.GpuType = params.get("GpuType")
        self.InstanceType = params.get("InstanceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResourceConfigInfo(AbstractModel):
    """资源配置

    """

    def __init__(self):
        r"""
        :param Role: 角色，eg：PS、WORKER、DRIVER、EXECUTOR
        :type Role: str
        :param Cpu: cpu核数，1000=1核
        :type Cpu: int
        :param Memory: 内存，单位为MB
        :type Memory: int
        :param GpuType: gpu卡类型
        :type GpuType: str
        :param Gpu: gpu数
        :type Gpu: int
        :param InstanceType: 算力规格ID
计算规格 (for后付费)，可选值如下：
TI.S.LARGE.POST: 4C8G 
TI.S.2XLARGE16.POST:  8C16G 
TI.S.2XLARGE32.POST:  8C32G 
TI.S.4XLARGE32.POST:  16C32G
TI.S.4XLARGE64.POST:  16C64G
TI.S.6XLARGE48.POST:  24C48G
TI.S.6XLARGE96.POST:  24C96G
TI.S.8XLARGE64.POST:  32C64G
TI.S.8XLARGE128.POST : 32C128G
TI.GN10.2XLARGE40.POST: 8C40G V100*1 
TI.GN10.5XLARGE80.POST:  18C80G V100*2 
TI.GN10.10XLARGE160.POST :  32C160G V100*4
TI.GN10.20XLARGE320.POST :  72C320G V100*8
TI.GN7.8XLARGE128.POST: 32C128G T4*1 
TI.GN7.10XLARGE160.POST: 40C160G T4*2 
TI.GN7.20XLARGE320.POST: 80C32
        :type InstanceType: str
        :param InstanceNum: 计算节点数
        :type InstanceNum: int
        :param InstanceTypeAlias: 算力规格名称
计算规格 (for后付费)，可选值如下：
4C8G 
8C16G 
8C32G 
16C32G
6C64G
24C48G
24C96G
32C64G
32C128G
8C40G V100*1 
8C80G V100*2 
32C160G V100*4
72C320G V100*8
32C128G T4*1 
40C160G T4*2 
80C32
        :type InstanceTypeAlias: str
        """
        self.Role = None
        self.Cpu = None
        self.Memory = None
        self.GpuType = None
        self.Gpu = None
        self.InstanceType = None
        self.InstanceNum = None
        self.InstanceTypeAlias = None


    def _deserialize(self, params):
        self.Role = params.get("Role")
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.GpuType = params.get("GpuType")
        self.Gpu = params.get("Gpu")
        self.InstanceType = params.get("InstanceType")
        self.InstanceNum = params.get("InstanceNum")
        self.InstanceTypeAlias = params.get("InstanceTypeAlias")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResourceGroup(AbstractModel):
    """资源组

    """

    def __init__(self):
        r"""
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        :param ResourceGroupName: 资源组名称
        :type ResourceGroupName: str
        :param FreeInstance: 可用节点个数(运行中的节点)
        :type FreeInstance: int
        :param TotalInstance: 总节点个数(所有节点)
        :type TotalInstance: int
        :param UsedResource: 资资源组已用的资源
注意：此字段可能返回 null，表示取不到有效值。
        :type UsedResource: :class:`tencentcloud.tione.v20211111.models.GroupResource`
        :param TotalResource: 资源组总资源
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalResource: :class:`tencentcloud.tione.v20211111.models.GroupResource`
        :param InstanceSet: 节点信息
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceSet: list of Instance
        :param TagSet: 标签列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TagSet: list of Tag
        """
        self.ResourceGroupId = None
        self.ResourceGroupName = None
        self.FreeInstance = None
        self.TotalInstance = None
        self.UsedResource = None
        self.TotalResource = None
        self.InstanceSet = None
        self.TagSet = None


    def _deserialize(self, params):
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.ResourceGroupName = params.get("ResourceGroupName")
        self.FreeInstance = params.get("FreeInstance")
        self.TotalInstance = params.get("TotalInstance")
        if params.get("UsedResource") is not None:
            self.UsedResource = GroupResource()
            self.UsedResource._deserialize(params.get("UsedResource"))
        if params.get("TotalResource") is not None:
            self.TotalResource = GroupResource()
            self.TotalResource._deserialize(params.get("TotalResource"))
        if params.get("InstanceSet") is not None:
            self.InstanceSet = []
            for item in params.get("InstanceSet"):
                obj = Instance()
                obj._deserialize(item)
                self.InstanceSet.append(obj)
        if params.get("TagSet") is not None:
            self.TagSet = []
            for item in params.get("TagSet"):
                obj = Tag()
                obj._deserialize(item)
                self.TagSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ResourceInfo(AbstractModel):
    """描述资源信息

    """

    def __init__(self):
        r"""
        :param Cpu: 处理器资源, 单位为1/1000核
注意：此字段可能返回 null，表示取不到有效值。
        :type Cpu: int
        :param Memory: 内存资源, 单位为1M
注意：此字段可能返回 null，表示取不到有效值。
        :type Memory: int
        :param Gpu: Gpu卡个数资源, 单位为0.01单位的GpuType.
Gpu=100表示使用了“一张”gpu卡, 但此处的“一张”卡有可能是虚拟化后的1/4卡, 也有可能是整张卡. 取决于实例的机型
例1 实例的机型带有1张虚拟gpu卡, 每张虚拟gpu卡对应1/4张实际T4卡, 则此时 GpuType=T4, Gpu=100, RealGpu=25.
例2 实例的机型带有4张gpu整卡, 每张卡对应1张实际T4卡, 则 此时 GpuType=T4, Gpu=400, RealGpu=400.
注意：此字段可能返回 null，表示取不到有效值。
        :type Gpu: int
        :param GpuType: Gpu卡型号 T4或者V100。仅展示当前 GPU 卡型号，若存在多类型同时使用，则参考 RealGpuDetailSet 的值。
注意：此字段可能返回 null，表示取不到有效值。
        :type GpuType: str
        :param RealGpu: 创建或更新时无需填写，仅展示需要关注
后付费非整卡实例对应的实际的Gpu卡资源, 表示gpu资源对应实际的gpu卡个数.
RealGpu=100表示实际使用了一张gpu卡, 对应实际的实例机型, 有可能代表带有1/4卡的实例4个, 或者带有1/2卡的实例2个, 或者带有1卡的实力1个.
注意：此字段可能返回 null，表示取不到有效值。
        :type RealGpu: int
        :param RealGpuDetailSet: 创建或更新时无需填写，仅展示需要关注。详细的GPU使用信息。
注意：此字段可能返回 null，表示取不到有效值。
        :type RealGpuDetailSet: list of GpuDetail
        """
        self.Cpu = None
        self.Memory = None
        self.Gpu = None
        self.GpuType = None
        self.RealGpu = None
        self.RealGpuDetailSet = None


    def _deserialize(self, params):
        self.Cpu = params.get("Cpu")
        self.Memory = params.get("Memory")
        self.Gpu = params.get("Gpu")
        self.GpuType = params.get("GpuType")
        self.RealGpu = params.get("RealGpu")
        if params.get("RealGpuDetailSet") is not None:
            self.RealGpuDetailSet = []
            for item in params.get("RealGpuDetailSet"):
                obj = GpuDetail()
                obj._deserialize(item)
                self.RealGpuDetailSet.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartAutoMLModelAccelerateTaskRequest(AbstractModel):
    """RestartAutoMLModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        """
        self.AutoMLTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartAutoMLModelAccelerateTaskResponse(AbstractModel):
    """RestartAutoMLModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.RequestId = params.get("RequestId")


class RestartModelAccelerateTaskRequest(AbstractModel):
    """RestartModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        :param ModelSource: 模型来源（JOB/COS）
        :type ModelSource: str
        :param ModelOutputPath: 模型输出cos路径
        :type ModelOutputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelAccTaskName: 模型加速任务名称
        :type ModelAccTaskName: str
        :param AlgorithmFramework: 算法框架（废弃）
        :type AlgorithmFramework: str
        :param ModelId: 模型ID
        :type ModelId: str
        :param ModelName: 模型名称
        :type ModelName: str
        :param ModelVersion: 模型版本
        :type ModelVersion: str
        :param ModelInputPath: 模型输入cos路径
        :type ModelInputPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param OptimizationLevel: 优化级别（NO_LOSS/FP16/INT8），默认FP16
        :type OptimizationLevel: str
        :param ModelInputNum: input节点个数（废弃）
        :type ModelInputNum: int
        :param ModelInputInfos: input节点信息（废弃）
        :type ModelInputInfos: list of ModelInputInfo
        :param ModelFormat: 模型格式 （TORCH_SCRIPT/DETECTRON2/SAVED_MODEL/FROZEN_GRAPH/MMDETECTION/ONNX/HUGGING_FACE）
        :type ModelFormat: str
        :param TensorInfos: 模型Tensor信息
        :type TensorInfos: list of str
        :param GPUType: GPU类型（T4/V100/A10），默认T4
        :type GPUType: str
        :param HyperParameter: 模型专业参数
        :type HyperParameter: :class:`tencentcloud.tione.v20211111.models.HyperParameter`
        :param AccEngineVersion: 加速引擎版本
        :type AccEngineVersion: str
        :param Tags: 标签
        :type Tags: list of Tag
        :param ModelSignature: SavedModel保存时配置的签名
        :type ModelSignature: str
        """
        self.ModelAccTaskId = None
        self.ModelSource = None
        self.ModelOutputPath = None
        self.ModelAccTaskName = None
        self.AlgorithmFramework = None
        self.ModelId = None
        self.ModelName = None
        self.ModelVersion = None
        self.ModelInputPath = None
        self.OptimizationLevel = None
        self.ModelInputNum = None
        self.ModelInputInfos = None
        self.ModelFormat = None
        self.TensorInfos = None
        self.GPUType = None
        self.HyperParameter = None
        self.AccEngineVersion = None
        self.Tags = None
        self.ModelSignature = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        self.ModelSource = params.get("ModelSource")
        if params.get("ModelOutputPath") is not None:
            self.ModelOutputPath = CosPathInfo()
            self.ModelOutputPath._deserialize(params.get("ModelOutputPath"))
        self.ModelAccTaskName = params.get("ModelAccTaskName")
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.ModelId = params.get("ModelId")
        self.ModelName = params.get("ModelName")
        self.ModelVersion = params.get("ModelVersion")
        if params.get("ModelInputPath") is not None:
            self.ModelInputPath = CosPathInfo()
            self.ModelInputPath._deserialize(params.get("ModelInputPath"))
        self.OptimizationLevel = params.get("OptimizationLevel")
        self.ModelInputNum = params.get("ModelInputNum")
        if params.get("ModelInputInfos") is not None:
            self.ModelInputInfos = []
            for item in params.get("ModelInputInfos"):
                obj = ModelInputInfo()
                obj._deserialize(item)
                self.ModelInputInfos.append(obj)
        self.ModelFormat = params.get("ModelFormat")
        self.TensorInfos = params.get("TensorInfos")
        self.GPUType = params.get("GPUType")
        if params.get("HyperParameter") is not None:
            self.HyperParameter = HyperParameter()
            self.HyperParameter._deserialize(params.get("HyperParameter"))
        self.AccEngineVersion = params.get("AccEngineVersion")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.ModelSignature = params.get("ModelSignature")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RestartModelAccelerateTaskResponse(AbstractModel):
    """RestartModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class RowItem(AbstractModel):
    """文本行信息

    """

    def __init__(self):
        r"""
        :param Values: rowValue 数组
注意：此字段可能返回 null，表示取不到有效值。
        :type Values: list of RowValue
        """
        self.Values = None


    def _deserialize(self, params):
        if params.get("Values") is not None:
            self.Values = []
            for item in params.get("Values"):
                obj = RowValue()
                obj._deserialize(item)
                self.Values.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class RowValue(AbstractModel):
    """文件行信息

    """

    def __init__(self):
        r"""
        :param Name: 列名
        :type Name: str
        :param Value: 列值
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: str
        """
        self.Name = None
        self.Value = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Scene(AbstractModel):
    """自动学习场景信息

    """

    def __init__(self):
        r"""
        :param Id: 场景id
注意：此字段可能返回 null，表示取不到有效值。
        :type Id: str
        :param Name: 场景名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Name: str
        :param Describe: 场景描述信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Describe: str
        :param Type: 场景类别
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param SceneDomain: 场景所属领域
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneDomain: str
        :param BackgroundUrl: 场景背景图下
注意：此字段可能返回 null，表示取不到有效值。
        :type BackgroundUrl: str
        :param ModelConfig: 模型配置信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelConfig: str
        :param DatasetConfig: 数据集配置信息
注意：此字段可能返回 null，表示取不到有效值。
        :type DatasetConfig: :class:`tencentcloud.tione.v20211111.models.DatasetConfigs`
        :param AnnotationType: 标签类别
注意：此字段可能返回 null，表示取不到有效值。
        :type AnnotationType: str
        """
        self.Id = None
        self.Name = None
        self.Describe = None
        self.Type = None
        self.SceneDomain = None
        self.BackgroundUrl = None
        self.ModelConfig = None
        self.DatasetConfig = None
        self.AnnotationType = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Describe = params.get("Describe")
        self.Type = params.get("Type")
        self.SceneDomain = params.get("SceneDomain")
        self.BackgroundUrl = params.get("BackgroundUrl")
        self.ModelConfig = params.get("ModelConfig")
        if params.get("DatasetConfig") is not None:
            self.DatasetConfig = DatasetConfigs()
            self.DatasetConfig._deserialize(params.get("DatasetConfig"))
        self.AnnotationType = params.get("AnnotationType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ScheduledAction(AbstractModel):
    """定时的事务和行为

    """

    def __init__(self):
        r"""
        :param ScheduleStop: 是否要定时停止服务，true or false。true 则 ScheduleStopTime 必填， false 则 ScheduleStopTime 不生效
        :type ScheduleStop: bool
        :param ScheduleStopTime: 要执行定时停止的时间，格式：“2022-10-13T19:46:22Z”
        :type ScheduleStopTime: str
        """
        self.ScheduleStop = None
        self.ScheduleStopTime = None


    def _deserialize(self, params):
        self.ScheduleStop = params.get("ScheduleStop")
        self.ScheduleStopTime = params.get("ScheduleStopTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SchemaInfo(AbstractModel):
    """表格数据集表头信息

    """

    def __init__(self):
        r"""
        :param Name: 长度30字符内
        :type Name: str
        :param Type: 数据类型
        :type Type: str
        """
        self.Name = None
        self.Type = None


    def _deserialize(self, params):
        self.Name = params.get("Name")
        self.Type = params.get("Type")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SegmentationInfo(AbstractModel):
    """图片分割参数信息

    """

    def __init__(self):
        r"""
        :param Points: 点坐标数组
注意：此字段可能返回 null，表示取不到有效值。
        :type Points: list of PointInfo
        :param Label: 分割标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Label: str
        :param Gray: 灰度值
注意：此字段可能返回 null，表示取不到有效值。
        :type Gray: int
        :param Color: 颜色
注意：此字段可能返回 null，表示取不到有效值。
        :type Color: str
        """
        self.Points = None
        self.Label = None
        self.Gray = None
        self.Color = None


    def _deserialize(self, params):
        if params.get("Points") is not None:
            self.Points = []
            for item in params.get("Points"):
                obj = PointInfo()
                obj._deserialize(item)
                self.Points.append(obj)
        self.Label = params.get("Label")
        self.Gray = params.get("Gray")
        self.Color = params.get("Color")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class Service(AbstractModel):
    """描述在线服务

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 服务组id
        :type ServiceGroupId: str
        :param ServiceId: 服务id
        :type ServiceId: str
        :param ServiceGroupName: 服务组名
        :type ServiceGroupName: str
        :param ServiceDescription: 服务描述
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceDescription: str
        :param ClusterId: 集群id
注意：此字段可能返回 null，表示取不到有效值。
        :type ClusterId: str
        :param Region: 地域
注意：此字段可能返回 null，表示取不到有效值。
        :type Region: str
        :param Namespace: 命名空间
注意：此字段可能返回 null，表示取不到有效值。
        :type Namespace: str
        :param ChargeType: 付费类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param ResourceGroupId: 后付费资源组id
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param CreatedBy: 创建者
注意：此字段可能返回 null，表示取不到有效值。
        :type CreatedBy: str
        :param CreateTime: 创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param Uin: 主账号
注意：此字段可能返回 null，表示取不到有效值。
        :type Uin: str
        :param SubUin: 子账号
注意：此字段可能返回 null，表示取不到有效值。
        :type SubUin: str
        :param AppId: app_id
注意：此字段可能返回 null，表示取不到有效值。
        :type AppId: int
        :param Version: 版本号
注意：此字段可能返回 null，表示取不到有效值。
        :type Version: str
        :param LatestVersion: 服务组下服务的最高版本号
注意：此字段可能返回 null，表示取不到有效值。
        :type LatestVersion: str
        :param ServiceInfo: 服务的详细信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceInfo: :class:`tencentcloud.tione.v20211111.models.ServiceInfo`
        :param BusinessStatus: 服务的业务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type BusinessStatus: str
        :param CreateSource: 服务的创建来源 AUTO_ML,DEFAULT
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateSource: str
        :param BillingInfo: 费用信息
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfo: str
        :param Status: 服务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param Weight: 模型权重
注意：此字段可能返回 null，表示取不到有效值。
        :type Weight: int
        :param IngressName: 服务所在的 ingress 的 name
注意：此字段可能返回 null，表示取不到有效值。
        :type IngressName: str
        :param ServiceLimit: 服务限速限流相关配置
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceLimit: :class:`tencentcloud.tione.v20211111.models.ServiceLimit`
        :param ScheduledAction: 定时停止的配置
注意：此字段可能返回 null，表示取不到有效值。
        :type ScheduledAction: :class:`tencentcloud.tione.v20211111.models.ScheduledAction`
        """
        self.ServiceGroupId = None
        self.ServiceId = None
        self.ServiceGroupName = None
        self.ServiceDescription = None
        self.ClusterId = None
        self.Region = None
        self.Namespace = None
        self.ChargeType = None
        self.ResourceGroupId = None
        self.CreatedBy = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Uin = None
        self.SubUin = None
        self.AppId = None
        self.Version = None
        self.LatestVersion = None
        self.ServiceInfo = None
        self.BusinessStatus = None
        self.CreateSource = None
        self.BillingInfo = None
        self.Status = None
        self.Weight = None
        self.IngressName = None
        self.ServiceLimit = None
        self.ScheduledAction = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        self.ServiceId = params.get("ServiceId")
        self.ServiceGroupName = params.get("ServiceGroupName")
        self.ServiceDescription = params.get("ServiceDescription")
        self.ClusterId = params.get("ClusterId")
        self.Region = params.get("Region")
        self.Namespace = params.get("Namespace")
        self.ChargeType = params.get("ChargeType")
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.CreatedBy = params.get("CreatedBy")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Uin = params.get("Uin")
        self.SubUin = params.get("SubUin")
        self.AppId = params.get("AppId")
        self.Version = params.get("Version")
        self.LatestVersion = params.get("LatestVersion")
        if params.get("ServiceInfo") is not None:
            self.ServiceInfo = ServiceInfo()
            self.ServiceInfo._deserialize(params.get("ServiceInfo"))
        self.BusinessStatus = params.get("BusinessStatus")
        self.CreateSource = params.get("CreateSource")
        self.BillingInfo = params.get("BillingInfo")
        self.Status = params.get("Status")
        self.Weight = params.get("Weight")
        self.IngressName = params.get("IngressName")
        if params.get("ServiceLimit") is not None:
            self.ServiceLimit = ServiceLimit()
            self.ServiceLimit._deserialize(params.get("ServiceLimit"))
        if params.get("ScheduledAction") is not None:
            self.ScheduledAction = ScheduledAction()
            self.ScheduledAction._deserialize(params.get("ScheduledAction"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceCallInfo(AbstractModel):
    """服务的调用信息，服务组下唯一

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 服务组id
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceGroupId: str
        :param InnerHttpAddr: 内网http调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type InnerHttpAddr: str
        :param InnerHttpsAddr: 内网https调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type InnerHttpsAddr: str
        :param OuterHttpAddr: 内网http调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type OuterHttpAddr: str
        :param OuterHttpsAddr: 内网https调用地址
注意：此字段可能返回 null，表示取不到有效值。
        :type OuterHttpsAddr: str
        :param AppKey: 调用key
注意：此字段可能返回 null，表示取不到有效值。
        :type AppKey: str
        :param AppSecret: 调用secret
注意：此字段可能返回 null，表示取不到有效值。
        :type AppSecret: str
        """
        self.ServiceGroupId = None
        self.InnerHttpAddr = None
        self.InnerHttpsAddr = None
        self.OuterHttpAddr = None
        self.OuterHttpsAddr = None
        self.AppKey = None
        self.AppSecret = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        self.InnerHttpAddr = params.get("InnerHttpAddr")
        self.InnerHttpsAddr = params.get("InnerHttpsAddr")
        self.OuterHttpAddr = params.get("OuterHttpAddr")
        self.OuterHttpsAddr = params.get("OuterHttpsAddr")
        self.AppKey = params.get("AppKey")
        self.AppSecret = params.get("AppSecret")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceGroup(AbstractModel):
    """在线服务一个服务组的信息

    """

    def __init__(self):
        r"""
        :param ServiceGroupId: 服务组id
        :type ServiceGroupId: str
        :param ServiceGroupName: 服务组名
        :type ServiceGroupName: str
        :param CreatedBy: 创建者
        :type CreatedBy: str
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param Uin: 主账号
        :type Uin: str
        :param ServiceCount: 服务组下服务总数
注意：此字段可能返回 null，表示取不到有效值。
        :type ServiceCount: int
        :param RunningServiceCount: 服务组下在运行的服务数量
注意：此字段可能返回 null，表示取不到有效值。
        :type RunningServiceCount: int
        :param Services: 服务描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Services: list of Service
        :param Status: 服务组状态，与服务一致
 CREATING 创建中
     CREATE_FAILED 创建失败
     Normal	正常运行中
     Stopped  已停止
     Stopping 停止中
     Abnormal 异常
     Pending 启动中
     Waiting 就绪中
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param Tags: 服务组标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param LatestVersion: 服务组下最高版本
注意：此字段可能返回 null，表示取不到有效值。
        :type LatestVersion: str
        :param BusinessStatus: 服务的业务状态
CREATING 创建中
     CREATE_FAILED 创建失败
     ARREARS_STOP 因欠费被强制停止
     BILLING 计费中
     WHITELIST_USING 白名单试用中
     WHITELIST_STOP 白名单额度不足
注意：此字段可能返回 null，表示取不到有效值。
        :type BusinessStatus: str
        :param BillingInfo: 服务的计费信息
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfo: str
        :param CreateSource: 服务的创建来源
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateSource: str
        :param WeightUpdateStatus: 服务组的权重更新状态 
UPDATING 更新中
     UPDATED 更新成功
     UPDATE_FAILED 更新失败
注意：此字段可能返回 null，表示取不到有效值。
        :type WeightUpdateStatus: str
        """
        self.ServiceGroupId = None
        self.ServiceGroupName = None
        self.CreatedBy = None
        self.CreateTime = None
        self.UpdateTime = None
        self.Uin = None
        self.ServiceCount = None
        self.RunningServiceCount = None
        self.Services = None
        self.Status = None
        self.Tags = None
        self.LatestVersion = None
        self.BusinessStatus = None
        self.BillingInfo = None
        self.CreateSource = None
        self.WeightUpdateStatus = None


    def _deserialize(self, params):
        self.ServiceGroupId = params.get("ServiceGroupId")
        self.ServiceGroupName = params.get("ServiceGroupName")
        self.CreatedBy = params.get("CreatedBy")
        self.CreateTime = params.get("CreateTime")
        self.UpdateTime = params.get("UpdateTime")
        self.Uin = params.get("Uin")
        self.ServiceCount = params.get("ServiceCount")
        self.RunningServiceCount = params.get("RunningServiceCount")
        if params.get("Services") is not None:
            self.Services = []
            for item in params.get("Services"):
                obj = Service()
                obj._deserialize(item)
                self.Services.append(obj)
        self.Status = params.get("Status")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.LatestVersion = params.get("LatestVersion")
        self.BusinessStatus = params.get("BusinessStatus")
        self.BillingInfo = params.get("BillingInfo")
        self.CreateSource = params.get("CreateSource")
        self.WeightUpdateStatus = params.get("WeightUpdateStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceHistory(AbstractModel):
    """服务历史版本

    """

    def __init__(self):
        r"""
        :param Revision: 版本
注意：此字段可能返回 null，表示取不到有效值。
        :type Revision: str
        :param UpdateTime: 更新时间
注意：此字段可能返回 null，表示取不到有效值。
        :type UpdateTime: str
        :param Image: 镜像
注意：此字段可能返回 null，表示取不到有效值。
        :type Image: str
        :param ModelFile: 模型文件
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelFile: str
        :param RawData: 原始数据
注意：此字段可能返回 null，表示取不到有效值。
        :type RawData: str
        """
        self.Revision = None
        self.UpdateTime = None
        self.Image = None
        self.ModelFile = None
        self.RawData = None


    def _deserialize(self, params):
        self.Revision = params.get("Revision")
        self.UpdateTime = params.get("UpdateTime")
        self.Image = params.get("Image")
        self.ModelFile = params.get("ModelFile")
        self.RawData = params.get("RawData")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceInfo(AbstractModel):
    """推理服务在集群中的信息

    """

    def __init__(self):
        r"""
        :param Replicas: 期望运行的Pod数量，停止状态是0
不同计费模式和调节模式下对应关系如下
PREPAID 和 POSTPAID_BY_HOUR:
手动调节模式下对应 实例数量
自动调节模式下对应 基于时间的默认策略的实例数量
HYBRID_PAID:
后付费实例手动调节模式下对应 实例数量
后付费实例自动调节模式下对应 时间策略的默认策略的实例数量
注意：此字段可能返回 null，表示取不到有效值。
        :type Replicas: int
        :param ImageInfo: 镜像信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param Env: 环境变量
注意：此字段可能返回 null，表示取不到有效值。
        :type Env: list of EnvVar
        :param Resources: 资源信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Resources: :class:`tencentcloud.tione.v20211111.models.ResourceInfo`
        :param InstanceType: 后付费实例对应的机型规格
注意：此字段可能返回 null，表示取不到有效值。
        :type InstanceType: str
        :param ModelInfo: 模型信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelInfo: :class:`tencentcloud.tione.v20211111.models.ModelInfo`
        :param LogEnable: 是否启用日志
注意：此字段可能返回 null，表示取不到有效值。
        :type LogEnable: bool
        :param LogConfig: 日志配置
注意：此字段可能返回 null，表示取不到有效值。
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param AuthorizationEnable: 是否开启鉴权
注意：此字段可能返回 null，表示取不到有效值。
        :type AuthorizationEnable: bool
        :param HorizontalPodAutoscaler: hpa配置
注意：此字段可能返回 null，表示取不到有效值。
        :type HorizontalPodAutoscaler: :class:`tencentcloud.tione.v20211111.models.HorizontalPodAutoscaler`
        :param Status: 服务的状态描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: :class:`tencentcloud.tione.v20211111.models.WorkloadStatus`
        :param Weight: 权重
注意：此字段可能返回 null，表示取不到有效值。
        :type Weight: int
        :param PodList: 实例列表
注意：此字段可能返回 null，表示取不到有效值。
        :type PodList: list of str
        :param ResourceTotal: 资源总量
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceTotal: :class:`tencentcloud.tione.v20211111.models.ResourceInfo`
        :param OldReplicas: 历史实例数
注意：此字段可能返回 null，表示取不到有效值。
        :type OldReplicas: int
        :param HybridBillingPrepaidReplicas: 计费模式[HYBRID_PAID]时生效, 用于标识混合计费模式下的预付费实例数, 若不填则默认为1
注意：此字段可能返回 null，表示取不到有效值。
        :type HybridBillingPrepaidReplicas: int
        :param OldHybridBillingPrepaidReplicas: 历史 HYBRID_PAID 时的实例数，用户恢复服务
注意：此字段可能返回 null，表示取不到有效值。
        :type OldHybridBillingPrepaidReplicas: int
        :param ModelHotUpdateEnable: 是否开启模型的热更新。默认不开启
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelHotUpdateEnable: bool
        """
        self.Replicas = None
        self.ImageInfo = None
        self.Env = None
        self.Resources = None
        self.InstanceType = None
        self.ModelInfo = None
        self.LogEnable = None
        self.LogConfig = None
        self.AuthorizationEnable = None
        self.HorizontalPodAutoscaler = None
        self.Status = None
        self.Weight = None
        self.PodList = None
        self.ResourceTotal = None
        self.OldReplicas = None
        self.HybridBillingPrepaidReplicas = None
        self.OldHybridBillingPrepaidReplicas = None
        self.ModelHotUpdateEnable = None


    def _deserialize(self, params):
        self.Replicas = params.get("Replicas")
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        if params.get("Env") is not None:
            self.Env = []
            for item in params.get("Env"):
                obj = EnvVar()
                obj._deserialize(item)
                self.Env.append(obj)
        if params.get("Resources") is not None:
            self.Resources = ResourceInfo()
            self.Resources._deserialize(params.get("Resources"))
        self.InstanceType = params.get("InstanceType")
        if params.get("ModelInfo") is not None:
            self.ModelInfo = ModelInfo()
            self.ModelInfo._deserialize(params.get("ModelInfo"))
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.AuthorizationEnable = params.get("AuthorizationEnable")
        if params.get("HorizontalPodAutoscaler") is not None:
            self.HorizontalPodAutoscaler = HorizontalPodAutoscaler()
            self.HorizontalPodAutoscaler._deserialize(params.get("HorizontalPodAutoscaler"))
        if params.get("Status") is not None:
            self.Status = WorkloadStatus()
            self.Status._deserialize(params.get("Status"))
        self.Weight = params.get("Weight")
        self.PodList = params.get("PodList")
        if params.get("ResourceTotal") is not None:
            self.ResourceTotal = ResourceInfo()
            self.ResourceTotal._deserialize(params.get("ResourceTotal"))
        self.OldReplicas = params.get("OldReplicas")
        self.HybridBillingPrepaidReplicas = params.get("HybridBillingPrepaidReplicas")
        self.OldHybridBillingPrepaidReplicas = params.get("OldHybridBillingPrepaidReplicas")
        self.ModelHotUpdateEnable = params.get("ModelHotUpdateEnable")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ServiceLimit(AbstractModel):
    """服务的限流限速等配置

    """

    def __init__(self):
        r"""
        :param EnableInstanceRpsLimit: 是否开启实例层面限流限速，true or false。true 则 InstanceRpsLimit 必填， false 则 InstanceRpsLimit 不生效
        :type EnableInstanceRpsLimit: bool
        :param InstanceRpsLimit: 每个服务实例的 request per second 限速, 0 为不限流
        :type InstanceRpsLimit: int
        """
        self.EnableInstanceRpsLimit = None
        self.InstanceRpsLimit = None


    def _deserialize(self, params):
        self.EnableInstanceRpsLimit = params.get("EnableInstanceRpsLimit")
        self.InstanceRpsLimit = params.get("InstanceRpsLimit")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetRenewBillingResourceFlagRequest(AbstractModel):
    """SetRenewBillingResourceFlag请求参数结构体

    """

    def __init__(self):
        r"""
        :param ResourceIds: 资源组节点id列表
注意: 单次最多100个
        :type ResourceIds: list of str
        :param AutoRenewFlag: 自动续费标识
注意：此字段为枚举值
说明：
NOTIFY_AND_MANUAL_RENEW：手动续费(取消自动续费)且到期通知
NOTIFY_AND_AUTO_RENEW：自动续费且到期通知
DISABLE_NOTIFY_AND_MANUAL_RENEW：手动续费(取消自动续费)且到期不通知
        :type AutoRenewFlag: str
        :param ResourceGroupId: 资源组id
        :type ResourceGroupId: str
        """
        self.ResourceIds = None
        self.AutoRenewFlag = None
        self.ResourceGroupId = None


    def _deserialize(self, params):
        self.ResourceIds = params.get("ResourceIds")
        self.AutoRenewFlag = params.get("AutoRenewFlag")
        self.ResourceGroupId = params.get("ResourceGroupId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SetRenewBillingResourceFlagResponse(AbstractModel):
    """SetRenewBillingResourceFlag返回参数结构体

    """

    def __init__(self):
        r"""
        :param FailResources: 失败节点及失败详情
注意：此字段可能返回 null，表示取不到有效值。
        :type FailResources: list of FailResource
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.FailResources = None
        self.RequestId = None


    def _deserialize(self, params):
        if params.get("FailResources") is not None:
            self.FailResources = []
            for item in params.get("FailResources"):
                obj = FailResource()
                obj._deserialize(item)
                self.FailResources.append(obj)
        self.RequestId = params.get("RequestId")


class Spec(AbstractModel):
    """计费项内容

    """

    def __init__(self):
        r"""
        :param SpecId: 计费项标签
        :type SpecId: str
        :param SpecName: 计费项名称
        :type SpecName: str
        :param SpecAlias: 计费项显示名称
        :type SpecAlias: str
        :param Available: 是否售罄
        :type Available: bool
        :param AvailableRegion: 当前资源售罄时，可用的区域有哪些
        :type AvailableRegion: list of str
        """
        self.SpecId = None
        self.SpecName = None
        self.SpecAlias = None
        self.Available = None
        self.AvailableRegion = None


    def _deserialize(self, params):
        self.SpecId = params.get("SpecId")
        self.SpecName = params.get("SpecName")
        self.SpecAlias = params.get("SpecAlias")
        self.Available = params.get("Available")
        self.AvailableRegion = params.get("AvailableRegion")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpecPrice(AbstractModel):
    """计费项询价结果

    """

    def __init__(self):
        r"""
        :param SpecName: 计费项名称
        :type SpecName: str
        :param TotalCost: 原价，单位：分。最大值42亿，超过则返回0
        :type TotalCost: int
        :param RealTotalCost: 优惠后的价格，单位：分
        :type RealTotalCost: int
        """
        self.SpecName = None
        self.TotalCost = None
        self.RealTotalCost = None


    def _deserialize(self, params):
        self.SpecName = params.get("SpecName")
        self.TotalCost = params.get("TotalCost")
        self.RealTotalCost = params.get("RealTotalCost")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SpecUnit(AbstractModel):
    """计费项询价单元

    """

    def __init__(self):
        r"""
        :param SpecName: 计费项名称
        :type SpecName: str
        :param SpecCount: 计费项数量,建议不超过100万
        :type SpecCount: int
        """
        self.SpecName = None
        self.SpecCount = None


    def _deserialize(self, params):
        self.SpecName = params.get("SpecName")
        self.SpecCount = params.get("SpecCount")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartAutoMLEvaluationTaskRequest(AbstractModel):
    """StartAutoMLEvaluationTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 待启动评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param TestDatasetIds: 评测数据集列表
        :type TestDatasetIds: list of str
        :param TestDatasetLabels: 评测标签列表
        :type TestDatasetLabels: list of str
        """
        self.AutoMLTaskId = None
        self.TestDatasetIds = None
        self.TestDatasetLabels = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TestDatasetIds = params.get("TestDatasetIds")
        self.TestDatasetLabels = params.get("TestDatasetLabels")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartAutoMLEvaluationTaskResponse(AbstractModel):
    """StartAutoMLEvaluationTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 启动的评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param AsyncTaskId: 异步任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class StartAutoMLTaskTrainRequest(AbstractModel):
    """StartAutoMLTaskTrain请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartAutoMLTaskTrainResponse(AbstractModel):
    """StartAutoMLTaskTrain返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param TrainTaskStatus: 训练任务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskStatus: str
        :param AsyncTaskId: 异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.TrainTaskStatus = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.TrainTaskStatus = params.get("TrainTaskStatus")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class StartCmdInfo(AbstractModel):
    """启动命令信息

    """

    def __init__(self):
        r"""
        :param StartCmd: 启动命令
        :type StartCmd: str
        :param PsStartCmd: ps启动命令
        :type PsStartCmd: str
        :param WorkerStartCmd: worker启动命令
        :type WorkerStartCmd: str
        """
        self.StartCmd = None
        self.PsStartCmd = None
        self.WorkerStartCmd = None


    def _deserialize(self, params):
        self.StartCmd = params.get("StartCmd")
        self.PsStartCmd = params.get("PsStartCmd")
        self.WorkerStartCmd = params.get("WorkerStartCmd")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartNotebookRequest(AbstractModel):
    """StartNotebook请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook id
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartNotebookResponse(AbstractModel):
    """StartNotebook返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StartTrainingTaskRequest(AbstractModel):
    """StartTrainingTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StartTrainingTaskResponse(AbstractModel):
    """StartTrainingTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StatefulSetCondition(AbstractModel):
    """实例状况

    """

    def __init__(self):
        r"""
        :param Message: 信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param Reason: 原因
注意：此字段可能返回 null，表示取不到有效值。
        :type Reason: str
        :param Status: Status of the condition, one of True, False, Unknown.
注意：此字段可能返回 null，表示取不到有效值。
        :type Status: str
        :param Type: 类型
注意：此字段可能返回 null，表示取不到有效值。
        :type Type: str
        :param LastTransitionTime: 上次更新的时间
注意：此字段可能返回 null，表示取不到有效值。
        :type LastTransitionTime: str
        """
        self.Message = None
        self.Reason = None
        self.Status = None
        self.Type = None
        self.LastTransitionTime = None


    def _deserialize(self, params):
        self.Message = params.get("Message")
        self.Reason = params.get("Reason")
        self.Status = params.get("Status")
        self.Type = params.get("Type")
        self.LastTransitionTime = params.get("LastTransitionTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopAutoMLEMSTaskRequest(AbstractModel):
    """StopAutoMLEMSTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务创建任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
        :type EMSTaskId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopAutoMLEMSTaskResponse(AbstractModel):
    """StopAutoMLEMSTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 发布模型服务创建任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EMSTaskId: 发布模型服务任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskId: str
        :param EMSTaskStatus: 模型服务状态
注意：此字段可能返回 null，表示取不到有效值。
        :type EMSTaskStatus: str
        :param AsyncTaskId: 异步任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EMSTaskId = None
        self.EMSTaskStatus = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EMSTaskId = params.get("EMSTaskId")
        self.EMSTaskStatus = params.get("EMSTaskStatus")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class StopAutoMLEvaluationTaskRequest(AbstractModel):
    """StopAutoMLEvaluationTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 待停止评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 待停止评测任务id
        :type EvaluationTaskId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopAutoMLEvaluationTaskResponse(AbstractModel):
    """StopAutoMLEvaluationTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 停止评测任务所属自动学习任务id
        :type AutoMLTaskId: str
        :param EvaluationTaskId: 停止评测任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskId: str
        :param EvaluationTaskStatus: 评测任务当前状态，状态类型NOTSTART(未创建评测任务), WAITING(排队中),INIT(初始化中), STARTING(启动中), RUNNING(运行中), FAILED(异常), STOPPING(停止中), STOPPED(已停止), SUCCEED(已完成)
注意：此字段可能返回 null，表示取不到有效值。
        :type EvaluationTaskStatus: str
        :param AsyncTaskId: 异步任务id
注意：此字段可能返回 null，表示取不到有效值。
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.EvaluationTaskId = None
        self.EvaluationTaskStatus = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.EvaluationTaskId = params.get("EvaluationTaskId")
        self.EvaluationTaskStatus = params.get("EvaluationTaskStatus")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class StopAutoMLModelAccelerateTaskRequest(AbstractModel):
    """StopAutoMLModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        """
        self.AutoMLTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopAutoMLModelAccelerateTaskResponse(AbstractModel):
    """StopAutoMLModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param ModelAccTaskStatus: 模型优化任务状态
        :type ModelAccTaskStatus: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.ModelAccTaskStatus = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.ModelAccTaskStatus = params.get("ModelAccTaskStatus")
        self.RequestId = params.get("RequestId")


class StopAutoMLTaskTrainRequest(AbstractModel):
    """StopAutoMLTaskTrain请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopAutoMLTaskTrainResponse(AbstractModel):
    """StopAutoMLTaskTrain返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        :param TrainTaskStatus: 训练任务状态
        :type TrainTaskStatus: str
        :param AsyncTaskId: 异步任务ID
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.TrainTaskStatus = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.TrainTaskStatus = params.get("TrainTaskStatus")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class StopBatchTaskRequest(AbstractModel):
    """StopBatchTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param BatchTaskId: 跑批任务ID
        :type BatchTaskId: str
        """
        self.BatchTaskId = None


    def _deserialize(self, params):
        self.BatchTaskId = params.get("BatchTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopBatchTaskResponse(AbstractModel):
    """StopBatchTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StopModelAccelerateTaskRequest(AbstractModel):
    """StopModelAccelerateTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
        :type ModelAccTaskId: str
        """
        self.ModelAccTaskId = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopModelAccelerateTaskResponse(AbstractModel):
    """StopModelAccelerateTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param ModelAccTaskId: 模型加速任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskId: str
        :param AsyncTaskId: 异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AsyncTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.ModelAccTaskId = None
        self.AsyncTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.ModelAccTaskId = params.get("ModelAccTaskId")
        self.AsyncTaskId = params.get("AsyncTaskId")
        self.RequestId = params.get("RequestId")


class StopNotebookRequest(AbstractModel):
    """StopNotebook请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: notebook id
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopNotebookResponse(AbstractModel):
    """StopNotebook返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class StopTrainingTaskRequest(AbstractModel):
    """StopTrainingTask请求参数结构体

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        """
        self.Id = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class StopTrainingTaskResponse(AbstractModel):
    """StopTrainingTask返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class SyncDatasetRequest(AbstractModel):
    """SyncDataset请求参数结构体

    """

    def __init__(self):
        r"""
        :param DatasetId: 数据集ID
        :type DatasetId: str
        """
        self.DatasetId = None


    def _deserialize(self, params):
        self.DatasetId = params.get("DatasetId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class SyncDatasetResponse(AbstractModel):
    """SyncDataset返回参数结构体

    """

    def __init__(self):
        r"""
        :param TaskId: 异步任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.TaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.TaskId = params.get("TaskId")
        self.RequestId = params.get("RequestId")


class Tag(AbstractModel):
    """描述腾讯云标签

    """

    def __init__(self):
        r"""
        :param TagKey: 标签键
注意：此字段可能返回 null，表示取不到有效值。
        :type TagKey: str
        :param TagValue: 标签值
注意：此字段可能返回 null，表示取不到有效值。
        :type TagValue: str
        """
        self.TagKey = None
        self.TagValue = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValue = params.get("TagValue")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TagFilter(AbstractModel):
    """Tag过滤参数

    """

    def __init__(self):
        r"""
        :param TagKey: 标签键
        :type TagKey: str
        :param TagValues: 多个标签值
        :type TagValues: list of str
        """
        self.TagKey = None
        self.TagValues = None


    def _deserialize(self, params):
        self.TagKey = params.get("TagKey")
        self.TagValues = params.get("TagValues")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextAnalyzeResult(AbstractModel):
    """数据中心查询文本数据透视

    """

    def __init__(self):
        r"""
        :param ContentNumber: 样本总数
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentNumber: int
        :param ContentAverageLength: 平均样本长度
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentAverageLength: int
        :param ContentMaxLength: 样本最长长度
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentMaxLength: int
        :param ContentLengthDistribution: 样本长度分布，返回以50为分隔区间的长度区间内样本数量
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentLengthDistribution: list of ContentLengthCount
        :param ContentWordDistribution: 样本词频分布，返回出现频率最高的前100个词频, 按照频率倒排
注意：此字段可能返回 null，表示取不到有效值。
        :type ContentWordDistribution: list of WordCount
        """
        self.ContentNumber = None
        self.ContentAverageLength = None
        self.ContentMaxLength = None
        self.ContentLengthDistribution = None
        self.ContentWordDistribution = None


    def _deserialize(self, params):
        self.ContentNumber = params.get("ContentNumber")
        self.ContentAverageLength = params.get("ContentAverageLength")
        self.ContentMaxLength = params.get("ContentMaxLength")
        if params.get("ContentLengthDistribution") is not None:
            self.ContentLengthDistribution = []
            for item in params.get("ContentLengthDistribution"):
                obj = ContentLengthCount()
                obj._deserialize(item)
                self.ContentLengthDistribution.append(obj)
        if params.get("ContentWordDistribution") is not None:
            self.ContentWordDistribution = []
            for item in params.get("ContentWordDistribution"):
                obj = WordCount()
                obj._deserialize(item)
                self.ContentWordDistribution.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextLabelDistributionDetailInfoFifthClass(AbstractModel):
    """五级标签

    """

    def __init__(self):
        r"""
        :param LabelValue: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelValue: str
        :param LabelCount: 标签个数
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelCount: int
        :param LabelPercentage: 标签占比
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelPercentage: float
        """
        self.LabelValue = None
        self.LabelCount = None
        self.LabelPercentage = None


    def _deserialize(self, params):
        self.LabelValue = params.get("LabelValue")
        self.LabelCount = params.get("LabelCount")
        self.LabelPercentage = params.get("LabelPercentage")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextLabelDistributionDetailInfoFirstClass(AbstractModel):
    """一级标签

    """

    def __init__(self):
        r"""
        :param LabelValue: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelValue: str
        :param LabelCount: 标签个数
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelCount: int
        :param LabelPercentage: 标签占比
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelPercentage: float
        :param ChildLabelList: 子标签分布
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildLabelList: list of TextLabelDistributionDetailInfoSecondClass
        """
        self.LabelValue = None
        self.LabelCount = None
        self.LabelPercentage = None
        self.ChildLabelList = None


    def _deserialize(self, params):
        self.LabelValue = params.get("LabelValue")
        self.LabelCount = params.get("LabelCount")
        self.LabelPercentage = params.get("LabelPercentage")
        if params.get("ChildLabelList") is not None:
            self.ChildLabelList = []
            for item in params.get("ChildLabelList"):
                obj = TextLabelDistributionDetailInfoSecondClass()
                obj._deserialize(item)
                self.ChildLabelList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextLabelDistributionDetailInfoFourthClass(AbstractModel):
    """四级标签

    """

    def __init__(self):
        r"""
        :param LabelValue: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelValue: str
        :param LabelCount: 标签个数
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelCount: int
        :param LabelPercentage: 标签占比
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelPercentage: float
        :param ChildLabelList: 子标签分布
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildLabelList: list of TextLabelDistributionDetailInfoFifthClass
        """
        self.LabelValue = None
        self.LabelCount = None
        self.LabelPercentage = None
        self.ChildLabelList = None


    def _deserialize(self, params):
        self.LabelValue = params.get("LabelValue")
        self.LabelCount = params.get("LabelCount")
        self.LabelPercentage = params.get("LabelPercentage")
        if params.get("ChildLabelList") is not None:
            self.ChildLabelList = []
            for item in params.get("ChildLabelList"):
                obj = TextLabelDistributionDetailInfoFifthClass()
                obj._deserialize(item)
                self.ChildLabelList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextLabelDistributionDetailInfoSecondClass(AbstractModel):
    """二级标签

    """

    def __init__(self):
        r"""
        :param LabelValue: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelValue: str
        :param LabelCount: 标签个数
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelCount: int
        :param LabelPercentage: 标签占比
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelPercentage: float
        :param ChildLabelList: 子标签分布
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildLabelList: list of TextLabelDistributionDetailInfoThirdClass
        """
        self.LabelValue = None
        self.LabelCount = None
        self.LabelPercentage = None
        self.ChildLabelList = None


    def _deserialize(self, params):
        self.LabelValue = params.get("LabelValue")
        self.LabelCount = params.get("LabelCount")
        self.LabelPercentage = params.get("LabelPercentage")
        if params.get("ChildLabelList") is not None:
            self.ChildLabelList = []
            for item in params.get("ChildLabelList"):
                obj = TextLabelDistributionDetailInfoThirdClass()
                obj._deserialize(item)
                self.ChildLabelList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextLabelDistributionDetailInfoThirdClass(AbstractModel):
    """三级标签

    """

    def __init__(self):
        r"""
        :param LabelValue: 标签名称
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelValue: str
        :param LabelCount: 标签个数
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelCount: int
        :param LabelPercentage: 标签占比
注意：此字段可能返回 null，表示取不到有效值。
        :type LabelPercentage: float
        :param ChildLabelList: 子标签分布
注意：此字段可能返回 null，表示取不到有效值。
        :type ChildLabelList: list of TextLabelDistributionDetailInfoFourthClass
        """
        self.LabelValue = None
        self.LabelCount = None
        self.LabelPercentage = None
        self.ChildLabelList = None


    def _deserialize(self, params):
        self.LabelValue = params.get("LabelValue")
        self.LabelCount = params.get("LabelCount")
        self.LabelPercentage = params.get("LabelPercentage")
        if params.get("ChildLabelList") is not None:
            self.ChildLabelList = []
            for item in params.get("ChildLabelList"):
                obj = TextLabelDistributionDetailInfoFourthClass()
                obj._deserialize(item)
                self.ChildLabelList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TextLabelDistributionInfo(AbstractModel):
    """文本标签

    """

    def __init__(self):
        r"""
        :param Theme: 文本分类题目名称
注意：此字段可能返回 null，表示取不到有效值。
        :type Theme: str
        :param ClassLabelList: 一级标签分布
注意：此字段可能返回 null，表示取不到有效值。
        :type ClassLabelList: list of TextLabelDistributionDetailInfoFirstClass
        """
        self.Theme = None
        self.ClassLabelList = None


    def _deserialize(self, params):
        self.Theme = params.get("Theme")
        if params.get("ClassLabelList") is not None:
            self.ClassLabelList = []
            for item in params.get("ClassLabelList"):
                obj = TextLabelDistributionDetailInfoFirstClass()
                obj._deserialize(item)
                self.ClassLabelList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainResourceConfig(AbstractModel):
    """训练资源配置

    """

    def __init__(self):
        r"""
        :param ChargeType: 计费模式
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param ResourceGroupId: 资源组ID
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param ResourceGroupName: 资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param ResourceConfigInfo: 资源配置
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceConfigInfo: :class:`tencentcloud.tione.v20211111.models.ResourceConfigInfo`
        """
        self.ChargeType = None
        self.ResourceGroupId = None
        self.ResourceGroupName = None
        self.ResourceConfigInfo = None


    def _deserialize(self, params):
        self.ChargeType = params.get("ChargeType")
        self.ResourceGroupId = params.get("ResourceGroupId")
        self.ResourceGroupName = params.get("ResourceGroupName")
        if params.get("ResourceConfigInfo") is not None:
            self.ResourceConfigInfo = ResourceConfigInfo()
            self.ResourceConfigInfo._deserialize(params.get("ResourceConfigInfo"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainTask(AbstractModel):
    """训练任务

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskId: str
        :param TrainId: 任务式建模任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainId: str
        :param TaskVersion: 任务版本
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskVersion: str
        :param Tags: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param AutoMLTaskDescription: 任务描述
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoMLTaskDescription: str
        :param SceneName: 场景名称
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneName: str
        :param Creator: 创建人
注意：此字段可能返回 null，表示取不到有效值。
        :type Creator: str
        :param Updator: 修改人
注意：此字段可能返回 null，表示取不到有效值。
        :type Updator: str
        :param TrainTaskStatus: 训练状态
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskStatus: str
        :param TrainTaskProgress: 训练进度
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskProgress: int
        :param TrainTaskStartTime: 训练开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskStartTime: str
        :param TrainTaskEndTime: 训练结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskEndTime: str
        :param ErrorMsg: 训练任务失败时错误详情
注意：此字段可能返回 null，表示取不到有效值。
        :type ErrorMsg: str
        :param ChargeType: 计费类型
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeType: str
        :param ChargeStatus: 计费状态
注意：此字段可能返回 null，表示取不到有效值。
        :type ChargeStatus: str
        :param TrainResourceConfig: 训练资源配置
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainResourceConfig: :class:`tencentcloud.tione.v20211111.models.TrainResourceConfig`
        :param CreateTime: 任务创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        :param TaskOutputCosInfo: 任务输出cos路径
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskOutputCosInfo: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelTrainConfig: 训练模型配置
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelTrainConfig: :class:`tencentcloud.tione.v20211111.models.ModelTrainConfig`
        :param SceneId: 场景ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneId: str
        :param BillingInfo: 账单信息
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfo: str
        :param SceneDomain: 场景领域
注意：此字段可能返回 null，表示取不到有效值。
        :type SceneDomain: str
        :param ModelAccTaskStatus: 模型优化状态
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelAccTaskStatus: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.TrainId = None
        self.TaskVersion = None
        self.Tags = None
        self.AutoMLTaskDescription = None
        self.SceneName = None
        self.Creator = None
        self.Updator = None
        self.TrainTaskStatus = None
        self.TrainTaskProgress = None
        self.TrainTaskStartTime = None
        self.TrainTaskEndTime = None
        self.ErrorMsg = None
        self.ChargeType = None
        self.ChargeStatus = None
        self.TrainResourceConfig = None
        self.CreateTime = None
        self.TaskOutputCosInfo = None
        self.ModelTrainConfig = None
        self.SceneId = None
        self.BillingInfo = None
        self.SceneDomain = None
        self.ModelAccTaskStatus = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.TrainId = params.get("TrainId")
        self.TaskVersion = params.get("TaskVersion")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.AutoMLTaskDescription = params.get("AutoMLTaskDescription")
        self.SceneName = params.get("SceneName")
        self.Creator = params.get("Creator")
        self.Updator = params.get("Updator")
        self.TrainTaskStatus = params.get("TrainTaskStatus")
        self.TrainTaskProgress = params.get("TrainTaskProgress")
        self.TrainTaskStartTime = params.get("TrainTaskStartTime")
        self.TrainTaskEndTime = params.get("TrainTaskEndTime")
        self.ErrorMsg = params.get("ErrorMsg")
        self.ChargeType = params.get("ChargeType")
        self.ChargeStatus = params.get("ChargeStatus")
        if params.get("TrainResourceConfig") is not None:
            self.TrainResourceConfig = TrainResourceConfig()
            self.TrainResourceConfig._deserialize(params.get("TrainResourceConfig"))
        self.CreateTime = params.get("CreateTime")
        if params.get("TaskOutputCosInfo") is not None:
            self.TaskOutputCosInfo = CosPathInfo()
            self.TaskOutputCosInfo._deserialize(params.get("TaskOutputCosInfo"))
        if params.get("ModelTrainConfig") is not None:
            self.ModelTrainConfig = ModelTrainConfig()
            self.ModelTrainConfig._deserialize(params.get("ModelTrainConfig"))
        self.SceneId = params.get("SceneId")
        self.BillingInfo = params.get("BillingInfo")
        self.SceneDomain = params.get("SceneDomain")
        self.ModelAccTaskStatus = params.get("ModelAccTaskStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainTaskGroup(AbstractModel):
    """训练任务组

    """

    def __init__(self):
        r"""
        :param TaskGroupId: 自动学习任务组ID
        :type TaskGroupId: str
        :param TaskName: 自动学习任务名称
注意：此字段可能返回 null，表示取不到有效值。
        :type TaskName: str
        :param TrainTasks: 自动学习任务列表
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTasks: list of TrainTask
        """
        self.TaskGroupId = None
        self.TaskName = None
        self.TrainTasks = None


    def _deserialize(self, params):
        self.TaskGroupId = params.get("TaskGroupId")
        self.TaskName = params.get("TaskName")
        if params.get("TrainTasks") is not None:
            self.TrainTasks = []
            for item in params.get("TrainTasks"):
                obj = TrainTask()
                obj._deserialize(item)
                self.TrainTasks.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingDataPoint(AbstractModel):
    """训练数据

    """

    def __init__(self):
        r"""
        :param Timestamp: 时间戳
注意：此字段可能返回 null，表示取不到有效值。
        :type Timestamp: int
        :param Value: 训练上报的值。可以为训练指标（双精度浮点数，也可以为Epoch/Step（两者皆保证是整数）
注意：此字段可能返回 null，表示取不到有效值。
        :type Value: int
        """
        self.Timestamp = None
        self.Value = None


    def _deserialize(self, params):
        self.Timestamp = params.get("Timestamp")
        self.Value = params.get("Value")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingMetric(AbstractModel):
    """训练指标

    """

    def __init__(self):
        r"""
        :param MetricName: 指标名
        :type MetricName: str
        :param Values: 数据值
注意：此字段可能返回 null，表示取不到有效值。
        :type Values: list of TrainingDataPoint
        :param Epochs: 上报的Epoch. 可能为空
注意：此字段可能返回 null，表示取不到有效值。
        :type Epochs: list of TrainingDataPoint
        :param Steps: 上报的Step. 可能为空
注意：此字段可能返回 null，表示取不到有效值。
        :type Steps: list of TrainingDataPoint
        :param TotalSteps: 上报的TotalSteps. 可能为空
注意：此字段可能返回 null，表示取不到有效值。
        :type TotalSteps: list of TrainingDataPoint
        """
        self.MetricName = None
        self.Values = None
        self.Epochs = None
        self.Steps = None
        self.TotalSteps = None


    def _deserialize(self, params):
        self.MetricName = params.get("MetricName")
        if params.get("Values") is not None:
            self.Values = []
            for item in params.get("Values"):
                obj = TrainingDataPoint()
                obj._deserialize(item)
                self.Values.append(obj)
        if params.get("Epochs") is not None:
            self.Epochs = []
            for item in params.get("Epochs"):
                obj = TrainingDataPoint()
                obj._deserialize(item)
                self.Epochs.append(obj)
        if params.get("Steps") is not None:
            self.Steps = []
            for item in params.get("Steps"):
                obj = TrainingDataPoint()
                obj._deserialize(item)
                self.Steps.append(obj)
        if params.get("TotalSteps") is not None:
            self.TotalSteps = []
            for item in params.get("TotalSteps"):
                obj = TrainingDataPoint()
                obj._deserialize(item)
                self.TotalSteps.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingModelDTO(AbstractModel):
    """模型列表

    """

    def __init__(self):
        r"""
        :param TrainingModelId: 模型id
        :type TrainingModelId: str
        :param TrainingModelName: 模型名称
        :type TrainingModelName: str
        :param Tags: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param CreateTime: 模型创建时间
注意：此字段可能返回 null，表示取不到有效值。
        :type CreateTime: str
        """
        self.TrainingModelId = None
        self.TrainingModelName = None
        self.Tags = None
        self.CreateTime = None


    def _deserialize(self, params):
        self.TrainingModelId = params.get("TrainingModelId")
        self.TrainingModelName = params.get("TrainingModelName")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.CreateTime = params.get("CreateTime")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingModelVersionDTO(AbstractModel):
    """模型版本列表

    """

    def __init__(self):
        r"""
        :param TrainingModelId: 模型id
        :type TrainingModelId: str
        :param TrainingModelVersionId: 模型版本id
        :type TrainingModelVersionId: str
        :param TrainingModelVersion: 模型版本
        :type TrainingModelVersion: str
        :param TrainingModelSource: 模型来源
        :type TrainingModelSource: str
        :param TrainingModelCreateTime: 创建时间
        :type TrainingModelCreateTime: str
        :param TrainingModelCreator: 创建人uin
        :type TrainingModelCreator: str
        :param AlgorithmFramework: 算法框架
        :type AlgorithmFramework: str
        :param ReasoningEnvironment: 推理环境
        :type ReasoningEnvironment: str
        :param ReasoningEnvironmentSource: 推理环境来源
        :type ReasoningEnvironmentSource: str
        :param TrainingModelIndex: 模型指标
        :type TrainingModelIndex: str
        :param TrainingJobName: 训练任务名称
        :type TrainingJobName: str
        :param TrainingModelCosPath: 模型cos路径
        :type TrainingModelCosPath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param TrainingModelName: 模型名称
        :type TrainingModelName: str
        :param TrainingJobId: 训练任务id
        :type TrainingJobId: str
        :param ReasoningImageInfo: 自定义推理环境
        :type ReasoningImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param CreateTime: 模型版本创建时间
        :type CreateTime: str
        :param TrainingModelStatus: 模型处理状态
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingModelStatus: str
        :param TrainingModelProgress: 模型处理进度
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingModelProgress: int
        :param TrainingModelErrorMsg: 模型错误信息
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingModelErrorMsg: str
        :param TrainingModelFormat: 模型格式
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingModelFormat: str
        :param VersionType: 模型版本类型
注意：此字段可能返回 null，表示取不到有效值。
        :type VersionType: str
        :param GPUType: GPU类型
注意：此字段可能返回 null，表示取不到有效值。
        :type GPUType: str
        :param AutoClean: 模型自动清理开关
注意：此字段可能返回 null，表示取不到有效值。
        :type AutoClean: str
        :param ModelCleanPeriod: 模型清理周期
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelCleanPeriod: int
        :param MaxReservedModels: 模型数量保留上限
注意：此字段可能返回 null，表示取不到有效值。
        :type MaxReservedModels: int
        :param ModelHotUpdatePath: 模型热更新目录
注意：此字段可能返回 null，表示取不到有效值。
        :type ModelHotUpdatePath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        """
        self.TrainingModelId = None
        self.TrainingModelVersionId = None
        self.TrainingModelVersion = None
        self.TrainingModelSource = None
        self.TrainingModelCreateTime = None
        self.TrainingModelCreator = None
        self.AlgorithmFramework = None
        self.ReasoningEnvironment = None
        self.ReasoningEnvironmentSource = None
        self.TrainingModelIndex = None
        self.TrainingJobName = None
        self.TrainingModelCosPath = None
        self.TrainingModelName = None
        self.TrainingJobId = None
        self.ReasoningImageInfo = None
        self.CreateTime = None
        self.TrainingModelStatus = None
        self.TrainingModelProgress = None
        self.TrainingModelErrorMsg = None
        self.TrainingModelFormat = None
        self.VersionType = None
        self.GPUType = None
        self.AutoClean = None
        self.ModelCleanPeriod = None
        self.MaxReservedModels = None
        self.ModelHotUpdatePath = None


    def _deserialize(self, params):
        self.TrainingModelId = params.get("TrainingModelId")
        self.TrainingModelVersionId = params.get("TrainingModelVersionId")
        self.TrainingModelVersion = params.get("TrainingModelVersion")
        self.TrainingModelSource = params.get("TrainingModelSource")
        self.TrainingModelCreateTime = params.get("TrainingModelCreateTime")
        self.TrainingModelCreator = params.get("TrainingModelCreator")
        self.AlgorithmFramework = params.get("AlgorithmFramework")
        self.ReasoningEnvironment = params.get("ReasoningEnvironment")
        self.ReasoningEnvironmentSource = params.get("ReasoningEnvironmentSource")
        self.TrainingModelIndex = params.get("TrainingModelIndex")
        self.TrainingJobName = params.get("TrainingJobName")
        if params.get("TrainingModelCosPath") is not None:
            self.TrainingModelCosPath = CosPathInfo()
            self.TrainingModelCosPath._deserialize(params.get("TrainingModelCosPath"))
        self.TrainingModelName = params.get("TrainingModelName")
        self.TrainingJobId = params.get("TrainingJobId")
        if params.get("ReasoningImageInfo") is not None:
            self.ReasoningImageInfo = ImageInfo()
            self.ReasoningImageInfo._deserialize(params.get("ReasoningImageInfo"))
        self.CreateTime = params.get("CreateTime")
        self.TrainingModelStatus = params.get("TrainingModelStatus")
        self.TrainingModelProgress = params.get("TrainingModelProgress")
        self.TrainingModelErrorMsg = params.get("TrainingModelErrorMsg")
        self.TrainingModelFormat = params.get("TrainingModelFormat")
        self.VersionType = params.get("VersionType")
        self.GPUType = params.get("GPUType")
        self.AutoClean = params.get("AutoClean")
        self.ModelCleanPeriod = params.get("ModelCleanPeriod")
        self.MaxReservedModels = params.get("MaxReservedModels")
        if params.get("ModelHotUpdatePath") is not None:
            self.ModelHotUpdatePath = CosPathInfo()
            self.ModelHotUpdatePath._deserialize(params.get("ModelHotUpdatePath"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingTaskDetail(AbstractModel):
    """训练任务详情

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        :param Name: 训练任务名称
        :type Name: str
        :param Uin: 主账号uin
        :type Uin: str
        :param SubUin: 子账号uin
        :type SubUin: str
        :param Region: 地域
        :type Region: str
        :param FrameworkName: 训练框架名称，eg：SPARK、TENSORFLOW、PYTORCH、LIGHT
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkName: str
        :param FrameworkVersion: 训练框架版本
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkVersion: str
        :param FrameworkEnvironment: 框架运行环境
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkEnvironment: str
        :param ChargeType: 计费模式
        :type ChargeType: str
        :param ResourceGroupId: 预付费专用资源组
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param ResourceConfigInfos: 资源配置
        :type ResourceConfigInfos: list of ResourceConfigInfo
        :param Tags: 标签
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        :param TrainingMode: 训练模式，eg：PS_WORKER、DDP、MPI、HOROVOD
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingMode: str
        :param CodePackagePath: 代码包
        :type CodePackagePath: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param StartCmdInfo: 启动命令信息
        :type StartCmdInfo: :class:`tencentcloud.tione.v20211111.models.StartCmdInfo`
        :param DataSource: 数据来源，eg：DATASET、COS
注意：此字段可能返回 null，表示取不到有效值。
        :type DataSource: str
        :param DataConfigs: 数据配置
注意：此字段可能返回 null，表示取不到有效值。
        :type DataConfigs: list of DataConfig
        :param TuningParameters: 调优参数
注意：此字段可能返回 null，表示取不到有效值。
        :type TuningParameters: str
        :param Output: 训练输出
        :type Output: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param LogEnable: 是否上报日志
        :type LogEnable: bool
        :param LogConfig: 日志配置
注意：此字段可能返回 null，表示取不到有效值。
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param VpcId: VPC ID
注意：此字段可能返回 null，表示取不到有效值。
        :type VpcId: str
        :param SubnetId: 子网ID
注意：此字段可能返回 null，表示取不到有效值。
        :type SubnetId: str
        :param ImageInfo: 自定义镜像信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param RuntimeInSeconds: 运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param StartTime: 训练开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param ChargeStatus: 计费状态，eg：BILLING计费中，ARREARS_STOP欠费停止，NOT_BILLING不在计费中
        :type ChargeStatus: str
        :param LatestInstanceId: 最近一次实例ID
注意：此字段可能返回 null，表示取不到有效值。
        :type LatestInstanceId: str
        :param TensorBoardId: TensorBoard ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TensorBoardId: str
        :param Remark: 备注
注意：此字段可能返回 null，表示取不到有效值。
        :type Remark: str
        :param FailureReason: 失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailureReason: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param EndTime: 训练结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param BillingInfo: 计费金额信息，eg：2.00元/小时 (for后付费)
注意：此字段可能返回 null，表示取不到有效值。
        :type BillingInfo: str
        :param ResourceGroupName: 预付费专用资源组名称
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupName: str
        :param Message: 任务信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param Status: 任务状态
        :type Status: str
        """
        self.Id = None
        self.Name = None
        self.Uin = None
        self.SubUin = None
        self.Region = None
        self.FrameworkName = None
        self.FrameworkVersion = None
        self.FrameworkEnvironment = None
        self.ChargeType = None
        self.ResourceGroupId = None
        self.ResourceConfigInfos = None
        self.Tags = None
        self.TrainingMode = None
        self.CodePackagePath = None
        self.StartCmdInfo = None
        self.DataSource = None
        self.DataConfigs = None
        self.TuningParameters = None
        self.Output = None
        self.LogEnable = None
        self.LogConfig = None
        self.VpcId = None
        self.SubnetId = None
        self.ImageInfo = None
        self.RuntimeInSeconds = None
        self.CreateTime = None
        self.StartTime = None
        self.ChargeStatus = None
        self.LatestInstanceId = None
        self.TensorBoardId = None
        self.Remark = None
        self.FailureReason = None
        self.UpdateTime = None
        self.EndTime = None
        self.BillingInfo = None
        self.ResourceGroupName = None
        self.Message = None
        self.Status = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.Uin = params.get("Uin")
        self.SubUin = params.get("SubUin")
        self.Region = params.get("Region")
        self.FrameworkName = params.get("FrameworkName")
        self.FrameworkVersion = params.get("FrameworkVersion")
        self.FrameworkEnvironment = params.get("FrameworkEnvironment")
        self.ChargeType = params.get("ChargeType")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("ResourceConfigInfos") is not None:
            self.ResourceConfigInfos = []
            for item in params.get("ResourceConfigInfos"):
                obj = ResourceConfigInfo()
                obj._deserialize(item)
                self.ResourceConfigInfos.append(obj)
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        self.TrainingMode = params.get("TrainingMode")
        if params.get("CodePackagePath") is not None:
            self.CodePackagePath = CosPathInfo()
            self.CodePackagePath._deserialize(params.get("CodePackagePath"))
        if params.get("StartCmdInfo") is not None:
            self.StartCmdInfo = StartCmdInfo()
            self.StartCmdInfo._deserialize(params.get("StartCmdInfo"))
        self.DataSource = params.get("DataSource")
        if params.get("DataConfigs") is not None:
            self.DataConfigs = []
            for item in params.get("DataConfigs"):
                obj = DataConfig()
                obj._deserialize(item)
                self.DataConfigs.append(obj)
        self.TuningParameters = params.get("TuningParameters")
        if params.get("Output") is not None:
            self.Output = CosPathInfo()
            self.Output._deserialize(params.get("Output"))
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.VpcId = params.get("VpcId")
        self.SubnetId = params.get("SubnetId")
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.ChargeStatus = params.get("ChargeStatus")
        self.LatestInstanceId = params.get("LatestInstanceId")
        self.TensorBoardId = params.get("TensorBoardId")
        self.Remark = params.get("Remark")
        self.FailureReason = params.get("FailureReason")
        self.UpdateTime = params.get("UpdateTime")
        self.EndTime = params.get("EndTime")
        self.BillingInfo = params.get("BillingInfo")
        self.ResourceGroupName = params.get("ResourceGroupName")
        self.Message = params.get("Message")
        self.Status = params.get("Status")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingTaskInfo(AbstractModel):
    """任务式建模训练任务详情

    """

    def __init__(self):
        r"""
        :param TrainTaskName: 任务名
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainTaskName: str
        :param TrainId: 训练任务ID
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainId: str
        :param TrainPodId: 训练podId
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainPodId: str
        """
        self.TrainTaskName = None
        self.TrainId = None
        self.TrainPodId = None


    def _deserialize(self, params):
        self.TrainTaskName = params.get("TrainTaskName")
        self.TrainId = params.get("TrainId")
        self.TrainPodId = params.get("TrainPodId")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class TrainingTaskSetItem(AbstractModel):
    """出参类型

    """

    def __init__(self):
        r"""
        :param Id: 训练任务ID
        :type Id: str
        :param Name: 训练任务名称
        :type Name: str
        :param FrameworkName: 框架名称
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkName: str
        :param FrameworkVersion: 训练框架版本
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkVersion: str
        :param FrameworkEnvironment: 框架运行环境
注意：此字段可能返回 null，表示取不到有效值。
        :type FrameworkEnvironment: str
        :param ChargeType: 计费模式
        :type ChargeType: str
        :param ChargeStatus: 计费状态，eg：BILLING计费中，ARREARS_STOP欠费停止，NOT_BILLING不在计费中
        :type ChargeStatus: str
        :param ResourceGroupId: 预付费专用资源组
注意：此字段可能返回 null，表示取不到有效值。
        :type ResourceGroupId: str
        :param ResourceConfigInfos: 资源配置
        :type ResourceConfigInfos: list of ResourceConfigInfo
        :param TrainingMode: 训练模式eg：PS_WORKER、DDP、MPI、HOROVOD
注意：此字段可能返回 null，表示取不到有效值。
        :type TrainingMode: str
        :param Status: 任务状态
        :type Status: str
        :param RuntimeInSeconds: 运行时长
注意：此字段可能返回 null，表示取不到有效值。
        :type RuntimeInSeconds: int
        :param CreateTime: 创建时间
        :type CreateTime: str
        :param StartTime: 训练开始时间
注意：此字段可能返回 null，表示取不到有效值。
        :type StartTime: str
        :param EndTime: 训练结束时间
注意：此字段可能返回 null，表示取不到有效值。
        :type EndTime: str
        :param Output: 训练输出
        :type Output: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param FailureReason: 失败原因
注意：此字段可能返回 null，表示取不到有效值。
        :type FailureReason: str
        :param UpdateTime: 更新时间
        :type UpdateTime: str
        :param BillingInfo: 计费金额信息，eg：2.00元/小时 (for后付费)
        :type BillingInfo: str
        :param ResourceGroupName: 预付费专用资源组名称
        :type ResourceGroupName: str
        :param ImageInfo: 自定义镜像信息
注意：此字段可能返回 null，表示取不到有效值。
        :type ImageInfo: :class:`tencentcloud.tione.v20211111.models.ImageInfo`
        :param Message: 任务信息
注意：此字段可能返回 null，表示取不到有效值。
        :type Message: str
        :param Tags: 标签配置
注意：此字段可能返回 null，表示取不到有效值。
        :type Tags: list of Tag
        """
        self.Id = None
        self.Name = None
        self.FrameworkName = None
        self.FrameworkVersion = None
        self.FrameworkEnvironment = None
        self.ChargeType = None
        self.ChargeStatus = None
        self.ResourceGroupId = None
        self.ResourceConfigInfos = None
        self.TrainingMode = None
        self.Status = None
        self.RuntimeInSeconds = None
        self.CreateTime = None
        self.StartTime = None
        self.EndTime = None
        self.Output = None
        self.FailureReason = None
        self.UpdateTime = None
        self.BillingInfo = None
        self.ResourceGroupName = None
        self.ImageInfo = None
        self.Message = None
        self.Tags = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Name = params.get("Name")
        self.FrameworkName = params.get("FrameworkName")
        self.FrameworkVersion = params.get("FrameworkVersion")
        self.FrameworkEnvironment = params.get("FrameworkEnvironment")
        self.ChargeType = params.get("ChargeType")
        self.ChargeStatus = params.get("ChargeStatus")
        self.ResourceGroupId = params.get("ResourceGroupId")
        if params.get("ResourceConfigInfos") is not None:
            self.ResourceConfigInfos = []
            for item in params.get("ResourceConfigInfos"):
                obj = ResourceConfigInfo()
                obj._deserialize(item)
                self.ResourceConfigInfos.append(obj)
        self.TrainingMode = params.get("TrainingMode")
        self.Status = params.get("Status")
        self.RuntimeInSeconds = params.get("RuntimeInSeconds")
        self.CreateTime = params.get("CreateTime")
        self.StartTime = params.get("StartTime")
        self.EndTime = params.get("EndTime")
        if params.get("Output") is not None:
            self.Output = CosPathInfo()
            self.Output._deserialize(params.get("Output"))
        self.FailureReason = params.get("FailureReason")
        self.UpdateTime = params.get("UpdateTime")
        self.BillingInfo = params.get("BillingInfo")
        self.ResourceGroupName = params.get("ResourceGroupName")
        if params.get("ImageInfo") is not None:
            self.ImageInfo = ImageInfo()
            self.ImageInfo._deserialize(params.get("ImageInfo"))
        self.Message = params.get("Message")
        if params.get("Tags") is not None:
            self.Tags = []
            for item in params.get("Tags"):
                obj = Tag()
                obj._deserialize(item)
                self.Tags.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateAutoMLCLSLogConfigRequest(AbstractModel):
    """UpdateAutoMLCLSLogConfig请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param LogEnable: 是否开启日志投递
        :type LogEnable: bool
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        :param LogConfig: 日志投递参数
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        """
        self.AutoMLTaskId = None
        self.LogEnable = None
        self.TrainTaskId = None
        self.LogConfig = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.LogEnable = params.get("LogEnable")
        self.TrainTaskId = params.get("TrainTaskId")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateAutoMLCLSLogConfigResponse(AbstractModel):
    """UpdateAutoMLCLSLogConfig返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param TrainTaskId: 训练任务ID
        :type TrainTaskId: str
        :param LogEnable: 是否开启日志投递
注意：此字段可能返回 null，表示取不到有效值。
        :type LogEnable: bool
        :param LogConfig: 日志投递参数
注意：此字段可能返回 null，表示取不到有效值。
        :type LogConfig: :class:`tencentcloud.tione.v20211111.models.LogConfig`
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.TrainTaskId = None
        self.LogEnable = None
        self.LogConfig = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.TrainTaskId = params.get("TrainTaskId")
        self.LogEnable = params.get("LogEnable")
        if params.get("LogConfig") is not None:
            self.LogConfig = LogConfig()
            self.LogConfig._deserialize(params.get("LogConfig"))
        self.RequestId = params.get("RequestId")


class UpdateAutoMLTaskConfigReqRequest(AbstractModel):
    """UpdateAutoMLTaskConfigReq请求参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param DataConfig: 数据配置
        :type DataConfig: :class:`tencentcloud.tione.v20211111.models.MLDataConfig`
        :param TaskOutputConfig: 自动学习任务输出路径
        :type TaskOutputConfig: :class:`tencentcloud.tione.v20211111.models.CosPathInfo`
        :param ModelTrainConfig: 模型配置
        :type ModelTrainConfig: :class:`tencentcloud.tione.v20211111.models.ModelTrainConfig`
        :param ModelParamConfig: 模型超参数
        :type ModelParamConfig: str
        :param TrainResourceConfig: 训练资源配置
        :type TrainResourceConfig: :class:`tencentcloud.tione.v20211111.models.TrainResourceConfig`
        """
        self.AutoMLTaskId = None
        self.DataConfig = None
        self.TaskOutputConfig = None
        self.ModelTrainConfig = None
        self.ModelParamConfig = None
        self.TrainResourceConfig = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        if params.get("DataConfig") is not None:
            self.DataConfig = MLDataConfig()
            self.DataConfig._deserialize(params.get("DataConfig"))
        if params.get("TaskOutputConfig") is not None:
            self.TaskOutputConfig = CosPathInfo()
            self.TaskOutputConfig._deserialize(params.get("TaskOutputConfig"))
        if params.get("ModelTrainConfig") is not None:
            self.ModelTrainConfig = ModelTrainConfig()
            self.ModelTrainConfig._deserialize(params.get("ModelTrainConfig"))
        self.ModelParamConfig = params.get("ModelParamConfig")
        if params.get("TrainResourceConfig") is not None:
            self.TrainResourceConfig = TrainResourceConfig()
            self.TrainResourceConfig._deserialize(params.get("TrainResourceConfig"))
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UpdateAutoMLTaskConfigReqResponse(AbstractModel):
    """UpdateAutoMLTaskConfigReq返回参数结构体

    """

    def __init__(self):
        r"""
        :param AutoMLTaskId: 自动学习任务ID
        :type AutoMLTaskId: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.AutoMLTaskId = None
        self.RequestId = None


    def _deserialize(self, params):
        self.AutoMLTaskId = params.get("AutoMLTaskId")
        self.RequestId = params.get("RequestId")


class UploadDataRequest(AbstractModel):
    """UploadData请求参数结构体

    """

    def __init__(self):
        r"""
        :param Data: 上传数据
        :type Data: str
        :param DataType: 上传数据类型
        :type DataType: str
        """
        self.Data = None
        self.DataType = None


    def _deserialize(self, params):
        self.Data = params.get("Data")
        self.DataType = params.get("DataType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class UploadDataResponse(AbstractModel):
    """UploadData返回参数结构体

    """

    def __init__(self):
        r"""
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.RequestId = None


    def _deserialize(self, params):
        self.RequestId = params.get("RequestId")


class VolumeMount(AbstractModel):
    """外部挂载信息

    """

    def __init__(self):
        r"""
        :param CFSConfig: cfs的配置信息
        :type CFSConfig: :class:`tencentcloud.tione.v20211111.models.CFSConfig`
        :param VolumeSourceType: 挂载源类型
        :type VolumeSourceType: str
        """
        self.CFSConfig = None
        self.VolumeSourceType = None


    def _deserialize(self, params):
        if params.get("CFSConfig") is not None:
            self.CFSConfig = CFSConfig()
            self.CFSConfig._deserialize(params.get("CFSConfig"))
        self.VolumeSourceType = params.get("VolumeSourceType")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WeDataHDFSConfig(AbstractModel):
    """WeData HDFS存储的配置

    """

    def __init__(self):
        r"""
        :param Id: WeData HDSF数据源ID
        :type Id: int
        :param Path: WeData HDSF 数据源存储的路径
        :type Path: str
        """
        self.Id = None
        self.Path = None


    def _deserialize(self, params):
        self.Id = params.get("Id")
        self.Path = params.get("Path")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WeightEntry(AbstractModel):
    """服务的权重

    """

    def __init__(self):
        r"""
        :param ServiceId: 服务id
        :type ServiceId: str
        :param Weight: 流量权重值，同 ServiceGroup 下 总和应为 100
        :type Weight: int
        """
        self.ServiceId = None
        self.Weight = None


    def _deserialize(self, params):
        self.ServiceId = params.get("ServiceId")
        self.Weight = params.get("Weight")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WordCount(AbstractModel):
    """数据中心查询文本透视

    """

    def __init__(self):
        r"""
        :param Word: 单词
注意：此字段可能返回 null，表示取不到有效值。
        :type Word: str
        :param Count: 单词出现的次数
注意：此字段可能返回 null，表示取不到有效值。
        :type Count: int
        """
        self.Word = None
        self.Count = None


    def _deserialize(self, params):
        self.Word = params.get("Word")
        self.Count = params.get("Count")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class WorkloadStatus(AbstractModel):
    """工作负载的状态

    """

    def __init__(self):
        r"""
        :param Replicas: 当前实例数
        :type Replicas: int
        :param UpdatedReplicas: 更新的实例数
        :type UpdatedReplicas: int
        :param ReadyReplicas: 就绪的实例数
        :type ReadyReplicas: int
        :param AvailableReplicas: 可用的实例数
        :type AvailableReplicas: int
        :param UnavailableReplicas: 不可用的实例数
        :type UnavailableReplicas: int
        :param Status: Normal	正常运行中
Abnormal	服务异常，例如容器启动失败等
Waiting	服务等待中，例如容器下载镜像过程等
Stopped   已停止 
Pending 启动中
Stopping 停止中
        :type Status: str
        :param StatefulSetCondition: 工作负载的状况信息
        :type StatefulSetCondition: list of StatefulSetCondition
        """
        self.Replicas = None
        self.UpdatedReplicas = None
        self.ReadyReplicas = None
        self.AvailableReplicas = None
        self.UnavailableReplicas = None
        self.Status = None
        self.StatefulSetCondition = None


    def _deserialize(self, params):
        self.Replicas = params.get("Replicas")
        self.UpdatedReplicas = params.get("UpdatedReplicas")
        self.ReadyReplicas = params.get("ReadyReplicas")
        self.AvailableReplicas = params.get("AvailableReplicas")
        self.UnavailableReplicas = params.get("UnavailableReplicas")
        self.Status = params.get("Status")
        if params.get("StatefulSetCondition") is not None:
            self.StatefulSetCondition = []
            for item in params.get("StatefulSetCondition"):
                obj = StatefulSetCondition()
                obj._deserialize(item)
                self.StatefulSetCondition.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        