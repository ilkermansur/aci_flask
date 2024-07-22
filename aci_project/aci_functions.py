import json
import requests
import urllib3
import time
import pandas as pd
import re

"""
1- login (ip="192.168.222.240",username="admin",password="Aa123456") -> return token
2- create_tenant (ip="192.168.222.240",tn_name=tn_test_name, tn_alias=tn_test_alias, tn_desc=tn_test_desc)
"""
################################################################################################################################
def login(ip, username, password):
        try:
            # define base URL
            base_url = f'https://{ip}/api/'

            # create credentials structure
            name_pwd = {'aaaUser': {'attributes': {'name': username, 'pwd': password}}}
            json_credentials = json.dumps(name_pwd)
            
            # log in to API
            login_url = base_url + 'aaaLogin.json'
            
            # disable warnings about SSL
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(url=login_url, data=json_credentials, verify=False)
            
            # get token from login response structure
            data = response.json()
            token = data['imdata'][0]['aaaLogin']['attributes']['token']
            print ('Getting TOKEN Succesfully')
            return token
        #Print error code and explaination
        except Exception as e:
            print (f"error is occured {e}")

################################################################################################################################

def create_tenant (ip,tn_name, tn_alias, tn_desc, token):
    try:
        create_tenant_url = f"https://{ip}/api/node/mo/uni/tn-{tn_name}.json"

        pre_payload = {
        "fvTenant":{
            "attributes":{
                "dn":f"uni/tn-{tn_name}",
                "name":f"{tn_name}",
                "nameAlias":f"{tn_alias}",
                "descr":f"{tn_desc}",
                "rn":f"tn-{tn_name}",
                "status":"created"},
                "children":[]
                }
            }
        payload = json.dumps(pre_payload)
        response = requests.post(url=create_tenant_url, cookies={"APIC-Cookie":token}, data=payload, verify=False)

        if response.status_code == 200 :
            result = f"Creating tenant {tn_name} succesfully"
            return result,response.status_code
        else:
            result = f" Error - {response} "
            return result
    except Exception as e:
        result = f"Error occurred {e}"
        return result
    
    ################################################################################################################################
    
def create_vrf (ip,tn_name, vrf_name, vrf_alias, vrf_desc, token):
    try:
        create_vrf_url = f"https://{ip}/api/node/mo/uni/tn-{tn_name}/ctx-{vrf_name}.json"

        pre_payload = {
            "fvCtx": {
                "attributes": {
                "dn": f"uni/tn-{tn_name}/ctx-{vrf_name}",
                "name": vrf_name,
                "nameAlias": vrf_alias,
                "descr": vrf_desc,
                "rn": f"ctx-{vrf_name}",
                "status": "created"
                },
                "children": []
                }
            }
        payload = json.dumps(pre_payload)
        response = requests.post(url=create_vrf_url, cookies={"APIC-Cookie":token}, data=payload, verify=False)

        if response.status_code == 200 :
            result = f"Creating vrf {vrf_name} succesfully"
            return result, response.status_code

        else:
            result = f"error - {response}"
            return result
    except Exception as e:
        result = f"Error occurred {e}"
        return result
################################################################################################################################

def create_bd (ip,tn_name, vrf_name, bd_name, bd_alias, bd_desc, token):
    try:
        create_bd_url = f"https://{ip}/api/node/mo/uni/tn-{tn_name}/BD-{bd_name}.json"
        pre_payload = {
            "fvBD": {
                "attributes": {
                "dn": f"uni/tn-{tn_name}/BD-{bd_name}",
                "mac": "00:22:BD:F8:19:FF",
                "arpFlood": "true",
                "name": bd_name,
                "nameAlias": bd_alias,
                "descr": bd_desc,
                "unicastRoute": "false",
                "mcastARPDrop": "false",
                "rn": f"BD-{bd_name}",
                "status": "created"
                },
                "children": [
                {
                    "fvRsCtx": {
                    "attributes": {
                        "tnFvCtxName": vrf_name,
                        "status": "created,modified"
                    },
                    "children": []
                    }
                }
                ]
            }
        }
        payload = json.dumps(pre_payload)

        response = requests.post(url=create_bd_url, cookies={"APIC-Cookie":token}, data=payload, verify=False)

        if response.status_code == 200 :
            result = f"Creating bd {bd_name} succesfully"
            return result, response.status_code
        else:
            result = f"error - {response}"
            return result
    except Exception as e:
        result = f"Error occurred {e}"
        return result

################################################################################################################################

