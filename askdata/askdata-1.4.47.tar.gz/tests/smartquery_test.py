import jsons
from askdata.smartquery import *

if __name__ == '__main__':
    # TEST SmartQuery Object
    field1 = Field(column='{{measure.A}}', aggregation="MAX", dataset='{{dataset.A}}', entityType="P_MEASURE", alias="max_measure")
    field2 = Field(column='{{dimension.A}}', dataset='{{dataset.B}}', entityType="P_DIMENSION")
    field3 = Field(column='{{timeDimension.A}}', dataset='{{dataset.C}}', entityType="P_TIMEDIM", aggregation="year")
    field4 = Field(column="{{unknownDateDimension.A}}")
    field5 = Field(complexExpression="A is better than B")
    from1 = From('{{dataset.A}}')
    from2 = From('{{dataset.B}}')
    from3 = From('{{dataset.C}}')
    condition1 = Condition(field4, "FROM", direction="NEXT", negate=True, steps="{{number.A}}",
                           interval="{{timeDimension.B}}", value=["{{contextTimeStart.A}}", "{{contextTimeEnd.A}}"])
    condition2 = Condition(field1, "LOE", ["{{number.B}}"])
    condition3 = Condition(field2, "IN", ["{{entity.A}}"])
    condition4 = Condition(field4, "RANGE", value=["{{timePeriodStart.A}}", "{{timePeriodEnd.A}}"])
    condition5 = Condition(field5)
    sorting1 = Sorting("{{measure.A}}", SQLSorting.DESC)
    component = ChartComponent(type='chart', queryId="0", chartType='LINE')
    query1 = Query(fields=[field1, field2, field3], datasets=[from1, from2, from3], where=[condition1, condition2, condition3, condition4, condition5],
                   orderBy=[sorting1], limit=10)
    print(query1.to_sql())
    smartquery = SmartQuery(queries=[query1], components=[component])
    dump = jsons.dumps(smartquery)
    print(dump)
    smartquery = jsons.loads(dump, SmartQuery)
    print(jsons.dumps(smartquery, strip_nulls=True))
    print(smartquery)
    print(smartquery.queries[0].to_sql())
    # print("ORIGINAL JSON: ", dump)
    # compressed_json = SmartQuery.compress(dump)
    # print("COMPRESSED JSON: ", compressed_json)
    # decompressed_json = SmartQuery.decompress(compressed_json)
    # print("DECOMPRESSED JSON: ", decompressed_json)
    # print(str(dump) == decompressed_json)

    # TEST SPELL OUT
    # smartquery spell_out
    sq = SmartQuery(queries=[Query(
        fields=[Field(column="store_city", alias="Store City", internalDataType="STRING", sourceDataType="TEXT"),
                Field(column="time_the_date", alias="Time", internalDataType="DATE", sourceDataType="TEXT")],
        where=[Condition(Field(column="time_the_date", aggregation="MONTH", alias="Time", internalDataType="DATE", sourceDataType="TEXT"),
                         operator="FROM", direction="NEXT", steps="2", value=["November", "December"]),
               Condition(Field(column="time_the_date", aggregation="MONTH", alias="Time", internalDataType="DATE",
                               sourceDataType="TEXT"),
                         operator="FROM", value=["2022"]),
               Condition(Field(column="units shipped", aggregation="MAX", alias="max_units_shipped", internalDataType="NUMERIC",
                               sourceDataType="REAL"),
                         operator="GOE", value=["100"]),
               Condition(Field(complexExpression="sum units shipped & 10 > 10", alias="sum_units_shipped",
                               internalDataType="NUMERIC",
                               sourceDataType="REAL"))
               ],
        groupBy=[GroupBy(field=Field(column="time_the_date", alias="Time", internalDataType="DATE", sourceDataType="TEXT"))],
        orderBy=[Sorting(field="Store City", order=SQLSorting.DESC),
                 Sorting(field="Time", order=SQLSorting.DESC)],
        limit=8,
        offset=0
    )])
    print(sq.spell_out())
