Q_FEATURES = """
select
    sb.id as "short-book-1-id" ,
	sb."ordered-distributor-id" as "short-book-distributor-id",
	sb."drug-id",
	coalesce(sb.quantity, 0) as "original-order",
	sb."required-quantity" as "final-unfulfilled",
	sb."created-at" as "original-created-at",
	sb."re-ordered-at" as "original-created-at-2",
	sbi."quantity" as "partial-quantity",
	i.id as "invoice-id",
	i."dc-id" as "partial-dc-id",
	i."distributor-id" as "partial-distributor-id",
	i."created-at" as "partial-created-at",
	i."approved-at" as "partial-invoiced-at",
	ii.id as "invoice-item-id",
	ii."drug-id" as "invoice-items-drug-id",
	inv.id as "inventory-id",
	inv."invoice-item-id" as "inv-invoice-item-id",
	inv."purchase-rate" as "distributor-rate",
	inv."selling-rate",
	inv."mrp",
	d."drug-name",
	d.type as "drug_type",
	sdm."forward-dc-id",
	s.name as "dc-name"
from
	"{schema}"."short-book-1" sb
left join "{schema}"."short-book-invoices" sbi on
	sbi."short-book-id" = sb.id
left join "{schema}".invoices i on
	sbi."invoice-id" = i.id
left join "{schema}"."short-book-invoice-items" sbii on
	sb.id = sbii."short-book-id"
left join "{schema}"."invoice-items" ii on
	ii.id = sbii."invoice-item-id"
left join "{schema}"."invoice-items-1" ii1 on
	ii1."invoice-item-reference" = ii.id
left join "{schema}"."inventory-1" inv on
	inv."invoice-item-id" = ii1.id
left join "{schema}".drugs d on
	sb."drug-id" = d.id
left join "{schema}".distributors dis on
	dis.id = sb."ordered-distributor-id"
left join "{schema}"."store-dc-mapping" sdm on
	sb."store-id" = sdm."store-id"
	and dis.type = sdm."drug-type"
left join "{schema}".stores s on
	i."dc-id" = s.id
where
	DATEDIFF(day, date(sb."created-at"), '{reset_date}') <= {time_interval} 
	and DATEDIFF(day, date(sb."created-at"), '{reset_date}') >= 7
	and sb."quantity" > 0
	and sb."ordered-distributor-id" != 76
	and sb."ordered-distributor-id" != 5000
	and sb."ordered-distributor-id" != 8105
	and i."distributor-id" != 8105
	and sb.status != 'deleted'
	and sb."store-id" in (2,4,7,16,54,82,231,234,244,278,297,23,28,39,216,218,235,229,280,8,13,21,26,31,45,188,208,221,222,230,241,260,264,20,36,61,134,160,184,195,215,224,226,245,252,273,281)
"""
# (2,4,7,16,54,82,231,234,244,278,297,23,28,39,216,218,235,229,280,8,13,21,26,31,45,188,208,221,222,230,241,260,264,20,36,61,134,160,184,195,215,224,226,245,252,273,281)

Q_FEATURES_FRANCHISEE = """
select
    sb.id as "short-book-1-id" ,
    sb."ordered-distributor-id" as "short-book-distributor-id",
    sb."store-id",
    ss."franchisee-id",
    sb."drug-id",
    coalesce(sb.quantity, 0) as "original-order",
    sb."required-quantity" as "final-unfulfilled",
    sb."created-at" as "original-created-at",
    sb."re-ordered-at" as "original-created-at-2",
	sbi."quantity" as "partial-quantity",
	i.id as "invoice-id",
	i."distributor-id" as "partial-distributor-id",
	i."created-at" as "partial-created-at",
	i."approved-at" as "partial-invoiced-at",
	ii.id as "invoice-item-id",
	ii."drug-id" as "invoice-items-drug-id",
	inv.id as "inventory-id",
	inv."invoice-item-id" as "inv-invoice-item-id",
	inv."purchase-rate" as "distributor-rate",
	inv."selling-rate",
	inv."mrp",
	d."drug-name",
	d.type as "drug_type",
    ss."name" as "store-name"
from
	"{schema}"."short-book-1" sb
left join "{schema}"."short-book-invoices" sbi on
	sbi."short-book-id" = sb.id
left join "{schema}".invoices i on
	sbi."invoice-id" = i.id
left join "{schema}"."short-book-invoice-items" sbii on
	sb.id = sbii."short-book-id"
left join "{schema}"."invoice-items" ii on
	ii.id = sbii."invoice-item-id"
left join "{schema}"."invoice-items-1" ii1 on
	ii1."invoice-item-reference" = ii.id
left join "{schema}"."inventory-1" inv on
	inv."invoice-item-id" = ii1.id
left join "{schema}".drugs d on
	sb."drug-id" = d.id
left join "{schema}".distributors dis on
	dis.id = sb."ordered-distributor-id"
left join "{schema}".stores s on
    i."dc-id" = s.id
left join "{schema}".stores ss on
    sb."store-id" = ss.id 
where
    DATEDIFF(day, date(sb."created-at"), '{reset_date}') <= {time_interval} 
	and DATEDIFF(day, date(sb."created-at"), '{reset_date}') >= 7
	and sb."quantity" > 0
	and sb."ordered-distributor-id" != 76
	and sb."ordered-distributor-id" != 5000
	and sb."ordered-distributor-id" != 8105
	and i."distributor-id" != 8105
    and sb.status != 'deleted' 
    and ss."franchisee-id" != 1
    {franchisee_stores_execute_query}
"""

