import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"D:\projects(DA)\funnel-ab-project\data\retention_cohorts.csv")
counts = df.pivot(index="cohort_week", columns="week_n", values="users")
retention = counts.div(counts[0], axis=0) * 100
print(retention.round(1).head())

plt.figure(figsize=(12, 7))
sns.heatmap(retention.iloc[:, :9], annot=True, fmt=".1f",
            cmap="Blues", cbar_kws={"label": "Retention %"})
plt.title("Weekly Cohort Retention (%)")
plt.xlabel("Weeks since first visit")
plt.ylabel("Cohort week")
plt.tight_layout()
plt.savefig(r"D:\projects(DA)\funnel-ab-project\data\retention_heatmap.png", dpi=150)
plt.show()

avg = retention.iloc[:-4].mean()
plt.figure(figsize=(8, 4))
plt.plot(avg.index[1:], avg.values[1:], marker="o")
plt.title("Average Retention Curve (Week 1 onward)")
plt.xlabel("Weeks since first visit")
plt.ylabel("Retention %")
plt.grid(alpha=0.3)
plt.savefig(r"D:\projects(DA)\funnel-ab-project\data\retention_curve.png", dpi=150)
plt.show()
print(avg.round(1))