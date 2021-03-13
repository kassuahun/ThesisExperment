
import ipaddres 
import json 

NETWORK="netsys_net" 
FLAVOR="m1.medium" 
SOURCE_IMAGE="Ubuntu 18.04" 
isinstancecount = 2
with open("/.ssh/id_rsa.pub") as file: 
    SSH_PUBLIC_KEY = file.read() 

def generate_ip(): 
    regex="\b(10)\.(10)\.(26)\.([0-254]?)\b" 
    #allowed IP= 10.10.26.1 - 10.10.26.254 needs some issue with try and error 
    ip=ipaddress.ip_address(regex) 
    return ip 

def generate_instance_name(): 
    isinstancecount += 1 
    instance_name='Worker_Node'+isinstancecount 
    return instance_name 
'''
subprocess.call(["apt","install","python3-pip"]) 
subprocess.call(["pip3", "install", "python-openstackclient"]) 
subprocess.call(["openstack", "keypair", "create", "--public-key", SSH_PUBLIC_KEY, "HighPerformanceTilesSshKey"]) 

#This function is not working at oslomet openstacks I guss due to security restriction
#we can use MLN excution as an alternative
def createInstance(): 
    subprocess.call(["openstack","server","create", "--flavor", FLAVOR,  "--image",SOURCE_IMAGE, "--key-name", "HighPerformanceTilesSshKey", 
    "--security-group", "default","--nic", NETWORK, instance_name]) 
    return instance_name 
'''

def stopInstance(): 
    INSTANCE_TO_BE_STOPPED=subprocess.call(["nova", "show", "name"])  
    CURRENT_STATUS=subprocess.call(["openstack","server","show", INSTANCE_TO_BE_STOPPED, "-f", "value", "-c", "status"]) 
    if(CURRENT_STATUS=='ACTIVE'): 
        subprocess.call(["nova", "shelve", INSTANCE_TO_BE_STOPPED]) #This is to stop (shelve) an instance  

def onLoadContainer(): 
    subprocess.call(["docker", "service", "create", "-publish-add","80","-- replicas", "-4", "HighPerformanceTilesWebService"]) 
    container_detail_json_array=subprocess.call(["docker", "service", "inspect", "HighPerformanceTilesWebService"]) 
    #This is to get a detail about the new added container in json format  #for further data processing 
    container_object = json.load(container_detail_json_array)  
    for container_name in container_object: 
        if container_name['name']=='HighPerformanceTilesWebService':  
            container_id=container_name['id'] 
    return container_id  

def OffLoadContainer(): 
    list_of_containers=json.dumps(subprocess.call(["docker", "service", "ls"])) 
    #This is to change the ls output (list) to json array 
    for container_name in list_of_containers: 
        container_id = container_name['id'] 
        active_containers = subprocess.call(["docker","service","inspect",container_id]) 

    for container_mode in active_containers: 
        container_mode_status = container_mode['Mode'] 
        if container_mode_status == "Replicated": 
            number_of_replicas = container_mode['Mode'['Replicas']]  
            if number_of_replicas<=2: 
                #If <=2 the container is running (assigned to) less tasks #just as threshold value 
                container_id_to_be_offloaded = container_name['id']  
                subprocess.call(["docker", "service", "scale", container_id_to_be_offloaded, "0"]) 

 
#this function needs modification to implment diff algorithm
def scaleExecutor(): 
    number_of_http_requests= 10000 
    #The number of http_reqests must be retrieved from a report like a  #report from Prometheus
    number_of_available_servers= 3 
    #This also must be retrieved from a report. I just want to show how the  #algorithm works 
    server_capacity= 2000 
    #let's assume that a single node can handle 2000 requests, the real data can be collected via tools like promotous 
    scale_flag="undefined" 
    while scale_flag == "optimized": 
        number_of_required_servers = number_of_http_requests/server_capacity  
        if number_of_required_servers > number_of_available_servers:  
            createInstance() 
            onLoadContainer() 
            scale_flag = "scale-up" 
        elif number_of_required_servers < number_of_available_servers:
            stopInstance() 
            OffLoadContainer() 
            scale_flag = "scale-down" 
        else: 
            scale_flag = "optimized"