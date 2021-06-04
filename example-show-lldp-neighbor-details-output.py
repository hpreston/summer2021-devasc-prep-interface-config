iosxr = {
    "interfaces": {
        "GigabitEthernet0/0/0/1": {
            "port_id": {
                "GigabitEthernet0/2": {
                    "neighbors": {
                        "edge-sw01": {
                            "chassis_id": "5254.001a.7018",
                            "port_description": "Connected to core-rtr01 GigabitEthernet0/0/0/1 - Primary core router",
                            "system_name": "edge-sw01",
                            "neighbor_id": "edge-sw01",
                            "system_description": "Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Version 15.2(CML_NIGHTLY_20190423)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  V152_6_0_81_E\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2019 by Cisc\n",
                            "time_remaining": 101,
                            "hold_time": 120,
                            "capabilities": {
                                "bridge": {"system": True},
                                "router": {"system": True, "enabled": True},
                            },
                            "management_address": "10.10.20.172",
                            "peer_mac": "52:54:00:16:e0:b6",
                        }
                    }
                }
            }
        },
        "GigabitEthernet0/0/0/2": {
            "port_id": {
                "GigabitEthernet2": {
                    "neighbors": {
                        "dist-rtr01.virl.info": {
                            "chassis_id": "001e.14b8.b300",
                            "port_description": "Connected to core-rtr01 GigabitEthernet0/0/0/2 - Path to core",
                            "system_name": "dist-rtr01.virl.info",
                            "neighbor_id": "dist-rtr01.virl.info",
                            "system_description": "Cisco IOS Software [Gibraltar], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.11.1b, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2019 by Cisco Systems, Inc.\nCompiled Tue 28-May-19 12:45",
                            "time_remaining": 101,
                            "hold_time": 120,
                            "capabilities": {
                                "bridge": {"system": True},
                                "router": {"system": True, "enabled": True},
                            },
                            "management_address": "172.16.252.21",
                            "peer_mac": "52:54:00:11:00:01",
                        }
                    }
                }
            }
        },
    },
    "total_entries": 2,
}

iosxe = {
    "interfaces": {
        "GigabitEthernet2": {
            "if_name": "GigabitEthernet2",
            "port_id": {
                "GigabitEthernet0/0/0/2": {
                    "neighbors": {
                        "core-rtr01.virl.info": {
                            "neighbor_id": "core-rtr01.virl.info",
                            "chassis_id": "0264.7269.a406",
                            "port_id": "GigabitEthernet0/0/0/2",
                            "port_description": "Connected to dist-rtr01 GigabitEthernet2 - Path to inside distribution",
                            "system_name": "core-rtr01.virl.info",
                            "system_description": "Copyright (c) 2017 by Cisco Systems, Inc., IOS XRv Series\n",
                            "time_remaining": 113,
                            "capabilities": {
                                "router": {
                                    "name": "router",
                                    "system": True,
                                    "enabled": True,
                                }
                            },
                            "management_address": "172.16.252.22",
                            "auto_negotiation": "not supported",
                        }
                    }
                }
            },
        },
        "GigabitEthernet4": {
            "if_name": "GigabitEthernet4",
            "port_id": {
                "Ethernet1/3": {
                    "neighbors": {
                        "dist-sw01": {
                            "neighbor_id": "dist-sw01",
                            "chassis_id": "5254.0019.6cf3",
                            "port_id": "Ethernet1/3",
                            "port_description": "Connected to dist-rtr01 GigabitEthernet4 - Path to distribution router",
                            "system_name": "dist-sw01",
                            "system_description": "Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved.\n",
                            "time_remaining": 119,
                            "capabilities": {
                                "mac_bridge": {
                                    "name": "mac_bridge",
                                    "system": True,
                                    "enabled": True,
                                },
                                "router": {
                                    "name": "router",
                                    "system": True,
                                    "enabled": True,
                                },
                            },
                            "management_address": "10.10.20.177",
                            "auto_negotiation": "not supported",
                        }
                    }
                }
            },
        },
    },
    "total_entries": 2,
}

nxos = {
    "interfaces": {
        "Ethernet1/3": {
            "port_id": {
                "GigabitEthernet4": {
                    "neighbors": {
                        "dist-rtr01.virl.info": {
                            "chassis_id": "001e.14b8.b300",
                            "port_description": "Connected to dist-sw01 Ethernet1/3 - Path to distribution switch 01",
                            "system_name": "dist-rtr01.virl.info",
                            "system_description": "Cisco IOS Software [Gibraltar], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.11.1b, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2019 by Cisco Systems, Inc.\nCompiled Tue 28-May-19 12:45",
                            "time_remaining": 102,
                            "capabilities": {
                                "bridge": {"name": "bridge", "system": True},
                                "router": {
                                    "name": "router",
                                    "system": True,
                                    "enabled": True,
                                },
                            },
                            "management_address_v4": "172.16.252.2",
                            "management_address_v6": "not advertised",
                            "vlan_id": "not advertised",
                        }
                    }
                }
            }
        }
    },
    "total_entries": 1,
}


# Example enabling and using LLDP info
for device in testbed.devices:
    # Enable LLDP
    testbed.devices[device].api.configure_lldp()

    # Parse LLDP Neighbor Details
    lldp_info = testbed.devices[device].parse("show lldp neighbors detail")

    # Print neighbors
    for interface, details in lldp_info["interfaces"].items():
        local_interface = interface
        for neighbor_interface, neighbors in details["port_id"].items():
            for neighbor, neighbor_details in neighbors["neighbors"].items():
                print(
                    f"Local Interface {local_interface} is connected to Neighbor {neighbor} Interface {neighbor_interface}"
                )
