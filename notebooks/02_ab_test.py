import pandas as pd
from scipy import stats

df = pd.read_csv(r"D:\projects(DA)\funnel-ab-project\data\cookie_cats.csv")

print(df.shape)
print(df.head())
print(df.isna().sum())

# group sizes + sample ratio mismatch (SRM) check
counts = df["version"].value_counts()
print(counts)
chi2, p = stats.chisquare(counts)
print(f"SRM check p-value: {p:.4f}")

# retention by group
print(df.groupby("version")[["retention_1", "retention_7"]].mean().round(4) * 100)
print(df.groupby("version")["sum_gamerounds"].describe())

import numpy as np
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

a = df[df["version"] == "gate_30"]
b = df[df["version"] == "gate_40"]

for col in ["retention_1", "retention_7"]:
    xa, xb = a[col].sum(), b[col].sum()
    na, nb = len(a), len(b)

    # z-test (control vs variant)
    z, p = proportions_ztest([xb, xa], [nb, na])
    # chi-square on the 2x2 table
    table = pd.crosstab(df["version"], df[col])
    chi2, p_chi, _, _ = stats.chi2_contingency(table, correction=False)
    # 95% CI for difference (gate_40 minus gate_30)
    lo, hi = confint_proportions_2indep(xb, nb, xa, na)

    print(f"\n{col}")
    print(f"  diff = {(xb/nb - xa/na)*100:.2f} pp")
    print(f"  z-test p = {p:.4f} | chi-square p = {p_chi:.4f}")
    print(f"  95% CI = [{lo*100:.2f}, {hi*100:.2f}] pp")

# bootstrap for 7-day retention
rng = np.random.default_rng(42)
diffs = []
for _ in range(10000):
    sa = a["retention_7"].sample(len(a), replace=True, random_state=rng.integers(1e9)).mean()
    sb = b["retention_7"].sample(len(b), replace=True, random_state=rng.integers(1e9)).mean()
    diffs.append(sb - sa)
print("\nBootstrap 7-day diff 95% CI (pp):",
      np.percentile(diffs, [2.5, 97.5]).round(4) * 100)
print("P(gate_40 worse):", (np.array(diffs) < 0).mean())

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

base = 0.1902
es = proportion_effectsize(base + 0.01, base)
n = NormalIndPower().solve_power(effect_size=es, alpha=0.05, power=0.8, ratio=1)
print(f"Users needed per group to detect a 1 pp lift: {n:,.0f}")

mde = NormalIndPower().solve_power(nobs1=len(a), alpha=0.05, power=0.8,
                                   ratio=len(b)/len(a))
print(f"Minimum detectable effect size (Cohen's h) with your data: {mde:.4f}")

print(df.groupby("version")["retention_7"].agg(["sum", "count"]))