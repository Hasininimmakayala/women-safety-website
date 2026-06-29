# 🛡️ StreeTranam — AI-Powered Women's Safety Platform

StreeTranam is a personal safety web app designed to help users stay protected during travel, share their live status with trusted contacts, and respond quickly in emergencies.

## ✨ Features

- **Guardian Mode** — Share live location and trip status with trusted contacts ("Guardians") in real time
- **Trip Safety Analyzer** — Start a trip with origin/destination, track travel mode, and send periodic check-ins
- **Emergency SOS** — One-tap SOS button to alert guardians and trigger emergency support
- **Safety Map** — Visual map view of current location and route using Folium
- **Incident Reporting** — Log and categorize incidents by severity (low/medium/high)
- **Safety Score Dashboard** — At-a-glance metrics: safety score, active guardians, check-ins, guardian mode status
- **Emergency Helplines** — Quick access to Police, Ambulance, Women's Helpline, and Emergency numbers

## 🧰 Tech Stack

- **Frontend/App Framework:** [Streamlit](https://streamlit.io/)
- **Data Handling:** Pandas, NumPy
- **Maps & Location:** Folium, streamlit-folium
- **Machine Learning:** scikit-learn (KMeans clustering — used for safety zone/route analysis)
- **Database:** MySQL (via mysql-connector-python)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MySQL server running locally (or update connection details to point to your own instance)

### Installation

```bash
git clone https://github.com/Hasininimmakayala/women-safety-website.git
cd women-safety-website
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure

```
women-safety-website/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

## 🔮 Future Improvements

- Real GPS integration (currently uses placeholder/simulated location data)
- Push notifications/SMS alerts to guardians via Twilio or similar
- User authentication and persistent accounts
- Mobile-responsive layout / PWA support

## 👩‍💻 Author

**Hasini Nimmakayala**
[LinkedIn](https://www.linkedin.com/in/hasini-nimmakayala-305293397/) · [GitHub](https://github.com/Hasininimmakayala)
