# Variable input class
# Retirement package version 0.1.3

class retirement():
     
    @staticmethod #This is added so that the interpreter does not add the variable "self" when this method is called in this class
    def intro(): 
        import time
        from time import sleep
        import sys

        lines = ['This is a game to see if you can help Fictitious Steve or Fictitious Stephanie make his or her retirement savings last', 
                 'through retirement.',
                 ' ',
                 'This is just a fictitious game, no retirement or investment or any other decision(s) should ever be made based on the',
                 'information in or from this game',
                 ' ',
                 'Have fun and see how you do!']

        for line in lines:          # for each line of text (or each message)
            for c in line:          # for each character in each line
                print(c, end='')    # print a single character, and keep the cursor there.
                sys.stdout.flush()  # flush the buffer
                sleep(0.02)         # wait a little to make the effect look good.
            print('')               # line break (optional, could also be part of the message)
     
    @staticmethod
    def var_input():
        import pandas as pd
        import numpy as np
        import time
        from time import sleep
        
        variables = []
        variable_names = []
        
        #starting age
        age = int(input('\nWhat is the age of either Fictitious Steve or Stephanie? '))
    
        #time to retirement
        years_to_retire = int(input('Fictitious Steve or Stephanie is planning to retire in how many years? '))
    
        #amount needed at retirement
        month_how_much_needed_at_retirement = float(input('How much per month does Fictitious Steve or Stephanie need at retirement? [In thousands of $; After taxes.] '))
        how_much_needed_at_retirement = 12 * month_how_much_needed_at_retirement
        
        #current retirement savings
        starting_principle = float(input('How much did Fictitious Steve or Stephanie have saved for retirement right now? [In thousands of $] '))
        
        #income after retirment
        month_how_much_ss_at_retirement = float(input('How much Social Security benefits per month will Fictitious Steve or Stephanie receive at retirement? [In thousands/month] '))
        how_much_ss_at_retirement = 12 * month_how_much_ss_at_retirement
        
        month_how_much_other_passive_income = float(input('How much will Fictitious Steve or Stephanie have in other income per month in retirement? [e.g. Pension, Rental Income, etc; In thousands of $] '))
        how_much_other_passive_income = 12 * month_how_much_other_passive_income / 1000
    
        #return on retirement savings
        rate_of_return = float(input('What is the annualized percent return (rate of return) on the retirement saving before retiring? '))

        #life expectance after retirement
        yrs_to_death = input('How long does Fictitious Steve or Stephanie need retirement income? [press enter if you want 20 yrs.] ')
        if yrs_to_death:
            yrs_to_death = float(yrs_to_death) + float(years_to_retire)
        else:
            yrs_to_death = float(20) + float(years_to_retire)
            print('The time Fictitious Steve or Stephanie needs retirement income is for ', yrs_to_death - float(years_to_retire), 'years. ')
    
        #contribution to retirement savings before retiring    
        month_additional_principle = float(input("How much in $'s will Fictitious Steve or Stephanie be adding to the retirement savings per month before retiring? "))
        additional_principle = 12 * month_additional_principle / 1000

        #inflation rate
        inflation = input('What is the inflation rate per year? [press enter if you want 3%.] ')
        if inflation:
            inflation = float(inflation)
        else:
            inflation = float(3)
            print('Based on your input the inflation rate is', inflation, '%.')

        #tax rate
        tax_rate = input('Based on what Fictitious Steve or Stephanie needs, what will be the tax rate? [press enter if you want to assume 25% for both state and federal taxes.] ')
        if tax_rate:
            tax_rate = float(tax_rate)
        else:
            tax_rate = float(25)
            print('Based on your input the overall income tax rate is', tax_rate, '%.')
            
        final_principle = float(0)
    
        variables = [years_to_retire, how_much_needed_at_retirement, starting_principle,
                 how_much_ss_at_retirement, how_much_other_passive_income, rate_of_return,
                 yrs_to_death, additional_principle, inflation, tax_rate, final_principle, age]
    
        variable_names = ['years_to_retire', 'how_much_needed_at_retirement', 'starting_principle',
                 'how_much_ss_at_retirement', 'how_much_other_passive_income', 'rate_of_return',
                 'yrs_to_death', 'additional_principle', 'inflation', 'tax_rate', 
                 'final_principle', 'age']
        ''' 
        legend 
        variables[0] = years_to_retire 
        variables[1] = how_much_needed_at_retirement
        variables[2] = starting_principle
        variables[3] = how_much_ss_at_retirement
        variables[4] = how_much_other_passive_income
        variables[5] = rate_of_return 
        variables[6] = yrs_to_death
        variables[7] = additional_principle
        variables[8] = inflation
        variables[9] = tax_rate
        variables[10] = final_principle
        variables[11] = age
        '''
        df = pd.DataFrame(columns= ['years_to_retire', 'how_much_needed_at_retirement', 'starting_principle',
                 'how_much_ss_at_retirement', 'how_much_other_passive_income', 'rate_of_return',
                 'yrs_to_death', 'additional_principle', 'inflation', 'tax_rate', 
                 'final_principle']) #creates the df using variable_names list
    
        return variables, variable_names, df

    #determines the amount of gain over entirement retirement period (retirement to death)
    @staticmethod
    def impact_years_compounding(variables, df):
        import pandas as pd
        yr = 1
        starting_principle = variables[2]
        while yr <= variables[6]: #calculates compounding across multiple years
            if yr > variables[0] :#ends additional contribution to retirement at the start of retirement    
                additional_principle = 0
            else:
                additional_principle = variables[7]
          
            if yr < variables[0]: #years_to_retire: starts retirement debit at the start of retirement
                #variables[0] = when retirement starts
                debit = 0
                taxes = 0
                inflat = 0
            else:
                debit = (1 + (variables[9]/100) + (variables[8]/100)*((yr + 1) - variables[0])) * (-variables[1]) 
                #how_much_needed_at_retirement
                # variables[9] are taxes; variables[1] is amount needed at retirement; variables[8] is inflation
                taxes = variables[9]
                inflat = variables[8]
            
            years_to_retire = variables[0] - yr
            if years_to_retire < 0:
                years_to_retire = 'Retired'
        
            years_left = variables[6] - yr
        
            #defines gain through monthly compounding while taking into account additional principle
                
            if yr > variables[0]:
                soc_security = variables[3]
                passive_retirement_income = variables[4]
            else: 
                soc_security = 0
                passive_retirement_income = 0
            mpr = variables[5]/1200 # APR divided by 12 to get monthly interest rate
            #print('mpr = ', mpr)
            month = 1    
            new_principle = starting_principle
            #print('new_principle = ', new_principle, '\n')
            while month < 13:
                gain_from_interest_on_principle = new_principle * mpr
                #print('gain_from_interest_on_principle =', gain_from_interest_on_principle)
                new_principle = new_principle + gain_from_interest_on_principle + additional_principle/12 + debit/12 + soc_security/12 + passive_retirement_income/12
                month += 1
                new_principle = float(new_principle)
            
            final_principle = new_principle 
            apr = variables[5]
                     
            df1 = pd.DataFrame({'years_to_retire': years_to_retire, 
                        'how_much_needed_at_retirement' : debit, 
                        'starting_principle': variables[2],
                        'how_much_ss_at_retirement': soc_security, #variables[3] 
                        'how_much_other_passive_income': passive_retirement_income, #variables[4], 
                        'investment_apr': variables[5],
                        'yrs_to_death': years_left, 
                        'additional_principle': additional_principle, 
                        'inflation': inflat, 
                        'tax_rate': taxes, 
                        'final_principle': final_principle}, index = {1})
            
            df = pd.concat([df, df1]) 
        
            starting_principle = final_principle
        
            yr += 1
        
        return df
    
    
    # summarizes the data
    @staticmethod
    def summary(df):
        
        import sys
        import time
        from time import sleep
    
        #prints out a typewriter effect
        #https://stackoverflow.com/questions/19911346/create-a-typewriter-effect-animation-for-strings-in-python
        print()
        lines = ['The Big question ... Will the retirement savings last long enough in this game?????']

        for line in lines:          # for each line of text (or each message)
            for c in line:          # for each character in each line
                print(c, end='')    # print a single character, and keep the cursor there.
                sys.stdout.flush()  # flush the buffer
                sleep(0.0)          # wait a little to make the effect look good.
            print('')               # line break (optional, could also be part of the message)
    
        #time.sleep(2)
    
        i = 0
        while i < len(df):
            print('year', i+1 , 'Retirement Savings: $', int(df.iloc[i,10] * 1000)) #prints out the year ending
        
            #time.sleep(0.5)
        
            if i == df.iloc[0,0] - 1: #defines the point when retirment starts
                #print(i, df.iloc[0,0])
                print('Congratulations, retirement has started! Fictitious Steve or Stephanie will start drawing from his or her retirement savings!!!')
            
            if df.iloc[i,10] < 0: #defines the point when the retirement savings crosses into the negative
                under_water = i - df.iloc[0,0] 
                print("\nOhhhhh Noooooo .... Fictitious Steve's or Stephanie's retirement savings ran out at between the", under_water , 'th and', under_water + 1 , 'th year of retirement!')
                #time.sleep(.5)
                print('\nBUMMERS ... BUT ... since Fictitous Steve or Stephanie is an easy going person and ... this is only a game, go back and change some of the conditions to see if you can make his retirement savings make it a bit farther!')
                print('\nTo play again just refresh this page! ')
               
                break    
            #else:
                #i = len(df) - 1
                #print('Looking Good!')
                #print('In the end your retirement accound will be worth', df.iloc[i,10])
            
            i += 1
    
        if i == len(df):
            print('\nYOU WON!!!! Fictitious Steve or Stephanie thanks you! The retirement savings lasted his or her entire retirement!!!!')
            print('\nTo play again just refresh this page! ')
