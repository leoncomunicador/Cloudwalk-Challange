import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

df1 = pd.read_csv('files/checkout_1.csv')
df2 = pd.read_csv('files/checkout_2.csv')

print("Dados Checkout 1:")
print(df1.head())

print("Dados Checkout 2:")
print(df2.head())

print("Informações estatísticas do Checkout 1:")
print(df1.describe())

print("Informações estatísticas do Checkout 2:")
print(df2.describe())

print("Correlação do Checkout 1:")
print(df1.drop('time', axis=1).astype(float).corr())

print("Correlação do Checkout 2:")
print(df2.drop('time', axis=1).astype(float).corr())

plt.figure(figsize=(12, 6))
sns.lineplot(data=df1, x='time', y='today', label='Today')
sns.lineplot(data=df1, x='time', y='yesterday', label='Yesterday')
sns.lineplot(data=df1, x='time', y='same_day_last_week',
             label='Same Day Last Week')
plt.title('Comparação de vendas por hora (Checkout 1)')
plt.xlabel('Hora')
plt.ylabel('Vendas')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=df2, x='time', y='today', label='Today')
sns.lineplot(data=df2, x='time', y='yesterday', label='Yesterday')
sns.lineplot(data=df2, x='time', y='same_day_last_week',
             label='Same Day Last Week')
plt.title('Comparação de vendas por hora (Checkout 2)')
plt.xlabel('Hora')
plt.ylabel('Vendas')
plt.legend()
plt.show()

conn = sqlite3.connect('checkout_data.db')
df1.to_sql('checkout_1', conn)
df2.to_sql('checkout_2', conn)

query = "SELECT * FROM checkout_1"
checkout_1_data = pd.read_sql(query, conn)
print("Dados do Checkout 1 (consulta SQL):")
print(checkout_1_data)

query = "SELECT * FROM checkout_2"
checkout_2_data = pd.read_sql(query, conn)
print("Dados do Checkout 2 (consulta SQL):")
print(checkout_2_data)
