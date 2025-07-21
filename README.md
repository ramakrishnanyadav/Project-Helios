# ☀️ Project Helios: Your Smart Hub for HealthKart Influencer Campaigns

Hey there! Welcome to Project Helios. Think of this as a special dashboard I built for HealthKart to really understand how well our influencer campaigns are doing. Instead of just looking at basic numbers, Helios helps us dig deeper to see the *real* impact of every campaign and every influencer.

This project was my take on the HealthKart intern assignment, and it was a fantastic journey in building a complete data tool from scratch – from making up realistic data to getting it all live for you to explore!

---

## 🚀 Take It For A Spin!

Go ahead, click here and see Helios in action:

https://project-helios-5lvpp8xmb2aasrxmxappjjt.streamlit.app/

---

## ✨ What Helios Can Do For You

Helios isn't just a bunch of charts; it's designed to give you clear answers:

*   **Quick Health Check (Executive Summary):** Get a super fast overview of how much we're spending, how much money influencers are bringing in, and the all-important **Incremental ROAS** – that's the real profit after subtracting what we would've made anyway!
*   **Smart Filters:** Want to see how Instagram influencers are performing with "Macro-Fitness" personas last month? Just pick your filters on the side, and the whole dashboard updates instantly. Easy peasy!
*   **Who Are Our Stars (And Who Needs a Boost)?** Dive into a dedicated section to see which individual influencers are crushing it, and which types of influencers (like "Micro-Nutrition" vs. "Macro-Lifestyle") are giving us the best bang for our buck.
*   **Get All The Details (Data Explorer):** Need to download the raw numbers for your own reports? Head over to the Data Explorer page, filter what you need, and grab a CSV file with all the juicy details.
*   **Clean & Easy Navigation:** It's all neatly organized into different pages, so you can jump straight to the insights you need without getting lost.

---

## 💡 The Brains Behind the Numbers: Incremental ROAS

You know how sometimes a campaign looks good on paper, but you're not sure if it actually brought in *new* business? That's where **Incremental ROAS** comes in.

Instead of just dividing total revenue by our spending, Helios takes it a step further:
*   We figure out how much money HealthKart would normally make (our "baseline").
*   Then, we only count the revenue that came *above and beyond* that normal amount, specifically thanks to our influencers.
*   This gives us the **true profit** from our influencer efforts, helping us spend smarter next time!

---

### ☁️ My Adventure with Cloud Data (Snowflake)

I initially pushed myself to build Helios to connect directly to a powerful cloud data warehouse called **Snowflake**. This is how big companies handle their data – it's super secure and scalable!

Here's what that journey involved:
*   **Setting up a whole database** in the cloud just for HealthKart's influencer data.
*   **Building a secure connection** between the app and Snowflake, managing passwords and access behind the scenes (like a digital bouncer!).
*   **Writing the code** to pull all the live campaign data directly from Snowflake.

It was an incredible learning experience in building real-world data pipelines! While I encountered a unique connection challenge during final deployment that was specific to the cloud platform, the good news is that the app is fully designed for it, and it ultimately pushed me to master advanced debugging and problem-solving.

To ensure you have a perfectly working demo to explore today, this live version fetches data from CSV files stored right in the project. But rest assured, the code is ready for Snowflake whenever needed!

---

## 🚀 How to Get Helios Running on Your Computer

Want to peek under the hood? It's easy to get Helios running locally:

1.  **Grab the Code:**
    ```bash
    git clone https://github.com/ramakrishnanyadav/Project-Helios
    cd project-helios
    ```
2.  **Set Up Your Lab (Virtual Environment):**
    ```bash
    python -m venv venv
    # If you're on Windows:
    .\venv\Scripts\activate
    # If you're on Mac/Linux:
    source venv/bin/activate
    ```
3.  **Install the Tools:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Launch the Dashboard!**
    ```bash
    streamlit run dashboard.py
    ```
    Your web browser should magically open up to Helios!

---

## 📂 Peeking Inside the Project

Here's a quick map of how everything is organized:
