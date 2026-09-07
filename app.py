import streamlit as st
import pandas as pd
from io import BytesIO

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Beta Maroc",
    layout="wide"
)

st.title("📈 Smart Beta Maroc")

st.markdown(
    """
    Application Smart Beta Maroc

    Facteurs utilisés :
    - Value
    - Quality
    - Momentum
    - Low Volatility
    """
)

# =====================================================
# EXPORT EXCEL
# =====================================================

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

# =====================================================
# IMPORT FICHIER
# =====================================================

uploaded_file = st.file_uploader(
    "Charger le fichier Smart Beta",
    type=["xlsx"]
)

# =====================================================
# TRAITEMENT
# =====================================================

if uploaded_file is not None:

    try:

        df = pd.read_excel(
            uploaded_file,
            sheet_name="Facteurs"
        )

        # Nettoyage

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        # Colonnes numériques

        numeric_cols = [

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

        for col in numeric_cols:

            if col in df.columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        df = df.dropna(
            subset=["Valeur"]
        )

        st.success(
            "Fichier chargé avec succès"
        )

        # =====================================================
        # PONDERATIONS
        # =====================================================

        st.subheader(
            "⚙️ Pondération des facteurs"
        )

        col1, col2 = st.columns(2)

        with col1:

            w_value = st.slider(
                "Value",
                0.0,
                1.0,
                0.30,
                0.05
            )

            w_quality = st.slider(
                "Quality",
                0.0,
                1.0,
                0.30,
                0.05
            )

        with col2:

            w_momentum = st.slider(
                "Momentum",
                0.0,
                1.0,
                0.20,
                0.05
            )

            w_lowvol = st.slider(
                "Low Volatility",
                0.0,
                1.0,
                0.20,
                0.05
            )

        total_weight = (
            w_value +
            w_quality +
            w_momentum +
            w_lowvol
        )

        if abs(total_weight - 1.0) > 0.001:

            st.error(
                f"La somme des pondérations doit être égale à 100%. Somme actuelle : {round(total_weight*100,2)}%"
            )

            st.stop()

        # =====================================================
        # RECALCUL SMART BETA
        # =====================================================

        df["CompositeScore"] = (

            w_value * df["ValueScore"]

            + w_quality * df["QualityScore"]

            + w_momentum * df["MomentumScore"]

            + w_lowvol * df["LowVolScore"]

        )

        df["Poids"] = (

            df["CompositeScore"]

            /

            df["CompositeScore"].sum()

        )

        classement = df.sort_values(
            by="CompositeScore",
            ascending=False
        )

        # =====================================================
        # KPIs
        # =====================================================

        st.subheader(
            "📊 Statistiques"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Nombre de titres",
            len(classement)
        )

        c2.metric(
            "Score moyen",
            round(
                classement["CompositeScore"].mean(),
                2
            )
        )

        c3.metric(
            "Poids total",
            f"{round(classement['Poids'].sum()*100,2)}%"
        )

        # =====================================================
        # TOP 10
        # =====================================================

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
            ]
            .head(10),

            use_container_width=True
        )

        # =====================================================
        # PORTEFEUILLE
        # =====================================================

        st.subheader(
            "📋 Portefeuille complet"
        )

        st.dataframe(
            classement,
            use_container_width=True
        )

        # =====================================================
        # GRAPHIQUE
        # =====================================================

        st.subheader(
            "📈 Classement Smart Beta"
        )

        chart_df = classement[
            [
                "Valeur",
                "CompositeScore"
            ]
        ]

        chart_df = chart_df.set_index(
            "Valeur"
        )

        st.bar_chart(chart_df)

        # =====================================================
        # POIDS
        # =====================================================

        st.subheader(
            "⚖️ Répartition des poids"
        )

        st.dataframe(

            classement[
                [
                    "Valeur",
                    "Poids"
                ]
            ],

            use_container_width=True
        )

        # =====================================================
        # EXPORT
        # =====================================================

        excel_file = export_excel(
            classement
        )

        st.download_button(
            label="📥 Télécharger le portefeuille Excel",
            data=excel_file,
            file_name="Portefeuille_Smart_Beta.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(
            f"Erreur : {str(e)}"
        )
