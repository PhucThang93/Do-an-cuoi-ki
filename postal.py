import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import numpy as np
from sklearn.linear_model import LinearRegression

postal_codes = {
    "Berlin": "10115-14199",
    "Leipzig": "04103-04357",
    "Munster": "48143-48167",
    "Celle": "29221-29229",
    "Duisburg": "47051-47279",
    "Krefeld": "47798-47839",
    "Augsburg": "86150-86199",
    "Hanover": "30159-30669",
    "Bremen": "28195-28779",
    "Bochum": "44787-44894",
    "Hamburg": "20095-21149, 22041",
    "Moers": "47441-47447",
    "Iserlohn": "58636-58644",
    "Weimar": "99423-99427",
    "Erlangen": "91052-91058",
    "Regensburg": "93047-93059",
    "Garbsen": "30823-30827",
    "Menden": "58706-58710",
    "Wetzlar": "35578-35586",
    "Nuremberg": "90402-90491",
    "Dortmund": "44135-44388",
    "Schwerin": "19053-19061",
    "Herford": "32049-32052",
    "Munich": "80331-81929",
    "Euskirchen": "53879-53881",
    "Frankfurt": "60306-60599, 65929-65936",
    "Trier": "54290-54296",
    "Stuttgart": "70173-70629",
    "Reutlingen": "72760-72770",
    "Rostock": "18055-18147",
    "Aachen": "52062-52080",
    "Dormagen": "41539-41542",
    "Mainz": "55116-55131",
    "Gronau": "48599",
    "Solingen": "42651-42719",
    "Cologne": "50667-51149",
    "Bottrop": "46236-46244",
    "Ulm": "89073-89081",
    "Castrop-Rauxel": "44575-44581",
    "Bonn": "53111-53229",
    "Herne": "44623-44653",
    "Oberhausen": "46045-46149",
    "Stolberg": "52222-52224",
    "Jena": "07743-07751",
    "Hildesheim": "31134-31141",
    "Wilhelmshaven": "26382-26389",
    "Kassel": "34117-34134",
    "Sindelfingen": "71063-71069",
    "Essen": "45127-45359",
    "Bielefeld": "33602-33739",
    "Langenhagen": "30851-30855",
    "Offenburg": "77652-77656",
    "Hamm": "59063-59077",
    "Remscheid": "42853-42899",
    "Brandenburg": "14770-14776",
    "Halle": "06108-06132",
    "Dresden": "01067-01328",
    "Aschaffenburg": "63739-63743",
    "Neuwied": "56564-56567",
    "Oldenburg": "26121-26135",
    "Ludwigshafen am Rhein": "67059-67071",
    "Troisdorf": "53840-53844",
    "Langen": "63225",
    "Pforzheim": "75172-75181",
    "Siegen": "57072-57080",
    "Gera": "07545-07557",
    "Potsdam": "14467-14482",
    "Neunkirchen": "66538-66540",
    "Aalen": "73430-73434",
    "Greifswald": "17489-17493",
    "Wiesbaden": "65183-65207",
    "Magdeburg": "39104-39130",
    "Erftstadt": "50374",
    "Lippstadt": "59555-59558",
    "Pulheim": "50259",
    "Offenbach": "63065-63075",
    "Kiel": "24103-24159",
    "Kaiserslautern": "67655-67663",
    "Rosenheim": "83022-83026",
    "Worms": "67547-67551",
    "Darmstadt": "64283-64297",
    "Minden": "32423-32429",
    "Herten": "45699-45701",
    "Ratingen": "40878-40885",
    "Paderborn": "33098-33106",
    "Wuppertal": "42103-42399",
    "Bayreuth": "95444-95448",
    "Ludwigsfelde": "14974",
    "Delmenhorst": "27749-27755",
    "Emden": "26721-26725",
    "Karlsruhe": "76131-76229",
    "Grevenbroich": "41515-41517",
    "Cottbus": "03042-03055",
    "Rheine": "48429-48432",
    "Heidelberg": "69115-69126",
    "Ingolstadt": "85049-85057",
    "Stralsund": "18435-18439",
    "Gelsenkirchen": "45879-45899",
    "Dorsten": "46282-46286",
    "Norderstedt": "22844-22851",
    "Chemnitz": "09111-09247",
    "Koblenz": "56068-56077",
    "Hagen": "58089-58135",
    "Heilbronn": "74072-74081",
    "Erfurt": "99084-99099",
    "Friedrichshafen": "88045-88048",
    "Marl": "45768-45772",
    "Villingen-Schwenningen": "78048-78056",
    "Recklinghausen": "45657-45665",
    "Friedberg": "61169",
    "Ludwigsburg": "71634-71642",
    "Lohne": "49393",
    "Unna": "59423-59427",
    "Wetter (Ruhr)": "58300",
    "Naumburg": "06618",
    "Dinslaken": "46535-46539",
    "Gummersbach": "51643-51647",
    "Langenfeld": "40764",
    "Freiburg": "79098-79117",
    "Bremerhaven": "27568-27580",
    "Gladbeck": "45964-45968",
    "Witten": "58452-58456",
    "Cuxhaven": "27472-27478",
    "Arnsberg": "59755-59823",
    "Leverkusen": "51371-51381",
    "Velbert": "42549-42555",
    "Eggenstein-Leopoldshafen": "76344",
    "Hilden": "40721",
    "Viersen": "41747-41751",
    "Neu-Ulm": "89231-89233",
    "Neubrandenburg": "17033-17036",
    "Bergheim": "50126-50129",
    "Bad Waldsee": "88339",
    "Bergisch Gladbach": "51427-51469",
    "Wolfsburg": "38440-38448",
    "Waiblingen": "71332-71336",
    "Bamberg": "96047-96052",
    "Mannheim": "68159-68309",
    "Ennigerloh": "59320",
    "Sonneberg": "96515",
    "Passau": "94032-94036",
    "Willich": "47877",
    "Kerpen": "50169-50171",
    "Flensburg": "24937-24944",
    "Baden-Baden": "76530-76534",
    "Fulda": "36037-36043",
    "Borken": "46325",
    "Schweinfurt": "97421-97424",
    "Hattingen": "45525-45527",
    "Schiffweiler": "66578",
    "Forst": "03149",
    "Zwickau": "08056-08066",
    "Detmold": "32756-32760",
    "Günzburg": "89312",
    "Stadtlohn": "48703"
}

