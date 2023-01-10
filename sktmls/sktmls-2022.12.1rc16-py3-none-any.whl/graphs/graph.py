from typing import Dict, Any, List

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSClientError, MLSResponse

MLS_VERTEX_API_URL = "/api/v1/vertices"
MLS_EDGE_API_URL = "/api/v1/edges"


class VertexSchema:
    """
    MLS Vertex 스키마 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (str) Vertex 스키마 ID
            - label: (str) Vertex 스키마 라벨
            - properties: (dict) Vertex property 데이터 타입 정의
        ## Returns
        `sktmls.graphs.VertexSchema`
        """
        self.id = kwargs.get("id")
        self.label = kwargs.get("label")
        self.properties = kwargs.get("properties")

    def get(self):
        return self.__dict__


class EdgeSchema:
    """
    MLS Edge 스키마 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (str) Edge 스키마 ID
            - label: (str) Edge 스키마 라벨
            - frm: (str) 출발 Vertex 라벨
            - to: (str) 도착 Vertex 라벨
            - properties: (dict) Edge property 데이터 타입 정의

        ## Returns
        `sktmls.graphs.EdgeSchema`
        """
        self.id = kwargs.get("id")
        self.label = kwargs.get("label")
        self.frm = kwargs.get("frm")
        self.to = kwargs.get("to")
        self.properties = kwargs.get("properties")

    def get(self):
        return self.__dict__


