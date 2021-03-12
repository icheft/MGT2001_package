from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math
import scipy.stats as stats
from scipy.stats import norm
import statsmodels.api as sm
import statsmodels.stats.api as sms
import statsmodels.formula.api as smf


def shapiro(df, treatment_name_list, treatment_name, value_name):
    """
    check normal distribution
    """
    for i, name in enumerate(treatment_name_list):
        data = df[value_name][df[treatment_name] == name]
        stat, p = stats.shapiro(data)
        print(f'{i + 1}: Statistics={stat:.4f}, p={p:.4f}')
    return


def qq_plot(row, col, df, treatment_name_list, treatment_name, value_name, figsize=(8, 3), hspace=0.4, wspace=4):
    """
    check normal distribution
    """
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)

    for i, name in enumerate(treatment_name_list):
        ax = fig.add_subplot(row, col, i + 1)
        data = df[value_name][df[treatment_name] == name]
        sm.qqplot(data, stats.norm, fit=True, line='45', ax=ax)
        ax.set_title(treatment_name_list[i])

    fig.tight_layout()
    plt.show()
    return


def bartlett(df, treatment_name_list, treatment_name, value_name):
    """
    Equal Variances (barlett's Test)
    """
    data = []
    for i, name in enumerate(treatment_name_list):
        data.append(df[value_name][df[treatment_name] == name])

    return stats.bartlett(data)


def f_oneway(data, treatment_name, value_name):
    """
    return aov_table, render_table, f_stat, p_value
    """
    results = smf.ols(f'{value_name} ~ C({treatment_name})', data=data).fit()
    aov_table = sms.anova_lm(results, typ=2)
    f_stat, p_value = aov_table['F'][0], aov_table['PR(>F)'][0]
    render_table = aov_table.copy()
    render_table.columns = ['Sum of Squares',
                            'Degree of Freedom', 'F', 'p-value']
    # render_table.index = ['Treatment', 'Error']
    render_table.loc['Total'] = render_table.sum()
    print(f'p-value: {p_value}')
    return aov_table, render_table, f_stat, p_value
