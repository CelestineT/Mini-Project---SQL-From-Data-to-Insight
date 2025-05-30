import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import FileLink
from scipy.stats import pearsonr

Brooklyn_property_sales_file_path = r'Data\Raw\Brooklyn_2019.csv'
Manhattan_property_sales_file_path = r'Data\Raw\Manhattan_2019.csv'
airbnb_file_path = r'Data\Raw\AB_NYC_2019.csv'

# Loading the Airbnb dataset
df_airbnb = pd.read_csv(airbnb_file_path, encoding='utf-8')

# Display the first 5 lines
df_Manhattan_Property_Sales = pd.read_csv(Manhattan_property_sales_file_path, encoding='utf-8')

# Loading the Brooklyn Property Sales dataset
df_Brooklyn_Property_Sales = pd.read_csv(Brooklyn_property_sales_file_path, encoding='utf-8')

# Display the first 5 lines
df_Brooklyn_Property_Sales = pd.read_csv(Brooklyn_property_sales_file_path, encoding='utf-8')

try:
    df_airbnb = pd.read_csv(airbnb_file_path)
except FileNotFoundError:
    print('Error: Airbnb file not found at specified location')
if 'price' in df_airbnb.columns:  # Note: dans Airbnb c'est 'price' (minuscule)
    # Nettoyage des prix (expression régulière corrigée)
    df_airbnb['price'] = df_airbnb['price'].replace('[^\d.]', '', regex=True).astype(float)

if df_airbnb is not None:
    if 'reviews_per_month' in df_airbnb.columns:
        df_airbnb = df_airbnb.assign(
            reviews_per_month=df_airbnb['reviews_per_month'].fillna(0),
            last_review=df_airbnb['last_review'].fillna(pd.NaT)
        )
    else:
        print("'reviews_per_month' column not found")

if df_airbnb is not None:
    if 'reviews_per_month' in df_airbnb.columns:
        df_airbnb['reviews_per_month'] = df_airbnb['reviews_per_month'].fillna(0)

# --- Handling missing values ---
if df_Manhattan_Property_Sales is not None:

    # Check column name (corrected from 'Columns' to 'columns')
    price_column = 'Sale Price' if 'Sale Price' in df_Manhattan_Property_Sales.columns else 'SALE PRICE'

    # Copy the DataFrame to avoid warnings
    df_clean = df_Manhattan_Property_Sales.copy()
    initial_rows = df_clean.shape[0]

    # 1. Delete rows with no sale price
    df_clean = df_clean.dropna(subset=[price_column])

    # 2. Delete rows with price = 0 (corrected syntax)
    df_clean = df_clean[df_clean[price_column] > 0]

    # 3. Optional area management (corrected quotes and indentation)
    if 'GROSS SQUARE FEET' in df_clean.columns:
        df_clean = df_clean.query('`GROSS SQUARE FEET` > 0')

    # Calculation of deleted lines (fixed f-string)
    deleted_rows = initial_rows - df_clean.shape[0]

    # Reassign the cleaned DataFrame
    df_Manhattan_Property_Sales = df_clean

    # --- Handling missing values ---
if df_Brooklyn_Property_Sales is not None:

    # Check column name (corrected from 'Columns' to 'columns')
    price_column = 'Sale Price' if 'Sale Price' in df_Brooklyn_Property_Sales.columns else 'SALE PRICE'

    # Copy the DataFrame to avoid warnings
    df_clean = df_Brooklyn_Property_Sales.copy()
    initial_rows = df_clean.shape[0]

    # 1. Delete rows with no sale price
    df_clean = df_clean.dropna(subset=[price_column])

    # 2. Delete rows with price = 0 (corrected syntax)
    df_clean = df_clean[df_clean[price_column] > 0]

    # 3. Optional area management (corrected quotes and indentation)
    if 'GROSS SQUARE FEET' in df_clean.columns:
        df_clean = df_clean.query('`GROSS SQUARE FEET` > 0')

    # Calculation of deleted lines (fixed f-string)
    deleted_rows = initial_rows - df_clean.shape[0]

    # Reassign the cleaned DataFrame
    df_Brooklyn_Property_Sales = df_clean
