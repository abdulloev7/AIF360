# Assignment 4: Evaluating Reweighing on Adult, German and COMPAS

This folder is part of my fork of [IBM AIF360](https://github.com/Trusted-AI/AIF360). It contains my evaluation of the **Reweighing** pre-processing algorithm (Kamiran & Calders, 2012) for the Data Wrangling course, Assignment 4, Task 2. I use the AIF360 implementation of Reweighing as it is; the code I wrote is the evaluation pipeline in the notebook.

## Files

| File | What it is |
|---|---|
| `Reweighing_evaluation.ipynb` | The full pipeline, already run with all outputs saved |
| `Reweighing_evaluation.html` | The same notebook as HTML, for reading without Jupyter |
| `download_data.py` | Downloads the three raw datasets into the folder AIF360 reads from |
| `requirements.txt` | Exact library versions I used |
| `results/` | CSV tables and the figure produced by the notebook |

## How to reproduce my results

Tested with **Python 3.13** on Linux. Run all commands from this folder.

```bash
# 1. Clone the fork and go to this folder
git clone https://github.com/abdulloev7/AIF360.git
cd AIF360/assignment4_reweighing

# 2. Create a clean virtual environment and install the exact versions
python3.13 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Download the raw data (AIF360 does not ship it)
python download_data.py

# 4. Run the notebook from top to bottom and save the outputs in place
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1200 Reweighing_evaluation.ipynb
```

The run takes about 1-2 minutes. You can also open the notebook with `jupyter notebook Reweighing_evaluation.ipynb` and choose *Run All*.

**Important:** use `pandas` 2.x as in `requirements.txt`. AIF360 0.6.1 crashes with pandas 3 when it loads the datasets.

If `archive.ics.uci.edu` is unreachable, download `adult.data`, `adult.test` (Adult) and `german.data` (Statlog German Credit) from any mirror and put them in `<site-packages>/aif360/data/raw/adult/` and `.../raw/german/`. `python download_data.py` prints that folder.

## Parameter settings

| Setting | Value |
|---|---|
| Adult | protected `sex` (privileged = Male); `fnlwgt` dropped; `race` one-hot encoded as a normal feature |
| German | protected `age` (privileged = older than 25); `personal_status` and `sex` dropped |
| COMPAS | protected `race` (privileged = Caucasian); `sex` dropped; favourable label = no re-offence in two years |
| Split | 70/30, stratified on label and protected group together, `random_state=42` |
| Reweighing | `aif360.algorithms.preprocessing.Reweighing`, fitted on the training set only |
| Classifier | `LogisticRegression(max_iter=1000, solver="lbfgs")` on `StandardScaler` features, weights passed as `sample_weight`; threshold 0.5 |
| Metrics | DP_Diff (`statistical_parity_difference`), DIR (`disparate_impact`), consistency (k = 5, standardised features), accuracy, balanced accuracy |
| Robustness | the full pipeline repeated for seeds 0-9, mean ± std reported |

Consistency uses the same formula as AIF360's `BinaryLabelDatasetMetric.consistency`, but with a vectorised brute-force kNN because the AIF360 version is very slow on Adult and COMPAS. The notebook checks that both give the same value on German.

## Main results (test set, mean ± std over 10 seeds)

| Dataset | Model | DP_Diff | DIR | Consistency | Accuracy |
|---|---|---|---|---|---|
| Adult | Baseline LR | -0.186 ± 0.005 | 0.293 ± 0.012 | 0.942 | 0.849 |
| Adult | Reweighing + LR | -0.087 ± 0.005 | 0.598 ± 0.017 | 0.944 | 0.843 |
| German | Baseline LR | -0.238 ± 0.069 | 0.702 ± 0.079 | 0.812 | 0.743 |
| German | Reweighing + LR | -0.070 ± 0.055 | 0.910 ± 0.070 | 0.816 | 0.743 |
| COMPAS | Baseline LR | -0.162 ± 0.030 | 0.777 ± 0.036 | 0.863 | 0.668 |
| COMPAS | Reweighing + LR | -0.002 ± 0.027 | 0.998 ± 0.042 | 0.861 | 0.663 |
