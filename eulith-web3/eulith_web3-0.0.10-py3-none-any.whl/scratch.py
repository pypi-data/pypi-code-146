from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3

ew3 = EulithWeb3(eulith_url="https://eth-goerli.eulithrpc.com/v0",
                 eulith_refresh_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ.eyJzdWIiOiJyYWNlciIsImV4cCI6MTcwMzg2NzY2OSwic291cmNlX2hhc2giOiIqIiwic2NvcGUiOiJBUElSZWZyZXNoIn0.etl63gdCAF97AyotM9bmKcznu8LgpMZrVIVpF0S_4Z4TLiDDD3TbljhCdO_H5pzyaFpW4luHI9Jo36-cnxWL7Rw")

link = ew3.eulith_get_erc_token(TokenSymbol.LINK)
print(link.address)
