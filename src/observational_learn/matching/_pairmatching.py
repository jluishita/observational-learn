import pandas as pd
from scipy.special import logit


class AbstractMatching():
    """
    Abstract class for matching methods
    """
    
    def __init__(self, datatable):
        self.df_control_copy = datatable.df_control.copy()
        self.df_treatment = datatable.df_treatment
        self.y_treatment = datatable.y_treatment
        self.y_control = datatable.y_control

        self.df_paired_idx = pd.DataFrame(columns=['treatment', 'control'])
        self.df_paired_outcomes = pd.DataFrame(columns=['treatment', 'control'])

    def add_outcomes_to_paired_outcomes(self, treatment_index, control_index):
        """
        Adds outcomes of paired treatment and control elements
        """
        series = pd.DataFrame({
            'treatment' : [self.y_treatment.loc[treatment_index]],
            'control' : [self.y_control.loc[control_index]]
        })

        self.df_paired_outcomes = pd.concat(
            [self.df_paired_outcomes,
            series], ignore_index=True)

    def add_idx_to_paired_idx(self, treatment_index, control_index):
        """
        Add paired outcomes to df_paired_outcomes dataframe
        """
        series = pd.DataFrame({
            'treatment' : [treatment_index],
            'control' : [control_index]
        })
        self.df_paired_idx = pd.concat(
            [self.df_paired_idx,
            series], ignore_index=True)

    def find_pair(self, element, element_index):
        pass

    def pair_matching(self):
        """
        Main function. It is the only function that is supposed to be called by the user
        """
        for treat in self.df_treatment.itertuples(index=False):

            treat_index = self.df_treatment.loc[self.df_treatment.eq(treat).all(1)].index[0]
            pair = self.find_pair(treat, treat_index)
            if not isinstance(pair, pd.DataFrame):
                continue
            pair_index = pair.index[0]
            self.df_control_copy = self.df_control_copy.drop([pair_index])
            self.add_outcomes_to_paired_outcomes(
                treat_index,
                pair_index
            )
            self.add_idx_to_paired_idx(treat_index, pair_index)


class GreedyPSM(AbstractMatching):
    """
    Class that performs matching based on the propensity score of the elements

    Each element in the control group is only considered once

    Follows a greedy approach: for each element in the treatment group takes as pair 
    the closest element in the control group, without considering global optima
    """

    def __init__(self, datatable, logit_score=False):
        super().__init__(datatable)
        self.logit_score = logit_score
        if self.logit_score: self.apply_logit()

    def apply_logit(self):
        """
        """
        self.table.df_control['logit_ps'] = logit(self.table.df_control['propensity_score'])
        self.table.df_treatment['logit_ps'] = logit(self.table.df_treatment['propensity_score'])

    def find_pair(self, element, element_index):
        """
        Finds the closest element in the control group based on the propensity score
        """
        if self.logit_score:
            index = (self.table.df_control['logit_ps']-element.logit_ps).abs().argsort()[:1]
        else:
            index = (self.table.df_control['propensity_score']-element.propensity_score).abs().argsort()[:1]
        pair = self.table.df_control.iloc[index]
        return pair


class ExactPairMatching(AbstractMatching):
    """
    Class that performs exact pair matching

    Unless the number of covariates is small, this method is NOT expected to work well

    It has been developed for illustrative purposes
    """

    def __init__(self, datatable):
        super().__init__(datatable)
        self.discarded_idx = []

    def find_pair(self, element, element_index):
        """
        Finds an element in the control group with the same covariates
        """
        pair = self.df_control_copy.loc[self.df_control_copy.eq(element).all(1)]
        if len(pair) == 0:
            self.discarded_idx.append(element_index)
            return 'NOPAIR'
        return pair.iloc[[0]]
