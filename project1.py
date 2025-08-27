import pandas as pd
import glob

## Read and combine all CSVs in the folder
files = glob.glob(r"C:/Users/ashut/Downloads/projects/*.csv")
combined_df = pd.concat((pd.read_csv(Female) for Female in files), ignore_index=True)

# print(combined_df.head())

## Select only float columns
float_df = combined_df.select_dtypes(include='float')

## Select only object columns
string_df = combined_df.select_dtypes(include='object')

## Show info
string_df.info()


## we dont have any missing data 

print("\n1. MISSING DATA SUMMARY FOR STRING/OBJECT COLUMNS:")
print("-" * 50)
missing_counts = string_df.isnull().sum()
missing_percentages = (string_df.isnull().sum() / len(string_df)) * 100

missing_summary = pd.DataFrame({
    'Column': string_df.columns,
    'Missing_Count': missing_counts,
    'Missing_Percentage': missing_percentages,
    'Non_Missing_Count': len(string_df) - missing_counts
})
