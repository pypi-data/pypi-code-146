import copy
import itertools
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model, tree



class scpQCA:
    def __init__(self,data, decision_name, caseid):
        self.data=data
        self.decision_name=decision_name
        self.caseid=caseid
        self.necessity=dict()
        for value in self.data[self.decision_name].unique():
            self.necessity[value]=None

        
    def direct_calibration(self, feature_list, full_membership, cross_over, full_nonmembership):
        def Ragin_direct(data, full_membership, cross_over, full_nonmembership):
            deviation=[i-cross_over for i in data]
            log_odds=[i*(3/(full_membership-cross_over)) if i>0 else i*(-3/(full_nonmembership-cross_over)) for i in deviation]
            return [round(np.exp(i)/(1+np.exp(i)),3) for i in log_odds]
        if self.caseid !=None and self.caseid in feature_list:
            feature_list.remove(self.caseid)
        for factor in feature_list:
            self.data[factor]=np.array(Ragin_direct(list(self.data[factor]), full_membership, cross_over, full_nonmembership))

    def indirect_calibration(self, feature_list, class_num, full_membership=None, full_nonmembership=None):
        def Ragin_indirect(data, class_num, full_membership, full_nonmembership):
            if full_membership!=None and full_nonmembership!=None:
                a,b=full_membership, full_nonmembership
            else:
                a,b=max(data),min(data)
            ruler=np.linspace(b,a,class_num+1)
            cali=[]
            for i in range(len(data)):
                for j in range(len(ruler)):
                    if data[i]<=ruler[j+1]:
                        cali.append(round(j/(class_num-1),3))
                        break
            return cali
        if self.caseid !=None and self.caseid in feature_list:
            feature_list.remove(self.caseid)
        for factor in feature_list:
            self.data[factor]=np.array(Ragin_indirect(list(self.data[factor]),class_num, full_membership, full_nonmembership))
    
    def raw_truth_table(self, decision_label, feature_list, cutoff=2, consistency_threshold=0.8, sortedby=True):
        if self.caseid !=None and self.caseid in feature_list:
            feature_list.remove(self.caseid)
        if self.decision_name in feature_list:
            feature_list.remove(self.decision_name)
        issues=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        Cartesian=[]
        for i in range(len(feature_list)):
            Cartesian.append(list(self.data[feature_list[i]].unique()))
        values=[d for d in itertools.product(*Cartesian)]
        raw=[]
        for v in range(len(values)):
            Q=''
            for i in range(len(feature_list)):
                Q+=str(feature_list[i])+'=='+str(values[v][i])+' & '
            Q=Q[:-3]
            result=self.data.query(Q)
            if len(result)!=0:
                number=len(result)
                raw_consistency=len(result.loc[(result[self.decision_name]==decision_label)])/len(result) if number>0 else 0
                raw_coverage=len(result.loc[(result[self.decision_name]==decision_label)])/issues if issues>0 else 0
                case_list=list(result[self.caseid]) if self.caseid!=None else []
                if number>=cutoff and raw_consistency>=consistency_threshold:
                    # true table value + number + cases + consistency + coverage
                    raw.append((values[v]+(number,case_list,raw_consistency,raw_coverage,)))
        if sortedby:
            # ordered by number (coverage)
            raw=sorted(raw, key=lambda raw: raw[len(feature_list)+2],reverse=True)
            raw=sorted(raw, key=lambda raw: raw[len(feature_list)+3],reverse=True)
        else:
            # ordered by consistency
            raw=sorted(raw, key=lambda raw: raw[len(feature_list)+3],reverse=True)
            raw=sorted(raw, key=lambda raw: raw[len(feature_list)+2],reverse=True)
        feature_list.append('number')
        feature_list.append('caseid')
        feature_list.append('consistency')
        feature_list.append('coverage')

        truth_table=pd.DataFrame(raw,columns=feature_list)
        print(truth_table)
        return truth_table

    def scp_truth_table(self,rules, feature_list,decision_label):
        if self.caseid !=None and self.caseid in feature_list:
            feature_list.remove(self.caseid)
        if self.decision_name in feature_list:
            feature_list.remove(self.decision_name)

        issues=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        rules=sorted(rules,key=lambda raw:raw[0],reverse=True)
        df=[]
        for i in range(len(rules)):
            row=['-']*(len(feature_list)+3)
            Q=rules[i][0].split(' & ')
            for j in Q:
                equation=j.split('==')
                factor=equation[0]
                value=equation[1]
                row[feature_list.index(factor)]=value
            result=self.data.query(rules[i][0])
            number=len(result)
            raw_consistency=len(result.loc[(result[self.decision_name]==decision_label)])/len(result) if number>0 else 0
            row[-3]=number
            row[-2]=format(raw_consistency, '.4f') 
            row[-1]=format(len(result.loc[(result[self.decision_name]==decision_label)])/issues, '.4f') 
            df.append(row)
        # value + number + consistency + coverage
        df=sorted(df, key=lambda raw: raw[-2],reverse=True)
        df=sorted(df, key=lambda raw: raw[-1],reverse=True)

        feature_list.append('number')
        feature_list.append('consistency')
        feature_list.append('coverage')
        truth_table=pd.DataFrame(df,columns=feature_list)
        with pd.option_context('display.max_rows', None):  
            print(truth_table)
        return truth_table

    def search_necessity(self, decision_label, feature_list,consistency_threshold=0.9):
        self.necessity[decision_label]=[]
        if self.caseid !=None and self.caseid in feature_list:
            feature_list.remove(self.caseid)
        if self.decision_name in feature_list:
            feature_list.remove(self.decision_name)

        issue=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        if issue==0:
            return []
        necessity=dict()
        for character in feature_list:
            for value in self.data[character].unique():
                if len(self.data.loc[(self.data[self.decision_name]==decision_label) & (self.data[character]==float(value))])/issue>=consistency_threshold:
                    print("{}=={} is a necessity condition".format(character,value))
                    necessity[character]=value
                    self.necessity[decision_label].append(str(character)+'=='+str(value))


    def __search_combination(self, items):
        if len(items) == 0:
            return [[]]
        return self.__search_combination(items=items[1:])+[[items[0]] + r for r in self.__search_combination(items=items[1:])]
        # subsets = []
        # first_elt = items[0] 
        # rest_list = items[1:]
        # for partial_sebset in self.__search_combination(rest_list):
        #     subsets.append(partial_sebset)
        #     next_subset = partial_sebset[:] +[first_elt]
        #     subsets.append(next_subset)
        # return subsets

    def candidate_rules(self,decision_label, feature_list,consistency,cutoff,rule_length=5):
        if self.caseid !=None and self.caseid in feature_list:
            feature_list.remove(self.caseid)
        if self.decision_name in feature_list:
            feature_list.remove(self.decision_name)
        
        # issues=len(self.data.loc[(self.data[self.decision_name]==decision_label)])
        candidate=[]
        for i in self.__search_combination(feature_list):
            if len(i)<=rule_length:
                candidate.append(i)  
        print("Running...please wait. There are {} factor combinations.".format(len(candidate)))
        rules=[]
        for i in range(len(candidate)):
            length=len(candidate[i])
            Cartesian=[]                  
            for j in range(length):
                Cartesian.append(list(self.data[candidate[i][j]].unique()))
            values=[d for d in itertools.product(*Cartesian)]   
            for r in range(len(values)):
                Q=''
                for j in range(length):
                    Q+=str(candidate[i][j])+'=='+str(values[r][j])+' & '
                Q=Q[:-3]

                # flag=True if (Q=='' or len(self.data.query(Q))==0) else False
                # for n in self.necessity[decision_label]:
                #     if n in Q:
                #         flag=True
                # if flag:
                #     continue
                if Q=='' or len(self.data.query(Q))==0:
                    continue
                   
                result=self.data.query(Q)
                p=result[self.decision_name].value_counts(normalize = True, dropna = False)
                # if p.idxmax()==decision_label and p[p.idxmax()]>=consistency and p[p.idxmax()]*len(result)>=cutoff: 
                if p.idxmax()==decision_label and p[p.idxmax()]>=consistency and len(result[result[self.decision_name]==decision_label])>=cutoff: 
                    row=[Q,len(result[result[self.decision_name]==decision_label]),p[p.idxmax()]] # cutoff, consistency
                    rules.append(row)
        print("There are {} candidate rules in total.".format(len(rules)))
        return rules

    def __check_subset(self, decision_label, new_rule, rules, unique_cover=2):
        final_rules=copy.deepcopy(rules)
        final_rules.append(new_rule)
        rules=[]
        set_A=set()
        for i in range(len(final_rules)):
            set_B=set()
            for j in range(i+1,len(final_rules)):
                temp=self.data.query(final_rules[j])
                index=set(temp[temp[self.decision_name] == decision_label].index.tolist())
                set_B=set_B.union(index)
                temp[self.decision_name].value_counts(normalize = False, dropna = True)
            temp=self.data.query(final_rules[i])
            index=set(temp[temp[self.decision_name] == decision_label].index.tolist())
            if len(index.difference(set_B.union(set_A)))<unique_cover:
                pass
            else:
                rules.append(final_rules[i])
                set_A=set_A.union(index)      
        return rules, set_A

    def greedy(self,rules,decision_label,unique_cover=2):
        if len(rules)==0:
            print("The candidate rule list is empty.")
            return [],set()

        final_set=set()
        final_rule=[]
        for i in range(len(rules)):
            flag=False
            for n in self.necessity[decision_label]:
                if n in rules[i][0]:
                    flag=True
            if flag:
                continue
            temp_final_rule, temp_set=self.__check_subset(decision_label,rules[i][0], final_rule, unique_cover)
            if len(temp_set)>len(final_set):
                final_rule, final_set=temp_final_rule, temp_set
        if len(final_rule)==0:
            return [],set()
        for i in range(len(final_rule)):
            for j in range(len(self.necessity[decision_label])):
                final_rule[i]=final_rule[i]+' & '+self.necessity[decision_label][j]
        final_set=set()
        for rule in final_rule:
            cases=self.data.query(rule)
            final_set=final_set.union(set(list(cases[cases[self.decision_name] == decision_label].index)))
        return final_rule, final_set

    def cov_n_con(self, decision_label,configuration,issue_sets):
        if issue_sets==set():
            print("consistency = {} and coverage = {}".format(0.0,0.0))
            return 0
        coverage=len(issue_sets)/len(self.data[self.data[self.decision_name] == decision_label]) if len(self.data[self.data[self.decision_name] == decision_label])!=0 else 0
        consistency1=set()
        consistency2=set()
        for rule in configuration:
            temp=self.data.query(rule)
            consistency1=consistency1.union(set(temp[temp[self.decision_name]==decision_label].index.tolist()))
            consistency2=consistency2.union(set(temp[temp[self.decision_name]!=decision_label].index.tolist()))
        consistency=len(consistency1)/(len(consistency1)+len(consistency2))
        print("consistency = {} and coverage = {}".format(consistency,coverage))
        return consistency*coverage

    def runQCA(self, decision_label, feature_list, necessary_consistency:list, sufficiency_consistency:list, cutoff:list, rule_length:int, unique_cover:list):
        self.necessity[decision_label]=[]
        total_rules=self.candidate_rules(decision_label=decision_label, feature_list=feature_list, consistency=min(sufficiency_consistency), cutoff=min(cutoff), rule_length=rule_length)
        pd_rules=pd.DataFrame(total_rules,columns=["candidate_rule","cutoff","consistency"]).sort_values(by=["cutoff","consistency"],ascending=False)
        Cartesian=[necessary_consistency,sufficiency_consistency,cutoff,unique_cover]
        values=[d for d in itertools.product(*Cartesian)]
        final_config, final_set, config_value=[],set(),0
        v,l=[],sys.maxsize
        for i in range(len(values)):
            self.search_necessity(decision_label=decision_label,feature_list=feature_list,consistency_threshold=values[i][0])
            rules=pd_rules[(pd_rules['consistency']>=values[i][1]) & (pd_rules['cutoff']>=values[i][2])]
            print("processing the simplification with para: necessary consistency={}, sufficiency consistency={}, cutoff={}, unique cover={}".format(values[i][0],values[i][1], values[i][2], values[i][3]))
            config, sets=self.greedy(rules.values.tolist(), decision_label=decision_label, unique_cover=values[i][3])
            con_cov=self.cov_n_con(decision_label=decision_label, configuration=config, issue_sets=sets)
            if con_cov>config_value or (con_cov==config_value and len(config)<l):
                print("changed")
                final_config,final_set=config, sets
                config_value=con_cov
                v=values[i]
                l=len(config)
            self.necessity[decision_label]=[]          
        print("The best opt parameter of scpQCA is: necessary consistency={}, sufficiency consistency={}, cutoff={}, unique cover={}".format(v[0],v[1], v[2], v[3]))
        return final_config, final_set

    # def comparison(self, data, feature_list, round, random_num, optimization, caseid, decision_name, rule_length, consistency=0.8,cutoff=2,unique_cover=2, index_list=[]):
    #     code1,code2,code3,code4=0,0,0,0
    #     dtr_score=[]
    #     lr_score=[]
    #     samply_index=[]
    #     code_result=[]
    #     for i in range(round):
    #         random_index=set()
    #         if index_list!=[]:
    #             random_index=set(index_list[i])
    #         else:
    #             for _ in range(int(random_num)):
    #                 random_index.add(random.randint(0,len(data)-1))
    #         print("The sample cases are:", random_index)
    #         samply_index.append(len(random_index))
    #         data_test=data.drop(list(random_index))
    #         if self.caseid !=None and self.caseid in feature_list:
    #             feature_list.remove(self.caseid)
    #         if self.decision_name in feature_list:
    #             feature_list.remove(self.decision_name)
    #         model = tree.DecisionTreeClassifier(max_depth=rule_length, min_samples_split=int(1/(1-consistency)), min_samples_leaf=cutoff)#Decision Tree Regression
    #         model.fit(data_test[feature_list],data_test[decision_name])
    #         score=model.score(data.loc[random_index,feature_list],data.loc[random_index,decision_name])
    #         dtr_score.append(score)
    #         print(model.predict(data.loc[random_index,feature_list]))
    #         print("Decision Tree's prediction precision is:",score)
    #         model = linear_model.LogisticRegression()# Linear Regression
    #         model.fit(data_test[feature_list],data_test[decision_name])
    #         score=model.score(data.loc[random_index,feature_list],data.loc[random_index,decision_name])
    #         lr_score.append(score)
    #         print(model.predict(data.loc[random_index,feature_list]))
    #         print("Linear Regression's prediction precision is:",score)
    #         result=list(data[decision_name].unique())
    #         rules,sets=[],[]
    #         for i in range(len(result)):
    #             obj=scpQCA(data_test,feature_list,decision_name,caseid)
    #             # obj.search_necessity(result[i])
    #             temp_rules,_=obj.runQCA(optimization,result[i], rule_length, consistency, cutoff, unique_cover)
    #             rules.append(temp_rules)
    #             sets.append(set())
    #             for rule in temp_rules:
    #                 sets[i]=sets[i].union(set(list(data.query(rule).index)))
    #         print(rules,sets)
    #         print("scpQCA's prediction solutions are:")
    #         for random_i in random_index:
    #             i=result.index(data.iloc[random_i][decision_name])
    #             right_set=sets[i]
    #             wrong_set=set()
    #             for j in range(len(result)):
    #                 if j!=i:
    #                     wrong_set=wrong_set.union(sets[j])
    #             if random_i in right_set and random_i not in wrong_set:
    #                 print("perfectly correct!")
    #                 code1+=1
    #             elif random_i in right_set and random_i in wrong_set:
    #                 print("confusion mistake!")
    #                 code2+=1
    #             elif random_i not in right_set and random_i in wrong_set:
    #                 print("totally mistake!")
    #                 code3+=1
    #             else:
    #                 print("not found")
    #                 code4+=1
    #         code_result.append([code1,code2,code3,code4])
    #         print()
    #     print("Decision Tree's results are:","model score=",dtr_score)
    #     print("Linear Regression's results are:","model score=",lr_score)
    #     print("The 4 solution codes are: perfectly correct!, confusion mistake!, totally mistake!, not found")
    #     print("scpQCA's solution codes are:",code_result)
    #     return samply_index,dtr_score,lr_score,code_result

    # def draw_plt(self, dtr_score, lr_score, code_result, round):
    #     dtr=dtr_score
    #     lr=lr_score
    #     code=code_result
    #     code1,code2,code3,code4=[code[0][0],],[code[0][1],],[code[0][2],],[code[0][3],]
    #     for i in range(1,len(code)):
    #         code1.append(code[i][0]-code[i-1][0])
    #         code2.append(code[i][1]-code[i-1][1])
    #         code3.append(code[i][2]-code[i-1][2])
    #         code4.append(code[i][3]-code[i-1][3])
    #     print(code1,code2,code3,code4)
    #     ratio1,ratio2,ratio3,ratio4,ratio5=[],[],[],[],[]
    #     for i in range(round):
    #         ratio1.append(code1[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
    #         ratio2.append(code2[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
    #         ratio3.append(code3[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
    #         ratio4.append(code4[i]/(code1[i]+code2[i]+code3[i]+code4[i]))
    #         ratio5.append(code1[i]/(code1[i]+code2[i]+code3[i]))
    #     x=range(len(lr))
    #     plt.figure(figsize=(12,8))
    #     plt.gcf().set_facecolor(np.ones(3)* 240 / 255)
    #     plt.grid()
    #     plt.plot(x, dtr, marker='.', ms=10, label="decision tree regression")
    #     plt.plot(x, lr, marker='.', ms=10, label="linear regression")
    #     plt.plot(x, ratio1, marker='.', ms=10, label="perfectly correct")
    #     plt.plot(x, ratio5, marker='.', ms=10, label="perfectly correct(except not found)")
    #     plt.xticks(rotation=45)
    #     plt.ylim(0,1)
    #     plt.xlabel("case number")
    #     plt.ylabel("ratio")
    #     plt.legend(loc="upper left")
    #     plt.show()
    #     print("The mean of Linear Regression, Decision Tree, perfect correct and perfectly correct(except not found) are:")
    #     print(np.mean(lr),np.mean(dtr),np.mean(ratio1),np.mean(ratio5))
    #     print("The variance of Linear Regression, Decision Tree, perfect correct and perfectly correct(except not found) are:")
    #     print(np.var(lr),np.var(dtr),np.var(ratio1),np.var(ratio5))
    #     return

