#!/usr/bin/env python
# coding: utf-8

# In[17]:


import json


json_data = '''
{
  "name": "Python Training",
  "date": "April 19, 2024",
  "completed": true,
  "instructor": {
    "name": "XYZ",
    "website": "http://pqr.com/"
  },
  "participants": [
    {
      "name": "Participant 1",
      "email": "email1@example.com"
    },
    {
      "name": "Participant 2",
      "email": "email2@example.com"
    }
  ]
}
'''
training_session = json.loads(json_data)

completed = training_session["completed"] # accessing boolean 


training_name = training_session["name"] # Accessing string 


training_date = training_session["date"] # Accessing date 


instructor_name = training_session["instructor"]["name"]             # Accessing dictionary 
instructor_website = training_session["instructor"]["website"]

print("Participants:")
for participant in training_session["participants"]:          #Accessing Participants 
    print("Name:", participant["name"])
    print("Email:", participant["email"])
    
# Printing values
print("Training Name:", training_name)
print("Date:", training_date)
print("Completed:", completed)
print("Instructor Name:", instructor_name)
print("Instructor Website:", instructor_website)
print("Participant Names:", participant_names)
print("Participant Emails:", participant_emails)

# Modifying data
training_session["completed"] = False  # Marking the session as incomplete
training_session["instructor"]["name"] = "ABC"  # Changing the instructor's name

# Adding a new participant
new_participant = {"name": "Participant 3", "email": "email3@example.com"}
training_session["participants"].append(new_participant)

# Converting back to JSON
updated_json_data = json.dumps(training_session, indent=2)
print("\nUpdated JSON data:")
print(updated_json_data)


# In[ ]:




