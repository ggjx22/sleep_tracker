import src.utils_gsheets as gs
import src.utils_form as ui_form
import src.utils_styling as style

# display web page title
style.title("Amend Your Sleep Records.")

# fetch data from google sheets
data = gs.fetch_data()

# retrieve records and amend based on date selection
ui_form.user_amend_form(data)