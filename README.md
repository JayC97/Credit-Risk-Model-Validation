# Retail Credit Scorecard Verification Framework

An institutional model validation suite built to satisfy Model Risk Management (MRM) guidelines. This framework replicates, stress-tests, and benchmarks the core credit risk rating engine against machine learning challenger models using an Out-of-Time (OOT) test matrix.

## 📁 Repository Architecture

```text
├── notebooks/
│   ├── 01_replication_check.ipynb    <- Verifies baseline Gini/KS replication
│   ├── 02_data_integrity_psi.ipynb   <- Population stability and drift tracking
│   ├── 03_global_calibration.ipynb   <- Wald Significance testing & Hosmer-Lemeshow checks
│   ├── 04_segment_analysis.ipynb     <- Portfolio micro-segment stress-testing 
│   ├── 05_challenger_models.ipynb    <- Monotone XGBoost & Random Forest benchmarking
│   └── 06_failure_analysis.ipynb     <- Post-mortem evaluation of boundary condition failures
├── src/
│   ├── data_loader.py                <- Automated validation data split ingest layer
│   └── metrics.py                    <- Base math routines (Gini, KS, PSI tracking)
├── validation_report.md              <- Official SR 11-7 validation summary document
└── requirements.txt                  <- Python pinning constraints

## 💾 Data Governance & Repository Structure

Due to enterprise data conservation guidelines and remote asset storage limits, the massive historic training and development data arrays are managed via decoupled upstream infrastructure (or simulated via local disk layers). 

To ensure immediate validation reproducibility for auditors and reviewers, this repository explicitly includes:
* **`df_oot_final.csv`**: The complete, standalone Out-of-Time (OOT) production validation split (86,951 accounts) required to replicate all Phase 3 through Phase 6 calibration, stress-testing, and forensic failure audits.
* **`df_scorecard_points.csv`**: The final production-approved credit scorecard allocation matrices utilized by the `ScorecardTransformer` engine.
