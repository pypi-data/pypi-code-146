# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd

def get_all_protocols():
    # import list of all protocols
    que = requests.get('https://api.llama.fi/protocols')
    data = que.json()
    proto = pd.DataFrame(data)
    return proto

def getDepositRate(util, reserveFactor, brate):
    srate = brate * util * (1 - reserveFactor)
    return (srate)

def getBorrowRate(util, kink1, kink2, multiplierPerSecond, jumpMultiplierPerSecond, baseRatePerSecond, secondsPerYear):
    # if (util <= kink1) {
    #         return util.mul(multiplierPerSecond).div(1e18).add(baseRatePerSecond);
    #     } else if (util <= kink2) {
    #         return kink1.mul(multiplierPerSecond).div(1e18).add(baseRatePerSecond);
    #     } else {
    #         uint256 normalRate = kink1.mul(multiplierPerSecond).div(1e18).add(baseRatePerSecond);
    #         uint256 excessUtil = util.sub(kink2);
    #         return excessUtil.mul(jumpMultiplierPerSecond).div(1e18).add(normalRate);
    #     }

    multiplierPerSecond = multiplierPerSecond * secondsPerYear
    jumpMultiplierPerSecond = jumpMultiplierPerSecond * secondsPerYear

    if (util <= kink1):
        brate = util * multiplierPerSecond / 1e18 + baseRatePerSecond
    elif util <= kink2:
        brate = kink1 * multiplierPerSecond / 1e18 + baseRatePerSecond
    else:
        normalRate = kink1 * multiplierPerSecond / 1e18 + baseRatePerSecond
        excessUtil = util - kink2
        brate = excessUtil * jumpMultiplierPerSecond / 1e18 + normalRate

    return (brate)

def getRate(util, kink1, kink2, multiplierPerSecond, jumpMultiplierPerSecond, baseRatePerSecond, secondsPerYear,
            reserveFactor):
    multiplierPerSecond = multiplierPerSecond * secondsPerYear
    jumpMultiplierPerSecond = jumpMultiplierPerSecond * secondsPerYear
    if (util <= kink1):
        brate = util * multiplierPerSecond / 1e18 + baseRatePerSecond
    elif util <= kink2:
        brate = kink1 * multiplierPerSecond / 1e18 + baseRatePerSecond
    else:
        normalRate = kink1 * multiplierPerSecond / 1e18 + baseRatePerSecond
        excessUtil = util - kink2
        brate = excessUtil * jumpMultiplierPerSecond / 1e18 + normalRate
    srate = brate * util * (1 - reserveFactor)
    return (srate)


def apy_calculator(UR_in):
    kink1 = 800000000000000000
    kink2 = 900000000000000000
    multiplierPerSecond = 5707762557
    jumpMultiplierPerSecond = 253678335870
    baseRatePerSecond = 0
    secondsPerYear = 31536000
    reserveFactor = 0.15

    apy = [getRate(util, kink1, kink2, multiplierPerSecond,
                   jumpMultiplierPerSecond, baseRatePerSecond, secondsPerYear, reserveFactor) for util in UR_in]
    return (apy)

# get the TVL for all tokens
class llama_df():
    def __init__(self, chain_in, chainTvl):
        self.chain_in = chain_in
        self.chainTvl = chainTvl

    # get the dataframe of all tokens in USD per time
    def locked_df(self):
        at = self.chainTvl[self.chain_in]['tokensInUsd'].copy()
        locked = None
        for i in range(len(at)):
            holder = pd.DataFrame(at[i])
            if locked is None:
                locked = holder.copy()
            else:
                locked = pd.concat([locked, holder])

        locked = locked.reset_index()
        #            locked['date'] = locked['date'].apply(lambda x: datetime.strftime(datetime.fromtimestamp(x), '%Y-%m-%d'))
        locked['date'] = pd.to_datetime(locked["date"], unit='s')

        locked_df = locked.pivot(columns='index', index='date')  # do we maybe want a date in the right format as index?
        locked_df = locked_df['tokens']
        locked_df.columns.name = None

        # Only output tokens who are currenly available (the reshaping was also including tokens dropped...)
        ll = len(self.chainTvl[self.chain_in]['tokens']) - 1
        recent_list = pd.DataFrame(self.chainTvl[self.chain_in]['tokens'][ll]).index
        final_list = list(set(list(locked_df.columns)) & set(list(recent_list)))
        locked_df_final = locked_df[final_list]

        return locked_df_final


