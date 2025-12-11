# **Advance Weather App – Cloudy**

A modern, feature-rich weather and news application.

---

## **Overview**

**Cloudy** is a smart desktop application built with Python that provides:

* Real-time weather updates
* Weather-based activity suggestions
* Latest Bangladesh news headlines
* Email delivery system for sending weather updates
* A clean, modern GUI built using **Tkinter** and **ttkbootstrap**

This project combines weather API data, AI-powered text generation, and email automation into one useful tool.

---

## **Technologies & Libraries Used**

The application uses the following Python packages:

```python
smtplib
requests
time
genai
MIMEMultipart
MIMEText
# GUI pkgs
tkinter
ttkbootstrap
```

---

## **✨ Features**

* 🌤️ **Live Weather Data**
  Fetches and displays real-time temperature, humidity, conditions, etc.

* 📰 **Bangladesh News Headlines**
  Shows the latest top news headlines.

* ✉️ **Automated Email System**
  Sends weather and news summaries to your email.

* 🤖 **AI Activity Suggestions**
  Uses Google GenAI to generate weather-based suggestions.

* 🖥️ **Modern GUI**
  Built using **Tkinter** + **ttkbootstrap** for a sleek, modern interface.

---

## **🚀 Getting Started**

### **1️⃣ Clone the Repository**

```bash
https://github.com/tihamsheikh/Advance-Weather-app.git
cd Advance-Weather-App
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

> Note: `smtplib`, `tkinter`, and email MIME libraries come pre-installed with Python.

### **3️⃣ Add Your API Keys (Required)**

Create a file named **KEYS.py** or create an **.env**:

```python
WEATHER_API = "your_api_key_here"
NEWS_API = "your_api_key_here"
GOOGLE_API = "your_genai_api_key_here"
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"
```

## **📜 License**

MIT License



