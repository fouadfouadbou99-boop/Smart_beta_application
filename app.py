import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# ====================================================
# CONFIGURATION
# ====================================================

st.set_page_config(
    page_title="Smart Beta Maroc",
    layout="wide"
)

st.title("📈 Smart Beta Maroc")

st.markdown(
    """
    Application de calcul Smart Beta :
    - Value
    - Quality
    - Momentum
    - Low Volatility
    """
)

# ====================================================
# UPLOAD
# ====================================================

uploaded_file = st.file_uploader(
    "Charger le fichier Excel Smart Beta",
    type=["xlsx"]
)

# ====================================================
# FONCTIONS
# ====================================================

def score_rank(series, ascending=False):

    n = len(series)

    ranks = series.rank(
        method="min",
        ascending=ascending
    )

    scores = (
        (n - ranks)
        / (n - 1)
        * 100
    )

    return scores


def export_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="SmartBeta"
        )

    return output.getvalue()


# ====================================================
# TRAITEMENT
# ====================================================

if uploaded_file:

    try:

        sheets = pd.ExcelFile(uploaded_file)

        st.success("Fichier chargé avec succès")

        st.write("Feuilles détectées :")

        st.write(sheets.sheet_names)

        sheet = st.selectbox(
            "Choisir la feuille contenant les facteurs",
            sheets.sheet_names
        )

        df = pd.read_excel(
            uploaded_file,
            sheet_name=sheet
        )

        st.subheader("Données")

        st.dataframe(df)

        st.divider()

        st.subheader("Paramètres")

        w_value = st.slider(
            "Poids Value",
            0.0,
            1.0,
            0.30
        )

        w_quality = st.slider(
            "Poids Quality",
            0.0,
            1.0,
            0.30
        )

        w_momentum = st.slider(
            "Poids Momentum",
            0.0,
            1.0,
            0.20
        )

        w_lowvol = st.slider(
            "Poids Low Vol",
            0.0,
            1.0,
            0.20
        )

        if st.button("Calculer Smart Beta"):

            data = df.copy()

            cols = data.columns.tolist()

            st.write("Colonnes disponibles :", cols)

            # Exemple attendu :
            # Société | PE | ROE | Momentum | Volatility

            required = [
                "PE",
                "ROE",
                "Momentum",
                "Volatility",
            ]

            missing = [
                c
                for c in required
                if c not in data.columns
            ]

            if len(missing) > 0:

                st.error(
                    f"Colonnes manquantes : {missing}"
                )

            else:

                data["ValueScore"] = score_rank(
                    data["PE"],
                    ascending=True
                )

                data["QualityScore"] = score_rank(
                    data["ROE"],
                    ascending=False
                )

                data["MomentumScore"] = score_rank(
                    data["Momentum"],
                    ascending=False
                )

                data["LowVolScore"] = score_rank(
                    data["Volatility"],
                    ascending=True
                )

                data["CompositeScore"] = (

                    w_value
                    * data["ValueScore"]

                    + w_quality
                    * data["QualityScore"]

                    + w_momentum
                    * data["MomentumScore"]

                    + w_lowvol
                    * data["LowVolScore"]
                )

                data = data.sort_values(
                    "CompositeScore",
                    ascending=False
                )

                data["Weight"] = (
                    data["CompositeScore"]
                    /
                    data["CompositeScore"].sum()
                )

                st.success(
                    "Calcul Smart Beta terminé"
                )

                st.subheader(
                    "Classement Smart Beta"
                )

                st.dataframe(data)

                st.bar_chart(
                    data.set_index(
                        data.columns[0]
                    )["CompositeScore"]
                )

                excel_file = export_excel(data)

                st.download_button(
                    label="📥 Télécharger Excel",
                    data=excel_file,
                    file_name="SmartBeta_Resultat.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:

        st.error(str(e))
