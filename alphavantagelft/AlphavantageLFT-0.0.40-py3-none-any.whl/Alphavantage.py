import requests

class Alphavantage:

    def __init__(self,key="", keys=[]): 
        self.key = key
        self.keys = {key: 0 for key in keys}        
        
        # TODO: Have a core query URL and then the dictionary for urls will contian the function name and the main argument alone
        self.urls = {
            'SymbolLookup': "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}",
            'CompanyOverview': "https://www.alphavantage.co/query?function=OVERVIEW&symbol={}",
            'NewsSentiment': "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={}",
            'QuoteEndpoint': "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}",
            'TimeSeriesDailyAdjusted': "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}",
            'IncomeStatement': "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={}",
            'BalanceSheet': "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={}",
            'CashFlow': "https://www.alphavantage.co/query?function=CASH_FLOW&symbol={}",
            'Earnings': "https://www.alphavantage.co/query?function=EARNINGS&symbol={}",
            'News': "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={}",
        }
        
        # Initialize variables for tracking the status of the current instance
        self.calls = self.request_failure = self.valid_response = self.conversion_failure = self.timeouts = 0
        return
    
    def _request(self,url): # Internal request method used for handling errors and using multiple keys based on their times used
        
        # Select the key for the request (could be single, or from dictionary based on lowest number of uses)
        if len(self.keys)!=0: # For using a dictionary of keys
            key = min(self.keys, key=self.keys.get)
            self.keys[key]+=1 # Increase count to keep using the key with the lowest usage
        else: key = self.key 
        
        # Send a get request using the given URL and the selected key
        response = requests.get(f'{url}&apikey={key}')
        self.calls+=1

        # Check if the request's response is valid/if it failed
        if response.status_code==200: # Check if the request worked 
            try: response = response.json()
            except: 
                self.conversion_failure+=1
                return {'Error': "Failed to convert response to JSON."}
            else:
                if "Note" not in response.keys(): 
                    self.valid_response+=1
                    return response
                else: 
                    self.timeouts+=1
                    return {'Error': f'Exceeded request limit for {key}'} # (Picks the smallest key, so if you ever encounter this error, just call again)
        else: 
            self.request_failure += 1
            return {'Error': f'Request Failed {response.status_code}'}

    def SymbolLookUp(self,symbol, internal=False): # Used internally as well (depending on optional variable related to output format)
        response = self._request(self.urls['SymbolLookup'].format(symbol))
        if internal: # Returns if the given symbol is in the symbol look up (verifying validity of symbols for other API calls)
            if 'Error' not in response.keys(): 
                if symbol in [ticker['1. symbol'] for ticker in response['bestMatches']]: return True
                else: return {'Error': 'Invalid Symbol'}
            else: return response
        return response
        
    def CompanyOverview(self,symbol):
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['CompanyOverview'].format(symbol))
        else: return lookup

    def NewsSentiment(self,symbol):
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['NewsSentiment'].format(symbol))
        else: return lookup
        
    def QuoteEndpoint(self,symbol):
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['QuoteEndpoint'].format(symbol))
        else: return lookup
        
    def TimeSeriesDailyAdjusted(self,symbol): #TODO: Have the option to return the data as a pandas dataframe or a SQLite3 command/string command to a cusor
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['TimeSeriesDailyAdjusted'].format(symbol))
        else: return lookup

    def IncomeStatement(self,symbol): #TODO: Have the option to return the data as a pandas dataframe or a SQLite3 command/string command to a cusor
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['IncomeStatement'].format(symbol))
        else: return lookup

    def BalanceSheet(self,symbol): #TODO: Have the option to return the data as a pandas dataframe or a SQLite3 command/string command to a cusor
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['BalanceSheet'].format(symbol))
        else: return lookup

    def CashFlow(self,symbol): #TODO: Have the option to return the data as a pandas dataframe or a SQLite3 command/string command to a cusor
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['CashFlow'].format(symbol))
        else: return lookup

    def Earnings(self,symbol): #TODO: Have the option to return the data as a pandas dataframe or a SQLite3 command/string command to a cusor
        lookup = self.SymbolLookUp(symbol,internal=True)
        if lookup==True: return self._request(self.urls['Earnings'].format(symbol))
        else: return lookup

    def News(self,topics):
        # User can pass either one topic or a list of topics
        response = self._request(self.urls['News'].format((', '.join(topics)) if len(topics)>1 else topics[0]))
        return response

    def __str__(self):
        status = """
            Key(s): {}
            Number of Calls: {}
            Number of Request Failures: {}
            Number of Conversion Failures: {}
            Number of Timeouts/Limit Exceeded: {}
            Number of Valid Responses: {}
        """.format(self.keys if len(self.keys)>=1 else self.key, self.calls, self.request_failure, self.conversion_failure, self.timeouts, self.valid_response)
        return status