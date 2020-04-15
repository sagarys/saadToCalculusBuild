#!/usr/bin/env python
import json
import requests
import sys
import os
import shutil
import subprocess

CALCULUS_HOST='calculus.efi.com'
f = open('cal_reqmon.txt', 'r')
calculus_requests = f.readlines()
f.close()

remaining_calculus_requests = calculus_requests.copy()
BUILD_LOCATION = "\\\\bawibld43\\bldtmp\\sagars\\"

def linuxBuildCopy(src_location,prodDir,build_type):
    dpkg = src_location.split("\\").pop() + ".dpkg"
    dpkg_roman = src_location.split("\\").pop() + "_roman.dpkg"
    dpkg_K2M = src_location.split("\\").pop()+ "_k2m.dpkg"
    dest_loc = os.path.join(BUILD_LOCATION,prodDir,build_type)
    if os.path.isdir(dest_loc) :
        shutil.rmtree(dest_loc)
    dpkg_copy ="copy_file.bat "+ src_location +" " +"\""+ dest_loc +"\""+" "+ dpkg + " "+ prodDir +"_"+build_type+"_dpkg.log"
    dpkg_roman_copy ="copy_file.bat "+ src_location +" " +"\""+ dest_loc +"\""+" "+ dpkg_roman + " "+ prodDir +"_"+build_type+"_dpkg_roman.log"
    dpkg_K2M_copy ="copy_file.bat "+ src_location +" " +"\""+ dest_loc +"\""+" "+ dpkg_K2M + " "+ prodDir +"_"+build_type+"_dpkg_K2M.log"
    if subprocess.call(dpkg_copy) != 0 :
        print("Copy Failed !!!!" + dpkg_copy)
    if subprocess.call(dpkg_roman_copy) != 0 :
        print("Copy Failed !!!!" + dpkg_roman_copy)
    if subprocess.call(dpkg_K2M_copy) != 0 :
        print("Copy Failed !!!!" + dpkg_K2M_copy)

def windowsBuildCopy(src_location,prodDir,build_type) :
    dest_loc = os.path.join(BUILD_LOCATION,prodDir,build_type)
    if os.path.isdir(dest_loc) :
        shutil.rmtree(dest_loc)
    exe_copy = "copy_dir.bat "+ installer_location +" " +"\""+ dest_loc +"\""+" "+ "\"" + r.json()['request']['name'] +"_"+build_type+"_windows.log" + "\""
    subprocess.call(exe_copy)

def checkOsType(src_location) :
    if os.path.exists(src_location):
        list_dir = os.listdir(src_location)
        for temp in os.listdir(src_location) :
            if ".exe" in temp :
                return True
    else 
        print("Path does not exists :- " + src_location)
    return False

def store_calculus_request(calReq,prodDir) :
    store_calculus_request = os.path.join(BUILD_LOCATION,prodDir,prodDir+"_cal_req.txt")
    if os.path.exists(os.path.join(BUILD_LOCATION,prodDir)):
        f = open(store_calculus_request, 'w')
        f.write(calReq)
        f.close()

for calculus_request in calculus_requests:
    r = requests.get("https://calculus.efi.com/api/v10/requests/"+calculus_request.split("/").pop().strip())
    store_calculus_request(calculus_request,r.json()['request']['name'])
    try:
        if(r.json()['request']['builds'][0]['status'] == "pass") :
            installer = format(r.json()['request']['builds'][0]['installer'])
            dest_loc = r.json()['request']['name']
            installer_location = installer.replace("/","\\").split(":").pop()
            if checkOsType(installer_location) == False :
                linuxBuildCopy(installer_location,r.json()['request']['name'],"Debug")
            else :
                windowsBuildCopy(installer_location,r.json()['request']['name'],"Debug")
        elif (r.json()['request']['builds'][0]['status'] == "fail"):
            print("Debug Build Failed for the request !!!! " + calculus_request)
        else:
            continue
        

        if(r.json()['request']['builds'][1]['status'] == "pass") :
            installer = format(r.json()['request']['builds'][1]['installer'])
            installer_location = installer.replace("/","\\").split(":").pop()
            dest_loc = r.json()['request']['name']
            if checkOsType(installer_location) == False :
                linuxBuildCopy(installer_location,r.json()['request']['name'],"Release")
            else :
                windowsBuildCopy(installer_location,r.json()['request']['name'],"Release")
            remaining_calculus_requests.remove(calculus_request)                
        elif (r.json()['request']['builds'][1]['status'] == "fail"):
            print("Release Build Failed for the request !!!! " + calculus_request)
            remaining_calculus_requests.remove(calculus_request)
        else:
            continue

    except ValueError:
       print(r.text)
if calculus_requests != remaining_calculus_requests :          
    f = open('cal_reqmon.txt', 'w')
    for line in remaining_calculus_requests :
        f.write(line)
    f.close()