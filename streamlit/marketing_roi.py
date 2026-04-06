import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Marketing ROI", layout="wide")
st.title("💰 AnyCompany – Marketing ROI & Performance")

# --- Performance par type de campagne ---
st.subheader("Performance par Type de Campagne")
df_type = session.sql("""
    SELECT CAMPAIGN_TYPE,
           COUNT(*) AS NB_CAMPAGNES,
           SUM(BUDGET) AS BUDGET_TOTAL,
           AVG(CONVERSION_RATE) AS TAUX_CONVERSION_MOYEN,
           SUM(REACH) AS REACH_TOTAL,
           SUM(BUDGET) / NULLIF(SUM(REACH), 0) AS COUT_PAR_REACH
    FROM ANYCOMPANY_LAB.SILVER.MARKETING_CAMPAIGNS_CLEAN
    GROUP BY 1 ORDER BY TAUX_CONVERSION_MOYEN DESC
""").to_pandas()

col1, col2 = st.columns(2)
with col1:
    st.bar_chart(df_type.set_index("CAMPAIGN_TYPE")[["TAUX_CONVERSION_MOYEN"]])
with col2:
    st.bar_chart(df_type.set_index("CAMPAIGN_TYPE")[["COUT_PAR_REACH"]])
st.dataframe(df_type, use_container_width=True)

# --- Performance par catégorie produit ---
st.subheader("Performance par Catégorie Produit")
df_cat = session.sql("""
    SELECT PRODUCT_CATEGORY,
           COUNT(*) AS NB_CAMPAGNES,
           SUM(BUDGET) AS BUDGET_TOTAL,
           AVG(CONVERSION_RATE) AS TAUX_CONVERSION_MOYEN
    FROM ANYCOMPANY_LAB.SILVER.MARKETING_CAMPAIGNS_CLEAN
    GROUP BY 1 ORDER BY TAUX_CONVERSION_MOYEN DESC
""").to_pandas()
st.bar_chart(df_cat.set_index("PRODUCT_CATEGORY")[["TAUX_CONVERSION_MOYEN"]])

# --- Performance par audience ---
st.subheader("Performance par Audience Cible")
df_audience = session.sql("""
    SELECT TARGET_AUDIENCE,
           COUNT(*) AS NB_CAMPAGNES,
           AVG(BUDGET) AS BUDGET_MOYEN,
           AVG(CONVERSION_RATE) AS TAUX_CONVERSION_MOYEN
    FROM ANYCOMPANY_LAB.SILVER.MARKETING_CAMPAIGNS_CLEAN
    GROUP BY 1 ORDER BY TAUX_CONVERSION_MOYEN DESC
""").to_pandas()
st.bar_chart(df_audience.set_index("TARGET_AUDIENCE")[["TAUX_CONVERSION_MOYEN"]])

# --- Top 20 campagnes les plus efficaces ---
st.subheader("Top 20 Campagnes les Plus Efficaces (Coût par Conversion)")
df_top = session.sql("""
    SELECT CAMPAIGN_ID, CAMPAIGN_NAME, CAMPAIGN_TYPE, PRODUCT_CATEGORY,
           TARGET_AUDIENCE, REGION, BUDGET, REACH, CONVERSION_RATE,
           REACH * CONVERSION_RATE AS CONVERSIONS_ESTIMEES,
           BUDGET / NULLIF(REACH * CONVERSION_RATE, 0) AS COUT_PAR_CONVERSION
    FROM ANYCOMPANY_LAB.SILVER.MARKETING_CAMPAIGNS_CLEAN
    ORDER BY COUT_PAR_CONVERSION ASC NULLS LAST
    LIMIT 20
""").to_pandas()
st.dataframe(df_top, use_container_width=True)

# --- Service client & Logistique ---
st.subheader("Service Client – Taux de Résolution par Catégorie")
df_service = session.sql("""
    SELECT ISSUE_CATEGORY,
           COUNT(*) AS NB_INTERACTIONS,
           AVG(CUSTOMER_SATISFACTION) AS SATISFACTION_MOYENNE,
           SUM(CASE WHEN RESOLUTION_STATUS = 'Resolved' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) AS TAUX_RESOLUTION
    FROM ANYCOMPANY_LAB.SILVER.CUSTOMER_SERVICE_INTERACTIONS_CLEAN
    GROUP BY 1 ORDER BY NB_INTERACTIONS DESC
""").to_pandas()
st.bar_chart(df_service.set_index("ISSUE_CATEGORY")[["TAUX_RESOLUTION", "SATISFACTION_MOYENNE"]])

st.subheader("Logistique – Ruptures de Stock")
df_rupture = session.sql("""
    SELECT PRODUCT_CATEGORY, REGION, COUNT(*) AS NB_RUPTURES
    FROM ANYCOMPANY_LAB.SILVER.INVENTORY_CLEAN
    WHERE CURRENT_STOCK <= REORDER_POINT
    GROUP BY 1, 2 ORDER BY NB_RUPTURES DESC
    LIMIT 20
""").to_pandas()
st.bar_chart(df_rupture.set_index("PRODUCT_CATEGORY")[["NB_RUPTURES"]])
st.dataframe(df_rupture, use_container_width=True)
