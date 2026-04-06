import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 AnyCompany – Tableau de Bord des Ventes")

# --- Ventes annuelles ---
df_annual = session.sql("""
    SELECT YEAR(TRANSACTION_DATE) AS ANNEE,
           COUNT(*) AS NB_TRANSACTIONS,
           SUM(AMOUNT) AS TOTAL_VENTES,
           AVG(AMOUNT) AS PANIER_MOYEN
    FROM ANYCOMPANY_LAB.SILVER.FINANCIAL_TRANSACTIONS_CLEAN
    WHERE TRANSACTION_TYPE = 'Sale'
    GROUP BY 1 ORDER BY 1
""").to_pandas()

st.subheader("Évolution annuelle des ventes")
st.line_chart(df_annual.set_index("ANNEE")[["TOTAL_VENTES"]])

col1, col2 = st.columns(2)
with col1:
    st.metric("Total ventes", f"${df_annual['TOTAL_VENTES'].sum():,.0f}")
with col2:
    st.metric("Panier moyen global", f"${df_annual['PANIER_MOYEN'].mean():,.0f}")

# --- Ventes par région ---
st.subheader("Ventes par Région")
df_region = session.sql("""
    SELECT REGION,
           COUNT(*) AS NB_TRANSACTIONS,
           SUM(AMOUNT) AS TOTAL_VENTES,
           AVG(AMOUNT) AS PANIER_MOYEN
    FROM ANYCOMPANY_LAB.SILVER.FINANCIAL_TRANSACTIONS_CLEAN
    WHERE TRANSACTION_TYPE = 'Sale'
    GROUP BY 1 ORDER BY TOTAL_VENTES DESC
""").to_pandas()
st.bar_chart(df_region.set_index("REGION")[["TOTAL_VENTES"]])
st.dataframe(df_region, use_container_width=True)

# --- Ventes par type de transaction ---
st.subheader("Répartition par Type de Transaction")
df_type = session.sql("""
    SELECT TRANSACTION_TYPE,
           COUNT(*) AS NB_TRANSACTIONS,
           SUM(AMOUNT) AS TOTAL_MONTANT
    FROM ANYCOMPANY_LAB.SILVER.FINANCIAL_TRANSACTIONS_CLEAN
    GROUP BY 1 ORDER BY TOTAL_MONTANT DESC
""").to_pandas()
st.bar_chart(df_type.set_index("TRANSACTION_TYPE")[["TOTAL_MONTANT"]])

# --- Ventes mensuelles ---
st.subheader("Évolution mensuelle des ventes")
df_monthly = session.sql("""
    SELECT DATE_TRUNC('MONTH', TRANSACTION_DATE) AS MOIS,
           SUM(AMOUNT) AS TOTAL_VENTES
    FROM ANYCOMPANY_LAB.SILVER.FINANCIAL_TRANSACTIONS_CLEAN
    WHERE TRANSACTION_TYPE = 'Sale'
    GROUP BY 1 ORDER BY 1
""").to_pandas()
st.line_chart(df_monthly.set_index("MOIS")[["TOTAL_VENTES"]])

# --- Démographie clients ---
st.subheader("Répartition des Clients")
col1, col2 = st.columns(2)

with col1:
    st.write("**Par genre**")
    df_gender = session.sql("""
        SELECT GENDER, COUNT(*) AS NB_CLIENTS
        FROM ANYCOMPANY_LAB.SILVER.CUSTOMER_DEMOGRAPHICS_CLEAN
        GROUP BY 1 ORDER BY NB_CLIENTS DESC
    """).to_pandas()
    st.bar_chart(df_gender.set_index("GENDER"))

with col2:
    st.write("**Par tranche de revenu**")
    df_income = session.sql("""
        SELECT SEGMENT_REVENU, COUNT(*) AS NB_CLIENTS
        FROM ANYCOMPANY_LAB.ANALYTICS.CLIENTS_ENRICHIS
        GROUP BY 1 ORDER BY NB_CLIENTS DESC
    """).to_pandas()
    st.bar_chart(df_income.set_index("SEGMENT_REVENU"))
