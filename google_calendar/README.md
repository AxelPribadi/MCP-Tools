# 📆 Google Calendar MCP
This MCP server allows you to manage your Google Calendar directly from Claude, enabling seamless event creation, updates, and deletions—all without leaving the chat.

## Setup
1. Set Up Google Cloud
Follow these steps to set up your Google Cloud project and obtain credentials:
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project.
- Enable the Google Calendar API for your project.
- Create OAuth 2.0 credentials:
    - Go to "Credentials" in the left sidebar.
    - Click "Create Credentials" and select "OAuth client ID".
    - Configure the consent screen and application type (Desktop app).
    - Download the `credentials.json` file.
Once you've completed these steps, make sure to place the `credentials.json` file in the same directory as your scripts.

2. Authorize the Application
Run the script below to authorize the application and generate the `token.json` file:
```bash
cd google_calendar
uv run calendar_functions.py
```
- This will open a browser window asking you to log in to your Google account and authorize the application. 
- After authorization, a `token.json` file will be created in the same directory, allowing the script to access your calendar without needing to log in again.

## ✅ You're Ready to Go!
Now that you've set up the authorization, you can follow the general instructions to install the server and start managing your calendar through Claude.