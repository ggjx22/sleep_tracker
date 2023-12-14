import src.utils_gsheets as gs
import src.utils_form as ui_form
import src.utils_styling as style

# display web page title
style.title("Submit Your Sleep Records.")

# init connection with google sheet and fetch data
gs_manager = gs.GSheetsManager()
data = gs_manager.fetch_data(worksheet_name='sleep')

# create user form for input and submission into google drive
ui_form.create_user_form(data)