import requests
import os
import shutil
import re
from sensitive import token

### This script reads from Asana Onboarding projects and transfers new user information into
### our human file format. It then saves the files in your local identity repo. After you
### run the script, open up Github desktop and you'll see all of the human files it has made for you.
### You'll likely need to make sure all of the titles and etc. match up in Terraform,
### since the new user information it's using are inputs from Talent.

def generate_human_file(project_id):
  # This is the get request of the project URL.
  url = f"https://app.asana.com/api/1.0/projects/{project_id}"

  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  response = response.json()
  user_details_string = response['data']['notes']

  # This gets the notes user data from the API configured into a dictionary so
  # they're easy to work with.
  user_details = user_details_string.splitlines()

  user_details_dict = {}
  
  for detail in user_details:
    key = detail.split(':', 1)[0].strip()
    value = detail.split(':', 1)[1].strip()
    
    user_details_dict.update({key: value})

  # These are the variables we need defined to create the dynamic human file.
  # Some logic to handle three name splits, as well as names with apostrophes.
  full_name_split = user_details_dict['Legal Full Name'].split(' ')
  if len(full_name_split) == 3:
    last_name = full_name_split[-2:]
    string_last_name = ' '.join(last_name)
    module_last_name = '_'.join(last_name)
    module_last_name = module_last_name.replace("'", "")
    last_name = ''.join(last_name)

  else:
    last_name = full_name_split[-1]
    string_last_name = last_name
    module_last_name = last_name
    module_last_name = module_last_name.replace("'", "")

  preferred_first_name = user_details_dict["Preferred First Name"]

  first_name = full_name_split[0]
  last_name = last_name.replace("'", "")

  # User shipping information.
  shipping_address = user_details_dict['Shipping Address']

  #Finds the State Code.
  state_code = re.search(r'\b[A-Z]{2}\b', shipping_address)
  state_code = state_code.group(0)

  # #Finds users in Denver.
  # denver_peeps = re.search(r'\bDenver\b', shipping_address)
  # denver_peeps = denver_peeps.group(0)

  # User and their manager's emails.
  user_email = preferred_first_name.lower() + "." + last_name.lower() + "@redcanary.com"
  manager_email = user_details_dict['Manager'].lower()
  manager_email = manager_email.replace(' ', ".") + "@redcanary.com"

  # User title information.
  user_department = user_details_dict['Department']
  user_division = user_details_dict['Functional Organization']
  user_cost_center = user_details_dict['Team']
  if user_cost_center == "N/A":
    user_cost_center = user_cost_center.replace("N/A", "")
  user_title = user_details_dict['Job Title']

  # This is the contents of the human file with the variables subbed in.
  human_file_contents = """module "okta_add_user_{preferred_first_name}_{module_last_name}" {{
  # Okta attributes
  source = "../modules/okta_user"
  status = "STAGED"
  user_type  = "Employee"
  user_email = "{user_email}"
  # Name Information
  first_name = "{preferred_first_name}"
  last_name  = "{string_last_name}"
  #     middleName = ""
  #     honorificPrefix = ""
  #     honorificSuffix = ""
  # Contact Information
  #     second_email = ""
  mobile_phone = ""
  # Location Information
  state        = ""
  country_code = "US"
  # Job Information
  organization = "Red Canary"
  division     = "{user_division}"
  department   = "{user_department}"
  cost_center  = "{user_cost_center}"
  title        = "{user_title}"
  #     manager_id = ""
  manager = "{manager_email}"
  # What groups are they a part of
  groups = [

  ]
}}
  """.format(**locals())

  # Writes a new .tf file with the specified content. To overwrite a file, we'd first check if 
  # it existed and then delete it before creating a new one.
  human_file = open(f"{preferred_first_name.lower()}.{last_name.lower()}.tf", "w")
  human_file.write(human_file_contents)

  # Moves the human file to the desired folder.
  file_being_moved = f"{preferred_first_name.lower()}.{last_name.lower()}.tf"
  destination_path = f"{os.path.expanduser('~')}/GitHub/infrastructure-it-terraform-okta-identity/users_and_groups/humans/"
  # destination_path = f"{os.path.expanduser('~')}/Desktop/Example_Folder"
  shutil.move(file_being_moved, destination_path)

print("")
print("Hello! Please enter the onboarding portoflio id #. \nThis is the sixteen digit number found in the onboarding portfolio's hyperlink. \n(ie, https://app.asana.com/api/1.0/portfolios/################/items)")
print("")
input = input()
# Grabs all of the user's project ids from the portfolio id in Asana.
def find_project_gids():
  url = f"https://app.asana.com/api/1.0/portfolios/{input}/items"

  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  projects = response.json()
  projects = projects['data']
  project_gids = [new_canary_project['gid'] for new_canary_project in projects]

  return project_gids

[generate_human_file(project_id) for project_id in find_project_gids()]

print("")
print("All done! Check Github Desktop and review your human files.")
print("")
