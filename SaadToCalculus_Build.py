#!/usr/bin/env python
import os
import requests
import sys
import pprint
import subprocess
import json

SAAD = "https://saad.efi.com"
calculus_req_json = {
  "request" : {
    "name"                  : "",
    "email_list"            : "sagar.s@efi.com",
    "region"                : "vCommander IDC",
    "user"                  : "sagars",

    "builds" :[
      {
        "arguments"           : "all",
        "version"             : "",
        "configspec"          : "",
        "products"            : ["",""]
      }
      ]
  }
}
ss = json.dumps(calculus_req_json)
calculus_req = json.loads(ss)
BUILD_LOCATION = "\\\\bawibld43\\bldtmp\\sagars\\"
MAX_REQUESTS = 20

def create_json(calculus_req) :
    f = open(key+"_cal_req.json", "w")
    f.write(json.dumps(calculus_req))
    f.close()
    
def store_cal_req(calculus_job_request) :
    print(calculus_job_request)
    if os.path.exists("cal_reqmon.txt"):
        append_write = 'a' 
    else:
        append_write = 'w' 
    f = open("cal_reqmon.txt", append_write)
    f.write(str(calculus_job_request))
    f.close()
    
def create_dir(dir_name):
    if not os.path.isdir (os.path.join(BUILD_LOCATION,dir_name)):
        os.mkdir (os.path.join(BUILD_LOCATION,dir_name))

def compare_configspec(dir_name,configspec):
    dir_name = dir_name.rstrip()
    configspec_path = os.path.join(BUILD_LOCATION,dir_name,dir_name+"_configspec.txt")
    if not os.path.exists(configspec_path) and not os.path.isfile(configspec_path):
        f = open(configspec_path, "w")
        f.write(configspec)
        f.close()
    else :
        f = open(configspec_path, "r")
        config_text=f.read()
        f.close()
        if(config_text == configspec) :
            return False
        else:
            os.remove(configspec_path)
            f = open(configspec_path, "w")
            f.write(configspec)
            f.close()
    return True
    
def format_configspec(configspec):
    temp = ""
    for line in configspec.splitlines():
        if "#" not in line and line != "" :
            temp = temp + line + "\n"
    calculus_req['request']['builds'][0]['configspec'] = temp
    return calculus_req['request']['builds'][0]['configspec']
    
def handle_response_errors(response):
    if response.status_code == 404:
        print("Not Found\n")
        sys.exit(404)

    if response.status_code == 401:
        print("Access Denied\n")
        sys.exit(401)

    if response.status_code != 200:
        print("Unhandled error: {}".format(response.status_code))
        sys.exit(response.status_code)

headers = {
    'Accept': 'application/json',
    'jira-login' : '',
    'jira-password' : '',
    'saad-api-key' : 'c0a109c2-9c81-4412-8ce8-55e743fe8215',
}

projects_url = "{saad}/api/v0/projects/".format(saad=SAAD)
projects_url_configspec = "{saad}/api/v0/projects/".format(saad=SAAD)

response = requests.get(projects_url, headers=headers)
projects = response.json()

prod_configpsec = " "
key = " "
calculus_name = " "
project_name = " "
req  = 0

for project_dict in projects:
    if req < MAX_REQUESTS :
        if len(str("{codebase}").format(**project_dict).strip()) == 0 :
            continue
        if 'Flame' not in str("{codebase}").format(**project_dict).strip() :
            continue
        flame = str("{codebase}").format(**project_dict)
        flame = flame.replace(".","")
        flame = flame.replace(" ","").lower()
        key = str("{key}".format(**project_dict))
        project_name = str("{name}".format(**project_dict))
        calculus_name = str("{calculus name}".format(**project_dict))
        if len(str("{calculus name}").format(**project_dict).strip()) == 0 :
            continue
        calculus_req['request']['builds'][0]['products'][0] = calculus_name + '/'+'debug' 
        calculus_req['request']['builds'][0]['products'][1] = calculus_name + '/'+'release' 
        prod_configpsec = "http://saad.efi.com/api/v0/projects/"+str("{key}".format(**project_dict))+"/configspec"
        response = requests.get(prod_configpsec, headers=headers)
        if response.status_code != 200 :
            print("Error Configspec not found for the product " + key + " with response status code "  + str(response.status_code))
        else :
            print("Configspec found for the product " + key)
            format_configspec(response.text)
            calculus_req['request']['name'] = project_name
            create_dir(project_name)            
            if compare_configspec(project_name,calculus_req['request']['builds'][0]['configspec']):
                print("Build triggered for the product " + key)
                create_json(calculus_req)
                calculus_job_request = subprocess.call("python apiv10.py "+ key +"_cal_req.json")      
                if os.path.exists(key +"_cal_req.json"):
                    os.remove(key +"_cal_req.json")
                req = req + 1
            else :
                continue
                