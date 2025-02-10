import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)

def update_postal_codes(df, postal_codes):
    def get_postal_code(city):
        return postal_codes.get(city, '').split('-')[0]

    df['Postal Code'] = df['City'].apply(get_postal_code)
    return df

st.title("Phân tích dữ liệu thị trường")
st.write("Upload file dữ liệu (.csv hoặc .xlsx) và chọn quốc gia để phân tích.")

# Upload file
uploaded_file = st.file_uploader("Upload file dữ liệu", type=['csv', 'xlsx'])
if uploaded_file:
    # Load dữ liệu
    df = load_data(uploaded_file)

    # Kiểm tra nếu có cột 'Country'
    if "Country" in df.columns:
        countries = df["Country"].dropna().unique()
        selected_country = st.selectbox("Chọn quốc gia", sorted(countries))

        # Lọc dữ liệu theo quốc gia
        df_cleaned = df[df["Country"] == selected_country].copy()

        # Tiền xử lý dữ liệu
        df_cleaned.drop_duplicates(inplace=True)
        df_cleaned.fillna(method='ffill', inplace=True)

        # Xử lý dữ liệu thời gian
        df_cleaned['Order Date'] = pd.to_datetime(df_cleaned['Order Date'], errors='coerce')
        df_cleaned['Ship Date'] = pd.to_datetime(df_cleaned['Ship Date'], errors='coerce')

        # Kiểm tra nếu có giá trị NaT (Not a Time)
        if df_cleaned['Order Date'].isnull().sum() > 0 or df_cleaned['Ship Date'].isnull().sum() > 0:
            st.warning(
                f"Có {df_cleaned['Order Date'].isnull().sum()} giá trị không hợp lệ trong 'Order Date' và {df_cleaned['Ship Date'].isnull().sum()} giá trị không hợp lệ trong 'Ship Date'.")

        # Tính khoảng thời gian giao hàng
        df_cleaned['Delivery Time'] = (df_cleaned['Ship Date'] - df_cleaned['Order Date']).dt.days
        average_delivery_time = df_cleaned['Delivery Time'].mean()

        # Xử lý ngoại lai bằng trung vị
        numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Shipping Cost']
        df_cleaned = df_cleaned.copy()

        for col in numeric_cols:
            if col in df_cleaned.columns:
                Q1 = df_cleaned[col].quantile(0.25)
                Q3 = df_cleaned[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                median_value = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].apply(
                    lambda x: median_value if x < lower_bound or x > upper_bound else x)

        # Cập nhật mã bưu chính
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
        df_cleaned = update_postal_codes(df_cleaned, postal_codes)

        st.write("Dữ liệu đã tải lên:")
        st.dataframe(df.head())
        # Hiển thị dữ liệu đã lọc và xử lý
        st.write("Dữ liệu đã lọc và xử lý: ")
        st.dataframe(df_cleaned.head())

        # Lưu dữ liệu đã xử lý vào file CSV
        if st.button("Lưu dữ liệu đã xử lý"):
            df_cleaned.to_csv(f'Updated_{selected_country}_data.csv', index=False)
            st.success(f"Dữ liệu đã được lưu vào file 'Updated_{selected_country}_data.csv'")

        # Tabs cho từng phần phân tích
        tab1, tab2, tab3,tab4=st.tabs(
            ["Tổng quan dữ liệu", "Trực quan hóa", "Phân tích dữ liệu",'Insight và Giải pháp'])

        # 2. Tổng quan dữ liệu
        with tab1:
            st.subheader(f"Tổng quan dữ liệu - {selected_country}")
            total_orders = len(df_cleaned)
            total_sales = df_cleaned['Sales'].sum()
            total_customers = df_cleaned['Customer ID'].nunique()
            total_profit = df_cleaned['Profit'].sum()

            st.write(f"**Số lượng đơn hàng**: {total_orders}")
            st.write(f"**Tổng doanh số**: ${total_sales:,.2f}")
            st.write(f"**Tổng lợi nhuận**: ${total_profit:,.2f}")
            st.write(f"**Số lượng khách hàng**: {total_customers}")
            st.write(f"**Thời gian giao hàng trung bình**: {average_delivery_time:.2f} ngày")

            st.subheader("Doanh số và lợi nhuận theo phân khúc khách hàng")

            # Grouping and aggregating data
            segment_analysis = df_cleaned.groupby('Segment').agg(
                total_sales=('Sales', 'sum'),
                total_profit=('Profit', 'sum'),
                total_orders=('Order ID', 'count')
            ).reset_index()

            # Format numbers for better readability
            segment_analysis['total_sales'] = segment_analysis['total_sales'].map('{:,.2f}'.format)
            segment_analysis['total_profit'] = segment_analysis['total_profit'].map('{:,.2f}'.format)
            segment_analysis['total_orders'] = segment_analysis['total_orders'].map('{:,}'.format)

            # Rename columns for display
            segment_analysis = segment_analysis.rename(columns={
                "total_sales": "Tổng doanh số",
                "total_profit": "Tổng lợi nhuận",
                "total_orders": "Tổng số đơn hàng"
            })

            st.dataframe(segment_analysis)

            st.subheader("Phân tích theo phân khúc vận chuyển")

            # Grouping and aggregating data for shipping analysis
            shipping_analysis = df_cleaned.groupby('Ship Mode').agg(
                total_orders=('Order ID', 'count'),
                avg_shipping_cost=('Shipping Cost', 'mean'),
                avg_profit=('Profit', 'mean')
            ).reset_index()

            # Format numbers for better readability
            shipping_analysis['avg_shipping_cost'] = shipping_analysis['avg_shipping_cost'].map('{:,.2f}'.format)
            shipping_analysis['avg_profit'] = shipping_analysis['avg_profit'].map('{:,.2f}'.format)
            shipping_analysis['total_orders'] = shipping_analysis['total_orders'].map('{:,}'.format)

            # Rename columns for display
            shipping_analysis = shipping_analysis.rename(columns={
                "total_orders": "Tổng số đơn hàng",
                "avg_shipping_cost": "Chi phí vận chuyển trung bình",
                "avg_profit": "Lợi nhuận trung bình"
            })
            st.dataframe(shipping_analysis)

            st.subheader("Phân tích theo thứ tự ưu tiên")

            # Grouping and aggregating data for order priority
            priority_analysis = df_cleaned.groupby('Order Priority').agg(
                total_orders=('Order ID', 'count'),
                avg_shipping_cost=('Shipping Cost', 'mean'),
                avg_profit=('Profit', 'mean')
            ).reset_index()

            # Format numbers for better readability
            priority_analysis['avg_shipping_cost'] = priority_analysis['avg_shipping_cost'].map('{:,.2f}'.format)
            priority_analysis['avg_profit'] = priority_analysis['avg_profit'].map('{:,.2f}'.format)
            priority_analysis['total_orders'] = priority_analysis['total_orders'].map('{:,}'.format)

            # Rename columns for display
            priority_analysis = priority_analysis.rename(columns={
                "total_orders": "Số lượng đơn hàng",
                "avg_shipping_cost": "Chi phí vận chuyển trung bình",
                "avg_profit": "Lợi nhuận trung bình"
            })
            st.dataframe(priority_analysis)

            st.subheader("Phân tích theo danh mục con (Sub-Category)")

            # Grouping and aggregating data
            sub_analysis = df_cleaned.groupby('Sub-Category').agg(
                total_sales=('Sales', 'sum'),
                total_profit=('Profit', 'sum'),
                total_orders=('Order ID', 'count')
            ).reset_index()

            # Format numbers for better readability
            sub_analysis['total_sales'] = sub_analysis['total_sales'].map('{:,.2f}'.format)
            sub_analysis['total_profit'] = sub_analysis['total_profit'].map('{:,.2f}'.format)
            sub_analysis['total_orders'] = sub_analysis['total_orders'].map('{:,}'.format)

            # Rename columns for display
            sub_analysis = sub_analysis.rename(columns={
                "total_sales": "Tổng doanh số",
                "total_profit": "Tổng lợi nhuận",
                "total_orders": "Tổng số đơn hàng"
            })

            st.dataframe(sub_analysis)

        # 3. Trực quan hóa dữ liệu
        with tab2:
            st.subheader(f"Trực quan hóa dữ liệu - {selected_country}")

            # Xu hướng doanh số theo thời gian
            sales_trend = df_cleaned.groupby(pd.Grouper(key='Order Date', freq='M'))[
                ['Sales', 'Profit', 'Quantity']].sum()

            fig1 = go.Figure()

            fig1.add_trace(go.Scatter(
                x=sales_trend.index,
                y=sales_trend['Sales'],
                mode='lines',
                name='Sales',
                line=dict(color='dodgerblue', width=2)
            ))

            fig1.add_trace(go.Scatter(
                x=sales_trend.index,
                y=sales_trend['Profit'],
                mode='lines',
                name='Profit',
                line=dict(color='coral', width=2)
            ))

            fig1.update_layout(
                title=dict(text="Biểu đồ thể hiện doanh thu theo tháng và xu hướng lợi nhuận", font=dict(size=20, color='white')),
                xaxis=dict(
                    title="Tháng",
                    tickformat='%b %Y',
                    tickfont=dict(size=12, color='white'),
                    showgrid=True
                ),
                yaxis=dict(
                    title="Giá trị",
                    tickfont=dict(size=12, color='white'),
                    showgrid=True
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=12, color='white')
                ),
                template="plotly_dark",
                margin=dict(l=40, r=40, t=60, b=50)
            )

            st.plotly_chart(fig1)

            city_sales = df_cleaned.groupby('City')[['Sales', 'Profit']].sum().sort_values(by='Sales',
                                                                                             ascending=False)
            fig2 = px.bar(city_sales, x=city_sales.index, y=['Sales','Profit'], title="Doanh số và lợi nhuận theo thành phố",
                          barmode='group',color_discrete_map={'Sales':'deepskyblue','Profit':'wheat'},labels={'value':'Giá trị','variable':'Phân loại'})
            st.plotly_chart(fig2)

            category_profit = df_cleaned.groupby('Category')['Profit'].sum()
            fig3 = px.pie(category_profit, values='Profit', names=category_profit.index,
                          title="Lợi nhuận theo danh mục sản phẩm")
            st.plotly_chart(fig3)

            # So sánh doanh số giữa các danh mục sản phẩm
            category_sales = df_cleaned.groupby('Category')['Sales'].sum()
            fig4 = px.pie(category_sales, values='Sales', names=category_sales.index,
                          title="Doanh số theo danh mục sản phẩm")
            st.plotly_chart(fig4)

            category_segment_data = df_cleaned.groupby(["Country", "Category", "Segment"])[
                ["Sales", "Profit"]].sum().reset_index()

            st.title("So sánh hiệu quả kinh doanh quốc gia theo phân khúc khách hàng")

            cleaned_data = category_segment_data[category_segment_data["Country"] == selected_country]

            fig5 = px.bar(
                cleaned_data,
                x="Category",
                y="Sales",
                color="Segment",
                barmode="group",
                text_auto=".2s",
                title=f"Tổng Doanh Thu theo phân khúc khách hàng tại {selected_country}",
                labels={"Sales": "Doanh Thu", "Category": "Danh mục sản phẩm", "Segment": "Phân khúc"},
            )

            fig6 = px.line(
                cleaned_data,
                x="Category",
                y="Profit",
                color="Segment",
                markers=True,
                title=f"Tổng Lợi Nhuận theo phân khúc khách hàng tại {selected_country}",
                labels={"Profit": "Lợi nhuận", "Category": "Danh mục sản phẩm", "Segment": "Phân khúc"},
            )

            st.plotly_chart(fig5, use_container_width=True)
            st.plotly_chart(fig6, use_container_width=True)

        with tab3:
            st.subheader(f"Phân tích dữ liệu - {selected_country}")

            ship_mode_analysis = df_cleaned.groupby('Ship Mode')[['Sales', 'Profit']].sum()
            fig7 = px.bar(ship_mode_analysis, x=ship_mode_analysis.index, y=['Sales','Profit'],
                          title="Doanh thu và lợi nhuận theo trạng thái vận chuyển",barmode='group',labels={'value':'Giá trị','variable':'Phân loại'},color_discrete_map={'Sales':'dodgerblue','Profit':'powderblue'})
            st.plotly_chart(fig7)

            order_priority_analysis = df_cleaned.groupby('Order Priority')[['Sales', 'Profit']].sum()
            fig8 = px.bar(order_priority_analysis, x=order_priority_analysis.index, y=['Sales','Profit'],
                          title="Doanh thu và lợi nhuận theo thứ tự ưu tiên đơn hàng",barmode='group',labels={'value':'Giá trị','variable':'Phân loại'},color_discrete_map={'Sales':'dodgerblue','Profit':'powderblue'})
            st.plotly_chart(fig8)
        with tab4:
            st.subheader('Insight:')
            st.write("- ")
            st.write("- ")
            st.write("- ")
            st.subheader('Giải pháp:')
            st.write("- Tăng doanh thu cho các danh mục có biên lợi nhuận cao.")
            st.write("- Giảm thiểu danh mục có doanh thu thấp, lợi nhuận thấp.")
            st.write("- Phân tích xu hướng mua hàng, đánh giá xem danh mục nào có tiềm năng tăng trưởng.")
            st.write("- Thử nghiệm chiến dịch tiếp thị trong 3-6 tháng để đo lường hiệu quả của việc tập trung vào danh mục có lợi nhuận cao.")
            st.write("- Xem xét dữ liệu bán hàng theo quý, nếu danh mục không cải thiện, cân nhắc thay thế bằng sản phẩm khác.")
            st.write("- Tối ưu chi phí để tăng lợi nhuận.")
            st.write("- Ổn định doanh thu để giảm rủi ro.")
            st.write("-	Tăng lợi nhuận bằng cách cải thiện biên lợi nhuận.")
            st.write("-	Dự báo và lập kế hoạch tài chính.")

    else:
        st.error("File dữ liệu không có cột 'Country'. Vui lòng kiểm tra lại.")
else:
    st.info("Vui lòng upload file dữ liệu để tiếp tục.")