def request_traderjoe_data():
    # protocolin must be taken from the 'slug' column
    protocol_in = 'trader-joe-lend'
    que = requests.get('https://api.llama.fi/protocol/' + protocol_in)
    tvl_history = que.json()
    # TVL for a specific chain -aggredated
    chain_in = 'Avalanche'
    chainTvl = tvl_history['chainTvls']

    # locked is the TVL
    # borrowed is the amount borrowed
    locked = llama_df(chain_in, chainTvl).locked_df()
    borrowed = llama_df(chain_in + '-borrowed', chainTvl).locked_df()

#    locked.USDC.plot()
    supply_df = locked.copy()
    supply_df.columns = [f'{col}_liquidity' for col in supply_df.columns ]
    # Get total deposits
    totLiq = borrowed + locked
    UR = borrowed / totLiq
    UR.index = pd.to_datetime(UR.index)

    # plot UR for a specific token
#    token_in = 'USDC'
#    UR[token_in].plot(rot=90, title=token_in + ' Utilization Rate - ' + protocol_in)
#    plt.legend(loc='lower left')
#    plt.show()


    # Compute Borrow and Supply Rate
    # https://github.com/traderjoe-xyz/research/blob/main/BankerJoe_DeFi_Leveraged_Trading.pdf
    # https://ianm.com/posts/2020-12-20-understanding-compound-protocols-interest-rates

    # https://help.traderjoexyz.com/en/security-and-contracts/contracts

    # Constants here e.g.from TripleSlopeRateModel (Stablecoins)
    # https://snowtrace.io/address/0x3C5486b85fAAE29B071F2a616a59cA7bF8F73682#readContract

    # Pool stats for e.g. USDC
    # https://snowtrace.io/address/0xEd6AaF91a2B084bd594DBd1245be3691F9f637aC#readContract

    # multi = muliplierPerSecond * secondsPerYear / 1e18

    # constants (kink, baserate, multuplier, reserve factor should come from SC. If not, we infer them from TJ webpage...)




    util = 0.415
    kink1 = 800000000000000000
    kink2 = 900000000000000000
    multiplierPerSecond = 5707762557
    jumpMultiplierPerSecond = 253678335870
    baseRatePerSecond = 0
    secondsPerYear = 31536000

    # Reserve factors from here
    # https://traderjoe-xyz.medium.com/trainer-joe-get-defit-lending-part-1-8780b7810308
    # for stable == 15%
    reserveFactor = 0.15

    brate = getBorrowRate(util, kink1, kink2, multiplierPerSecond, jumpMultiplierPerSecond, baseRatePerSecond,
                          secondsPerYear)
    srate = getDepositRate(util, reserveFactor, brate)

    brate = [getBorrowRate(util, kink1, kink2, multiplierPerSecond,
                           jumpMultiplierPerSecond, baseRatePerSecond, secondsPerYear) for util in UR.USDC]

    UR = UR.assign(BTCB_apy=apy_calculator(UR['BTC.B']))

    UR = UR.assign(USDC_apy=apy_calculator(UR.USDC))
    UR = UR.assign(USDT_apy=apy_calculator(UR.USDT))
    UR = UR.assign(USDCE_apy=apy_calculator(UR['USDC.E']))
    UR = UR.assign(USDTE_apy=apy_calculator(UR['USDT.E']))

    final_df = pd.merge(UR.copy(), supply_df.copy(), left_index=True, right_index=True)
    traderjoe_usdc_df = final_df[['USDC_liquidity', 'USDC_apy']].copy()
    traderjoe_usdt_df = final_df[['USDT_liquidity', 'USDT_apy']].copy()
    traderjoe_btcb_df = final_df[['BTC.B_liquidity', 'BTCB_apy']].copy()
    #    final_df[['USDC.E_liquidity', 'USDC.E', 'USDCE_apy']].copy()
    #    final_df[['USDT.E_liquidity','USDT.E', 'USDTE_apy']].copy()

    traderjoe_usdc_df = traderjoe_usdc_df.rename(columns={'USDC_liquidity': 'supply_liquidity', 'USDC_apy': 'apy'})
    traderjoe_usdt_df = traderjoe_usdt_df.rename(columns={'USDT_liquidity': 'supply_liquidity', 'USDT_apy': 'apy'})
    traderjoe_btcb_df = traderjoe_btcb_df.rename(columns={'BTC.B_liquidity': 'supply_liquidity', 'BTCB_apy': 'apy'})
    return traderjoe_usdc_df, traderjoe_usdt_df, traderjoe_btcb_df


