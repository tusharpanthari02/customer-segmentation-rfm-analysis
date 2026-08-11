"""
Customer Segmentation & Retention Strategy — RFM Analysis
Dataset: UCI Online Retail Dataset (541,909 transactions, Dec 2010-Dec 2011)

This script:
1. Cleans raw transaction data
2. Calculates Recency, Frequency, Monetary (RFM) scores per customer
3. Segments customers into actionable business groups
4. Outputs a summary table and chart for reporting
"""

import pandas as pd
import matplotlib.pyplot as plt

RAW_FILE = "data/Online_Retail.xlsx"  # place the raw UCI file here
OUTPUT_DIR = "outputs"


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Drop transactions with no customer ID -- can't attribute to a customer
    df = df.dropna(subset=["CustomerID"])

    # Drop cancelled orders (InvoiceNo starting with 'C')
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Drop invalid quantity/price rows (data entry errors)
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["CustomerID"] = df["CustomerID"].astype(int)

    return df


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg(
        {
            "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
            "InvoiceNo": "nunique",
            "TotalPrice": "sum",
        }
    ).reset_index()
    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]

    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    ).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    rfm["Segment"] = rfm.apply(assign_segment, axis=1)
    return rfm


def assign_segment(row) -> str:
    if row["RFM_Score"] >= 13:
        return "Champions"
    elif row["R_Score"] >= 4 and row["F_Score"] >= 3:
        return "Loyal Customers"
    elif row["R_Score"] >= 4 and row["F_Score"] <= 2:
        return "New Customers"
    elif row["R_Score"] == 3:
        return "Potential Loyalists"
    elif row["R_Score"] <= 2 and row["F_Score"] >= 4:
        return "At Risk"
    elif row["R_Score"] <= 2 and row["F_Score"] <= 2 and row["M_Score"] <= 2:
        return "Lost"
    else:
        return "Needs Attention"


def summarize(rfm: pd.DataFrame) -> pd.DataFrame:
    summary = (
        rfm.groupby("Segment")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Recency_Days=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Total_Revenue=("Monetary", "sum"),
            Avg_Revenue_Per_Customer=("Monetary", "mean"),
        )
        .round(1)
        .sort_values("Total_Revenue", ascending=False)
    )
    summary["Pct_of_Customers"] = (
        summary["Customers"] / summary["Customers"].sum() * 100
    ).round(1)
    summary["Pct_of_Revenue"] = (
        summary["Total_Revenue"] / summary["Total_Revenue"].sum() * 100
    ).round(1)
    return summary


def plot_segments(summary: pd.DataFrame, out_path: str):
    summary = summary.sort_values("Total_Revenue", ascending=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].barh(summary.index, summary["Pct_of_Customers"], color="#6E8898")
    axes[0].set_xlabel("% of Total Customers")
    axes[0].set_title("Customer Share by Segment")

    axes[1].barh(summary.index, summary["Pct_of_Revenue"], color="#CD5334")
    axes[1].set_xlabel("% of Total Revenue")
    axes[1].set_title("Revenue Share by Segment")

    plt.suptitle(
        "RFM Customer Segmentation — Customer Share vs Revenue Share",
        fontsize=13,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    df = load_and_clean(RAW_FILE)
    df.to_csv(f"data/cleaned_transactions.csv", index=False)

    rfm = calculate_rfm(df)
    rfm.to_csv(f"{OUTPUT_DIR}/rfm_segmented_customers.csv", index=False)

    summary = summarize(rfm)
    summary.to_csv(f"{OUTPUT_DIR}/segment_summary.csv")
    print(summary)

    plot_segments(summary, f"{OUTPUT_DIR}/segment_chart.png")
    print("Done. Outputs saved to", OUTPUT_DIR)
