# Customer Segmentation & Retention Strategy - RFM Analysis

## Business Problem
A UK-based online retailer (all-occasion gifts, ~4,300 active customers, £8.9M annual revenue) has no formal way of distinguishing its most valuable customers from one-time or lapsed buyers. Marketing spend is applied uniformly across all customers, with no targeting based on purchase behavior.

**Question:** Which customers drive the business, which are at risk of churning, and what should marketing do differently for each group?

## Approach
1. **Data cleaning** — Started with 541,909 raw transaction records (Dec 2010–Dec 2011). Removed 135,080 rows with no Customer ID (can't attribute to a customer), 9,288 cancelled orders, and rows with invalid quantity/price. Final dataset: 397,884 transactions across 4,338 customers.
2. **RFM scoring** — For every customer, calculated:
   - **Recency**: days since last purchase
   - **Frequency**: number of distinct orders
   - **Monetary**: total amount spent
   Each dimension was scored 1–5 using quintiles, then combined into 7 customer segments (Champions, Loyal Customers, At Risk, Lost, etc.)
3. **Segment analysis** — Measured what share of customers and revenue each segment represents.

## Key Findings

| Segment | % of Customers | % of Revenue | Avg Days Since Last Purchase |
|---|---|---|---|
| Champions | 21.5% | **70.2%** | 15 |
| At Risk | 6.3% | 4.9% | 137 |
| Lost | 19.0% | 2.1% | 229 |

- **A fifth of customers generate over two-thirds of all revenue.** Champions (934 customers) alone drive £6.26M of the £8.9M total — this is the segment the business cannot afford to lose, and current marketing treats them the same as everyone else.
- **The At Risk segment is the clearest missed opportunity.** These 275 customers used to purchase frequently (avg. 4.9 orders) and spent an average of £1,575 each — the highest average spend outside Champions — but haven't ordered in ~137 days. This is a warm audience, not a cold one.
- **19% of the customer base (824 people) is effectively Lost**, contributing just 2.1% of revenue. Continued marketing spend on this group has a low return.

## Recommendations
1. **Protect Champions**: introduce a loyalty/VIP tier (early access, free shipping) — losing even 5% of this segment would cost more revenue than the entire Lost + At Risk segments combined.
2. **Win back At Risk customers**: targeted email campaign with a time-limited incentive. This group has proven high spend behavior, making it the highest-ROI segment to re-engage versus acquiring new customers.
3. **Stop broad-spend marketing to Lost customers**: reallocate that budget toward At Risk win-back and Champions retention.

## Tools Used
Python (Pandas, Matplotlib) for data cleaning and RFM scoring · CSV outputs designed to plug directly into Power BI/Excel for dashboarding.

## Files in this repo
- `data/cleaned_transactions.csv` — cleaned transaction-level data
- `outputs/rfm_segmented_customers.csv` — every customer with RFM scores and assigned segment
- `outputs/segment_summary.csv` — segment-level summary table
- `outputs/segment_chart.png` — customer share vs. revenue share by segment
- `rfm_analysis.py` — full analysis script, cleaning to segmentation

## Dataset
[UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail) — transnational transaction data, Dec 2010–Dec 2011, UK-based online retailer.