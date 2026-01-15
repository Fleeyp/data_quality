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

# Print header with dataset information
print("=" * 80)
print("DATA QUALITY CHECK - ORDER ITEMS")
print("=" * 80)
print("\nDataset Statistics:")
print(f"  Total Rows: {len(df):,}")
print(f"  Total Columns: {len(df.columns)}")
print(f"  Columns: {', '.join(df.columns.tolist())}")

# Print summary statistics for numeric columns
print("\nNumeric Column Statistics:")
for col in ['price', 'freight_value']:
    if col in df.columns:
        print(f"  {col}:")
        print(f"    Min: {df[col].min():.2f}")
        print(f"    Max: {df[col].max():.2f}")
        print(f"    Mean: {df[col].mean():.2f}")
        print(f"    Median: {df[col].median():.2f}")
        print(f"    Null Count: {df[col].isnull().sum():,} ({df[col].isnull().sum()/len(df)*100:.2f}%)")

# Print overall validation result
print(f"\n{'=' * 80}")
print("VALIDATION SUMMARY")
print(f"{'=' * 80}")
print(f"Overall Success: {'✓ PASSED' if results['success'] else '✗ FAILED'}")
print(f"Total Expectations Evaluated: {len(results['results'])}")
passed = sum(1 for r in results['results'] if r['success'])
failed = len(results['results']) - passed
print(f"Passed: {passed} | Failed: {failed}")

# Print detailed results for each expectation
print(f"\n{'=' * 80}")
print("DETAILED EXPECTATION RESULTS")
print(f"{'=' * 80}")

for i, res in enumerate(results["results"], 1):
    expectation_type = res['expectation_config']['expectation_type']
    success = res['success']
    result_data = res.get('result', {})
    config = res.get('expectation_config', {})
    kwargs = config.get('kwargs', {})
    
    status = "✓ PASSED" if success else "✗ FAILED"
    
    print(f"\n[{i}] {expectation_type}")
    print(f"    Status: {status}")
    
    # Extract column name(s)
    if 'column' in kwargs:
        print(f"    Column: {kwargs['column']}")
    elif 'column_list' in kwargs:
        print(f"    Columns: {', '.join(kwargs['column_list'])}")
    
    # Print specific details based on expectation type
    if expectation_type == 'expect_column_values_to_not_be_null':
        unexpected_count = result_data.get('unexpected_count', 0)
        element_count = result_data.get('element_count', len(df))
        null_percentage = (unexpected_count / element_count * 100) if element_count > 0 else 0
        print(f"    Null Values Found: {unexpected_count:,} ({null_percentage:.2f}%)")
        print(f"    Non-null Values: {element_count - unexpected_count:,}")
        
    elif expectation_type == 'expect_column_values_to_be_between':
        min_val = kwargs.get('min_value', 'N/A')
        max_val = kwargs.get('max_value', 'N/A')
        mostly = kwargs.get('mostly', 1.0)
        unexpected_count = result_data.get('unexpected_count', 0)
        element_count = result_data.get('element_count', len(df))
        out_of_range_pct = (unexpected_count / element_count * 100) if element_count > 0 else 0
        
        print(f"    Expected Range: [{min_val}, {max_val}]")
        print(f"    Mostly Threshold: {mostly*100:.1f}%")
        print(f"    Values Out of Range: {unexpected_count:,} ({out_of_range_pct:.2f}%)")
        print(f"    Values In Range: {element_count - unexpected_count:,}")
        
        if unexpected_count > 0 and 'partial_unexpected_list' in result_data:
            unexpected_samples = result_data['partial_unexpected_list'][:5]
            print(f"    Sample Out-of-Range Values: {unexpected_samples}")
            if len(result_data['partial_unexpected_list']) > 5:
                print(f"    ... and {len(result_data['partial_unexpected_list']) - 5} more")
                
    elif expectation_type == 'expect_compound_columns_to_be_unique':
        unexpected_count = result_data.get('unexpected_count', 0)
        element_count = result_data.get('element_count', len(df))
        duplicate_pct = (unexpected_count / element_count * 100) if element_count > 0 else 0
        print(f"    Duplicate Rows Found: {unexpected_count:,} ({duplicate_pct:.2f}%)")
        print(f"    Unique Rows: {element_count - unexpected_count:,}")
        
        if unexpected_count > 0 and 'partial_unexpected_list' in result_data:
            duplicate_samples = result_data['partial_unexpected_list'][:3]
            print("    Sample Duplicate Combinations:")
            for dup in duplicate_samples:
                print(f"      {dup}")

print(f"\n{'=' * 80}")
print("END OF DATA QUALITY REPORT")
print(f"{'=' * 80}\n")