# Data Dictionary

This document defines the schemas, units, and constraints for the raw data layers in the `tourism_weather_dw` database.

---

## 1. Weather Data (`raw.weather_daily`)

**Source:** Open-Meteo Historical Weather API (ERA5)
**Timezone:** `Asia/Phnom_Penh` (GMT+7). **Note:** The API calculates daily aggregations (e.g., daily max, daily sum) based on local Cambodian time (midnight to midnight), not UTC.

| Column | Data Type | Unit | Description |
|---|---|---|---|
| `city` | TEXT | N/A | Name of the city (e.g., 'Phnom Penh'). |
| `time` | TEXT | YYYY-MM-DD | The local calendar date. |
| `temperature_2m_mean` | TEXT | °C (Celsius) | Mean air temperature at 2 meters above ground. |
| `precipitation_sum` | TEXT | mm (Millimeters) | Total precipitation (rain, showers, snow) during the day. |
| `relative_humidity_2m_mean` | TEXT | % (Percentage) | Mean relative humidity at 2 meters. Range: 0 to 100. |
| `wind_speed_10m_max` | TEXT | km/h (Kilometers per hour) | Maximum wind speed at 10 meters above ground. |

---

## 2. Tourism Data (`raw.tourism_monthly`)

**Source:** Ministry of Tourism (MOT) via MEF Open Data API
**Timezone:** N/A (Aggregated by calendar month)

| Column | Data Type | Unit | Description |
|---|---|---|---|
| `year` | TEXT | YYYY | Calendar year. |
| `months` | TEXT | Jan-Dec | Three-letter abbreviation of the month. |
| `number_of_tourists` | TEXT | Persons | Total international tourist arrivals. |

---

## 3. Exchange Rate Data (`raw.exchange_rate_daily`)

**Source:** National Bank of Cambodia (NBC) via MEF Open Data CSV
**Timezone:** N/A (Daily records)

| Column | Data Type | Unit | Description |
|---|---|---|---|
| `date` | TEXT | YYYY-MM-DD | The date of the exchange rate. |
| `purchase` | TEXT | KHR | The rate at which banks buy USD. |
| `sale` | TEXT | KHR | The rate at which banks sell USD. |
| `midpoint` | TEXT | KHR | The average of purchase and sale. |
| `exchange_rate` | TEXT | KHR | Official NBC reference rate. |
| `spread_...` | TEXT | % | The percentage spread between the market and official rate. |