# if __name__=="__main__":
#     data=pd.read_csv(r'E:\CCDA-PC\my paper\scpQCA\SMR一拒\Bara2014set.csv', encoding='ISO-8859-1')
#     feature_list=['groupid','onset', 'polx', 'oust', 'ruler', 'tiny', 'precon', 'petrol', 'instab']1
#     #    'tekcon', 'conc', 'xpoor', 'havtek', 'polx2', 'xrich70', 'xrich80',
#     #    'polx_precon', 'oust_instab', 'tekcon_instab', 'petrol_polx_instab',
#     #    'petrol_polx', 'petrol_instab', 'polx_instab', 'nottiny', 'notruler',
#     #    'nottinynotruler', 'ntnr_polx_precon', 'ntnr_oust_instab',
#     #    'ntnr_tekcon_instab', 'ntnr_polx', 'ntnr_precon', 'ntnr_oust',
#     #    'ntnr_instab', 'ntnr_tekcon']
#     data=data[feature_list]
#     test=scpQCA(data,decision_name='onset',caseid='groupid')
#     test.search_necessity(1,feature_list=feature_list,consistency_threshold=0.9)
#     rules=test.candidate_rules(decision_label=1,feature_list=feature_list,consistency=0.8,cutoff=20,rule_length=4)
#     configuration,issue_set=test.greedy(rules=rules,decision_label=1,unique_cover=1)
#     # configuration,issue_set=test.runQCA(decision_label=1,feature_list=list(data.columns),necessary_consistency=[0.8,0.9,1],sufficiency_consistency=[0.75,0.8,1],cutoff=[1,2],rule_length=5,unique_cover=[2])
#     print(configuration,issue_set)
    # data=[[random.randint(0,100) for _ in range(7)] for _ in range(60)]
    # data=pd.DataFrame(data)
    # data.columns=['A','B','C','D','E','F','cases']
    # obj=scpQCA(data,decision_name='F',caseid='cases')
    # feature_list=['A','B','C','D','E','F','cases']

    # obj.indirect_calibration(feature_list,2,100,0)

    # configuration,issue_set=obj.runQCA(decision_label=1, feature_list=feature_list, necessary_consistency=[0.8,0.9],sufficiency_consistency=[0.75,0.8],cutoff=[1,2],rule_length=5,unique_cover=[1])
    # print(configuration, issue_set)

    # obj.search_necessity(decision_label=1, feature_list=feature_list,consistency_threshold=0.6)

    # rules=obj.candidate_rules(decision_label=1, feature_list=feature_list, consistency=0.6,cutoff=1)

    # obj.raw_truth_table(decision_label=1, feature_list=feature_list, cutoff=1,consistency_threshold=0.6,sortedby=False)
    # obj.scp_truth_table(rules, feature_list=feature_list,decision_label=1)

    # configuration,issue_set=obj.greedy(rules=rules,decision_label=1,unique_cover=2)
    # print(configuration)
    # print(issue_set)

    # obj.cov_n_con(decision_label=1, configuration=configuration,issue_sets=issue_set)