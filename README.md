# OSM Hackfest 11 Team Asterisk 1 NFV Onboarding 

[OSM Hackfest 11](https://osm.etsi.org/wikipub/index.php/OSM11_Hackfest) Team Asterisk1 vnf onboarding progress. Main task of the Hackfest was onboarding [Asterisk](https://www.asterisk.org/) framework as a Virtual Network Function on OSM infrastructure.

## Installation

Make sure you install osm and have a valid vim account. Clone the repository and run the following commands:

```bash
osm nfpkg-create asteriskOSM_vnf
osm nspkg-create asteriskOSM_ns
osm ns-create --ns_name <asteriskOSM-ns> --nsd_name <asteriskOSM-ns> --vim_account <vim_account_name>
```


## Day 0: VNF Instantiation & Management setup

- Virtual Network Service written as:


![Image of NS](https://github.com/umutcangulmez/AsteriskOSM/blob/main/images/ns.png)

![Image of NS](https://github.com/umutcangulmez/AsteriskOSM/blob/main/images/ns2.png)


- Virtual Network Function (VNF) written as a 2 Virtual Deployment Units. One used for Asterisk in this purpose and the other one to serve as a softphone.  

![Image of VNF](https://github.com/umutcangulmez/AsteriskOSM/blob/main/images/vnf.png)




## Day 1: VNF Services Initialization

[Asterisk VOIP Server Setup](https://www.youtube.com/watch?v=rtHFdhCm434) used for Asterisk setup and config. Config file written line by line but It should have been written as a function that uploads given config file to asterisk path.



```python
# Asterisk Setup
def installasterisk(self,event):
    ...
    proxy = self.get_ssh_proxy()
    stdout,stderr = proxy.run("sudo apt-get update")
    stdout,stderr = proxy.run("sudo apt-get upgrade -y")
    stdout,stderr = proxy.run("sudo apt-get install asterisk -y")
    ...
```

```python
# To write a config file the following method used. However it shouldn't be the way to do it, due to time constraints this method was used.  
def configsip(self,event):
    ...
    proxy = self.get_ssh_proxy()
    stdout,stderr = proxy.run("printf '[general]' | sudo tee -a /etc/asterisk/sip.conf")
    stdout,stderr = proxy.run("echo | sudo tee -a /etc/asterisk/sip.conf")
    ...
```




## Day 2: VNF Runtime Operations

Adding an extension to a user, creating a SIP account and restarting asterisk service is written as a Runtime Operations.

```python
def addextension(self,event):
    ...
    extension = event.params["extensionId"]                
    extensionId = str(extension)
    cmd = "printf 'exten => "+extensionId+",1,Answer()' | sudo tee -a /etc/asterisk/extensions.conf"    
    stdout,stderr = proxy.run(cmd)
    ...
```

```python
def createsipaccount(self,event):
    ...
    account = event.params["accountId"]
    accountId = str(account)
    stdout,stderr = proxy.run("printf '["+accountId+"]' | sudo tee -a /etc/asterisk/sip.conf")
    stdout,stderr = proxy.run("echo | sudo tee -a /etc/asterisk/sip.conf")    
    ...
```


```python
def restartasterisk(self,event):
    ...
    proxy = self.get_ssh_proxy()
    stdout,stderr = proxy.run("sudo systemctl restart asterisk")
    ...
```

After initial-config-primitives run, you can ssh into vnf and see whether Asterisk is running:


![Asterisk](https://github.com/umutcangulmez/AsteriskOSM/blob/main/images/asterisk.png)



## Known Issues

- The following snippet needs to run in installation of Asterisk. However, running sed commands with using framework function somehow gives an error. This issue needs to be solved for the future.

```python
def installasterisk(self,event):
    ...
    cmd = "sudo sed -i 's\";\[radius\]\"\[radius\]\"g' /etc/asterisk/cdr.conf"
    stdout,stderr = proxy.run(cmd)
    cmd = "sudo sed -i 's\";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf\"radiuscfg => /etc/radcli/radiusclient.conf\"g' /etc/asterisk/cdr.conf"
    stdout,stderr = proxy.run(cmd)
    cmd = "sudo sed -i 's\";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf\"radiuscfg => /etc/radcli/radiusclient.conf\"g' /etc/asterisk/cel.conf"
    stdout,stderr = proxy.run(cmd)
    ...
```



## Troubleshooting

- Using endline in printf or echo command doesn't give desired behaviour. Because of that after the command single echo command is called.   

```python
def installasterisk(self,event):
    ...
    stdout,stderr = proxy.run("printf '["+accountId+"] \n' | sudo tee -a /etc/asterisk/sip.conf")
    stdout,stderr = proxy.run("echo | sudo tee -a /etc/asterisk/sip.conf")   
    ...
```

- Bad action name error appears due to underscore usage in function names. 

```bash
Operation: INSTANTIATING.042be29f-7a58-4b48-b98f-0360b2bfb0c2, Stage 2/5: deployment of KDUs, VMs and execution environments. Detail: Deploying VCA 1.: Install
 configuration Software Error desploying charm into ee=4d0ee0c5-79d4-4c5c-a7cc-04b8e8a5827f.app-vnf-fb0869d79d-z0.0 : {"error":"cannot upload charm: invalid charm 
 archive: bad action name add_extention","error-code":"bad request"}. Deploying VCA 2.: Install configuration Software Error desploying charm into 
 ee=4d0ee0c5-79d4-4c5c-a7cc-04b8e8a5827f.app-vnf-268d1b3507-z0.1 : {"error":"cannot upload charm: invalid charm archive: bad action name restart_asterisk","error-code":"
 bad request"}
```


- The hook failed: "install" error solved by copying src/charm.py to hooks/install,hooks/start and hooks/upgrade-charm files. Constructing symbolic link to src/charm.py could be a solution too. 

![Hook Install Failure](https://github.com/umutcangulmez/AsteriskOSM/blob/main/images/hookinstallfailure.png)



- Following commands are very useful for day1/2 primitive debugging. They show whether functions called complete,running or failed. Also the show-action-output shows the output of the charm function. 
```bash
juju show-action-status --model <model-id> 
juju show-action-output --model <model-id> <action-id>
```

## Future Work 

Missing features needs to be implemented for better usage:

- Removing a SIP account and extension given sip account id. 
- Uploading the config file to service instead of writing config line by line using ssh proxy.
- Softphone software needs to be installed on Softphone VDU.
- Sed commands errors need to be solved. 



## License
[MIT](https://choosealicense.com/licenses/mit/)
