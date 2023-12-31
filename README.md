<div align="center">
  <h1>Sleep Tracker Web App 😴</h1>
</div>

## Introduction

This project is mainly created to log a person's sleep-related information. There are 2 main pages to this web app:<br>
1. Submit details page (for logging of sleep-related information).
2. Amend details page (for amending or updating previously submitted information).

## Project prerequisite
The prerequisites are simple. A valid Google account which you probably already have and an account with Streamlit.

Links to create accounts (if you have not created them):
1. [Google account](https://accounts.google.com/lifecycle/steps/signup/name?continue=https://myaccount.google.com?utm_source%3Daccount-marketing-page%26utm_medium%3Dcreate-account-button&dsh=S554448893:1704008136916243&flowEntry=SignUp&flowName=GlifWebSignIn&theme=glif&TL=AHNYTIQUWJ_R0SHQjbUNoq7ExQd-oSdQ0qQ4MFZkyobs4qcq6IxRLntGEwuCyxrR)
2. [Streamlit account](https://streamlit.io/)

## Tools required

The following tools are used for building this project.

| Tools | Purpose |
| :------------ | :------------- |
| [Google Sheets](https://www.google.com/sheets/about/#overview) | Cloud storage of sleep data |
| [Google Drive & Sheets API in Python](https://console.cloud.google.com/projectselector2/apis/dashboard?supportedpurview=project) | Interaction with Google Drive & Sheets |
| [Streamlit](https://streamlit.io/) | Framework to build and deploy web app |

## Getting Started

From here onwards, you should already have a valid google account and signed in to it.

### 1. Enable access for two APIs (google drive and sheets).

We do this so that we can connect google sheets with the streamlit app.

- Go to [Google Developer Console](https://console.cloud.google.com/projectselector2/apis/dashboard?supportedpurview=project) and complete the following tasks.
  - Create a new project.<br>
    - Click on "Select a project" and "NEW PROJECT".
      ![create_project](img/1a.%20create_project.png)

    - Give your project a name and click on "CREATE".
      ![name_project_name](img/1b.%20name_project_name.png)

    - Make sure the project has been selected in the console.
      ![select_project](img/1c.%20select_project.png)

  - Activate google drive and google sheets API.
    - Google Drive API.
      ![search_google_drive_api](img/1d.%20search_google_drive_api.png)
      ![enable_google_drive_api](img/1e.%20enable_google_drive_api.png)

    - Google Sheets API.
      ![search_google_sheets_api](img/1f.%20search_google_sheets_api.png)
      ![enable_google_sheets_api](img/1g.%20enable_google_sheets_api.png)

  - Create a service account to use the APIs.
    - Click on "Credentials", select "+ CREATE CREDENTIALS" and "Service account".
      ![select_credentials](img/1h.%20select_credentials.png)

    - Provide a name for the service account and click on "CREATE AND CONTINUE".
      ![name_service_account_name](img/1i.%20name_service_account_name.png)

    - Enable read and write access for the service account by giving the "Editor" role. Click on "DONE" to grant the access.
      ![assign_editor_role](img/1j.%20assign_editor_role.png)

  - Create secrets.toml file
    - To obtain credentials for secrets.toml file, we need to create them first. Select on the service account that you have just created.
    ![select_service_account](img/1k.%20select_service_account.png)

    - Click on "KEYS" -> "ADD KEY" -> "Create new key" -> ensure Key type JSON is selected. Then click on "CREATE"
    ![create_service_account_key](img/1l.%20create_service_account_key.png)

    - A `.json` file which contains the credentials should be automatically downloaded into your Downloads folder.
    ![keys_json_file_downloaded](img/1m.%20keys_json_file_downloaded.png)

    - Create a `.streamlit` folder in the root directory of your working folder. Place the downloaded `.json` file into it. Create a new file called `secrets.toml`.
    - From your preferred IDE, open the working folder and both `.json` and `secrets.toml` files.
    - Copy the following format and paste into `secrets.toml` file.
      ```
      # .streamlit/secrets.toml

      [connections.gsheets]
      spreadsheet = "<spreadsheet-name-or-url>"
      worksheet = "<worksheet-gid-or-folder-id>"  # worksheet GID is used when using Public Spreadsheet URL, when usign service_account it will be picked as folder_id
      type = ""  # leave empty when using Public Spreadsheet URL, when using service_account -> type = "service_account"
      project_id = ""
      private_key_id = ""
      private_key = ""
      client_email = ""
      client_id = ""
      auth_uri = ""
      token_uri = ""
      auth_provider_x509_cert_url = ""
      client_x509_cert_url = ""
      ```
    - Transfer the relevant information from `.json` file into the `secrets.toml` file. Save `secrets.toml` file.
      ![create_secrets_toml_file](img/1n.%20create_secrets_toml_file.png)

    - From `secrets.toml`, copy `client_email`. We need this email address from the service account to grant access for our google sheet.
    - Create a new google sheet, and click on "Share". Paste `client_email` and click "Send".
    ![share_gsheets_with_service_account_user](img/1o.%20share_ghseets_with_service_account_user.png)

    - Copy the URL of the google sheet from the beginning until `/edit...`. Go back to `secrets.toml` and paste it in `spreadsheet`. Save `secrets.toml` file.
    ![copy_ghseets_url](img/1p.%20copy_gsheets_url.png)
    - The `.json` file can be deleted.
  
