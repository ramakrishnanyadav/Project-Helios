# ☀️ Project Helios: The HealthKart Influencer ROI Hub

Welcome to Project Helios, an interactive dashboard built to track, analyze, and optimize influencer marketing campaigns for HealthKart. This tool moves beyond simple metrics to provide actionable insights on campaign performance, influencer effectiveness, and true incremental return on investment.

---

## 🚀 Live Demo

[**<< INSERT YOUR STREAMLIT COMMUNITY CLOUD LINK HERE >>**] 
*(You can deploy your app for free on Streamlit Community Cloud after pushing it to GitHub)*

---

## ✨ Core Features

*   **Executive KPI Dashboard:** At-a-glance view of total spend, attributed revenue, and both Simple and Incremental ROAS.
*   **Interactive Filtering:** Dynamically filter the entire dashboard by date range, influencer platform, and custom-defined influencer personas.
*   **Deep-Dive Analysis:** Dedicated page to visualize top and bottom performing influencers and compare the effectiveness of different personas (e.g., 'Micro-Fitness' vs. 'Macro-Nutrition').
*   **Data Explorer:** View and export the detailed, influencer-level performance data to CSV for further analysis.

---

## 🛠️ Tech Stack

*   **Language:** Python
*   **Libraries:** Streamlit, Pandas, Plotly Express, Faker
*   **Data:** Simulated with Python scripts to create a realistic, interconnected dataset.

---

## 🧠 Analytical Approach: Incremental ROAS

A key feature of this dashboard is the calculation of **Incremental ROAS**. 

*   **Simple ROAS** (`Attributed Revenue / Spend`) can be misleading because it doesn't account for sales that would have happened anyway.
*   **Incremental ROAS** (`(Attributed Revenue - Baseline Revenue) / Spend`) provides a truer picture of the campaign's financial impact by subtracting the expected "organic" baseline revenue from the sales attributed to influencers.

This project estimates the baseline by calculating the average daily revenue from non-influencer sources (`organic_search`, `direct`) and projecting it over the campaign period.

---

## ⚙️ Setup and Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [YOUR GITHUB REPO URL]
    cd project-helios
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run dashboard.py
    ```
---

## 📂 Project Structure