Q_DISTRIBUTORS = """
select db.id as "partial-distributor-id", 
    db.name as "partial-distributor-name", 
    db."credit-period" as "partial-distributor-credit-period", 
    d."type" as "drug-type", count(distinct dd."drug-id") as "dist-type-portfolio-size"
from "{schema}".distributors db
    left join "{schema}"."distributor-drugs" dd on db.id = dd."distributor-id" 
    left join "{schema}".drugs d on dd."drug-id" = d.id 
    group by "partial-distributor-id", "partial-distributor-name", 
        "partial-distributor-credit-period", "drug-type"
"""

Q_DC_DISTRIBUTOR_MAPPING = """
select "dc-id" as "partial-dc-id", "distributor-id" as "partial-distributor-id"
from "{schema}"."dc-distributor-mapping" ddm 
where "is-active" = 1
group by "dc-id" , "distributor-id"
"""

Q_DISTRIBUTOR_DRUGS = """
select "distributor-id" as "partial-distributor-id" , "drug-id" 
from "{schema}"."distributor-drugs" dd 
group by "distributor-id" , "drug-id"
"""


def pull_data_dc(reset_date, time_interval, db, schema):
    df_features = db.get_df(Q_FEATURES.format(
        reset_date=reset_date, time_interval=time_interval, schema=schema))
    df_features.columns = [c.replace('-', '_') for c in df_features.columns]

    df_distributors = db.get_df(Q_DISTRIBUTORS.format(schema=schema))
    df_distributors.columns = [c.replace('-', '_') for c in df_distributors.columns]
    df_distributors = df_distributors.dropna()
    df_distributors = df_distributors.loc[df_distributors["drug_type"] != '']

    df_dc_distributors_mapping = db.get_df(Q_DC_DISTRIBUTOR_MAPPING.format(schema=schema))
    df_dc_distributors_mapping.columns = [c.replace('-', '_') for c in
                                          df_dc_distributors_mapping.columns]

    df_distributor_drugs = db.get_df(Q_DISTRIBUTOR_DRUGS.format(schema=schema))
    df_distributor_drugs.columns = [c.replace('-', '_') for c in
                                    df_distributor_drugs.columns]
    df_distributor_drugs.drop_duplicates(inplace=True)

    # ensure data types
    df_features["distributor_rate"] = df_features["distributor_rate"].astype(float)
    df_features["selling_rate"] = df_features["selling_rate"].astype(float)
    df_features["mrp"] = df_features["mrp"].astype(float)

    return df_features, df_distributors, df_dc_distributors_mapping, df_distributor_drugs


def pull_data_franchisee(reset_date, time_interval, franchisee_stores,
                         db, schema):
    if franchisee_stores == [0]:
        franchisee_stores_execute_query = ""
    else:
        franchisee_stores_execute_query = f"""
        and sb."store-id" in {str(franchisee_stores).replace('[', '(').replace(']',')')}
        """

    df_features = db.get_df(Q_FEATURES_FRANCHISEE.format(
        reset_date=reset_date, time_interval=time_interval,
        franchisee_stores_execute_query=franchisee_stores_execute_query,
        schema=schema))
    df_features.columns = [c.replace('-', '_') for c in df_features.columns]

    df_distributors = db.get_df(Q_DISTRIBUTORS.format(schema=schema))
    df_distributors.columns = [c.replace('-', '_') for c in df_distributors.columns]
    df_distributors = df_distributors.dropna()

    df_distributor_drugs = db.get_df(Q_DISTRIBUTOR_DRUGS.format(schema=schema))
    df_distributor_drugs.columns = [c.replace('-', '_') for c in
                                    df_distributor_drugs.columns]
    df_distributor_drugs.drop_duplicates(inplace=True)

    # ensure data types
    df_features["distributor_rate"] = df_features["distributor_rate"].astype(float)
    df_features["selling_rate"] = df_features["selling_rate"].astype(float)
    df_features["mrp"] = df_features["mrp"].astype(float)

    return df_features, df_distributors, df_distributor_drugs

