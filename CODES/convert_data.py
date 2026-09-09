import pandas as pd
import json

df = pd.read_csv('Riyadh_NDVI_Priority.csv')

data = df[['latitude', 'longitude', 'nd', 'priority']].to_dict('records')

with open('data.js', 'w') as f:
    f.write('const data = ')
    f.write(json.dumps(data))
    f.write(';')

print("تم!")