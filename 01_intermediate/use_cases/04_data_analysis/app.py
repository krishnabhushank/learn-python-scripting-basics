import pandas as pd

# Read CSV file into a dataframe
df = pd.read_csv('data.csv')

# Display the first few rows of the dataframe
print(df.head())

# Accessing specific columns
column_names = ['Name', 'Age', 'City']
subset_df = df[column_names]
print(subset_df)

# Filtering rows based on a condition
filtered_df = df[df['Age'] > 30]
print(filtered_df)

# Sorting the dataframe by a column
sorted_df = df.sort_values('Age', ascending=False)
print(sorted_df)

# Adding a new column
df['Profession'] = ['Engineer', 'Teacher', 'Doctor', 'Lawyer', 'Artist']
print(df)

# Saving dataframe to a new CSV file
df.to_csv('new_data.csv', index=False)