/* Diresctive to add dynamic model with check of ng-comp-name attribute */
   myApp.directive('ngCompName', ['$compile', '$parse', function ($compile, $parse ) {
    return {
        restrict: 'A',
        terminal: true,
        priority: 100000,
        link: function (scope, elem) {
            var model_value =  $parse(elem.attr('value'))(scope);
            //var name = $parse(elem.attr('ng-model-name'))(scope);   
            var name = elem.attr('ng-comp-name');
             elem.removeAttr('ng-comp-name');
            var model_name = name.toString() + model_value.toString();
            elem.attr('ng-model', model_name);
            $compile(elem)(scope);
        }
    };
}]) 
    myApp.controller("releaseCtrl", function ($scope, $http, $timeout, $filter, myService , AuthenticationService) {
        /*$(document).ready(function () {
            $('.rel-sel').select2();
        });*/

        $scope.infraValue = function () {
            $scope.instance = undefined;
            $scope.infraID = undefined;
        };
        $('.multiselect-hidden').removeAttr('style');
        var fixHelperModified = function (e, tr) {
                var $originals = tr.children();
                var $helper = tr.clone();
                $helper.children().each(function (index) {
                    $(this).width($originals.eq(index).width())
                });
                return $helper;
            },
            updateIndex = function (e, ui) {
                $('td.index span.step', ui.item.parent()).each(function (i) {
                    $(this).html(i + 1);
                });
                $scope.$apply(function () {
                    $scope.deployment_step = ui.item.parent().find('.selected').children().find('.step').text();
                });
            };

        $("#release-item tbody").sortable({
            helper: fixHelperModified,
            stop: updateIndex
        }).disableSelection();

        $scope.filterVersion = function (comp_name) {
            return function (components) {
                angular.forEach(components, function (comp) {
                    if (comp.component_name == comp_name) {
                        return comp.components_versions;
                    };
                });
            }
        };
        $scope.filterByDate = function (elm) {
            var date = new Date(elm.creation_date)
            elm.creation_date = date.getTime();
            return elm;
        };
        // Perform Scope Apply to show the changes
        var applyScope = function () {
            $scope.$apply(function () {
                $scope.show = true;
                $scope.loading = false;
                $scope.initLoading = false;
            });
            //        angular.element(document).ready(function () { $('select').selectpicker("destroy");
            //        $('select').selectpicker("render"); 
            //        $('select').selectpicker("refresh");});

        }

        // Show loading
        $scope.onLoading = function () {
            $scope.initLoading = true;
            $scope.show = false;
        }
        // Handle Success response
        var handleSuccessResponse = function (resp) {
            $scope.$apply(function () {
                $scope.loading = false;
                $scope.initLoading = false;
                $scope.reqFailed = false;
                $scope.reqSuccess = true;
                $scope.successMsg = resp["resp"];
            });
        };

        // Handle Failure response
        var handleFailureResponseJson = function (resp) {
           
                $scope.$apply(function () {
                    $scope.loading = false;
                    $scope.initLoading = false;
                    $scope.reqSuccess = false;
                    $scope.reqFailed = true;
                    $scope.errMsg = resp["resp"];
                });
                
        };



        // Handle Failure response
        var handleFailureResponse = function (resp) {
            resp.fail(function (req, status, err) {
                $scope.$apply(function () {
                    $scope.loading = false;
                    $scope.initLoading = false;
                    $scope.reqSuccess = false;
                });
                if (status == "timeout") {
                    $scope.$apply(function () {
                        $scope.reqFailed = true;
                        $scope.reqSuccess = false;
                        $scope.errMsg = "Time out Error"
                    });
                } else if (status == "error") {
                    $scope.$apply(function () {
                        $scope.reqFailed = true;
                        $scope.reqSuccess = false;
                        $scope.errMsg = err;
                    });
                }
            });
        };
        // Initialize values
        var initializeApiCall = function (initialSortType, sortReverse = false) {
            $scope.sortType = initialSortType;
            $scope.sortReverse = sortReverse;
            $scope.search = '';
            $scope.loading = true;
            $scope.reqFailed = false;
            $scope.showRepStatus = false;
        };

        var uniqueArrayByKey = function (collection, keyname) {
            var output = [],
                keys = [];
            angular.forEach(collection, function (item) {
                var key = item[keyname];
                if (keys.indexOf(key) === -1) {
                    keys.push(key);
                    output.push(item);
                }
            });
            return output;
        };
        // Handle Get Systems Api Call
        $scope.getSystems = function () {
            $scope.sortType1 = "creation_date";
            $scope.sortReverse1 = false;
            initializeApiCall("system_name");
            var url_val = '/api/get/system';
            var getSystemsResponse = myService.getAJAXObject(url_val);
            getSystemsResponse.done(function (status) {
                var syslist = $.parseJSON(status);
                $scope.systems = syslist["systems"];
                applyScope();
            });
            handleFailureResponse(getSystemsResponse);
        };
        // Handle Get Environment Api Call
        $scope.getEnv = function () {
            initializeApiCall("environment_name");
            var url_val = '/api/get/environment';
            var getEnvResponse = myService.getAJAXObject(url_val);
            getEnvResponse.done(function (status) {
                var envlist = $.parseJSON(status);
                $scope.environments = envlist["environments"];
                applyScope();
            });
            handleFailureResponse(getEnvResponse);
        };

        // Handle Get Component Api Call
        $scope.getComponents = function () {
            initializeApiCall("component_name");
            var url_val = '/api/get/component';
            var getComponentsResponse = myService.getAJAXObject(url_val);
            getComponentsResponse.done(function (status) {
                var complist = $.parseJSON(status);
                $scope.components = complist["components"];
                applyScope();
            });
            handleFailureResponse(getComponentsResponse);
        };

        // Handle Get Instance Api Call
        $scope.getInstances = function () {
            initializeApiCall("instance_name");
            var url_val = '/api/get/instance';
            var getInstancesResponse = myService.getAJAXObject(url_val);
            getInstancesResponse.done(function (status) {
                var instList = $.parseJSON(status);
                $scope.instances = instList["instances"];
                applyScope();
            });
            handleFailureResponse(getInstancesResponse);
        };

        // Handle Get Release Api Call
        $scope.get_release = function () {
            //if (rel_id)
            initializeApiCall("release_name");
            var url_val = '/api/get/release';
            var getReleaseResponse = myService.getAJAXObject(url_val);
            getReleaseResponse.done(function (status) {
                var releaseList = $.parseJSON(status);
                $scope.releases = releaseList["releases"];
                applyScope();
            });
            handleFailureResponse(getReleaseResponse);
        };
        // Get the list of unique systems related to the release
        $scope.getSystemFromRelease = function () {
            $scope.releaseSystems = []
            if ($scope.release != undefined) {
                release_version = $scope.release.release_versions;
                angular.forEach(release_version, function (rel_ver) {
                    relItems = rel_ver.release_items;
                    angular.forEach(relItems, function (relItem) {
                        relSystem = {
                            "system_id": relItem.system_version.system_id,
                            "system_name": relItem.system_version.system_name
                        };
                        $scope.releaseSystems.push(relSystem);
                    });
                });
                $scope.releaseSystems = uniqueArrayByKey($scope.releaseSystems, "system_id");
                //        angular.element(document).ready(function () {$('select').selectpicker("destroy");
                //        $('select').selectpicker("render");
                //       $('select').selectpicker("refresh");});
            };
        };
        // Handle Get Release By ID Api Call
        $scope.get_release_by_id = function (rel_id) {
            if (rel_id != '' && rel_id != undefined) {
                initializeApiCall("release_name");
                var url_val = '/api/get_release_by_id/' + rel_id;
                var getReleaseByIdResponse = myService.getAJAXObject(url_val);
                getReleaseByIdResponse.done(function (status) {
                    var releaseList = $.parseJSON(status);
                    $scope.releaseById = releaseList["releases"][0];
                    applyScope();
                });
                handleFailureResponse(getReleaseByIdResponse);
            } else {
                $scope.releaseById = undefined;
            };
        };


         function inArrayCheck(myArray,myValue){
            var inArray = false;
            myArray.map(function(key){
                if (key === myValue){
                    inArray=true;
                }
                else if(key.key === myValue.key)
                {
                    inArray = true;
                }
            });
            return inArray;
        };
        $scope.getInstanceAllocation = function (env) {
            
            var sys_id = document.getElementById("checkId").getAttribute("sys_id");
            //var sys_version_id = document.getElementById("checkId").getAttribute("sys_version_id");
            var sys_elem_id = document.getElementById("checkId").getAttribute("sys_ele");
            var url_val = '/api/get_instance_allocation/' + env + '/' + sys_id + '/' + sys_elem_id;
            var getInstanceFromEnvResponse = myService.getAJAXObject(url_val);
            getInstanceFromEnvResponse.done(function (status) {
                DataList = $.parseJSON(status);
                angular.forEach(DataList, function (instance) {
                    if (instance != "No InstanceAllocation found."){

                        let  instanceList1 = $scope.instanceList;

                        let newObjInstance = instanceList1.map(obj => ({ 
                            key: obj.key,
                            value: obj.value
                        }));

                         var check = inArrayCheck(newObjInstance,instance);
                         if(!check){
                             $scope.instanceList.push(instance);
                         }

                       
                    }
                });

                   
                if ($scope.instanceList.length == 0) {
                    $(".instance-default").text("No Instances associated to the Selected Environment");
                }
                applyScope();
            });
        };
        $scope.getInstanceFromEnv = function (env_id) {
            //alert("hello");
            if (env_id != '' && env_id != '-1' && env_id != undefined) {
                initializeApiCall("release_name");
                var url_val = '/api/get_instance_from_env/' + env_id;
                var getInstanceFromEnvResponse = myService.getAJAXObject(url_val);
                getInstanceFromEnvResponse.done(function (status) {
                    $scope.instanceList = $.parseJSON(status);
                    //if ($scope.instanceList.length == 0) {
                    //    $(".instance-default").text("No Instances associated to the Selected Environment");
                   // } else {
                        $(".instance-default").text("--Select--");
                    //};
                    applyScope();
                });
                handleFailureResponse(getInstanceFromEnvResponse);
            } else {
                $scope.instanceList = [];
                $(".instance-default").text("No Instances associated to the Selected Environment");
            };
        };

        // Handle Get Infrastructure Template Api Call
        $scope.getInfra = function () {
            initializeApiCall("infra_template_name");
            var url_val = '/api/get/infrastructure_template';
            var getInfraResponse = myService.getAJAXObject(url_val);
            getInfraResponse.done(function (status) {
                var infraList = $.parseJSON(status);
                $scope.infraTemplates = infraList["infrastructure_templates"];
                applyScope();
            });
            handleFailureResponse(getInfraResponse);
        };

        $scope.getInfraTemplateFromInstance = function (inst) {
            inst_id = inst["key"];
            if (inst_id != '' && inst_id != '-1' && inst_id != undefined) {
                var url_val = '/api/get_infra_template_from_inst/' + inst_id;
                var getInfraTemplateFromInstanceResponse = myService.getAJAXObject(url_val);
                getInfraTemplateFromInstanceResponse.done(function (status) {
                    infraList = $.parseJSON(status);
                    $scope.host = infraList[0]["host"].toString()
                    $scope.infraID = {
                        "infra_template_id": infraList[0]["key"].toString()
                    };
                    applyScope();
                });
                handleFailureResponse(getInfraTemplateFromInstanceResponse);
            } else {
                $scope.infraID = undefined;
            };
        };

        $scope.checkDeployementUserPermissions = function(){
         
            var message = 'Permission denied to access page';
            var permssionsArray  = AuthenticationService.checkPermissions('Deployments');
            if(permssionsArray.length<1){
                $(location).attr('href','/?message='+message);
            }else{
               
                var permission = permssionsArray.map(perObj =>{ 
                    var rObj = perObj.buisnessProcessPermission;
                    return rObj;
                 });

                 if(permission.includes("View")){
                    if(permission.includes("Deploy Development")){
                        $scope.developmentView = true;
                    }
                    if(permission.includes("Deploy Acceptance")){
                        $scope.acceptanceView = true;
                    }
                    if(permission.includes("Deploy Production")){
                        $scope.productionView = true;
                    }
                 }
                 else{
                   
                    $(location).attr('href','/?message='+message);
                 }
            }
           
        }

        // Handle Get deployments Api Call
        $scope.get_deployments = function () {
            $scope.checkDeployementUserPermissions();
            initializeApiCall("deployment_id", true);
            var url_val = '/api/get/deployment';
            var getDeployResponse = myService.getAJAXObject(url_val);
            getDeployResponse.done(function (status) {
                var infraList = $.parseJSON(status);
                $scope.deployments = infraList["deployments"];
                applyScope();
            });
            handleFailureResponse(getDeployResponse);
        };

        var getNetworkSet = function (envType) {

            initializeApiCall("network_set_name");
            var url_val = '/api/get/network_set';
            var getReleaseResponse = myService.getAJAXObject(url_val);
            getReleaseResponse.done(function (status) {
                var networkSetList = $.parseJSON(status);
                network_sets = networkSetList["network_sets"];
                angular.forEach(network_sets, function (network_set) {
                    if (envType == network_set.environment_type.environment_type_id) {
                        $scope.$apply(function () {
                            $scope.network_set_name = network_set.network_set_name;
                        });
                    }
                });
                applyScope();
            });
            handleFailureResponse(getReleaseResponse);
        };

        $scope.getNetworkSetName = function (env) {
            $scope.network_set_name = undefined;
            var url_val = '/api/get/environment';
            var getEnvResponse = myService.getAJAXObject(url_val);
            getEnvResponse.done(function (status) {
                var envList = $.parseJSON(status);
                $scope.environments = envList["environments"];
                applyScope();
                angular.forEach($scope.environments, function (environment) {
                    if (env == environment.environment_id) {
                        $scope.envType = environment.environment_type.environment_type_id;
                        $scope.$apply(function () {
                            $scope.env_type_name = environment.environment_type.environment_type_name;
                            manipulateInstanceName();
                        });
                        getNetworkSet($scope.envType);
                    }
                })
            });
            handleFailureResponse(getEnvResponse);
        };

        $scope.getHostSite = function (host) {
            $scope.host_site_name = undefined;
            var url_val = '/api/get/host_region';
            var getReleaseResponse = myService.getAJAXObject(url_val);
            getReleaseResponse.done(function (status) {
                var hostRegionList = $.parseJSON(status);
                host_regions = hostRegionList["host_regions"];
                angular.forEach(host_regions, function (host_region) {
                    if (host == host_region.host_type.host_type_id) {
                        $scope.$apply(function () {
                            $scope.host_site_name = host_region.host_region_name;
                            manipulateInstanceName();
                        });
                    };
                });
            });
            handleFailureResponse(getReleaseResponse);
        };

        $scope.setShortName = function (sys_short_name) {
            $scope.system_element_short_name = sys_short_name;
        }

        var manipulateInstanceName = function () {
            //(~env_type_name | limitTo:1 | lowercase ~)(~host_site_name | limitTo:4 | lowercase ~)(~"f"~)
            if ($scope.env_type_name != '' && $scope.env_type_name != undefined && $scope.host_site_name != '' && $scope.host_site_name != undefined) {
                instanceNameFirtPart = $scope.env_type_name.charAt(0).toLowerCase();
                instanceNameFirtPart += $scope.host_site_name.substring(0, 4).toLowerCase();
                if($scope.system_element_short_name!= undefined){
                    instanceNameFirtPart += "f" + $scope.system_element_short_name.toLowerCase();
                }
               
                var count = 1;
                calcInstanceName = instanceNameFirtPart + "00" + count;
                var url_val = '/api/get_instance_names';
                var getReleaseResponse = myService.getAJAXObject(url_val);
                getReleaseResponse.done(function (status) {
                    var instanceNameList = $.parseJSON(status);
                    var instanceNames = instanceNameList["instance_names"];
                    instanceNames.forEach(function (instance) {
                        if (calcInstanceName == instance) {
                            count += 1;
                            incVal = "00" + count;
                            incVal.substr(incVal.length - 3);
                            calcInstanceName = instanceNameFirtPart + incVal;
                        }
                    });
                    $scope.$apply(function () {
                        $scope.calc_instance_name = calcInstanceName;
                    });
                });
                handleFailureResponse(getReleaseResponse);
            };
        };


        $scope.checkDeployStatus = function (deploy) {
            deploy_comp = deploy["deployment_components"];
            no_comp = deploy_comp.length;
            deploy_status_cnt = 0;
            deploy_status = ''
            angular.forEach(deploy_comp, function (value) {
                if (deploy_status_cnt == 0) {
                    deploy_status = value["deployment_component_status"]["status_description"];
                    deploy_status_cnt = deploy_status_cnt += 1;
                } else {
                    if (deploy_status == value["deployment_component_status"]["status_description"]) {
                        deploy_status_cnt += 1;
                    };
                };
            });
            if (no_comp === deploy_status_cnt) {
                deploy["deployStatus"] = deploy_status;
            } else {
                deploy["deployStatus"] = "Mixed";
            };
        };

        $scope.checkDeploymentType = function (deploy) {
            deploy_comp = deploy["deployment_components"];
            no_comp = deploy_comp.length;
            auto_deploy_cnt = 0;
            manual_deploy_cnt = 0;
            angular.forEach(deploy_comp, function (value) {
                deployment_type = value["system_element_component"]["component_version"]["component"]["deployment_type"]["deployment_type_description"].toUpperCase()
                if (deployment_type == "FULLY AUTOMATED") {
                    auto_deploy_cnt += 1;
                } else {
                    manual_deploy_cnt += 1;
                };
            });
            if (no_comp === auto_deploy_cnt) {
                deploy["autoDeploy"] = true;
                deploy["manualDeploy"] = false;
            } else if (no_comp == manual_deploy_cnt) {
                deploy["autoDeploy"] = false;
                deploy["manualDeploy"] = true;
            } else {
                deploy["autoDeploy"] = false;
                deploy["manulaDeploy"] = false;
            };
        };

        // Call the jenkins job
        $scope.callJenkinsJob = function (mode, deploy, comp_id) {
            var url_val = '/api/call_jenkins_job/' + mode + "/" + deploy + "/" + comp_id;
            var getJenkinsJobResponse = myService.getAJAXObject(url_val);
            getJenkinsJobResponse.done(function (status) {
                var jenkinsResponse = $.parseJSON(status);
                if(jenkinsResponse.status == 'success'){
                    handleSuccessResponse(jenkinsResponse);    
                }
                else
                {
                   handleFailureResponseJson(jenkinsResponse);  
                }
            });
            handleFailureResponse(getJenkinsJobResponse);
        }

        // Update deployment component status
        $scope.updateDeployCompSts = function (mode, deploy_id, comp_id) {
            var url_val = '/api/update_deploy_comp_sts/' + mode + "/" + deploy_id + "/" + comp_id;
            var getDeployCompStsResponse = myService.getAJAXObject(url_val);
            getDeployCompStsResponse.done(function (status) {
                var deployStatusResp = $.parseJSON(status);
                handleSuccessResponse(deployStatusResp);
            });
            handleFailureResponse(getDeployCompStsResponse);
        }

        // Handle generic Api get details
        $scope.getApiDetails = function (model) {
            initializeApiCall(model + "_name")
            var url_val = '/api/get/' + model;
            var getApiDetailsResponse = myService.getAJAXObject(url_val);
            getApiDetailsResponse.done(function (status) {
                $scope.apiResponse = $.parseJSON(status);
                applyScope();
            });
            handleFailureResponse(getApiDetailsResponse);
        };
        var traverseComponent = function (comp_id) {
            var comp_obj = []
            angular.forEach($scope.components, function (comp) {
                if (comp.component_id == comp_id) {
                    comp_obj.push(comp);
                }
            });
            return comp_obj;
        };

        // Code related to Add Release Version
        var traverseSystem = function (sys_id) {
            var sys_obj = []
            angular.forEach($scope.systems, function (sys) {
                if (sys.system_id == sys_id) {
                    sys_obj.push(sys);
                }
            });
            return sys_obj;
        };
        $scope.addReleaseItem = function (obj) {
            $scope.releaseItems = []
            var relItemCnt = 0;
            if (obj) {
                if (obj.release_items.length > 0) {
                    angular.forEach(obj.release_items, function (rel_item) {
                        var system_obj = traverseSystem(rel_item.system_version.system.system_id)
                        $scope.releaseItems.push({
                            'sysCount': 'relItem' + relItemCnt,
                            'system': system_obj[0],
                            'system_version': rel_item.system_version,
                            'rel_note_url': rel_item.release_note_url
                        });
                        relItemCnt = relItemCnt + 1;
                    });
                } else {
                    $scope.releaseItems.push({
                        'sysCount': 'relItem' + relItemCnt
                    });
                }
            } else {
                $scope.releaseItems.push({
                    'sysCount': 'relItem' + relItemCnt
                });
            };
        }
        $scope.addNewReleaseItem = function () {
            var newItemCount = $scope.releaseItems.length + 1;
            $scope.releaseItems.push({
                'sysCount': newItemCount
            });
        };
        $scope.removeReleaseItem = function (index) {
            if (index === -1) {
                $scope.releaseItems = [];
            } else {
                $scope.releaseItems.splice(index, 1);
            }
        };

        $scope.addRTL = function () {
            $scope.rtls = [{
                'rtl_id': 1
            }];
        }
        $scope.addNewRTL = function () {
            var newRTLCount = $scope.rtls.length + 1;
            $scope.rtls.push({
                'rtl_id': newRTLCount
            });
        };
        $scope.removeRTL = function (index) {
            if (index === -1) {
                $scope.rtls = [];
            } else {
                $scope.rtls.splice(index, 1);
            }
        };
        $scope.checkCritical = function (index) {
            if (index != undefined) {
                curRTL = $scope.rtls[index]
                angular.forEach($scope.rtls, function (itm) {
                    if (itm.order == curRTL.order && itm.critical && itm.rtl_id != curRTL.rtl_id) {
                        curRTL.critical = false;
                    };
                });
            };
        }
        $scope.groupRTL = function (release) {
            $scope.grpRtl = [];
            listenv_use = [];
            angular.forEach(release.route_to_live, function (itm) {
                if (listenv_use.indexOf(itm.environment_use.environment_use_name) == -1) {
                    listenv_use.push(itm.environment_use.environment_use_name);
                };
            });
            angular.forEach(listenv_use, function (env) {
                rtl_data = {};
                rtl_data["name"] = env;
                env_list = [];
                angular.forEach(release.route_to_live, function (itm) {
                    env_data = {};
                    if (itm.environment_use.environment_use_name == env) {
                        env_data["system_name"] = itm.environment.system.system_name;
                        env_data["env_name"] = itm.environment.environment_name;
                        env_list.push(env_data);
                    };
                });
                rtl_data["env"] = env_list;
                $scope.grpRtl.push(rtl_data);
            });
        };
        /*
            $scope.copySysComp = function(index) {
                var newItemNo = $scope.system_comps.length+1;
                var copiedSysComp = $scope.system_comps[index];
                $scope.system_comps.push({'sys_comp_name': 'compVer' + newItemNo,
                            'sys_comp_id': copiedSysComp['sys_comp_id'],
                            'comp_name': copiedSysComp['comp_name'],
                            'comp_ver': copiedSysComp['comp_ver'],
                            'comp_type': copiedSysComp['comp_type'],
                            'logical_name': 'logicalName' + newItemNo});
            };
        */
        $(".remove, .addComp").click(function (e) {
            e.preventDefault();
        });

        $('#id_creation_date_1').attr('placeholder', 'Creation Time');
        var links = $('a[role="button"]');
        links.on('show.bs.tab', function (e) {
            $('a[aria-expanded="true"]').addClass("active");
            $('a[aria-expanded="false"]').removeClass("active");
        })
        var $myForm = $('.my-form')
        $myForm.click(function (event) {
            $(".alert").removeClass("alert-success alert-danger show in");
        })
        $myForm.submit(function (event) {
            $(".alert").removeClass("alert-success alert-danger show in");
            event.preventDefault()
            var $formData = $(this).serialize()
            var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
            $.ajax({
                method: "POST",
                url: $thisURL,
                data: $formData,
                success: handleFormSuccess,
                error: handleFormError,
            })
        })


    

        function handleFormSuccess(data, textStatus, jqXHR) {
            if (data.url) {
                $(location).attr('href', data.url)
            }
            var obj = jqXHR.responseJSON;
            if (typeof obj != 'object') {
                var obj = jQuery.parseJSON(jqXHR.responseJSON);
            };
            $(".a-text").remove();
            $.each(obj, function (key, value) {
                $("#alert").removeClass("alert-danger").addClass("alert-success show in");
                $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + ' ' + '</span>');
            });
            $myForm[0].reset(); // reset form data
            $('.filter-option').html('--Select--');
            $timeout(function () {
                angular.element('#rm-cmp').triggerHandler('click');
            }, 0);
        }

        function handleFormError(jqXHR, textStatus, errorThrown) {
            //var obj = jQuery.parseJSON(jqXHR.responseJSON);
            var obj = jqXHR.responseJSON;
            if (typeof obj != 'object') {
                var obj = jQuery.parseJSON(jqXHR.responseJSON);
            };
            $(".a-text").remove();
            $.each(obj, function (key, value) {
                $("#alert").removeClass("alert-success").addClass("alert-danger show in");
                $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + '</span>');
            });
        };
        $scope.clearSelectedRelItem = function () {
            $scope.selectedRelItem = {};
            $scope.planned_deployment_date = '';
            $scope.planned_deployment_time = '';
            $scope.deploy_audit = {};
            $scope.instance_detail = undefined;
            $scope.deployment_step = undefined;
        };
        $scope.relItemHead = ['system_component.component.component_name', 'system_component.component_version.component_version_name',
            'system_component.component_version.component.component_type.component_type_description', 'logical_instance_name'
        ];
        $scope.selItem = function ($event, rel) {
            var elm = $event.currentTarget;
            var step = angular.element(elm).children().children().children().text();
            $scope.selectedRelItem = rel;

            if ($scope.selectedRelItem) {
                var deployment_state = $scope.selectedRelItem.deployment_state;
                if (deployment_state.length > 0) {
                    $scope.instance_detail = $scope.selectedRelItem.deployment_state[0].instance;
                    var date = new Date($scope.selectedRelItem.deployment_state[0].planned_deployment_date)
                    var date_time = date.getTime();
                    $scope.planned_deployment_date = $filter('date')(date_time, 'yyyy-dd-MM');
                    $scope.planned_deployment_time = $filter('date')(date_time, 'HH:mm:ss');
                    var deploy_audit_history = $scope.selectedRelItem.deployment_state[0].deployment_audit_history;
                    if (deploy_audit_history.length > 0) {
                        var res = Math.max.apply(Math, deploy_audit_history.map(function (o) {
                            return o.deployment_audit_id;
                        }))
                        $scope.deploy_audit = deploy_audit_history.find(function (o) {
                            return o.deployment_audit_id == res;
                        })
                    }
                } else {
                    $scope.instance_detail = undefined;
                    $scope.deploy_audit = {};
                    $scope.planned_deployment_date = '';
                    $scope.planned_deployment_time = '';
                }
                $scope.deployment_step = step;
            }
        };
        $scope.isSelected = function (relItem, step) {
            return $scope.selectedRelItem === relItem;
        };
        

        
