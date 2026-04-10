import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─────────────────────────────────────────
# SETUP
# seaborn is a charting library built on top of matplotlib
# it makes professional looking charts with very little code
# matplotlib is the base layer — seaborn uses it under the hood
# ─────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="muted")

# Create a folder to save chart images
# exist_ok=True means don't throw an error if folder already exists
os.makedirs("../dashboard/charts", exist_ok=True)

# ─────────────────────────────────────────
# LOAD DATA
# We load CSVs directly — no SQL needed here
# Pandas can read any CSV into a DataFrame in one line
# ─────────────────────────────────────────

orders    = pd.read_csv("../data/orders.csv")
products  = pd.read_csv("../data/products.csv")
suppliers = pd.read_csv("../data/suppliers.csv")
shipments = pd.read_csv("../data/shipments.csv")

# Filter to completed orders only — same as WHERE status = 'Completed' in SQL
completedOrders = orders[orders["status"] == "Completed"]

print("Data loaded successfully.")
print(f"Total orders: {len(orders)}")
print(f"Completed orders: {len(completedOrders)}")


# ─────────────────────────────────────────
# ANALYSIS 1 — Summary Statistics
# .describe() gives count, mean, min, max, std deviation automatically
# This is the first thing any analyst does with a new dataset
# ─────────────────────────────────────────

print("\n" + "="*50)
print("ANALYSIS 1 — Revenue & Profit Summary")
print("="*50)

summary = completedOrders[["revenue", "cost", "profit"]].describe()
print(summary)

totalRevenue = completedOrders["revenue"].sum()
totalProfit  = completedOrders["profit"].sum()
marginPct    = round(totalProfit / totalRevenue * 100, 2)

print(f"\nTotal Revenue : ₹{totalRevenue:,.0f}")
print(f"Total Profit  : ₹{totalProfit:,.0f}")
print(f"Profit Margin : {marginPct}%")


# ─────────────────────────────────────────
# ANALYSIS 2 — Revenue by Category
# merge() is the Pandas equivalent of SQL JOIN
# we join orders with products to get the category column
# ─────────────────────────────────────────

print("\n" + "="*50)
print("ANALYSIS 2 — Revenue by Category")
print("="*50)

# merge = JOIN in Pandas
# left_on and right_on = the columns to join on (like ON o.product_id = p.ProductId)
orderProducts = completedOrders.merge(
    products,
    left_on="product_id",
    right_on="ProductId"
)

categoryRevenue = (
    orderProducts
    .groupby("category")["revenue"]   # GROUP BY category, focus on revenue column
    .sum()                             # SUM(revenue)
    .sort_values(ascending=False)      # ORDER BY revenue DESC
    .reset_index()                     # converts the grouped result back to a clean DataFrame
)

print(categoryRevenue)

# Draw bar chart
plt.figure(figsize=(10, 5))
sns.barplot(data=categoryRevenue, x="category", y="revenue", palette="Blues_d")
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Revenue (₹)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("../dashboard/charts/revenue_by_category.png", dpi=150)
plt.close()
print("Chart saved: revenue_by_category.png")


# ─────────────────────────────────────────
# ANALYSIS 3 — Monthly Revenue Trend
# pd.to_datetime converts a string date column into an actual date type
# .dt.to_period("M") extracts just the year-month (like strftime in SQL)
# ─────────────────────────────────────────

print("\n" + "="*50)
print("ANALYSIS 3 — Monthly Revenue Trend")
print("="*50)

completedOrders = completedOrders.copy()
completedOrders["orderDate"]  = pd.to_datetime(completedOrders["orderDate"])
completedOrders["yearMonth"]  = completedOrders["orderDate"].dt.to_period("M")

monthlyRevenue = (
    completedOrders
    .groupby("yearMonth")["revenue"]
    .sum()
    .reset_index()
)

# Convert period back to string for plotting
monthlyRevenue["yearMonth"] = monthlyRevenue["yearMonth"].astype(str)

print(monthlyRevenue.tail(6))  # show last 6 months

plt.figure(figsize=(12, 5))
plt.plot(
    monthlyRevenue["yearMonth"],
    monthlyRevenue["revenue"],
    marker="o", linewidth=2, color="#2196F3"
)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../dashboard/charts/monthly_revenue_trend.png", dpi=150)
plt.close()
print("Chart saved: monthly_revenue_trend.png")


# ─────────────────────────────────────────
# ANALYSIS 4 — On-Time vs Late Deliveries
# value_counts() counts how many times each unique value appears
# like SELECT isLate, COUNT(*) FROM shipments GROUP BY isLate
# ─────────────────────────────────────────

print("\n" + "="*50)
print("ANALYSIS 4 — Delivery Performance")
print("="*50)

deliveryStatus = shipments["isLate"].value_counts()
labels         = ["On Time", "Late"]
sizes          = [deliveryStatus.get(False, 0), deliveryStatus.get(True, 0)]

print(f"On Time : {sizes[0]} shipments")
print(f"Late    : {sizes[1]} shipments")
print(f"On-Time Rate: {round(sizes[0]/sum(sizes)*100, 2)}%")

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct="%1.1f%%",
        colors=["#4CAF50", "#F44336"], startangle=90)
plt.title("On-Time vs Late Deliveries")
plt.tight_layout()
plt.savefig("../dashboard/charts/delivery_performance.png", dpi=150)
plt.close()
print("Chart saved: delivery_performance.png")


# ─────────────────────────────────────────
# ANALYSIS 5 — Supplier Performance
# Here we do multiple merges (JOINs) to connect
# orders → products → suppliers
# same as a 3-table JOIN in SQL
# ─────────────────────────────────────────

print("\n" + "="*50)
print("ANALYSIS 5 — Supplier Performance")
print("="*50)

# First merge: orders + products
ordersWithProducts = completedOrders.merge(
    products, left_on="product_id", right_on="ProductId"
)

# Second merge: result + suppliers
ordersWithSuppliers = ordersWithProducts.merge(
    suppliers, left_on="SupplierId", right_on="SuppliersId"
)

supplierPerformance = (
    ordersWithSuppliers
    .groupby("SuppliersName")
    .agg(
        totalRevenue=("revenue", "sum"),   # SUM(revenue)
        totalProfit=("profit", "sum"),     # SUM(profit)
        totalOrders=("order_id", "count")  # COUNT(order_id)
    )
    .sort_values("totalRevenue", ascending=True)  # ascending for horizontal bar
    .reset_index()
)

print(supplierPerformance)

plt.figure(figsize=(10, 5))
sns.barplot(
    data=supplierPerformance,
    x="totalRevenue", y="SuppliersName",
    palette="Greens_d"
)
plt.title("Revenue by Supplier")
plt.xlabel("Total Revenue (₹)")
plt.ylabel("Supplier")
plt.tight_layout()
plt.savefig("../dashboard/charts/supplier_performance.png", dpi=150)
plt.close()
print("Chart saved: supplier_performance.png")


print("\n" + "="*50)
print("EDA Complete — 5 charts saved to /dashboard/charts/")
print("="*50)