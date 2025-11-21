# NoSQL

# 📈 IoT Data Science Project: Real-Time Monitoring and Analysis
This project establishes a complete Internet of Things (IoT) data flow using an ESP32 microcontroller, AWS IoT Core (MQTT), and a MongoDB Atlas NoSQL database for real-time storage and subsequent analysis using Python and the Dash Web App.

## 🚀 Project Overview

The system uses an **ESP32** to gather sensor data, publishes it to a cloud MQTT broker, and stores it in **MongoDB Atlas**. A **Dash Web Application** is used for real-time visualization and data analysis.

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Hardware** | ESP32, DHT11 Sensor, LCD Display | Data acquisition and local display. |
| **Messaging** | AWS IoT Core | Managed **MQTT Broker** for scalable data ingestion. |
| **Database** | MongoDB Atlas (NoSQL) | Persistent storage for time-series sensor data. |
| **Visualization** | Dash (Python/Plotly) | Retrieves and plots data for dashboards. |

---

## 🌊 Data Flow Pipeline

The data follows a six-step journey from the sensor to the visualization layer.

1.  **Sensor Data:** **DHT11** collects readings.
2.  **Publishing:** **ESP32** reads data and publishes it via **MQTT** to **AWS IoT Core**.
3.  **Local Feedback:** **ESP32** simultaneously displays data on the **LCD Display**.
4.  **Persistence:** AWS IoT Core routes the data to **MongoDB Atlas** for storage.
5.  **Retrieval:** **Dash Web App** queries MongoDB Atlas using a data retrieval API.
6.  **Visualization:** Dash plots real-time and historical graphs.



---

## 💾 Database Details (MongoDB Atlas)

| Attribute | Value | Note |
| :--- | :--- | :--- |
| **Database Name** | `add232iotdb` | |
| **Collection Name** | `humidity` | Stores all sensor documents. |
| **Indexed Fields** | `time` (Single), `temperature` and `humidity` (Compound) | Optimized for faster time-series querying and complex filtering. |

### Document Structure Example

```json
{
  "_id": ObjectId("..."),
  "humidity": 75.81,
  "temperature": 29.66,
  "time": "12:45:18" 
}
