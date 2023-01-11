import hashlib
import os
import sys
from pathlib import Path
from typing import Dict, List, Union

from assertpy import assert_that

from deepdriver.sdk.chart.chart import Chart
from deepdriver.sdk.data_types.image import Image
from deepdriver.sdk.data_types.run import get_run
from deepdriver.sdk.data_types.table import Table
from deepdriver.sdk.interface import interface
from deepdriver.sdk.interface.grpc_interface_pb2 import ArtifactEntry as grpc_ArtifactEntry


class ArtifactEntry:

    def __init__(self, path: str, local_path: str, size: int, digest: str, status: str, lfs_yn: str, repo_tag: str,
                 type: str, metadata: str, key: str = ""):
        assert_that(path).is_not_none()
        assert_that(local_path).is_not_none()

        self.path = path  # path는 서버에 전송될 경로
        self.local_path = local_path  # local_path는 artifact.add()를 통해서 추가된 파일의 로컬 경로
        self.size = size  # 파일의 사이즈
        self.digest = digest  # 파일의 digest 값
        self.status = status  # 파일의 상태(로컬과의 비교)
        self.lfs_yn = lfs_yn
        self.repo_tag = repo_tag
        self.type = type
        self.metadata = metadata
        self.key = key

    # ArtifactEntry 객체를 기반으로 파일 다운로드 수행
    def download(self, local_root_path: str, artifact_id: int, team_name: str, exp_name: str, artifact_name: str,
                 artifact_type: str, versioning: str, file_index: int, total_file_count: int):
        assert_that(local_root_path).is_not_none()
        assert_that(artifact_id).is_not_none()

        local_path = os.path.join(local_root_path, self.repo_tag, self.path)
        if sys.platform.startswith('win32'):
            # 윈도우인 경우 Path Seperator를 리눅스 형식으로 강제로 변경함
            local_path = local_path.replace("\\", "/")
        i_last_separator = len(local_path) - local_path[::-1].find("/") - 1
        Path(local_path[:i_last_separator]).mkdir(parents=True, exist_ok=True)

        interface.download_file(self.path, artifact_id, local_path, team_name, exp_name, artifact_name, artifact_type,
                                versioning, self.lfs_yn, self.repo_tag, file_index, total_file_count, self.size)
        # 다운로드 후 파일의 digest 확인
        with open(local_path, "rb") as f:
            downloaded_file_digest = hashlib.md5(f.read()).hexdigest()
        if self.digest != downloaded_file_digest:
            raise Exception(
                f"file check sum error : checksum value are '{self.digest}' expected, but '{downloaded_file_digest}'")

        # 다운로드 완료 후 local_path 설정
        self.local_path = local_path

    # ArtifactEntry 객체를 기반으로 파일 업로드 수행
    def upload(self, upload_type: str, root_path: str, run_id: int, artifact_id: int, last_file_yn: str, team_name: str,
               exp_name: str, run_name: str, artifact_name: str, artifact_type: str, artifact_digest: str,
               entry_list: List[grpc_ArtifactEntry], file_index: int) -> bool:
        assert_that(root_path).is_not_none()
        assert_that(run_id).is_not_none()
        assert_that(artifact_id).is_not_none()
        assert_that(last_file_yn).is_not_none()
        assert_that(artifact_digest).is_not_none()
        assert_that(entry_list).is_not_none()
        if self.local_path:
            return interface.upload_file(upload_type, self.local_path, root_path, self.path, run_id, artifact_id,
                                         last_file_yn, team_name, exp_name, run_name, artifact_name, artifact_type,
                                         artifact_digest, self.digest, entry_list, file_index=file_index)
        else:
            return True

    def __str__(self) -> str:
        return str(self.__dict__)


