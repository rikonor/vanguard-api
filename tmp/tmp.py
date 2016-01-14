import requests
from bs4 import BeautifulSoup as BS

s = requests.session()
r = s.get("https://investor.vanguard.com/my-account/log-on")

soup = BS(r.content)
form = soup.find("form")

inputs = form.findAll("input")

# Extract form fields and values
form_info = dict()
for inpt in inputs:
    fid, fname, fval = inpt.attrs.get("id"), inpt.attrs.get("name"), inpt.attrs.get("value")
    form_info[fname] = fval

form_info["USER"] = "rikonor"
form_info["PASSWORD"] = ""

form_submit_path = form.attrs.get("action")

r = s.post(form_submit_path, data=form_info)

# Submit form for answering the question
