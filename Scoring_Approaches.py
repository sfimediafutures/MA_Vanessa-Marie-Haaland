import math

"""
Class for inferring the different scores of preference for user-item pairs.

All methods take a pandas dataframe with user-item interaction data as input, 
and requires the columns:
- 'click': number of clicks the user made on the item.
- 'impressions': number of times the item was shown to the user.

All methods also take a threshold for simplicity, but it is not used in all of them.

Each method returns the dataframe with at least one new column added for the inference in question.
Details on the inferences can be found my thesis document.

Methods:
- binary
- clickThroughRate
- normalized
- sqrtNormalized
- impressionPenaltyNormalized
- all_approaches
    - Runs all the methods above and returns the dataframe with all the new columns added.
"""

class Scoring_Approaches:
    def __init__(self) -> None:
        pass

    def binary(self, threshold, df):
        df['binary'] = df['click'].apply(lambda x: 1 if x > 0 else 0)
        return df

    def clickThroughRate(self, threshold, df):
        df['CTR'] = df['click'] / df['Impressions']
        return df
    
    def normalized(self, threshold, df):
        df['N'] = df['click'] / threshold
        df['N'] = df['N'].apply(lambda x: min(1, x))
        return df
    
    def sqrtNormalized(self, threshold, df):
        df['SqrtN'] = df['click'] / threshold
        df['SqrtN'] = df['SqrtN'].apply(lambda x: min(1, math.sqrt(x)))
        return df
    
    def impressionPenaltyNormalized(self, threshold, df):
        df['IPN'] = df['click'] / threshold
        df['IPN'] = df['IPN'].apply(lambda x: min(1, x))
        df['IPN'] = df.apply(lambda row: max(-0.5,-0.005 * row['Impressions']) if row['IPN'] == 0 else row['IPN'], axis=1)
        return df
    
    
    def all_approaches(self,threshold, df):
        for i in [self.binary, self.clickThroughRate, self.normalized, self.sqrtNormalized, self.impressionPenaltyNormalized]:
            df = i(threshold, df)
        return df
