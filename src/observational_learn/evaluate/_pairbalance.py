import pandas as pd
import numpy as np


class StandarizedDifferences():
    """
    """
    
    def __init__(self, pairing, data=None):
        self.pairing = pairing
        self.data = data

    
    def get_standarized_diff(self, df_treat, df_control):
        """
        """
        mean_treatment = df_treat.mean()
        mean_control = df_control.mean()
        
        var_treatment = df_treat.var()
        var_control = df_control.var()
        
        return (mean_treatment - mean_control) / np.sqrt((var_treatment + var_control)/2)

    
    def build_df_for_differences(self):
        """
        """
        idx_treatment = self.pairing.df_treatment.index
        idx_control = self.pairing.df_control.index
        idx_paired_control = self.pairing.df_paired_control.index
        
        data_treatment = self.data.loc[idx_treatment,:]
        data_control = self.data.loc[idx_control,:]
        data_paired_control = self.data.loc[idx_paired_control,:]

        return (data_treatment, data_control, data_paired_control)
    
    
    def differences(self):
        """
        """
        if isinstance(self.data, pd.DataFrame):
            data_treatment, data_control, data_paired_control = self.build_df_for_differences()
            std_diff_original = self.get_standarized_diff(data_treatment, data_control)
            std_diff_paired = self.get_standarized_diff(data_treatment, data_paired_control)
        else:
            std_diff_original = self.get_standarized_diff(self.pairing.df_treatment, self.pairing.df_control)
            std_diff_paired = self.get_standarized_diff(self.pairing.df_treatment, self.pairing.df_paired_control)

        df = pd.DataFrame({'Original': std_diff_original, 'Paired': std_diff_paired})

        return df
        