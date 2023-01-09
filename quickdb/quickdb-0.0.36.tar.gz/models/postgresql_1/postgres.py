# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'companys'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('companys_seq'::regclass)"))
    qccid = Column(String(255), comment='企查查 id')
    tycid = Column(String(255), comment='天眼查 id')
    company = Column(String(255), unique=True, comment='企业名称')
    tel = Column(String(255), comment='固定电话')
    phone = Column(String(255), comment='手机号码')
    email = Column(String(255), comment='邮箱')
    credit_code = Column(String(255), unique=True, comment='统一社会信用代码')
    law_person = Column(String(255), comment='法人')
    status = Column(String(255), comment='企业状态')
    start_date = Column(TIMESTAMP(precision=6), comment='成立日期')
    regist_capi = Column(String(255), comment='注册资本')
    rec_cap = Column(String(255), comment='实缴资本')
    check_date = Column(TIMESTAMP(precision=6), comment='核准日期')
    org_no = Column(String(255), comment='组织机构代码')
    regist_no = Column(String(255), comment='公司注册号')
    tax_no = Column(String(255), comment='纳税人识别号')
    econ_kind = Column(String(255), comment='企业类型')
    term_start = Column(TIMESTAMP(precision=6), comment='营业期限开始')
    team_end = Column(TIMESTAMP(precision=6), comment='营业期限结束')
    taxpayer_type = Column(String(255), comment='纳税人资质')
    industry = Column(String(255), comment='所属行业')
    province = Column(String(255), index=True, comment='所属地区：省')
    city = Column(String(255), index=True, comment='所属地区：市')
    county = Column(String(255), comment='所属地区：区')
    belong_org = Column(String(255), comment='登记机关')
    people_count = Column(String(255), comment='人员规模')
    insured_person = Column(String(255), comment='参保人数')
    original_name = Column(String(255), comment='曾用名')
    english_name = Column(String(255), comment='英文名')
    export_code = Column(String(255), comment='进出口企业代码和投资情况')
    address = Column(String(255), comment='注册地址')
    scope = Column(Text, comment='经营范围')
    has_trade = Column(Integer, index=True, server_default=text("0"), comment='是否有商标（1是0否，默认否）')
    has_patent = Column(Integer, index=True, server_default=text("0"), comment='是否有专利（1是0否，默认否）')
    create_time = Column(TIMESTAMP(precision=6), server_default=text("now()"), comment='创建时间（不需要手动放）')
    update_time = Column(TIMESTAMP(precision=6), comment='更新时间（不需要手动放，触发器自动设置）')


class Test(Base):
    __tablename__ = 'test'

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('test_seq'::regclass)"))
    name = Column(String(255), unique=True)
    age = Column(Integer)
