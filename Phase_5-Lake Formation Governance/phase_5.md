# Phase 5: Lake Formation and Analytics Permissions

This document summarizes the Phase 5 AWS Lake Formation setup, including resource registration, LF tags, user roles, permissions, and Athena query access.

## Lake Formation Resource Registration

The raw data lake resources are registered in AWS Lake Formation to manage access centrally.

- Registered database: `retailflow_raw`
- Registered tables from the raw data catalog

![Registered Lake Formation Tables](./phase5-screenshots/retailflow_raw_tables_in_lake_formation.png)

![Registering Data Lake Location](./phase5-screenshots/resgistering_data_lake_location.png)

## Lake Formation Tags

Lake Formation tags are used to classify data assets and drive fine-grained access control.

- `order_table_tags` are applied to the orders table
- The `customers` table was updated to use a column-level tag on the `email` field with `datasensitivity=PII` instead of a broader table-level tag like `confidential`
- Tags are updated and propagated for consistent permissions

![LF Tags](./phase5-screenshots/LF-tags.png)

## orders table: 
![Order Table Tags](./phase5-screenshots/order_table_tags.png)

## customers table:
![Updated LF Tags](./phase5-screenshots/updated_LF_tags.png)

## IAM Users and Roles

Phase 5 includes distinct user identities for analytics and engineering personas.

- Data Engineer user
- Data Analyst user
- Administrative role with privileged Lake Formation and Glue access

![Data Engineer User Created](./phase5-screenshots/DataEngineer_user_created.png)

![Data Analyst User Created](./phase5-screenshots/DataAnalyst_user_created.png)

![Administrative Role and Tasks](./phase5-screenshots/Administrative_role_and_tasks.png)

## Data Permissions

Lake Formation permissions are configured to grant the correct access level to each persona.

- Analysts receive read/query permissions on curated and consumption tables
- Engineers receive broader access for ingestion, transformation, and metadata management

![Data Permissions](./phase5-screenshots/Data_permissions.png)

## Athena Query Validation

Athena queries are executed against the Lake Formation-managed tables to validate access and data readability.

In this validation, I am logged in as the Data Analyst user. The Data Analyst user is intentionally restricted from viewing the sensitive `email` column because the Lake Formation tag `datasensitivity=PII` is not granted to that persona. This demonstrates fine-grained column-level governance, where the analyst can query permitted data but cannot access personally identifiable information.

![Data Analyst Athena Query](./phase5-screenshots/DataAnalyst_athena_query.png)

![Data Analyst Athena Query Result](./phase5-screenshots/DataAnalyst_atehna_query_result.png)

## Summary

Phase 5 confirms the Lake Formation governance layer is in place with:

1. Registered raw data locations and tables
2. Lake Formation tags for classification
3. User identities and roles for Data Engineer, Data Analyst, and Admin
4. Permission enforcement for governed data access
5. Athena query validation against governed resources