# Artifact 객체에 추가되는 객체는 Image, 일반 파일, 폴더(하위 파일 포함), Table, 소스코드 등이 있다
class Artifacts:

    def __init__(self, name: str, type: str, id: int = 0, desc: str = None, versioning: str = "Y",
                 meta_data: Dict = None, entry_list: List[ArtifactEntry] = None) -> None:
        assert_that(name).is_not_none()
        assert_that(type).is_not_none()

        self.name = name
        self.type = type
        self.id = id
        self.desc = desc
        self.versioning = versioning
        self.run = get_run()

        # 메타정보 (for 모델 or 코드)
        # Ai 학습 모델과 같은 데이터가 아티펙트로 추가될 때 추가정보( 하이퍼파라미터)도 같이 기록되기위한 meta_data 정보
        self.meta_data: Dict = meta_data if meta_data else {}

        # ArtifactEntry 의 list
        # Artifacts.add() 함수로 데이터가 추가될때마다 리스트에 추가됨
        self.entry_list: List[ArtifactEntry] = entry_list if entry_list else []

    # 해당 Artifacts의 파일을 다운로드 후에 key에 해당하는 객체를 찾아 객체로 복원해서 반환
    def get(self, key: str = None) -> Union[str, Table, Image, Chart]:
        self.download()
        try:
            artifact_entry = next(item for item in self.entry_list if item.key == key)
        except StopIteration as e:
            raise Exception(f"Cannnot find Entry by Key: key=[{key}]")

        if artifact_entry.type == "TABLE":
            return Table.from_file(artifact_entry.local_path)
        if artifact_entry.type == "IMAGE":
            return Image(artifact_entry.local_path)
        if artifact_entry.type == "CHART":
            return Chart.from_file(artifact_entry.local_path)

    # 해당 Artifact에 데이터를 추가하는 함수
    # obj 및 파일 내용이 추가되면 임시 파일로 저장후 path를 추가한다
    # 추가된 각 항목에 대해서 ArtifactEntry를 생성한 후 Artifact가 가진 ArtifactEntry list에 추가함
    # name: 아티펙트에 각 엔트리의 식별자로 기록될 이름
    # data: 아티펙트에 추가될 데이터( Table  | Image | chart | file name | directory path | reference url )
    def add(self, data: Union[str, Table, Image, Chart], name: str = None) -> None:
        if isinstance(data, str):
            # if data is file_path
            data = os.path.relpath(data)  # Convert any path to a relative path
            data = os.path.join(".", data)  # Prefix with a dot
            self.__add_file(data, name)
            # local 파일의 존재여부를 판단하여 "DELETE" 상태로 마킹
            self.__local_path_sync_for_delete()
        elif isinstance(data, Table):
            # if data is Table
            assert_that(name).is_not_none()
            # TODO: local_path?
            local_path = os.path.join(".", data.get_path(name))
            digest, size = data.file_dump(local_path)
            self.entry_list.append(
                ArtifactEntry(path=data.get_path(name), local_path=local_path, size=size, digest=digest, status="ADD",
                              lfs_yn="", repo_tag="", type="TABLE", metadata=data.to_json(name), key=name))
        elif isinstance(data, Image):
            assert_that(name).is_not_none()
            local_path = data.local_path
            digest = data.get_digest()
            size = data.get_size()
            self.entry_list.append(
                ArtifactEntry(path=data.get_path(name), local_path=local_path, size=size, digest=digest, status="ADD",
                              lfs_yn="", repo_tag="", type="IMAGE", metadata=data.to_json(name), key=name))
        elif isinstance(data, Chart):
            assert_that(name).is_not_none()
            # TODO: local_path?
            local_path = os.path.join(".", data.get_path(name))
            digest, size = data.file_dump(local_path)
            self.entry_list.append(
                ArtifactEntry(path=data.get_path(name), local_path=local_path, size=size, digest=digest, status="ADD",
                              lfs_yn="", repo_tag="", type="CHART", metadata=data.to_json(name), key=name))

    def __add_file(self, data: Union[str], name: str = None, depth: int = 0) -> None:
        # data에 str가 들어오면 file 인지, dir 인지 reference url(http:// or s3:// ..) 인지 체크
        if isinstance(data, str):
            if not os.path.isfile(data):
                # dir인경우 하위 파일을 순회하며 위의 과정 반복
                dir_path = data
                for file_dir_name in os.listdir(dir_path):
                    file_dir_path = os.path.join(dir_path, file_dir_name)
                    # add시 name이 지정된 경우: name/하위폴더명/파일명
                    # add시 name이 지정되지 않은 경우: 하위폴더명/파일명
                    target_name = file_dir_name if depth == 0 and not name else name
                    self.__add_file(file_dir_path, target_name, depth + 1)
            else:
                # file인경우 ArtifactEntry 생성후 local_path, path,size, digest등을 설정한 후 Artifact의 entry_list에 추가
                local_path = data
                fd_names = local_path.split(os.path.sep)
                for i, fd_name in enumerate(fd_names):
                    if fd_name == name:
                        fd_names = fd_names[i:]
                        break
                path = os.path.join(*fd_names)
                if sys.platform.startswith('win32'):
                    # 윈도우인 경우 Path Seperator를 리눅스 형식으로 강제로 변경함
                    path = path.replace("\\", "/")
                size = os.stat(local_path).st_size
                with open(local_path, "rb") as f:
                    local_file_digest = hashlib.md5(f.read()).hexdigest()

                entry = self.__find_entry_by_path(local_path, path)
                if entry:
                    entry.status = "SYNC"  # 변경이 없는 경우
                    if entry.digest != local_file_digest:   # local의 root 경로가 바껴서 파일명은 동일하지만, 파일내용이 바뀐경우
                        entry.local_path = local_path
                        entry.digest = local_file_digest
                        entry.size = size
                else:
                    self.entry_list.append(
                        ArtifactEntry(path, local_path, size, local_file_digest, status="ADD", lfs_yn="", repo_tag="", type="FILE",
                                      metadata=""))  # 파일이 추가된 경우

    def __local_path_sync_for_delete(self) -> None:
        # local에서 삭제된 파일의 status를 "DELETE"로 변경
        for entry in self.entry_list:
            if entry.status == "ADD":  # 상태가 "ADD"인 entry만 확인
                if not os.path.isfile(entry.local_path):
                    entry.status = "DELETE"

    def __find_entry_by_path(self, local_path: str, path: str) -> ArtifactEntry:
        for entry in self.entry_list:
            if not entry.local_path:  # download()를 실행하지 않은 경우 local_path가 ""이므로 entry.path에서 비교
                if entry.path == path:
                    return entry

            if entry.local_path == local_path:
                return entry
        else:
            return None

    # Artifact의 정보를 전송하고, ArtifactEntry 각각의 파일을 전송한다
    def upload(self) -> bool:
        # Interface.py의 upoad_artifact ( grpc_interface.py의 upoad_artifact)를 호출 하여 artifact 정보에 대해 전송
        entry_dict = {entry.path: entry for entry in self.entry_list}
        entry_list: List(grpc_ArtifactEntry) = []
        hasher = hashlib.md5()
        # TODO: 상태에 따라서 status 변경
        for entry_path, entry in sorted(entry_dict.items()):
            entry_list.append(grpc_ArtifactEntry(
                path=entry_path,
                digest=entry.digest,
                size=entry.size,
                status="ADD",
                key=entry.key,
                type=entry.type,
                metadata=entry.metadata,
            ))
            hasher.update(f"{entry_path}:{entry.digest}\n".encode())
        artifact_digest = hasher.hexdigest()
        id = interface.upload_artifact(self.run.run_id, self, artifact_digest, self.run.team_name, self.run.exp_name,
                                       entry_list)
        if id is None:
            return False
        self.id = id

        # artifact에 추가된 파일들(ArtifactEntry의 파일)은 각각의 upload함수 호출
        for i, entry in enumerate(self.entry_list):
            # ArtifactEntry.upload() 호출시 인자로서 파일이 저장될 폴더 정보를 넘겨줌
            root_path = os.path.join(str(self.run.run_id), "artifact", self.type, self.name)
            last_file_yn = "Y" if i == len(self.entry_list) - 1 else "N"
            if self.versioning == "Y":
                upload_type = "ARTI_REPO"
            else:
                upload_type = "ARTI_FILES"

            succeeded = entry.upload(upload_type, root_path, self.run.run_id, self.id, last_file_yn, self.run.team_name,
                                     self.run.exp_name, self.run.run_name, self.name, self.type, artifact_digest,
                                     entry_list, file_index=i)
            if not succeeded:
                return False
        return True

    # Artifact 객체를 기반으로 Artifact에 등록된 모든 엔트리의 다운로드 수행
    def download(self) -> str:
        local_root_path = self.get_download_dir(with_repo_tag=False)
        # Artifact 객체가 가진 entry_list 의  ArtifactEntry.download()를 각각 호출
        for idx, entry in enumerate(self.entry_list):
            entry.download(local_root_path, self.id, self.run.team_name, self.run.exp_name, self.name, self.type,
                           self.versioning, idx, total_file_count=len(self.entry_list))
        return local_root_path

    def get_download_dir(self, with_repo_tag: bool = True):
        # ./deepdriver/artifact/{artifact_id}/{tag} 폴더가 생성된다
        download_path = os.path.join(".", "deepdriver", "artifact", str(self.id))

        if with_repo_tag and len(self.entry_list) > 0:
            return os.path.join(download_path, self.entry_list[0].repo_tag)
        else:
            return download_path

    def __str__(self) -> str:
        return "[" + ",".join(str(entry) for entry in self.entry_list) + "]"
