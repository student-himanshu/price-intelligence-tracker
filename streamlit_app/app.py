"""Streamlit dashboard for the Price Intelligence Tracker."""
import requests
import streamlit as st
API_BASE_URL = "http://127.0.0.1:8000"
def api_get(path: str) -> dict | list:
    """Send a GET request to the FastAPI backend."""
    response = requests.get(
        f"{API_BASE_URL}{path}",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
def api_post(path: str, params: dict) -> dict:
    """Send a POST request to the FastAPI backend."""
    response = requests.post(
        f"{API_BASE_URL}{path}",
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
def api_delete(path: str) -> dict:
    """Send a DELETE request to the FastAPI backend."""
    response = requests.delete(
        f"{API_BASE_URL}{path}",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
@st.cache_data(ttl=30)
def get_products() -> list[dict]:
    """Fetch all products."""
    data = api_get("/products")
    if isinstance(data, dict) and "value" in data:
        return data["value"]
    if isinstance(data, list):
        return data
    return []
@st.cache_data(ttl=30)
def get_comparison(product_id: int) -> dict:
    """Fetch seller comparison."""
    data = api_get(
        f"/analytics/products/{product_id}/comparison",
    )
    if not isinstance(data, dict):
        raise ValueError("Invalid comparison response.")
    return data
@st.cache_data(ttl=30)
def get_history(product_id: int) -> dict:
    """Fetch product price history."""
    data = api_get(
        f"/analytics/products/{product_id}/history",
    )
    if not isinstance(data, dict):
        raise ValueError("Invalid price history response.")
    return data
@st.cache_data(ttl=30)
def get_forecast(product_id: int) -> dict:
    """Fetch product forecast."""
    data = api_get(
        f"/forecast/{product_id}",
    )
    if not isinstance(data, dict):
        raise ValueError("Invalid forecast response.")
    return data
@st.cache_data(ttl=10)
def get_alerts(product_id: int) -> list[dict]:
    """Fetch price alerts for a product."""
    data = api_get(
        f"/price-alerts/{product_id}",
    )
    if isinstance(data, dict) and "value" in data:
        return data["value"]
    if isinstance(data, list):
        return data
    raise ValueError("Invalid price alert response.")
st.set_page_config(
    page_title="Price Intelligence Tracker",
    page_icon="💰",
    layout="wide",
)
st.title("💰 Price Intelligence Tracker")
st.markdown(
    """
    Track product prices, compare sellers, analyze price history,
    view forecasts, and monitor price alerts.
    """
)
st.divider()
try:
    products = get_products()
    if not products:
        st.warning("No products found.")
        st.stop()
    product_options = {
        f'{product["id"]} — {product["normalized_name"]}': product
        for product in products
    }
    selected_label = st.selectbox(
        "Select Product",
        list(product_options.keys()),
    )
    product = product_options[selected_label]
    product_id = product["id"]
    st.subheader(product["normalized_name"])
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.metric("Product ID", product_id)
    with info_col2:
        st.metric(
            "Brand",
            product.get("brand") or "N/A",
        )
    with info_col3:
        st.metric(
            "Category",
            product.get("category") or "N/A",
        )
    st.divider()
    # Seller comparison
    comparison = get_comparison(product_id)
    st.subheader("💰 Seller Comparison")
    comparison_col1, comparison_col2 = st.columns(2)
    with comparison_col1:
        st.metric(
            "Lowest Price",
            comparison.get("lowest_price", "N/A"),
        )
    with comparison_col2:
        st.metric(
            "Seller Count",
            comparison.get("seller_count", 0),
        )
    best_deal = comparison.get("best_deal")
    if best_deal:
        st.success(
            f'🏆 Best Deal: {best_deal["seller_name"]} — '
            f'{best_deal["price"]}'
        )
    listings = comparison.get("listings", [])
    if listings:
        st.dataframe(
            listings,
            width="stretch",
            hide_index=True,
        )
    st.divider()
    # Price history
    history_data = get_history(product_id)
    history = history_data.get("history", [])
    st.subheader("📈 Price History")
    if history:
        chart_rows = [
            {
                "Date": item["collected_at"],
                "Seller": item["seller_name"],
                "Price": float(item["price"]),
            }
            for item in history
        ]
        st.line_chart(
            chart_rows,
            x="Date",
            y="Price",
            color="Seller",
        )
        st.dataframe(
            chart_rows,
            width="stretch",
            hide_index=True,
        )
        st.caption(
            f'{history_data.get("observation_count", len(history))} '
            "price observations"
        )
    else:
        st.info("No price history available.")
    st.divider()
    # Forecast
    forecast = get_forecast(product_id)
    st.subheader("🔮 Price Forecast")
    forecast_col1, forecast_col2, forecast_col3 = st.columns(3)
    with forecast_col1:
        st.metric(
            "Current Price",
            forecast.get("current_price", "N/A"),
        )
    with forecast_col2:
        st.metric(
            "Forecast Price",
            forecast.get("forecast_price", "N/A"),
        )
    with forecast_col3:
        trend = forecast.get("trend", "N/A")
        st.metric(
            "Trend",
            trend.replace("_", " ").title(),
        )
    explanation = forecast.get("explanation")
    if explanation:
        st.info(f"🤖 {explanation}")
    st.divider()
    # Price alerts
    st.subheader("🔔 Price Alerts")
    alert_col1, alert_col2 = st.columns([2, 1])
    with alert_col1:
        target_price = st.number_input(
            "Target Price (INR)",
            min_value=0.01,
            step=100.00,
            format="%.2f",
        )
    with alert_col2:
        st.write("")
        st.write("")
        create_alert = st.button(
            "🔔 Create Alert",
            width="stretch",
        )
    if create_alert:
        if target_price <= 0:
            st.error(
                "Target price must be greater than zero."
            )
        else:
            try:
                alert = api_post(
                    f"/price-alerts/{product_id}",
                    {"target_price": target_price},
                )
                get_alerts.clear()
                st.success(
                    f'Price alert created for INR '
                    f'{float(alert["target_price"]):.2f}.'
                )
                st.rerun()
            except requests.RequestException as exc:
                st.error(
                    f"Unable to create price alert: {exc}"
                )
    alerts = get_alerts(product_id)
    if alerts:
        st.write("### Active & Previous Alerts")
        for alert in alerts:
            alert_id = alert["id"]
            alert_price = float(alert["target_price"])
            is_active = alert["is_active"]
            triggered_at = alert.get("triggered_at")
            alert_col1, alert_col2, alert_col3 = st.columns(
                [2, 2, 1]
            )
            with alert_col1:
                st.write(
                    f"**Target:** INR {alert_price:.2f}"
                )
            with alert_col2:
                if is_active:
                    st.success("🟢 Active")
                elif triggered_at:
                    st.error("🔴 Triggered")
                else:
                    st.caption("⚪ Inactive")
            with alert_col3:
                if is_active:
                    if st.button(
                        "Deactivate",
                        key=f"deactivate_{alert_id}",
                    ):
                        try:
                            api_delete(
                                f"/price-alerts/{alert_id}"
                            )
                            get_alerts.clear()
                            st.success(
                                "Alert deactivated."
                            )
                            st.rerun()
                        except requests.RequestException as exc:
                            st.error(
                                f"Unable to deactivate alert: {exc}"
                            )
            st.caption(
                f'Created: {alert["created_at"]}'
            )
            if triggered_at:
                st.caption(
                    f"⚡ Triggered: {triggered_at}"
                )
    else:
        st.info(
            "No price alerts have been created for this product."
        )
except requests.RequestException as exc:
    st.error(
        "Unable to connect to the FastAPI backend."
    )
    st.caption(str(exc))
except (KeyError, TypeError, ValueError) as exc:
    st.error(f"Invalid API response: {exc}")
