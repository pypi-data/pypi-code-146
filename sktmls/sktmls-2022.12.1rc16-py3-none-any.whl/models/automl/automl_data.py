from pandas import DataFrame
from google.cloud.bigquery import PartitionRange, RangePartitioning, TimePartitioning
from google.cloud.bigquery.job import QueryJobConfig
from sktmls.models import MLSModelError
from typing import List
import hvac

mls_feature_store_path = "x1112834.mls_featurestore"
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
        dest_str = f"{t.project}.{t.dataset_id}.{t.table_id}" if t else "no destination"
        print(
            f"destination: {dest_str}\n"
            f"total_rows: {query_job.result().total_rows}\n"
            f"slot_secs: {query_job.slot_millis/1000}\n"
        )
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
        target_df: DataFrame,
        model_name: str,
        model_version: str,
        features: List[str] = [
            "sex_cd",
            "cust_age_cd",
            "eqp_mfact_cd_apple",
            "eqp_mfact_cd_samsung",
            "eqp_mfact_cd_etc",
            "bf_m1_arpu",
            "bf_m3_avg_arpu",
            "bf_m1_mng_nice_cb_scr",
            "mng_isas_scr",
            "sml_settl_amt",
            "sml_settl_use_cnt",
            "bf_m1_google_dcb_cnt",
            "bf_m1_google_dcb_amt",
            "dom_call",
            "mth_cnsl_cnt",
            "dsat_cnsl_cnt",
            "mms_use_cnt",
            "dom_data_usag_amt",
            "use_mbl_phon_svc_cnt",
            "mms_score",
            "elementary_school_student",
            "middle_school_student",
            "high_school_student",
            "university_student",
            "lower_elementary_school_parent",
            "higher_elementary_school_parent",
            "middle_school_parent",
            "high_school_parent",
            "university_parent",
            "inf_0to2_parent",
            "inf_3to4_parent",
            "inf_5to7_parent",
            "kindergarden_parent",
            "one_person_household",
            "soldier",
            "soldier_parent",
            "cherry_picker",
            "office_worker",
            "self_employed",
            "topic_max_banking_and_finance_bank_visitor",
            "topic_max_banking_and_finance_call_to_bank",
            "topic_max_banking_and_finance_call_to_customer_service",
            "topic_max_banking_and_finance_card_app_users",
            "topic_max_banking_and_finance_crowdfunding",
            "topic_max_banking_and_finance_cryptocurrency",
            "topic_max_banking_and_finance_general_insurance",
            "topic_max_banking_and_finance_life_insurance",
            "topic_max_banking_and_finance_loan_needs",
            "topic_max_banking_and_finance_loan_pickers",
            "topic_max_banking_and_finance_mobile_banking",
            "topic_max_banking_and_finance_pension",
            "topic_max_banking_and_finance_stock_investors",
            "topic_max_banking_and_finance_tax_and_accounting",
            "topic_max_beauty_and_wellness_beauty_mavens",
            "topic_max_beauty_and_wellness_childbirth",
            "topic_max_beauty_and_wellness_health_care",
            "topic_max_beauty_and_wellness_medicine_and_health_supplement",
            "topic_max_dining_pub_and_bar",
            "topic_max_education_child_education",
            "topic_max_education_learning",
            "topic_max_education_student_education",
            "topic_max_fashion_accessories",
            "topic_max_fashion_brand_fashion",
            "topic_max_fashion_designers",
            "topic_max_fashion_sports_and_outdoor",
            "topic_max_fashion_trend_fashion",
            "topic_max_fashion_women_trend_fashion",
            "topic_max_food_and_dining_30_minute_chefs",
            "topic_max_food_and_dining_bakery_hunters",
            "topic_max_food_and_dining_cafe_regulars",
            "topic_max_food_and_dining_family_restaurant_and_buffet",
            "topic_max_food_and_dining_fastfood_cravers",
            "topic_max_food_and_dining_food_ordering",
            "topic_max_food_and_dining_foodies",
            "topic_max_food_and_dining_k_food_lovers",
            "topic_max_food_and_dining_pizza_lovers",
            "topic_max_food_and_dining_pub_and_bar",
            "topic_max_food_and_dining_western_food",
            "topic_max_home_home_deco",
            "topic_max_home_home_maintanence",
            "topic_max_home_living_items",
            "topic_max_industry_business",
            "topic_max_industry_civil_service",
            "topic_max_industry_construction",
            "topic_max_industry_distribution_industry",
            "topic_max_industry_enterprise_employee",
            "topic_max_industry_florist",
            "topic_max_industry_food",
            "topic_max_industry_funeral",
            "topic_max_industry_heating",
            "topic_max_industry_internet_and_it",
            "topic_max_industry_laundry",
            "topic_max_industry_living_services",
            "topic_max_industry_logistics___drivers",
            "topic_max_industry_manufacturing",
            "topic_max_industry_office_stationery",
            "topic_max_industry_optician",
            "topic_max_industry_printing",
            "topic_max_industry_public_affairs",
            "topic_max_industry_real_estate",
            "topic_max_industry_rental",
            "topic_max_industry_retail",
            "topic_max_industry_security",
            "topic_max_industry_wedding",
            "topic_max_lifestyle_and_hobbies_amusement_parks_and_water_parks",
            "topic_max_lifestyle_and_hobbies_camping",
            "topic_max_lifestyle_and_hobbies_child_care",
            "topic_max_lifestyle_and_hobbies_community_mania",
            "topic_max_lifestyle_and_hobbies_cycling",
            "topic_max_lifestyle_and_hobbies_fishing",
            "topic_max_lifestyle_and_hobbies_gambling_and_lottery",
            "topic_max_lifestyle_and_hobbies_information",
            "topic_max_lifestyle_and_hobbies_international_communication",
            "topic_max_lifestyle_and_hobbies_leisure",
            "topic_max_lifestyle_and_hobbies_license",
            "topic_max_lifestyle_and_hobbies_membership_and_point",
            "topic_max_lifestyle_and_hobbies_mobile_contents",
            "topic_max_lifestyle_and_hobbies_news",
            "topic_max_lifestyle_and_hobbies_pet",
            "topic_max_lifestyle_and_hobbies_photo",
            "topic_max_lifestyle_and_hobbies_political_party",
            "topic_max_lifestyle_and_hobbies_religion",
            "topic_max_lifestyle_and_hobbies_searching_jobs",
            "topic_max_lifestyle_and_hobbies_seeking_date",
            "topic_max_lifestyle_and_hobbies_sharing_platform",
            "topic_max_lifestyle_and_hobbies_social_media",
            "topic_max_lifestyle_and_hobbies_spa_lover",
            "topic_max_lifestyle_and_hobbies_univ_student",
            "topic_max_lifestyle_and_hobbies_fortune_telling",
            "topic_max_media_and_entertainment_back_up_photos_to_the_cloud",
            "topic_max_media_and_entertainment_book_lovers",
            "topic_max_media_and_entertainment_contents_discount",
            "topic_max_media_and_entertainment_gamer",
            "topic_max_media_and_entertainment_movie_theater_audience",
            "topic_max_media_and_entertainment_music_lovers",
            "topic_max_media_and_entertainment_ott_users",
            "topic_max_media_and_entertainment_video_sharing_and_podcast",
            "topic_max_media_and_entertainment_webtoon_and_novel",
            "topic_max_media_and_entertainment_pay_for_media_content",
            "topic_max_shoppers_cvs_mania",
            "topic_max_shoppers_department_store_customer",
            "topic_max_shoppers_design_items",
            "topic_max_shoppers_dutyfree",
            "topic_max_shoppers_early_morning_delivery",
            "topic_max_shoppers_electronics",
            "topic_max_shoppers_fresh_foods",
            "topic_max_shoppers_health_care",
            "topic_max_shoppers_homeshopping_lovers",
            "topic_max_shoppers_luxury_shopper",
            "topic_max_shoppers_malling",
            "topic_max_shoppers_mart_mania",
            "topic_max_shoppers_mobile_payment",
            "topic_max_shoppers_mobile_shoppers",
            "topic_max_shoppers_on_site_shopping",
            "topic_max_shoppers_overseas_purchase",
            "topic_max_shoppers_pantry_staples",
            "topic_max_shoppers_picky_shopper",
            "topic_max_shoppers_used_item",
            "topic_max_sport_and_fitness_fitness",
            "topic_max_sport_and_fitness_golfers",
            "topic_max_sport_and_fitness_sport_equipments",
            "topic_max_sports_and_fitness_diet",
            "topic_max_technology_need_electro_a_s",
            "topic_max_technology_skt_service",
            "topic_max_technology_telecom",
            "topic_max_technology_utility",
            "topic_max_travel_air_travel",
            "topic_max_travel_hotel_and_stay",
            "topic_max_travel_park_lover",
            "topic_max_travel_travel_buffs",
            "topic_max_vehicle_and_transportation_gas_station",
            "topic_max_vehicles_and_transportation_call_taxi",
            "topic_max_vehicles_and_transportation_car_maintenance",
            "topic_max_vehicles_and_transportation_harbor_ship",
            "topic_max_vehicles_and_transportation_need_to_substitute_drivers",
            "topic_max_vehicles_and_transportation_rail_and_bus",
            "topic_max_vehicles_and_transportation_rent_a_car",
            "topic_max_vehicles_and_transportation_looking_for_a_car",
            "topic_cnt_banking_and_finance_bank_visitor",
            "topic_cnt_banking_and_finance_call_to_bank",
            "topic_cnt_banking_and_finance_call_to_customer_service",
            "topic_cnt_banking_and_finance_card_app_users",
            "topic_cnt_banking_and_finance_crowdfunding",
            "topic_cnt_banking_and_finance_cryptocurrency",
            "topic_cnt_banking_and_finance_general_insurance",
            "topic_cnt_banking_and_finance_life_insurance",
            "topic_cnt_banking_and_finance_loan_needs",
            "topic_cnt_banking_and_finance_loan_pickers",
            "topic_cnt_banking_and_finance_mobile_banking",
            "topic_cnt_banking_and_finance_pension",
            "topic_cnt_banking_and_finance_stock_investors",
            "topic_cnt_banking_and_finance_tax_and_accounting",
            "topic_cnt_beauty_and_wellness_beauty_mavens",
            "topic_cnt_beauty_and_wellness_childbirth",
            "topic_cnt_beauty_and_wellness_health_care",
            "topic_cnt_beauty_and_wellness_medicine_and_health_supplement",
            "topic_cnt_dining_pub_and_bar",
            "topic_cnt_education_child_education",
            "topic_cnt_education_learning",
            "topic_cnt_education_student_education",
            "topic_cnt_fashion_accessories",
            "topic_cnt_fashion_brand_fashion",
            "topic_cnt_fashion_designers",
            "topic_cnt_fashion_sports_and_outdoor",
            "topic_cnt_fashion_trend_fashion",
            "topic_cnt_fashion_women_trend_fashion",
            "topic_cnt_food_and_dining_30_minute_chefs",
            "topic_cnt_food_and_dining_bakery_hunters",
            "topic_cnt_food_and_dining_cafe_regulars",
            "topic_cnt_food_and_dining_family_restaurant_and_buffet",
            "topic_cnt_food_and_dining_fastfood_cravers",
            "topic_cnt_food_and_dining_food_ordering",
            "topic_cnt_food_and_dining_foodies",
            "topic_cnt_food_and_dining_k_food_lovers",
            "topic_cnt_food_and_dining_pizza_lovers",
            "topic_cnt_food_and_dining_pub_and_bar",
            "topic_cnt_food_and_dining_western_food",
            "topic_cnt_home_home_deco",
            "topic_cnt_home_home_maintanence",
            "topic_cnt_home_living_items",
            "topic_cnt_industry_business",
            "topic_cnt_industry_civil_service",
            "topic_cnt_industry_construction",
            "topic_cnt_industry_distribution_industry",
            "topic_cnt_industry_enterprise_employee",
            "topic_cnt_industry_florist",
            "topic_cnt_industry_food",
            "topic_cnt_industry_funeral",
            "topic_cnt_industry_heating",
            "topic_cnt_industry_internet_and_it",
            "topic_cnt_industry_laundry",
            "topic_cnt_industry_living_services",
            "topic_cnt_industry_logistics___drivers",
            "topic_cnt_industry_manufacturing",
            "topic_cnt_industry_office_stationery",
            "topic_cnt_industry_optician",
            "topic_cnt_industry_printing",
            "topic_cnt_industry_public_affairs",
            "topic_cnt_industry_real_estate",
            "topic_cnt_industry_rental",
            "topic_cnt_industry_retail",
            "topic_cnt_industry_security",
            "topic_cnt_industry_wedding",
            "topic_cnt_lifestyle_and_hobbies_amusement_parks_and_water_parks",
            "topic_cnt_lifestyle_and_hobbies_camping",
            "topic_cnt_lifestyle_and_hobbies_child_care",
            "topic_cnt_lifestyle_and_hobbies_community_mania",
            "topic_cnt_lifestyle_and_hobbies_cycling",
            "topic_cnt_lifestyle_and_hobbies_fishing",
            "topic_cnt_lifestyle_and_hobbies_gambling_and_lottery",
            "topic_cnt_lifestyle_and_hobbies_information",
            "topic_cnt_lifestyle_and_hobbies_international_communication",
            "topic_cnt_lifestyle_and_hobbies_leisure",
            "topic_cnt_lifestyle_and_hobbies_license",
            "topic_cnt_lifestyle_and_hobbies_membership_and_point",
            "topic_cnt_lifestyle_and_hobbies_mobile_contents",
            "topic_cnt_lifestyle_and_hobbies_news",
            "topic_cnt_lifestyle_and_hobbies_pet",
            "topic_cnt_lifestyle_and_hobbies_photo",
            "topic_cnt_lifestyle_and_hobbies_political_party",
            "topic_cnt_lifestyle_and_hobbies_religion",
            "topic_cnt_lifestyle_and_hobbies_searching_jobs",
            "topic_cnt_lifestyle_and_hobbies_seeking_date",
            "topic_cnt_lifestyle_and_hobbies_sharing_platform",
            "topic_cnt_lifestyle_and_hobbies_social_media",
            "topic_cnt_lifestyle_and_hobbies_spa_lover",
            "topic_cnt_lifestyle_and_hobbies_univ_student",
            "topic_cnt_lifestyle_and_hobbies_fortune_telling",
            "topic_cnt_media_and_entertainment_back_up_photos_to_the_cloud",
            "topic_cnt_media_and_entertainment_book_lovers",
            "topic_cnt_media_and_entertainment_contents_discount",
            "topic_cnt_media_and_entertainment_gamer",
            "topic_cnt_media_and_entertainment_movie_theater_audience",
            "topic_cnt_media_and_entertainment_music_lovers",
            "topic_cnt_media_and_entertainment_ott_users",
            "topic_cnt_media_and_entertainment_video_sharing_and_podcast",
            "topic_cnt_media_and_entertainment_webtoon_and_novel",
            "topic_cnt_media_and_entertainment_pay_for_media_content",
            "topic_cnt_shoppers_cvs_mania",
            "topic_cnt_shoppers_department_store_customer",
            "topic_cnt_shoppers_design_items",
            "topic_cnt_shoppers_dutyfree",
            "topic_cnt_shoppers_early_morning_delivery",
            "topic_cnt_shoppers_electronics",
            "topic_cnt_shoppers_fresh_foods",
            "topic_cnt_shoppers_health_care",
            "topic_cnt_shoppers_homeshopping_lovers",
            "topic_cnt_shoppers_luxury_shopper",
            "topic_cnt_shoppers_malling",
            "topic_cnt_shoppers_mart_mania",
            "topic_cnt_shoppers_mobile_payment",
            "topic_cnt_shoppers_mobile_shoppers",
            "topic_cnt_shoppers_on_site_shopping",
            "topic_cnt_shoppers_overseas_purchase",
            "topic_cnt_shoppers_pantry_staples",
            "topic_cnt_shoppers_picky_shopper",
            "topic_cnt_shoppers_used_item",
            "topic_cnt_sport_and_fitness_fitness",
            "topic_cnt_sport_and_fitness_golfers",
            "topic_cnt_sport_and_fitness_sport_equipments",
            "topic_cnt_sports_and_fitness_diet",
            "topic_cnt_technology_need_electro_a_s",
            "topic_cnt_technology_skt_service",
            "topic_cnt_technology_telecom",
            "topic_cnt_technology_utility",
            "topic_cnt_travel_air_travel",
            "topic_cnt_travel_hotel_and_stay",
            "topic_cnt_travel_park_lover",
            "topic_cnt_travel_travel_buffs",
            "topic_cnt_vehicle_and_transportation_gas_station",
            "topic_cnt_vehicles_and_transportation_call_taxi",
            "topic_cnt_vehicles_and_transportation_car_maintenance",
            "topic_cnt_vehicles_and_transportation_harbor_ship",
            "topic_cnt_vehicles_and_transportation_need_to_substitute_drivers",
            "topic_cnt_vehicles_and_transportation_rail_and_bus",
            "topic_cnt_vehicles_and_transportation_rent_a_car",
            "topic_cnt_vehicles_and_transportation_looking_for_a_car",
            "online_shopping_cnt",
            "online_shopping_duration",
            "online_shopping_order_cnt",
            "credit_card_cnt",
            "credit_card_use_cnt",
            "residence_lowprice_own",
            "residence_lowprice_rent",
            "residence_midprice_own",
            "residence_midprice_rent",
            "residence_midhighprice_norm",
            "residence_highprice_norm",
            "subscription_app_cnt",
            "subscription_cat_cnt",
            "subscription_max_use_dt",
            "subscription_pay_sum",
            "subscription_pay_avg",
            "subscription_real_use_cnt",
            "hday_n_loc_cnt",
            "hday_y_loc_cnt",
            "hday_n_tot_move_cnt",
            "hday_n_tot_move_distance",
            "hday_y_tot_move_cnt",
            "hday_y_tot_move_distance",
            "move_type_taxi_cnt",
            "move_type_navi_cnt",
            "move_type_subway_cnt",
            "move_type_train_cnt",
            "move_type_intl_flight_cnt",
            "move_type_dome_flight_cnt",
            "fmly_memb_cnt",
            "hhld_memb_cnt",
            "call_duration_fmly",
            "call_cnt_fmly",
            "call_duration_hhld",
            "call_cnt_hhld",
            "fmly_decision_maker_yn",
            "hhld_decision_maker_yn",
            "bf_1m_int_call_cnt",
            "bf_1m_int_call_duration",
            "bf_1m_int_call_amt",
        ],
    ):
        assert isinstance(model_name, str), "`model_name`은 str 타입이어야 합니다."
        assert isinstance(model_version, str), "`model_version`은 str 타입이어야 합니다."
        assert isinstance(target_df, DataFrame), "`target_data`은 Pandas DataFrame 타입이어야 합니다."
        assert isinstance(features, list), "`features`은 list 타입이어야 합니다."

        bq = get_bigquery_client()
        try:
            target_df = target_df.astype({"label": "int"})
        except Exception as e:
            raise MLSModelError(f"EurekaModel: target_df의 label의 int 타입 변환에 실패했습니다. {e}")
        columns = ["user_id" if "svc_mgmt_num" == i else i for i in target_df.columns]
        target_df.columns = columns
        for i in ["user_id", "label"]:
            assert i in target_df.columns, f"target_df 에 `{i}` 컬럼이 없습니다."
        if "ym" in target_df.columns:
            try:
                pandas_to_bq_table(pd_df=target_df, dataset="temp_1d", table_name=f"{model_name}")
            except Exception as e:
                raise MLSModelError(f"EurekaModel: target_df의 업로드에 실패했습니다. {e}")
        else:
            try:
                pandas_to_bq_table(pd_df=target_df, dataset="temp_1d", table_name=f"{model_name}_temp")
            except Exception as e:
                raise MLSModelError(f"EurekaModel: target_df의 업로드에 실패했습니다. {e}")
            max_ym = bq_to_pandas(f"SELECT MAX(ym) FROM {PROJECT_ID}.{mls_feature_store_path}")
            bq.query(f"DROP TABLE IF EXISTS {PROJECT_ID}.temp_1d.{model_name}").result()
            query = f"""
            CREATE TABLE IF NOT EXISTS {PROJECT_ID}.temp_1d.{model_name} AS
            SELECT user_id, label, {max_ym.values[0][0]} AS ym FROM {PROJECT_ID}.temp_1d.{model_name}_temp
            """
            bq.query(query).result()
            bq.query(f"DROP TABLE IF EXISTS {PROJECT_ID}.temp_1d.{model_name}_temp").result()

        available_features = [f"{i}" for i in features]
        feature_list_query = ", ".join(available_features)

        if target_df["label"].nunique() == 1:
            assert target_df["label"].unique()[0] == 1, "`target_data`의 정답을 1개만 줄거라면 1만 입력되어야 합니다."

            try:
                bq.query(f"DROP TABLE IF EXISTS {PROJECT_ID}.temp_1d.{model_name}_label1").result()
                query = f"""
                CREATE TABLE IF NOT EXISTS {PROJECT_ID}.temp_1d.{model_name}_label1 AS
                SELECT label_1.*
                  FROM (SELECT target.user_id
                             , target.label
                             , {feature_list_query}
                          FROM (SELECT * FROM {PROJECT_ID}.{mls_feature_store_path}) AS features
                         INNER JOIN (SELECT * FROM {PROJECT_ID}.temp_1d.{model_name}) AS target
                            ON features.ym = target.ym
                           AND features.svc_mgmt_num = target.user_id) AS label_1
                """
                bq.query(query).result()
                cnts = bq_to_pandas(f"SELECT COUNT(*) FROM {PROJECT_ID}.temp_1d.{model_name}_label1")

                bq.query(f"DROP TABLE IF EXISTS {PROJECT_ID}.temp_1d.{model_name}_{model_version}").result()
                query = f"""
                CREATE TABLE IF NOT EXISTS {PROJECT_ID}.temp_1d.{model_name}_{model_version} AS
                SELECT label_1.*
                  FROM {PROJECT_ID}.temp_1d.{model_name}_label1 AS label_1
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
                                          FROM {PROJECT_ID}.{mls_feature_store_path}
                                         WHERE ym IN (SELECT MAX(ym) FROM {PROJECT_ID}.{mls_feature_store_path})) AS features
                                  LEFT JOIN (SELECT * FROM {PROJECT_ID}.temp_1d.{model_name}) AS target
                                    ON features.svc_mgmt_num = target.user_id
                                 WHERE target.user_id IS NULL) AS shuffle
                         WHERE rnd <= {cnts.values[0][0]}) AS label_2
                """  # noqa: W291
                bq.query(query).result()
            except Exception as e:
                raise MLSModelError(f"EurekaModel: 데이터 생성에 실패했습니다. {e}")
        else:
            try:
                bq.query(f"DROP TABLE IF EXISTS {PROJECT_ID}.temp_1d.{model_name}_{model_version}").result()
                query = f"""
                CREATE TABLE {PROJECT_ID}.temp_1d.{model_name}_{model_version} AS
                SELECT target.user_id
                     , target.label
                     , {feature_list_query}
                  FROM (SELECT *
                          FROM {PROJECT_ID}.{mls_feature_store_path}) AS features
                 INNER JOIN (SELECT * FROM {PROJECT_ID}.temp_1d.{model_name}) AS target
                    ON features.ym = target.ym
                   AND features.svc_mgmt_num = target.user_id
                """
                bq.query(query).result()
            except Exception as e:
                raise MLSModelError(f"EurekaModel: 데이터 생성에 실패했습니다. {e}")

        self.model_name = model_name
        self.model_version = model_version
        self.features = features
        self.destination = f"{PROJECT_ID}.temp_1d.{model_name}_{model_version}"

    def GetTrainDataQuery(self):
        return f"SELECT * FROM {self.destination}"
