# Summer 2021 DevNet Associate Preperation Webinar Series: Enforcing Interface Configuration Standards through Automation
This repository provides code and examples as part of a [DevNet Associate Certification Preparation Webinar Series](https://learningnetwork.cisco.com/s/article/devnet-associate-prep-program-in-one-place). The recording for this webinar, and others, can be found in the [DevNet Associate Prep Program Training Plan](https://learningnetwork.cisco.com/s/learning-plan-detail-standard?ltui__urlRecordId=a1c3i0000007q9cAAA&ltui__urlRedirect=learning-plan-detail-standard&t=1596603514739).

### Enforcing Interface Configuration Standards through Automation

> You are walking out of root cause analysis readout meeting from last weeks network down situation when the network architect walks up. Like so many before, this outage was partially caused by inconsistent configuration in the network. It’ll be a big project to fully resolve, but she asks if you can come up with a way to update interface descriptions across the network based on the CSV “Source of Truth”.

## Using this repository 
If you'd like to explore the solution to the above use case yourself, here is everything you should need to know.  

### Lab/Sandbox Resources 
This example leverages the [Cisco NSO Reservable Sandbox from DevNet](https://devnetsandbox.cisco.com/RM/Diagram/Index/43964e62-a13c-4929-bde7-a2f68ad6b27c?diagramType=Topology).  You can reserve this sandbox for use with the [nso_sandbox_devices.xlsx](nso_sandbox_devices.xlsx) inventory spreadsheet.  

If you have your own lab you'd like to try the network inventory script on, you will need to create your own inventory spreadsheet and CSV based Source of Truth for your lab.  This use case should support devices running Cisco IOS, IOS XE, IOS XR, and NX-OS.

> Note: Even if you'd like to replicate this on your own lab, it is suggested to test with the Sandbox first to understand how the code and use case works.

### Creating the Python venv 
While other versions of Python will likley work, this use case was tested with Python 3.8.  It leverages [pyATS](https://developer.cisco.com/pyats) for interacting with network devices and Jinja2 for creating configuration templates.

```
# Create your Virtual Env
python3 -m venv venv
source venv/bin/activate
# Install the entire pyATS set of tools
pip install pyats[full] jinja2
# Install just the basics for this exercise
pip install pyats pyats.contrib genie jinja2
```

### Creating the pyATS Testbed File 
The pyATS YAML testbed is included with the GitHub repo, but you can create one from the Excel file with this command. 

```
pyats create testbed file \
--path nso_sandbox_devices.xlsx \
--output nso_sandbox_testbed.yaml
```

Some suggested improvements to the created testbed file include: 

* Move credentials from each device to testbed level
* `ASK{}` for Username as well as passwords

These changes are included in the [`improved_nso_sandbox_testbed.yaml`](improved_nso_sandbox_testbed.yaml) file. 

### Running the `network_inventory.py` script 
The [`config_interface_descriptions.py`](config_interface_descriptions.py) script in the repo should work and be ready to go.  

> Note: The sandbox credentials for devices are `cisco / cisco`

The script uses the Python argparse module to take arguments for processing.  

```
./config_interface_descriptions.py --help

# Output
Deploying standard interface descriptions to network.
usage: config_interface_descriptions.py [-h] --testbed TESTBED --sot SOT [--apply] [--check-neighbors]

Deploying standard interface descriptions to network.

optional arguments:
  -h, --help         show this help message and exit
  --testbed TESTBED  pyATS Testbed File
  --sot SOT          Interface Connection Source of Truth Spreadsheet
  --apply            Should configurations be applied to network. If not set, config not applied.
  --check-neighbors  Should we try to use LLDP to verify interface neighbors. Default is NO.
```

See the output from the help command to understand the inputs required. 

```
./config_interface_descriptions.py --testbed improved_nso_sandbox_testbed.yaml \
    --sot interface-connections-source-of-truth.csv \
    --check-neighbors --apply
```

<details>
  <summary>Click to See Sample Output from the Script</summary>
  
```
Deploying standard interface descriptions to network.
Generating interface descriptions from file interface-connections-source-of-truth.csv for testbed improved_nso_sandbox_testbed.yaml.
Configurations will be applied to network devices.

Opening and readying Source of Truth File.

Device edge-sw01       Interface GigabitEthernet0/1        SOT connection: edge-firewall01 GigabitEthernet0/1
Device edge-sw01       Interface GigabitEthernet0/2        SOT connection: core-rtr01 GigabitEthernet0/0/0/1
Device edge-sw01       Interface GigabitEthernet0/3        SOT connection: core-rtr02 GigabitEthernet0/0/0/1
Device edge-sw01       Interface GigabitEthernet0/0        SOT connection: oob-mgmt GigabitEthernet1/1
Device core-rtr01      Interface GigabitEthernet0/0/0/0    SOT connection: core-rtr02 GigabitEthernet0/0/0/0
Device core-rtr01      Interface GigabitEthernet0/0/0/1    SOT connection: edge-sw01 GigabitEthernet0/2
Device core-rtr01      Interface GigabitEthernet0/0/0/2    SOT connection: dist-rtr01 GigabitEthernet2
Device core-rtr01      Interface GigabitEthernet0/0/0/3    SOT connection: dist-rtr02 GigabitEthernet2
Device core-rtr01      Interface MgmtEth 0/0/CPU0/0        SOT connection: oob-mgmt GigabitEthernet1/2
Device core-rtr02      Interface GigabitEthernet0/0/0/0    SOT connection: core-rtr01 GigabitEthernet0/0/0/0
Device core-rtr02      Interface GigabitEthernet0/0/0/1    SOT connection: edge-sw01 GigabitEthernet0/3
Device core-rtr02      Interface GigabitEthernet0/0/0/2    SOT connection: dist-rtr01 GigabitEthernet3
Device core-rtr02      Interface GigabitEthernet0/0/0/3    SOT connection: dist-rtr02 GigabitEthernet3
Device core-rtr02      Interface MgmtEth 0/0/CPU0/0        SOT connection: oob-mgmt GigabitEthernet1/3
Device dist-rtr01      Interface GigabitEthernet2          SOT connection: core-rtr01 GigabitEthernet0/0/0/2
Device dist-rtr01      Interface GigabitEthernet3          SOT connection: core-rtr02 GigabitEthernet0/0/0/2
Device dist-rtr01      Interface GigabitEthernet4          SOT connection: dist-sw01 Ethernet1/3
Device dist-rtr01      Interface GigabitEthernet5          SOT connection: dist-sw02 Ethernet1/3
Device dist-rtr01      Interface GigabitEthernet6          SOT connection: dist-rtr02 GigabitEthernet6
Device dist-rtr01      Interface GigabitEthernet1          SOT connection: oob-mgmt GigabitEthernet1/4
Device dist-rtr02      Interface GigabitEthernet2          SOT connection: core-rtr01 GigabitEthernet0/0/0/3
Device dist-rtr02      Interface GigabitEthernet3          SOT connection: core-rtr02 GigabitEthernet0/0/0/3
Device dist-rtr02      Interface GigabitEthernet4          SOT connection: dist-sw01 Ethernet1/4
Device dist-rtr02      Interface GigabitEthernet5          SOT connection: dist-sw02 Ethernet1/4
Device dist-rtr02      Interface GigabitEthernet6          SOT connection: dist-rtr02 GigabitEthernet6
Device dist-rtr02      Interface GigabitEthernet1          SOT connection: oob-mgmt GigabitEthernet1/5
Device dist-sw01       Interface Ethernet1/1               SOT connection: dist-sw02 Ethernet1/1
Device dist-sw01       Interface Ethernet1/2               SOT connection: dist-sw02 Ethernet1/2
Device dist-sw01       Interface Ethernet1/3               SOT connection: dist-rtr01 GigabitEthernet4
Device dist-sw01       Interface Ethernet1/4               SOT connection: dist-rtr02 GigabitEthernet4
Device dist-sw01       Interface Ethernet1/11              SOT connection: inside-host01 ensp0s2
Device dist-sw01       Interface Mgmt 0                    SOT connection: oob-mgmt GigabitEthernet1/6
Device dist-sw02       Interface Ethernet1/1               SOT connection: dist-sw01 Ethernet1/1
Device dist-sw02       Interface Ethernet1/2               SOT connection: dist-sw01 Ethernet1/2
Device dist-sw02       Interface Ethernet1/3               SOT connection: dist-rtr01 GigabitEthernet5
Device dist-sw02       Interface Ethernet1/4               SOT connection: dist-rtr02 GigabitEthernet5
Device dist-sw02       Interface Ethernet1/11              SOT connection: inside-host02 ensp0s2
Device dist-sw02       Interface Mgmt 0                    SOT connection: oob-mgmt GigabitEthernet1/7

Loading testbed file improved_nso_sandbox_testbed.yaml
Connecting to all devices in testbed improved_nso_sandbox_testbed
Learning current interface state for device edge-sw01
Learning current interface state for device core-rtr01
Learning current interface state for device core-rtr02
Learning current interface state for device dist-rtr01
Learning current interface state for device dist-rtr02
Learning current interface state for device dist-sw01
Learning current interface state for device dist-sw02

New Device Configurations for Interface Descriptions
----------------------------------------------------
! Device edge-sw01
interface GigabitEthernet0/1
  description Connected to edge-firewall01 GigabitEthernet0/1 - Connection to outbound firewall
interface GigabitEthernet0/2
  description Connected to core-rtr01 GigabitEthernet0/0/0/1 - Primary core router
interface GigabitEthernet0/3
  description Connected to core-rtr02 GigabitEthernet0/0/0/1 - Secondary core router
interface GigabitEthernet0/0
  description Connected to oob-mgmt GigabitEthernet1/1 - Management network
!

Would you like to apply this configuration to device edge-sw01 (y/n)? y
Applying configuration to device edge-sw01.

----------------------------------------------------

! Device core-rtr01
interface GigabitEthernet0/0/0/0
  description Connected to core-rtr02 GigabitEthernet0/0/0/0 - Peer link to secondary core
interface GigabitEthernet0/0/0/1
  description Connected to edge-sw01 GigabitEthernet0/2 - Path to outside edge
interface GigabitEthernet0/0/0/2
  description Connected to dist-rtr01 GigabitEthernet2 - Path to inside distribution 
interface GigabitEthernet0/0/0/3
  description Connected to dist-rtr02 GigabitEthernet2 - Path to inside distribution 
interface MgmtEth 0/0/CPU0/0
  description Connected to oob-mgmt GigabitEthernet1/2 - Management network
!

Would you like to apply this configuration to device core-rtr01 (y/n)? y
Applying configuration to device core-rtr01.

----------------------------------------------------

! Device core-rtr02
interface GigabitEthernet0/0/0/0
  description Connected to core-rtr01 GigabitEthernet0/0/0/0 - Peer link to primary core
interface GigabitEthernet0/0/0/1
  description Connected to edge-sw01 GigabitEthernet0/3 - Path to outside edge
interface GigabitEthernet0/0/0/2
  description Connected to dist-rtr01 GigabitEthernet3 - Path to inside distribution 
interface GigabitEthernet0/0/0/3
  description Connected to dist-rtr02 GigabitEthernet3 - Path to inside distribution 
interface MgmtEth 0/0/CPU0/0
  description Connected to oob-mgmt GigabitEthernet1/3 - Management network
!

Would you like to apply this configuration to device core-rtr02 (y/n)? y
Applying configuration to device core-rtr02.

----------------------------------------------------

! Device dist-rtr01
interface GigabitEthernet2
  description Connected to core-rtr01 GigabitEthernet0/0/0/2 - Path to core
interface GigabitEthernet3
  description Connected to core-rtr02 GigabitEthernet0/0/0/2 - Path to core
interface GigabitEthernet4
  description Connected to dist-sw01 Ethernet1/3 - Path to distribution switch 01
interface GigabitEthernet5
  description Connected to dist-sw02 Ethernet1/3 - Path to distribution switch 02
interface GigabitEthernet6
  description Connected to dist-rtr02 GigabitEthernet6 - Peer link to distribution router
interface GigabitEthernet1
  description Connected to oob-mgmt GigabitEthernet1/4 - Management network
!

Would you like to apply this configuration to device dist-rtr01 (y/n)? y
Applying configuration to device dist-rtr01.

----------------------------------------------------

! Device dist-rtr02
interface GigabitEthernet2
  description Connected to core-rtr01 GigabitEthernet0/0/0/3 - Path to core
interface GigabitEthernet3
  description Connected to core-rtr02 GigabitEthernet0/0/0/3 - Path to core
interface GigabitEthernet4
  description Connected to dist-sw01 Ethernet1/4 - Path to distribution switch 01
interface GigabitEthernet5
  description Connected to dist-sw02 Ethernet1/4 - Path to distribution switch 02
interface GigabitEthernet6
  description Connected to dist-rtr02 GigabitEthernet6 - Peer link to distribution router
interface GigabitEthernet1
  description Connected to oob-mgmt GigabitEthernet1/5 - Management network
!

Would you like to apply this configuration to device dist-rtr02 (y/n)? y
Applying configuration to device dist-rtr02.

----------------------------------------------------

! Device dist-sw01
interface Ethernet1/1
  description Connected to dist-sw02 Ethernet1/1 - Peer link to distribution switch 02
interface Ethernet1/2
  description Connected to dist-sw02 Ethernet1/2 - Peer link to distribution switch 02
interface Ethernet1/3
  description Connected to dist-rtr01 GigabitEthernet4 - Path to distribution router
interface Ethernet1/4
  description Connected to dist-rtr02 GigabitEthernet4 - Path to distribution router
interface Ethernet1/11
  description Connected to inside-host01 ensp0s2 - Access port for inside-host
interface Mgmt 0
  description Connected to oob-mgmt GigabitEthernet1/6 - Management network
!

Would you like to apply this configuration to device dist-sw01 (y/n)? y
Applying configuration to device dist-sw01.

----------------------------------------------------

! Device dist-sw02
interface Ethernet1/1
  description Connected to dist-sw01 Ethernet1/1 - Peer link to distribution switch 01
interface Ethernet1/2
  description Connected to dist-sw01 Ethernet1/2 - Peer link to distribution switch 01
interface Ethernet1/3
  description Connected to dist-rtr01 GigabitEthernet5 - Path to distribution router
interface Ethernet1/4
  description Connected to dist-rtr02 GigabitEthernet5 - Path to distribution router
interface Ethernet1/11
  description Connected to inside-host02 ensp0s2 - Access port for inside-host
interface Mgmt 0
  description Connected to oob-mgmt GigabitEthernet1/7 - Management network
!

Would you like to apply this configuration to device dist-sw02 (y/n)? y
Applying configuration to device dist-sw02.

----------------------------------------------------

Will attempt to check interface neighbors with LLDP.
Configuring LLDP on edge-sw01
Learning LLDP Neighbor Details from on edge-sw01
Configuring LLDP on core-rtr01
Learning LLDP Neighbor Details from on core-rtr01
Configuring LLDP on core-rtr02
Learning LLDP Neighbor Details from on core-rtr02
Configuring LLDP on dist-rtr01
Learning LLDP Neighbor Details from on dist-rtr01
Configuring LLDP on dist-rtr02
Learning LLDP Neighbor Details from on dist-rtr02
Configuring LLDP on dist-sw01
Learning LLDP Neighbor Details from on dist-sw01
Configuring LLDP on dist-sw02
Learning LLDP Neighbor Details from on dist-sw02
Checking if edge-sw01 GigabitEthernet0/1 is connected to edge-firewall01 GigabitEthernet0/1
  ⚠️ No LLDP Info for interface GigabitEthernet0/1 for device edge-sw01
Checking if edge-sw01 GigabitEthernet0/2 is connected to core-rtr01 GigabitEthernet0/0/0/1
  Interface GigabitEthernet0/2 on device edge-sw01 is connected as expected.
Checking if edge-sw01 GigabitEthernet0/3 is connected to core-rtr02 GigabitEthernet0/0/0/1
  Interface GigabitEthernet0/3 on device edge-sw01 is connected as expected.
Checking if edge-sw01 GigabitEthernet0/0 is connected to oob-mgmt GigabitEthernet1/1
  ⚠️ No LLDP Info for interface GigabitEthernet0/0 for device edge-sw01
Checking if core-rtr01 GigabitEthernet0/0/0/0 is connected to core-rtr02 GigabitEthernet0/0/0/0
  Interface GigabitEthernet0/0/0/0 on device core-rtr01 is connected as expected.
Checking if core-rtr01 GigabitEthernet0/0/0/1 is connected to edge-sw01 GigabitEthernet0/2
  Interface GigabitEthernet0/0/0/1 on device core-rtr01 is connected as expected.
Checking if core-rtr01 GigabitEthernet0/0/0/2 is connected to dist-rtr01 GigabitEthernet2
  Interface GigabitEthernet0/0/0/2 on device core-rtr01 is connected as expected.
Checking if core-rtr01 GigabitEthernet0/0/0/3 is connected to dist-rtr02 GigabitEthernet2
  Interface GigabitEthernet0/0/0/3 on device core-rtr01 is connected as expected.
Checking if core-rtr01 MgmtEth 0/0/CPU0/0 is connected to oob-mgmt GigabitEthernet1/2
  ⚠️ No LLDP Info for interface MgmtEth 0/0/CPU0/0 for device core-rtr01
Checking if core-rtr02 GigabitEthernet0/0/0/0 is connected to core-rtr01 GigabitEthernet0/0/0/0
  Interface GigabitEthernet0/0/0/0 on device core-rtr02 is connected as expected.
Checking if core-rtr02 GigabitEthernet0/0/0/1 is connected to edge-sw01 GigabitEthernet0/3
  Interface GigabitEthernet0/0/0/1 on device core-rtr02 is connected as expected.
Checking if core-rtr02 GigabitEthernet0/0/0/2 is connected to dist-rtr01 GigabitEthernet3
  Interface GigabitEthernet0/0/0/2 on device core-rtr02 is connected as expected.
Checking if core-rtr02 GigabitEthernet0/0/0/3 is connected to dist-rtr02 GigabitEthernet3
  Interface GigabitEthernet0/0/0/3 on device core-rtr02 is connected as expected.
Checking if core-rtr02 MgmtEth 0/0/CPU0/0 is connected to oob-mgmt GigabitEthernet1/3
  ⚠️ No LLDP Info for interface MgmtEth 0/0/CPU0/0 for device core-rtr02
Checking if dist-rtr01 GigabitEthernet2 is connected to core-rtr01 GigabitEthernet0/0/0/2
  Interface GigabitEthernet2 on device dist-rtr01 is connected as expected.
Checking if dist-rtr01 GigabitEthernet3 is connected to core-rtr02 GigabitEthernet0/0/0/2
  Interface GigabitEthernet3 on device dist-rtr01 is connected as expected.
Checking if dist-rtr01 GigabitEthernet4 is connected to dist-sw01 Ethernet1/3
  Interface GigabitEthernet4 on device dist-rtr01 is connected as expected.
Checking if dist-rtr01 GigabitEthernet5 is connected to dist-sw02 Ethernet1/3
  Interface GigabitEthernet5 on device dist-rtr01 is connected as expected.
Checking if dist-rtr01 GigabitEthernet6 is connected to dist-rtr02 GigabitEthernet6
  Interface GigabitEthernet6 on device dist-rtr01 is connected as expected.
Checking if dist-rtr01 GigabitEthernet1 is connected to oob-mgmt GigabitEthernet1/4
  ⚠️ No LLDP Info for interface GigabitEthernet1 for device dist-rtr01
Checking if dist-rtr02 GigabitEthernet2 is connected to core-rtr01 GigabitEthernet0/0/0/3
  Interface GigabitEthernet2 on device dist-rtr02 is connected as expected.
Checking if dist-rtr02 GigabitEthernet3 is connected to core-rtr02 GigabitEthernet0/0/0/3
  Interface GigabitEthernet3 on device dist-rtr02 is connected as expected.
Checking if dist-rtr02 GigabitEthernet4 is connected to dist-sw01 Ethernet1/4
  Interface GigabitEthernet4 on device dist-rtr02 is connected as expected.
Checking if dist-rtr02 GigabitEthernet5 is connected to dist-sw02 Ethernet1/4
  Interface GigabitEthernet5 on device dist-rtr02 is connected as expected.
Checking if dist-rtr02 GigabitEthernet6 is connected to dist-rtr02 GigabitEthernet6
  ⚠️ Interface GigabitEthernet6 on device dist-rtr02 is NOT connected as expected.
Checking if dist-rtr02 GigabitEthernet1 is connected to oob-mgmt GigabitEthernet1/5
  ⚠️ No LLDP Info for interface GigabitEthernet1 for device dist-rtr02
Checking if dist-sw01 Ethernet1/1 is connected to dist-sw02 Ethernet1/1
  Interface Ethernet1/1 on device dist-sw01 is connected as expected.
Checking if dist-sw01 Ethernet1/2 is connected to dist-sw02 Ethernet1/2
  Interface Ethernet1/2 on device dist-sw01 is connected as expected.
Checking if dist-sw01 Ethernet1/3 is connected to dist-rtr01 GigabitEthernet4
  Interface Ethernet1/3 on device dist-sw01 is connected as expected.
Checking if dist-sw01 Ethernet1/4 is connected to dist-rtr02 GigabitEthernet4
  Interface Ethernet1/4 on device dist-sw01 is connected as expected.
Checking if dist-sw01 Ethernet1/11 is connected to inside-host01 ensp0s2
  ⚠️ No LLDP Info for interface Ethernet1/11 for device dist-sw01
Checking if dist-sw01 Mgmt 0 is connected to oob-mgmt GigabitEthernet1/6
  ⚠️ No LLDP Info for interface Mgmt 0 for device dist-sw01
Checking if dist-sw02 Ethernet1/1 is connected to dist-sw01 Ethernet1/1
  Interface Ethernet1/1 on device dist-sw02 is connected as expected.
Checking if dist-sw02 Ethernet1/2 is connected to dist-sw01 Ethernet1/2
  Interface Ethernet1/2 on device dist-sw02 is connected as expected.
Checking if dist-sw02 Ethernet1/3 is connected to dist-rtr01 GigabitEthernet5
  Interface Ethernet1/3 on device dist-sw02 is connected as expected.
Checking if dist-sw02 Ethernet1/4 is connected to dist-rtr02 GigabitEthernet5
  Interface Ethernet1/4 on device dist-sw02 is connected as expected.
Checking if dist-sw02 Ethernet1/11 is connected to inside-host02 ensp0s2
  ⚠️ No LLDP Info for interface Ethernet1/11 for device dist-sw02
Checking if dist-sw02 Mgmt 0 is connected to oob-mgmt GigabitEthernet1/7
  ⚠️ No LLDP Info for interface Mgmt 0 for device dist-sw02
Disconnecting from devices.
Writing config report to file 2021-06-07-00-39-31_interface_config_report.csv.
```
</details>

> Or view the [`example-configuration-script-output.txt`](example-configuration-script-output.txt) file in the repository.

And it will create a CSV report that looks like 

```csv
Device Name,Interface,Connected Device,Connected Interface,Purpose,Previous Interface Description,LLDP Neighbor Check Test
edge-sw01,GigabitEthernet0/1,edge-firewall01,GigabitEthernet0/1,Connection to outbound firewall,Connected to edge-firewall01 GigabitEthernet0/1 - Connection to outbound firewall,Unknown - No LLDP Info for Interface
edge-sw01,GigabitEthernet0/2,core-rtr01,GigabitEthernet0/0/0/1,Primary core router,Connected to core-rtr01 GigabitEthernet0/0/0/1 - Primary core router,Confirmed
edge-sw01,GigabitEthernet0/3,core-rtr02,GigabitEthernet0/0/0/1,Secondary core router,to GigabitEthernet0/0/0/1.core-rtr02,Confirmed
edge-sw01,GigabitEthernet0/0,oob-mgmt,GigabitEthernet1/1,Management network,to port3.sandbox-backend,Unknown - No LLDP Info for Interface
,,,,,,LLDP Test Not Run.
core-rtr01,GigabitEthernet0/0/0/0,core-rtr02,GigabitEthernet0/0/0/0,Peer link to secondary core,Connected to core-rtr02 GigabitEthernet0/0/0/0 - Peer link to secondary core,Confirmed
core-rtr01,GigabitEthernet0/0/0/1,edge-sw01,GigabitEthernet0/2,Path to outside edge,Connected to edge-sw01 GigabitEthernet0/2 - Path to outside edge,Confirmed
core-rtr01,GigabitEthernet0/0/0/2,dist-rtr01,GigabitEthernet2,Path to inside distribution ,Connected to dist-rtr01 GigabitEthernet2 - Path to inside distribution,Confirmed
core-rtr01,GigabitEthernet0/0/0/3,dist-rtr02,GigabitEthernet2,Path to inside distribution ,Connected to dist-rtr02 GigabitEthernet2 - Path to inside distribution,Confirmed
core-rtr01,MgmtEth 0/0/CPU0/0,oob-mgmt,GigabitEthernet1/2,Management network,,Unknown - No LLDP Info for Interface
,,,,,,LLDP Test Not Run.
core-rtr02,GigabitEthernet0/0/0/0,core-rtr01,GigabitEthernet0/0/0/0,Peer link to primary core,L3 Link to core-rtr01,Confirmed
core-rtr02,GigabitEthernet0/0/0/1,edge-sw01,GigabitEthernet0/3,Path to outside edge,L3 Link to edge-sw01,Confirmed
core-rtr02,GigabitEthernet0/0/0/2,dist-rtr01,GigabitEthernet3,Path to inside distribution ,L3 Link to dist-rtr01,Confirmed
core-rtr02,GigabitEthernet0/0/0/3,dist-rtr02,GigabitEthernet3,Path to inside distribution ,L3 Link to dist-rtr02,Confirmed
core-rtr02,MgmtEth 0/0/CPU0/0,oob-mgmt,GigabitEthernet1/3,Management network,,Unknown - No LLDP Info for Interface
,,,,,,LLDP Test Not Run.
dist-rtr01,GigabitEthernet2,core-rtr01,GigabitEthernet0/0/0/2,Path to core,Connected to core-rtr01 GigabitEthernet0/0/0/2 - Path to core,Confirmed
dist-rtr01,GigabitEthernet3,core-rtr02,GigabitEthernet0/0/0/2,Path to core,Connected to core-rtr02 GigabitEthernet0/0/0/2 - Path to core,Confirmed
dist-rtr01,GigabitEthernet4,dist-sw01,Ethernet1/3,Path to distribution switch 01,Connected to dist-sw01 Ethernet1/3 - Path to distribution switch 01,Confirmed
dist-rtr01,GigabitEthernet5,dist-sw02,Ethernet1/3,Path to distribution switch 02,Connected to dist-sw02 Ethernet1/3 - Path to distribution switch 02,Confirmed
dist-rtr01,GigabitEthernet6,dist-rtr02,GigabitEthernet6,Peer link to distribution router,Connected to dist-rtr02 GigabitEthernet6 - Peer link to distribution router,Confirmed
dist-rtr01,GigabitEthernet1,oob-mgmt,GigabitEthernet1/4,Management network,Connected to oob-mgmt GigabitEthernet1/4 - Management network,Unknown - No LLDP Info for Interface
,,,,,,LLDP Test Not Run.
dist-rtr02,GigabitEthernet2,core-rtr01,GigabitEthernet0/0/0/3,Path to core,L3 Link to core-rtr01,Confirmed
dist-rtr02,GigabitEthernet3,core-rtr02,GigabitEthernet0/0/0/3,Path to core,L3 Link to core-rtr02,Confirmed
dist-rtr02,GigabitEthernet4,dist-sw01,Ethernet1/4,Path to distribution switch 01,L3 Link to dist-sw01,Confirmed
dist-rtr02,GigabitEthernet5,dist-sw02,Ethernet1/4,Path to distribution switch 02,L3 Link to dist-sw02,Confirmed
dist-rtr02,GigabitEthernet6,dist-rtr02,GigabitEthernet6,Peer link to distribution router,L3 Link to dist-rtr01,Incorrect
dist-rtr02,GigabitEthernet1,oob-mgmt,GigabitEthernet1/5,Management network,to port7.sandbox-backend,Unknown - No LLDP Info for Interface
,,,,,,LLDP Test Not Run.
dist-sw01,Ethernet1/1,dist-sw02,Ethernet1/1,Peer link to distribution switch 02,Connected to dist-sw02 Ethernet1/1 - Peer link to distribution switch 02,Confirmed
dist-sw01,Ethernet1/2,dist-sw02,Ethernet1/2,Peer link to distribution switch 02,Connected to dist-sw02 Ethernet1/2 - Peer link to distribution switch 02,Confirmed
dist-sw01,Ethernet1/3,dist-rtr01,GigabitEthernet4,Path to distribution router,Connected to dist-rtr01 GigabitEthernet4 - Path to distribution router,Confirmed
dist-sw01,Ethernet1/4,dist-rtr02,GigabitEthernet4,Path to distribution router,Connected to dist-rtr02 GigabitEthernet4 - Path to distribution router,Confirmed
dist-sw01,Ethernet1/11,inside-host01,ensp0s2,Access port for inside-host,Connected to inside-host01 ensp0s2 - Access port for inside-host,Unknown - No LLDP Info for Interface
dist-sw01,Mgmt 0,oob-mgmt,GigabitEthernet1/6,Management network,,Unknown - No LLDP Info for Interface
,,,,,,LLDP Test Not Run.
dist-sw02,Ethernet1/1,dist-sw01,Ethernet1/1,Peer link to distribution switch 01,VPC Peer Link,Confirmed
dist-sw02,Ethernet1/2,dist-sw01,Ethernet1/2,Peer link to distribution switch 01,VPC Peer Link,Confirmed
dist-sw02,Ethernet1/3,dist-rtr01,GigabitEthernet5,Path to distribution router,L3 link to dist-rtr01,Confirmed
dist-sw02,Ethernet1/4,dist-rtr02,GigabitEthernet5,Path to distribution router,L3 link to dist-rtr02,Confirmed
dist-sw02,Ethernet1/11,inside-host02,ensp0s2,Access port for inside-host,Link to inside-host02,Unknown - No LLDP Info for Interface
dist-sw02,Mgmt 0,oob-mgmt,GigabitEthernet1/7,Management network,,Unknown - No LLDP Info for Interface
```

> Or view the [`example_interface_config_report.csv`](example_interface_config_report.csv) file in the repository.


## Following the development process 
If you'd like to see how the script was built, you can look at the commit log on the `config_interface_descriptions.py` file, or explore the files in the [`development-steps`](development-steps/) folder.  You'll find numbered files showing how the script was build, step by step, that you can run individually, or use as resources to create your own file.  

```
ls -l development-steps 
-rw-r--r-- 1 hpreston hpreston   992 Jun  4 20:43 01_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  1898 Jun  4 20:43 02_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  2225 Jun  4 20:43 03_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  2487 Jun  4 20:43 03a_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  4128 Jun  4 20:43 04_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  4547 Jun  4 20:43 04a_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  4908 Jun  4 20:43 05_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  5605 Jun  4 20:43 06_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  6040 Jun  7 01:02 06a_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  6843 Jun  7 01:26 07_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  7424 Jun  7 01:05 07a_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  7740 Jun  7 01:06 08_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  8107 Jun  7 01:07 08a_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  8376 Jun  7 01:08 08b_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  9080 Jun  7 01:10 08c_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston  9645 Jun  7 01:12 09_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 10388 Jun  7 01:12 09a_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 11186 Jun  7 01:17 09b1_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 11134 Jun  7 01:17 09b_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 11855 Jun  7 01:18 09c_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 12650 Jun  7 01:21 09d_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 14152 Jun  7 01:22 09e_config_interface_descriptions.py
-rw-r--r-- 1 hpreston hpreston 14690 Jun  7 01:23 10_config_interface_descriptions.py
```

> Note: letters after a number indicate an improvement to the main step number, or a multi-stage development step.