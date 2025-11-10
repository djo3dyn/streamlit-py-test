import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# Global variable to hold latest MQTT data
latest_data = {}

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    client.subscribe("sensor/flow_energy/data")

def on_message(client, userdata, msg):
    global latest_data
    try:
        latest_data = json.loads(msg.payload.decode())
    except Exception as e:
        print(f"Error decoding MQTT message: {e}")

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

# Streamlit UI
st.set_page_config(page_title="Flow & Power Dashboard", layout="wide")
st.title("🔌 Flow & Power Monitoring Dashboard")

placeholder = st.empty()

while True:
    with placeholder.container():
        if latest_data:
            st.markdown(f"**Timestamp:** {latest_data.get('timestamp', 'N/A')}")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💧 Flow Data")
                flow = latest_data.get("flow", {})
                st.metric("Flow (L/min)", flow.get("flow_lpm", 0))
                st.metric("Total Liters", round(flow.get("total_liters", 0), 2))

            with col2:
                st.subheader("⚡ Power Data")
                power = latest_data.get("power", {})
                for key, value in power.items():
                    st.write(f"**{key.replace('_', ' ').title()}**: {value}")
        else:
            st.info("Waiting for MQTT data...")

    time.sleep(1)