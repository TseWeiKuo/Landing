import csv
import numpy as np

l = np.full(20, 1)
print(l)

with open(r"C:\Users\agrawal-admin\Desktop\Sample_CSV.xlsx", 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(l)