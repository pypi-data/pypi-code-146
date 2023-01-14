import SaleOrder.rdsalesorder.mainModel as srm

if __name__ == '__main__':

    # option1 = {
    #     "acct_id": '63310e555e38b1',
    #     "user_name": '张志',
    #     "app_id": '234673_6darRxsuzoGe5U+t5+WCVZ/KTNQY5Nnv',
    #     "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
    #     "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    # }

    # 新账套

    option1 = {
        "acct_id": '62777efb5510ce',
        "user_name": '张志',
        "app_id": '235685_4e6vScvJUlAf4eyGRd3P078v7h0ZQCPH',
        # "app_sec": 'd019b038bc3c4b02b962e1756f49e179',
        "app_sec": 'b105890b343b40ba908ed51453940935',
        "server_url": 'http://cellprobio.gnway.cc/k3cloud',
    }

    srm.perform(option1,"","")

