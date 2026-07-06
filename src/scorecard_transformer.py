# src/scorecard_transformer.py
import pandas as pd
import numpy as np

class ScorecardTransformer:
    """
    Unified institutional-grade transformation layer that maps raw portfolio 
    numerical and categorical data into standardized Weight-of-Evidence (WoE) features
    and calculated credit scores based on a production scorecard ledger.
    """
    def __init__(self, scorecard_points_df):
        self.scorecard_points = scorecard_points_df
        self.raw_variables = scorecard_points_df['Variable'].unique().tolist()
        
        # Isolate variables by type based on scorecard definition
        self.problematic_drops = ['mo_sin_rcnt_rev_tl_op', 'num_tl_op_past_12m', 'mo_sin_rcnt_rev_tl_op_woe', 'num_tl_op_past_12m_woe']
        self.categorical_originals = ['grade', 'term', 'verification_status']
        self.numerical_originals = [
            col for col in self.raw_variables 
            if col not in self.categorical_originals + self.problematic_drops
        ]
        self.final_features = [f"{col}_woe" for col in self.numerical_originals + self.categorical_originals]

    def fit_transform_portfolio(self, df_raw):
        """Transforms raw inputs to WoE metrics and returns standard execution arrays."""
        df = df_raw.copy()
        
        # 1. Map Numerical WoE Continuous Bins
        for col in self.numerical_originals:
            pts_sub = self.scorecard_points[self.scorecard_points['Variable'] == col]
            woe_lookup = pts_sub.set_index('Bin/Category')['WoE'].to_dict()
            
            for bin_str, woe_val in woe_lookup.items():
                raw_left = bin_str.split(',')[0].replace('(', '').replace('[', '').strip()
                raw_right = bin_str.split(',')[1].replace(')', '').replace(']', '').strip()
                
                left_side = float('-inf') if raw_left == '-inf' else float(raw_left)
                right_side = float('inf') if raw_right == 'inf' else float(raw_right)
                
                if bin_str.startswith('(') and bin_str.endswith(']'):
                    df.loc[(df[col] > left_side) & (df[col] <= right_side), f'{col}_woe'] = woe_val
                else:
                    df.loc[(df[col] >= left_side) & (df[col] <= right_side), f'{col}_woe'] = woe_val
                    
        # 2. Map Categorical WoE Strings
        for col in self.categorical_originals:
            pts_sub = self.scorecard_points[self.scorecard_points['Variable'] == col]
            cat_to_woe = pts_sub.set_index('Bin/Category')['WoE'].to_dict()
            df[f'{col}_woe'] = df[col].fillna('Missing').astype(str).map(cat_to_woe)
            
        # Ensure matrix columns are strictly numeric data frames
        X_matrix = df[self.final_features].apply(pd.to_numeric, errors='coerce').fillna(0)
        return X_matrix, df

    def generate_credit_scores(self, df_raw):
        """Generates absolute production points-based credit scores."""
        score_matrix = pd.DataFrame(0, index=df_raw.index, columns=self.scorecard_points['Variable'].unique())
        
        for col in self.numerical_originals:
            points_sub = self.scorecard_points[self.scorecard_points['Variable'] == col]
            for _, row in points_sub.iterrows():
                bin_str = str(row['Bin/Category'])
                pts = row['Score Points']
                raw_left = bin_str.split(',')[0].replace('(', '').replace('[', '').strip()
                raw_right = bin_str.split(',')[1].replace(')', '').replace(']', '').strip()
                left_side = float('-inf') if raw_left == '-inf' else float(raw_left)
                right_side = float('inf') if raw_right == 'inf' else float(raw_right)
                
                if bin_str.startswith('(') and bin_str.endswith(']'):
                    score_matrix.loc[(df_raw[col] > left_side) & (df_raw[col] <= right_side), col] = pts
                else:
                    score_matrix.loc[(df_raw[col] >= left_side) & (df_raw[col] <= right_side), col] = pts
                    
        for col in self.categorical_originals:
            points_sub = self.scorecard_points[self.scorecard_points['Variable'] == col]
            cat_to_points = points_sub.set_index('Bin/Category')['Score Points'].to_dict()
            score_matrix[col] = df_raw[col].fillna('Missing').astype(str).map(cat_to_points).fillna(int(points_sub['Score Points'].mean()))
            
        return score_matrix.sum(axis=1)