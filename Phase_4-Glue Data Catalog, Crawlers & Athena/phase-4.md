# Phase 4: AWS Glue Data Catalog & Query Results

This document captures the Phase 4 AWS Glue implementation, including the raw database, crawlers, tables, and the sample analytics queries and outputs.

## Phase 4 Data Catalog Database

The Glue Data Catalog contains a dedicated database for the raw retail data landing zone.

- Database name: `retailflow_raw`
- Catalog: `983457875389`
- Data location: `s3://phase4-glue-data-.../`

![Glue Database](./phase4-screenshots/retailflow_raw_database.png)

## Crawlers and Table Creation

Four Glue crawlers were created to automatically discover schemas and populate the Glue Data Catalog tables from the raw S3 data.

The crawlers are:

- `crawler_customers_mapping`
- `crawler_order_items_mapping`
- `crawler_orders_mapping`
- `crawler_products_mapping`

Each crawler is configured to scan the appropriate S3 prefix and create the matching table in the `retailflow_raw` database.

![Glue Crawlers](./phase4-screenshots/four_crawler_tables.png)

## Discovered Tables

The crawlers produced four tables in the `retailflow_raw` database:

- `customers`
- `order_items`
- `orders`
- `products`

These tables were discovered from the raw S3 objects and registered with the Glue Data Catalog.

![Glue Tables](./phase4-screenshots/four_tables.png)

## Table Details

### Customers Table
- File format: CSV
- Schema discovered from the raw customer dataset

![Customers Table](./phase4-screenshots/customers_table.png)

### Products Table
- File format: CSV
- Schema discovered from raw product metadata

![Products Table](./phase4-screenshots/products_table.png)

### Orders Table
- File format: JSON
- Schema discovered from raw order events
- Partitioned by date to support time-based query performance and incremental processing

![Orders Table](./phase4-screenshots/orders_table.png)

### Order Items Table
- File format: JSON
- Schema discovered from raw order line-item events
- Partitioned by date to support time-based query performance and incremental processing

![Order Items Table](./phase4-screenshots/order_items_table.png)

## Sample Queries and Results

Phase 4 includes sample SQL analytics executed against the Glue-managed tables.

### Query 1: Region-wise Order Distribution

This query calculates total orders by store region.

![Query 1 Region Distribution](./phase4-screenshots/query_1-Region-wise%20Order%20Distribution.png)

Result:

![Query 1 Result](./phase4-screenshots/query_1_result.png)

### Query 2: Top Customers by Number of Orders

This query identifies the highest-order customers.

![Query 2 Top Customers](./phase4-screenshots/query_2-Top%20Customers%20by%20Number%20of%20Orders.png)

Result:

![Query 2 Result](./phase4-screenshots/query_2_results.png)

### Query 3: Customers with Cancelled Orders

This query filters customers who have cancelled orders.

![Query 3 Cancelled Orders](./phase4-screenshots/query_3-Customers%20with%20Cancelled%20Orders.png)

Result:

![Query 3 Result](./phase4-screenshots/query_3_results.png)

## Summary

Phase 4 demonstrates a complete Glue data ingestion and discovery flow:

1. Raw datasets are stored in S3.
2. Glue crawlers scan the raw data and infer schema.
3. The Glue Data Catalog database `retailflow_raw` stores table metadata.
4. Query results validate that the discovered data is available for analytics.
