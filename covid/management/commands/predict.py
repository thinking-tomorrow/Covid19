from django.core.management.base import BaseCommand
from covid.models import DailyData, Predictions

import pandas as pd
import numpy as np
import math
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

class Command(BaseCommand):

    @staticmethod
    def getDailyData(country):
        daily_data = DailyData.objects.filter(country=country)
        num_of_date = iter(range(len(daily_data)))
        data_list = [{'Date': str(data.date), 'num_of_date': next(num_of_date), 'num_of_patients': data.totalcase} for data in daily_data]
        df = pd.DataFrame(data_list)
        return df


    @staticmethod
    def predict_cases(country):
        ds = Command.getDailyData(country)

        last = ds.shape[0]
        ds1 = ds.sample(frac =.15)
        ds.drop(ds1.index) 

        x = ds['num_of_date']
        y = ds['num_of_patients']
        x_test_patient = ds1['num_of_date']
        y_test_patient = ds1['num_of_patients']
        x_prediction =[[x] for x in range(last, last+7)]

        print(x_prediction)

        yy=np.log10(y)

        scores_1 = []
        scores_2 = []
        scores_3 = []
        scores_4 = []
        scores_5 = []
        ######################################################################################################################
        MLP_Regressor_1 = MLPRegressor(hidden_layer_sizes=(4), activation='tanh', solver='lbfgs' ,learning_rate_init=0.01, max_iter=1000,random_state=120, validation_fraction=0.1)
        MLP_Regressor_2 = MLPRegressor(hidden_layer_sizes=(5), activation='tanh', solver='lbfgs' ,learning_rate_init=0.01, max_iter=500,random_state=120, validation_fraction=0.1)
        MLP_Regressor_3 = MLPRegressor(hidden_layer_sizes=(1), activation='tanh', solver='lbfgs' ,learning_rate_init=0.3, max_iter=1000,random_state=120, validation_fraction=0.2)
        MLP_Regressor_4 = MLPRegressor(hidden_layer_sizes=(5), activation='relu', solver='lbfgs' ,learning_rate_init=0.01, max_iter=1000,random_state=1, validation_fraction=0.1)
        MLP_Regressor_5 = MLPRegressor(hidden_layer_sizes=(5), activation='tanh', solver='sgd' ,learning_rate_init=0.01, max_iter=1000,random_state=1, validation_fraction=0.1)
        ######################################################################################################################
        cv = KFold(n_splits=10, random_state=1, shuffle=True)
        for train_index, test_index in cv.split(x):
            X_train, X_test, y_train, y_test ,yy_train, yy_test= x[train_index], x[test_index], y[train_index], y[test_index], yy[train_index], yy[test_index]
            #
            MLP_Regressor_1.fit(X_train.values.reshape(-1,1), yy_train)
            scores_1.append(MLP_Regressor_1.score(X_test.values.reshape(-1,1), yy_test))
            #
            MLP_Regressor_2.fit(X_train.values.reshape(-1,1), yy_train)
            scores_2.append(MLP_Regressor_2.score(X_test.values.reshape(-1,1), yy_test))
            #
            MLP_Regressor_3.fit(X_train.values.reshape(-1,1), yy_train)
            scores_3.append(MLP_Regressor_3.score(X_test.values.reshape(-1,1), yy_test))
            #
            MLP_Regressor_4.fit(X_train.values.reshape(-1,1), yy_train)
            scores_4.append(MLP_Regressor_4.score(X_test.values.reshape(-1,1), yy_test))
            #
            MLP_Regressor_5.fit(X_train.values.reshape(-1,1), yy_train)
            scores_5.append(MLP_Regressor_5.score(X_test.values.reshape(-1,1), yy_test))

        print("Average score for MLP_Regressor_1:",sum(scores_1)/10,"\nAverage score for MLP_Regressor_2:",sum(scores_2)/10,"\nAverage score for MLP_Regressor_3:",sum(scores_3)/10
            ,"\nAverage score for MLP_Regressor_4:",sum(scores_4)/10,"\nAverage score for MLP_Regressor_5:",sum(scores_5)/10)

        """**After the validation we chosed best parameter for MLP (MLP_Regressor_2) to evaluate:**

        ### Evaluation
        """

        MLP_Regressor = MLPRegressor(hidden_layer_sizes=(1), activation='tanh', solver='lbfgs' ,learning_rate_init=0.01, max_iter=1000,random_state=120, validation_fraction=0.1)
        MLP_Regressor.fit(x.values.reshape(-1,1), yy)
        y_test_patient_log=np.log10(y_test_patient)
        evaluation_3 =MLP_Regressor.predict(x_test_patient.values.reshape(-1,1))
        score=MLP_Regressor.score(x_test_patient.values.reshape(-1,1), y_test_patient_log)   
        print("Final Evaluation Score for MLP_Regressor :",score)

        print('Evaluation for expecting 6 days in future in MLP_Regressor:')
        for predict in x_prediction:
            print('day',predict,'=',int(10**MLP_Regressor.predict([predict])))


    # define logic of command
    def handle(self, *args, **options):
        Command.predict_cases('India')