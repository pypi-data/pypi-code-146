from connectors_to_databases.ClickHouse import ClickHouse

ch = ClickHouse(
    login='click',
    password='click',
)

print(ch.execute_to_df('''select 1 as one'''))