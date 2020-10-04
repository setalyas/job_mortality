# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 00:11:38 2020

@author: setat
"""

import pandas as pd
import matplotlib.pyplot as plt; plt.style.use('ggplot')

fp = 'RawData\\Mortality by occupation in England and Wales.xls'
xls = pd.read_excel(fp, sheet_name=None, encoding='utf8')

# Codes from https://www.hesa.ac.uk/support/documentation/occupational/soc90

for sex in xls.keys():
    df = xls[sex]
    df.columns = ['rank', 'SOC', 'person-years', 'mortality']
    df['mortality'], df['ci'] = df['mortality'].str.split(' ', 1).str
    df['ci'] = df['ci'].str.replace('(', '').str.replace(')', '')
    df['ci_min'], df['ci_max'] = df['ci'].str.split('–').str
    df.drop(['rank', 'SOC', 'ci'], axis=1, inplace=True)
    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    df = df.iloc[:-1]
    print(df.head(1).T)
    df.to_csv('AmendedData\\Mortality_by_occupation_{}.xls'.format(sex))
    df['cops'] = df.index.str.contains('Protective service occupations')  # *
    xls[sex] = df
    
"""Category 331: Protective service occupations
3311 Non-commissioned officers and other ranks
3312 Police officers (sergeant and below)
3313 Fire service officers (watch manager and below)
3314 Prison service officers (below principal officer)
3319 Protective service associate professionals n.e.c."""

fig, ax = plt.subplots(figsize=(10, 20))
color_swap = {True: '#960018', False: '#aec6cf'}
colors = [color_swap[i] for i in xls['Men']['cops']]
xls['Men']['mortality'].plot.barh(ax=ax, color=colors)
ax.set_title('Mortality by occupation in\nEngland and Wales in men',
             fontsize=20)
ax.set_xlabel('Age-standardised mortality rates per 100,000 person-years',
              fontsize=10)
sources = """Data from: ONS Longitudinal Study
Source: https://doi.org/10.1016/S2468-2667(17)30193-7"""
ax.annotate(sources, (10, 60), xycoords='figure points',
            color='grey')
plt.tight_layout()
plt.savefig('Outputs\\mortality_by_occupation_men.png')