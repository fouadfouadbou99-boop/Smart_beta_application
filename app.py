import streamlit as st
import pandas as pd
from io import BytesIO

# ===================================================
# PARAMETRES
# ===================================================

st.set_page_config(
    page_title="Smart Beta Maroc",
    layout="wide"
)

st.title("📈 Smart Beta Maroc")

st.markdown("""
### Modèle Smart Beta Maroc

Facteurs utilisés :

- Value
- Quality
- Momentum
- Low Volatility

Chargement du fichier Excel Smart Beta.
""")

# ===================================================
# EXPORT EXCEL
# ===================================================

def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Portefeuille"
        )

    return output.getvalue()

# ===================================================
# UPLOAD
# ===================================================

uploaded_file = st.file_uploader(
    "Charger le fichier Smart Beta",
    type=["xlsx"]
)

# ===================================================
# TRAITEMENT
# ===================================================

if uploaded_file:

    try:

        df = pd.read_excel(
            uploaded_file,
            sheet_name="Facteurs"
        )

        st.success(
            "Fichier chargé avec succès"
        )

        # Suppression lignes vides éventuelles

        df = df.dropna(
            subset=["Valeur"]
        )

        # Tri classement

        classement = df.sort_values(
            "CompositeScore",
            ascending=False
        )

        # ===================================================
        # INDICATEURS
        # ===================================================

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Nombre de titres",
            len(classement)
        )

        col2.metric(
            "Score moyen",
            round(
                classement["CompositeScore"].mean(),
                2
            )
        )

        col3.metric(
            "Poids total",
            round(
                classement["Poids"].sum()*100,
                2
            )
        )

        # ===================================================
        # TOP 10
        # ===================================================

        st.subheader(
            "🏆 Top 10 Smart Beta"
        )

        st.dataframe(

            classement[
                [
                    "Valeur",
                    "CompositeScore",
                    "Poids"
                ]
            ].head(10)

        )

        # ===================================================
        # PORTEFEUILLE COMPLET
        # ===================================================

        st.subheader(
            "📋 Portefeuille complet"
        )

        st.dataframe(
            classement
        )

        # ===================================================
        # GRAPHIQUE SCORE
        # ===================================================

        st.subheader(
            "Classement Smart Beta"
        )

        chart = classement.set_index(
            "Valeur"
        )["CompositeScore"]

        st.bar_chart(chart)

        # ===================================================
        # REPARTITION DES POIDS
        # ===================================================

        st.subheader(
            "Répartition des poids"
        )
