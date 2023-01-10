from typing import Union
from pandas import DataFrame, concat, melt
from tim.core.types import (
    UploadDatasetConfiguration,
    UpdateDatasetConfiguration
)

def find_feature(sub_parts):
    dow_list = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']
    features_list = []
    for c,s in enumerate(sub_parts):
        if   s['type']=='β':                        sub_feature = ''
        elif s['type']=='TimeOffsets':              sub_feature = s['predictor']+'(t'+str(s['offset'])+')'
        elif s['type']=='RestOfWeek':               sub_feature = 'DoW(t'+str(s['offset'])+') <= '+dow_list[s['day']-1]
        elif s['type']=='Intercept':                sub_feature = 'Intercept('+str(int(s['value']))+')'
        elif s['type']=='Cos':                      sub_feature = 'Cos('+str(int(s['period']))+';'+s['unit']+')'
        elif s['type']=='Sin':                      sub_feature = 'Sin('+str(int(s['period']))+';'+s['unit']+')'
        elif s['type']=='ExponentialMovingAverage': sub_feature = 'EMA_'+s['predictor']+'(t'+str(int(s['offset']))+'; w='+str(int(s['window']))+')'
        elif s['type']=='Identity':                 sub_feature = s['predictor']
        elif s['type']=='PiecewiseLinear':          sub_feature = 'max(0;'+str(s['subtype'])+'*('+str(round(s['knot'],6))+'-'+s['predictor']+'(t'+str(s['offset'])+')))'
        elif s['type']=='SimpleMovingAverage':      sub_feature = 'SMA_'+s['predictor']+'(t'+str(int(s['offset']))+'; w='+str(int(s['window']))+')'
        elif s['type']=='Fourier':                  sub_feature = 'Fourier('+str(s['period'])+')'
        elif s['type']=='Weekday':                  sub_feature = 'DoW(t'+str(s['offset'])+') = '+dow_list[s['day']-1]
        elif s['type']=='Month':                    sub_feature = 'Month<='+month_list[s['month']]
        elif s['type']=='PublicHolidays':           sub_feature = s['predictor']
        elif s['type']=='Trend':                    sub_feature = 'Trend'
        else:                                       sub_feature = '_test_'
        if s['type']=='β':
            features_list.append(sub_feature)
            beta = s['value']
        else:
            features_list.append(' & '+sub_feature) if c>0 else features_list.append(sub_feature)
    feature_output = ''.join(str(e) for e in features_list)
    return feature_output,beta

def is_valid_csv_configuration(
    configuration: Union[UploadDatasetConfiguration, UpdateDatasetConfiguration]
    ) -> bool:
    if configuration is None:
        return True
    if "csvSeparator" in configuration:
        return False
    return True

class postProcess:

    def properties(response):
        try:
            properties = response['model']['modelZoo']['variableProperties']
        except:
            properties = response['model']['normalBehaviorModel']['variableProperties']
        df = DataFrame(properties).sort_values(by='importance',ascending=False)
        df['rel_importance'] = df['importance']/df.sum()['importance']
        return df
    
    def features(response):
        try:
            models = response['model']['modelZoo']['models']
        except:
            models = response['model']['normalBehaviorModel']['models']
        features = []
        for model in models:
            terms = model['terms']
            for count,term in enumerate(terms):
                feature,beta = find_feature(term['parts'])
                features.append([model['index'],count,feature,term['importance'],beta])
        return DataFrame(features,columns=['Model','Term','Feature','importance','beta'])

    def forecast_accuracy_table(response):
        bin_json = response['bin']
        bin_accuracy_df = DataFrame()
        for n in bin_json: bin_accuracy_df = concat([bin_accuracy_df,DataFrame(n).reset_index().rename(columns={'index':'KPI'})])
        bin_accuracy_df['accuracy_type'] = 'bin'

        samplesAhead_json = response['samplesAhead']
        samplesAhead_accuracy_df = DataFrame()
        for n in samplesAhead_json: samplesAhead_accuracy_df = concat([samplesAhead_accuracy_df,DataFrame(n).reset_index().rename(columns={'index':'KPI'})])
        samplesAhead_accuracy_df['accuracy_type'] = 'samplesAhead'

        all_accuracy_df = DataFrame(response['all']).reset_index().rename(columns={'index':'KPI'})
        all_accuracy_df['accuracy_type'] = 'all'
        id_columns = ['KPI','name','accuracy_type']
        acc_df = concat([all_accuracy_df,samplesAhead_accuracy_df,bin_accuracy_df])
        return melt(acc_df, id_vars=id_columns, value_vars=list(set(acc_df.columns)-set(id_columns)))