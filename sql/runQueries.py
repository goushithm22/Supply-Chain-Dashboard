import sqlite3
import pandas as pd

conn = sqlite3.connect("../data/supplychain.db")

pd.read_csv("../data/suppliers.csv").to_sql("suppliers",  conn, if_exists="replace", index=False)
pd.read_csv("../data/products.csv").to_sql("products",   conn, if_exists="replace", index=False)
pd.read_csv("../data/orders.csv").to_sql("orders",     conn, if_exists="replace", index=False)
pd.read_csv("../data/shipments.csv").to_sql("shipments",  conn, if_exists="replace", index=False)


queries = {
  
    "Q1 - To find total revenue, total cost, total profit": """
    SELECT
      SUM(revenue) as totalRevenue,
      SUM(cost) as totalCost,
      SUM(profit) as totalProfit, 
      ROUND(SUM(profit) * 100.00 / SUM(revenue), 2) as totalProfitMargin
    FROM orders
    WHERE status = 'Completed'
    """,
    
    
    "Q2 - Revenue by Product Category": """
    SELECT
        p.category,
        COUNT(o.order_id) AS totalOrders,
        SUM(o.revenue)    AS totalRevenue,
        SUM(o.profit)     AS totalProfit
    FROM orders o
    JOIN products p ON o.product_id = p.ProductId
    WHERE o.status = 'Completed'
    GROUP BY p.category
    ORDER BY totalRevenue DESC
    """,
    
    "Q3 - Top 5 Products By Profit": """
    SELECT
        p.productName,
        SUM(o.revenue) as totalRevenue,
        SUM(o.profit) as totalProfit,
        SUM(o.quantity) as unitsSold
    FROM orders o
    JOIN products p ON o.productId = p.productID
    WHERE o.status = 'Completed' 
    GROUP BY p.productName
    ORDER BY totalProfit DESC
    LIMIT 5 
        
    """,
    
    
    "Q4 — Monthly Revenue Trend": """
        SELECT
            strftime('%Y-%m', orderDate) AS yearMonth,
            COUNT(order_id)              AS totalOrders,
            SUM(revenue)                 AS monthlyRevenue,
            SUM(profit)                  AS monthlyProfit
        FROM orders
        WHERE status = 'Completed'
        GROUP BY yearMonth
        ORDER BY yearMonth ASC
    """,

    "Q5 — On-Time vs Late Deliveries": """
        SELECT
            CASE WHEN s.isLate = 1 THEN 'Late' ELSE 'On Time' END AS deliveryStatus,
            COUNT(*) AS totalShipments,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM shipments), 2) AS pct
        FROM shipments s
        GROUP BY deliveryStatus
    """,

    "Q6 — Supplier Performance Scorecard": """
        SELECT
            sup.SuppliersName,
            sup.SupplierCountry,
            sup.SupplierRating,
            COUNT(o.order_id)                                     AS totalOrders,
            SUM(o.revenue)                                        AS totalRevenue,
            SUM(o.profit)                                         AS totalProfit,
            ROUND(AVG(s.actualDays), 1)                           AS avgDeliveryDays,
            SUM(CASE WHEN s.isLate = 1 THEN 1 ELSE 0 END)        AS lateDeliveries
        FROM orders o
        JOIN products p    ON o.product_id  = p.ProductId
        JOIN suppliers sup ON p.SupplierId  = sup.SuppliersId
        JOIN shipments s   ON o.order_id    = s.order_id
        WHERE o.status = 'Completed'
        GROUP BY sup.SuppliersName, sup.SupplierCountry, sup.SupplierRating
        ORDER BY totalProfit DESC
    """,

    "Q7 — Order Status by Region": """
        SELECT
            region,
            status,
            COUNT(order_id) AS totalOrders,
            SUM(revenue)    AS totalRevenue
        FROM orders
        GROUP BY region, status
        ORDER BY region, totalOrders DESC
    """,

    "Q8 — Profit Margin by Product": """
        SELECT
            p.ProductName,
            p.UnitCost,
            p.UnitPrice,
            p.UnitPrice - p.UnitCost AS marginPerUnit,
            ROUND((p.UnitPrice - p.UnitCost) * 100.0 / p.UnitPrice, 2) AS marginPct
        FROM products p
        ORDER BY marginPct DESC
    """,

    "Q9 — Running Total of Revenue (Window Function)": """
        SELECT
            strftime('%Y-%m', orderDate) AS yearMonth,
            SUM(revenue)                 AS monthlyRevenue,
            SUM(SUM(revenue)) OVER (
                ORDER BY strftime('%Y-%m', orderDate)
            ) AS runningTotal
        FROM orders
        WHERE status = 'Completed'
        GROUP BY yearMonth
        ORDER BY yearMonth
    """,

    "Q10 — Late Orders with Full Details": """
        SELECT
            o.order_id,
            p.ProductName,
            sup.SuppliersName,
            o.orderDate,
            s.shipDate,
            s.promisedDays,
            s.actualDays,
            s.actualDays - s.promisedDays AS daysLate,
            s.carrier
        FROM orders o
        JOIN products p    ON o.product_id  = p.ProductId
        JOIN suppliers sup ON p.SupplierId  = sup.SuppliersId
        JOIN shipments s   ON o.order_id    = s.order_id
        WHERE s.isLate = 1
        ORDER BY daysLate DESC
    """
    
}


pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

for queryName, sql in queries.items():
    print(f"\n{'='*60}")
    print(f"  {queryName}")
    print(f"{'='*60}")
    try:
        result = pd.read_sql_query(sql, conn)
        print(result.to_string(index=False))
    except Exception as e:
        print(f"  ERROR: {e}")

conn.close()