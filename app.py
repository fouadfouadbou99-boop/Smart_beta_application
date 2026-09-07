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
            index=False,
            sheet_name="Classement"
        )

    return output.getvalue()


if uploaded_file is not None:

    try:

        xls = pd.ExcelFile(uploaded_file)

        st.success("Fichier chargé avec succès")

        st.write("Feuilles détectées :")
        st.write(xls.sheet_names)

        # Lecture brute de la feuille Recap Scores

        recap = pd.read_excel(
            uploaded_file,
            sheet_name="Recap Scores",
            header=None
        )

        st.subheader("Recap Scores (brut)")

        st.dataframe(recap)

        st.divider()

        st.subheader("Extraction automatique")

        lignes = []

        for i in range(len(recap)):

            try:

                valeur = str(recap.iloc[i, 0])

                score = recap.iloc[i, 1]

                if pd.notna(score):

                    score = float(score)

                    if 0 <= score <= 100:

                        lignes.append(
                            [valeur, score]
                        )

            except:
                pass

        classement = pd.DataFrame(
            lignes,
            columns=[
                "Valeur",
                "Score Composite"
            ]
        )

        classement = classement.sort_values(
            "Score Composite",
            ascending=False
        )

        classement["Poids"] = (
            classement["Score Composite"]
            /
            classement["Score Composite"].sum()
        )

        st.subheader("Classement Smart Beta")

        st.dataframe(classement)

        st.bar_chart(
            classement.set_index(
                "Valeur"
            )["Score Composite"]
        )

        fichier_excel = export_excel(
            classement
        )

        st.download_button(
            "📥 Télécharger Excel",
            data=fichier_excel,
            file_name="SmartBeta_Classement.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        st.error(
            f"Erreur : {e}"
        )