# --- Duplicate management ---
if df_airbnb is not None:
    initial_rows_airbnb = df_airbnb.shape[0]  # Ajout de [0] pour obtenir le nombre de lignes
    df_airbnb.drop_duplicates(inplace=True)

if df_Brooklyn_Property_Sales is not None:
    
    initial_rows_Brooklyn_Property_Sales = df_Brooklyn_Property_Sales.shape[0]  # Add [0] to obtain the number of lines
    df_Brooklyn_Property_Sales.drop_duplicates(inplace=True)


if df_Manhattan_Property_Sales is not None:
    initial_rows_Manhattan_Property_Sales = df_Manhattan_Property_Sales.shape[0]  # Add [0] to obtain the number of lines
    df_Manhattan_Property_Sales.drop_duplicates(inplace=True)

if df_Manhattan_Property_Sales is not None:
    # Important columns: SALE PRICE, SALE DATE, GROSS SQUARE FEET, LAND SQUARE FEET
    # SALE PRICE' and areas can be objects (strings) because of formatting ($, commas, spaces, NaN)
    # 'SALE DATE' is probably a string

    columns_to_numeric = ['SALE PRICE', 'GROSS SQUARE FEET', 'LAND SQUARE FEET'] # Adapt if other surface columns exist

    for col in columns_to_numeric:
        if col in df_Manhattan_Property_Sales.columns:
            # Clean up strings (remove $, ',', etc. and deal with empty spaces)
            df_Manhattan_Property_Sales[col] = df_Manhattan_Property_Sales[col].astype(str).str.replace(r"[$, -]", '', regex=True)
            # Convert to numeric (non-convertible values become NaN)
            df_Manhattan_Property_Sales[col] = pd.to_numeric(df_Manhattan_Property_Sales[col], errors='coerce')

    # Optional: Convert SALE DATE to datetime
    if 'SALE DATE' in df_Manhattan_Property_Sales.columns:
        df_Manhattan_Property_Sales['SALE DATE'] = pd.to_datetime(df_Manhattan_Property_Sales['SALE DATE'], errors='coerce')

# --- Correction of Brooklyn Property Sales data types ---
if df_Brooklyn_Property_Sales is not None:
    # Important columns: SALE PRICE, SALE DATE, GROSS SQUARE FEET, LAND SQUARE FEET
    # SALE PRICE' and areas can be objects (strings) because of formatting ($, commas, spaces, NaN)
    # 'SALE DATE' is probably a string

    columns_to_numeric = ['SALE PRICE', 'GROSS SQUARE FEET', 'LAND SQUARE FEET'] # Adapt if other surface columns exist

    for col in columns_to_numeric:
        if col in df_Brooklyn_Property_Sales.columns:
            # Clean up strings (remove $, ',', etc. and deal with empty spaces)
            df_Brooklyn_Property_Sales[col] = df_Brooklyn_Property_Sales[col].astype(str).str.replace(r"[$, -]", '', regex=True)
            # Convert to numeric (non-convertible values become NaN)
            df_Brooklyn_Property_Sales[col] = pd.to_numeric(df_Brooklyn_Property_Sales[col], errors='coerce')
            
# Optional: Convert SALE DATE to datetime
if 'SALE DATE' in df_Brooklyn_Property_Sales.columns:
    df_Brooklyn_Property_Sales['SALE DATE'] = pd.to_datetime(df_Brooklyn_Property_Sales['SALE DATE'], errors='coerce')

    # Convert 'SALE DATE' to datetime
    if 'SALE DATE' in df_Manhattan_Property_Sales.columns:
        df_Manhattan_Property_Sales['SALE DATE'] = pd.to_datetime(df_Manhattan_Property_Sales['SALE DATE'], errors='coerce')

    # After conversion, manage missing values (NaNs)
    if 'SALE PRICE' in df_Manhattan_Property_Sales.columns:
        # 1. Delete rows where SALE PRICE is NaN
        df_Manhattan_Property_Sales.dropna(subset=['SALE PRICE'], inplace=True)
        
        # 2. Keep only rows with price > 0
        df_Manhattan_Property_Sales = df_Manhattan_Property_Sales[df_Manhattan_Property_Sales['SALE PRICE'] > 0]

    # Surface management
    if 'GROSS SQUARE FEET' in df_Manhattan_Property_Sales.columns:
        df_Manhattan_Property_Sales['GROSS SQUARE FEET'].fillna(0, inplace=True)

    # Convert 'SALE DATE' to datetime
    if 'SALE DATE' in df_Brooklyn_Property_Sales.columns:
        df_Brooklyn_Property_Sales['SALE DATE'] = pd.to_datetime(df_Brooklyn_Property_Sales['SALE DATE'], errors='coerce')

    # After conversion, manage missing values (NaNs)
    if 'SALE PRICE' in df_Brooklyn_Property_Sales.columns:
        # 1. Delete rows where SALE PRICE is NaN
        df_Brooklyn_Property_Sales.dropna(subset=['SALE PRICE'], inplace=True)
        
        # 2. Keep only rows with price > 0
        df_Brooklyn_Property_Sales = df_Brooklyn_Property_Sales[df_Brooklyn_Property_Sales['SALE PRICE'] > 0]

    # Surface management
    if 'GROSS SQUARE FEET' in df_Brooklyn_Property_Sales.columns:
        df_BrooklynProperty_Sales['GROSS SQUARE FEET'].fillna(0, inplace=True)

# --- Dealing with inconsistencies and standardisation ---
if df_airbnb is not None:
 print("\n--- Standardisation Airbnb ---")
    # Standardise the names of neighbourhoods and boroughs (“neighbourhood_group”) [3]
    # Convert to lower case and remove leading/leading white space
 df_airbnb['neighbourhood'] = df_airbnb['neighbourhood'].str.strip().str.lower()
 df_airbnb['neighbourhood_group'] = df_airbnb['neighbourhood_group'].str.strip().str.lower()

    # You might want to check the unique values to identify typos or variations
    # print(df_airbnb[“neighbourhood”].unique())
    # print(df_airbnb[“neighbourhood_group”].unique())
    # Use .replace() if manual corrections are required [my previous response]

# --- Standardisation Manhattan Property Sales ---
if df_Manhattan_Property_Sales is not None:
    print("\n--- Standardisation Manhattan Property Sales ---")
    
    # Checking column names
    neighborhood_col = 'NEIGHBORHOOD' if 'NEIGHBORHOOD' in df_Manhattan_Property_Sales.columns else 'Neighborhood'
    borough_col = 'BOROUGH' if 'BOROUGH' in df_Manhattan_Property_Sales.columns else 'Borough'
    
    # Standardisation of district names
    if neighborhood_col in df_Manhattan_Property_Sales.columns:
        df_Manhattan_Property_Sales[neighborhood_col] = df_Manhattan_Property_Sales[neighborhood_col].str.strip().str.lower()
    
    # Standardisation of borough names
    if borough_col in df_Manhattan_Property_Sales.columns:
        # Conversion to string and cleaning
        df_Manhattan_Property_Sales[borough_col] = df_Manhattan_Property_Sales[borough_col].astype(str).str.strip().str.lower()
        
        # Mapping numeric codes to names
        borough_mapping = {
            '1': 'manhattan',
            '2': 'bronx', 
            '3': 'brooklyn',
            '4': 'queens',
            '5': 'staten island'
        }
        df_Manhattan_Property_Sales[borough_col] = df_Manhattan_Property_Sales[borough_col].replace(borough_mapping)
    
    # Display of single values for verification
    print("\nSingle values after standardisation:")
    if neighborhood_col in df_Manhattan_Property_Sales.columns:
        print("Neighbourhoods:", df_Manhattan_Property_Sales[neighborhood_col].unique()[:10])  # Displays the top 10
    if borough_col in df_Manhattan_Property_Sales.columns:
        print("Boroughs:", df_Manhattan_Property_Sales[borough_col].unique())

