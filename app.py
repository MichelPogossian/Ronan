import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction des Marées", layout="wide")
st.title("Analyse des Marées au port de la Rochelle")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('data_legal_time.csv')
    # Afficher les noms des colonnes pour le débogage
    #st.write("Colonnes disponibles:", df.columns.tolist())
    
    # Si la colonne s'appelle différemment, ajustez le nom ici
    # Par exemple, si elle s'appelle 'date' ou 'time' au lieu de 'datetime'
    date_column = 'date'  # Ajustez ce nom selon votre CSV
    df['datetime'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sélection des dates
col1, col2 = st.columns(2)
with col1:
    date_debut = st.date_input(
        "Date de début",
        min_value=df['datetime'].dt.date.min(),
        max_value=df['datetime'].dt.date.max(),
        value=df['datetime'].dt.date.min()
    )
with col2:
    date_fin = st.date_input(
        "Date de fin",
        min_value=df['datetime'].dt.date.min(),
        max_value=df['datetime'].dt.date.max(),
        value=date_debut + pd.Timedelta(days=1)  # Configure la date de fin au jour suivant
    )

# Filtrage des données
mask = (df['datetime'].dt.date >= date_debut) & (df['datetime'].dt.date <= date_fin)
df_filtered = df[mask]

# Calcul des min et max par jour
daily_stats = df_filtered.groupby(df_filtered['datetime'].dt.date).agg({
    'hauteur': ['min', 'max']
}).reset_index()
daily_stats.columns = ['date', 'hauteur_min', 'hauteur_max']

# Affichage des statistiques quotidiennes
st.subheader("Hauteurs minimales et maximales par jour")
st.dataframe(daily_stats.style.format({
    'hauteur_min': '{:.2f} m',
    'hauteur_max': '{:.2f} m'
}))

# Création du graphique
st.subheader("Évolution de la hauteur des marées au port de la Rochelle")
fig = px.line(df_filtered, 
              x='datetime', 
              y='hauteur',
              title='Hauteur des marées',
              labels={'datetime': 'Date et heure', 'hauteur': 'Hauteur (m)'})

fig.update_layout(
    xaxis_title="Date et heure",
    yaxis_title="Hauteur (m)",
    hovermode='x'
)

st.plotly_chart(fig, use_container_width=True)
