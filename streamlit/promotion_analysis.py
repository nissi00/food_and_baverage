import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Analyse Promotions", layout="wide")
st.title("🎯 AnyCompany – Analyse de l'Impact des Promotions")

# --- Vue d'ensemble ---
st.subheader("Vue d'ensemble des promotions")
df_overview = session.sql("""
    SELECT PRODUCT_CATEGORY, PROMOTION_TYPE,
           COUNT(*) AS NB_PROMOTIONS,
           AVG(DISCOUNT_PERCENTAGE) AS DISCOUNT_MOYEN,
           AVG(DATEDIFF('DAY', START_DATE, END_DATE)) AS DUREE_MOYENNE
    FROM ANYCOMPANY_LAB.SILVER.PROMOTIONS_CLEAN
    GROUP BY 1, 2 ORDER BY NB_PROMOTIONS DESC
""").to_pandas()
st.dataframe(df_overview, use_container_width=True)

# --- Avec / sans promotion ---
st.subheader("Ventes avec vs sans promotion")
df_promo = session.sql("""
    SELECT PENDANT_PROMO,
           COUNT(*) AS NB_TRANSACTIONS,
           SUM(AMOUNT) AS TOTAL_VENTES,
           AVG(AMOUNT) AS PANIER_MOYEN
    FROM ANYCOMPANY_LAB.ANALYTICS.VENTES_ENRICHIES
    WHERE TRANSACTION_TYPE = 'Sale'
    GROUP BY 1
""").to_pandas()
df_promo["PENDANT_PROMO"] = df_promo["PENDANT_PROMO"].map({True: "Avec promo", False: "Sans promo"})

col1, col2 = st.columns(2)
with col1:
    st.bar_chart(df_promo.set_index("PENDANT_PROMO")[["TOTAL_VENTES"]])
with col2:
    st.bar_chart(df_promo.set_index("PENDANT_PROMO")[["PANIER_MOYEN"]])
st.dataframe(df_promo, use_container_width=True)

# --- Promotions par région ---
st.subheader("Promotions par Région")
df_region = session.sql("""
    SELECT REGION, COUNT(*) AS NB_PROMOTIONS, AVG(DISCOUNT_PERCENTAGE) AS DISCOUNT_MOYEN
    FROM ANYCOMPANY_LAB.SILVER.PROMOTIONS_CLEAN
    GROUP BY 1 ORDER BY NB_PROMOTIONS DESC
""").to_pandas()
st.bar_chart(df_region.set_index("REGION")[["NB_PROMOTIONS"]])

# --- Promotions actives enrichies ---
st.subheader("Promotions avec campagnes associées")
df_actives = session.sql("""
    SELECT PROMOTION_ID, PRODUCT_CATEGORY, PROMOTION_TYPE, DISCOUNT_PERCENTAGE,
           REGION, DUREE_PROMO_JOURS, NB_CAMPAGNES_ASSOCIEES, BUDGET_CAMPAGNES_TOTAL
    FROM ANYCOMPANY_LAB.ANALYTICS.PROMOTIONS_ACTIVES
    ORDER BY NB_CAMPAGNES_ASSOCIEES DESC
    LIMIT 30
""").to_pandas()
st.dataframe(df_actives, use_container_width=True)

# --- Distribution temporelle ---
st.subheader("Distribution temporelle des promotions")
df_time = session.sql("""
    SELECT YEAR(START_DATE) AS ANNEE, COUNT(*) AS NB_PROMOTIONS
    FROM ANYCOMPANY_LAB.SILVER.PROMOTIONS_CLEAN
    GROUP BY 1 ORDER BY 1
""").to_pandas()
st.bar_chart(df_time.set_index("ANNEE")[["NB_PROMOTIONS"]])