/*function to generate YAML which include user defined param 
screen input params and multi param */
    $scope.generateYaml = function($event){
        $event.preventDefault();        
        var output_obj = {};
        output_obj['infra'] = {};
        output_obj['infraConf'] = {};
        output_obj['app'] = {};
        var api_data_param = {}; 
        var yaml_error = [];
        $('#deploy-form input, #deploy-form select').each(
        function(index){  
            var input = $(this);
            var input_id = input.attr('id');
            var input_name = input.attr('name');
            var input_label = input.attr('labelerror');
            var val_inp = document.getElementById(input_id);       
            if(val_inp != null){          
                if(val_inp.validity != undefined){ 
                    if(val_inp.validity.valid == false && val_inp.validity.valueMissing){
                        if(input_label != undefined){
                            if(input_label != ''){
                               var errorMsg = input_label ;
                            }
                        }
                        else{
                           var errorMsg = input_name + ' is required.';   
                        }
                    }
                    if(val_inp.validity.valid == false && (val_inp.validity.rangeOverflow|| val_inp.validity.rangeUnderflow)){
                        if(input_label != undefined){
                            if(input_label != ''){
                                var errorMsg = input_label ;
                            }
                        }   
                    }

                    if(errorMsg != undefined)
                    {
                        yaml_error.push(errorMsg);
                    }
                    
                }
            }

            var input_name = input.attr('name');
            var input_data_param = input.attr('data-internal-name');
            var input_multiple = input.attr('multiple');
            var multi_param = [];
            var multi_param_string = "";
            var known_data_param = ['environment_id','sys_elem_id','instance_id','system_version_id'];
            var input_comp_type = input.attr('data-comp-type');
            var input_comp_id = input.attr('data-comp-id');
            var component_info = angular.element($('#component_info')).val();
            component_info = JSON.parse(component_info);
           
            
            if(typeof input_data_param !== "undefined")
            {   
                if(typeof input_multiple !== "undefined")
                {
                    $('.list-multiple').each( function(index){ 
                        var input_multi = $(this);
                        var inputmulti_data_param = input_multi.attr('data-internal-name');
                        
                            if(input_data_param == inputmulti_data_param)
                            {
                                multi_param = input_multi.val();
                                var input_multi_string = "";
                                if(input_multi.val() !== null){
                                    input_multi_string =input_multi.val().toString();
                                }
                                if(multi_param_string == ""){
                                    multi_param_string = input_multi_string + ",";
                                }
                                else{
                                    multi_param_string = multi_param_string + input_multi_string;
                                }
                            }  
                    });
                    if(multi_param != null){
                        if(input_comp_type !=null){
                            if(input_comp_id!=null && input_comp_id != 0)
                            {   
                                var input_multi = $(this);
                                input_multi_string =input_multi.val().toString();
                                multi_param_string = "";
                                if(multi_param_string == ""){
                                    multi_param_string = input_multi_string + ",";
                                }
                                else{
                                    multi_param_string = multi_param_string + input_multi_string;
                                }
                                comp_id = component_info[input_comp_id]['comp_id'];
                                if(output_obj[input_comp_type][comp_id] == undefined){
                                    output_obj[input_comp_type][comp_id] = {};
                                }
                                output_obj[input_comp_type][comp_id][input_data_param] = multi_param_string;
                            }
                            else{
                                output_obj[input_comp_type][input_data_param] = multi_param_string;
                            }
                        }else{
                            output_obj[input_data_param]  =  multi_param_string;
                        }
                    }                                 
                }
                else
                {
                    var input_value = input.val();
                    if (input_value == "True" || input_value == "False"){
                        input_value = (input_value == 'True');
                    }
                    if(input_value !== ''){
                        if(known_data_param.indexOf(input_data_param) === -1)
                        {
                            if(input_comp_type !=null){
                                if(input_comp_id!=null && input_comp_id != 0)
                                {
                                    comp_id = component_info[input_comp_id]['comp_id'];
                                    if(output_obj[input_comp_type][comp_id] == undefined){
                                        output_obj[input_comp_type][comp_id] = {};
                                    }
                                    output_obj[input_comp_type][comp_id][input_data_param] = input_value;
                                }
                                else{
                                    output_obj[input_comp_type][input_data_param] = input_value ;
                                }
                                
                            }
                            else{
                                output_obj[input_data_param] = input_value ;
                            } 
                        }   
                    }
                    
                    if(known_data_param.indexOf(input_data_param) !== -1)
                    {
                        api_data_param[input_data_param] = input_value;
                    } 
                }    
            }                   
        });

        if($scope.infra){
            if(output_obj["'environmentAppParams'.'instance_user'"])
            {
                output_obj["'environmentAppParams'.'instance_user'"] = '';
            } 
            if(output_obj["'environmentAppParams'.'instance_password'"])
            {
                output_obj["'environmentAppParams'.'instance_password'"] = '';
            } 
            if(!$scope.infraConf && !$scope.app){
                if(output_obj['infra']["'commonParams'.'specs_ansible_version'"])
                {
                    output_obj['infra']["'commonParams'.'specs_ansible_version'"] = '';
                } 
            }  
        }
        
        if(yaml_error.length>0)
        {
            str = '';
            var errorNames = [];
            angular.forEach(yaml_error, function(text, key){
                if(errorNames.indexOf(text) === -1)
                {
                    errorNames.push(text);
                }

            });

            errorNames.forEach(function(item){ 
                str =  str+'<li style="color:red"><b>'+ item +'</b></li>';
            });
            
            YamlFormSuccess(str);
        }
        else{
            if($scope.infra){
                output_obj['infra']["'infrastructureEnvironmentParams'.'instance_type'"] = $('#infra_template option:selected').text();
            }
           
            var component_info = angular.element($('#component_info')).val();
            component_info = JSON.parse(component_info);

            var available_infra_config = [];
            angular.forEach(angular.element($("input[name='available_infra_config']:checked")), function (input_component){
                var infra_conf_comp_id = angular.element(input_component).val();
                available_infra_config.push(component_info[infra_conf_comp_id]);
            });
            api_data_param['available_infra_config'] = available_infra_config;

            var available_application = [];
            angular.forEach(angular.element($("input[name='available_application']:checked")), function (input_component){
                var app_comp_id = angular.element(input_component).val();
                available_application.push(component_info[app_comp_id]);
            });
            api_data_param['available_application'] = available_application;
            
            var available_infra = [];
            if($scope.infra){
                angular.forEach(component_info, function (comp){
                   if(comp.component_type == 'Infrastructure'){
                        available_infra.push(comp);
                   } 
                });
            }
            api_data_param['available_infra'] = available_infra;
            api_data_param['infra'] = $scope.infra;
            api_data_param['infraConf'] = $scope.ICFullyAutomatedData;
            api_data_param['app'] = $scope.appFullyAutomatedData;
            output_obj['api_data_param'] = api_data_param;
            var $thisURL = '/deployment/yamlgeneration/';
            $.ajax({
                method: "POST",
                url: $thisURL,
                data: JSON.stringify(output_obj),
                success: YamlFormSuccess,
                error: YamlFormError, // add your error function
            })
        }
    };

        function YamlFormSuccess(data, textStatus, jqXHR) {
            $('.yamldata').html(data);
            $("#yamlPopup").modal();
        }

        function YamlFormError(data, textStatus, jqXHR) {
            data =  'YAML can not be generated';
            $('.yamldata').html(data);
            $("#yamlPopup").modal();
        }

