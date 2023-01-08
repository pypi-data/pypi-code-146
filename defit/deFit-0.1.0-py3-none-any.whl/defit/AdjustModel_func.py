import pandas as pd
import warnings
def AdjustModel_func(model):
    if model is None:
        print('Model is not defined.Program just fit Binary first order differential equational .And the field of data must contain "seq","time","x","y" .You can see here')
        model = '''
                    x =~ x
                    y =~ y
                    time =~ time
                    x(1) ~ x + y
                    y(1) ~ y + x
                '''
    model = model.strip()
    model = model.split('\n')
    modelDF = pd.DataFrame()
    for i in range(len(model)):
        if '=~' in model[i]:
            modelDF.loc[i, 'field'] = model[i].split('=~')[0].strip()
            modelDF.loc[i, 'operator'] = '=~'
            modelDF.loc[i, 'variable'] = model[i].split('=~')[1].strip()
        elif '~' in model[i]:
            modelDF.loc[i, 'field'] = model[i].split('~')[0].strip()
            modelDF.loc[i, 'operator'] = '~'
            modelDF.loc[i, 'variable'] = model[i].split('~')[1].strip()
        else:
            warnings.warn('Your model has some problems you can see https://github.com/yueqinhu/defit', category=None, stacklevel=1, source=None)
    return modelDF