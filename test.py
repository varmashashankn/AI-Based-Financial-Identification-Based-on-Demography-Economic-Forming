import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

child_schemes = ['Samagra Shiksha', 'CBSE Udaan Scholarship Scheme', 'Integrated Child Development Services']
male_schemes = ['Public Provident Fund (PPF)', 'Recurring Deposits (RD)', 'Time Deposit (TD)']
female_schemes = ['Sukanya Samriddhi Account (SSA)', 'Mahila Samriddhi Samman Patras (MSSC)']
senior_schemes = ['Senior Citizen Social Security (SCSS)', 'Postal Life Insurance (PLI)', 'Rural Postal Life Insurance (RPLI)']

dataset = pd.read_csv("Dataset/India_demography")
names = np.unique(dataset['State name']).ravel()
'''
for i in range(len(names)):
    population = dataset.loc[dataset['State name'] == names[i]]
    population = population.values
    for j in range(len(population)):
        male = population[j,3]
        female = population[j,4]
        child = population[j,5]/1.3
        senior =  population[j,6]
        count = np.asarray([male, female, child, senior])
        highest = np.argmax(count)
        print(highest)
        result = ""
        if highest == 0:
            result = "Male Population is high so MALE Schemes can be applied"
        elif highest == 1:
            result = "Female Population is high so FEMALE Schemes can be applied ==== "+names[i]
        elif highest == 2:
            result = "Child Population is high so Childrens Schemes can be applied === "+names[i]
        elif highest == 3:
            result = "Senior Citizens Population is high so Senior Citizen Schemes can be applied"
        print(result)    
'''
population = dataset.loc[dataset['State name'] == 'HIMACHAL PRADESH']
population = population[['Male', 'Female', 'Child', 'Senior_Citizen']]
population = population.values
pop = [np.sum(population[:,0]), np.sum(population[:,1]), np.sum(population[:,2]), np.sum(population[:,3])]
plt.pie(pop, labels=['Male', 'Female', 'Child', 'Senior_Citizen'], autopct='%.0f%%')
plt.title("State Wise Population Graph")
plt.show()


