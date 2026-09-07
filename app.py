import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Smart Beta Maroc",
    layout="wide"
)

st.title("📈 Smart Beta Maroc")

uploaded_file = st.file_uploader(
    "Charger le fichier Smart Beta",
    type=["xlsx"]
)

def export_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Portefeuille",
            index=False
        )

    return output.getvalue()

if uploaded_file is not None:

    try:

        df = pd.read_excel(
            uploaded_file,
            sheet_name="Facteurs"
        )

        # Nettoyage
        df.columns = [str(c).strip() for c in df.columns]

        # Conversion numérique
        cols_num = [
            "PE",
            "ROE",
            "Momentum",
            "Volatilite",
            "ValueScore",
            "QualityScore",
            "MomentumScore",
            "LowVolScore",
            "CompositeScore",
            "Poids"
        ]

        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        df = df.dropna(
            subset=["Valeur"]
        )

        classement = df.sort_values(
            by="CompositeScore",
            ascending=False
        )

        st.success(
            "Fichier chargé avec succès"
        )

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
            "Poids total %",
            round(
                classement["Poids"].sum() * 100,
                2
            )
        )

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

        st.subheader(
            "📊 Portefeuille complet"
        )

        st.dataframe(
            classement,
            use_container_width=True
        )

        st.subheader(
            "Classement Smart Beta"
        )

        chart_df = classement[
            ["Valeur", "CompositeScore"]
        ].copy()

        chart_df = chart_df.set_index(
            "Valeur"
        )

        st.bar_chart(chart_df)

        st.subheader(
            "Poids du portefeuille"
        )

        poids_df = classement[
            ["Valeur", "Poids"]
        ]

        st.dataframe(
            poids_df,
            use_container_width=True
        )

        excel_file = export_excel(
            classement
        )

        st.download_button(
            label="📥 Télécharger Excel",
            data=excel_file,
            file_name="Portefeuille_Smart_Beta.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(
            f"Erreur : {str(e)}"
        )
