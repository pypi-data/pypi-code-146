import pandas as pd


class BlanketFill:
    def __init__(self, df_data: pd.DataFrame = False):
        """ CSV must have features/col headers from template
        @param df_data: df data from caller function.
        """
        self.filled_data = df_data

    def populate_csv(self, attr_to_change: tuple, selected_cols: list = 'all'):
        if len(attr_to_change) != 2:
            raise ValueError(f'attr_to_change value should only contain TWO values. We received {len(attr_to_change)}')

        old_val, new_val = attr_to_change[0], attr_to_change[1]
        new_val = new_val if isinstance(new_val, list) else [new_val]

        if not isinstance(selected_cols, list):
            if selected_cols == 'all':
                selected_cols = self.filled_data.columns.tolist()
            else:
                selected_cols = [selected_cols]

        new_data_collect = []
        gather_old_idx = []
        for idx in self.filled_data.index:
            row_data = self.filled_data.loc[idx]
            for col in selected_cols:
                col_data = row_data[col]
                if isinstance(col_data, float):
                    try:
                        col_data = str(int(col_data)).lstrip().rstrip()
                    except:
                        continue
                else:
                    col_data = str(col_data).lstrip().rstrip()

                if old_val != col_data:
                    continue
                else:
                    gather_old_idx.append(idx)
                    old_row = row_data.to_dict()
                    for nv in new_val:
                        new_row = old_row.copy()
                        new_row[col] = nv
                        new_data_collect.append(new_row)

        self.filled_data.drop(gather_old_idx, inplace=True)
        self.filled_data.reset_index(inplace=True, drop=True)
        new_data = pd.DataFrame(new_data_collect)
        self.filled_data = pd.concat([self.filled_data, new_data], ignore_index=True)
        self.filled_data.drop_duplicates(inplace=True)

    def fix_csv(self, config_dict: dict, affect_only_columns_dict: dict):
        for k, v in config_dict.items():
            change_item = tuple([k, v])
            # if we only want to AFFECT one col values
            if affect_only_columns_dict:
                # if BOTH keys match then we must only want to work on specific column(s)
                for k_affect, only_affect in affect_only_columns_dict.items():
                    if k_affect == k:
                        only_affect = only_affect if isinstance(only_affect, list) else [only_affect]
                        self.populate_csv(attr_to_change=change_item, selected_cols=only_affect)
                    else:
                        self.populate_csv(attr_to_change=change_item)
            else:
                self.populate_csv(attr_to_change=change_item)