def request_samurai_aave_v3_usdc():
    # https://yieldsamurai.com/pool/avalanche/0x625e7708f30ca75bfd92586e17077590c60eb4cd
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    aave_usdc_payload = {
        "id": "103079215106",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=aave_usdc_payload)
    data_aavev3_usdc_df = pd.DataFrame().from_records(json.loads(x.text))
    data_aavev3_usdc_df['date'] = pd.to_datetime(data_aavev3_usdc_df['timestamp'], unit='ms')
    data_aavev3_usdc_df = data_aavev3_usdc_df.set_index('date')
    data_aavev3_usdc_df['supply_liquidity'] = data_aavev3_usdc_df['tvl']/(1. + data_aavev3_usdc_df['utilization'])
    data_aavev3_usdc_df = data_aavev3_usdc_df.rename(columns={'dapr':'apy'})
    return data_aavev3_usdc_df[['supply_liquidity','apy']]



def request_samurai_benqi_usdc():
    ####https://yieldsamurai.com/pool/avalanche/0xb715808a78f6041e46d61cb123c9b4a27056ae9c
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    benqi_usdc_payload = {
        "id": "60129542152",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=benqi_usdc_payload)
    data_benqi_usdc_df = pd.DataFrame().from_records(json.loads(x.text))
    data_benqi_usdc_df['date'] = pd.to_datetime(data_benqi_usdc_df['timestamp'], unit='ms')
    data_benqi_usdc_df = data_benqi_usdc_df.set_index('date')
    data_benqi_usdc_df['supply_liquidity'] = data_benqi_usdc_df['tvl']/(1. + data_benqi_usdc_df['utilization'])
    data_benqi_usdc_df = data_benqi_usdc_df.rename(columns={'dapr':'apy'})
    return data_benqi_usdc_df[['supply_liquidity','apy']]




def request_samurai_aavev3_savax():
    #https://yieldsamurai.com/pool/avalanche/0x513c7e3a9c69ca3e22550ef58ac1c0088e918fff
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    aave_savax_payload ={
        "id": "103079215112",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=aave_savax_payload)
    data_aave_savax_df = pd.DataFrame().from_records(json.loads(x.text))
    data_aave_savax_df['date'] = pd.to_datetime(data_aave_savax_df['timestamp'], unit='ms')
    data_aave_savax_df = data_aave_savax_df.set_index('date')
    data_aave_savax_df['supply_liquidity'] = data_aave_savax_df['tvl']/(1. + data_aave_savax_df['utilization'])
    data_aave_savax_df = data_aave_savax_df.rename(columns={'dapr':'apy'})
    return data_aave_savax_df[['supply_liquidity','apy']]

def request_samurai_benqi_savax():
    #https: // yieldsamurai.com / pool / avalanche / 0xf362fea9659cf036792c9cb02f8ff8198e21b4cb
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    benqi_savax_payload ={
            "id": "60129542154",
            "period": 0,
            "range": None,
            "rateKeys": [
                "dapr",
                "bapr",
                "tvl",
                "utilization"
            ]
    }
    x = requests.post(samurai_url, json=benqi_savax_payload)
    data_benqi_savax_df = pd.DataFrame().from_records(json.loads(x.text))
    data_benqi_savax_df['date'] = pd.to_datetime(data_benqi_savax_df['timestamp'], unit='ms')
    data_benqi_savax_df = data_benqi_savax_df.set_index('date')
    data_benqi_savax_df['supply_liquidity'] = data_benqi_savax_df['tvl']/(1. + data_benqi_savax_df['utilization'])
    data_benqi_savax_df = data_benqi_savax_df.rename(columns={'dapr':'apy'})
    return data_benqi_savax_df[['supply_liquidity','apy']]


