import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings
try:
    import matplotlib.pyplot as plt
except ImportError:
    warnings.warn("Matplotlib failed to import", ImportWarning)

class Oaxaca:

    def __init__(self, data, by, endo, debug = True):

        self.data = data
        self.by = by
        self.df_type = ""
        self.f_df = ""
        self.s_df = ""
        self.endo = endo
        self.two_gap = 0
        self.three_gap = 0

        self.f_mean = 0
        self.s_mean = 0

        self.char_eff = 0
        self.coef_eff = 0
        self.int_eff = 0

        self.exp_eff = 0
        self.unexp_ex = 0

        self.t_x = 0
        self.t_y = 0

        self.explained = 0
        self.unexplained = 0

        self.char_eff_var = 0
        self.coef_eff_var = 0

        self.cotton_fix_model = 0

        #A bunch of error checking
        if type(self.data) != type(pd.DataFrame()) and type(self.data) != type(np.array(1)):
            raise ValueError('The data must be in a DataFrame or a numpy array')


        if type(self.data) == type(pd.DataFrame()):
            #By must be a string
            if type(self.by) != str:
                raise ValueError('The "by" variable must be a string if datatype is {}'.format(type(self.data)))

            if type(self.endo) != str:
                raise ValueError('The "endo" variable must be a string if datatype is {}'.format(type(self.data)))

            #The by is not in the columns
            if by not in self.data.columns.values:
                raise ValueError('The "by" variable must be in the DataFrame')

            if endo not in self.data.columns.values:
                raise ValueError('The "endo" variable must be in the DataFrame')

            self.df_type = 'df'

        if type(self.data) == type(np.array(1)):
            #By must be an integer to index the numpy array
            if type(self.by) != int:
                raise ValueError('The "by" variable must be a int if datatype is {}'.format(type(self.data)))

            if type(self.by) != int:
                raise ValueError('The "endo" variable must be a int')

            self.df_type = 'np'

        if debug == False and data.shape[0] < data.shape[1]:
            raise ValueError("You have more columns, {}, than rows, {}".format(data.shape[0], data.shape[1]))

        #Split the Dataframe by the 'By' value
        if self.df_type == 'np':
            self.data = pd.DataFrame(self.data)
            split = self.data.iloc[:,by].value_counts().index

            #We need binary differences for this value
            if len(split) != 2:
                print("These are the attempted split values: {}".format(split))
                raise KeyError('There are more than 2 unique values in the by columns')

            print("These are the attempted split values: {}".format(split))

            self.t_x = self.data.drop(self.data.columns[endo], axis = 1)
            self.t_y = self.data.iloc[:, endo]

            self.f_df = self.data[self.data.iloc[:, by] == split[0]]
            self.s_df = self.data[self.data.iloc[:, by] != split[0]]

            self.f_x = self.f_df.drop(self.f_df.columns[[by, endo]], axis = 1)
            self.f_y = self.f_df.iloc[:, endo]

            self.s_x = self.s_df.drop(self.s_df.columns[[by, endo]], axis = 1)
            self.s_y = self.s_df.iloc[:, endo]

            self.f_x = sm.add_constant(self.f_x)
            self.s_x = sm.add_constant(self.s_x)
            self.t_x = sm.add_constant(self.t_x)

        if self.df_type == 'df':
            split = self.data[by].value_counts().index

            if len(split) != 2:
                print("These are the attempted split values: {}".format(split))
                raise KeyError('There are more than 2 unique values in the by columns')

            print("These are the attempted split values: {}".format(split))

            self.t_x = self.data.drop([endo], axis = 1)
            self.t_y = self.data[endo]


            self.f_df = self.data[self.data[by] == split[0]]
            self.s_df = self.data[self.data[by] != split[0]]

            self.f_x = self.f_df.drop([by,endo], axis = 1)
            self.f_y = self.f_df[endo]

            self.s_x = self.s_df.drop([by,endo], axis = 1)
            self.s_y = self.s_df[endo]

            self.f_x = sm.add_constant(self.f_x)
            self.s_x = sm.add_constant(self.s_x)
            self.t_x = sm.add_constant(self.t_x)

    def two_fold(self, plot = False, round_val = 5):
        self.f_mean = self.f_y.mean()
        self.s_mean = self.s_y.mean()

        if round_val != False:
            try:
                round_val = int(round_val)
            except ValueError:
                raise ValueError("Your round value must either by an int or be able to be casted into one.")

        self.t_model = sm.OLS(self.t_y, self.t_x).fit()
        self.t_params = self.t_model.params.drop(self.by)
        self.f_model = sm.OLS(self.f_y, self.f_x).fit()
        self.s_model = sm.OLS(self.s_y, self.s_x).fit()

        self.unexplained = (self.f_x.mean() @ (self.f_model.params - self.t_params)) + (self.s_x.mean() @ (self.t_params - self.s_model.params))

        self.explained = (self.f_x.mean() - self.s_x.mean()) @ self.t_params

        self.two_gap = self.f_mean - self.s_mean

        if round_val != False:
            self.unexplained = round(self.unexplained, round_val)
            self.explained = round(self.explained, round_val)
            self.two_gap = round(self.two_gap, round_val)

        print('Unexplained Effect: {}'.format(self.unexplained))
        print('Explained Effect: {}'.format(self.explained))
        print('Gap: {}'.format(self.two_gap))
        if plot == True:
            self.plot(plt_type = 2)

        return self.unexplained, self.explained, self.two_gap