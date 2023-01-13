import logging
import os
import threading

import mlflow
from waveletai._version import get_versions
from waveletai import constants, envs
from waveletai.backends.hosted_backend import HostedBackend
from waveletai.constants import ModelRegisterMode, Visibility, DataSource, FileExt, ModelSourceType
from waveletai.exceptions import InitFailed
from waveletai.sessions import Session
from waveletai.utils import MLflowModuleRegister, set_mlflow_tracing_waveletai_store

logging.basicConfig(format='[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    level=logging.INFO)

_logger = logging.getLogger(__name__)

__lock = threading.RLock()

""""Access as an anonymous user.
You can pass this value as api_token during init() call, either by an environment variable or passing it directly
"""
ANONYMOUS = constants.ANONYMOUS
"""Anonymous user API token.
You can pass this value as api_token during init() call, either by an environment variable or passing it directly
"""
ANONYMOUS_API_TOKEN = constants.ANONYMOUS_API_TOKEN

__version__ = get_versions()

_backend = None


def init(backend=None, api_token=None, internal_login=True):
    with __lock:
        global _backend

        if backend is None:
            # backend_name = os.getenv(envs.BACKEND)
            # if backend_name == 'offline':
            #     backend = OfflineBackend()

            # elif backend_name is None:
            _backend = HostedBackend(api_token, internal_login=internal_login)

            # else:
            #     raise InvalidBackend(backend_name)
        return _backend
        # session = Session(backend=backend)
        # return session


def _get_backend():
    global _backend
    if _backend:
        return _backend
    if _backend is None and os.getenv(envs.API_TOKEN):
        return init()
    else:
        raise InitFailed()


def close():
    global _backend
    if _backend:
        _backend.close()


def set_app(app_id):
    """
    设置app_id
    :param app_id:
    :return:
    """
    return _get_backend().set_app(app_id)


def set_model(model_id):
    """
    设置model_id
    :param model_id:
    :return:
    """
    return _get_backend().set_model(model_id)


def create_app(name, tags, desc=None, visibility=Visibility.PRIVATE.value):
    """
    创建应用
    :param name :str 应用名称
    :param tags :list 应用标签
    :param desc :str 应用说明
    :param visibility: 公有私有 public private 默认 private
    :return: App对象
    """
    return _get_backend().create_app(name, tags, desc, visibility)


def update_app(name, tags, desc=None):
    """
    更改应用
    :param name :str 应用名称
    :param tags :list 应用标签
    :param desc :str 应用说明
    :return: App对象
    """
    return _get_backend().update_app(name, tags, desc)


def delete_app():
    """
    删除应用
    """
    return _get_backend().delete_app()


def get_app():
    """
    获取应用
    :return: App对象
    """
    return _get_backend().get_app()


def create_dataset(name, path, data_type=constants.DataType.TYPE_FILE.value, visibility=Visibility.PRIVATE.value,
                   desc=None, label_type=None):
    """
    创建数据集
    :param name: 数据集名称
    :param path: 要上传的本地数据的路径
    :param data_type: 一个数据集中的数据类型是唯一的。备选值constants.DataType，固定提供图片、文件、视频、视频帧的数据类型
    :param visibility: 可见性，默认为私有
    :param desc: 数据集详情
    :return: Dataset对象
    """
    return _get_backend().create_dataset(name, path, data_type, visibility, desc, label_type)


def get_dataset(dataset_id):
    """
    获取数据集对象
    :param dataset_id:数据集ID
    :return: Dataset对象
    """
    return _get_backend().get_dataset(dataset_id)


def download_dataset_artifact(dataset_id, path, destination):
    """
    下载数据集指定文件或目录到本地
    :param dataset_id:数据集ID
    :param path:当前文件或文件路径在数据集目录的相对位置, eg 下载单个文件: data/test.csv, 下载data文件夹: data
    :param destination:本地存储路径
    :return:
    """
    return _get_backend().download_dataset_artifact(dataset_id, path, destination)


def download_dataset_artifacts(data_id, destination, unzip=False, feature_type=None):
    """
    下载数据集/特征库全部文件到本地指定目录
    :param data_id:数据集ID/特征库ID
    :param destination:本地存储路径
    :param unzip:仅当当前数据ID为特征库ID时生效，是否自动解压zip数据，默认为不解压
    :param imgtype: 特征库图片类型 pascal_voc/coco
    :return:
    """
    return _get_backend().download_dataset_artifacts(data_id, destination, unzip, feature_type)


def download_data(dataset_id, path="raw_data.csv", destination_dir=None, datasource=DataSource.MAMMUT.value,
                  fileext=FileExt.CSV.value, query=None):
    """
        当dataset仅为外部数据引用时，下载对应源的rawdata
        :param path to the file to be downloaded. path=raw_data.csv
        :param destination_dir (:obj:`str`): default current dir
        :param datasource (:obj:`str`): Constants.DataSource 数据来源,默认MAMMUT,网易猛犸
        :param fileext (:obj:`str`): Constants.FileExt 文件保存格式，默认csv
        :param query (:obj:`dict`): 自定义参数,当为{}时，将使用数据的默认参数请求数据
        Examples:
             .. code:: python3

                dataset.download_data()

                dataset.download_data(path='raw_data.csv',destination_dir='dataset/'
                   query={"page_num":1,"startTime":"2021-08-25","endTime":"2021-08-26","page_size":3000})
        """
    if query is None:
        query = {}
    return _get_backend().download_data(dataset_id, path, destination_dir, datasource, fileext, query)


def upload_dataset_artifacts(dataset_id, path):
    """
    上传数据集资产文件
    :param dataset_id: 文件所属数据集
    :param path: 要上传的文件夹/文件路径
    :return:  上传文件 succ，共xxx个
    """
    return _get_backend().upload_dataset_artifacts(dataset_id, path)


def create_model(name, desc=None, git_url=None, http_url=None, visibility=Visibility.PRIVATE.value, source=ModelSourceType.GITCODE.value):
    """
    创建模型
    :param visibility: 公有私有 public private 默认 private
    :param http_url: http地址 默认空
    :param git_url: git地址 默认空
    :param auth_id: auth_id 默认空
    :param name:模型名称
    :param desc:模型备注 默认空
    :param source:模型来源 flow:画布 gitcode:git代码
    :return:
    """
    return _get_backend().create_model(name, desc, git_url, http_url, visibility, source)


def get_model():
    """
    获取模型对象
    :return:
    """
    return _get_backend().get_model()


def register_model_version(desc, artifacts, mode=ModelRegisterMode.PYFUNC.value, json_data=None):
    """
    注册模型库版本
    :param desc: 备注
    :param artifacts: 注册文件路径，可以是文件夹,当为docker模式时，此处为docker-image,可以用save命令导出  eg：deployment.tar
    :param mode: 注册模式,默认为自定义(ModelRegisterMode.PYFUNC.value)
    :param json_data: 模型版本其他信息
    :return:
    """
    return _get_backend().register_model_version(desc, artifacts, mode, json_data)


def get_model_version_by_model(version):
    """
    过模型获取模型库指定信息
    :param version:模型版本号
    :return:
    """
    return _get_backend().get_model_version(version)


def get_model_version_by_id(model_version_id):
    """
    通过模型库ID获取模型库指定信息
    :param model_version_id:模型库ID
    :return:
    """
    return _get_backend().get_repo_by_repo_id(model_version_id)


def list_models():
    """
    获取模型对象
    :return:
    """
    return _get_backend().list_models()


def update_dataset(dataset_id, name, zone, desc=None, label_type=None):
    """
    更新数据集id
    :param dataset_id:
    :param name:
    :param zone:
    :param desc:
    :return:
    """
    return _get_backend().update_dataset(dataset_id, name, zone, desc, label_type)


def delete_dataset(dataset_id):
    """
    删除数据集
    :param dataset_id:
    :return:
    """
    return _get_backend().delete_dataset(dataset_id)


def update_model(name, visibility, desc=None):
    """
    更新模型集
    :param name:
    :param desc:
    :param visibilty:
    :return:
    """
    return _get_backend().update_model(name, visibility, desc)


def delete_model():
    """
    删除模型
    :return:
    """
    return _get_backend().delete_model()


def list_model_versions(page=1, pagesize=10):
    """
    获取注册的各版本模型信息列表
    :return:
    """
    return _get_backend().list_model_versions(page, pagesize)


def abandon_model_version(version):
    """
    根据模型id，删除指定version
    :param version:
    :return:
    """
    return _get_backend().abandon_model_version(version)


def update_model_version(version, desc=None):
    """
    根据模型id，修改指定模型版本
    :param desc:
    :param version:
    :return:
    """
    return _get_backend().update_model_version(version, desc)


def list_experiments():
    """
    根据模型id，获取实验数据
    :return:
    """
    return _get_backend().list_experiments()


def download_model_version_asset(repo_id, path, destination):
    """
    根据repo_id下载指定path(文件或文件夹)到本地的destination
    :param repo_id:
    :param path:
    :param destination:
    :return:
    """
    return _get_backend().download_model_version_asset(repo_id, path, destination)


def download_model_version_artifacts(repo_id, destination):
    """
    根据repo_id下载全部文件到本地的destination
    :param repo_id:
    :param destination:
    :return:
    """
    return _get_backend().download_model_version_artifacts(repo_id, destination)


def list_model_releases(version):
    """
    根据模型id，版本，获取发布数据
    :param version: 默认为None
    :return:
    """
    return _get_backend().list_model_releases(version)


def list_model_releases_by_repo(repo_id):
    """
    查询当前模型版本的发布服务列表
    :param repo_id:
    :return:
    """
    return _get_backend().list_model_releases_by_repo(repo_id)


def create_experiment(name, desc=None):
    """
    创建实验
    :param name:模型名称
    :param desc:模型备注
    :param params: 参数字典{key:value, ...}
    :return:
    """
    return _get_backend().create_experiment(name=name, params=None, host_id=None,
                                            dataset_id=None, feature_id=None, is_train=True, desc=desc,
                                            mlexp_id=None, artifact_location=None, online_train=False,
                                            docker_args={})


@set_mlflow_tracing_waveletai_store
def get_experiment(experiment_id):
    """
    获取实验对象
    :param experiment_id:实验ID
    :return:
    """
    return _get_backend().get_experiment(experiment_id)


def get_experiment_by_mlflow_experiment(experiment_id):
    """
    根据mlexperiment id 查询wai experiment
    :return:
    """
    return _get_backend().get_experiment_by_mlflow_experiment(experiment_id)


def get_experiment_by_mlflow_run(run_id):
    """
    根据mlrun id 查询wai experiment
    :param run_id:
    :return:
    """
    return _get_backend().get_experiment_by_mlflow_run(run_id)


@set_mlflow_tracing_waveletai_store
def log_metric(key, value, step=None):
    """
    记录实验标量
    :param key:
    :param value:
    :param step:
    :return:
    """
    return mlflow.log_metric(key, value, step)


@set_mlflow_tracing_waveletai_store
def log_metrics(metrics, step=None):
    """
    批量记录实验标量
    :param metrics: Dict[str, float]
    :param step:
    :returns:
    """
    return mlflow.log_metrics(metrics, step)


@set_mlflow_tracing_waveletai_store
def log_param(key, value):
    """
    记录实验参数
    :param key:
    :param value:
    :return:
    """
    return mlflow.log_param(key, value)


@set_mlflow_tracing_waveletai_store
def log_params(params):
    """
    批量记录参数
    :param params: Dict[str, Any]
    :return:
    """
    return mlflow.log_params(params)


@set_mlflow_tracing_waveletai_store
def set_tag(key, value):
    """
    记录标签
    :param key:
    :param value:
    :return:
    """
    return mlflow.set_tag(key, value)


@set_mlflow_tracing_waveletai_store
def set_tags(tags):
    """
    批量记录标签
    :param tags: Dict[str, Any]
    :return:
    """
    return mlflow.set_tags(tags)


def upload_artifact(local_file, artifact_path, run_id):
    """
    上传模型文件
    :param local_file:
    :param artifact_path:
    :param run_id:
    :return:
    """
    return _get_backend().upload_artifact(local_file, artifact_path, run_id)


@set_mlflow_tracing_waveletai_store
def log_batch(metrics=None, params=None, tags=None):
    """
    批量上传 metric param tag
    :param metrics:
    :param params:
    :param tags:
    :return:
    """
    if metrics is None:
        metrics = []
    if params is None:
        params = []
    if tags is None:
        tags = []
    from mlflow.tracking.fluent import _get_or_start_run, MlflowClient
    run_id = _get_or_start_run().info.run_id
    MlflowClient().log_batch(run_id, metrics, params, tags)
    _logger.warning(f'成功记录metric {len(metrics)}个, param {len(params)}个, tag {len(tags)}个')


@set_mlflow_tracing_waveletai_store
def log_artifact(local_path: str, artifact_path=None):
    """
    上传artifact
    :param local_path:
    :param artifact_path:
    :return:
    """
    return mlflow.log_artifact(local_path=local_path, artifact_path=artifact_path)


@set_mlflow_tracing_waveletai_store
def log_artifacts(local_dir: str, artifact_path=None):
    """
    上传artifact文件夹
    :param local_dir:
    :param artifact_path:
    :return:
    """
    return mlflow.log_artifacts(local_dir=local_dir, artifact_path=artifact_path)


@set_mlflow_tracing_waveletai_store
def auto_log(log_input_examples: bool = False,
             log_model_signatures: bool = True,
             log_models: bool = True,
             disable: bool = False,
             exclusive: bool = False,
             disable_for_unsupported_versions: bool = False,
             silent: bool = False):
    """
    上传artifact文件夹
     :param log_input_examples: If ``True``, input examples from training datasets are collected and
                               logged along with model artifacts during training. If ``False``,
                               input examples are not logged.
                               Note: Input examples are MLflow model attributes
                               and are only collected if ``log_models`` is also ``True``.
    :param log_model_signatures: If ``True``,
                                 :py:class:`ModelSignatures <mlflow.models.ModelSignature>`
                                 describing model inputs and outputs are collected and logged along
                                 with model artifacts during training. If ``False``, signatures are
                                 not logged. Note: Model signatures are MLflow model attributes
                                 and are only collected if ``log_models`` is also ``True``.
    :param log_models: If ``True``, trained models are logged as MLflow model artifacts.
                       If ``False``, trained models are not logged.
                       Input examples and model signatures, which are attributes of MLflow models,
                       are also omitted when ``log_models`` is ``False``.
    :param disable: If ``True``, disables all supported autologging integrations. If ``False``,
                    enables all supported autologging integrations.
    :param exclusive: If ``True``, autologged content is not logged to user-created fluent runs.
                      If ``False``, autologged content is logged to the active fluent run,
                      which may be user-created.
    :param disable_for_unsupported_versions: If ``True``, disable autologging for versions of
                      all integration libraries that have not been tested against this version
                      of the MLflow client or are incompatible.
    :param silent: If ``True``, suppress all event logs and warnings from MLflow during autologging
                   setup and training execution. If ``False``, show all events and warnings during
                   autologging setup and training execution.
    :return:
    """
    return mlflow.autolog(log_input_examples,
                          log_model_signatures,
                          log_models,
                          disable,
                          exclusive,
                          disable_for_unsupported_versions,
                          silent)
