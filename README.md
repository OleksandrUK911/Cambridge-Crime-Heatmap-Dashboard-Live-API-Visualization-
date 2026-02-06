
# 🔍 Cambridge Crime Heatmap Dashboard (Live API + Visualization)

An interactive Streamlit dashboard that visualizes real-time crime data in Cambridge, UK using the UK Police API and Folium heatmaps.

---

## 🔗 Live App
[https://cambridge-crime-heatmap.streamlit.app](https://cambridge-crime-heatmap.streamlit.app)

---

## 📊 Features

- ✨ Real-time crime data via UK Police Open API
- 🔹 Filter by crime type, month, and street
- 📊 Interactive heatmap and clustering of locations
- 🗂️ Data table with export
- 📈 Trend analysis by month
- 🏆 Top streets by incidents
- 🔄 Auto-updates monthly
- 🌐 Built with Python, Streamlit, Folium, and Pandas

---

## 🛠️ How to Use

### Filters
- **Month**: Select a month to view incidents for that period
- **Crime Type**: Filter by specific type of crime or view all
- **Street**: (Optional) Filter incidents by street name

### Tabs
- **Теплова карта**: Heatmap of all incidents for the selected filters
- **Кластери**: KMeans clustering of incidents, with interactive markers
- **Таблиця**: Detailed table of filtered incidents, with CSV export
- **Графік тенденцій**: Line chart showing monthly crime trends
- **ТОП вулиць**: (Planned) List of streets with the highest number of incidents

---

## 💡 Use Cases
- Portfolio project for Data Science / GIS / ML
- Geo-visualization demo
- Public insight tool
- Urban safety analytics

---

## 🚀 Quickstart (Run Locally)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/cambridge-crime-heatmap
cd cambridge-crime-heatmap

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Streamlit
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud
1. Fork this repo to your GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Choose this repo and set `app.py` as the entry point
5. Deploy ✨

---

## 💾 Tech Stack
- Python 3.9+
- Streamlit
- Folium & Leaflet.js
- Pandas & Requests
- scikit-learn, matplotlib, seaborn
- UK Police API

---

## 📚 Example Usage

1. Select a month and crime type to analyze patterns
2. Use the heatmap to spot hotspots
3. Download the filtered data for your own analysis
4. Use clustering to identify crime-prone areas

---

## ❓ FAQ

**Q: Where does the data come from?**
A: Data is fetched live from the [UK Police API](https://data.police.uk/docs/).

**Q: How often is the data updated?**
A: The dashboard fetches new data every month and caches it for 1 hour.

**Q: Can I use this for other cities?**
A: Yes, by changing the polygon coordinates in `app.py`.

**Q: How do I add new features?**
A: Fork the repo, make your changes, and submit a pull request!

---

## 📬 Contact & Feedback

- Author: [Your Name](mailto:your@email.com)
- Issues: [GitHub Issues](https://github.com/yourusername/cambridge-crime-heatmap/issues)

---

## 🎨 Screenshots
<!-- Add screenshots to docs/preview.png or update this section -->
![screenshot](docs/preview.png)

---

## 📈 SEO Keywords
`cambridge crime data`, `heatmap UK police`, `streamlit folium map`, `real-time API visualization`, `crime data project portfolio`, `open data dashboard`, `urban analytics`, `public safety map`

---

Made with ❤️ for open data and open science.
