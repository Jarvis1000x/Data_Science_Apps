import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error, r2_score

dataset = pd.read_csv("solubility.csv")
X = dataset.drop(['logS'], axis=1)
Y = dataset.iloc[:, -1]

model = linear_model.LinearRegression()
model.fit(X, Y)

Y_pred = model.predict(X)

# Model Performance
print('Coefficients:', model.coef_)
print('Intercept:', model.intercept_)
print('Mean squared error (MSE): %.2f'
      % mean_squared_error(Y, Y_pred))
print('Coefficient of determination (R^2): %.2f'
      % r2_score(Y, Y_pred))

# Model equation
print('LogS = %.2f %.2f LogP %.4f MW + %.4f RB %.2f AP' % (model.intercept_, model.coef_[0], model.coef_[1], model.coef_[2], model.coef_[3]))

plt.figure(figsize=(5,5))
plt.scatter(x=Y, y=Y_pred, c="#7CAE00", alpha=0.3)
z = np.polyfit(Y, Y_pred, 1)
p = np.poly1d(z)

plt.plot(Y, p(Y), "#F8569D")
plt.ylabel('Predicted LogS')
plt.xlabel('Experimental LogS')

pickle.dump(model, open('solubility_model.pkl', 'wb'))
