import boto3
import cv2
import obs

from . import constants
from .decorator import args_log
from .loggings import logger


class ObjectStorage(object):
    def __init__(self, app_config):
        self.app_config = app_config
        self.path_dict = constants.OBJECT_STORAGE_PATHS
        self.path_dict_temp = constants.OBJECT_STORAGE_PATHS_TEMP
        self.allow_file_size_dict = constants.OBJECT_STORAGE_ALLOW_FILE_SIZE
        self.allow_file_size_default = (
            constants.OBJECT_STORAGE_ALLOW_FILE_SIZE_DEFAULT)
        self.file_format_whitelist = (
            constants.OBJECT_STORAGE_FILE_FORMAT_WHITELIST)

        self.bucket_obs = app_config.get("obs/bucket")
        self.bucket_s3 = app_config.get("s3/bucket")

        self.path_prefix_obs = app_config.get("obs/path-prefix")
        self.path_prefix_s3 = app_config.get("s3/path-prefix")

        self.base_url_obs = app_config.get("obs/base-url")
        self.base_url_s3 = app_config.get("s3/base-url")

        self.base_url_raw_obs = app_config.get("obs/base-url-raw")
        self.base_url_raw_s3 = app_config.get("s3/base-url-raw")

        self.video_base_url_obs = app_config.get("obs/video-base-url")
        self.video_base_url_s3 = app_config.get("s3/video-base-url")

        self.content_type = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "png": "image/png",
            "ico": "image/x-icon",
            "pdf": "application/pdf",
            "doc": ("application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"),
            "docx": ("application/vnd.openxmlformats-officedocument."
                     "wordprocessingml.document"),
            "mp4": "video/mp4",
            "xls": "application/vnd.ms-excel",
            "xlsx": ("application/vnd.openxmlformats-officedocument."
                     "spreadsheetml.sheet"),
            "txt": "text/plain"
        }

    @property
    def client_s3(self):
        return boto3.client(
            's3', region_name=self.app_config.get("s3/region"),
            aws_access_key_id=self.app_config.get("s3/key"),
            aws_secret_access_key=self.app_config.get("s3/secret"))

    @property
    def client_obs(self):
        return obs.ObsClient(
            access_key_id=self.app_config.get("obs/access_key_id"),
            secret_access_key=self.app_config.get("obs/secret_access_key"),
            server=self.app_config.get("obs/server_url"))

    def parse_file_key_of_obs(self, url):
        return url.replace(
            self.base_url_obs.replace("{file}", ""), "").replace(
                self.base_url_raw_obs.replace("{file}", ""), "")

    def parse_file_key_of_s3(self, url):
        return url.replace(
            self.base_url_s3.replace("{file}", ""), "").replace(
                self.base_url_raw_s3.replace("{file}", ""), "")

    @args_log()
    def parse_file_key(self, system, url):
        return {
            constants.OBJECT_STORAGE_SYSTEM_OBS: self.parse_file_key_of_obs,
            constants.OBJECT_STORAGE_SYSTEM_S3: self.parse_file_key_of_s3
        }[system](url)

    @args_log()
    def _check_resource_file(
            self, resource_name, file_name, binary_content=None):
        if resource_name not in list(self.path_dict.keys()):
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg="The resource name is invalid.")
        # 验证文件类型
        file_format = file_name.split(".")[-1]
        allow_file_format = self.file_format_whitelist.get(resource_name, ())
        if not file_name or file_format not in allow_file_format:
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg="This file type is not supported.")
        if not binary_content:
            return
        # 验证文件大小
        allow_file_size = self.allow_file_size_dict.get(
            resource_name, self.allow_file_size_default)
        content_size = float(len(binary_content)) / 1024**2
        if content_size > allow_file_size:
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg="The file size is too large.")

    @args_log()
    def _get_video_screenshot_bytes(self, video_name):
        vc = cv2.VideoCapture(video_name)  # pylint: disable=no-member
        if not vc.isOpened():
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg="Not a qualified video file.")
        frames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))  # pylint: disable=no-member
        # fps = vc.get(cv2.CAP_PROP_FPS)  # 视频帧率
        # duration = frames / fps  # 视频时长
        if frames < 10:
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg="Not a qualified video file.")
        currentframe = 1
        while True:
            res, frame = vc.read()
            if res:
                if currentframe == 10:  # 取第10帧图片
                    _, jpeg = cv2.imencode('.jpg', frame)
                    jb = jpeg.tobytes()
                    vc.release()
                    return jb
                currentframe += 1
            else:
                break
        vc.release()

    @args_log()
    def upload_file_to_obs(
            self, path, file_name, binary_content, path_kargs=None):
        try:
            # 填充路径前缀, 填充路径参数
            if path_kargs is not None:
                path = path.format(prefix=self.path_prefix_obs, **path_kargs)
            else:
                path = path.format(prefix=self.path_prefix_obs)
            name_suffix = file_name.split('.')[-1].lower()
            _object_key = "{}/{}".format(path, file_name)
            _object_url = self.base_url_raw_obs.format(file=_object_key)
            _headers = obs.PutObjectHeader(
                contentType=self.content_type[name_suffix]
            )
            self.client_obs.putContent(
                self.bucket_obs, _object_key, content=binary_content,
                headers=_headers)
        except Exception as err:
            logger.exception(err)
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg=str(err))
        return {"objectKey": _object_key, "objectUrl": _object_url}

    def upload_file_to_s3(
            self, path, file_name, binary_content=None, path_kargs=None):
        try:
            # 填充路径前缀, 填充路径参数
            if path_kargs is not None:
                path = path.format(prefix=self.path_prefix_s3, **path_kargs)
            else:
                path = path.format(prefix=self.path_prefix_s3)
            name_suffix = file_name.split('.')[-1].lower()
            _object_key = "{}/{}".format(path, file_name)
            _object_url = self.base_url_raw_s3.format(file=_object_key)
            resp = self.client_s3.put_object(
                Bucket=self.bucket_s3, Key=_object_key,
                Body=binary_content, ContentType=self.content_type[name_suffix])
            print(resp)
        except Exception as err:
            logger.exception(err)
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg=str(err))
        return {"objectKey": _object_key, "objectUrl": _object_url}

    @args_log()
    def upload_file(
            self, system, resource_name, file_name, binary_content,
            is_temp=None, path_kargs=None):
        # 统一将文件名小写
        file_name = file_name.lower()
        # 检查文件类型
        self._check_resource_file(resource_name, file_name, binary_content)
        # 判断是否临时文件
        if is_temp is True:
            path = self.path_dict_temp.get(resource_name)
            if not path:
                raise DEF_EXCEPTIONS.InvalidOperationException(
                    code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                    msg="未配置临时文件路径, 请联系管理.")
        else:
            path = self.path_dict.get(resource_name)

        # 根据system参数不同选择不同的上传方法
        upload_method = {
            constants.OBJECT_STORAGE_SYSTEM_OBS: self.upload_file_to_obs,
            constants.OBJECT_STORAGE_SYSTEM_S3: self.upload_file_to_s3
        }[system]
        result = upload_method(path, file_name, binary_content, path_kargs)

        _object_url = result["objectUrl"]
        # 如果是视频, 存视频展示图
        if resource_name.find('video') != -1:
            video_img = self._get_video_screenshot_bytes(_object_url)
            try:
                upload_method(
                    path=path,
                    file_name='{}{}'.format(file_name.split('.')[0], '.jpg'),
                    binary_content=video_img, path_kargs=path_kargs)
            except Exception as err:
                logger.exception(err)
                raise DEF_EXCEPTIONS.InvalidOperationException(
                    code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                    msg=str(err))
        return result

    @args_log()
    def confirm_temp_file_in_obs(self, resource, temp_obj_key, path_kargs=None):
        # 如果temp_obj_key是http开头的, 直接返回
        temp_obj_key = self.parse_file_key_of_obs(temp_obj_key)
        if temp_obj_key.startswith("http"):
            return temp_obj_key
        # 处理文件在临时目录和正式目录的路径
        temp_path = self.path_dict_temp.get(resource)
        path = self.path_dict.get(resource)
        if path_kargs is not None:
            temp_path = temp_path.format(
                prefix=self.path_prefix_obs, **path_kargs)
            path = path.format(
                prefix=self.path_prefix_obs, **path_kargs)
        else:
            temp_path = temp_path.format(prefix=self.path_prefix_obs)
            path = path.format(prefix=self.path_prefix_obs)
        obj_key = temp_obj_key.replace(temp_path, path)
        # 检测文件在正式目录是否存在, 若存在则直接返回
        res = self.client_obs.getObjectMetadata(self.bucket_obs, obj_key)
        if res.status == 200:
            return obj_key
        # 从临时目录复制一份到正式目录
        resp = self.client_obs.copyObject(
            sourceBucketName=self.bucket_obs, sourceObjectKey=temp_obj_key,
            destBucketName=self.bucket_obs, destObjectKey=obj_key)
        if resp.status >= 300:
            logger.error(str(resp))
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg=str(resp.reason))
        # 如果是视频, 转存视频展示图
        if resource.find('video') != -1:
            temp_video_img_obj_key = temp_obj_key.replace("mp4", "jpg")
            video_img_obj_key = obj_key.replace("mp4", "jpg")
            resp = self.client_obs.copyObject(
                sourceBucketName=self.bucket_obs,
                sourceObjectKey=temp_video_img_obj_key,
                destBucketName=self.bucket_obs,
                destObjectKey=video_img_obj_key)
            if resp.status >= 300:
                logger.error(str(resp))
                raise DEF_EXCEPTIONS.InvalidOperationException(
                    code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                    msg=str(resp.reason))
        return obj_key

    @args_log()
    def confirm_temp_file_in_s3(self, resource, temp_obj_key, path_kargs=None):
        # 如果temp_obj_key是http开头的, 直接返回
        temp_obj_key = self.parse_file_key_of_s3(temp_obj_key)
        if temp_obj_key.startswith("http"):
            return temp_obj_key
        # 处理文件在临时目录和正式目录的路径
        temp_path = self.path_dict_temp.get(resource)
        path = self.path_dict.get(resource)
        if path_kargs is not None:
            temp_path = temp_path.format(
                prefix=self.path_prefix_s3, **path_kargs)
            path = path.format(
                prefix=self.path_prefix_s3, **path_kargs)
        else:
            temp_path = temp_path.format(prefix=self.path_prefix_s3)
            path = path.format(prefix=self.path_prefix_s3)
        obj_key = temp_obj_key.replace(temp_path, path)
        # 检测文件在正式目录是否存在, 若存在则直接返回
        try:
            self.client_s3.get_object(Bucket=self.bucket_s3, Key=obj_key)
            return obj_key
        except Exception:  # pylint: disable=broad-except
            pass
        # 从临时目录复制一份到正式目录
        try:
            copy_source = {"Bucket": self.bucket_s3, "Key": temp_obj_key}
            self.client_s3.copy_object(
                Bucket=self.bucket_s3, Key=obj_key, CopySource=copy_source)
        except Exception as err:
            raise DEF_EXCEPTIONS.InvalidOperationException(
                code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                msg=str(err))
        # 如果是视频, 转存视频展示图
        if resource.find('video') != -1:
            temp_video_img_obj_key = temp_obj_key.replace("mp4", "jpg")
            video_img_obj_key = obj_key.replace("mp4", "jpg")
            copy_source = {"Bucket": self.bucket_s3, "Key": temp_video_img_obj_key}
            try:
                self.client_s3.copy_object(
                    Bucket=self.bucket_s3, Key=video_img_obj_key,
                    CopySource=copy_source)
            except Exception as err:
                raise DEF_EXCEPTIONS.InvalidOperationException(
                    code=DEF_EXCEPTIONS.CODE_UPLOAD_FILE_FAILED,
                    msg=str(err))
        return obj_key

    @args_log()
    def confirm_temp_file(
            self, system, resource, temp_obj_key, path_kargs=None):
        confirm_temp_file_mmthod = {
            constants.OBJECT_STORAGE_SYSTEM_OBS: self.confirm_temp_file_in_obs,
            constants.OBJECT_STORAGE_SYSTEM_S3: self.confirm_temp_file_in_s3
        }[system]
        try:
            return confirm_temp_file_mmthod(resource, temp_obj_key, path_kargs)
        except Exception:
            return self.confirm_temp_file_in_s3(
                resource, temp_obj_key, path_kargs)
