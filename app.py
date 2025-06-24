import streamlit as st
import pandas as pd
import requests
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Cambridge Crime Heatmap", layout="wide")

st.title("🔍 Теплова карта злочинності в Кембріджі")
st.markdown("Дані отримано з UK Police API. Інтерактивна аналітика та машинне навчання.")

@st.cache_data(ttl=3600)
def fetch_crime_data():
    poly = "52.209,0.123:52.202,0.117:52.206,0.130"
    months = pd.date_range("2024-01-01", "2024-12-01", freq="MS").strftime("%Y-%m").tolist()
    all_data = []
    for date in months:
        url = f"https://data.police.uk/api/crimes-street/all-crime?poly={poly}&date={date}"
        r = requests.get(url)
        if r.status_code == 200:
            all_data.extend(r.json())
    df = pd.json_normalize(all_data)
    if df.empty:
        return pd.DataFrame()
    df = df[["category", "location.latitude", "location.longitude", "month", "location.street.name"]]
    df.columns = ["crime_type", "latitude", "longitude", "date", "street"]
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = fetch_crime_data()

if df.empty:
    st.warning("Дані відсутні або API не відповідає.")
    st.stop()

# --- Filters ---
df["month"] = df["date"].dt.to_period("M")
unique_months = sorted(df["month"].astype(str).unique())
selected_month = st.selectbox("Оберіть місяць", unique_months)
df = df[df["month"] == selected_month]

crime_types = sorted(df["crime_type"].unique())
selected_type = st.selectbox("Оберіть тип злочину", ["Усі"] + crime_types)
if selected_type != "Усі":
    df = df[df["crime_type"] == selected_type]

# Optional street filter
streets = sorted(df["street"].dropna().unique())
selected_street = st.selectbox("Фільтр по вулиці (опціонально)", ["Усі"] + streets)
if selected_street != "Усі":
    df = df[df["street"] == selected_street]

st.markdown(f"Знайдено **{len(df)}** інцидентів.")

# --- Map Tabs ---
tabs = st.tabs(["Теплова карта", "Кластери", "Таблиця", "Графік тенденцій", "ТОП вулиць"])

with tabs[0]:
    st.subheader("🗺️ Теплова карта")
    m = folium.Map(location=[52.2053, 0.1218], zoom_start=14)
    heat_data = df[["latitude", "longitude"]].values.tolist()
    if heat_data:
        HeatMap(heat_data).add_to(m)
    st_folium(m, width=1000, height=600)

with tabs[1]:
    st.subheader("📊 Кластеризація KMeans")
    m2 = folium.Map(location=[52.2053, 0.1218], zoom_start=14)
    if len(df) >= 3:
        kmeans = KMeans(n_clusters=5, random_state=0).fit(df[["latitude", "longitude"]])
        df["cluster"] = kmeans.labels_
        marker_cluster = MarkerCluster().add_to(m2)
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"Тип: {row['crime_type']}<br>Вулиця: {row['street']}<br><a href='https://maps.google.com/?q={row['latitude']},{row['longitude']}' target='_blank'>Google Maps</a>",
                icon=folium.Icon(color="red")
            ).add_to(marker_cluster)
    st_folium(m2, width=1000, height=600)

with tabs[2]:
    st.subheader("📄 Детальна таблиця")
    st.dataframe(df[["crime_type", "date", "street", "latitude", "longitude"]], use_container_width=True)
    st.download_button("⬇️ Завантажити CSV", data=df.to_csv(index=False), file_name="cambridge_crime.csv")

with tabs[3]:
    st.subheader("📈 Динаміка злочинності по місяцях")
    trend_df = df.groupby(df["date"].dt.to_period("M")).size().reset_index(name="count")
    trend_df["date"] = trend_df["date"].astype(str)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=trend_df, x="date", y="count", marker="o", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tabs[4]:
    st.subheader("🔝 Найнебезпечніші вулиці")
    top_streets = df["street"].value_counts().head(10)
    st.bar_chart(top_streets)
