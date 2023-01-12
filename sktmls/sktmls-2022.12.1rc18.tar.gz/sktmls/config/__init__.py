CONFIG = {
    "YE": {
        "MLS_AB_API_URL": {
            "dev": "https://ab-internal.dev.sktmls.com",
            "stg": "https://ab-internal.stg.sktmls.com",
            "prd": "https://ab-internal.sktmls.com",
        },
        "MLS_PROFILE_API_URL": {
            "dev": "https://pf-internal.dev.sktmls.com",
            "stg": "https://pf-internal.stg.sktmls.com",
            "prd": "https://pf-internal.sktmls.com",
        },
        "MLS_RECOMMENDATION_API_URL": {
            "dev": "https://rec-internal.dev.sktmls.com",
            "stg": "https://rec-internal.stg.sktmls.com",
            "prd": "https://rec-internal.sktmls.com",
        },
        "MLS_CONVERSION_TRACKING_API_URL": {
            "dev": "https://ct-internal.dev.sktmls.com",
            "stg": "https://ct-internal.stg.sktmls.com",
            "prd": "https://ct-internal.sktmls.com",
        },
        "MLS_GRAPH_API_URL": {
            "dev": "https://graph-internal.dev.sktmls.com",
            "stg": "https://graph-internal.stg.sktmls.com",
            "prd": "https://graph-internal.sktmls.com",
        },
        "HDFS_OPTIONS": "",
    },
    "EDD": {
        "MLS_AB_API_URL": {
            "dev": "http://ab-onprem.dev.sktmls.com",
            "stg": "http://ab-onprem.stg.sktmls.com",
            "prd": "http://ab-onprem.sktmls.com",
        },
        "HDFS_OPTIONS": """-Dfs.s3a.proxy.host=awsproxy.datalake.net \
                 -Dfs.s3a.proxy.port=3128 \
                 -Dfs.s3a.endpoint=s3.ap-northeast-2.amazonaws.com \
                 -Dfs.s3a.security.credential.provider.path=jceks:///user/tairflow/s3_mls.jceks \
                 -Dfs.s3a.fast.upload=true -Dfs.s3a.acl.default=BucketOwnerFullControl""",
    },
    "MMS": {
        "MLS_PROFILE_API_URL": {
            "dev": "http://mls-up-nlb-c1258767e988aad3.elb.ap-northeast-2.amazonaws.com:8080",
            "stg": "http://mls-up-nlb-14dacbe8358f4ba2.elb.ap-northeast-2.amazonaws.com:8080",
            "prd": "http://mls-up-nlb-c0a691baaeae6cdb.elb.ap-northeast-2.amazonaws.com:8080",
        },
        "MLS_RECOMMENDATION_API_URL": {
            "dev": "http://mls-rec-nlb-29f22a1dae916c93.elb.ap-northeast-2.amazonaws.com:8080",
            "stg": "http://mls-rec-nlb-fb87c46248c7c6d0.elb.ap-northeast-2.amazonaws.com:8080",
            "prd": "http://mls-rec-nlb-53cd4d17757f3628.elb.ap-northeast-2.amazonaws.com:8080",
        },
        "MLS_GRAPH_API_URL": {
            "dev": "http://mls-graph-nlb-5887b6bfea9d1d4e.elb.ap-northeast-2.amazonaws.com:8080",
            "stg": "http://mls-graph-nlb-96dbdf574f454513.elb.ap-northeast-2.amazonaws.com:8080",
            "prd": "http://mls-graph-nlb-de1de70b72d7eb76.elb.ap-northeast-2.amazonaws.com:8080",
        },
    },
    "LOCAL": {
        "MLS_AB_API_URL": {
            "local": "http://ab.local.sktmls.com:8000",
            "dev": "https://ab.dev.sktmls.com",
            "stg": "https://ab.stg.sktmls.com",
            "prd": "https://ab.sktmls.com",
        },
        "MLS_PROFILE_API_URL": {
            "local": "https://pf.dev.sktmls.com",
            "dev": "https://pf.dev.sktmls.com",
            "stg": "https://pf.stg.sktmls.com",
            "prd": "https://pf.sktmls.com",
        },
        "MLS_RECOMMENDATION_API_URL": {
            "local": "https://rec.dev.sktmls.com",
            "dev": "https://rec.dev.sktmls.com",
            "stg": "https://rec.stg.sktmls.com",
            "prd": "https://rec.sktmls.com",
        },
        "MLS_CONVERSION_TRACKING_API_URL": {
            "local": "https://ct.dev.sktmls.com",
            "dev": "https://ct.dev.sktmls.com",
            "stg": "https://ct.stg.sktmls.com",
            "prd": "https://ct.sktmls.com",
        },
        "MLS_GRAPH_API_URL": {
            "local": "http://graph.local.sktmls.com:8080",
            "dev": "https://graph.dev.sktmls.com",
            "stg": "https://graph.stg.sktmls.com",
            "prd": "https://graph.sktmls.com",
        },
        "HDFS_OPTIONS": "",
    },
}


class Config:
    def __init__(self, runtime_env: str):
        setattr(self, "MLS_RUNTIME_ENV", runtime_env)

        for key, value in CONFIG.get(runtime_env).items():
            setattr(self, key, value)
