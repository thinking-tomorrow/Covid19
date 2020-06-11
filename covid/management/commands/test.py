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
    def predict_cases(country):

        path = 'https://raw.githubusercontent.com/AbedMHroub/Corona-virus-COVID19-predictions-project/master/dataset/Infected.csv'
        ds = pd.read_csv(path, index_col=0)
        ds.head(13)
        x = ds['num_of_date']
        y = ds['num_of_patients']
        x_test_patient = ds['num_of_date_test'][:12]
        y_test_patient = ds['num_of_patients_test'][:12]
        x_prediction = [[95], [96], [97], [98], [99], [100], [101]]

        linear_regression = LinearRegression()

        yy = np.log10(y)

        scores = []
        ######################################################################################################################
        Linear_Regression = LinearRegression()
        ######################################################################################################################
        cv = KFold(n_splits=10, random_state=1, shuffle=True)
        for train_index, test_index in cv.split(x):
            X_train, X_test, y_train, y_test, yy_train, yy_test = x[train_index], x[test_index], y[train_index], y[
                test_index], yy[train_index], yy[test_index]
            Linear_Regression.fit(X_train.values.reshape(-1, 1), yy_train)
            scores.append(Linear_Regression.score(X_test.values.reshape(-1, 1), yy_test))

        print("Average score for Linear Regression:", sum(scores) / len(scores))

        Linear_Regression.fit(x.values.reshape(-1, 1), yy)
        y_test_patient_log = np.log10(y_test_patient)
        evaluation_1 = Linear_Regression.predict(x_test_patient.values.reshape(-1, 1))
        score = Linear_Regression.score(x_test_patient.values.reshape(-1, 1), y_test_patient_log)
        print("Final Evaluation Score for Linear Regression :", score)

        print('Evaluation for expecting 6 days in future in Linear_Regression:')
        for predict in x_prediction:
            print('day', predict, '=', int(10 ** Linear_Regression.predict([predict])))

    def handle(self, *args, **options):
        x = Command.predict_cases('India')
        print(x)