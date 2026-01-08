import pandas as pd
import great_expectations as ge
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://dadosfera_reader:dadosfera_pass@localhost:5432/olist_case"
)

query = """
SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    price,
    freight_value
FROM olist_raw.order_items
"""

df = pd.read_sql(query, engine)

ge_df = ge.from_pandas(df)

ge_df.expect_column_values_to_not_be_null("order_id")
ge_df.expect_column_values_to_not_be_null("product_id")
ge_df.expect_column_values_to_not_be_null("seller_id")

ge_df.expect_column_values_to_be_between("price", min_value=0, mostly=0.99)
ge_df.expect_column_values_to_be_between("freight_value", min_value=0, mostly=0.99)

ge_df.expect_compound_columns_to_be_unique(
    ["order_id", "order_item_id"]
)

results = ge_df.validate()

print("Data Quality Check - Order Items")
print(f"Success: {results['success']}")
print(f"Evaluated Expectations: {len(results['results'])}")
for res in results["results"]:
    print(
        f"Expectation: {res['expectation_config']['expectation_type']}, "
        f"Success: {res['success']}, "
        f"Details: {res.get('result', {})}"
    )