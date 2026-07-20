# Live Demo Script

## Before presenting
- Run `docker compose up --build`.
- Register the first account so it receives Admin access.
- Keep browser zoom at 90–100%.
- Open the app and API docs in separate tabs.

## 90-second demo
**0–10 sec:** “This is PulsePredict, an explainable heart-risk screening platform.”

**10–25 sec:** Show registration/login and mention secure JWT accounts and encrypted passwords.

**25–45 sec:** Open Assessment, click **Use demo data**, then **Calculate risk**.

**45–65 sec:** “The system does not only give a percentage. It shows the factors that pushed the result up or down, making the model easier to understand and act on.”

**65–78 sec:** Open **Model Lab**. “We compare multiple models and expose Accuracy, Recall, F1 and AUC rather than hiding model quality.”

**78–90 sec:** Open Admin or print the report. “The architecture is ready for validated clinical datasets, PostgreSQL, and deployment.”

## Backup plan
If the API is unavailable, show the frontend and explain the complete architecture using README. Keep screenshots of the result and Model Lab on your laptop.
