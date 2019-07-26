"""
Author : Yogaraja Gopal
This module contains all the response dumps of Delivery DB API - Used for testing
"""
SYSTEMS = {
    "systems": [
        {
            "creation_date": "Thu, 23 Nov 2017 12:53:12 GMT",
            "system_id": 25,
            "system_name": "Plato7",
            "system_short_name": "p7",
            "system_versions": [
                {
                    "creation_date": "Thu, 23 Nov 2017 12:53:56 GMT",
                    "system_version_components": [
                        {
                            "component_version": {
                                "artefact_store_type": {
                                    "artefact_store_type_desc": "Nexus",
                                    "artefact_store_type_id": 1
                                },
                                "artefact_store_url": "https://buildrepo.uk.specsavers.com/nexus/"
                                                      "service/local/repositories/releases/content/"
                                                      "com/specsavers/datamigration/"
                                                      "plato-data-migration-tc-nz/1.14/"
                                                      "plato-data-migration-tc-nz-1.14.rpm",
                                "component": {
                                    "component_id": 20,
                                    "component_name": "Plato Data Migration",
                                    "component_short_name": "plato-data-mig",
                                    "component_type": {
                                        "component_type_description": "Application",
                                        "component_type_id": 1
                                    },
                                    "creation_date": "Tue, 21 Nov 2017 12:55:25 GMT"
                                },
                                "component_version_id": 10,
                                "component_version_name": "nz-1.14",
                                "creation_date": "Tue, 21 Nov 2017 12:57:30 GMT",
                                "source_code_repository_url": "http://svn.uk.specsavers.com/"
                                                              "oracledelivery/ProductDataHub/"
                                                              "Retail-data-migration/"
                                                              "plato-data-migration-tc-nz/trunk/",
                                "source_tag_reference": "RELEASE-2b-nz-1.14",
                                "stable_flag": 1
                            },
                            "system_component_id": 13
                        }
                    ],
                    "system_version_id": 31,
                    "system_version_name": "p7-pdh-ext-1.14"
                }
            ]
        }
    ]
}
SYSTEM_BY_ID = {
    "systems": [
        {
            "creation_date": "Fri, 01 Dec 2017 16:30:25 GMT",
            "system_id": 1,
            "system_name": "Socrates UK English",
            "system_short_name": "",
            "system_versions": [
                {
                    "creation_date": "Fri, 01 Dec 2017 16:30:25 GMT",
                    "system_version_components": [],
                    "system_version_id": 1,
                    "system_version_name": "D2.4.42"
                },
                {
                    "creation_date": "Fri, 01 Dec 2017 16:30:25 GMT",
                    "system_version_components": [],
                    "system_version_id": 6,
                    "system_version_name": "D2.4.41"
                },
                {
                    "creation_date": "Fri, 01 Dec 2017 16:30:25 GMT",
                    "system_version_components": [],
                    "system_version_id": 11,
                    "system_version_name": "D2.4.40"
                },
                {
                    "creation_date": "Tue, 05 Dec 2017 09:01:52 GMT",
                    "system_version_components": [],
                    "system_version_id": 23,
                    "system_version_name": "tes"
                },
                {
                    "creation_date": "Wed, 13 Dec 2017 00:00:00 GMT",
                    "system_version_components": [],
                    "system_version_id": 24,
                    "system_version_name": "1235"
                },
                {
                    "creation_date": "Wed, 06 Dec 2017 11:56:35 GMT",
                    "system_version_components": [],
                    "system_version_id": 25,
                    "system_version_name": "jhjhj"
                },
                {
                    "creation_date": "Fri, 01 Dec 2017 10:22:28 GMT",
                    "system_version_components": [],
                    "system_version_id": 28,
                    "system_version_name": "ver x.x"
                },
                {
                    "creation_date": "Thu, 14 Dec 2017 14:30:06 GMT",
                    "system_version_components": [],
                    "system_version_id": 29,
                    "system_version_name": "uoi"
                },
                {
                    "creation_date": "Thu, 14 Dec 2017 14:32:26 GMT",
                    "system_version_components": [],
                    "system_version_id": 30,
                    "system_version_name": "test"
                },
                {
                    "creation_date": "Tue, 09 Jan 2018 18:25:51 GMT",
                    "system_version_components": [
                        {
                            "component_version": {
                                "artefact_store_type": {
                                    "artefact_store_type_desc": "Nexus",
                                    "artefact_store_type_id": 1
                                },
                                "artefact_store_url": "Nexus",
                                "component": {
                                    "component_id": 6,
                                    "component_name": "RHEL",
                                    "component_short_name": "RHEL",
                                    "component_type": {
                                        "component_type_description": "Operating System",
                                        "component_type_id": 3
                                    },
                                    "creation_date": "Tue, 21 Nov 2006 16:30:25 GMT"
                                },
                                "component_version_id": 4,
                                "component_version_name": "RHEL 7",
                                "creation_date": "Fri, 01 Dec 2017 16:30:25 GMT",
                                "source_code_repository_url": "GIT",
                                "source_tag_reference": "tag",
                                "stable_flag": 1
                            },
                            "system_component_id": 25
                        }
                    ],
                    "system_version_id": 39,
                    "system_version_name": "1.1"
                }
            ]
        }
    ]
}
COMPONENTS = {
    "components": [
        {
            "component_id": 20,
            "component_name": "Plato Data Migration",
            "component_short_name": "plato-data-mig",
            "component_type": {
                "component_type_description": "Application",
                "component_type_id": 1
            },
            "component_versions": [
                {
                    "artefact_store_type": {
                        "artefact_store_type_desc": "Nexus",
                        "artefact_store_type_id": 1
                    },
                    "artefact_store_url": "https://buildrepo.uk.specsavers.com/nexus/service/"
                                          "local/repositories/releases/content/com/specsavers/"
                                          "datamigration/plato-data-migration-tc-nz/1.14/"
                                          "plato-data-migration-tc-nz-1.14.rpm",
                    "component_version_id": 10,
                    "component_version_name": "nz-1.14",
                    "creation_date": "Tue, 21 Nov 2017 12:57:30 GMT",
                    "source_code_repository_url": "http://svn.uk.specsavers.com/oracledelivery/"
                                                  "ProductDataHub/Retail-data-migration/"
                                                  "plato-data-migration-tc-nz/trunk/",
                    "source_tag_reference": "RELEASE-2b-nz-1.14",
                    "stable_flag": 1
                }
            ],
            "creation_date": "Tue, 21 Nov 2017 12:55:25 GMT"
        }
    ]
}

