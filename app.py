import streamlit as st
import pandas as pd
import requests
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(page_title="Cambridge Crime Heatmap", layout="wide")

st.title("🔍 Теплова карта злочинності в Кембріджі")
st.markdown("Дані отримано в реальному часі з UK Police API.")

@st.cache_data(ttl=3600)
def fetch_crime_data():
    poly = "52.209,0.123:52.202,0.117:52.206,0.130"
    
    # 🔧 ТУТ встановлюємо стабільну дату (остання з доступних)
    date = "2024-12"
    
    url = f"https://data.police.uk/api/crimes-street/all-crime?poly={poly}&date={date}"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("❌ Не вдалося отримати дані з API.")
        return pd.DataFrame()

    data = response.json()
    df = pd.json_normalize(data)

    if df.empty:
        return pd.DataFrame()

    df = df[["category", "location.latitude", "location.longitude", "month"]]
    df.columns = ["crime_type", "latitude", "longitude", "date"]
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["date"] = pd.to_datetime(df["date"])

    return df

df = fetch_crime_data()

if df.empty:
    st.warning("Дані відсутні або API не відповідає.")
    st.stop()

crime_types = sorted(df["crime_type"].unique())
selected_type = st.selectbox("Оберіть тип злочину", ["Усі"] + crime_types)

if selected_type != "Усі":
    df_filtered = df[df["crime_type"] == selected_type]
else:
    df_filtered = df.copy()

st.markdown(f"Знайдено **{len(df_filtered)}** інцидентів.")

st.subheader("🗺️ Теплова карта")
m = folium.Map(location=[52.2053, 0.1218], zoom_start=14)

heat_data = df_filtered[["latitude", "longitude"]].values.tolist()
if heat_data:
    HeatMap(heat_data).add_to(m)
else:
    folium.Marker([52.2053, 0.1218], popup="Даних немає").add_to(m)

st_folium(m, width=1000, height=600)

with st.expander("📋 Показати таблицю злочинів"):
    st.dataframe(df_filtered, use_container_width=True)

st.markdown("---")
st.markdown("Джерело даних: [data.police.uk](https://data.police.uk/docs/)")
