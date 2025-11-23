Global Air Quality Analysis (全球空气质量分析)
(一) Project Overview (项目概览)This is a data storytelling project built with Streamlit, aiming to analyze global air quality trends, identify pollution hotspots, and explore meteorological impacts using machine learning.Target Audience: Policy makers, Environmental researchers, and General public.
（二） Team & Supervisors (团队与指导教师)
Student: Wangbeinuo (beinuo.wang@efrei.net)
Supervisor: Mano Joseph Mathew (mano.mathew@efrei.fr)
Institution: EFREI Paris / WUT
（三）Features (功能特色)Interactive Dashboard: 
Real-time filtering by country and date.
Deep Dive Analysis: Correlation heatmaps and bubble charts for weather impact.
AI Prediction Simulator: A Random Forest model to predict PM2.5 levels based on user inputs.
Professional UI: Dark-themed sidebar with institutional branding.
（四）Installation & Setup (安装与运行)
Clone the repositorygit clone 
cd YOUR_REPO_NAME
Install dependenciespip install -r requirements.txt
Run the applicationstreamlit run app.py
（五）Project Structure.
├── app.py                  # Main entry point
├── sections/               # Page logic (Intro, Overview, Deep Dives, ML, Conclusions)
├── utils/                  # Helper functions (Data IO, Preprocessing, Visualization)
├── data/                   # Dataset folder
├── assets/                 # Logos and images
└── requirements.txt        # Python dependencies
（六）Data SourceDataset: Global Air Quality DatasetLicense: Open Dat.