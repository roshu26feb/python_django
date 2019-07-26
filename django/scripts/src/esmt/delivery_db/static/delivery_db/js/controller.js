myApp.controller("deliveryDBCtrl", function($scope, $http, $timeout, myService) {
    $scope.showError = false;
    $scope.filterVersion = function(comp_name){
        return function(components){
          angular.forEach(components, function(comp){
              if(comp.component_name == comp_name){
                  return comp.components_versions;
              };
          });
        }
    };
    $scope.filterByDate = function(elm){
        var date = new Date(elm.creation_date)
        elm.creation_date = date.getTime();
        return elm;
    };
    $scope.filterInVer = function(e) {
        return $scope.sys_ele_in_ver.indexOf(e.system_element_id) !== -1;
    }  
// Perform Scope Apply to show the changes
    var applyScope = function(){
        $scope.$apply(function(){
            $scope.show = true;
            $scope.loading = false;
            $scope.initLoading = false;
        });
    }
// Show loading
    $scope.onLoading = function(){
        $scope.initLoading = true;
        $scope.show = false;
    }
// Handle Failure response
    var handleFailureResponse = function(resp){
        resp.fail(function(req, status, err){
            $scope.$apply(function(){
                $scope.initLoading = false;
                $scope.loading = false;
            });
            if (status ==  "timeout"){
                 $scope.$apply(function(){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Time out Error"
                 });
            }else if( status ==  "error"){
                 $scope.$apply(function(){   
                     $scope.reqFailed = true;
                     $scope.errMsg = err;
                 });
            }
        });
    };
// Initialize values
    var initializeApiCall = function(initialSortType){
        $scope.sortType = initialSortType;
        $scope.sortReverse = false;
        $scope.search = '';
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
    };

    $scope.getSystemById = function(id){
      if(id != undefined){
        $scope.sortType1 = "creation_date";
        $scope.sortReverse1 = false;
        $scope.search = '';
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        var url_val = '/api/get_system_by_id/' + id + '/';
        var getSystemsResponse = myService.getAJAXObject(url_val);
        getSystemsResponse.done(function(status){
            var syslist = $.parseJSON(status);
            $scope.systems = syslist["systems"][0];
            applyScope();
        });
        handleFailureResponse(getSystemsResponse);
      }else{
        $scope.systems = [];
      };
    };



    $scope.getSystemVersionById = function(id){
      $scope.system_versions = [];
      if(id != undefined){
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        var url_val = '/api/get_system_version_by_id/' + id + '/';
        var getSystemVersionResponse = myService.getAJAXObject(url_val);
        getSystemVersionResponse.done(function(status){
            var sysversionlist = $.parseJSON(status);
            $scope.system_versions = sysversionlist["system_versions"];
            applyScope();
        });
        handleFailureResponse(getSystemVersionResponse);
      }else{
        $scope.systems = [];
      };
    };

    // Handle Get Systems Api Call
    $scope.getSystems = function(){
        $scope.sortType1 = "creation_date";
        $scope.sortReverse1 = false;
        initializeApiCall("system_name");
        var url_val = '/api/get/system';
        var getSystemsResponse = myService.getAJAXObject(url_val);
        getSystemsResponse.done(function(status){
            var syslist = $.parseJSON(status);
            $scope.systems = syslist["systems"];
            applyScope();
        });
        handleFailureResponse(getSystemsResponse);
    };

    $scope.getSystemElements = function(id){
        $scope.system_elements = [];
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        if(id != undefined && id != ''){
            var url_val = '/api/get_system_element_by_id/' + id ; 
            var getSystemElementResponse = myService.getAJAXObject(url_val);
            getSystemElementResponse.done(function(status){
                var systemEleList = $.parseJSON(status);
                $scope.system_elements = systemEleList["system_elements"];
                applyScope();
            });
            handleFailureResponse(getSystemElementResponse);
        }else{
            $scope.systems = [];
        };
    };

    $scope.getElementType = function(){
        
        initializeApiCall("system_element_type_name");
        var url_val = '/api/get/system_element_type';
        var getSystemElementResponse = myService.getAJAXObject(url_val);
        getSystemElementResponse.done(function(status){
            $scope.systemEleResponse = $.parseJSON(status);
            $scope.system_element_types = $scope.systemEleResponse["system_element_types"]; 
            applyScope();
        });
        handleFailureResponse(getSystemElementResponse);
    };

    // Handle Get Component Api Call
    $scope.getComponents = function(){
        $scope.sortType1 = "creation_date";
        $scope.sortReverse1 = false;
        initializeApiCall("component_name");
        var url_val = '/api/get/component';
        var getComponentsResponse = myService.getAJAXObject(url_val);
        getComponentsResponse.done(function(status){
            var complist = $.parseJSON(status);
            $scope.components = complist["components"];
            applyScope();
        });
        handleFailureResponse(getComponentsResponse);
    };

    // Handle Get Instance Api Call
    $scope.getInstances = function(){
        // console.log("Called By Devendra");
        $scope.sortType = "instance_state";
        $scope.sortReverse = true;
        $scope.search = '';
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        var url_val = '/api/get_instance_list_without_destroyed';
        var getInstancesResponse = myService.getAJAXObject(url_val);
        getInstancesResponse.done(function(status){
            var inslist = $.parseJSON(status);
            //$scope.instances = inslist["instances"];
            $scope.instances = inslist;
            applyScope();
        });
        handleFailureResponse(getInstancesResponse);
    };

    // Handle Get Disk Type Api Call
    $scope.getDiskType = function(){
        $scope.instance_disks = [];
        var url_val = '/api/get/disk_type';
        var getDiskTypeResponse = myService.getAJAXObject(url_val);
        getDiskTypeResponse.done(function(status){
            var diskTypeList = $.parseJSON(status);
            $scope.disk_types = diskTypeList["disk_types"];
            applyScope();
        });
        handleFailureResponse(getDiskTypeResponse);
    };

    // Handle Get Infrastructure Template Api Call
    $scope.getInfra = function(){
        initializeApiCall("infra_template_name");
        var url_val = '/api/get/infrastructure_template';
        var getInfraResponse = myService.getAJAXObject(url_val);
        getInfraResponse.done(function(status){
            var infraList = $.parseJSON(status);
            $scope.infraNames = infraList["infrastructure_templates"];
            applyScope();
        });
        handleFailureResponse(getInfraResponse);
    };

    $scope.getInfraById = function(id){
      if($scope.infra_id != undefined){
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        var url_val = '/api/get_infra_by_id/' + $scope.infra_id + '/';
        var getInfraIdResponse = myService.getAJAXObject(url_val);
        getInfraIdResponse.done(function(status){
            var syslist = $.parseJSON(status);
            $scope.instance_disks = [];
            $scope.infraID = syslist["infrastructure_templates"][0];
            applyScope();
        });
        handleFailureResponse(getInfraIdResponse);
      }else{
        $scope.infraID = {};
      };
    };
    

    $scope.getEnvType = function(){
        initializeApiCall("environment_type_name");
        var url_val = '/api/get/environment_type';
        var getEnvTypeResponse = myService.getAJAXObject(url_val);
        getEnvTypeResponse.done(function(status){
            var EnvTypeList = $.parseJSON(status);
            $scope.environment_types = EnvTypeList["environment_types"];
            applyScope();
        });
        handleFailureResponse(getEnvTypeResponse);
    };

    $scope.getSystemNetworkSet = function(){
        initializeApiCall("system_network_set_name");
        var url_val = '/api/get/system_network_set';
        var getSysNetSetResponse = myService.getAJAXObject(url_val);
        getSysNetSetResponse.done(function(status){
            var SysNetSetList = $.parseJSON(status);
            $scope.system_network_sets = SysNetSetList["system_network_sets"];
            applyScope();
        });
        handleFailureResponse(getEnvTypeResponse);
    };

    $scope.getEnvSubType = function(){
        initializeApiCall("environment_subscription_type_name");
        var url_val = '/api/get/environment_subscription_type';
        var getEnvSubTypeResponse = myService.getAJAXObject(url_val);
        getEnvSubTypeResponse.done(function(status){
            var EnvSubList = $.parseJSON(status);
            $scope.environment_subscriptions = EnvSubList["environment_subscription_types"];
            applyScope();
        });
        handleFailureResponse(getEnvSubTypeResponse);
    };


    $scope.getHostSite = function(){
        initializeApiCall("host_site_name");
        var url_val = '/api/get/host_site';
        var getHostSiteResponse = myService.getAJAXObject(url_val);
        getHostSiteResponse.done(function(status){
            var HostSiteList = $.parseJSON(status);
            $scope.host_sites = HostSiteList["host_sites"];
            applyScope();
        });
        handleFailureResponse(getHostSiteResponse);
    };

    $scope.getSysEleType = function(){
        initializeApiCall("system_element_type_name");
        var url_val = '/api/get/system_element_type';
        var getSysEleTypeResponse = myService.getAJAXObject(url_val);
        getSysEleTypeResponse.done(function(status){
            var SysEleTypeList = $.parseJSON(status);
            $scope.system_element_types = SysEleTypeList["system_element_types"];
            applyScope();
        });
        handleFailureResponse(getSysEleTypeResponse);
    };


    $scope.getApiDetails = function(model){
        initializeApiCall(model + "_name")
        var url_val = '/api/get/' + model;
        var getApiDetailsResponse = myService.getAJAXObject(url_val);
        getApiDetailsResponse.done(function(status){
            $scope.apiResponse = $.parseJSON(status);
            applyScope();
        });
        handleFailureResponse(getApiDetailsResponse);
    };

//call Instance Update
$scope.callUpdate = function(inst_id){
  if(inst_id != undefined && inst_id != ''){
      $(location).attr('href','/delivery_db/instance_update/' + inst_id)
  }
};

//system Element releated stuff here
$scope.addSystemElement = function(){
    var sysCompCnt = 0;
    if($scope.system_element == undefined){$scope.system_element = [] }; 
    if($scope.system_element.length > 0){
        $scope.system_element.push({'system_element_id' : -1,
            'system_element_components': [{
            'name': 'compVer' + sysCompCnt,
            'sys_ele_comp_id': -1
            }]
        });
    }else{
        $scope.system_element.push({'system_element_id' : -1,
            'system_element_components': [
            {'name': 'compVer' + sysCompCnt, 'sys_ele_comp_id': -1 }
            ]
        });    
    };
};
$scope.removeSystemElement = function(index){
    if (index === -1){
        $scope.system_element = [];
    }else{
        $scope.system_element.splice(index, 1);
    }
};
$scope.addNewSysEleComp = function(outerIndex, innerIndex) {
    var system_element_comp = $scope.system_element[outerIndex]["system_element_components"]
    var newItemNo = system_element_comp.length;
    system_element_comp.push({ 'name': 'compVer'+newItemNo, 'sys_ele_comp_id': -1});
};
$scope.removeSysEleComp = function(outerIndex, innerIndex) {
    var system_element_comp = $scope.system_element[outerIndex]["system_element_components"]
    system_element_comp.splice(innerIndex, 1);
    //console.log($scope.system_element)
};
    $scope.getSystemElementComponentsById = function(sys_ver_id){
        $scope.sys_element_components = [];
        var url_val = '/api/get_system_element_component_by_id/'+ sys_ver_id;
        var getSysEleCompResponse = myService.getAJAXObject(url_val, async=false);
        getSysEleCompResponse.done(function(status){
            var sysEleCompList = $.parseJSON(status);
            var sysEleCompList_array = [];
            var sysEleCompList_infra = [];
            angular.forEach(sysEleCompList["system_element_components"], function(list,val){
                if(list['component_version']['component']['component_type']['component_type_description'] == 'Infrastructure')
                {
                    sysEleCompList_infra.push(list);
                }
            });

            sysEleCompList_infra.sort(function(a,b) {
                if ( a.install_order < b.install_order )
                    return -1;
                if ( a.install_order > b.install_order )
                    return 1;
                return 0;
            } );

            var sysEleCompList_infraConf = [];
            angular.forEach(sysEleCompList["system_element_components"], function(list,val){
                if(list['component_version']['component']['component_type']['component_type_description'] == 'Infrastructure Configuration')
                {
                    sysEleCompList_infraConf.push(list);
                }
            });

            sysEleCompList_infraConf.sort(function(a,b) {
                if ( a.install_order < b.install_order )
                    return -1;
                if ( a.install_order > b.install_order )
                    return 1;
                return 0;
            } );
            sysEleCompList_app = [];
            angular.forEach(sysEleCompList["system_element_components"], function(list,val){
                if(list['component_version']['component']['component_type']['component_type_description'] == 'Application')
                {
                    sysEleCompList_app.push(list);
                }
            });

            sysEleCompList_app.sort(function(a,b) {
                if ( a.install_order < b.install_order )
                    return -1;
                if ( a.install_order > b.install_order )
                    return 1;
                return 0;
            } );
            sysEleCompList_array = sysEleCompList_infra.concat(sysEleCompList_infraConf, sysEleCompList_app);
            $scope.sys_element_components = sysEleCompList_array;
            
            $scope.sys_ele_in_ver =  uniqueValuesByKey($scope.sys_element_components, 'system_element_id'); 
            //applyScope();
        });
        //handleFailureResponse(getSysEleCompResponse);
    };

    $scope.getSystemElementById = function(sys_id){
        $scope.system_elements = [];
        var url_val = '/api/get_system_element_by_id/' + sys_id;
        var getSysEleResponse = myService.getAJAXObject(url_val);
        getSysEleResponse.done(function(status){
            var sysEleList = $.parseJSON(status);
            $scope.system_elements = sysEleList["system_elements"];
            //console.log($scope.system_elements);
            applyScope();
        });
        handleFailureResponse(getSysEleResponse);
    };

    var traverseComponent = function(comp_id){
        var comp_obj = []
        angular.forEach($scope.components, function(comp){
            if (comp.component_id == comp_id){
                comp_obj.push(comp);
            }
        });
        return comp_obj;
    };
    // check if the system element with the same system element name already exists for that system
    $scope.IsSEExists = function(se){
        notUpdate = true;
        angular.forEach($scope.system_elements, function(sys_ele){
            if (sys_ele.system_element_name == se.sys_element.sys_ele_name ){   
                se.system_element_id = sys_ele.system_element_id;
                notUpdate = false;
            }else{
                if (notUpdate){
                    se.system_element_id = -1;
                }
            };
        });
    };
//
    $scope.addSysVersionElementComponent = function(obj){
        $scope.system_element = undefined;
        $scope.system_element = [];
        var sysEleCnt = 0;
        if (obj){
            //getSystemElementComponents(obj.system_version_id)
            var url_val = '/api/get_system_element_component_by_id/' + obj.system_version_id;
            var getSysEleCompResponse = myService.getAJAXObject(url_val, async=false);
            getSysEleCompResponse.done(function(status){
                var sysEleCompList = $.parseJSON(status);
                $scope.system_element_components = sysEleCompList["system_element_components"];
               
                if($scope.system_elements.length >0){
                    angular.forEach($scope.system_elements, function(sys_element){
                        var system_element_component = [];
                        var sysEleCompCnt = 0;
                        angular.forEach($scope.system_element_components, function(sys_ele_comp){
                            if (sys_ele_comp.system_element_id == sys_element.system_element_id ){
                                var component_obj = traverseComponent(sys_ele_comp.component_version.component.component_id)
                                system_element_component.push({'sys_ele_comp_id': sys_ele_comp.system_element_component_id,
                                'comp_type': sys_ele_comp.component_version.component.component_type,
                                'comp_name': component_obj[0],
                                'comp_ver': sys_ele_comp.component_version,
                                'compDeployementOrder': sys_ele_comp.install_order });
                            }
                        });
                        if (system_element_component.length != 0){
                        //$scope.$apply(function(){
                            $scope.system_element.push({'system_element_id': sys_element.system_element_id, 'sys_element': {'sys_ele_name': sys_element.system_element_name, 'sys_ele_short_name': sys_element.system_element_short_name, 'sys_ele_type': sys_element.system_element_type}, 
                                'system_element_components' : system_element_component
                            });
                        //});
                        };  
                        sysEleCompCnt = sysEleCompCnt + 1;
                   });
                }else{
                    $scope.system_element.push({'system_element_id': -1 ,'sys_element' : {}, 'system_element_components': [{'name': 'compVer' + sysEleCnt, 'sys_ele_comp_id': -1}]});
                }
          });
        }else{
            $scope.system_element.push({'system_element_id': 'sysEle-1', 'system_element' : {}, 'system_element_components': [{'name': 'compVer' + sysEleCnt, 'sys_ele_comp_id': -1}]});
        }
        //console.log($scope.system_element);
    };
    $scope.addSysVersionComponent = function(obj){
        $scope.system_ver_comp = []
        var sysCompCnt = 0;
        if (obj){
            if(obj.system_version_components.length >0){
                angular.forEach(obj.system_version_components, function(comp){
                    var component_obj = traverseComponent(comp.component_version.component.component_id)
                    $scope.system_ver_comp.push({'name': 'compVer' + sysCompCnt,
                    'comp_type': comp.component_version.component.component_type,
                    'comp_name': component_obj[0],
                    'comp_ver': comp.component_version });
                    sysCompCnt = sysCompCnt + 1;
                });
            }else{
                $scope.system_ver_comp.push({'name': 'compVer' + sysCompCnt});
            }
        }else{
            $scope.system_ver_comp.push({'name': 'compVer' + sysCompCnt});
        }
    }
    $scope.removeSysVerComp = function(index){
        if (index === -1){
            $scope.system_ver_comp = [];
        }else{
            $scope.system_ver_comp.splice(index, 1);
        }
    };
    $scope.addNewSysVerComp = function() {
        var newItemNo = $scope.system_ver_comp.length+1;
        $scope.system_ver_comp.push({ 'name': 'compVer'+newItemNo });
    };
    $scope.addComponent = function(){
        $scope.system_comp = [{ name: "component1", comp_ver: "compVer1" }];
    }
    $scope.removeComponent = function(){
        $scope.system_comp = [{}];
    }
    $scope.system_comp = [{ name: "component1", comp_ver: "compVer1" }];
    $scope.addNewComp = function() {
        var newItemNo = $scope.system_comp.length+1;
        $scope.system_comp.push({ 'name': 'component'+newItemNo, 'comp_ver': 'compVer'+newItemNo });
    };

    $scope.removeComp = function(index) {
        // remove the row specified in index
        $scope.system_comp.splice( index, 1);
        // if no rows left in the array create a blank array
        if ( $scope.system_comp.length === 0 || $scope.system_comp.length == null){
            alert('no rec');
            $scope.system_comp.push = [{ name: "component1", comp_ver: "compVer1" }];
        }
    }
   $(".remove, .addComp").click(function(e) {
    e.preventDefault();
  });

// Code related to Add Instance Disk
$scope.addInstanceDisk = function(){
    $scope.instance_disks = [];
    $scope.instance_disks.push({'diskCnt': 1});
};
$scope.addNewInstanceDisk = function() {
    var newItemCount = $scope.instance_disks.length+1;
    $scope.instance_disks.push({ 'diskCnt': newItemCount });
};
$scope.removeInstanceDisk = function(index){
    if (index === -1){
        $scope.instance_disks = [];
    }else{
        $scope.instance_disks.splice(index, 1);
    }
};

$scope.checkOSDisk = function(indx){
      OSDiskCnt = 0
     // console.log($scope.instance_disks);
      $scope.instance_disks[indx]['disk_size'] = $scope.instance_disks[indx]["disk_type_id"]["min_size"];
      angular.forEach($scope.instance_disks, function(inst_disk, index){
           disk_desc = inst_disk["disk_type_id"]["disk_type_description"].toUpperCase();           
           if(disk_desc.indexOf("OS") != -1){
               OSDiskCnt = OSDiskCnt + 1;
               if (OSDiskCnt >=2){
                   $scope.instance_disks.splice(index, 1);
                   alert("Maximum OS Disks Allowed is 1");
               };
           };
      });
}
$scope.isDeploymentOrderPresent = function (sysElement, sysComp) {
           var isValid = false;
           var filterdata = (sysElement.system_element_components.filter(e => e.compDeployementOrder === sysComp.compDeployementOrder && e.comp_type.component_type_id === sysComp.comp_type.component_type_id));
           isValid = (filterdata.length <= 1) ? true : false;
           if (!isValid) {
               sysComp.compDeployementOrder="";
               $scope.errMsg = "Deployment order can not be duplicate for specific component type.";
               $timeout(
                   function () { $scope.showError = true }, 60
               )
           }
           else {
               $scope.errMsg = "";
               $timeout(
                   function () { $scope.showError = false }, 60
               )
           }
           return isValid;
       }

    $scope.checkInfraComponentType = function (sysElement, sysComp) {
        var isValid = false;
        var filterdata = (sysElement.system_element_components.filter(e => e.comp_type.component_type_id === sysComp.comp_type.component_type_id && sysComp.comp_type.component_type_id === 3));
        isValid = (filterdata.length <= 1) ? true : false;

        if (!isValid) {
            delete sysComp.comp_type ;
            $scope.errMsg = "A System Element should have only one Infrastructure component type. ";
            $timeout(
                function () { $scope.showError = true }, 60
            )
        }
        else {
            $scope.errMsg = "";
            $timeout(
                function () { $scope.showError = false }, 60
            )
        }
        return isValid;
    }

    $scope.isSENameExist = function(inputSE){
        SEName = [];
        angular.forEach($scope.system_element,function(se){
            if(se.sys_element != undefined){
                SEName.push(se.sys_element.sys_ele_name.toLowerCase());
            }
        });
       
        var arr = SEName;
        var sortedArr = arr.slice().sort(); 
        var results = [];
        for (var i = 0; i < sortedArr.length - 1; i++) {
            if (sortedArr[i + 1] == sortedArr[i]) {
                results.push(sortedArr[i]);
            }
        }

        isValid = (results.length < 1) ? true : false;
        str = '';
        if (!isValid) {    
            inputSE.sys_element.sys_ele_name = '';
            results.forEach(function(item){ 
                str =  str + item +'';
            });
            
            $scope.errMsg = "Duplicate System Element Name '"+ str + "'.";
            $timeout(
                function () { $scope.showError = true }, 60
            )
        }
        else {
            $scope.errMsg = "";
            $timeout(
                function () { $scope.showError = false }, 60
            )
        }
        return isValid;        
    }


    $scope.disk_size_type = [
        {'name': 'gb',
        'desc': 'GB'}
    ];

    $scope.manipulateEnvSet = function(envSet){
        envSet["env_cnt"] = envSet["environments_linked"].length;
        env_data_type_id = undefined;
        env_type_id = undefined;
        same_env_type = true;
        same_env_data_type = true;
        angular.forEach(envSet["environments_linked"], function(value){
            if (env_data_type_id == undefined){
                env_data_type_id = value["environment"]["environment_data_type"]["environment_data_type_id"];
            };
            if (env_type_id == undefined){
                env_type_id = value["environment"]["environment_type"]["environment_type_id"]
            };
            if (env_type_id != value["environment"]["environment_type"]["environment_type_id"]){
                same_env_type = false;
            }else{
                envSet["env_type"] = value["environment"]["environment_type"]["environment_type_name"]
            };
            if (env_data_type_id != value["environment"]["environment_data_type"]["environment_data_type_id"]){
                same_env_data_type = false;
            }else{
                envSet["env_data_type"] = value["environment"]["environment_data_type"]["environment_data_type_name"]
            };
        });
        if (!same_env_data_type){
            envSet["env_data_type"] = "Mixed"
        };
        if (!same_env_type){
            envSet["env_type"] = "Mixed"
        };
    };
/*$(document).on('click', '.accordion-toggle', function(e) {
        e.preventDefault();

        var $this = $(this);
        var openedClass = 'glyphicon-minus-sign';
        var closedClass = 'glyphicon-plus-sign';

        if ($this.next().hasClass('show')) {
            var icon = $(this).children().children().children('i:first');
            icon.toggleClass(openedClass + " " + closedClass);
            $(this).children().children().children().find('i:first').toggleClass(openedClass + " " + closedClass);
            $this.next().removeClass('show');
            $this.next().slideUp(350);
        } else {
            $this.parent().parent().find('.indicator').removeClass(openedClass).addClass(closedClass);
            var icon = $(this).children().children().children('i:first');
            icon.toggleClass(openedClass + " " + closedClass);
            $(this).children().children().children().find('i:first').toggleClass(openedClass + " " + closedClass);
            $this.parent().parent().find('li .inner').removeClass('show');
            $this.parent().parent().find('li .inner').slideUp(350);
            $this.next().toggleClass('show');
            $this.next().slideToggle(350);
        }
    });
*/
    $('#id_creation_date_1').attr('placeholder', 'Creation Time');
    var links = $('a[role="button"]');
    links.on('show.bs.tab', function(e){
        $('a[aria-expanded="true"]').addClass("active");
        $('a[aria-expanded="false"]').removeClass("active");
    })
    var $myForm = $('.my-form')
    $myForm.click(function(event){
        $(".alert").removeClass("alert-success alert-danger show in");
    })
    $myForm.submit(function(event){
       
        $(".alert").removeClass("alert-success alert-danger show in");
        event.preventDefault()
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
        $.ajax({ method: "POST", url: $thisURL, data: $formData, success: handleFormSuccess, error: handleFormError, })
    })

    function handleFormSuccess(data, textStatus, jqXHR){
        
        if(data.url){
            $(location).attr('href',data.url)
        }
        var obj = jQuery.parseJSON(jqXHR.responseJSON);
        $(".a-text").remove();
        $.each(obj, function(key,value) {
          $("#alert").removeClass("alert-danger").addClass("alert-success show in");
          $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + ' '+ '</span>');
        });
        $myForm[0].reset(); // reset form data
        $('.filter-option').html('--Select--');
        $scope.system_element = []; //reset the system element form
        $scope.systems = [];
        $timeout(function() {
            angular.element('#rm-cmp').triggerHandler('click');
        }, 0);

        //  ESMT-777
        $(".selectpicker").selectpicker("refresh");
        // ESMT-836
        $scope.system_version = null;
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        var obj = jQuery.parseJSON(jqXHR.responseJSON);
        $(".a-text").remove();
        $.each(obj, function(key,value) {
          $("#alert").removeClass("alert-success").addClass("alert-danger show in");
          $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + '</span>');
        });
    }
 $.fn.extend({
        treed: function (o) {

          var openedClass = 'glyphicon-minus-sign';
          var closedClass = 'glyphicon-plus-sign';

          if (typeof o != 'undefined'){
            if (typeof o.openedClass != 'undefined'){
            openedClass = o.openedClass;
            }
            if (typeof o.closedClass != 'undefined'){
            closedClass = o.closedClass;
            }
          };

            //initialize each of the top levels
            var tree = $(this);
            tree.addClass("tree");
            tree.find('li').has("ul").each(function () {
                var branch = $(this); //li with children ul
                branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>");
                branch.addClass('branch');
                branch.on('click', function (e) {
                    if (this == e.target) {
                        var icon = $(this).children('i:first');
                        icon.toggleClass(openedClass + " " + closedClass);
                        $(this).children().children().toggle();
                    }
                })
                branch.children().children().toggle();
            });
            //fire event from the dynamically added icon
          tree.find('.branch .indicator').each(function(){
            $(this).on('click', function () {
                $(this).closest('li').click();
            });
          });
            //fire event to open branch if the li contains an anchor instead of text
            tree.find('.branch>a').each(function () {
                $(this).on('click', function (e) {
                    $(this).closest('li').click();
                    e.preventDefault();
                });
            });
            //fire event to open branch if the li contains a button instead of text
            tree.find('.branch>button').each(function () {
                $(this).on('click', function (e) {
                    $(this).closest('li').click();
                    e.preventDefault();
                });
            });
            tree.find('.branch>span').each(function () {
                $(this).on('click', function (e) {
                    $(this).closest('li').click();
                    e.preventDefault();
                });
            });

        }
    });

    //Initialization of treeviews

    $('#tree1').treed();

    $('#tree2').treed({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});

    $('#tree3').treed({openedClass:'glyphicon-chevron-right', closedClass:'glyphicon-chevron-down'});

});