CONFIG_FILE_PATH = "config.json"
API_URL = 'api_url'
API_VERSION = 'api_version'
TARGET_ID = 'tid'
CLIENT_ID = 'cid'
TARGET = 't'
RECORD_CATEGORY = 'dp'
USER_LANG = 'ul'
RECORD_PARTICULARS = 'dt'
ENABLED = 'collection_status'
APP_NAME = "goog-stats"


analytics_config = {
    ENABLED: True,
    API_URL: 'https://www.google-analytics.com/j/collect',
    API_VERSION: '1',
    TARGET: 'pageview',
    USER_LANG: 'en-in',
    RECORD_PARTICULARS: '',
    TARGET_ID: '',
    CLIENT_ID: '',
    RECORD_CATEGORY: 'scan_page'
}
