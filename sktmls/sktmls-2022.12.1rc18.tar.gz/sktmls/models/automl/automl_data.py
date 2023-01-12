from pandas import DataFrame
from google.cloud.bigquery import PartitionRange, RangePartitioning, TimePartitioning
from google.cloud.bigquery.job import QueryJobConfig
from sktmls.models import MLSModelError
from typing import Dict
import hvac

CREDENTIALS_SECRET_PATH = "gcp/skt-datahub/dataflow"
PROJECT_ID = "skt-datahub"
TEMP_DATASET = "temp_1d"


def get_secrets(path, parse_data=True):
    vault_client = hvac.Client()
    data = vault_client.secrets.kv.v2.read_secret_version(path=path)
    if parse_data:
        data = data["data"]["data"]
    return data


def get_spark(scale=0, queue=None, jars=None):
    import os
    import uuid
    import tempfile
    from pyspark.sql import SparkSession
    from pyspark import version as spark_version

    is_spark_3 = spark_version.__version__ >= "3.0.0"

    tmp_uuid = str(uuid.uuid4())
    app_name = f"skt-{os.environ.get('USER', 'default')}-{tmp_uuid}"

    key = get_secrets("gcp/sktaic-datahub/dataflow")["config"]
    key_file_name = tempfile.mkstemp()[1]
    with open(key_file_name, "wb") as key_file:
        key_file.write(key.encode())
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file.name

    if not queue:
        if "JUPYTERHUB_USER" in os.environ:
            queue = "dmig_eda"
        else:
            queue = "airflow_job"

    bigquery_jars = (
        "hdfs:///jars/spark-bigquery-with-dependencies_2.12-0.24.2.jar"
        if is_spark_3
        else "hdfs:///jars/spark-bigquery-with-dependencies_2.11-0.17.3.jar"
    )

    spark_jars = ",".join([bigquery_jars, jars]) if jars else bigquery_jars

    arrow_enabled = "spark.sql.execution.arrow.pyspark.enabled" if is_spark_3 else "spark.sql.execution.arrow.enabled"

    arrow_pre_ipc_format = "0" if is_spark_3 else "1"
    os.environ["ARROW_PRE_0_15_IPC_FORMAT"] = arrow_pre_ipc_format

    if queue == "nrt":
        spark = (
            SparkSession.builder.config("spark.app.name", app_name)
            .config("spark.driver.memory", "6g")
            .config("spark.executor.memory", "4g")
            .config("spark.driver.maxResultSize", "6g")
            .config("spark.rpc.message.maxSize", "1024")
            .config("spark.executor.core", "4")
            .config("spark.executor.instances", "32")
            .config("spark.yarn.queue", queue)
            .config("spark.ui.enabled", "false")
            .config("spark.port.maxRetries", "128")
            .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config(
                "spark.jars",
                spark_jars,
            )
            .enableHiveSupport()
            .getOrCreate()
        )
        spark.conf.set(arrow_enabled, "true")
        return spark

    if scale in [1, 2, 3, 4]:
        spark = (
            SparkSession.builder.config("spark.app.name", app_name)
            .config("spark.driver.memory", f"{scale*8}g")
            .config("spark.executor.memory", f"{scale*3}g")
            .config("spark.executor.instances", f"{scale*8}")
            .config("spark.driver.maxResultSize", f"{scale*4}g")
            .config("spark.rpc.message.maxSize", "1024")
            .config("spark.yarn.queue", queue)
            .config("spark.ui.enabled", "false")
            .config("spark.port.maxRetries", "128")
            .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config(
                "spark.jars",
                spark_jars,
            )
            .enableHiveSupport()
            .getOrCreate()
        )
    elif scale in [5, 6, 7, 8]:
        spark = (
            SparkSession.builder.config("spark.app.name", app_name)
            .config("spark.driver.memory", "8g")
            .config("spark.executor.memory", f"{2 ** scale}g")
            .config("spark.executor.instances", "32")
            .config("spark.driver.maxResultSize", "8g")
            .config("spark.rpc.message.maxSize", "1024")
            .config("spark.yarn.queue", queue)
            .config("spark.ui.enabled", "false")
            .config("spark.port.maxRetries", "128")
            .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
            .config(
                "spark.jars",
                spark_jars,
            )
            .enableHiveSupport()
            .getOrCreate()
        )
    else:
        if is_spark_3:
            spark = (
                SparkSession.builder.config("spark.app.name", app_name)
                .config("spark.driver.memory", "8g")
                .config("spark.executor.memory", "8g")
                .config("spark.executor.instances", "8")
                .config("spark.driver.maxResultSize", "6g")
                .config("spark.rpc.message.maxSize", "1024")
                .config("spark.yarn.queue", queue)
                .config("spark.ui.enabled", "false")
                .config("spark.port.maxRetries", "128")
                .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config(
                    "spark.jars",
                    spark_jars,
                )
                .enableHiveSupport()
                .getOrCreate()
            )
        else:
            spark = (
                SparkSession.builder.config("spark.app.name", app_name)
                .config("spark.driver.memory", "6g")
                .config("spark.executor.memory", "8g")
                .config("spark.shuffle.service.enabled", "true")
                .config("spark.dynamicAllocation.enabled", "true")
                .config("spark.dynamicAllocation.maxExecutors", "200")
                .config("spark.driver.maxResultSize", "6g")
                .config("spark.rpc.message.maxSize", "1024")
                .config("spark.yarn.queue", queue)
                .config("spark.ui.enabled", "false")
                .config("spark.port.maxRetries", "128")
                .config("spark.executorEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config("spark.yarn.appMasterEnv.ARROW_PRE_0_15_IPC_FORMAT", arrow_pre_ipc_format)
                .config(
                    "spark.jars",
                    spark_jars,
                )
                .enableHiveSupport()
                .getOrCreate()
            )
    spark.conf.set(arrow_enabled, "true")
    return spark


def _df_to_bq_table(
    df,
    dataset,
    table_name,
    partition=None,
    partition_field=None,
    clustering_fields=None,
    mode="overwrite",
    project_id=PROJECT_ID,
):
    import base64

    from skt.vault_utils import get_secrets

    key = get_secrets(CREDENTIALS_SECRET_PATH)["config"]
    table = f"{dataset}.{table_name}${partition}" if partition else f"{dataset}.{table_name}"
    df = (
        df.write.format("bigquery")
        .option("project", project_id)
        .option("credentials", base64.b64encode(key.encode()).decode())
        .option("table", table)
        .option("temporaryGcsBucket", "temp-seoul-7d")
    )
    if partition_field:
        df = df.option("partitionField", partition_field)
    if clustering_fields:
        df = df.option("clusteredFields", ",".join(clustering_fields))
    df.save(mode=mode)


def pandas_to_bq_table(
    pd_df,
    dataset,
    table_name,
    partition=None,
    partition_field=None,
    clustering_fields=None,
    mode="overwrite",
    project_id=PROJECT_ID,
):
    try:
        spark = get_spark()
        spark_df = spark.createDataFrame(pd_df)
        _df_to_bq_table(
            spark_df, dataset, table_name, partition, partition_field, clustering_fields, mode, project_id=project_id
        )
    finally:
        spark.stop()


def get_credentials():
    import json

    from google.oauth2 import service_account

    from skt.vault_utils import get_secrets

    key = get_secrets(CREDENTIALS_SECRET_PATH)["config"]
    json_acct_info = json.loads(key)
    credentials = service_account.Credentials.from_service_account_info(json_acct_info)
    scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

    return scoped_credentials


def get_bigquery_client(credentials=None, project_id=PROJECT_ID):
    from google.cloud import bigquery

    if credentials is None:
        credentials = get_credentials()

    return bigquery.Client(credentials=credentials, project=project_id)


def load_query_result_to_partitions(query, dest_table, project_id=PROJECT_ID):
    from google.cloud.bigquery.dataset import DatasetReference  # noqa: F401
    from google.cloud.bigquery.table import TableReference  # noqa: F401

    bq = get_bigquery_client(project_id=project_id)
    table = bq.get_table(dest_table)

    """
    Destination 이 파티션일 때는 임시테이블 만들지 않고 직접 저장
    """
    if "$" in dest_table:
        qjc = QueryJobConfig(
            destination=table,
            write_disposition="WRITE_TRUNCATE",
            create_disposition="CREATE_IF_NEEDED",
            time_partitioning=table.time_partitioning,
            range_partitioning=table.range_partitioning,
            clustering_fields=table.clustering_fields,
        )
        job = bq.query(query, job_config=qjc)
        job.result()
        _print_query_job_results(job)
        return dest_table


def _print_query_job_results(query_job):
    try:
        t = query_job.destination
        dest_str = f"{t.project}.{t.dataset_id}.{t.table_id}" if t else "no destination"  # noqa: F841
    except Exception as e:
        print("Warning: exception on print statistics")
        print(e)


def bq_insert_overwrite_table(sql, destination, project_id=PROJECT_ID):
    bq = get_bigquery_client(project_id=project_id)
    table = bq.get_table(destination)
    if table.time_partitioning or table.range_partitioning:
        load_query_result_to_partitions(sql, destination, project_id)
    else:
        config = QueryJobConfig(
            destination=destination,
            write_disposition="WRITE_TRUNCATE",
            create_disposition="CREATE_NEVER",
            clustering_fields=table.clustering_fields,
        )
        job = bq.query(sql, config)
        job.result()
        _print_query_job_results(job)
        bq.close()


def get_temp_table(project_id=PROJECT_ID):
    import uuid

    table_id = str(uuid.uuid4()).replace("-", "_")
    full_table_id = f"{project_id}.{TEMP_DATASET}.{table_id}"

    return full_table_id


def _get_result_schema(sql, bq_client=None, project_id=PROJECT_ID):
    from google.cloud.bigquery.job import QueryJobConfig

    if bq_client is None:
        bq_client = get_bigquery_client(project_id=project_id)
    job_config = QueryJobConfig(
        dry_run=True,
        use_query_cache=False,
    )
    query_job = bq_client.query(sql, job_config=job_config)
    schema = query_job._properties["statistics"]["query"]["schema"]
    return schema


def _bq_query_to_new_table(sql, destination=None, project_id=PROJECT_ID):
    return bq_ctas(sql, destination, project_id=project_id)


def _get_result_column_type(sql, column, bq_client=None, project_id=PROJECT_ID):
    schema = _get_result_schema(sql, bq_client=bq_client, project_id=project_id)
    fields = schema["fields"]
    r = [field["type"] for field in fields if field["name"] == column]
    if r:
        return r[0]
    else:
        raise ValueError(f"Cannot find column {column} in {sql}")


def bq_ctas(sql, destination=None, partition_by=None, clustering_fields=None, project_id=PROJECT_ID):
    """
    create new table and insert results
    """
    from google.cloud.bigquery.job import QueryJobConfig

    bq = get_bigquery_client(project_id=project_id)
    if partition_by:
        partition_type = _get_result_column_type(sql, partition_by, bq_client=bq, project_id=project_id)
        if partition_type == "DATE":
            qjc = QueryJobConfig(
                destination=destination,
                write_disposition="WRITE_EMPTY",
                create_disposition="CREATE_IF_NEEDED",
                time_partitioning=TimePartitioning(field=partition_by),
                clustering_fields=clustering_fields,
            )
        elif partition_type == "INTEGER":
            qjc = QueryJobConfig(
                destination=destination,
                write_disposition="WRITE_EMPTY",
                create_disposition="CREATE_IF_NEEDED",
                range_partitioning=RangePartitioning(
                    PartitionRange(start=200001, end=209912, interval=1), field=partition_by
                ),
                clustering_fields=clustering_fields,
            )
        else:
            raise Exception(f"Partition column[{partition_by}] is neither DATE or INTEGER type.")
    else:
        qjc = QueryJobConfig(
            destination=destination,
            write_disposition="WRITE_EMPTY",
            create_disposition="CREATE_IF_NEEDED",
            clustering_fields=clustering_fields,
        )

    job = bq.query(sql, qjc)
    job.result()
    _print_query_job_results(job)
    bq.close()

    return job.destination


def _bq_table_to_pandas(table, project_id=PROJECT_ID):
    credentials = get_credentials()
    bq = get_bigquery_client(credentials=credentials, project_id=project_id)
    bqstorage_client = get_bigquery_storage_client(credentials=credentials)
    row_iterator = bq.list_rows(table)
    df = row_iterator.to_dataframe(bqstorage_client=bqstorage_client, progress_bar_type="tqdm")
    bq.close()

    return df


def get_bigquery_storage_client(credentials=None):
    from google.cloud import bigquery_storage

    if credentials is None:
        credentials = get_credentials()

    return bigquery_storage.BigQueryReadClient(credentials=credentials)


def bq_to_pandas(sql, large=False, project_id=PROJECT_ID):
    destination = None
    if large:
        destination = get_temp_table(project_id=project_id)
    destination = _bq_query_to_new_table(sql, destination, project_id=project_id)
    return _bq_table_to_pandas(destination, project_id=project_id)


class EurekaData:
    def __init__(
        self,
        model_name: str,
        model_version: str,
        features: Dict[str, list] = {},
        mls_feature_store_path: str = "di_mno_offer_etl.mls_featurestore",
        mls_feature_store_meta_path: str = "di_mno_offer_etl.mls_featurestore_meta",
    ):
        assert isinstance(model_name, str), "`model_name`은 str 타입이어야 합니다."
        assert isinstance(model_version, str), "`model_version`은 str 타입이어야 합니다."
        assert isinstance(mls_feature_store_path, str), "`mls_feature_store_path`은 str 타입이어야 합니다."
        assert isinstance(mls_feature_store_meta_path, str), "`mls_feature_store_meta_path`은 str 타입이어야 합니다."

        self.model_name = model_name
        self.model_version = model_version
        self.mls_feature_store_path = mls_feature_store_path
        self.mls_feature_store_meta_path = mls_feature_store_meta_path

        assert isinstance(features, dict), "`features`은 dict 타입이어야 합니다."
        for i in features:
            assert isinstance(features[i], list), "변수들은 list 타입이어야 합니다."
        if features:
            if sum(features.values(), []):  # 카테고리만 인입
                features = sum(features.values(), [])
            else:  # 변수도 함께 들어옴
                query = f"SELECT DISTINCT feature_nm FROM {PROJECT_ID}.{self.mls_feature_store_meta_path} WHERE feature_category IN ({str(list(features.keys()))[1:-1]})"
                meta = bq_to_pandas(query)
                features = meta["feature_nm"].values.tolist()

        else:
            query = f"SELECT DISTINCT feature_nm FROM {PROJECT_ID}.{self.mls_feature_store_meta_path}"  # 아무것도 안들어옴
            meta = bq_to_pandas(query)
            features = meta["feature_nm"].values.tolist()
        self.features = features

    def TrainPathLoader(
        self,
        target_df: DataFrame,
    ):
        assert isinstance(target_df, DataFrame), "`target_data`은 Pandas DataFrame 타입이어야 합니다."

        bq = get_bigquery_client()
        try:
            target_df = target_df.astype({"label": "int"})
        except Exception as e:
            raise MLSModelError(f"EurekaModel: target_df의 label의 int 타입 변환에 실패했습니다. {e}")
        columns = ["user_id" if "svc_mgmt_num" == i else i for i in target_df.columns]
        target_df.columns = columns
        for i in ["user_id", "period"]:
            assert i in target_df.columns, f"target_df 에 `{i}` 컬럼이 없습니다."

        if "label" not in target_df.columns:
            target_df["label"] = 1

        try:
            pandas_to_bq_table(pd_df=target_df, dataset=TEMP_DATASET, table_name=f"{self.model_name}")
        except Exception as e:
            raise MLSModelError(f"EurekaModel: target_df의 업로드에 실패했습니다. {e}")

        feature_list_query = ", ".join(self.features)

        if target_df["label"].nunique() == 1:
            assert target_df["label"].unique()[0] == 1, "`target_data`의 정답을 1개만 줄거라면 1만 입력되어야 합니다."

            try:
                bq.query(f"DROP TABLE IF EXISTS {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_label1").result()
                query = f"""
                CREATE TABLE IF NOT EXISTS {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_label1 AS
                SELECT label_1.*
                  FROM (SELECT target.user_id
                             , target.label
                             , {feature_list_query}
                          FROM (SELECT * FROM {PROJECT_ID}.{self.mls_feature_store_path}) AS features
                         INNER JOIN (SELECT * FROM {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}) AS target
                            ON features.ym = target.period
                           AND features.svc_mgmt_num = target.user_id) AS label_1
                """
                bq.query(query).result()
                cnts = bq_to_pandas(f"SELECT COUNT(*) FROM {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_label1")

                bq.query(
                    f"DROP TABLE IF EXISTS {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_{self.model_version}"
                ).result()
                query = f"""
                CREATE TABLE IF NOT EXISTS {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_{self.model_version} AS
                SELECT label_1.*
                  FROM {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_label1 AS label_1
                 UNION DISTINCT  
                SELECT label_2.*
                  FROM (SELECT shuffle.svc_mgmt_num AS user_id
                             , shuffle.label
                             , {feature_list_query}
                          FROM (SELECT features.svc_mgmt_num
                                     , 0 AS label
                                     , {feature_list_query}
                                     , ROW_NUMBER() OVER (ORDER BY RAND()) AS rnd
                                  FROM (SELECT *
                                          FROM {PROJECT_ID}.{self.mls_feature_store_path}
                                         WHERE ym IN (SELECT MAX(ym) FROM {PROJECT_ID}.{self.mls_feature_store_path})) AS features
                                  LEFT JOIN (SELECT * FROM {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}) AS target
                                    ON features.svc_mgmt_num = target.user_id
                                 WHERE target.user_id IS NULL) AS shuffle
                         WHERE rnd <= {cnts.values[0][0]}) AS label_2
                """  # noqa: W291
                bq.query(query).result()
            except Exception as e:
                raise MLSModelError(f"EurekaModel: 데이터 생성에 실패했습니다. {e}")
        else:
            try:
                bq.query(
                    f"DROP TABLE IF EXISTS {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_{self.model_version}"
                ).result()
                query = f"""
                CREATE TABLE {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_{self.model_version} AS
                SELECT target.user_id
                     , target.label
                     , {feature_list_query}
                  FROM (SELECT *
                          FROM {PROJECT_ID}.{self.mls_feature_store_path}) AS features
                 INNER JOIN (SELECT * FROM {PROJECT_ID}.{TEMP_DATASET}.{self.model_name}) AS target
                    ON features.ym = target.period
                   AND features.svc_mgmt_num = target.user_id
                """
                bq.query(query).result()
            except Exception as e:
                raise MLSModelError(f"EurekaModel: 데이터 생성에 실패했습니다. {e}")

        self.destination = f"{PROJECT_ID}.{TEMP_DATASET}.{self.model_name}_{self.model_version}"
        return f"SELECT * FROM {self.destination}"

    def TrainDataLoader(
        self,
        target_df: DataFrame,
    ):
        assert isinstance(target_df, DataFrame), "`target_data`은 Pandas DataFrame 타입이어야 합니다."
        destination = self.TrainPathLoader(target_df)
        return bq_to_pandas(destination)

    def BatchLoader(self, periods, limit=None):
        assert isinstance(periods, list), "`periods`은 List 타입이어야 합니다."
        feature_list_query = ", ".join(self.features)
        if limit:
            assert isinstance(limit, int), "`limit`은 int 타입이어야 합니다."
            return bq_to_pandas(
                f"SELECT svc_mgmt_num, {feature_list_query} FROM {PROJECT_ID}.{self.mls_feature_store_path} WHERE ym IN ({', '.join(periods)}) LIMIT {limit}"
            )
        else:
            return bq_to_pandas(
                f"SELECT svc_mgmt_num, {feature_list_query} FROM {PROJECT_ID}.{self.mls_feature_store_path} WHERE ym IN ({', '.join(periods)})"
            )
