# Supply Chain Analytics Dashboard

An end-to-end data analytics project simulating a real-world supply chain,
built to demonstrate SQL, Python, and data visualisation skills.

**Live Dashboard →  https://goushithm22.github.io/supply-chain-dashboard/dashboard/ **

---

## What This Project Does

Analyses 500 orders across 10 products and 5 global suppliers over 2 years,
surfacing key business insights around revenue, profitability, delivery
performance, and supplier efficiency.

---

## Key Insights Found

| Metric | Value |
|--------|-------|
| Total Revenue | ₹2.04 Crore |
| Profit Margin | 65.9% |
| On-Time Delivery Rate | ~75% |
| Top Category by Revenue | Electronics |
| Best Performing Supplier | EuroGoods GmbH |

---

## Tech Stack

| Layer | Tools Used |
|-------|-----------|
| Data Generation | Python, Faker |
| Data Storage | SQLite |
| Analysis | SQL (10 queries), Pandas |
| Visualisation | Matplotlib, Seaborn, Chart.js |
| Dashboard | HTML, CSS, JavaScript |

---

## Project Structure

SupplyChainDashboard/
│
├── data/                   # Generated CSV files + SQLite database
│   ├── orders.csv
│   ├── products.csv
│   ├── suppliers.csv
│   └── shipments.csv
│
├── sql/                    # SQL queries + runner script
│   ├── analysis_queries.sql
│   └── runQueries.py
│
├── analysis/               # Python scripts
│   ├── generateData.py     # Synthetic data generation
│   └── eda.py              # Exploratory data analysis + charts
│
├── dashboard/              # Interactive web dashboard
│   ├── index.html
│   └── charts/             # PNG charts from EDA
│
└── README.md

---

## SQL Queries Covered

| # | Query | Concept |
|---|-------|---------|
| 1 | Total revenue, cost, profit | Aggregation |
| 2 | Revenue by product category | GROUP BY |
| 3 | Top 5 products by profit | ORDER BY + LIMIT |
| 4 | Monthly revenue trend | Date functions |
| 5 | On-time vs late deliveries | JOIN + CASE WHEN |
| 6 | Supplier performance scorecard | 3-table JOIN |
| 7 | Order status by region | Multi-column GROUP BY |
| 8 | Profit margin by product | Calculated columns |
| 9 | Running total of revenue | Window function |
| 10 | Late orders with full details | Multi-table JOIN + filter |

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/goushithm22/supply-chain-dashboard.git
cd supply-chain-dashboard
```

**2. Install dependencies**
```bash
pip install pandas faker matplotlib seaborn
```

**3. Generate the dataset**
```bash
cd analysis
python generateData.py
```

**4. Run SQL queries**
```bash
cd ../sql
python runQueries.py
```

**5. Run Python EDA**
```bash
cd ../analysis
python eda.py
```

**6. Launch the dashboard**
```bash
cd ..
python -m http.server 8000
# Open http://localhost:8000/dashboard/
```

---

## What I Learned

- Designing a **star schema** data model from scratch
- Writing **production-style SQL** including window functions and multi-table JOINs
- Using **Pandas** for in-memory data transformation and EDA
- Building a **standalone interactive dashboard** without BI tool dependencies
- The difference between **fact tables and dimension tables** in data warehousing

---

*Built by [Goushith](https://github.com/goushithm22)*
