import pandas as pd

df = pd.read_csv('Riyadh_NDVI_Coords.csv')

def get_priority(ndvi):
    if ndvi < 0.1:
        return 'High'
    elif ndvi < 0.2:
        return 'Medium'
    else:
        return 'Low'

df['priority'] = df['nd'].apply(get_priority)

# حفظ مع ألوان
def color_priority(val):
    if val == 'High':
        return 'background-color: #ff4d4d'  # أحمر
    elif val == 'Medium':
        return 'background-color: #ffd700'  # أصفر
    else:
        return 'background-color: #90ee90'  # أخضر

styled = df.style.map(color_priority, subset=['priority'])
styled.to_excel('Riyadh_NDVI_Priority_Colored.xlsx', index=False)

print("DONNEE")