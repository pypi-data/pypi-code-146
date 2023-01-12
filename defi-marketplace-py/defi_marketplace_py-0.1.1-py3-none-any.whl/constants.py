class Commands:
    INSTALL_CLI = 'npm install -g @nevermined-io/cli'
    CLI_HELP = 'ncli --help'
    DOWNLOAD_ARTIFACTS = 'ncli utils download-artifacts {version} --networkId {networkId} --tag public --destination {destination}'
    LIST_ASSETS = 'ncli assets query {query} -n {network} --page {page} --json --onlyMetadata --offset 30'
    DOWNLOAD_DID = 'ncli -n {network} -v nfts721 access {did} --destination {destination} --accountIndex {accountIndex} --json'
    PUBLISH_ASSET = """ncli -n {network} -v nfts721 create {nftAddress} --metadata {metadata} --services nft-access --json"""
    UPLOAD_TO_FILECOIN = 'ncli utils upload {file_path} --json'


class AddressProvider:
    NFT_SUBSCRIPTION = {
        'local': '0xEBe77E16736359Bf0F9013F6017242a5971cAE76',
        'Mumbai': '0x95Ba21f858b57beb7B19990E8B072EF52999856D'
    }
    GATEWAY_HOST = {
        'local': 'http://localhost:8030',
        'Mumbai': 'https://node.mumbai.public.nevermined.network'
    }


class NetworkValues:
    ARTIFACTS_VERSION = {
        'local': '2.1.0',
        'Mumbai': '2.1.0'
    }

    NETWORKD_ID = {
        'local': '80001',
        'Mumbai': '80001'
    }

    ARTIFACTS_FOLDER = '/tmp'


class Values:
    MAX_WORKERS = 10


class Nevermined:
    METADATA = {
        "curation": {
            "rating": 0,
            "numVotes": 0,
            "isListed": True
        },
        "main": {
            "name": "fileName",
            "dateCreated": "dateCreated",
            "author": "Nevermined AG",
            "license": "CC0: Public Domain",
            "price": "price",
            "datePublished": "datePublished",
            "files": [
                {
                    "index": 0,
                    "contentType": "text/csv",
                    "contentLength": "contentLength",
                    "url": "url",
                    "name": "filename",
                }
            ],
            "type": "dataset"
        },
        "additionalInformation": {
            "description": "description",
            "source": "filecoin",
            "file_name": "filename",
            "customData": {
                "subtype": "dataset"
            },
            "categories":[
                "UseCase:defi-datasets"
            ]
        },
    }
