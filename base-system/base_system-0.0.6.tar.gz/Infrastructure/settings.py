"""
Django settings for Infrastructure project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
from pathlib import Path
from calendar import timegm

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pkqnis3u&hvqkrit2-3v3iitdt82vxdkd7k0%mt*p(_44c7p=e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # 解决跨域
    'rest_framework',
    'django_filters',
    'base_system',
    'work_scheduling',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域问题解决
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# dj-rest-auth设置token过期时间
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
}

# 在 dj-rest-auth 中启用 JWT 身份验证
REST_USE_JWT = True

# 声明希望调用 cookie 密钥的内容。如果想使用刷新令牌功能，请务必设置该变量
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True  # 允许所有主机跨域
CORS_ORIGIN_ALLOW_ALL = True  # 允许携带cookie
# CORS_ORIGIN_WHITELIST = (
#     '*'
# )

# 请求方法
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

# 请求头
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)


ROOT_URLCONF = 'Infrastructure.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Infrastructure.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'infrasdb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
AUTH_USER_MODEL = 'base_system.User'

IMG_URL = "/images/"
IMG_ROOT = os.path.join(BASE_DIR, "images")

FILE_URL = "/file/"
FILE_ROOT = os.path.join(BASE_DIR, "file")

REST_FRAMEWORK = {

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,  # 每页数目
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
        # 'drf_renderer_xlsx.renderers.XLSXRenderer',  # 导出Excel使用
        'drf_excel.renderers.XLSXRenderer',  # excel导出渲染器
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 将 simple_jwt 身份验证配置添加到身份验证类列表中
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
}

def jwt_response_handler(token, user=None, request=None):

    from base_system import serializers
    # from base_system.models import PasswordSafety, LoginToLog
    # pwd_safety = PasswordSafety.objects.filter(is_active=True).first()
    # if not user.error_times:
    #     user.error_times = 0
    #     user.save()
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip_info = x_forwarded_for
    # else:
    #     ip_info = request.META.get('REMOTE_ADDR')
    # login_to_log = LoginToLog()
    # login_to_log.user = user.username
    # login_to_log.username = user
    # login_to_log.from_url = ip_info
    # login_to_log.log_type = '登录'
    #
    # if user.error_times >= pwd_safety.allow_error_times:
    #     login_to_log.operat_status = False
    #     login_to_log.operat_content = '帐号锁定'
    #     login_to_log.save()
    #     return {
    #             "msg": "密码错误次数超过最大限制，账号锁定，请联系管理员修改密码进行解锁",
    #             "code": 4001
    #         }
    # login_to_log.operat_status = True
    # login_to_log.operat_content = '登录成功'
    # login_to_log.save()
    return {
        'jwt_token': token,
        # 'refresh_token': token,
        'user': serializers.UserSerializer(user, context={'request': request}).data
    }

    # from base_system import serializers_folder
    # try:
    #     results = {
    #     "msg": "登录成功",
    #     "code": "200",
    #     "jwt_token": token,
    #     "refresh_token": token,
    #     "user": serializers_folder.UserSerializer(user, context={'request': request}).data
    #     }
    #     return {'data': results}
    #
    # except:
    #     results = {
    #         "msg": "认证失败",
    #         "code": "10001"
    #     }
    #     return {'data': results}


def jwt_response_payload_error_handler(serializer, request=None):
    from base_system.models import User
    from base_system.views import PyDES3
    uname = request.data.get('username')
    if uname:
        key = 'K3bDD6Zytur5RLCJ'
        pdes2 = PyDES3(key)
        decrypt_username = pdes2.decrypt(uname)
        user = User.objects.filter(username=decrypt_username).first()
        if user:
            if not user.error_times:
                user.error_times = 0
        else:
            results = {
                "msg": "用户名或者密码错误",
                "code": 4002,
                "detail": serializer.errors
            }
            return {'data': results}
        # if user.error_times:
        # user.error_times = user.error_times + 1
        # pwd_safety = PasswordSafety.objects.filter(is_active=True).first()
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip_info = x_forwarded_for
        # else:
        #     ip_info = request.META.get('REMOTE_ADDR')
        # login_to_log = LoginToLog()
        # login_to_log.user = user.username
        # login_to_log.username = user
        # login_to_log.from_url = ip_info
        # login_to_log.operat_status = False
        # login_to_log.operat_content = '密码错误'
        # login_to_log.log_type = '登录'
        # login_to_log.save()
        # if user.error_times > pwd_safety.allow_error_times:
        #     return {
        #             "msg": "密码错误次数超过最大限制，账号锁定，请联系管理员修改密码进行解锁",
        #             "code": 4003,
        #             "detail": serializer.errors
        #     }
        # user.save()


    results = {
        "msg": "用户名或者密码错误",
        "code": 4002,
        "detail": serializer.errors
    }
    return {'data': results}


def jwt_payload_handler(user):
    payload = {}
    payload['user_name'] = user.username
    payload['username'] = user.username
    payload['user_email'] = user.email
    payload['"path" : "$.user.all_roles",'] = "$.user.all_roles"
    payload['https://hasura.io/jwt/claims'] = {}
    # payload['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] = [g.name for g in user.groups.all()]
    payload['https://hasura.io/jwt/claims']['x-hasura-allowed-roles'] = ['admin','public']

    # default_group = user.get_default_group
    payload['https://hasura.io/jwt/claims']['x-hasura-default-role'] = 'admin'
    payload['exp'] = datetime.datetime.utcnow() + JWT_AUTH['JWT_EXPIRATION_DELTA']

    if JWT_AUTH['JWT_ALLOW_REFRESH']:
        payload['orig_iat'] = timegm(
            datetime.datetime.utcnow().utctimetuple()
        )

    # if default_group:
    #     payload['https://hasura.io/jwt/claims']['x-hasura-default-role'] = default_group.name
    #     payload['https://hasura.io/jwt/claims']['x-hasura-default-role-id'] = str(default_group.id)
    #
    # payload['https://hasura.io/jwt/claims']['x-hasura-allowed-org-ids'] = str([org.id for org in user.organizations.all()])

    #default_org = user.get_default_organization
    #if default_org:
    #    payload['https://hasura.io/jwt/claims']['x-hasura-default-org'] = default_org.departname
    #    payload['https://hasura.io/jwt/claims']['x-hasura-default-rog-id'] = str(default_org.id)

    #payload['https://hasura.io/jwt/claims']['x-hasura-user-id'] = str(user.id)

    return payload


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),  # token过期时间
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),  # 登录一次token可持续时间
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_ALLOW_REFRESH': True,
    'JWT_RESPONSE_PAYLOAD_HANDLER': jwt_response_handler,
    'JWT_PAYLOAD_HANDLER': jwt_payload_handler,
    'JWT_RESPONSE_PAYLOAD_ERROR_HANDLER': jwt_response_payload_error_handler,
}

# 重写用户验证
AUTHENTICATION_BACKENDS = [
    'base_system.views.OverrideUserAuthentication'
]