def create_app (ip, tn_name, app_name, app_alias, app_desc, token):
    try:
        create_app_url = f"https://{ip}/api/node/mo/uni/tn-{tn_name}/ap-{app_name}.json"
        pre_payload = {
            "fvAp": {
                "attributes": {
                "dn": f"uni/tn-{tn_name}/ap-{app_name}",
                "name": app_name,
                "nameAlias": app_alias,
                "descr": app_desc,
                "rn": f"ap-{app_name}",
                "status": "created"
                },
                "children": []
            }
            }
        payload = json.dumps(pre_payload)

        response = requests.post(url=create_app_url, cookies={"APIC-Cookie":token}, data=payload, verify=False)

        if response.status_code == 200 :
            result = f"Creating app {app_name} succesfully"
            return result,response.status_code
        else:
            result = f" error - {response}"
            return result
    except Exception as e:
        result = f"Error occurred {e}"
        return result
################################################################################################################################

def create_epg (ip, tn_name, app_name, bd_name, epg_name,epg_alias, epg_desc, token):
    try:
        create_epg_url = f"https://{ip}/api/node/mo/uni/tn-{tn_name}/ap-{app_name}/epg-{epg_name}.json"
        pre_payload = {
            "fvAEPg": {
                "attributes": {
                "dn": f"uni/tn-{tn_name}/ap-{app_name}/epg-{epg_name}",
                "prio": "level3",
                "name": epg_name,
                "nameAlias": epg_alias,
                "descr": epg_desc,
                "rn": f"epg-{epg_name}",
                "status": "created"
                },
                "children": [
                {
                    "fvRsBd": {
                    "attributes": {
                        "tnFvBDName": bd_name,
                        "status": "created,modified"
                    },
                    "children": []
                    }
                }
                ]
            }
            }
        payload = json.dumps(pre_payload)

        response = requests.post(url=create_epg_url, cookies={"APIC-Cookie":token}, data=payload, verify=False)

        if response.status_code == 200 :
            result = f"Creating epg {epg_name} succesfully"
            return result, response.status_code
        else:
            result = f"error - {response}"
            return result
    except Exception as e:
        result = f"Error occurred {e}"
        return result
################################################################################################################################

def create_bulk (file, host, token ):
        try:

            if file :
                df = pd.read_excel("bulk_temp.xlsx")
                tn_name_list = df["TN_Name"].to_list()
                tn_alias_list = df["TN_Alias"].to_list()
                tn_desc_list = df["TN_Desc"].to_list()
                vrf_name_list = df["VRF_Name"].to_list()
                vrf_alias_list = df["VRF_Alias"].to_list()
                vrf_desc_list = df["VRF_Desc"].to_list()
                bd_name_list = df["BD_Name"].to_list()
                bd_alias_list = df["BD_Alias"].to_list()
                bd_desc_list = df["BD_Desc"].to_list()
                app_name_list = df["APP_Name"].to_list()
                app_alias_list = df["APP_Alias"].to_list()
                app_desc_list = df["APP_Desc"].to_list()
                epg_name_list = df["EPG_Name"].to_list()
                epg_alias_list = df["EPG_Alias"].to_list()
                epg_desc_list = df["EPG_Desc"].to_list()

                zip_list = zip (
                    tn_name_list, tn_alias_list, tn_desc_list,
                    vrf_name_list,vrf_alias_list, vrf_desc_list,
                    bd_name_list, bd_alias_list, bd_desc_list,
                    app_name_list, app_alias_list, app_desc_list,
                    epg_name_list, epg_alias_list, epg_desc_list
                                )
            all_successful = True
            for tn_name, tn_alias, tn_desc, vrf_name, vrf_alias, vrf_desc, bd_name, bd_alias, bd_desc, app_name, app_alias, app_desc, epg_name, epg_alias, epg_desc  in zip_list:

                    msg, status_code = create_tenant (ip=host, tn_name=tn_name, tn_alias=tn_alias, tn_desc=tn_desc, token=token)
                    if status_code != 200:
                        all_successful=False
                        break
                          
                    msg, status_code = create_vrf (ip=host, tn_name=tn_name,vrf_name=vrf_name, vrf_alias=vrf_alias, vrf_desc=vrf_desc, token=token)
                    if status_code != 200:
                        all_successful=False
                        break

                    msg, status_code = create_bd (ip=host, tn_name=tn_name, vrf_name=vrf_name, bd_name=bd_name, bd_alias=bd_alias,bd_desc=bd_desc, token=token)
                    if status_code != 200:
                        all_successful=False
                        break

                    msg, status_code = create_app (ip=host, tn_name=tn_name, app_name=app_name, app_alias=app_alias, app_desc=app_desc, token=token)
                    if status_code != 200:
                        all_successful=False
                        break

                    msg, status_code = create_epg ( ip=host, tn_name=tn_name, app_name=app_name, bd_name=bd_name, epg_name=epg_name, epg_alias=epg_alias, epg_desc=epg_desc, token=token)
                    if status_code != 200:
                        all_successful=False
                        break
            if all_successful == True:
                result = "Successfully configured :) "
                return result
            else:
                result = "Error is occured :( "
                return result

        except:
            result = "Error is occured :( "
            return result