# --- Standardisation Brooklyn Property Sales ---
if df_Brooklyn_Property_Sales is not None:
    print("\n--- Standardisation Brooklyn Property Sales ---")
    
    # Checking column names
    neighborhood_col = 'NEIGHBORHOOD' if 'NEIGHBORHOOD' in df_Brooklyn_Property_Sales.columns else 'Neighborhood'
    borough_col = 'BOROUGH' if 'BOROUGH' in df_Brooklyn_Property_Sales.columns else 'Borough'
    
    # Standardisation des noms de quartiers
    if neighborhood_col in df_Brooklyn_Property_Sales.columns:
        df_Brooklyn_Property_Sales[neighborhood_col] = df_Brooklyn_Property_Sales[neighborhood_col].str.strip().str.lower()
    
    # Standardisation of district names
    if borough_col in df_Brooklyn_Property_Sales.columns:
        # Conversion to string and cleaning
        df_Brooklyn_Property_Sales[borough_col] = df_Brooklyn_Property_Sales[borough_col].astype(str).str.strip().str.lower()
        
        # Mapping numeric codes to names
        borough_mapping = {
            '1': 'manhattan',
            '2': 'bronx', 
            '3': 'brooklyn',
            '4': 'queens',
            '5': 'staten island'
        }
        df_Brooklyn_Property_Sales[borough_col] = df_Brooklyn_Property_Sales[borough_col].replace(borough_mapping)
    
    # Display of single values for verification
    print("\nSingle values after standardisation:")
    if neighborhood_col in df_Brooklyn_Property_Sales.columns:
        print("Neighbourhoods:", df_Brooklyn_Property_Sales[neighborhood_col].unique()[:10])  # Display the top 10
    if borough_col in df_Brooklyn_Property_Sales.columns:
        print("Boroughs:", df_Brooklyn_Property_Sales[borough_col].unique())
    
    # --- Identifying and managing outliers ---
# Outliers are common in prices (Airbnb and sales) and surfaces. [3, 4, 6, 7]
# The approach (remove, transform, or leave) depends on the analysis.
# For ROI calculations, extreme sale or rental prices can distort averages. [6, 7]

if df_airbnb is not None:
 print("\n--- Analysis of Airbnb outliers ---")
    # Analyse 'price
    # You could use a boxplot to visualise (requires matplotlib/seaborn) [my previous response]
    # import matplotlib.pyplot as plt
    # import seaborn as sns
    # sns.boxplot(x=df_airbnb[“price”])
    # plt.show()

    # Identify extreme values (e.g. price > 10000 or very low <= 10)
    # print(df_airbnb[df_airbnb[“price”] > 10000].shape)
    # print(df_airbnb[df_airbnb[“price”] <= 10].shape)

    # Decision: Remove prices considered unrealistic for a standard analysis
 df_airbnb = df_airbnb[(df_airbnb['price'] > 10) & (df_airbnb['price'] < 10000)] # Example of thresholds, to be adjusted

# --- Final preparation ---
# Rename columns if necessary for clarity or SQL compatibility
if df_airbnb is not None:
 df_airbnb.rename(columns={'neighbourhood_group': 'borough'}, inplace=True) # Potentially align with other dataset name [4]

if df_Brooklyn_Property_Sales is not None:
    df_Brooklyn_Property_Sales.rename(columns={'BOROUGH': 'borough', 'NEIGHBORHOOD': 'neighbourhood'}, inplace=True) # Aligner potentiellement les noms [3]