COMPONENT_TYPE = {
    "component_types": [
        {
            "component_type_description": "Application",
            "component_type_id": 1
        },
        {
            "component_type_description": "Infrastructure",
            "component_type_id": 2
        },
        {
            "component_type_description": "Operating System",
            "component_type_id": 3
        },
        {
            "component_type_description": "External",
            "component_type_id": 4
        },
        {
            "component_type_description": "Database",
            "component_type_id": 5
        }
    ]
}

ARTEFACT_TYPE = {
    "artefact_store_types": [
        {
            "artefact_store_type_desc": "Nexus",
            "artefact_store_type_id": 1
        },
        {
            "artefact_store_type_desc": "Artifactory",
            "artefact_store_type_id": 2
        }
    ]
}
HOST_TYPE = {
    "host_types": [
        {
            "host_name": "RHEV GSY",
            "host_type_id": 1
        },
        {
            "host_name": "VMWARE",
            "host_type_id": 2
        },
        {
            "host_name": "Azure EMEU",
            "host_type_id": 3
        },
        {
            "host_name": "PHYSICAL",
            "host_type_id": 4
        },
        {
            "host_name": "Azure AU",
            "host_type_id": 5
        },
        {
            "host_name": "null",
            "host_type_id": 6
        },
        {
            "host_name": "Azure",
            "host_type_id": 7
        },
        {
            "host_name": "Sunguard",
            "host_type_id": 8
        },
        {
            "host_name": "On-premise",
            "host_type_id": 9
        },
        {
            "host_name": "AWS",
            "host_type_id": 10
        },
        {
            "host_name": "Oracle-Cloud",
            "host_type_id": 11
        }
    ]
}

INSTANCES = {
    "instances": [
        {
            "assigned_ip": "10.80.3.50",
            "creation_date": "Wed, 13 Dec 2017 06:51:52 GMT",
            "host_instance_name": "workstation_nz_p7_1",
            "infrastructure_template": {
                "cpu": 2,
                "host_template_description": "Standard_DSL2_v2",
                "host_type": {
                    "host_name": "Azure",
                    "host_type_id": 7
                },
                "infra_template_id": 2,
                "infra_template_name": "Small",
                "max_no_disk": 8,
                "memory_size": 7.0
            },
            "instance_disks": [
                {
                    "disk_size": 150,
                    "disk_size_type": "gb",
                    "disk_type": {
                        "disk_type_description": "OS disk",
                        "disk_type_id": 1,
                        "host_type_id": 7,
                        "max_size": 150,
                        "min_size": "null"
                    },
                    "instance_disk_id": 1,
                    "instance_id": 1
                },
                {
                    "disk_size": 200,
                    "disk_size_type": "gb",
                    "disk_type": {
                        "disk_type_description": "Standard disk",
                        "disk_type_id": 2,
                        "host_type_id": 7,
                        "max_size": "null",
                        "min_size": "null"
                    },
                    "instance_disk_id": 2,
                    "instance_id": 1
                }
            ],
            "instance_id": 1,
            "instance_name": "Plato7 Server (NZ-SIT)",
            "instance_state": "UP",
            "last_update_date": "Wed, 13 Dec 2017 06:51:52 GMT",
            "remarks": "Instance created for SIT"
        }
    ]
}
INFRA_TEMPLATE = {
    "infrastructure_templates": [
        {
            "cpu": 1,
            "host_template_description": "Standard_DSL1_v2",
            "host_type": {
                "host_name": "Azure",
                "host_type_id": 7
            },
            "infra_template_id": 1,
            "infra_template_name": "XSmall",
            "max_no_disk": 4,
            "memory_size": 3.5
        },
        {
            "cpu": 2,
            "host_template_description": "Standard_DSL2_v2",
            "host_type": {
                "host_name": "Azure",
                "host_type_id": 7
            },
            "infra_template_id": 2,
            "infra_template_name": "Small",
            "max_no_disk": 8,
            "memory_size": 7.0
        }
    ]
}
