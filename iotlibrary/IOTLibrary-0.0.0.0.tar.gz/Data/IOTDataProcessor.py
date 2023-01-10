import Data.IOTDataStructure as dt
import matplotlib.pyplot as plt
import seaborn as seaborn_plotter
import pandas as pd
import numpy as np
import random as rdn
import os as _os


class IOTDataProcessor(object):
    """description of class"""

    def __init__(self):
        print("Initial Data Processor")
        self._plot_size = (8, 8)

    #Public
    def loadData(self, csv_file):
        print('Load ' + csv_file + "...")

        if not _os.path.exists(csv_file):
            print('Can not find => ' + csv_file )
            return 

        try:
            fp = open(csv_file, 'r', encoding="utf-8")

            all_lines = fp.readlines()
            all_labels = []
            all_rawdatas = []
            all_classes = []
            output_name = ""

            split_title = all_lines[0].replace('\n','').split(',')
            #Setup Title Data
            for title_index in range(0,len(split_title),1):
                if title_index == 0:
                    output_name = split_title[title_index]
                else:
                    all_labels.append((split_title[title_index]))

            #Setup Value Data
            for each_row_index in range(1,len(all_lines),1):
                split_strings = all_lines[each_row_index].replace('\n','').split(',')

                new_data = dt.IOTDataStructure()
                for each_col_index in range(0,len(split_strings),1):
                    current_col_data = (int)(split_strings[each_col_index])
                    if each_col_index == 0:
                        if not (current_col_data in all_classes):
                            all_classes.append(current_col_data)

                        new_data.set_true_label(current_col_data)
                    else:
                        new_data.add_variable(current_col_data)

                new_data.set_variable_list(all_labels)
                new_data.set_output_name(output_name)
                new_data.set_class_name_list(all_classes)
                all_rawdatas.append(new_data)
            
            print('Load File Finished')
            return all_rawdatas

        except:
            print('Load File Error')

    def showData(self, data_list):
        try:
            data_array = []
            column_names = []

            get_first_column = dt.IOTDataStructure()
            get_first_column = data_list[0]

            column_names.append(get_first_column.output_name)
            for single_column in get_first_column.variable_list:
                column_names.append(single_column)

            for data in data_list:
                single_raw_data = []
                single_raw_data.append(data.true_label)
                for single_data_variable in data.variables:
                    single_raw_data.append(single_data_variable)
                data_array.append(single_raw_data)
            
            data_df = pd.DataFrame(data_array, columns = column_names)
            print(data_df)
        except:
            print('Plot Error')
        
    def split(self, data_list, ratio):
        
        if type(ratio) != float:
            raise ValueError("ratio type error")
        elif (ratio <= 0 or ratio >1):
            raise ValueError("ratio range error")

        train_data_list = []
        test_data_list = []
        #Get the dictionary of each label data
        dic = {}
        for data in data_list:
            if not(data.true_label in dic):
                dic[data.true_label]= []
            dic[data.true_label].append(data)

        for dic_data_key in dic:
            count_length = len(dic[dic_data_key])
            train_count = count_length * ratio
            test_count = count_length - train_count

            rdn.shuffle(dic[dic_data_key])

            for index in range(0, len(dic[dic_data_key]),1):
                if train_count > index:
                    train_data_list.append(dic[dic_data_key][index])
                else:
                    test_data_list.append(dic[dic_data_key][index])


        print('-Finish Split Data-')
        print('First Data Count : ' + str(len(train_data_list)))
        print('Second Data Count : ' + str(len(test_data_list)))

        return train_data_list, test_data_list

    def showHistogram(self, data_list, row_index):
        self._show_common_data(data_list,row_index,'histplot')
        
    def showViolin(self, data_list, row_index):
        self._show_common_data(data_list,row_index,'violinplot')

    def showCorrelation(self,data_list , show_index_list):
        try:
            data_array = []
            column_names = []

            get_first_column = dt.IOTDataStructure()
            get_first_column = data_list[0]

            column_names.append(get_first_column.output_name)

            index = 0
            for single_column in get_first_column.variable_list:
                if index in show_index_list:
                    column_names.append(single_column)
                index = index + 1
            
            for data in data_list:
                single_raw_data = []
                single_raw_data.append(data.true_label)
                index = 0
                for single_data_variable in data.variables:
                    if index in show_index_list:
                        single_raw_data.append(single_data_variable)

                    index = index + 1
                data_array.append(single_raw_data)

            data_df = pd.DataFrame(data_array, columns = column_names)
            seaborn_plotter.heatmap(data_df.corr() , cmap="coolwarm", annot=True, vmin=-1, vmax=1, fmt='.2f')
            plt.title("Correlation")
            plt.rcParams['figure.figsize'] = self._plot_size
            plt.show()
        except ValueError:
            print('Plot Error')

    def showConfusionMatrix(self, data_list):
        try:
            confusion_matrix = []

            get_first_column = dt.IOTDataStructure()
            get_first_column = data_list[0]

            label_length = len(get_first_column.class_name_list)

            for xIndex in range(label_length):
                new_list = []
                for xIndex in range(label_length):
                    new_list.append(0)
                confusion_matrix.append(new_list)

            for single_data in data_list:
                if single_data.predict_label != -1:
                    current_count = confusion_matrix[single_data.true_label][single_data.predict_label]
                    confusion_matrix[single_data.true_label][single_data.predict_label] = current_count + 1

            seaborn_plotter.heatmap(data = confusion_matrix, vmin=0, cmap="Greens", annot=True,fmt="d")
            plt.title("Confusion Matrix")
            plt.show()
        except Exception as ex:
            print(str(ex))
            print('Plot Matrix Fail')


    #Private
    def _show_common_data(self,data_list, row_index, type):
        try:
            get_first_column = dt.IOTDataStructure()
            get_first_column = data_list[0]

            if(row_index < 0 or row_index > len(get_first_column.variables)):
                raise "No Varaiable Index [" + str(row_index) +"]"

            fig = plt.figure()
            datas = []

            data_array = []
            column_names = []

            column_names.append(get_first_column.output_name)
            for single_column in get_first_column.variable_list:
                column_names.append(single_column)

            for data in data_list:
                single_raw_data = []
                single_raw_data.append(data.true_label)
                for single_data_variable in data.variables:
                    single_raw_data.append(single_data_variable)
                data_array.append(single_raw_data)
            
            data_df = pd.DataFrame(data_array, columns = column_names)

            title_name = get_first_column.variable_list[row_index]

            # === 定義字符數量
            n_cat_unique = data_df.iloc[:,row_index].nunique()
            xticks_list = list(np.linspace(0, n_cat_unique-1, num=n_cat_unique).astype(int))

            if type == 'histplot':
                seaborn_plotter.histplot(data=data_df,bins=xticks_list, x=data_df.iloc[:,row_index], multiple='dodge', discrete=True, shrink=.8 )
            elif type == 'violinplot':
                seaborn_plotter.violinplot(data=data_df, x=data_df.iloc[:,row_index], multiple='dodge', discrete=True, shrink=.8  )


            # === 圖軸設定
            plt.rcParams['axes.titlesize'] = 16
            plt.rcParams['axes.labelsize'] = 14
            plt.rcParams['xtick.labelsize'] = 12
            plt.rcParams['ytick.labelsize'] = 12
            plt.rcParams['legend.fontsize'] = 12
            seaborn_plotter.set_style('white')

            plt.title('Histogram (%s)'%data_df.columns[row_index])
            plt.figure(figsize=(2*n_cat_unique,6))
            plt.show()

        except Exception as ex:
            print(ex)
            print('Plot Error')