class VertexClient(MLSClient):
    """
    MLS Vertex 스키마 관련 기능들을 제공하는 클라이언트입니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.graphs.VertexClient`

        ## Example

        ```python
        vertex_client = VertexClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env, runtime_env, username, password)

    def create_vertex(self, label: str, properties: Dict[str, str] = {}) -> VertexSchema:
        """
        Vertex 스키마를 생성합니다.

        ## Args

        - label: (str) Vertex 스키마 라벨
        - properties: (optional) (dict) Vertex 스키마의 데이터 속성 (`Float(single)`|`Float(set)`|`String(single)`|`String(set)`)
            - Float, String: 데이터 타입
            - single: 단일 property 값을 계속 업데이트
            - set: property값을 여러 개 계속 누적해 저장

        ## Returns
        `sktmls.graphs.VertexSchema`

        ## Example

        ```python
        vertex = vertex_client.create_vertex(
            label="SampleVertex",
            properties={
                "name":"String(single)",
                "lat":"Float(single)",
                "long": "Float(single)"
            }
        )
        ```
        """

        for p in properties.values():
            assert p in ["Float(single)", "Float(set)", "String(single)", "String(set)"], "허용되지 않은 property 타입입니다."
        data = {"label": label}
        if properties:
            data["properties"] = properties
        return VertexSchema(**self._request(method="POST", url=f"{MLS_VERTEX_API_URL}", data=data).results)

    def list_vertices(self, **kwargs) -> List[VertexSchema]:
        """
        vertex 스키마 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) vertex 스키마 id
            - label: (str) vertex 스키마 라벨
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.graphs.VertexSchema`)

        ## Example

        ```python
        vertices = vertex_client.list_vertices()
        ```
        """
        response = self._request(method="GET", url=f"{MLS_VERTEX_API_URL}", params=kwargs).results
        return [VertexSchema(**vertex) for vertex in response]

    def get_vertex(self, id: int = None, label: str = None) -> VertexSchema:
        """
        단일 Vertex 스키마 정보를 가져옵니다.

        ## Args: `id` 또는 `label` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) vertex 스키마 id
        - label: (str) vertex 스키마 라벨

        ## Returns
        `sktmls.graphs.VertexSchema`

        ## Example

        ```python
        vertex = vertex_client.get_vertex(id=1)
        vertex = vertex_client.get_vertex(label="SampleVertex")
        ```
        """
        assert id or label, "`id` 또는 `label` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        vertices = self.list_vertices(id=id, label=label)
        if len(vertices) == 0:
            raise MLSClientError(code=404, msg="Vertex 스키마가 없습니다.")
        if len(vertices) > 1:
            raise MLSClientError(code=409, msg="Vertex 스키마가 여러개 존재합니다.")
        return vertices[0]

    def update_vertex(self, vertex: VertexSchema, label: str, properties: Dict[str, Any] = {}) -> VertexSchema:
        """
        단일 Vertex 스키마를 수정합니다.
        ## Args

        - vertex: (VertexSchema) Vertex 스키마 객체
        - label: (str) Vertex 스키마 라벨
        - properties: (optional) (dict) Vertex 스키마의 데이터 속성 (`Float(single)`|`Float(set)`|`String(single)`|`String(set)`)
            - Float, String: 데이터 타입
            - single: 단일 property 값을 계속 업데이트
            - set: property값을 여러 개 계속 누적해 저장

        ## Returns
        `sktmls.graphs.VertexSchema`

        ## Example

        ```python
        new_vertex = vertex_client.update_vertex(
            vertex,
            label="SampleVertex2",
            properties={
                "name":"String(single)"
            }
        )
        ```
        """
        for p in properties.values():
            assert p in ["Float(single)", "Float(set)", "String(single)", "String(set)"], "허용되지 않은 property 타입입니다."
        data = {"label": label}
        if properties:
            data["properties"] = properties
        return VertexSchema(**self._request(method="PUT", url=f"{MLS_VERTEX_API_URL}/{vertex.id}", data=data).results)

    def delete_vertex(self, vertex: VertexSchema) -> MLSResponse:
        """
        단일 Vertex 스키마를 삭제합니다. 연결된 Edge 스키마도 함께 삭제됩니다.

        ## Args

        - vertex: (VertexSchema) Vertex 스키마 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        vertex_client.delete_vertex(vertex)
        ```
        """
        assert type(vertex) == VertexSchema
        return self._request(method="DELETE", url=f"{MLS_VERTEX_API_URL}/{vertex.id}")


class EdgeClient(MLSClient):
    """
    MLS Edge 스키마 관련 기능들을 제공하는 클라이언트입니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV.LOCAL = None,
        username: str = None,
        password: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.graphs.EdgeClient`

        ## Example

        ```python
        edge_client = EdgeClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env, runtime_env, username, password)

    def create_edge(self, label: str, frm: str, to: str, properties: Dict[str, str] = {}) -> EdgeSchema:
        """
        Edge 스키마를 생성합니다.

        ## Args
        - label: (str) Edge 스키마 라벨
        - frm: (str) Edge 시작 Vertex 라벨
        - to: (str) Edge 종료 Vertex 라벨
        - properties: (optional) (dict) Vertex 스키마의 데이터 속성 (`Float(single)`|`Float(set)`|`String(single)`|`String(set)`)
            - Float, String: 데이터 타입
            - single: 단일 property 값을 계속 업데이트
            - set: property값을 여러 개 계속 누적해 저장

        ## Returns
        `sktmls.graphs.EdgeSchema`

        ## Example

        ```python
        edge = edge_client.create_edge(
            label="SampleEdge",
            frm="startVertex",
            to="endVertex",
            properties={
                "name":"String(single)",
                "lat":"Float(single)",
                "long": "Float(single)"
            }
        )
        ```
        """

        for p in properties.values():
            assert p in ["Float(single)", "Float(set)", "String(single)", "String(set)"], "허용되지 않은 property 타입입니다."
        data = {"label": label, "frm": frm, "to": to}
        if properties:
            data["properties"] = properties
        return EdgeSchema(**self._request(method="POST", url=f"{MLS_EDGE_API_URL}", data=data).results)

    def list_edges(self, **kwargs) -> List[EdgeSchema]:
        """
        Edge 스키마 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) Edge 스키마 id
            - label: (str) Edge 스키마 라벨
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.graphs.EdgeSchema`)

        ## Example

        ```python
        edges = edge_client.list_edges()
        ```
        """
        response = self._request(method="GET", url=f"{MLS_EDGE_API_URL}", params=kwargs).results
        return [EdgeSchema(**edge) for edge in response]

    def get_edge(self, id: int = None, label: str = None) -> EdgeSchema:
        """
        단일 Edge 스키마 정보를 가져옵니다.

        ## Args: `id` 또는 `label` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) Edge 스키마 id
        - label: (str) Edge 스키마 라벨

        ## Returns
        `sktmls.graphs.EdgeSchema`

        ## Example

        ```python
        edge = edge_client.get_edge(id=1)
        edge = edge_client.get_edge(label="SampleEdge")
        ```
        """
        assert id or label, "`id` 또는 `label` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        edges = self.list_edges(id=id, label=label)
        if len(edges) == 0:
            raise MLSClientError(code=404, msg="Edge 스키마가 없습니다.")
        if len(edges) > 1:
            raise MLSClientError(code=409, msg="Edge 스키마가 여러개 존재합니다.")
        return edges[0]

    def update_edge(
        self, edge: EdgeSchema, label: str, frm: str, to: str, properties: Dict[str, Any] = {}
    ) -> EdgeSchema:
        """
        단일 Edge 스키마를 수정합니다.

        ## Args

        - edge: (EdgeSchema) Edge 스키마 객체
        - label: (str) Edge 스키마 라벨
        - frm: (str) Edge 시작 Vertex 라벨
        - to: (str) Edge 종료 Vertex 라벨
        - properties: (optional) (dict) Vertex 스키마의 데이터 속성 (`Float(single)`|`Float(set)`|`String(single)`|`String(set)`)
            - Float, String: 데이터 타입
            - single: 단일 property 값을 계속 업데이트
            - set: property값을 여러 개 계속 누적해 저장

        ## Returns
        `sktmls.graphs.EdgeSchema`

        ## Example

        ```python
        edge_client.update_edge(
            edge,
            label="SampleEdge2",
            frm="startVertex",
            to="endVertex",
            properties={
                "name":"String(single)"
            }
        )
        ```
        """
        for p in properties.values():
            assert p in ["Float(single)", "Float(set)", "String(single)", "String(set)"], "허용되지 않은 property 타입입니다."
        data = {"label": label, "frm": frm, "to": to}
        if properties:
            data["properties"] = properties
        return EdgeSchema(**self._request(method="PUT", url=f"{MLS_EDGE_API_URL}/{edge.id}", data=data).results)

    def delete_edge(self, edge: EdgeSchema) -> MLSResponse:
        """
        단일 Edge 스키마를 삭제합니다.

        ## Args

        - edge: (EdgeSchema) Edge 스키마 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        edge_client.delete_edge(edge)
        ```
        """
        assert type(edge) == EdgeSchema
        return self._request(method="DELETE", url=f"{MLS_EDGE_API_URL}/{edge.id}")
