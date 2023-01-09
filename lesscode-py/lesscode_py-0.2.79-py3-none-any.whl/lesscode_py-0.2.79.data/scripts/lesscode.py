#!python
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--project", help="create new project in current dir")
group.add_argument("-i", "--is_current_dir", help="current dir as project dir", type=bool, default=True)
args = parser.parse_args()

config_text = """# -*- coding: utf-8 -*-
from tornado.options import options
from lesscode.db.connection_info import ConnectionInfo

# 运行环境
options.running_env = "local"
# 项目前缀
options.route_prefix = ""
# 服务启动端口
options.port = 8000

# 日志级别
# 10-DEBUG       输出详细的运行情况，主要用于调试。
# 20-INFO        确认一切按预期运行，一般用于输出重要运行情况。
# 30-WARNING     系统运行时出现未知的事情（如：警告内存空间不足），但是软件还可以继续运行，可能以后运行时会出现问题。
# 40-ERROR       系统运行时发生了错误，但是还可以继续运行。
# 50-CRITICAL    一个严重的错误，表明程序本身可能无法继续运行。
options.logging = "DEBUG"
# 日志文件分割方式，时间与文件大小，默认采用时间分割
# time/size
options.log_rotate_mode = "time"
# 日志文件名前缀
options.log_file_prefix = "log"
# 日志文件间隔的时间单位
# S 秒
# M 分
# H 小时、
# D 天、
# W 每星期（interval==0时代表星期一）
# midnight 每天凌晨
options.log_rotate_when = "D"
# 备份文件的个数，如果超过这个个数，就会自动删除
options.log_file_num_backups = 30

# rabbitmq配置
options.rabbitmq_config = {
    "host": "127.0.0.1",
    "port": 5672,
    "username": "guest",
    "password": "guest"
}

# kafka配置
options.kafka_config = {
    "bootstrap_servers": ["120.92.35.156:8985"]
}

# 金山对象存储配置
options.ks3_connect_config = {"host": "ks3-cn-beijing.ksyun.com", "access_key_id": "123456",
                              "access_key_secret": "123456"}

# 任务调度配置                            
options.scheduler_config = {
    "enable": True
}

# 是否打印sql
options.echo_sql = True

# 数据库连接配置
options.conn_info = [
    ConnectionInfo(dialect="postgresql", host="127.0.0.1", port=5432, user="root", password="root",
                   db_name="test", enable=True),
    ConnectionInfo(dialect="mongodb", name="mongodb", host="127.0.0.1", port=27017, user="root",
                   password="root", enable=True),
    ConnectionInfo(dialect="mysql", name="mysql", host="127.0.0.1", port=3306, user="root",
                   password="root", db_name="test", enable=True),
    ConnectionInfo(dialect="sqlalchemy", name="sa", host="127.0.0.1", port=3306, user="root",
                   password="root", db_name="test", params={"db_type":"mysql"}, enable=True),
    ConnectionInfo(dialect="elasticsearch", name="es", host="127.0.0.1", port=9200, user="root",
                   password="root", enable=True),
    ConnectionInfo(dialect="esapi", name="esapi", host="127.0.0.1", port=9200, user="root",
                   password="root", enable=True),
    ConnectionInfo(dialect="neo4j", name="neo4j", host="127.0.0.1", port=7474, user="neo4j",
                   password="neo4j", db_name="neo4j", enable=True),
    ConnectionInfo(dialect="redis", name="redis", host="localhost", port=6379, user=None,
                   password=None, db_name=1, enable=True)
]

"""

requirements_text = """lesscode-py>=0.2.60"""
README_text = f"""# {args.project}
## 框架涉及的包：
```
  "tornado==6.0",
  "tornado-sqlalchemy==0.7.0",
  "aiomysql==0.0.22",
  "motor==2.5.1",
  "elasticsearch==7.15.2",
  "aiohttp==3.8.1",
  "crypto==1.4.1",
  "pycryptodome==3.12.0",
  "aioredis==2.0.1",
  "DBUtils==3.0.2",
  "redis==4.1.4",
  "requests==2.27.1",
  "neo4j==5.0.0",
  "snowland-smx==0.3.1",
  "py_eureka_client==0.11.3",
  "ks3sdk==1.5.0",
  "filechunkio==1.8",
  "APScheduler==3.9.1",
  "nacos-sdk-python==0.1.8",
  "pika==1.3.0",
  "kafka-python==2.0.2"
  "aiopg>=1.3.3"  # 除了pg库没安装，以上包均已安装，如有需要自行安装
```
  
"""
server_text = """# -*- coding: utf-8 -*-
from lesscode.web.web_server import WebServer

if __name__ == "__main__":
    server = WebServer()
    server.start()
"""

demo_handler_file_text = """# -*- coding: utf-8 -*-
from sqlalchemy import NVARCHAR, Column
#from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from lesscode.db.sqlalchemy.sqlalchemy_helper import SqlAlchemyHelper, result_to_json, result_page
from lesscode.web.base_handler import BaseHandler
from lesscode.web.router_mapping import Handler, GetMapping, PostMapping

Base = declarative_base()


class LcAuthUser(Base):
    __tablename__ = "lc_auth_user"
    id = Column(NVARCHAR, primary_key=True)
    username = Column()
    account_status = Column()
    password = Column()
    phone_no = Column()
    display_name = Column()
    create_time = Column()


@Handler("/sqlalchemy")
class SqlAlchemyHandler(BaseHandler):

    @PostMapping("/test")
    def test(self):
        with SqlAlchemyHelper("auth_engine").make_session() as session:
            params = [LcAuthUser.id, LcAuthUser.username, LcAuthUser.phone_no]
            al = session.query(*params).all()
            return result_to_json(al)
"""


def create_file_or_dir(path, path_type, text=""):
    path_obj = Path(path)
    if not path_obj.exists():
        if path_type == 0:
            os.mkdir(path)
        elif path_type == 1:
            with open(path, 'w+') as file:
                file.write(text)
    if not path_obj.exists():
        if path_type == 0:
            path_type = "目录"
        elif path_type == 1:
            path_type = "文件"
        raise Exception(f"{path_type}({path})创建失败")


def main():
    current_dir = os.getcwd()
    if args.project:
        project_dir = f"{current_dir}/{args.project}"
    else:
        project_dir = current_dir
    handlers_dir = f"{project_dir}/handlers"
    profiles_dir = f"{project_dir}/profiles"
    create_file_or_dir(project_dir, path_type=0)
    create_file_or_dir(handlers_dir, path_type=0)
    create_file_or_dir(profiles_dir, path_type=0)

    demo_handler_file = f"{handlers_dir}/demo_handler.py"
    create_file_or_dir(demo_handler_file, path_type=1, text=demo_handler_file_text)
    config_file = f"{profiles_dir}/config.py"
    create_file_or_dir(config_file, path_type=1, text=config_text)
    requirements_file = f"{project_dir}/requirements.txt"
    create_file_or_dir(requirements_file, path_type=1, text=requirements_text)
    reade_me_file = f"{project_dir}/README.md"
    create_file_or_dir(reade_me_file, path_type=1, text=README_text)
    server_file = f"{project_dir}/server.py"
    create_file_or_dir(server_file, path_type=1, text=server_text)


if __name__ == "__main__":
    main()
