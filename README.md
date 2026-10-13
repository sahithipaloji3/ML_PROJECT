# AttritionIQ — Step 3 Employee Directory + Profile

This project is the UI/Flask stage of the B.Tech Employee Attrition Analysis website.

## Current features
- HR and Manager login only
- Professional dashboard UI
- Employee directory with search and filters
- Employee profile page for demo records
- HR organization-wide sample view and Manager restricted demo scope
- Prediction Studio with employee-context review and model-readiness checklist
- Workforce analytics calculated from the clearly labelled fictional sample records
- Honest unavailable states for attrition results and model metrics until real data/model exist
- Clear DEMO DATA labeling
- Dashboard and employee pages are connected to the Flask app

## Important
Employee details are fictional UI examples, not IBM dataset records. The descriptive sample counts on Analytics are computed from those ten records; they are not attrition analysis. The Manager role currently sees a six-record demo subset because team assignments have not been configured. This demonstrates restricted access but is not a real manager/team mapping. Prediction Studio does not generate a risk score, and model metrics remain unavailable until the real dataset is supplied and a model is trained and evaluated.

Later stages will connect:
1. IBM HR Analytics dataset
2. Data preprocessing
3. Logistic Regression
4. Random Forest
5. Real evaluation metrics
6. Prediction Studio
7. SHAP explanations
8. CSV import and validation workflow

## Run
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Deploy on Render
This Flask application cannot run on GitHub Pages. It can be deployed as a web service on Render using the `render.yaml` Blueprint in this repository:
1. Sign in to Render and choose **New +** → **Blueprint**.
2. Connect the `sahithipaloji3/ML_PROJECT` GitHub repository and deploy the Blueprint.
3. Render installs the requirements, starts the app with Gunicorn, and generates `FLASK_SECRET_KEY`.
4. Open the service URL Render provides.

Future pushes to the `main` branch will trigger redeployments. The login accounts and employee records are hard-coded demo data; do not use real employee or confidential information in this deployment.

## Demo login
HR:
- Email: hr@attritioniq.com
- Password: hr123

Manager:
- Email: manager@attritioniq.com
- Password: manager123

## Notes
- The hard-coded demo accounts are for local development only.
- Production authentication should use secure password hashing and a stronger secret management approach.
- The employee directory and profile pages are a starter UI layer before the real ML pipeline is connected.
