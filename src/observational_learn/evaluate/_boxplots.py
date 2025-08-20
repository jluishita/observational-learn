import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def compare_boxplots(datatable, variable, **kwargs):
    """
    """
    sns.boxplot(
        data=datatable.dataframe, 
        x="treat", 
        y=variable,
        **kwargs)