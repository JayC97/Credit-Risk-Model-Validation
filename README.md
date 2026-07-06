# Retail Credit Scorecard Verification Framework

An institutional model validation suite built to satisfy Model Risk Management (MRM) guidelines (SR 11-7). This framework replicates, stress-tests, and benchmarks the core credit risk rating engine against machine learning challenger fleets using an Out-of-Time (OOT) test matrix.

## 📁 Repository Architecture & Data Governance

Due to enterprise data conservation guidelines, information security protocols, and remote asset storage limits, massive historic training and development data arrays are managed via decoupled upstream infrastructure. To ensure immediate validation reproducibility for auditors and reviewers, this repository houses both the core codebase and the critical standalone validation files:

```text
├── notebooks/
│   ├── 01_replication_check.ipynb    <- Verifies baseline Gini/KS replication
│   ├── 02_data_integrity_psi.ipynb   <- Population stability, missingness audits & CSI tracking
│   ├── 03_global_calibration.ipynb   <- Wald Significance, Hosmer-Lemeshow, and Visual Reliability Diagrams
│   ├── 04_segment_analysis.ipynb     <- Portfolio micro-segment share & tail-risk concentration filtering
│   ├── 05_challenger_models.ipynb    <- Monotone XGBoost & Random Forest cross-segment battle grids
│   └── 06_failure_analysis.ipynb     <- Risk decile error concentrations & percentile boundary forensics
├── src/
│   ├── data_loader.py                <- Automated validation data split ingest layer
│   ├── metrics.py                    <- Base math routines (Gini, KS, PSI tracking)
│   └── scorecard_transformer.py      <- Centralized object-oriented scorecard scoring engine
├── df_oot_final.csv                  <- Complete standalone Out-of-Time (OOT) validation split (86,951 accounts)
├── df_scorecard_points.csv           <- Production-approved scorecard allocation matrices for the transformer
├── validation_report.md              <- Official SR 11-7 validation summary sign-off document
└── requirements.txt                  <- Python pinning constraints
