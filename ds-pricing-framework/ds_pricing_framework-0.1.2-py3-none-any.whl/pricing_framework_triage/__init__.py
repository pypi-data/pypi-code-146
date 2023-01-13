"""
pricing_framework_modules.py - a set of functions for creating looks to analyze pricing variables

author: Kelsey Messonnier
email:  kelsey@just.insure
date:   12 January 2023
"""


from tabulate import tabulate
import statsmodels.formula.api as smf


# REQUIRED_COLUMNS = ['claim_indicator','il','ep','policy_number']

class TriageVariable(object):
    """ Class for Triage Functions """

    
    def __init__(self,
                 df: "pd.DataFrame",
                 target_variable: str,
                 proposed_variable: str,
                 control_variable_list: list 
                ):
        
        """
        :param df: dataframe must contain target_variable, proposed_variable, control variables, ep, and il (see additional API Documentation)
        :param target_variable: should be claim frequency
        :param proposed_variable:  should be new variable
        :param control_variables: list of control variables already used in model
        """
        
        # if REQUIRED_COLUMNS not in df.columns:
            # raise ValueError(f"DataFrame must contain {REQUIRED_COLUMNS}")
            
        self.df = df
        self.target = target_variable
        self.proposed = proposed_variable
        self.control_variables = control_variable_list

        
    def get_loss_table(self):
        
        df = self.df
        proposed_variable = self.proposed
        
        variable = df[proposed_variable].unique()
        variable = variable.tolist()
        
        count = df.groupby([proposed_variable])["policy_number"].count()
        claim = df.groupby([proposed_variable])["claim_indicator"].sum()
        # claim_liab = df.groupby([proposed_variable])["claim_indicator_liab"].sum()
        
        freq = claim/count
        # freq_liab = claim_liab/count

        il = df.groupby([proposed_variable])["il"].sum()
        # il_liab = df.groupby([proposed_variable])["il_liab"].sum()
        ep = df.groupby([proposed_variable])["ep"].sum()
        total_ep = df["ep"].sum()
        
        lr = il/ep
        # lr_liab = il_liab/ep
        ep_pct = (ep/total_ep)*100

        titles = [proposed_variable, 'Policy Count', '% of Premium', '# of Claims', 'Freq.', 'LR']
        rows = list(zip(variable, count, ep_pct, claim, freq, lr))

        return tabulate(rows, headers=titles, floatfmt=".4f")
        
        
    def get_balance_table(self):  
        df = self.df
        proposed_variable = self.proposed
        return df[["policy_gen", "age", "price_per_mile", proposed_variable]].groupby([proposed_variable]).describe() 
    
    
    def get_ols_model(self):
        df = self.df
        proposed_variable = self.proposed
        target_variable = self.target
        control_variable_list = self.control_variables
        
        equation = f"{target_variable} ~ {proposed_variable} + {' + '.join(control_variable_list)}"
    
        model = smf.ols(equation, data = self.df).fit()

        return model.summary()

    def get_logit_model(self):
        df = self.df
        proposed_variable = self.proposed
        target_variable = self.target
        control_variable_list = self.control_variables
        
        equation = f"{target_variable} ~ {proposed_variable} + {' + '.join(control_variable_list)}"
    
        model = smf.logit(equation, data = self.df).fit()

        return model.summary()
    
    def run_triage(self):
        display(self.get_balance_table())
        print(self.get_loss_table())
        print(self.get_logit_model())

    
    def __str__(self):
        return f'{self.name}={self.value}'