path=r'Germany_Global_Superstore.xlsx'
df=pd.read_excel(path)
for index, row in df.iterrows():
    city = row['City']
    if city in postal_codes:  # Ensure the city exists in the dictionary
        postal_code = postal_codes[city].split('-')[0]  # Extract first postal code
        df.loc[index, 'Postal Code'] = postal_code  # Update the DataFrame

# Save to CSV
df.to_csv('updated.csv', index=False)

'''plt.figure(figsize=(10, 5))
sns.histplot(df['Profit'], bins=30, kde=True, color='green')

# Thêm tiêu đề và nhãn
plt.title('Histogram', fontsize=14)
plt.xlabel('Doanh Số', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)

# Hiển thị biểu đồ
plt.show()'''


# Giả sử df là DataFrame ban đầu của bạn


# Các cột cần xử lý ngoại lai
'''cols_to_fix = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost']

for col in cols_to_fix:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Thay thế giá trị ngoại lai bằng giá trị gần nhất trong khoảng hợp lệ
    df[col] = df[col].apply(lambda x: lower_bound if x < lower_bound else (upper_bound if x > upper_bound else x))

# Lưu lại dữ liệu đã làm sạch
#df.to_excel("Cleaned_Germany_Global_Superstore1.xlsx", index=False)

# Vẽ biểu đồ
plt.figure(figsize=(10, 5))
sns.histplot(df['Shipping Cost'], bins=30, kde=True, color='green')

# Thêm tiêu đề và nhãn
plt.title('Histogram của Shipping Cost', fontsize=14)
plt.xlabel('Shipping Cost', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)

# Hiển thị biểu đồ
plt.show()'''

# Kiểm tra các dòng trùng lặp (dựa trên tất cả các cột)
duplicate_rows = df[df.duplicated()]
num_duplicates = duplicate_rows.shape[0]

# Loại bỏ các dòng trùng lặp
df_cleaned = df.drop_duplicates()

# Kiểm tra các giá trị ngoại lai bằng phương pháp IQR cho các cột số
numerical_cols = df_cleaned.select_dtypes(include=['number']).columns

Q1 = df_cleaned[numerical_cols].quantile(0.25)
Q3 = df_cleaned[numerical_cols].quantile(0.75)
IQR = Q3 - Q1

outliers = ((df_cleaned[numerical_cols] < (Q1 - 1.5 * IQR)) |
            (df_cleaned[numerical_cols] > (Q3 + 1.5 * IQR))).sum()

print(f'Số các giá trị trùng lặp là: {num_duplicates}')
print(f'Số các giá trị ngoại lai là: {outliers}')


