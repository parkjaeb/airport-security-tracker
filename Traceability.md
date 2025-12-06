📘 Project Traceability Log

Airport Security Tracker — Development History (v0.1)

This document records every development step taken so far.

⸻

🟦 1. Project Initialization

1.1 Created local project folder

A new folder named airport-security-tracker was created on the local machine to host the project files.

1.2 Developed frontend prototype

Created an index.html file using Gemini and refined it in VS Code.
Initial features included:
	•	Airport selector
	•	Real-time checkpoint wait-time UI (mock data)
	•	Historical trends and predictions chart
	•	TSA item checker section
	•	Favorites system (local only)
	•	UI styled using TailwindCSS and Chart.js

1.3 Verified UI locally

Opened the HTML file directly in the browser to confirm layout and interactions.

⸻

🟦 2. Git & GitHub Setup

2.1 Initialized local Git repository

A Git repository was initialized inside the project directory.

2.2 Renamed the default branch

The branch was renamed from master to main for consistency with GitHub standards.

2.3 Linked local repo to GitHub

A new GitHub repository named airport-security-tracker was created and set as the remote origin.

2.4 Resolved divergent branch histories

Encountered an issue where Git refused to merge unrelated histories.
This was resolved by allowing unrelated histories during the first pull from GitHub.

2.5 Successfully pushed project to GitHub

After fixing the history conflict, the full project was pushed to GitHub on the main branch.

⸻

🟦 3. GitHub Pages Deployment

3.1 Noticed GitHub Pages was unavailable

GitHub Pages could not be activated because the repository was private.

3.2 Changed repository visibility

Updated repository status from Private to Public.

3.3 Enabled GitHub Pages

Configured Pages to deploy from the main branch at the root folder.

3.4 Frontend deployed successfully

GitHub displayed a green banner confirming the live deployment of the site at:
https://parkjaeb.github.io/airport-security-tracker/

⸻

🟦 4. Backend Development (FastAPI)

4.1 Created backend folder

A subfolder named backend was created to isolate backend files from frontend assets.

4.2 Set up Python virtual environment

A Python virtual environment (venv) was created to manage backend dependencies.

4.3 Installed FastAPI and Uvicorn

Installed FastAPI for the backend framework and Uvicorn for running the server.

4.4 Created the backend API (main.py)

Developed a FastAPI service that:
	•	Accepts requests at /api/wait-times/{airport_id}
	•	Generates randomized checkpoint wait-times
	•	Creates simulated historical data
	•	Returns structured JSON to the frontend
	•	Supports CORS to allow browser fetch requests

4.5 Ran backend server locally

Started FastAPI server using Uvicorn.
Backend was accessible at:
	•	API Endpoint: http://127.0.0.1:8000/api/wait-times/SFO_T3
	•	API Documentation: http://127.0.0.1:8000/docs

4.6 Validated API output

Verified that the backend returned correct JSON data including checkpoints, wait times, and historical averages.

⸻

🟦 5. Frontend → Backend Integration

5.1 Removed mock data system

Deleted or disabled the original mock functions used for generating fake wait-time data inside the frontend.

5.2 Added API base URL

Defined a constant representing the backend URL (http://127.0.0.1:8000) for local development.

5.3 Updated data-loading function

Rewrote the loadWaitTimeData() function to fetch real backend data instead of relying on local mock objects.

5.4 Verified integration

Loaded the frontend locally while the backend was running and confirmed:
	•	The UI updated with real server data
	•	Changing airports triggered new backend requests
	•	Dynamic wait time and trend data appeared correctly

This completed the full-stack integration.

