#!/usr/bin/env python3
import sys

sys.path.append("lib")

from charms.osm.sshproxy import SSHProxyCharm
from ops.main import main

#todo observerlar
class SampleProxyCharm(SSHProxyCharm):
    def __init__(self, framework, key):
        super().__init__(framework, key)

        # Listen to charm events
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)
        # self.framework.observe(self.on.upgrade_charm, self.on_upgrade_charm)

        # Listen to the touch action event
        # self.framework.observe(self.on.configure_remote_action, self.configure_remote)
        # self.framework.observe(self.on.start_service_action, self.start_service)
        self.framework.observe(self.on.install_asterisk_action,self.install_asterisk)
        self.framework.observe(self.on.config_sip_action,self.config_sip)
        self.framework.observe(self.on.create_sip_account_action,self.create_sip_account)
        self.framework.observe(self.on.add_extention_action,self.add_extention)
        self.framework.observe(self.on.restart_asterisk_action,self.restart_asterisk)
        self.framework.observe(self.on.connect_asterisk_action,self.connect_asterisk)
        self.framework.observe(self.on.connect_running_asterisk_action,self.connect_running_asterisk)

    def on_config_changed(self, event):
        """Handle changes in configuration"""
        super().on_config_changed(event)

    def on_install(self, event):
        """Called when the charm is being installed"""
        super().on_install(event)


    def on_start(self, event):
        """Called when the charm is being started"""
        super().on_start(event)

    # def configure_remote(self, event):
    #     """Configure remote action."""

    #     if self.model.unit.is_leader():
    #         stderr = None
    #         try:
    #             mgmt_ip = self.model.config["ssh-hostname"]
    #             destination_ip = event.params["destination_ip"]
    #             cmd = "vnfcli set license {} server {}".format(
    #                 mgmt_ip,
    #                 destination_ip
    #             )
    #             proxy = self.get_ssh_proxy()
    #             stdout, stderr = proxy.run(cmd)
    #             event.set_results({"output": stdout})
    #         except Exception as e:
    #             event.fail("Action failed {}. Stderr: {}".format(e, stderr))
    #     else:
    #         event.fail("Unit is not leader")

    # def start_service(self, event):
    #     """Start service action."""

    #     if self.model.unit.is_leader():
    #         stderr = None
    #         try:
    #             cmd = "sudo service vnfoper start"
    #             proxy = self.get_ssh_proxy()
    #             stdout, stderr = proxy.run(cmd)
    #             event.set_results({"output": stdout})
    #         except Exception as e:
    #             event.fail("Action failed {}. Stderr: {}".format(e, stderr))
    #     else:
    #         event.fail("Unit is not leader")

    def install_asterisk(self,event):
        stderr = None
        try:
            proxy = self.get_ssh_proxy()
            stdout,stderr = proxy.run("sudo apt-get install asterisk -y")
            event.set_results({"output": stdout})
        except Exception as e:
            event.fail("Action failed {}. Stderr: {}".format(e, stderr))



    def config_sip(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("echo -e \"[general]\ncontext=internal\nallowguest=no\nallowoverlap=no\nbindport=5060\nbindaddr=0.0.0.0\nsrvlookup=no\ndisallow=all\nallow=ulaw\nalwaysauthreject=yes\ncanreinvite=no\nnat=yes\nsession-timers=refuse\nlocalnet=192.168.0.0/255.255.255.0\n \" | sudo tee -a /etc/asterisk/sip.conf")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return           

    def create_sip_account(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                accountId = event.params["accountId"]
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("echo -e \"["+accountId+"]\ntype=friend\nhost=dynamic\nsecret="+accountId+"\ncontext=internal \" | sudo tee -a /etc/asterisk/sip.conf")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return  
    
    def add_extention(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                extensionId = event.params["extensionId"]                
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("echo -e \" [internal]\nexten => "+extensionId+",1,Answer()\nexten => "+extensionId+",2,Dial(SIP/"+extensionId+",60)\nexten => "+extensionId+",3,Playback(vm-nobodyavail)\nexten => "+extensionId+",4,VoiceMail("+extensionId+"@main)\nexten => "+extensionId+",5,Hangup()\n \" | sudo tee -a /etc/asterisk/extensions.conf")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return 

    def restart_asterisk(self,event):
        if self.model.unit.is_leader():
            stderr = None
            try:
                proxy = self.get_ssh_proxy()
                stdout,stderr = proxy.run("sudo systemctl restart asterisk")
                stdout,stderr = proxy.run("sudo systemctl enable asterisk")
                event.set_results({"output":stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))                
        else:
            event.fail("Unit is not leader")
            return           

    def connect_asterisk(self,event):
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

    def connect_running_asterisk(self,event):
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