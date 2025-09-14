Stock Analysis & Prediction Dashboard 📈

🚀 [View the Live Application Here!](https://stock-analysis-and-prediction-apooorv19.streamlit.app)

![CAPM Page](https://github.com/apooorv19/stock-analysis-and-prediction/blob/main/CAPM%20Page.png?raw=true)

![Stock Analysis Page](https://github.com/apooorv19/stock-analysis-and-prediction/blob/main/Stock%20Analysis%20Page.png?raw=true)

![Stock Analysis Visualization Page](https://github.com/apooorv19/stock-analysis-and-prediction/blob/main/Stock%20Analysis%20Visulaization%20Page.png?raw=true)

![Stock Prediction Page](https://github.com/apooorv19/stock-analysis-and-prediction/blob/main/Stock%20Prediction%20Page.png?raw=true)

What Can You Do With This App?

I've split the app into three simple tools:

1. 📊 Stock Analysis 

2. 🔮 Stock Prediction

3. 💹 CAPM Analysis

📂 Project Structure

The project is organized in a modular way that is easy to understand and maintain. This is the standard structure for a multi-page Streamlit application.

trading-app/
│
├── Trading_App.py              # The main homepage of the app
├── requirements.txt            # A list of all necessary Python libraries
│
└── pages/                      # This folder holds all the other app pages
    ├── 1_Stock_Analysis.py     # Code for the "Report Card" page
    ├── 2_Stock_Prediction.py   # Code for the "Forecast" page
    ├── 3_CAPM_Analysis.py      # Code for the "Risk vs. Reward" page
    │
    └── utils/                  # A folder for helper functions
        ├── __init__.py         # Makes 'utils' a Python package
        ├── capm_logic.py       # Functions for CAPM calculations
        ├── model_train.py      # Logic for the forecasting model
        └── plotly_figure.py    # Functions that create the charts


For Developers: How to Run This on Your Computer

If you're a fellow coder and want to run this project yourself, here’s how:
1. Download the Code

This command copies all the project files to your machine.

git clone [https://github.com/apooorv19/Stock-Analysis-and-Prediction.git](https://github.com/apooorv19/Stock-Analysis-and-Prediction.git)

cd Stock-Analysis-and-Prediction

2. Install the Required Tools

This single command installs all the libraries the project needs to work.

pip install -r requirements.txt

3. Run the App

This command will start the application on your computer.

streamlit run Trading_App.py

Disclaimer: This is an educational project created to showcase programming and data analysis skills. The information and predictions provided are not financial advice.
