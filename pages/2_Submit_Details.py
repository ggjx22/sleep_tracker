import src.utils_gsheets as gs
import src.utils_form as ui_form
import src.utils_styling as style

# display web page title
style.title("Record Previous Night's Details.")

# fetch data from google sheets
data = gs.fetch_data()

# create user form for input and submission into google drive
ui_form.create_user_form(data)