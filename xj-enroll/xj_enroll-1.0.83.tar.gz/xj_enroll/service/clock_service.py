# encoding: utf-8
"""
@project: djangoModel->clock_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 报名计时服务
@created_time: 2022/10/28 13:37
"""
from django.db.models import F
from django_redis import get_redis_connection

from ..models import EnrollRecord, Enroll, EnrollSubitem, EnrollSubitemRecord
from ..utils.custom_tool import deal_equally

ENROLL_CLOCK = "enroll-clock-ttl-{}"  # 倒计时
ENROLLED_HSET_LIST = "enroll-hset-list"


class ClockService:
    def __init__(self):
        self.conn = get_redis_connection()

    def add_clock(self, enroll_id=None, user_id=None):
        if not enroll_id or not user_id:
            return None, "enroll_id 和 user_id 必传"

        # 报名状态进入356 (已接单待上传)
        clock_key = ENROLL_CLOCK.format(enroll_id)
        has_clock = self.conn.get(clock_key)
        # print("has_clock:", has_clock)
        if not has_clock:
            self.conn.set(clock_key, user_id)
            self.conn.expire(clock_key, 600)

        # 记录报名用户
        enroll_users = self.conn.hget(ENROLLED_HSET_LIST, enroll_id)
        # print("enroll_users:", enroll_users)
        users_list = enroll_users.decode().split(";") if enroll_users else []
        users_list.append(str(user_id))
        users_list = list(set(users_list))

        users_list_str = ""
        for i in users_list:
            users_list_str = users_list_str + (";" if users_list_str else "") + i

        self.conn.hset(ENROLLED_HSET_LIST, enroll_id, users_list_str)
        self.conn.expire(ENROLLED_HSET_LIST, 660)
        return "ok", None

    # 闹钟是否停止
    def check_clock(self, enroll_id=None):
        if not enroll_id:
            return None, "enroll_i 必传且不能为空"
        clock_key = ENROLL_CLOCK.format(enroll_id)
        clock_ttl = self.conn.ttl(clock_key)
        return {"clock_ttl": clock_ttl}, None

    # 闹钟是否停止
    def check_end_clock(self):
        """定时脚本执行方法"""
        enroll_ids = self.conn.hkeys(ENROLLED_HSET_LIST)
        print("enroll_ids:", enroll_ids)
        for enroll_id in enroll_ids:
            # 时候报名结束
            is_active_clock = self.conn.get(ENROLL_CLOCK.format(enroll_id.decode()))
            if is_active_clock:
                continue

            # 计时结束则进行如下操作
            enroll_obj = Enroll.objects.filter(id=enroll_id)
            enroll_obj_first = enroll_obj.first()
            eroll_count = enroll_obj_first.to_json().get("count", 0) if enroll_obj_first else 0  # 需求份数
            if eroll_count == 0:
                continue

            enroll_record_obj = EnrollRecord.objects.filter(enroll_id=enroll_id)  # 主报名记录
            enroll_people_count = enroll_record_obj.count()  # 实际报名人数，报名人数按照主要的报名份数来计算

            # 根据报名定时截至的时候报名人数处理报名
            if enroll_people_count == 0:
                # 当前没有人报名，什么都不做，报名人数为0。
                continue
            elif enroll_people_count == 1:
                print("一人报名拿到所有 需求分数：", eroll_count)
                # 一个人报名，生成多条记录
                overplus = eroll_count - enroll_people_count
                if overplus < 0:
                    continue

                subtems_obj = EnrollSubitem.objects.annotate(enroll_subitem_id=F("id")).annotate(subitem_amount=F("amount")).filter(enroll_id=enroll_id)  # 报名分项
                if subtems_obj.count() == 0:  # 没有报名分项的的报名则跳过下面的逻辑
                    continue

                EnrollRecord.objects.filter(enroll_id=enroll_id).update(count=eroll_count, enroll_status_code=356)
                EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=356)

                values = list(subtems_obj.values("price", "count", "enroll_subitem_id", "subitem_amount"))
                enroll_record_dict = EnrollRecord.objects.filter(enroll_id=enroll_id).first().to_json()
                print("当前用户ID", enroll_record_dict.get("user_id", 0))
                for i in values:
                    params = i
                    params["enroll_record_id"] = enroll_record_obj.first().id
                    params["enroll_subitem_status_code"] = 356
                    params["user_id"] = enroll_record_dict.get("user_id", 0)
                    EnrollSubitemRecord.objects.create(**params)

            elif enroll_people_count > 1:
                # 发牌平均分逻辑
                num_list = deal_equally(eroll_count, enroll_people_count)
                # 获取所有的报名用户记录ID与用户ID
                enroll_record_list = EnrollRecord.objects.filter(enroll_id=enroll_id).values("id", "user_id")
                enroll_record_ids = {i["id"]: i["user_id"] for i in enroll_record_list}
                print("num_list", num_list, "enroll_record_ids", enroll_record_ids)
                # 修改主报名记录人数
                for enroll_record_id, num in zip(enroll_record_ids.keys(), num_list):
                    EnrollRecord.objects.filter(id=enroll_record_id).update(count=num, enroll_status_code=356)

                # 获取报名分项数据;修改报名分项 状态码
                EnrollSubitem.objects.filter(enroll_id=enroll_id).update(enroll_subitem_status_code=356)
                subtems_obj = EnrollSubitem.objects.annotate(enroll_subitem_id=F("id")).annotate(subitem_amount=F("amount")).filter(enroll_id=enroll_id)  # 报名分项
                if subtems_obj.count() == 0:  # 没有报名分项的的报名则跳过下面的逻辑
                    continue
                values = list(subtems_obj.values("price", "count", "enroll_subitem_id", "subitem_amount"))

                # 创建报名分项记录
                enroll_record_id_list = []
                for i in values:
                    if not enroll_record_id_list:
                        enroll_record_id_list = list(enroll_record_ids.keys())
                    params = i
                    params["enroll_record_id"] = enroll_record_id_list.pop()
                    params["user_id"] = enroll_record_ids.get(params["enroll_record_id"], None)
                    params["enroll_subitem_status_code"] = 356
                    # print("params:", params)
                    EnrollSubitemRecord.objects.create(**params)

            # 当超过一个人的时候，则仅仅改动报名住哪个太由后台人员指定报名
            enroll_obj.update(enroll_status_code=356)
            self.conn.hdel(ENROLLED_HSET_LIST, enroll_id)
