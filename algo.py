
import matplotlib.pyplot as plt
import numpy
import pandas

from mlxtend.frequent_patterns import (apriori, association_rules)
from mlxtend.preprocessing import TransactionEncoder

Imaginary_Store = pandas.read_csv('Imaginary_Store.csv')

# Convert the Sale Receipt data to the Item List format
ListItem = Imaginary_Store.groupby(['Customer'])['Item'].apply(list).values.tolist()

# Convert the Item List format to the Item Indicator format
te = TransactionEncoder()
te_ary = te.fit(ListItem).transform(ListItem)
ItemIndicator = pandas.DataFrame(te_ary, columns=te.columns_)
nCustomer, nProduct = ItemIndicator.shape

# Calculate the frequency table of number of customers per item
nCustomerPurchase = Imaginary_Store.groupby('Item').size()
freqTable = pandas.Series.sort_index(pandas.Series.value_counts(nCustomerPurchase))
print('Frequency of Number of Customers Purchase Item')
print(freqTable)

# Calculate the frequency table of number of items purchase
nItemPurchase = Imaginary_Store.groupby('Customer').size()
freqTable = pandas.Series.sort_index(pandas.Series.value_counts(nItemPurchase))
print('Frequency of Number of Items Purchase')
print(freqTable)

# Find the frequent itemsets
lowest_support = 10.0 / nCustomer
frequent_itemsets = apriori(ItemIndicator, min_support = lowest_support, max_len = 7, use_colnames = True)

# Discover the association rules
assoc_rules = association_rules(frequent_itemsets, metric = "confidence", min_threshold = 0.5)

print('=== Summary of Metrics Values ===')
print(assoc_rules[['consequent support','confidence','lift']].describe())

# Scatterplot of Support versus Confidence with Lift as color
plt.figure(figsize=(10,6), dpi = 200)
plt.scatter(assoc_rules['confidence'], assoc_rules['support'],
            c = assoc_rules['lift'], s = 5**assoc_rules['lift'])
plt.grid(True, axis = 'both')
plt.xlabel("Confidence")
plt.ylabel("Support")
plt.colorbar(boundaries = numpy.arange(0.0, 4.5, 0.5)).set_label('lift')
plt.show()

# Find the desired itemsets and association rules
frequent_itemsets = apriori(ItemIndicator, min_support = 0.1, max_len = 7, use_colnames = True)
assoc_rules = association_rules(frequent_itemsets, metric = "confidence", min_threshold = 0.8)

# Scatterplot of Support versus Confidence with Lift as color
plt.figure(figsize=(10,6), dpi = 200)
plt.scatter(assoc_rules['confidence'], assoc_rules['support'],
            c = assoc_rules['lift'], s = 10**assoc_rules['lift'])
plt.grid(True, axis = 'both')
plt.xlabel("Confidence")
plt.ylabel("Support")
plt.colorbar().set_label('lift')
plt.show()

# Show rules that have the 'CEREAL' consquent
Cereal_Consequent_Rule = assoc_rules[numpy.isin(assoc_rules["consequents"].values, {"Cereal"})]

# Show rules that have the 'Oranges' antecedent
antecedent = assoc_rules["antecedents"]
selectAntecedent = numpy.ones((assoc_rules.shape[0], 1), dtype=bool)

i = 0
for f in antecedent:
    selectAntecedent[i,0] = "Oranges" in f
    i = i + 1

Orange_Antecedent_Rule = assoc_rules[selectAntecedent]
