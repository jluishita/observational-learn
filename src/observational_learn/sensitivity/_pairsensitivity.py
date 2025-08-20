import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def _get_q_statistic(paired_data, q_statistic):
    """
    """
    if q_statistic == 't-statistic':
        result = np.abs(paired_data)
    return result

def _get_sum_q_statistic(q_stat):
    """
    """
    result = np.sum(q_stat)
    return result

def _get_sum_q_statistic_squared(q_stat):
    """
    """
    result = np.sum(q_stat**2)
    return result

def _get_T_value(paired_data, q_stat):
    """
    """
    return (q_stat[paired_data>0]).sum()

def _get_approximate_pvalue(q_stat, T_value, Gamma=1):
    """
    """
    mean = (Gamma/(1 + Gamma)) * _get_sum_q_statistic(q_stat)
    variance = (Gamma/((1 + Gamma)**2)) * _get_sum_q_statistic_squared(q_stat)
    p_value = 1 - norm.cdf(T_value, loc=mean, scale=np.sqrt(variance))
    return p_value

def plot_sensitivity_analysis(
        data,
        Gamma_i=1,
        Gamma_f=10,
        n_points=50,
        q_statistic='t-statistic'
        ):
    """
    """
    q_stat = _get_q_statistic(data.paired_data, q_statistic)
    T_value = _get_T_value(data.paired_data, q_stat)
    gamma_array = np.linspace(Gamma_i, Gamma_f, n_points)
    pvalue_array = []
    for gamma in gamma_array:
        pvalue_array.append(_get_approximate_pvalue(q_stat, T_value, gamma))

    plt.figure()
    plt.plot(gamma_array, [0.05]*len(gamma_array), '--')
    plt.plot(gamma_array, pvalue_array, '-', label='p-value')
    plt.xlabel('Gamma')
    plt.ylabel('p-value')
    plt.legend()
    plt.show()