import docker

SOURCE_IMAGE = ""
NO_CPU = ''
MEMORY_SIZE = ''

CONTAINER_NAME="EXPERMENT"
NO_NODES = 15

testinglist = ["thesis_experment","prom_grafana.1.wli1f8ji1xbzrs099fwecsbbt", "prom_cadvisor.r7oqhkmdyy644stu8sxc7fv8l.fy3le2skald6zlycou23a9y9g"
               ,"prom_alertmanager.1.ra4p45cg4b1tug62eq8lbq9wo", "EXPERMENT101","EXPERMENT106"
               ,"prom_node-exporter.r7oqhkmdyy644stu8sxc7fv8l.xkxysl9no7jc942d4his81h6q", "EXPERMENT103", "EXPERMENT104"
               ,"sad_babbage" 
               ,"EXPERMENT105", "EXPERMENT102"]

def generate_instance_name():
   listContainerName = getcontainerlist()
   #listContainerName = testinglist
   #filter the containers in our experiment
   mycontainers = [name for name in listContainerName if CONTAINER_NAME in name]
   mycontainers.sort()
   if len(mycontainers)>0:
      lastcontainerNo = int(mycontainers[-1][-3:]) #get the last container ID the Id is composed of CONTAINER_NAME+xxx(3 digit no started with 101)
      newContainername = CONTAINER_NAME + str(lastcontainerNo+1)
   else:
      newContainername = CONTAINER_NAME + str(101)
   return newContainername 

def newcontainer():
   #" docker run -dit --name thesis_experment -m 512m -p 8085:80 -v /index.html:/usr/local/apache2/htdocs/ httpd:2.4 "
   #container = client.containers.run("bfirsh/reticulate-splines", detach=True)

   new_containername = generate_instance_name()
   #port = get_portNo()
   #container = client.containers.run("webhost", ["echo", "hello", "world from httpd"],ports={8085:80}, name=new_containername, detach=True)
   container = client.containers.run(new_containername, [],ports={"8095/tcp":8095}, name="kassahun151", detach=True, stdin_open=True,tty=True)
   print(container.id)

def stopcontainers(containerID):
   container = client.containers.get(containerID)
   container.stop()

def pausecontainers(containerID):
   container = client.containers.get(containerID)
   container.pause()

def removecontainers(containerID):
   container = client.containers.get(containerID)
   container.remove()

def getcontainerlist():
   containername =[]
   for container in client.containers.list():
      containername.append(container.name)
      print("ID = ", container.id, "NAME=" ,container.name)
   return containername

def listImages():
   for image in client.images.list():
      print("Images ID = ",image.id, "Image Name = ", image.name)

client = docker.from_env()
getcontainerlist()

'''

print("All instances = ", testinglist)
print("New instance Name = ", generate_instance_name())
'''