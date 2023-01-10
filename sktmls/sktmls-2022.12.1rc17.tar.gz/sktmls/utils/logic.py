import math
import random
from calendar import monthrange
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functools import reduce

import numpy as np
from haversine import haversine
from pytz import timezone

from sktmls import MLSClientError

TZ = timezone("Asia/Seoul")


class LogicProcessor:
    """
    상품 선택 로직 등을 프로세스하는 클래스입니다.

    아래 operations를 참조하여 json 형식의 로직을 구현하면 됩니다.

    ## 기본 문법

    기본적으로 JSON 형태의 로직은 아래 포맷을 따릅니다.

    ```python
    {
        "operator": [*args]
    }
    ```

    각각의 arg는 또 다른 JSON 형태의 로직이 될 수 있으며 recursive하게 프로세스됩니다.

    ```json
    {
        "and": [
            {"==": [3, 3]},
            {">": [
                5,
                {"max": [3, 10]}
            ]}
        ]
    }
    ```

    ## 피쳐 참조

    피쳐를 참조하는 방법은

    ```
    {
        "var": ["feature_name", 기본값]
    }
    ```

    형식입니다.

    리스트 또는 딕셔너리 타입의 피쳐 값을 참조하는 경우

    ```
    {
        "var": ["feature_name.0", 기본값]
    }
    ```

    ```
    {
        "var": ["feature_name.key_name", 기본값]
    }
    ```

    과 같은 형태로 하위 값에 접근이 가능합니다.

    ## 추가 키 참조

    Recommendation API v3 이후부터 지원하는 추가 키(세컨 키 등) 리스트는

    ```
    {
        "var": ["additional_keys.0", 기본값]
    }
    ```

    와 같이 `additional_key.index` 포맷으로 접근 가능합니다.

    ## 연산자

    - `==`: 두 값이 같은 경우 True. 타입을 고려하지 않음
    - `===`: 두 값이 같은 경우 True. 타입을 고려함
    - `!=`: 두 값이 다른 경우 True. 타입을 고려하지 않음
    - `!==`: 두 값이 다른 경우 True. 타입을 고려함
    - `<`: 왼쪽 값이 오른쪽 값보다 작은 경우 True
    - `<=`: 왼쪽 값이 오른쪽 값보다 작거나 같은 경우 True
    - `>`: 왼쪽 값이 오른쪽 값보다 큰 경우 True
    - `>=`: 왼쪽 값이 오른쪽 값보다 크거나 같은 경우 True
    - `!`: not
    - `and`: 모든 args가 True인 경우 True
    - `or`: 하나 이상의 args가 True인 경우 True
    - `any`: args[0]의 하나 이상의 element가 True인 경우 True
    - `all`: arg[0]의 모든 element가 True인 경우 True
    - `?:`: args[0]이 True이면 args[1] 반환, 아니면 args[2] 반환
    - `is`: args[0] is args[1]
    - `if`: args[0]이 True이면 args[1] 반환, 아닌 경우 만약 args[2]이 True이면 args[3] 반환, ... , 조건이 모두 False면 args[-1] 반환
    - `if_min`: args[0], args[2], args[4]... 중 args[i]가 최소인 경우 args[i + 1] 반환
    - `if_max`: args[0], args[2], args[4]... 중 args[i]가 최대인 경우 args[i + 1] 반환
    - `if_closest`: args[1], args[3], args[5]... 중 args[0]과 가장 가까운 값이 args[i]인 경우 args[i + 1] 반환
    - `if_closest_upper`: args[1], args[3], args[5]... 중 args[0]보다 크면서 가장 가까운 값이 args[i]인 경우 args[i + 1] 반환
    - `if_closest_lower`: args[1], args[3], args[5]... 중 args[0]보다 작으면서 가장 가까운 값이 args[i]인 경우 args[i + 1] 반환
    - `all_in`: args[0]의 element가 모두 args[1]에 포함된 경우 True
    - `any_in`: args[0]의 element가 하나라도 args[1]에 포함된 경우 True
    - `in`: 왼쪽 값이 오른쪽 값에 포함된 경우 True
    - `cat`: args들을 문자열 join
    - `join`: 리스트 args[0]을 args[1]을 구분자로 하여 문자열로 join
    - `split`: 문자열 args[0]을 args[1]을 구분자로 하여 분할
    - `+`: args들의 합
    - `*`: args들의 곱
    - `-`: 왼쪽 빼기 오른쪽. args의 길이가 1인 경우 -args[0]
    - `/`: 왼쪽 나누기 오른쪽
    - `%`: 왼쪽 나누기 오른쪽한 나머지
    - `inner`: arg[0]과 arg[1]의 내적 (둘 모두 1차원 배열인 경우 숫자를 반환하고 2차원 배열인 경우 리스트 반환)
    - `exp`: 지수함수 값 반환
    - `sigmoid`: Sigmoid 함수 값 반환
    - `norm`: norm 값 반환
    - `min`: args 중 최소값
    - `max`: args 중 최대값
    - `argmin`: 최소값을 가지는 인덱스
    - `argmax`: 최대값을 가지는 인덱스
    - `get`: args[0]의 args[1]번째 element. 딕셔너리 타입의 경우 args[0]의 args[1] 키에 해당하는 값
    - `for_get`: args[0] 자료구조 내 모든 element들의 args[1]번째 값을 모아 리스트로 반환한다.
    - `int`: int 파싱
    - `float`: float 파싱
    - `str`: str 파싱
    - `list`: args들을 리스트에 넣어 그대로 반환
    - `dict`: {args[0]: args[1], args[2]: args[3], ...}
    - `dict_keys`: 딕셔너리 타입의 args[0]의 키 리스트 반환
    - `dict_values`: 딕셔너리 타입의 args[0]의 값 리스트 반환
    - `pick`: args[0] 리스트 element 중 args[1]에서 정의한 인덱스만 뽑아냄
    - `pick_in`: args[0] 리스트 element 중 args[1]에 존재하는 것들만 필터
    - `remove`: args[1]에서 args[0] 값을 가진 element들을 삭제 후 반환
    - `remove_empty`: args[0]에서 빈 자료구조나 None인 element들을 삭제
    - `remove_duplicated`: 중복된 element들을 삭제. 순서가 앞인 element가 우선 (args[1]: 비교 index. None인 경우 element 자체를 비교).
    - `sample`: args[0] 중 args[1]개 만큼 랜덤 추출 (seed: args[2])
    - `first`: args[0] 중 첫 args[1]개를 반환
    - `replace`: args[2]의 element 중 args[0] 값을 args[1] 값으로 교체하여 반환
    - `repeat`: args[0]이 args[1]번 반복되는 리스트 반환
    - `range`: range 함수 값 반환
    - `len`: args[0]의 길이 반환
    - `empty`: args[0]의 길이가 0이면 True
    - `unique`: args[0] 리스트에서 중복값을 제거
    - `merge`: args들을 하나의 리스트로 합침
    - `vmerge`: 길이가 같은 리스트 args[0], args[1], args[2]... 의 같은 순서 element들끼리 묶어 반환
    - `count`: args의 길이
    - `abs`: args[0]의 절대값
    - `round`: 반올림 (args[0]을 args[1] 자리까지 반올림)
    - `mean`: 평균값 (리스트들이 args로 들어오는 경우 각 element의 평균값을 가지는 리스트 반환)
    - `closest`: args[1], args[2]... 중 args[0]과 가장 가까운 값
    - `closest_upper`: args[1], args[2]... 중 args[0]보다 크면서 가장 가까운 값
    - `closest_lower`: args[1], args[2]... 중 args[0]보다 작으면서 가장 가까운 값
    - `weekday`: 요일 인덱스 반환 (월요일 1 ~ 일요일 7)
    - `ndays`: 이번 달의 마지막 날짜
    - `day`: 오늘 날짜
    - `month`: 이번 달
    - `year`: 올해
    - `hour`: 시
    - `minute`: 분
    - `second`: 초
    - `microsecond`: 마이크로초
    - `now`: 현재 시각 반환 (datetime 객체)
    - `strptime`: 문자열을 시각으로 변환 (시각 문자열: args[0], 형식: args[1])
    - `strftime`: 시각을 문자열로 변환 (datetime 객체: args[0], 형식: args[1])
    - `timedelta`: 시간차 객체 반환 (relativedelta 객체) ([참조](https://dateutil.readthedocs.io/en/stable/relativedelta.html))
    - `dt+`: datetime 객체와 relativedelta 객체들의 합을 반환 (datetime 객체)
    - `km_to_latitude_degrees`: km 거리를 위도상 각도로 변환 (args[0]: km)
    - `km_to_longitude_degrees`: km 거리를 경도상 각도로 변환 (args[0]: km, args[1]: 기준 위도)
    - `distance`: 유클리디안 거리 계산 (args: x1, y1, x2, y2)
    - `geo_distance`: 위경도 기반 거리 계산 (args: lat1, lon1, lat2, lon2) (단위: km)
    - `rand`: 0~1 사이의 난수 (seed: args[0])
    - `beta`: 베타 분포를 따르는 random variable (a: args[0], b: args[1], seed: args[2])
    - `pf`: 프로파일 API 조회 (api_type: args[0], profile_id: args[1], item_id/user_id: args[2], keys: args[3])
    - `with`: args[-1]의 프로세스에 {args[0]: arg[1], args[2]: args[3]...}의 데이터를 `var`로 참조 가능
    - `for`: args[0]를 iterator로 사용하여 args[1] 루프. {"var": "i"}, {"var": "i.0"} 등으로 iterator 참조 가능 (map과 유사)
    """

    def __init__(self):
        self.operations = {
            "==": self._soft_equals,
            "===": self._hard_equals,
            "!=": lambda a, b: not self._soft_equals(a, b),
            "!==": lambda a, b: not self._hard_equals(a, b),
            ">": lambda a, b: self._less(b, a),
            ">=": lambda a, b: self._less(b, a) or self._soft_equals(a, b),
            "<": self._less,
            "<=": self._less_or_equal,
            "!": lambda a: not a,
            "!!": bool,
            "and": lambda *args: reduce(lambda total, arg: total and arg, args, True),
            "or": lambda *args: reduce(lambda total, arg: total or arg, args, False),
            "all": lambda a: all(a),
            "any": lambda a: any(a),
            "?:": lambda a, b, c: b if a else c,
            "is": lambda a, b: a is b,
            "if": self._if,
            "if_min": self._if_min,
            "if_max": self._if_max,
            "if_closest": self._if_closest,
            "if_closest_upper": self._if_closest_upper,
            "if_closest_lower": self._if_closest_lower,
            "any_in": lambda a, b: any([i in b for i in a]),
            "all_in": lambda a, b: all([i in b for i in a]),
            "in": lambda a, b: a in b if "__contains__" in dir(b) else False,
            "contains": lambda a, b: b in a if "__contains__" in dir(a) else False,
            "cat": lambda *args: "".join(str(arg) for arg in args),
            "join": lambda a, sep: sep.join(str(i) for i in a),
            "split": lambda a, sep: [x.strip() for x in a.split(sep)],
            "+": self._plus,
            "*": lambda *args: reduce(lambda total, arg: total * float(arg), args, 1),
            "-": self._minus,
            "/": lambda a, b=None: a if b is None else float(a) / float(b),
            "%": lambda a, b: a % b,
            "inner": lambda a, b: np.inner(a, b).tolist(),
            "exp": lambda a: np.exp(a).tolist(),
            "sigmoid": lambda a: (1.0 / (1.0 + np.exp(np.negative(a)))).tolist(),
            "norm": lambda a: np.linalg.norm(a).tolist(),
            "min": lambda *args: min(args),
            "max": lambda *args: max(args),
            "argmin": lambda *args: np.argmin(args),
            "argmax": lambda *args: np.argmax(args),
            "get": self._get,
            "for_get": self._for_get,
            "int": self._int,
            "float": self._float,
            "str": self._str,
            "list": lambda *args: list(args),
            "dict": self._dict,
            "dict_keys": lambda a: list(a.keys()),
            "dict_values": lambda a: list(a.values()),
            "pick": lambda a, b: [a[i] for i in b],
            "pick_in": self._pick_in,
            "remove": lambda a, b: [i for i in b if i != a],
            "remove_empty": lambda a: [i for i in a if i],
            "remove_duplicated": self._remove_duplicated,
            "sample": self._sample,
            "first": lambda a, num_pick: list(a[:num_pick]),
            "replace": lambda a, b, c: [b if i == a else i for i in c],
            "repeat": lambda a, n: [a] * n,
            "range": lambda *args: list(range(*args)),
            "len": lambda a: len(a),
            "empty": lambda a: len(a) == 0,
            "unique": self._unique,
            "merge": self._merge,
            "vmerge": self._vmerge,
            "count": lambda *args: sum(1 if a else 0 for a in args),
            "abs": lambda a: abs(a),
            "round": lambda a, b: round(a, b),
            "mean": lambda *args: np.mean(args, axis=0).tolist(),
            "closest": self._closest,
            "closest_upper": self._closest_upper,
            "closest_lower": self._closest_lower,
            "sort": lambda a, b: sorted(a, reverse=(b == "reverse")),
            "sort_by": lambda a, b, c: sorted(a, key=lambda x: x[b], reverse=(c == "reverse")),
            "weekday": lambda: datetime.now(TZ).isoweekday(),
            "ndays": lambda: monthrange(datetime.now(TZ).year, datetime.now(TZ).month)[1],
            "day": lambda: datetime.now(TZ).day,
            "month": lambda: datetime.now(TZ).month,
            "year": lambda: datetime.now(TZ).year,
            "hour": lambda: datetime.now(TZ).hour,
            "minute": lambda: datetime.now(TZ).minute,
            "second": lambda: datetime.now(TZ).second,
            "microsecond": lambda: datetime.now(TZ).microsecond,
            "now": lambda: datetime.now(TZ),
            "strptime": lambda a, b: TZ.localize(datetime.strptime(a, b)),
            "strftime": lambda a, b: datetime.strftime(a, b),
            "timedelta": lambda *args: relativedelta(**self._dict(*args)),
            "dt+": self._dt_plus,
            "km_to_latitude_degrees": lambda a: 360 * a / 40075,
            "km_to_longitude_degrees": lambda a, lat: 360 * a / 2 / math.pi / 6371 / math.cos(math.radians(lat)),
            "distance": lambda x1, y1, x2, y2: math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2),
            "geo_distance": lambda lat1, long1, lat2, long2: haversine((lat1, long1), (lat2, long2)),
            "rand": self._rand,
            "beta": self._beta,
            "return": lambda *args: args,
        }

    def _if_min(self, *args):
        min_arg = np.argmin([args[i] for i in range(0, len(args) - 1, 2)])
        return args[min_arg * 2 + 1]

    def _if_max(self, *args):
        max_arg = np.argmax([args[i] for i in range(0, len(args) - 1, 2)])
        return args[max_arg * 2 + 1]

    def _if_closest(self, arg, *comps):
        args = list(comps)
        for i in range(0, len(args) - 1, 2):
            args[i] = abs(arg - args[i])
        return self._if_min(*args)

    def _if_closest_upper(self, arg, *comps):
        args = []
        for i in range(0, len(comps) - 1, 2):
            if comps[i] > arg:
                args.append(comps[i])
                args.append(comps[i + 1])
        if not args:
            return None
        return self._if_closest(arg, *args)

    def _if_closest_lower(self, arg, *comps):
        args = []
        for i in range(0, len(comps) - 1, 2):
            if comps[i] < arg:
                args.append(comps[i])
                args.append(comps[i + 1])
        if not args:
            return None
        return self._if_closest(arg, *args)

    def _soft_equals(self, a, b):
        if isinstance(a, str) or isinstance(b, str):
            return str(a) == str(b)
        if isinstance(a, bool) or isinstance(b, bool):
            return bool(a) is bool(b)
        return a == b

    def _hard_equals(self, a, b):
        if type(a) != type(b):
            return False
        return a == b

    def _less(self, a, b, *args):
        types = set([type(a), type(b)])
        if float in types or int in types:
            try:
                a, b = float(a), float(b)
            except TypeError:
                return False
        return a < b and (not args or self._less(b, *args))

    def _less_or_equal(self, a, b, *args):
        return (self._less(a, b) or self._soft_equals(a, b)) and (not args or self._less_or_equal(b, *args))

    def _to_numeric(self, arg):
        if isinstance(arg, str):
            if "." in arg:
                return float(arg)
            else:
                return int(arg)
        return arg

    def _plus(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]
        return sum(self._to_numeric(arg) for arg in args)

    def _minus(self, *args):
        if len(args) == 1:
            return -self._to_numeric(args[0])
        return self._to_numeric(args[0]) - self._to_numeric(args[1])

    def _closest(self, arg, *comps):
        closest = comps[0]
        min_diff = abs(arg - comps[0])
        for i in range(1, len(comps)):
            diff = abs(arg - comps[i])
            if min_diff > diff:
                min_diff = diff
                closest = comps[i]
        return closest

    def _closest_upper(self, arg, *comps):
        args = [c for c in comps if c > arg]
        if not args:
            return None
        return self._closest(arg, *args)

    def _closest_lower(self, arg, *comps):
        args = [c for c in comps if c < arg]
        if not args:
            return None
        return self._closest(arg, *args)

    def _get(self, a, b, not_found=None):
        try:
            return a[b]
        except (KeyError, TypeError, ValueError, IndexError):
            return not_found

    def _for_get(self, a, b, not_found=None):
        result = []
        for i in a:
            try:
                result.append(i[b])
            except (KeyError, TypeError, ValueError, IndexError):
                result.append(not_found)
        return result

    def _float(self, a):
        if isinstance(a, list) or isinstance(a, tuple):
            return [float(i) for i in a]
        return float(a)

    def _int(self, a):
        if isinstance(a, list) or isinstance(a, tuple):
            return [int(i) for i in a]
        return int(a)

    def _str(self, a):
        if isinstance(a, list) or isinstance(a, tuple):
            return [str(i) for i in a]
        return str(a)

    def _dict(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        d = {}
        for i in range(0, len(args), 2):
            if i == len(args) - 1:
                break
            d[args[i]] = args[i + 1]
        return d

    def _pick_in(self, a, b):
        result = []
        for i in a:
            if i in b:
                result.append(i)
        return result

    def _remove_duplicated(self, a, b=None):
        result = []
        keys = []
        for i in a:
            comp = i[b] if b is not None else i
            if comp not in keys:
                keys.append(comp)
                result.append(i)
        return result

    def _dt_plus(self, dt, *args):
        if not isinstance(dt, datetime):
            raise ValueError("첫 arg가 datetime이 아닙니다.")
        for arg in args:
            if not isinstance(arg, relativedelta):
                raise ValueError("arg가 relativedelta가 아닙니다.")
            dt += arg
        return dt

    def _sample(self, a, num_pick, seed):
        random.seed(seed)
        return random.sample(a, num_pick)

    def _rand(self, seed):
        random.seed(seed)
        return random.random()

    def _beta(self, a, b, seed=None):
        if seed is not None:
            np.random.seed(seed)
        return np.random.beta(a, b)

    def _unique(self, a):
        result = []
        for item in a:
            if item not in result:
                result.append(item)
        return result

    def _merge(self, *args):
        ret = []

        if len(args) == 1 and isinstance(args[0], list):
            args = args[0]

        for arg in args:
            if isinstance(arg, list) or isinstance(arg, tuple):
                ret += list(arg)
            else:
                ret.append(arg)
        return ret

    def _vmerge(self, *args):
        ret = []
        for i in range(len(args[0])):
            r = []
            for j in range(len(args)):
                r.append(args[j][i])
            ret.append(r)
        return ret

    def _pf(self, pf_client, *args):
        if not pf_client:
            return None

        try:
            api_type = args[0]
            profile_id = args[1]
            target_id = args[2]
            keys = args[3]
        except (KeyError, TypeError, ValueError, IndexError):
            return None

        try:
            if api_type == "user":
                pf = pf_client.get_user_profile(profile_id=profile_id, user_id=target_id, keys=keys)
            elif api_type == "item":
                pf = pf_client.get_item_profile(profile_id=profile_id, item_id=target_id, keys=keys)
            else:
                pf = pf_client.get_profile(profile_id=profile_id, id=target_id, keys=keys)
        except MLSClientError:
            return None

        return [pf.get(key) for key in keys]

    def _graph(self, graph_client, *args):
        if not graph_client:
            return None

        try:
            request_type = args[0]
            params = self._dict(*args[1:])
        except (KeyError, TypeError, ValueError, IndexError):
            return None

        try:
            if request_type == "vertex":
                entities = graph_client.list_vertices(params)
            elif request_type == "edge":
                entities = graph_client.list_edges(params)
            else:
                return None
        except MLSClientError:
            return None

        return [e.get() for e in entities]

    def _dynamodb(self, dynamodb_client, *args):
        if not dynamodb_client:
            return None

        try:
            request_type = args[0]
            table_name = args[1]
            arg = self._dict(*args[2:])
        except (KeyError, TypeError, ValueError, IndexError):
            return None

        try:
            if request_type == "get":
                return dynamodb_client.get_item(table_name=table_name, key=arg)["item"]
            elif request_type == "put":
                return dynamodb_client.put_item(table_name=table_name, item=arg)
            elif request_type == "update":
                return dynamodb_client.update_item(table_name=table_name, item=arg)
            else:
                return None
        except MLSClientError:
            return None

    def _if(self, data, pf_client, graph_client, dynamodb_client, *args):
        for i in range(0, len(args) - 1, 2):
            if self.apply(args[i], data, pf_client, graph_client, dynamodb_client):
                return self.apply(args[i + 1], data, pf_client, graph_client, dynamodb_client)
        if len(args) % 2:
            return self.apply(args[-1], data, pf_client, graph_client, dynamodb_client)
        else:
            return None

    def _with(self, data, pf_client, graph_client, dynamodb_client, *args):
        if len(args) % 2 == 0:
            raise ValueError("with operator에 오류가 있습니다.")

        body = args[-1]
        for i in range(0, len(args), 2):
            if i == len(args) - 1:
                break
            data[args[i]] = self.apply(args[i + 1], data, pf_client, graph_client, dynamodb_client)

        results = self.apply(body, data, pf_client, graph_client, dynamodb_client)

        for i in range(0, len(args), 2):
            if i == len(args) - 1:
                break
            data.pop(args[i], None)

        return results

    def _for(self, data, pf_client, graph_client, dynamodb_client, *args):
        results = []
        it = self.apply(args[0], data, pf_client, graph_client, dynamodb_client)
        for i in it:
            data["i"] = i
            if isinstance(it, dict):
                data["k"] = i
                data["v"] = it[i]
            results.append(self.apply(args[1], data, pf_client, graph_client, dynamodb_client))
        data.pop("i", None)
        data.pop("k", None)
        data.pop("v", None)
        return results

    def _get_var(self, data, var_name, not_found=None):
        try:
            for key in str(var_name).split("."):
                try:
                    data = data[key]
                except TypeError:
                    data = data[int(key)]
        except (KeyError, TypeError, ValueError, IndexError):
            return not_found
        else:
            return data

    def _missing(self, data, *args):
        not_found = object()
        if args and isinstance(args[0], list):
            args = args[0]
        ret = []
        for arg in args:
            if self._get_var(data, arg, not_found) is not_found:
                ret.append(arg)
        return ret

    def _missing_some(self, data, min_required, args):
        if min_required < 1:
            return []
        found = 0
        not_found = object()
        ret = []
        for arg in args:
            if self._get_var(data, arg, not_found) is not_found:
                ret.append(arg)
            else:
                found += 1
                if found >= min_required:
                    return []
        return ret

    def apply(self, tests, data=None, pf_client=None, graph_client=None, dynamodb_client=None):
        """
        ## Args

        - tests: (dict) 테스트 할 json 형식의 로직
        - data: (optional) (dict) 로직에서 참조할 데이터 dict (기본값: None)
        - pf_client: (optional) (`sktmls.apis.profile_api.MLSProfileAPIClient`) 로직에서 사용할 프로파일 API 클라이언트 (기본값: None)
        - graph_client: (optional) (`sktmls.apis.graph_api.MLSGraphAPIClient`) 로직에서 사용할 그래프 API 클라이언트 (기본값: None)
        - dynamodb_client: (optional) (`sktmls.dynamodb.DynamoDBClient`) 로직에서 사용할 DynamoDB 클라이언트 (기본값: None)
        """
        if tests is None or not isinstance(tests, dict):
            return tests

        operator = list(tests.keys())[0]
        data = data or {}
        values = tests[operator]

        if operator == "if":
            return self._if(data, pf_client, graph_client, dynamodb_client, *values)

        if operator == "with":
            return self._with(data, pf_client, graph_client, dynamodb_client, *values)

        if operator == "for":
            return self._for(data, pf_client, graph_client, dynamodb_client, *values)

        if not isinstance(values, list) and not isinstance(values, tuple):
            values = [values]

        values = [self.apply(val, data, pf_client, graph_client, dynamodb_client) for val in values]

        if operator == "pf":
            return self._pf(pf_client, *values)
        if operator == "graph":
            return self._graph(graph_client, *values)
        if operator == "dynamodb":
            return self._dynamodb(dynamodb_client, *values)
        if operator == "var":
            return self._get_var(data, *values)
        if operator == "missing":
            return self._missing(data, *values)
        if operator == "missing_some":
            return self._missing_some(data, *values)

        if operator not in self.operations:
            raise ValueError(f"없는 operator입니다: {operator}")

        return self.operations[operator](*values)
