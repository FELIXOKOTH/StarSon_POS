
# Apillo AI API Documentation

Welcome to the official API documentation for the Apillo AI, an embeddable engine for Environmental, Social, and Governance (ESG) analytics.

## Overview

The Apillo API provides a simple way to get powerful sustainability insights from your business's operational data. By processing a list of daily transactions, Apillo can calculate key environmental and social impact metrics and provide intelligent, actionable recommendations.

This document details the available endpoints, the expected data formats, and the structure of the returned responses.

---

## Endpoints

### 1. ESG Impact Report

- **URL:** `/apillo/esg_report`
- **Method:** `GET`
- **Description:** This is the core endpoint for getting a full ESG analysis. It requires no input body, as it reads transaction data that has been accumulated in the backend server.

#### Response Body

The endpoint returns a JSON object containing three main sections: `environmental_impact`, `social_impact`, and `sustainability_insight`.

**Example Response:**

```json
{
  "environmental_impact": {
    "digital_receipts": 15,
    "estimated_carbon_reduction_kg": 0.0225,
    "trees_saved_estimate": 0.0015,
    "waste_diverted_kg": 0.0225,
    "water_saved_liters": 0.75
  },
  "social_impact": {
    "community_give_back_kes": 1.0,
    "program_description": "Donating KES 1.0 to local charities for every 10 paperless transactions."
  },
  "sustainability_insight": {
    "esg_insight": "The reduction of 0.0225 kg of CO2e and saving 0.75 liters of water are significant steps. The community donation of KES 1.00 also strengthens social bonds. To improve further, consider sourcing from local suppliers to reduce supply chain emissions."
  }
}
```

#### Field Descriptions

| Key                               | Type    | Description                                                                                                |
|-----------------------------------|---------|------------------------------------------------------------------------------------------------------------|
| `digital_receipts`                | Integer | The total number of transactions that did not generate a paper receipt.                                    |
| `estimated_carbon_reduction_kg`   | Float   | The estimated kilograms of CO2 equivalent emissions avoided by not printing receipts.                      |
| `trees_saved_estimate`            | Float   | An estimation of the fraction of trees saved, based on paper production metrics.                           |
| `waste_diverted_kg`               | Float   | The estimated weight of paper waste (in kg) that was diverted from landfills.                            |
| `water_saved_liters`              | Float   | The estimated volume of water (in Liters) saved by avoiding paper production for receipts.                 |
| `community_give_back_kes`         | Float   | The total amount (in KES) donated to a local charity as part of a defined social program.                  |
| `program_description`             | String  | A brief explanation of the social initiative driving the community give-back.                              |
| `esg_insight`                     | String  | A brief, actionable recommendation from the Apillo AI to help improve overall sustainability performance.    |

---

### 2. Daily Business Summary

- **URL:** `/apillo/daily_summary`
- **Method:** `GET`
- **Description:** Provides a combined business and eco-report for a POS dashboard. It is a lighter, more operational-focused summary.

#### Response Body

**Example Response:**

```json
{
    "summary_title": "Apillo's End-of-Day Business Summary",
    "key_metric": "Total Sales: KES 3000.00 from 2 transactions.",
    "actionable_insight": "Today's peak activity was around 14:00. The 2 digital receipts are a great sustainability achievement!",
    "raw_data": {
        "report_date": "2024-05-20",
        "total_sales": 3000.0,
        "transaction_count": 2,
        "payment_methods": {
            "safaricom_mpesa": 2
        },
        "sales_by_hour": {
            "00": 0, "01": 0, ... , "14": 2, ... , "23": 0
        },
        "digital_receipts": 2,
        "eco_metrics": {
            "digital_receipts_issued": 2,
            "trees_saved": 0.0002
        }
    }
}
```
