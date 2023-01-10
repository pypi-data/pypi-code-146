from syncqb import qb_client

def main():
    client = qb_client.get_client(True, creds={
        'QB_URL': 'https://rmcgroup.quickbase.com',
        'USER_TOKEN': 'b46fjf_ictm_0_c6ikfnbcer5zzpcvkhaynddjctsq'
    })

    response = client.do_query(query='{3.GT.8075}', columns=[3, 6], database='bpxua87ct', sort=[6, 3], ascending=False)

    print(response)



if __name__ == '__main__':
    main()