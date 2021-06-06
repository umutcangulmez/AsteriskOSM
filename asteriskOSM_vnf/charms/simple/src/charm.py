#!/usr/bin/env python3
import sys

sys.path.append("lib")

from charms.osm.sshproxy import SSHProxyCharm
from ops.main import main
import subprocess

#todo observerlar
class SampleProxyCharm(SSHProxyCharm):
    def __init__(self, framework, key):
        super().__init__(framework, key)

        # Listen to charm events
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)
        # self.framework.observe(self.on.upgrade_charm, self.on_upgrade_charm)


        self.framework.observe(self.on.installasterisk_action,self.installasterisk)
        self.framework.observe(self.on.configsip_action,self.configsip)
        self.framework.observe(self.on.createsipaccount_action,self.createsipaccount)
        self.framework.observe(self.on.addextension_action,self.addextension)
        self.framework.observe(self.on.restartasterisk_action,self.restartasterisk)
        self.framework.observe(self.on.connectasterisk_action,self.connectasterisk)
        self.framework.observe(self.on.connectrunningasterisk_action,self.connectrunningasterisk)

    def on_config_changed(self, event):
        """Handle changes in configuration"""
        super().on_config_changed(event)

    def on_install(self, event):
        """Called when the charm is being installed"""
        super().on_install(event)


    def on_start(self, event):
        """Called when the charm is being started"""
        super().on_start(event)


    def installasterisk(self,event):
        stderr = None
        try:
            proxy = self.get_ssh_proxy()
            # commented due to touch trials 
            # stdout,stderr = proxy.run("sudo apt-get update")
            # stdout,stderr = proxy.run("sudo apt-get upgrade -y")
            # stdout,stderr = proxy.run("sudo apt-get install asterisk -y")
            stdout,stderr = proxy.run("touch first")
            stdout,stderr = proxy.run("echo \"aa\" | tee -a /home/ubuntu/first")


            # cmd = "sudo sed -i 's\";\\[radius\\]\"\\[radius\\]\"g' /etc/asterisk/cdr.conf"
            # stdout,stderr = proxy.run(cmd)            
            event.set_results({"output": stdout})
        except Exception as e:
            event.fail("Action failed {}. Stderr: {}".format(e, stderr))



    def configsip(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                proxy = self.get_ssh_proxy()
                # cmd = "sudo sed -i 's\";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf\"radiuscfg => /etc/radcli/radiusclient.conf\"g' /etc/asterisk/cdr.conf"
                # stdout,stderr = proxy.run(cmd)
                # cmd = "sudo sed -i 's\";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf\"radiuscfg => /etc/radcli/radiusclient.conf\"g' /etc/asterisk/cel.conf"
                # stdout,stderr = proxy.run(cmd)                
                stdout,stderr = proxy.run("echo -e \"[general]\ncontext=internal\nallowguest=no\nallowoverlap=no\nbindport=5060\nbindaddr=0.0.0.0\nsrvlookup=no\ndisallow=all\nallow=ulaw\nalwaysauthreject=yes\ncanreinvite=no\nnat=yes\nsession-timers=refuse\nlocalnet=192.168.0.0/255.255.255.0 \" | sudo tee -a /etc/asterisk/sip.conf")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return           

    def createsipaccount(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:

                account = event.params["accountId"]
                accountId = str(account)
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("echo -e \"["+accountId+"]\ntype=friend\nhost=dynamic\nsecret="+accountId+"\ncontext=internal \" | sudo tee -a /etc/asterisk/sip.conf")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return  
    
    def addextension(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                extension = event.params["extensionId"]                
                extensionsId = str(extension)
                cmd = "echo -e \" [internal]\nexten => "+extensionId+",1,Answer()\nexten => "+extensionId+",2,Dial(SIP/"+extensionId+",60)\nexten => "+extensionId+",3,Playback(vm-nobodyavail)\nexten => "+extensionId+",4,VoiceMail("+extensionId+"@main)\nexten => "+extensionId+",5,Hangup() \" | sudo tee -a /etc/asterisk/extensions.conf"
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run(cmd)
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return 

    def restartasterisk(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                proxy = self.get_ssh_proxy()
                # cmd = "sudo sed -i 's\";\[radius\]\"\[radius\]\"g' /etc/asterisk/cdr.conf"
                # stdout,stderr = proxy.run(cmd)
                # cmd = "sudo sed -i 's\";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf\"radiuscfg => /etc/radcli/radiusclient.conf\"g' /etc/asterisk/cdr.conf"
                # stdout,stderr = proxy.run(cmd)
                # cmd = "sudo sed -i 's\";radiuscfg => /usr/local/etc/radiusclient-ng/radiusclient.conf\"radiuscfg => /etc/radcli/radiusclient.conf\"g' /etc/asterisk/cel.conf"
                # stdout,stderr = proxy.run(cmd)

                stdout,stderr = proxy.run("sudo systemctl restart asterisk")
                stdout,stderr = proxy.run("sudo systemctl enable asterisk")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return           

    def connectasterisk(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("sudo asterisk -cvvvvv")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return       

    def connectrunningasterisk(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("sudo asterisk -rx \"core restart now\" ")
                stdout,stderr = proxy.run("sudo asterisk -rvvvvv ")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return  

#todo call kismi eksik


if __name__ == "__main__":
    main(SampleProxyCharm)