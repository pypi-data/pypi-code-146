import pandas as pd


class PySmells:
    def __init__(self, file):
        self.file = file

    def pylint_insigth(self, count_by_type=False):
        ''''''
        error_code = []

        with open(self.file, 'r+') as _:
            arq = _.readlines()

        for i in arq:
            try:
                if count_by_type:
                    x, _ = i.split('::')[0][0], i.split('::')[1]
                else:
                    x, _ = i.split('::')[0], i.split('::')[1]
                    
                error_code.append(x)
            except BaseException:
                continue

        return pd.Series(error_code).value_counts()

    def pylint_score(self):
        with open(self.file, 'r+') as _:
            arq = _.readlines()
            while '\n' in arq:
                arq.remove('\n')

        return arq[-1].split('/')[0].split()[-1]

    def pep8_insigth(self):
        error_codes = []

        with open(self.file, 'r+') as _:
            arq = _.readlines()

        for error in arq:
            count, error_code = error.split()[0], error.split()[1]
            error_codes.append([error_code, count])

        return pd.Series([i[1] for i in error_codes], index=[i[0] for i in error_codes])

    def mypy_insigth(self):
        errors = []

        with open(self.file, 'r+') as _:
            arq = _.readlines()

        for error in arq:
            a = error.split('  ')[-1]
            errors.append(a[:-1])

        errors.pop()
        return pd.Series(errors).value_counts()