//  function call on initialization onload of form
        $scope.initializeForm = function(){
            $scope.getInfra();
            $scope.fullyAutomatedData = true;
            $scope.infraFullyAutomatedData = false;
            $scope.ICFullyAutomatedData = false;
            $scope.appFullyAutomatedData = false;
            $scope.check_list_app = [];
            $scope.check_list_infraconfig = [];
        }

        /* uncheck all App component on uncheck app component type */
        $scope.clearAppComp = function () {
            $scope.checkCommonParams();
            if (!$scope.app) {
                var apparray = document.getElementsByName('available_application');
                for (var i = 0; i < apparray.length; i++) {
                    apparray[i].checked = false;
                }
            }
            $scope.compVal();
        }

        /* uncheck all infrconfig component on uncheck infraconfig component type */
        $scope.clearInfraConfigComp = function () {
            $scope.checkCommonParams();
            if (!$scope.infraConf) {
                var icarray = document.getElementsByName('available_infra_config');
                for (var i = 0; i < icarray.length; i++) {
                    icarray[i].checked = false;
                }
            }
            $scope.compVal();
        }


        $scope.checkCommonParams = function(){
            if($scope.app){
                $('#deploy-form input, #deploy-form select').each(
                    function(index){ 
                        var input = $(this); 
                        var dataInternalName = input.attr('data-internal-name');
                        if(dataInternalName != undefined){
                            var id = input.attr('id');
                            var ele = document.getElementById(id);
                            var aele = angular.element(ele);
                            var inputBlockClass = aele.parent().attr('class');
                            if(inputBlockClass === 'app-class'){
                                if(dataInternalName == "'booleanParams'.'kitchenci_deploy_noop'" || dataInternalName == "'booleanParams'.'puppet_noop'" ){
                                    if($scope.infraConf && $scope.ICFullyAutomatedData){
                                        aele.parent().parent().css('display','none');
                                        aele.val('');
                                    }
                                    else{
                                        aele.parent().parent().css('display','table-row');
                                    }
                                }                              
                                
                            }
                        }
                    }
                );
            }
            
        }

        /* ESMT 770 function to check manual or fully automated deployement of  infrastructure type components */
        $scope.clearInfraComp = function(){
            $timeout(function () {
                $scope.checkAzure();
            }, 1000);
  
            //var infra_component_selected = event.target.checked;
            //if(infra_component_selected == true){
            if($scope.infra){
                $scope.infraFullyAutomatedData = true;  
            }else{
                $scope.infraFullyAutomatedData = false; 
             }

             if($scope.ICFullyAutomatedData == true || $scope.appFullyAutomatedData == true || $scope.infraFullyAutomatedData == true){
                 $scope.fullyAutomatedData = true;
             }
             else{
                $scope.fullyAutomatedData = false;
             } 
        }

        $scope.checkAzure = function(){
            if($scope.infra){
                $('#deploy-form input, #deploy-form select').each(
                    function(index){ 
                        var input = $(this); 
                        var dataInternalName = input.attr('data-internal-name');
                        var id = input.attr('id');
                        var ele = document.getElementById(id);
                        var aele = angular.element(ele);
                        if(dataInternalName != undefined){
                            if($scope.host == 2){
                                if(dataInternalName.indexOf('azure') !== -1){
                                    aele.parent().parent().css('display','table-row');
                                    aele.attr('required','required');
                                    aele.parent().prev().addClass('required');
                                }
                            }
                            else{
                                if(dataInternalName.indexOf('azure') !== -1){  
                                    aele.parent().parent().css('display','none');
                                    aele.val('');
                                    if(ele.hasAttribute('required')){
                                        ele.removeAttribute('required');
                                    }
                                    
                                    if(ele.className== 'input-group date'){
                                        ele.children[1].click();
                                    }   
                                }
                            }
                        }
                    }
                );
                
            }
        }


        /* ESMT 770 function to check manual or fully automated deployement of  infra config and application type components */
        $scope.compVal = function(event){
            /*var component_input_id = event.target.id;
            var component_selected = event.target.checked;
            var component_value= event.target.value;*/
            var comp_list = [];
            var compListIC = []; 
            var compListApp = []; 
            $scope.check_list_app = [];
            $scope.check_list_infraconfig = [];
    
            var i = 0;
            $('.input_component_checkbox').each(
                function(index){  
                var input = $(this);
                var comp_list_id = input.val();
                if(comp_list_id != ''){
                    var component_info = angular.element($('#component_info')).val();
                    component_info = JSON.parse(component_info);
                    var get_ele = component_info[comp_list_id];
                    var comp_status = input.is(":checked");
                    if(comp_status == true){
                        if(get_ele['component_type'] == 'Application'){
                            $scope.check_list_app.push(comp_list_id);
                        }
                        if(get_ele['component_type'] == 'Infrastructure Configuration'){
                            $scope.check_list_infraconfig.push(comp_list_id);
                        }
    
                        if(get_ele['deployment_type_description'] == 'Manual'){
                            comp_list[i] = 'Manual_'+comp_list_id+'_'+input.is(":checked");
                            if(get_ele['component_type'] == 'Infrastructure Configuration'){
                                compListIC[i] = 'Manual_'+comp_list_id+'_'+input.is(":checked")+'_ic';
                                i++;
                            }
                            if(get_ele['component_type'] == 'Application'){
                                compListApp[i] = 'Manual_'+comp_list_id+'_'+input.is(":checked")+'_app';
                                i++;
                            }
                        }
                   
                    }
                    else{
                        if(get_ele['component_type'] == 'Application'){
                            var index = $scope.check_list_app.indexOf(comp_list_id);
                            if (index > -1) {
                                $scope.check_list_app = $scope.check_list_app.filter(function(item) { 
                                    return item !== comp_list_id;
                                })
                                
                                //$scope.check_list_app.splice(index, 1);
                            }
                        }
                        if(get_ele['component_type'] == 'Infrastructure Configuration'){
                            var index = $scope.check_list_infraconfig.indexOf(comp_list_id);
                            if (index > -1) {
                                //$scope.check_list_infraconfig.splice(index, 1);
                                $scope.check_list_infraconfig = $scope.check_list_infraconfig.filter(function(item) { 
                                    return item !== comp_list_id;
                                })
                            }
                        }
                        
                    }
                }
            });

           
        $scope.check_list_infraconfig = Array.from(new Set($scope.check_list_infraconfig));
        compListIC = compListIC.filter(function (el) {
            return el != null;
        });
          
        if(compListIC.length === $scope.check_list_infraconfig.length)
        {
            $scope.ICFullyAutomatedData = false;
        }else{
            $scope.ICFullyAutomatedData = true;   
        }

        $scope.check_list_app = Array.from(new Set($scope.check_list_app));
        compListApp = compListApp.filter(function (el) {
            return el != null;
        });
        
        if(compListApp.length === $scope.check_list_app.length)
        {
            $scope.appFullyAutomatedData = false;
        }else{
            $scope.appFullyAutomatedData = true;   
        }
       
        $scope.checkCommonParams();
        if($scope.ICFullyAutomatedData == true || $scope.appFullyAutomatedData == true || $scope.infraFullyAutomatedData == true){
            $scope.fullyAutomatedData = true;
        }
        else{
            $scope.fullyAutomatedData = false;
        }
        
    }


});