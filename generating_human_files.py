import requests
import os
import shutil

project_id = 1203677918601943

def generate_human_file(project_id):
  # This is the get request of the project URL. The #s are the project ID.
  url = f"https://app.asana.com/api/1.0/projects/{project_id}"

  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer ##INSERT BEARER TOKEN##'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  response = response.json()
  user_details_string = response['data']['notes']

  # This gets the notes data from the API configured into a dictionary.
  user_details_dict = []
  user_details = user_details_string.splitlines()
  for detail in user_details:
    for data in detail.split(', '):
        if ':' in data:
            user_details_dict.append(map(str.strip, data.split(':', 1)))

  user_details_dict = dict(user_details_dict)

  # These are the variables we need defined to create a human file.
  full_name_split = user_details_dict['Legal Full Name'].split(' ')
  first_name = full_name_split[0]
  last_name = full_name_split[-1]
  user_email = first_name.lower() + "." + last_name.lower() + "@redcanary.com"
  manager_email = user_details_dict['Manager'].lower()
  manager_email = manager_email.replace(' ', ".") + "@redcanary.com"
  user_department = user_details_dict['Department']
  user_division = user_details_dict['Functional Organization']
  user_cost_center = user_details_dict['Team']
  user_title = user_details_dict['Job Title']

  # This is the contents of the human file with the variables subbed in.
  human_file_contents = """
  module "okta_add_user_{first_name}_{last_name}" {{
    # Okta attributes
    source = "../modules/okta_user"
    status = "STAGED"
    user_type  = "Employee"
    user_email = "{user_email}"
    # Name Information
    first_name = "{first_name}"
    last_name  = "{last_name}"
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

  # Writes a new .tf file with the specified content.
  human_file = open(f"{first_name.lower()}.{last_name.lower()}.tf", "w")
  human_file.write(human_file_contents)

  # Moves the human file to the desired folder.
  file_being_moved = f"{first_name.lower()}.{last_name.lower()}.tf"
  destination_path = f"{os.path.expanduser('~')}/Desktop/Example_Folder"
  shutil.move(file_being_moved, destination_path)

def find_project_gids():
  url = "https://app.asana.com/api/1.0/portfolios/1203496810966165/items"

  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer ##INSERT BEARER TOKEN##'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  projects = response.json()
  projects = projects['data']
  project_gids = [new_canary_project['gid'] for new_canary_project in projects]

  return project_gids

for project_id in find_project_gids():
  generate_human_file(project_id)