def request_samurai_benqi_btcb():
    #https://yieldsamurai.com/pool/avalanche/0x89a415b3d20098e6a6c8f7a59001c67bd3129821
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    benqi_btcb_payload ={
        "id": "60129542155",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=benqi_btcb_payload)
    data_benqi_btcb_df = pd.DataFrame().from_records(json.loads(x.text))
    data_benqi_btcb_df['date'] = pd.to_datetime(data_benqi_btcb_df['timestamp'], unit='ms')
    data_benqi_btcb_df = data_benqi_btcb_df.set_index('date')
    data_benqi_btcb_df['supply_liquidity'] = data_benqi_btcb_df['tvl']/(1. + data_benqi_btcb_df['utilization'])
    data_benqi_btcb_df = data_benqi_btcb_df.rename(columns={'dapr':'apy'})
    return data_benqi_btcb_df[['supply_liquidity','apy']]

def request_samurai_aave_v3_btcb():
    # https://yieldsamurai.com/pool/avalanche/0x8ffdf2de812095b1d19cb146e4c004587c0a0692
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    aave_btcb_payload ={
        "id": "103079215115",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=aave_btcb_payload)
    data_aavev3_btcb_df = pd.DataFrame().from_records(json.loads(x.text))
    data_aavev3_btcb_df['date'] = pd.to_datetime(data_aavev3_btcb_df['timestamp'], unit='ms')
    data_aavev3_btcb_df = data_aavev3_btcb_df.set_index('date')
    data_aavev3_btcb_df['supply_liquidity'] = data_aavev3_btcb_df['tvl']/(1. + data_aavev3_btcb_df['utilization'])

    data_aavev3_btcb_df = data_aavev3_btcb_df.rename(columns={'dapr':'apy'})
    return data_aavev3_btcb_df[['supply_liquidity','apy']]


def request_samurai_aave_v3_usdt():
    # https://yieldsamurai.com/pool/avalanche/0x6ab707aca953edaefbc4fd23ba73294241490620
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    aave_usdt_payload ={
        "id": "103079215109",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=aave_usdt_payload)
    data_aavev3_usdt_df = pd.DataFrame().from_records(json.loads(x.text))
    data_aavev3_usdt_df['date'] = pd.to_datetime(data_aavev3_usdt_df['timestamp'], unit='ms')
    data_aavev3_usdt_df = data_aavev3_usdt_df.set_index('date')
    data_aavev3_usdt_df['supply_liquidity'] = data_aavev3_usdt_df['tvl']/(1. + data_aavev3_usdt_df['utilization'])
    data_aavev3_usdt_df = data_aavev3_usdt_df.rename(columns={'dapr':'apy'})
    return data_aavev3_usdt_df[['supply_liquidity','apy']]

def request_samurai_benqi_usdt():
    # https://yieldsamurai.com/pool/avalanche/0xd8fcda6ec4bdc547c0827b8804e89acd817d56ef
    samurai_url = 'https://yieldsamurai.com/api/pool-historical-data'
    benqi_usdt_payload ={
        "id": "60129542153",
        "period": 0,
        "range": None,
        "rateKeys": [
            "dapr",
            "bapr",
            "tvl",
            "utilization"
        ]
    }
    x = requests.post(samurai_url, json=benqi_usdt_payload)
    data_benqi_usdt_df = pd.DataFrame().from_records(json.loads(x.text))
    data_benqi_usdt_df['date'] = pd.to_datetime(data_benqi_usdt_df['timestamp'], unit='ms')
    data_benqi_usdt_df = data_benqi_usdt_df.set_index('date')
    data_benqi_usdt_df['supply_liquidity'] = data_benqi_usdt_df['tvl']/(1. + data_benqi_usdt_df['utilization'])
    data_benqi_usdt_df = data_benqi_usdt_df.rename(columns={'dapr':'apy'})
    return data_benqi_usdt_df[['supply_liquidity','apy']]