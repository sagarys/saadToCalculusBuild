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
BUILD_LOCATION = "\\\\bauser\\Fiery-products\\Sustaining_builds"


def CopyBuilds(src_location,prodDir,build_type) :
    dest_loc = os.path.join(BUILD_LOCATION,prodDir,build_type)
    if os.path.isdir(dest_loc) :
        remReadonly = "remReadonly.bat "+dest_loc
        subprocess.call(remReadonly)
        shutil.rmtree(dest_loc)
        #shutil.rmtree(dest_loc,ignore_errors=False,onerror=HandleError)
    exe_copy = "copy_dir.bat "+ installer_location +" " +"\""+ dest_loc +"\""+" "+ "\""+".\Log\\" + prodDir +"_"+build_type+".log" + "\""
    subprocess.call(exe_copy)

def HandleError(func, path, exc) :
    print("Shutil delete error :- "+path) 

def checkWinOsType(osType) :
    if (str(osType).find('windows') != -1): 
        return True
    return False

def store_calculus_request(calReq,prodDir) :
    prdName = prodDir.split('\\')[-1]
    store_calculus_request = os.path.join(BUILD_LOCATION,prodDir,prdName+"_cal_req.txt")
    if os.path.exists(os.path.join(BUILD_LOCATION,prodDir)):
        f = open(store_calculus_request, 'w')
        f.write(calReq)
        f.close()

def pdbLocation(installer_location,pdb_loc) :
    installer_location_symbol = "runtime\\release\\server\\system\\"
    symbolPath = installer_location.split("\\")
    symbolPath = [i for i in symbolPath if i] 
    K = 2
    symbolPath = symbolPath[: -K or None] 
    symbolPath = "\\\\".join(symbolPath)
    symbolPath = "\\\\" +symbolPath
    symbolPath = os.path.join(symbolPath,installer_location_symbol)
    return symbolPath

def copyBreakPadSymbols(prodDir) :
    symbolPath = installer_location.split("\\")
    symbolPath = [i for i in symbolPath if i] 
    K = 2
    symbolPath = symbolPath[: -K or None] 
    symbolPath = "\\\\".join(symbolPath)
    symbolPath = "\\\\" +symbolPath
    symbolPath = os.path.join(symbolPath,"symbols")
    dest_loc = os.path.join(BUILD_LOCATION,prodDir,"symbols")
    exe_copy = "copy_dir.bat "+ symbolPath +" " +"\""+ dest_loc +"\""+" "+ "\""+".\Log\\" + prodDir +"_breakpadsymbols"+".log" + "\""
    subprocess.call(exe_copy)
    
def store_symbols(installer_location,prodDir,build_type) :
    symbolPath = installer_location.split("\\")
    symbolPath = [i for i in symbolPath if i] 
    K = 2
    symbolPath = symbolPath[: -K or None] 
    symbolPath = "\\\\".join(symbolPath)
    symbolPath = "\\\\" +symbolPath
    symbolPath = os.path.join(symbolPath,"runtime")
    dest_loc = os.path.join(BUILD_LOCATION,prodDir,"pdbs")
    for folder in os.listdir(symbolPath):
        for pdb in os.listdir(os.path.join(symbolPath,folder,"server\\system\\")):
            if pdb.split(".")[-1] == "pdb" :
                pdb_copy ="copy_file.bat "+ os.path.join(symbolPath,folder,"server\\system\\") +" " +"\""+ dest_loc +"\""+" "+ pdb + " "+"\""+".\Log\\"+ prodDir +"_"+build_type+"_pdb.log"+"\""
                subprocess.call(pdb_copy)

def store_calFail_req(calculus_job_request,prodDir,build_type,fileName) :
    print(calculus_job_request)
    if os.path.exists(fileName):
        append_write = 'a' 
    else:
        append_write = 'w' 
    f = open(fileName, append_write)
    f.write("build failed for the product " + prodDir + " and the build type is " + build_type+"\n")
    f.write(str(calculus_job_request)+"\n")
    f.close()

