from defit import defit
import pandas as pd
# import os
def test_defit():
    # data_path = os.path.join(os.path.dirname(__file__), 'data', 'example1.csv')
    # df = pd.read_csv(data_path)
    df = pd.read_csv('defit/data/example1.csv')
    model = '''
                x =~ myX
                time =~ myTime
                x(2) ~ x + x(1)
            '''
    result = defit(data=df,model=model,plot=False)
    assert result['convergence'] in ["convergence: False (tol=1e-08, See Tolerance Details)","convergence: True (tol=1e-08, See Tolerance Details)"]
    # assert 0

def test_defit2():
    df= pd.read_csv('defit/data/example2.csv')
    model = '''
        x =~ myX
        y =~ myY
        time =~ myTime
        x(1) ~ x + y
        y(1) ~ x + y
    '''
    result = defit(data=df,model = model,plot=False)
    assert result['convergence'] in ["convergence: False (tol=1e-08, See Tolerance Details)","convergence: True (tol=1e-08, See Tolerance Details)"]
    # assert 0