# Select only the columns needed for analysis and ROI calculation
if df_airbnb is not None:
    airbnb_cols_for_analysis = [
        'id', 
        'name', 
        'host_id', 
        'borough', 
        'neighbourhood', 
        'latitude', 
        'longitude',
        'room_type', 
        'price', 
        'minimum_nights', 
        'number_of_reviews',
        'reviews_per_month', 
        'calculated_host_listings_count', 
        'availability_365'
    ]
    df_airbnb_cleaned = df_airbnb[airbnb_cols_for_analysis]

# Creating download links
if 'df_airbnb_cleaned' in locals():
    df_airbnb_cleaned.to_csv("2019_airbnb_cleaned.csv", index=False)
    display(FileLink("airbnb_cleaned.csv", result_html_prefix="Télécharger Airbnb: "))

if 'df_Manhattan_Property_Sales' in locals():
    df_Manhattan_Property_Sales.to_csv("2019_manhattan_properties_cleaned.csv", index=False)
    display(FileLink("manhattan_properties_cleaned.csv", result_html_prefix="Télécharger Manhattan: "))

if 'df_Brooklyn_Property_Sales' in locals():
    df_Brooklyn_Property_Sales.to_csv("2019_brooklyn_properties_cleaned.csv", index=False)
    display(FileLink("brooklyn_properties_cleaned.csv", result_html_prefix="Télécharger Brooklyn: "))

clean_airbnb_file_path = r'Data\Clean\2019_airbnb_cleaned.csv'
clean_manhattan_file_path = r'Data\Clean\2019_manhattan_properties_cleaned.csv'
clean_brooklyn_file_path = r'Data\Clean\2019_brooklyn_properties_cleaned.csv'
df = pd.DataFrame()
manhattan_df = pd.DataFrame()
brooklyn_df = pd.DataFrame()

def inicialize():
    global df 
    df = pd.read_csv(clean_airbnb_file_path)
    global manhattan_df
    manhattan_df = pd.read_csv(clean_manhattan_file_path)
    global brooklyn_df
    brooklyn_df = pd.read_csv(clean_brooklyn_file_path)

def get_z_prices(dataframe):
    analysis_df = dataframe[['id', 'borough','neighbourhood', 'host_id', 'price','availability_365']].copy()
    return analysis_df

def get_borough_name(value):
    if isinstance(value, str) and not value.isdigit():
        return value.lower()
    
    borough_mapping = {
        1: 'manhattan',
        2: 'bronx', 
        3: 'brooklyn',
        4: 'queens',
        5: 'staten island'
    }
    
    try:
        return borough_mapping[int(value)]
    except (ValueError, KeyError):
        return None

def fill_column_with_average(dataframe,column_name):
    grp = dataframe.groupby('Neighborhood')[column_name].mean()
    # create a condition to only update rows with 0 or NaN
    mask = (dataframe[column_name] == 0) | (dataframe[column_name].isna())
    #find the values and change them to map the average
    dataframe.loc[mask, column_name] = dataframe.loc[mask, 'Neighborhood'].map(grp)
    return dataframe

def get_clean_df(dataframe):
    dataframe = dataframe[['Sale Date','Borough','Neighborhood','Residential Units', 'Gross Square Feet','Sale Price']].copy()
    dataframe['Borough'] = dataframe['Borough'].apply(get_borough_name)
    dataframe = dataframe.loc[dataframe['Sale Price'] != 0]
    dataframe['Sale Price'].dropna()
    return dataframe

def get_clean_new_york_df():
    new_york_df = pd.concat([get_clean_df(manhattan_df),get_clean_df(brooklyn_df)])
    new_york_df = fill_column_with_average(new_york_df,'Gross Square Feet')
    new_york_df = fill_column_with_average(new_york_df,'Residential Units')
    return new_york_df

def main():
    inicialize()
    final_df = get_z_prices(df)
    final_df.to_csv('NYC_Airbnb_2019.csv')
    new_york_2019_df = get_clean_new_york_df()
    new_york_2019_df.to_csv('NYC_Housing_2019.csv')

main()