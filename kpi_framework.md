# KPI Framework — Amman Digital Market

Define 5 KPIs for the Amman Digital Market. At least 2 must be time-based and 1 must be cohort-based.

---

## KPI 1

- **Name:** Monthly Revenue Trend (Time-based)
- **Definition:** The total revenue generated from sales each month to track growth and seasonality.
- **Formula:** $$\sum (\text{Quantity} \times \text{Unit Price}) \text{ grouped by Month}$$
- **Data Source (tables/columns):** `order_items` (quantity, unit_price), `orders` (order_date)
- **Baseline Value:** Approximately $5,100 (Latest peak in June 2025)
- **Interpretation:** Shows a significant upward spike recently, indicating strong market growth or successful recent campaigns.

---

## KPI 2

- **Name:** Revenue by City (Segment-based)
- **Definition:** Total sales distribution across different cities in Jordan to identify key regional markets.
- **Formula:** $$\sum (\text{Total Price}) \text{ grouped by City}$$
- **Data Source (tables/columns):** `customers` (city), `order_items` (quantity, unit_price)
- **Baseline Value:** Amman is the leader with over $9,000 in total revenue.
- **Interpretation:** Amman is the primary market, followed by Irbid. This helps in allocating marketing budgets geographically.

---

## KPI 3

- **Name:** Average Order Value (AOV) by Category
- **Definition:** The average amount spent by a customer per order within specific product categories.
- **Formula:** $$\frac{\text{Total Category Revenue}}{\text{Total Number of Orders in Category}}$$
- **Data Source (tables/columns):** `products` (category), `order_items` (quantity, unit_price)
- **Baseline Value:** Books category has the highest AOV at approximately $70.
- **Interpretation:** High AOV in "Books" suggests customers tend to buy premium items or larger bundles in this category.

---

## KPI 4

- **Name:** Weekly Order Volume (Time-based)
- **Definition:** Monitoring the number of orders processed every week to evaluate operational load.
- **Formula:** Count of `order_id` grouped by Week.
- **Data Source (tables/columns):** `orders` (order_id, order_date)
- **Baseline Value:** Peaked at approximately 19 orders per week recently.
- **Interpretation:** Fluctuations show stable operations with a recent massive surge, requiring higher logistics readiness.

---

## KPI 5

- **Name:** Customer Retention Rate (Cohort-based)
- **Definition:** The percentage of customers who have made more than one purchase, indicating loyalty.
- **Formula:** $$\left( \frac{\text{Customers with >1 Order}}{\text{Total Customers}} \right) \times 100$$
- **Data Source (tables/columns):** `orders` (customer_id)
- **Baseline Value:** 94.0%
- **Interpretation:** An extremely high retention rate indicates exceptional customer loyalty and satisfaction with the Amman Digital Market.