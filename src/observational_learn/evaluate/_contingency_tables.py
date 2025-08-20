import pandas as pd


def _create_variable_list(table, variables):
    """
    """
    return [table[variable] for variable in variables]

def _create_contingency_table(table, x_variables, y_variables):
    """
    """
    list_x_variables = _create_variable_list(table, x_variables)
    list_y_variables = _create_variable_list(table, y_variables)
    return pd.crosstab(list_x_variables, list_y_variables).astype('str')

def contingency_table(datatable, x_variables, y_variables):
    """
    """
    control_table = _create_contingency_table(datatable.df_control, x_variables, y_variables)
    treatment_table = _create_contingency_table(datatable.df_treatment, x_variables, y_variables)
    result_table = control_table + ' / ' + treatment_table
    return result_table