for calculus_request in calculus_requests:
    r = requests.get("https://calculus.efi.com/api/v10/requests/"+calculus_request.split("/").pop().strip())
    if (r.json()['request']['builds'][0]['status'] == "canceled" and r.json()['request']['builds'][1]['status'] == "canceled") :
            remaining_calculus_requests.remove(calculus_request)
            continue
    try:
        if(r.json()['request']['builds'][0]['status'] != "canceled" and r.json()['request']['installs'][0]['status'] != "canceled" and r.json()['request']['tests'][0]['status'] != "canceled") :
            prod_name = (r.json()['request']['name']).replace(" ","").split("__")
            dest_loc = os.path.join(prod_name[0],prod_name[1])
            if(r.json()['request']['builds'][0]['status'] == "pass" or r.json()['request']['installs'][0]['status'] == "pass" or r.json()['request']['tests'][0]['status'] == "pass") :
                installer = format(r.json()['request']['builds'][0]['installer'])
                installer_location = installer.replace("/","\\").split(":").pop()   
                CopyBuilds(installer_location,dest_loc,"Debug")
            elif (r.json()['request']['builds'][0]['status'] == "fail"):
                print("Debug Build Failed for the request !!!! " + calculus_request)
                store_calFail_req(calculus_request,dest_loc,"Debug","cal_Failures.txt")
            elif (r.json()['request']['installs'][0]['status'] == "fail"):
                print("Debug Build Failed for the request !!!! " + calculus_request)
                store_calFail_req(calculus_request,dest_loc,"Debug","cal_install_Failures.txt")
            elif (r.json()['request']['tests'][0]['status'] == "fail"):
                print("Debug Build Failed for the request !!!! " + calculus_request)
                store_calFail_req(calculus_request,dest_loc,"Debug","cal_tests_Failures.txt")
            else:
                continue
        else:
            print("Debug Build Cancelled for the request !!!! " + calculus_request)
        
        if(r.json()['request']['builds'][1]['status'] != "canceled" and r.json()['request']['installs'][1]['status'] != "canceled" and r.json()['request']['tests'][1]['status'] != "canceled") :
            prod_name = (r.json()['request']['name']).replace(" ","").split("__")
            dest_loc = os.path.join(prod_name[0],prod_name[1])
            if(r.json()['request']['builds'][1]['status'] == "pass" or r.json()['request']['installs'][1]['status'] == "pass" or r.json()['request']['tests'][1]['status'] == "pass") :
                installer = format(r.json()['request']['builds'][1]['installer'])
                installer_location = installer.replace("/","\\").split(":").pop()
                CopyBuilds(installer_location,dest_loc,"Release")
                if checkWinOsType(r.json()['request']['builds'][1]['products']) != False :
                    store_symbols(installer_location,dest_loc,"Release")
                    copyBreakPadSymbols(dest_loc)
                store_calculus_request(calculus_request,dest_loc)
                remaining_calculus_requests.remove(calculus_request)                
            elif (r.json()['request']['builds'][1]['status'] == "fail"):
                print("Release Build Failed for the request !!!! " + calculus_request)
                store_calFail_req(calculus_request,dest_loc,"Release","cal_Failures.txt")
                remaining_calculus_requests.remove(calculus_request)
            elif (r.json()['request']['installs'][1]['status'] == "fail"):
                print("Release Build Failed for the request !!!! " + calculus_request)
                store_calFail_req(calculus_request,dest_loc,"Release","cal_install_Failures.txt")
                remaining_calculus_requests.remove(calculus_request)
            elif (r.json()['request']['tests'][1]['status'] == "fail"):
                print("Release Build Failed for the request !!!! " + calculus_request)
                store_calFail_req(calculus_request,dest_loc,"Release","cal_tests_Failures.txt")                       
                remaining_calculus_requests.remove(calculus_request)
            else:
                continue
        else :
            print("Release Build Cancelled for the request !!!! " + calculus_request)

    except ValueError:
       print(r.text)
if calculus_requests != remaining_calculus_requests :          
    f = open('cal_reqmon.txt', 'w')
    for line in remaining_calculus_requests :
        f.write(line)
    f.close()