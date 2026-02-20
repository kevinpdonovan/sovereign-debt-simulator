import streamlit as st
import random

st.set_page_config(page_title="Sovereign Debt Simulator", layout="wide")

# ---------------------------
# INITIALIZE GAME STATE
# ---------------------------

if "initialized" not in st.session_state:
    st.session_state.year = 2008
    st.session_state.turn = 1
    st.session_state.gdp = 100.0
    st.session_state.external_debt = 40.0
    st.session_state.fx_reserves = 20.0
    st.session_state.exchange_rate = 5.0
    st.session_state.inflation = 8.0
    st.session_state.commodity_price = 100.0
    st.session_state.public_approval = 60.0
    st.session_state.history = []
    st.session_state.initialized = True


# ---------------------------
# TITLE
# ---------------------------

st.title("Sovereign Debt Simulator")
st.subheader("Commodity Exporter Model (Zambia-Style Structure)")


# ---------------------------
# DISPLAY DASHBOARD
# ---------------------------

col1, col2, col3 = st.columns(3)

col1.metric("GDP", round(st.session_state.gdp, 2))
col1.metric("External Debt", round(st.session_state.external_debt, 2))

col2.metric("FX Reserves", round(st.session_state.fx_reserves, 2))
col2.metric("Exchange Rate (LC per USD)", round(st.session_state.exchange_rate, 2))

col3.metric("Inflation (%)", round(st.session_state.inflation, 2))
col3.metric("Public Approval", round(st.session_state.public_approval, 2))

st.write(f"**Year:** {st.session_state.year}")
st.write(f"**Turn:** {st.session_state.turn} of 8")
st.write(f"**Commodity Price Index:** {st.session_state.commodity_price}")

st.divider()


# ---------------------------
# SHOCK ENGINE
# ---------------------------

def apply_commodity_shock():
    shock = random.choice([-20, -10, 0, 10, 20])
    st.session_state.commodity_price += shock

    if shock < 0:
        st.session_state.fx_reserves -= 5
        st.session_state.gdp -= 5
        st.session_state.exchange_rate *= 1.15
        st.session_state.inflation += 3
        st.session_state.public_approval -= 4
    elif shock > 0:
        st.session_state.fx_reserves += 5
        st.session_state.gdp += 5
        st.session_state.exchange_rate *= 0.95
        st.session_state.inflation -= 1
        st.session_state.public_approval += 2

    return shock


# ---------------------------
# POLICY CHOICE
# ---------------------------

st.subheader("Policy Decision")

policy = st.radio(
    "Choose your policy response:",
    (
        "Borrow $10 externally",
        "Cut spending (Austerity)",
        "Do nothing",
    ),
)

if st.button("End Turn"):

    shock = apply_commodity_shock()

    if policy == "Borrow $10 externally":
        st.session_state.external_debt += 10
        st.session_state.fx_reserves += 10
        st.session_state.public_approval += 2

    elif policy == "Cut spending (Austerity)":
        st.session_state.gdp -= 3
        st.session_state.public_approval -= 6
        st.session_state.external_debt -= 2

    # Debt servicing rule (10% of external debt per turn)
    debt_service = st.session_state.external_debt * 0.10
    st.session_state.fx_reserves -= debt_service

    # Record history
    st.session_state.history.append({
        "year": st.session_state.year,
        "debt": st.session_state.external_debt,
        "gdp": st.session_state.gdp
    })

    # Default condition
    if st.session_state.fx_reserves <= 0:
        st.error("DEFAULT! The country has run out of foreign reserves.")
        st.stop()

    # Advance time
    st.session_state.year += 2
    st.session_state.turn += 1

    st.success(f"Commodity shock this turn: {shock}")

    if st.session_state.turn > 8:
        st.success("Simulation Complete!")
        st.stop()


# ---------------------------
# RESET BUTTON
# ---------------------------

if st.button("Reset Game"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()