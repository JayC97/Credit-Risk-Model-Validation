import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.metrics import roc_auc_score

def calculate_gini_and_ks(y_true, y_prob):
    """
    Computes global validation metrics down to identical floating-point precision.
    """
    auc = roc_auc_score(y_true, y_prob)
    gini = 2 * auc - 1
    
    # Calculate KS via empirical CDFs
    df = pd.DataFrame({'target': y_true, 'prob': y_prob})
    df = df.sort_values(by='prob').reset_index(drop=True)
    
    df['cum_goods'] = (1 - df['target']).cumsum() / (1 - df['target']).sum()
    df['cum_bads'] = df['target'].cumsum() / df['target'].sum()
    ks_stat = (df['cum_goods'] - df['cum_bads']).abs().max()
    
    return {"AUC": auc, "Gini": gini, "KS": ks_stat}

def calculate_psi(expected, actual, num_bins=10):
    """
    Computes Population Stability Index with automated zero-frequency epsilon padding.
    """
    # Create fixed cuts based on expected (Training) distribution
    percentiles = np.linspace(0, 100, num_bins + 1)
    cuts = np.percentile(expected, percentiles)
    cuts = sorted(list(set(cuts))) # Deduplicate overlapping score ties
    cuts[0], cuts[-1] = -np.inf, np.inf
    
    expected_binned = pd.cut(expected, bins=cuts).value_counts(normalize=True).sort_index()
    actual_binned = pd.cut(actual, bins=cuts).value_counts(normalize=True).sort_index()
    
    psi_df = pd.DataFrame({'Expected': expected_binned, 'Actual': actual_binned}).fillna(1e-5)
    
    psi_val = np.sum((psi_df['Actual'] - psi_df['Expected']) * np.log(psi_df['Actual'] / psi_df['Expected']))
    return psi_val, psi_df

def hosmer_lemeshow_test(y_true, y_prob, num_groups=10):
    """
    Executes the formal statistical Hosmer-Lemeshow test for global calibration tracking.
    """
    df = pd.DataFrame({'actual': y_true, 'prob': y_prob})
    # Group into risk deciles
    df['decile'] = pd.qcut(df['prob'], q=num_groups, duplicates='drop', labels=False)
    
    hl_df = df.groupby('decile').agg(
        total_obs=('actual', 'count'),
        observed_bads=('actual', 'sum'),
        expected_prob=('prob', 'mean')
    ).reset_index()
    
    hl_df['expected_bads'] = hl_df['total_obs'] * hl_df['expected_prob']
    hl_df['observed_goods'] = hl_df['total_obs'] - hl_df['observed_bads']
    hl_df['expected_goods'] = hl_df['total_obs'] - hl_df['expected_bads']
    
    # Compute chi-squared component
    chi_square_stat = np.sum(
        ((hl_df['observed_bads'] - hl_df['expected_bads'])**2 / hl_df['expected_bads']) +
        ((hl_df['observed_goods'] - hl_df['expected_goods'])**2 / hl_df['expected_goods'])
    )
    
    degrees_of_freedom = num_groups - 2
    p_value = 1.0 - chi2.cdf(chi_square_stat, degrees_of_freedom)
    
    return {"HL_Statistic": chi_square_stat, "p_value": p_value}