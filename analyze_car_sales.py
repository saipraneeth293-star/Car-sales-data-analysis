# analyze_car_sales.py
# Car Sales Data Visualization — Clean and Robust Version

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sys

# -------------------------------
# Step 1: Load the dataset safely
# -------------------------------
try:
    data = pd.read_csv("car_sales.csv")
    print("✅ Dataset loaded successfully!\n")
except FileNotFoundError:
    print("❌ Error: The file 'car_sales.csv' was not found in this folder.")
    print("Please make sure it’s in the same directory as this script.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    print("❌ Error: The dataset file is empty.")
    sys.exit(1)
except pd.errors.ParserError as e:
    print(f"❌ Error reading CSV file: {e}")
    sys.exit(1)

# -------------------------------
# Step 2: Validate required columns
# -------------------------------
required_columns = ['Model', 'Sales_in_thousands']

for col in required_columns:
    if col not in data.columns:
        print(f"❌ Missing required column: '{col}' in dataset.")
        print("👉 Please check column names in the CSV file.")
        print(f"Available columns: {list(data.columns)}")
        sys.exit(1)

# -------------------------------
# Step 3: Clean and prepare data
# -------------------------------
try:
    # Convert sales data to numeric
    data['Sales_in_thousands'] = pd.to_numeric(data['Sales_in_thousands'], errors='coerce')
    data = data.dropna(subset=['Sales_in_thousands'])

    # Group total sales by model
    model_sales = (
        data.groupby('Model')['Sales_in_thousands']
        .sum()
        .sort_values(ascending=False)
    )

    if model_sales.empty:
        raise ValueError("Sales data appears empty after grouping.")

except ValueError as ve:
    print(f"❌ ValueError: {ve}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error while preparing data: {e}")
    sys.exit(1)

# -------------------------------
# Step 4: Display sample data
# -------------------------------
print("🔍 Data Preview:")
print(data[['Manufacturer', 'Model', 'Sales_in_thousands']].head(), "\n")

# -------------------------------
# Step 5: Matplotlib Visualizations
# -------------------------------
try:
    # --- Bar Chart ---
    plt.figure(figsize=(12, 6))
    model_sales.plot(kind='bar', color='skyblue')
    plt.title('Total Sales (in thousands) by Car Model')
    plt.xlabel('Car Model')
    plt.ylabel('Total Sales (in thousands)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # --- Pie Chart ---
    top_models = model_sales.head(10)
    plt.figure(figsize=(8, 8))
    plt.pie(top_models, labels=top_models.index, autopct='%1.1f%%', startangle=140)
    plt.title('Sales Distribution Among Top 10 Car Models')
    plt.show()

except Exception as e:
    print(f"⚠️ Plotting Error: {e}")

# -------------------------------
# Step 6: Interactive Plotly Chart
# -------------------------------
try:
    fig = px.bar(
        data_frame=model_sales.reset_index(),
        x='Model',
        y='Sales_in_thousands',
        title='Total Sales (in thousands) by Car Model (Interactive)',
        color='Sales_in_thousands',
        color_continuous_scale='Blues'
    )
    fig.show()

except Exception as e:
    print(f"⚠️ Plotly Error: {e}")

print("\n✅ Analysis completed successfully!")
