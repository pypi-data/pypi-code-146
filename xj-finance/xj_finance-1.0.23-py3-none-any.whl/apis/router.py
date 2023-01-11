# -*- coding: UTF-8 -*-

import logging, re, urllib.parse
from django.conf import settings
from .middleware import GlobalRequestMiddleware
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger(__name__)

# 获取当前域名
def getSiteDomain(request = None):
	request = request or GlobalRequestMiddleware.getRequest()
	if request:
		header = request.META.get("HTTP_SITE_ROUTER") or request.headers.get("Site-Router")
		if header and header in settings.ALLOWED_HOSTS:
			return header
		
		query = request.GET.get("site-router")
		if query and query in settings.ALLOWED_HOSTS:
			return query
		
		site = get_current_site(request)
		if site:
			return site.domain
	return None
#end - getSiteDomain

# 当前是否为移动端访问
def isMobile(request = None):
	request = request or GlobalRequestMiddleware.getRequest()
	userAgent = request.META.get("HTTP_USER_AGENT")
	if userAgent and re.search(r"(mobile|android|iphone|ipad|phone|micromessenger|alipay)", userAgent, re.IGNORECASE):
		return True
	
	return False
#end - isMobile

# 当前是否为微信浏览器访问
def isWeChat(request = None):
	request = request or GlobalRequestMiddleware.getRequest()
	if request.META.get("HTTP_WECHAT") == "1" or request.headers.get("wechat") == "1" or request.GET.get("wechat") == "1":
		return True
	
	userAgent = request.META.get("HTTP_USER_AGENT")
	if userAgent and re.search(r"(micromessenger)", userAgent, re.IGNORECASE):
		return True
	
	return False
#end - isWeChat

# 当前是否为小程序访问
def isMiniProgram(request = None):
	request = request or GlobalRequestMiddleware.getRequest()
	if request.META.get("HTTP_MINIPROGRAM") == "1" or request.headers.get("miniprogram") == "1" or request.GET.get("miniprogram") == "1":
		return True
	
	userAgent = request.META.get("HTTP_USER_AGENT")
	if userAgent and re.search(r"(miniprogram)", userAgent, re.IGNORECASE):
		return True
	
	return False
#end - isMiniProgram

# 当前是否为支付宝浏览器访问
def isAlipay(request = None):
	request = request or GlobalRequestMiddleware.getRequest()
	if request.META.get("HTTP_ALIPAY") == "1" or request.headers.get("alipay") == "1" or request.GET.get("alipay") == "1":
		return True
	
	userAgent = request.META.get("HTTP_USER_AGENT")
	if userAgent and re.search(r"(alipay)", userAgent, re.IGNORECASE):
		return True
	
	return False
#end - isAlipay

# 获取接口白名单域名
def getBlackListSite():
	site = list(settings.DATABASE_MAPPING.keys())
	if not site:
		return getSiteDomain()
	return site[0]
#end - getBlackListSite

def getCurrentURL(request = None):
	request = request or GlobalRequestMiddleware.getRequest()
	if request:
		referrer = request.get_full_path()
		if not referrer.startswith("http"):
			referrer = "http://{}{}".format(getSiteDomain(request), referrer)
		return referrer
	#end if
	
	return ""
#end - getCurrentURL

# 生成白名单跳转链接
def getGateway(url, referrer = "", request = None):
	if not referrer:
		request = request or GlobalRequestMiddleware.getRequest()
		if request:
			referrer = request.get_full_path()
			if not referrer.startswith("http"):
				referrer = "http://{}{}".format(getSiteDomain(request), referrer)
	#end if
	
	return "http://{}/gateway?url={}&referrer={}".format(getBlackListSite(), urllib.parse.quote(url), urllib.parse.quote(referrer))
#end - getGateway

class DatabaseAppsRouter(object):
	def db_for_read(self, model, **hints):
		connection = settings.DATABASE_MAPPING.get(getSiteDomain())
		logger.debug("DatabaseAppsRouter.db_for_read site is {}".format(connection))
		return connection
	#end db_for_read
	
	def db_for_write(self, model, **hints):
		connection = settings.DATABASE_MAPPING.get(getSiteDomain())
		logger.debug("DatabaseAppsRouter.db_for_write site is {}".format(connection))
		return connection
	#end db_for_read
	
	def allow_relation(self, obj1, obj2, **hints):
		return None
	#end allow_relation
	
	def allow_migrate(self, db, app_label, model_name=None, **hints):
		return None
	#end allow_migrate
#end - DatabaseAppsRouter
