# Smart Beta Maroc

Application Streamlit permettant de construire automatiquement un portefeuille Smart Beta sur les actions cotées à la Bourse de Casablanca.

## Fonctionnalités

- Import Excel
- Calcul des facteurs Value
- Calcul des facteurs Quality
- Calcul des facteurs Momentum
- Calcul des facteurs Low Volatility
- Score composite paramétrable
- Classement Smart Beta
- Construction automatique du portefeuille
- Backtesting
- Comparaison avec le MASI
- Export Excel
- Export PDF
- Dashboard interactif Streamlit

---

## Architecture

smart-beta-maroc/

├── app.py

├── requirements.txt

├── README.md

├── .gitignore

├── modules/

│   ├── data_loader.py

│   ├── factor_engine.py

│   ├── ranking.py

│   ├── portfolio.py

│   ├── backtest.py

│   ├── charts.py

│   ├── excel_export.py

│   └── pdf_report.py

├
