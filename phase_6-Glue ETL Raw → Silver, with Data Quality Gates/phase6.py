import sys

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.context import SparkContext
from pyspark.sql.functions import col

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# -------------------------
# READ FROM GLUE CATALOG
# -------------------------

customers_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="phase6_db",
    table_name="customers"
)

products_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="phase6_db",
    table_name="products"
)

orders_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="phase6_db",
    table_name="orders"
)

order_items_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="phase6_db",
    table_name="order_items"
)

# -------------------------
# CONVERT TO DATAFRAME
# -------------------------

customers_df = customers_dyf.toDF()
products_df = products_dyf.toDF()
orders_df = orders_dyf.toDF()
order_items_df = order_items_dyf.toDF()

# -------------------------
# NULL HANDLING
# -------------------------

customers_df = customers_df.fillna({
    "email": "UNKNOWN"
})

# -------------------------
# TYPE CASTING
# -------------------------

products_df = (
    products_df
    .withColumn(
        "unit_price",
        col("unit_price").cast("double")
    )
    .withColumn(
        "active_flag",
        col("active_flag").cast("int")
    )
)

order_items_df = (
    order_items_df
    .withColumn(
        "quantity",
        col("quantity").cast("int")
    )
    .withColumn(
        "unit_price",
        col("unit_price").cast("double")
    )
    .withColumn(
        "line_total",
        col("line_total").cast("double")
    )
)

# -------------------------
# DEDUPLICATION
# -------------------------

orders_df = orders_df.dropDuplicates(
    ["order_id"]
)

order_items_df = order_items_df.dropDuplicates()

# -------------------------
# REFERENTIAL INTEGRITY
# -------------------------

valid_products = products_df.select(
    "product_id"
)

good_order_items = order_items_df.join(
    valid_products,
    "product_id",
    "inner"
)

bad_order_items = order_items_df.join(
    valid_products,
    "product_id",
    "left_anti"
)

# -------------------------
# WRITE GOOD DATA
# -------------------------

customers_df.write \
    .mode("overwrite") \
    .parquet(
        "s3://dinesh-phase6/curated/customers/"
    )

products_df.write \
    .mode("overwrite") \
    .partitionBy("category") \
    .parquet(
        "s3://dinesh-phase6/curated/products/"
    )

orders_df.write \
    .mode("overwrite") \
    .partitionBy("store_region") \
    .parquet(
        "s3://dinesh-phase6/curated/orders/"
    )

good_order_items.write \
    .mode("overwrite") \
    .partitionBy("discount_code") \
    .parquet(
        "s3://dinesh-phase6/curated/order_items/"
    )

# -------------------------
# QUARANTINE
# -------------------------

bad_order_items.write \
    .mode("overwrite") \
    .parquet(
        "s3://dinesh-phase6/quarantine/order_items/"
    )

job.commit()