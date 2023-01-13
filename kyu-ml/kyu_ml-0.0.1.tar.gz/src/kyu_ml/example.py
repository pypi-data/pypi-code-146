"""판다스 칼럼 조회하기"""
import pandas as pd 

def getColumn(df, columnName):
  return df.loc[:,[columnName]]