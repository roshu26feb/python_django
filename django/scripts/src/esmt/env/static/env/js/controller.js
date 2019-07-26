myApp.controller('envController', ['$scope', '$window', '$interval','myService','$timeout',function($scope, $window, $interval, myService,$timeout){

    // Set the name of the hidden property and the change event for visibility
    var hidden, visibilityChange;
    if (typeof document.hidden !== "undefined") { // Opera 12.10 and Firefox 18 and later support
      hidden = "hidden";
      visibilityChange = "visibilitychange";
    } else if (typeof document.msHidden !== "undefined") {
      hidden = "msHidden";
      visibilityChange = "msvisibilitychange";
    } else if (typeof document.webkitHidden !== "undefined") {
      hidden = "webkitHidden";
      visibilityChange = "webkitvisibilitychange";
    }

    var PageVisible = true;
    document.addEventListener(visibilityChange, function(){
        if (document[hidden]) {
            PageVisible = false;
         }else{
            PageVisible = true;
         }
    }, false);


    var polling_store_num = '';

   var beforeAJAXCall = function(){
//       $scope.$apply(function(){
            $scope.loading = true;
            $scope.showTab = false;
            $scope.reqFailed = false;
//       });
   }
// Handle get Store and client service status Click

    $scope.getServiceStatus = function($store){
        var isCollapsed = $("[href='#" + $store  + "']").attr("aria-expanded");
        if (isCollapsed == "false"){
            polling_store_num = $store;
            //var url_val = '../static/data/' + $store + '.json';
            var url_val = 'service/socrates/' + $store + '/status';
            beforeAJAXCall();
            $scope.updateStatus();
            var serviceStatusResponse = myService.getAJAXObject(url_val);
            serviceStatusResponse.done(function(status){
                var status_object = $.parseJSON(status);
                updateTabServiceStatus($store,status_object);
                $scope.$apply(function(){
                    $scope.showTab = true;
                    $scope.loading = false;
                });
            });
            serviceStatusResponse.fail(function(req, status, err){
                $scope.loading = false;
                if (status ==  "timeout"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Time out Error"
                }else if( status ==  "error"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Requested Service Data not found"
                }
            });
        }
    }
// Show loading
    $scope.onLoading = function(){
            $scope.initLoading = true;
            $scope.show = false;
    }

// get Server status
    $scope.checkServerStatus = function($ip, last_node){
        last_node = last_node || "not a last node";
        var url_val = 'server/socrates/status/'+ $ip;
        var ServerStatusResponse = myService.getAJAXObject(url_val);
        ServerStatusResponse.done(function(status){
            if (status == "btn-success"){
                $("[href='#" + $ip  + "']").removeClass("btn-danger").addClass("btn-success").html("Service Details");
            }else{
                $("[href='#" + $ip  + "']").removeClass("btn-success").addClass("btn-danger").html("Server Down");
            }
            if (last_node == 'last-node'){
                $scope.$apply(function(){
                    $scope.initLoading = false;
                    $scope.show = true;
                });
            }
        });
        ServerStatusResponse.fail(function(req, status, err){
            $scope.loading = false;
            if (status ==  "timeout"){
                 $scope.reqFailed = true;
                 $scope.errMsg = "Time out Error"
            }else if( status ==  "error"){
                 $scope.reqFailed = true;
                 $scope.errMsg = "Requested Store Server data not found";
            }

        });
    }

// Handle Fix Store comms fix
    $scope.handleStoreCommsFix = function($ip, $action){
        var boolRun = false;
        //$scope.showRepl = false;
        $scope.modalBody = false;
        $scope.modalLoading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        if ($action == "run"){
            if ($window.confirm("Are You Sure you want to restart LOP Store Comms?")) {
                boolRun = true
            }else{
                boolRun = false
            }
        }else{
            boolRun = true
        }
        if (boolRun){
            var url_val = 'storecomms/socrates/' + $ip + "/" + $action;
            var storeCommsFixResponse = myService.getAJAXObject(url_val);
            storeCommsFixResponse.done(function(status){
                if ($action == "status"){
                    $scope.$apply(function(){
                    $scope.modalLoading = false;
                    $scope.modalBody = true;
                    $scope.storeCommsFixLog = $.parseJSON(status);
                    });
                }else{
                    $scope.$apply(function(){
                        $scope.repStatus = status;
                        $scope.showRepStatus = true;
                    });
                }
            });
            storeCommsFixResponse.fail(function(req, status, err){
                $scope.loading = false;
                if (status ==  "timeout"){
                    $scope.reqFailed = true;
                    $scope.errMsg = "Time out Error"
                }else if( status ==  "error"){
                    $scope.reqFailed = true;
                    $scope.errMsg = "Requested action cannot be completed";
                }
            });
    }}

// Handle getMountDetails Click

    $scope.getMountDetail = function($ip, $r2_r3){
        var isCollapsed = $("[href='#" + $ip  + "-mount-details']").attr("aria-expanded");
        if (isCollapsed == "false"){
            $scope.stopUpdate();
            $scope.mntshow = false;
            $scope.loading = true;
            $scope.reqFailed = false;
            var url_val = 'mount/socrates/'+ $r2_r3 + '/' + $ip;
            var mntDetailResponse = myService.getAJAXObject(url_val);
            mntDetailResponse.done(function(status){
                $scope.mountDetail = $.parseJSON(status);
                updateMountStatus($scope.mountDetail, $ip);
                $scope.$apply(function(){
                    $scope.mntshow = true;
                    $scope.loading = false;
                });
            });
            mntDetailResponse.fail(function(req, status, err){
                $scope.loading = false;
                if (status ==  "timeout"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Time out Error"
                }else if( status ==  "error"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Failed to get Mount details data";
                }
            });
        }
    }

    var updateMountStatus = function(mntDetails, ip){
        var sts = 'btn-success';
        if (mntDetails == '[]'){
            sts = 'btn-danger'
            $scope.reqFailed = true;
            $scope.errMsg = "Failed to get Mount details data";
        }else{
            $.each(mntDetails, function(index, mntDetail){
                var mnt_per = parseInt(mntDetail[4].split("%")[0],10)
                if(mnt_per >= 95){
                    sts = 'btn-danger';
                }else if (mnt_per > 89 && mnt_per < 95){
                    sts = ( sts != 'btn-danger') ? 'btn-warning' : sts;
                }else{
                    sts = ( sts != 'btn-danger' &&  sts != 'btn-warning' ) ? 'btn-success' : sts;
                }
            });
        }
        $("[href='#" + ip  + "-mount-details']").removeClass("btn-success btn-warning btn-danger").addClass(sts);
    }

    $scope.mntPercentStyle = function(mntVal){
        if(mntVal >= 95){
            return 'bg-danger';
        }else if (mntVal >89 && mntVal <95 ){
            return 'bg-warning';
        }else{
            return 'bg-success';
        }
    }

// Handle Get Replication Click

    $scope.getReplDetail = function($ip, $r2_r3){
        var isCollapsed = $("[href='#" + $ip  + "-replication-status']").attr("aria-expanded");
            if (isCollapsed == "false"){
            $scope.stopUpdate();
            beforeAJAXCall();
            $scope.showRepl = false;
            $scope.showRepStatus = false;
            var url_val = 'replication/socrates/get/'+ $ip + '/' + $r2_r3;
            var replDetailResponse = myService.getAJAXObject(url_val);
            replDetailResponse.done(function(status){
                $scope.repl = $.parseJSON(status);
                $scope.$apply(function(){
                    $scope.showRepl = true;
                    $scope.loading = false;
                });
                //updateReplStatus($scope.repl,$ip);
            });
            replDetailResponse.fail(function(req, status, err){
                $scope.loading = false;
                if (status ==  "timeout"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Time out Error"
                }else if( status ==  "error"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Requested Replication details not found";
                }
            });
        }
    }
/*
    var updateReplStatus = function(repl, store){

        var completedPattern = /Completed OK/i;
        var failedPattern = /Failed/i;

        var socCompletedMatched = repl["soc_log"].match(completedPattern);
        var platoCompletedMatched = repl["plato_log"].match(completedPattern);
        var socFailedMatched = repl["soc_log"].match(failedPattern);
        var platoFailedMatched = repl["plato_log"].match(failedPattern);

        if( socFailedMatched || platoFailedMatched ){
            $("[href='#" + store  + "-replication-status']").removeClass("btn-warning btn-success").addClass("btn-danger");
        }else if(socCompletedMatched && platoCompletedMatched){
            $("[href='#" + store  + "-replication-status']").removeClass("btn-warning btn-danger").addClass("btn-success");
        }else{
            $("[href='#" + store  + "-replication-status']").removeClass("btn-danger btn-success").addClass("btn-warning");
        }

    }
*/
// Handle Run Replication Request
    $scope.handleReplication = function($ip, $action){
        var boolRun = false;
        $scope.stopUpdate();
        //$scope.showRepl = false;
        $scope.modalBody = false;
        $scope.modalLoading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        if ($action == "run"){
            if ($window.confirm("Are You Sure you want to run force replication?")) {
                boolRun = true
            }else{
                boolRun = false
            }
        }else{
            boolRun = true
        }
        if (boolRun){
            var url_val = 'replication/socrates/' + $ip + "/" + $action;
            var replDetailResponse = myService.getAJAXObject(url_val);
            replDetailResponse.done(function(status){
                if ($action == "status"){
                    $scope.$apply(function(){
                    $scope.modalLoading = false;
                    $scope.modalBody = true;
                    $scope.repLogs = $.parseJSON(status);
                    });
                }else{
                    $scope.$apply(function(){
                        $scope.repStatus = status;
                        $scope.showRepStatus = true;
                    });
                }
            });
            replDetailResponse.fail(function(req, status, err){
                $scope.loading = false;
                if (status ==  "timeout"){
                    $scope.reqFailed = true;
                    $scope.errMsg = "Time out Error"
                }else if( status ==  "error"){
                    $scope.reqFailed = true;
                    $scope.errMsg = "Requested replication action cannot be completed";
                }
            });
    }}
// Handle Get EOD log request
    $scope.handleEodLog = function($ip){
        $scope.stopUpdate();
        //$scope.showRepl = false;
        $scope.modalBody = false;
        $scope.modalLoading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;

        var url_val = 'eod/socrates/' + $ip ;
        var eodLogResponse = myService.getAJAXObject(url_val);
        eodLogResponse.done(function(status){
            $scope.$apply(function(){
                $scope.modalLoading = false;
                $scope.modalBody = true;
                $scope.eodLogs = $.parseJSON(status);
            });

        });
        eodLogResponse.fail(function(req, status, err){
            $scope.loading = false;
            if (status ==  "timeout"){
                $scope.reqFailed = true;
                $scope.errMsg = "Time out Error"
            }else if( status ==  "error"){
                $scope.reqFailed = true;
                $scope.errMsg = "Requested EOD log request cannot be completed";
            }
        });
    }
// Handle getUtilsDetails Click

    $scope.getUtilsDetail = function($ip){
        var isCollapsed = $("[href='#" + $ip  + "-utils']").attr("aria-expanded");
        if(isCollapsed == "false"){
            $scope.stopUpdate();
            $scope.showUtils = false;
            $scope.loading = true;
            $scope.reqFailed = false;
            var url_val = 'utils/socrates/'+ $ip;
            var utilsResponse = myService.getAJAXObject(url_val);
            utilsResponse.done(function(status){
                $scope.utils = $.parseJSON(status);
                $scope.$apply(function(){
                    $scope.showUtils = true;
                    $scope.loading = false;
                });
            });
            utilsResponse.fail(function(req, status, err){
                $scope.loading = false;
                if (status ==  "timeout"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Time out Error"
                }else if( status ==  "error"){
                     $scope.reqFailed = true;
                     $scope.errMsg = "Requested Utils details data not found";
                }
            });
        }
    }
    // Handle getStoreFacts Click
    $scope.getStoreFacts = function($ip, $r2_r3){
        $scope.stopUpdate();
        var url_val = 'facts/socrates/'+ $ip + '/' + $r2_r3;
        var factsResponse = myService.getAJAXObject(url_val);
        factsResponse.done(function(status){
            var facts = $.parseJSON(status);
            updateStoreFacts($ip, facts);
        });
        factsResponse.fail(function(req, status, err){
            $scope.loading = false;
            if (status ==  "timeout"){
                 $scope.reqFailed = true;
                 $scope.errMsg = "Time out Error"
            }else if( status ==  "error"){
                 $scope.reqFailed = true;
                 $scope.errMsg = "Requested Utils details data not found";
            }

        });
    }
    var updateStoreFacts = function(store, facts){
        $.each(facts, function(fact, factValue){
            $("#" + store + "-facts ." + fact).html(factValue);
        });
    }
    // Handle Service start/stop Click
    $scope.startStopService = function($client, $service, r2_r3){
        var server_client = $client.split("-");
        var third_octet = server_client[0];
        var client = server_client[1];
        var selector = "#" + $client;
        var value = $(selector + " ." + $service + " .action").attr("data-original-title");
        console.log(value);
        if( value == "stop" ){
          //  $(selector + " ." + $service + " .action").attr("data-original-title","stopping").attr("ng-disabled","true");
            $(selector + " ." + $service + " .status").removeClass("btn-sucess").addClass("btn-danger progress-bar-striped");
            var service_url = "service/socrates/" + r2_r3 + "/" + third_octet + "/" + client + "/" + $service + "/stop";
        }else if(value == "start"){
            $(selector + " ." + $service + " .action").attr("data-original-title","starting").attr("ng-disabled","true");
            $(selector + " ." + $service + " .status").removeClass("btn-danger").addClass("btn-success progress-bar-striped");
            service_url = "service/socrates/" + r2_r3 + "/" + third_octet+ "/" + client + "/" + $service + "/start";
        }
        if(value == "start" || value == "stop"){
            myService.getResponse(service_url, function(status){
           //     console.log(status);
            });
        }
    }

    var getStoreServiceStatus = function($store_num){
        var isCollapsed = $("[href='#" + $store_num  + "']").attr("aria-expanded");
     //   console.log(PageVisible); 
        if(isCollapsed == "true" && PageVisible){
            polling_store_num = $store_num;
            var store_service_url = 'service/socrates/' + $store_num + '/status';
            myService.getResponse(store_service_url, function(status){
                updateTabServiceStatus($store_num,status);
            });
        }
    }
    // Update the Server/client server status at an interval
    var promise;
    $scope.updateStatus = function(){
        if ( angular.isDefined(promise) ) return;
            promise = $interval(function(){
                if (polling_store_num != "" ){
                    getStoreServiceStatus(polling_store_num);
                }
            },4000);
    };

    $scope.stopUpdate = function() {
      if (angular.isDefined(promise)) {
        $interval.cancel(promise);
        promise = undefined;
      }
    };

    $scope.$on('$destroy', function() {
      // Make sure that the interval is destroyed too
      $scope.stopUpdate();
    });

    var cancel = function(){
        $interval.cancel(promise);
    }

    // Functions related to Env Set Add
    $scope.inc_env_set = [{"cnt" : "env-1"}];

    $scope.addIncEnvSet = function(){
        var newEnvCount = $scope.inc_env_set.length+1;
        $scope.inc_env_set.push({ 'cnt': "env-" + newEnvCount });
    };

    $scope.removeIncEnvSet = function(index){
        if (index === -1){
            $scope.inc_env_set = [];
        }else{
            $scope.inc_env_set.splice(index, 1);
        }
    };

    // Perform Scope Apply to show the changes
    var applyScope = function(){
        $scope.$apply(function(){
            $scope.show = true;
            $scope.loading = false;
            $scope.initLoading = false;
        });
    }

    var handleSuccessResponse = function(resp){
        $scope.$apply(function(){
            $scope.loading = false;
            $scope.initLoading = false;
            $scope.reqFailed = false;
            $scope.reqSuccess = true;
            $scope.successMsg = resp["resp"]
        });
    };
    // Handle Failure response
    var handleFailureResponse = function(resp){
        resp.fail(function(req, status, err){
            $scope.$apply(function(){
                $scope.loading = false;
                $scope.initLoading = false;
                $scope.reqSuccess = false;
            });
            if (status ==  "timeout"){
                 $scope.$apply(function(){
                     $scope.reqFailed = true;
                     $scope.reqSuccess = false;
                     $scope.errMsg = "Time out Error"
                 });
            }else if( status ==  "error"){
                 $scope.$apply(function(){
                     $scope.reqFailed = true;
                     $scope.reqSuccess = false;
                     $scope.errMsg = err;
                 });
            }
        });
    };


    // To handle delivery DB api call
    $scope.getApiDetails = function(model){
        $scope.sortType = model + "_name";
        $scope.sortReverse = false;
        $scope.search = '';
        beforeAJAXCall(); 
        var url_val = '/api/get/' + model;
        var getApiDetailsResponse = myService.getAJAXObject(url_val);
        getApiDetailsResponse.done(function(status){
            $scope.apiResponse = $.parseJSON(status);
            applyScope();
        });
        handleFailureResponse(getApiDetailsResponse);
    };

    $scope.getSystem = function(){
        //console("getSystem")
        beforeAJAXCall();
        var url_val = '/api/get/system';
        var getSystemResponse = myService.getAJAXObject(url_val);
        getSystemResponse.done(function(status){
            $scope.systemResponse = $.parseJSON(status);
            $scope.systems = $scope.systemResponse["systems"]; 
            applyScope();
        });
        handleFailureResponse(getSystemResponse);
    };
 /* 
    $scope.getSystemElements = function(id, env_id){
        $scope.system_elements = [];
        $scope.deployments = [];
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        if(id != undefined && id != ''){
            var url_val = '/api/get_system_element_by_id/' + id ;
            var getSystemElementResponse = myService.getAJAXObject(url_val);
            getSystemElementResponse.done(function(status){
                var systemEleList = $.parseJSON(status);
                $scope.system_elements = systemEleList["system_elements"];
                var url_val = '/api/get_deploy_by_env/' + env_id ;
                var getDeployEnvResponse = myService.getAJAXObject(url_val);
                getDeployEnvResponse.done(function(status){
                    var DeployList = $.parseJSON(status);
                    $scope.deployments = DeployList["deployments"];
                    applyScope();
                });
                handleFailureResponse(getDeployEnvResponse);
                applyScope();
            });
            handleFailureResponse(getSystemElementResponse);
        }else{
            $scope.systems = [];
        };
    };
*/
    var getDeployedSystemElement = function (){
        $scope.deployed_sys_element = [];
        var sys_element_list = [],
            instance ;
        angular.forEach($scope.deployments, function(deploy){
            sys_elem = {};

            deploy_status = deploy["deployment_audit_history"][(deploy["deployment_audit_history"].length-1)]["deployment_status"]["status_description"];
           
            //&& deploy_status == "Completed"
            if(sys_element_list.indexOf(deploy["system_element"]["system_element_id"]) === -1 ){
                sys_element_list.push(deploy["system_element"]["system_element_id"]);
                sys_elem["system_element_id"] = deploy["system_element"]["system_element_id"];
                sys_elem["system_element_name"] = deploy["system_element"]["system_element_name"];
                sys_elem["system_element_type_name"] = deploy["system_element"]["system_element_type"]["system_element_type_name"];
                instances = [];
                angular.forEach(deploy["system_element"]["instances"], function(ins){
                    inst = {};
                    inst["instance_name"] = ins["instance_name"];
                    inst["instance_id"] = ins["instance_id"];
                    inst["assigned_ip"] = ins["assigned_ip"];
                    inst["status"] = deploy_status;
                    
                    var url_val = '/api/get_system_element_deploy_version/'+ ins["instance_id"] + "/" + sys_elem["system_element_id"];
                    var getSysEleVerResponse = myService.getAJAXObject(url_val, async=false);
                    getSysEleVerResponse.done(function(status){
                        var sysEleVerList = $.parseJSON(status);
                        inst["system_version"] = sysEleVerList["system_version_id"];

                    });
                    instances.push(inst);
                });
                sys_elem['instances'] = instances;
                $scope.deployed_sys_element.push(sys_elem);
                
            };
            //console.log($scope.deployed_sys_element);
        });
    }

 /* Map disabledflag */ 
    $scope.checkdisabledmap = function(system_version_id, system_element_id){
    var result, resultFound = false;
    if($scope.disabledflag) {
        for (var i = 0; i < $scope.disabledflag.length; i++) {
            if($scope.disabledflag[i].system_version_id == system_version_id &&
                $scope.disabledflag[i].system_element_id == system_element_id) {
                result = $scope.disabledflag[i].flagValue;
                resultFound = true;
                break;
            }
        }
    }

    if(!resultFound) {
    /*if(system_version_id != undefined && system_version_id != '' && system_element_id != undefined && system_element_id != ''){*/
        var url_val = '/api/get_sys_ele_comp_by_sysversion_syselem/' + system_version_id + '/' + system_element_id ;
        var checkdisabledmapResponse = myService.getAJAXObject(url_val);
        checkdisabledmapResponse.done(function(status){
            var resp = $.parseJSON(status);
           // console.log(resp["map_disable_flag"]);
            //$scope.disabledflag = resp["map_disable_flag"];
            var newFlagValue = {system_version_id: system_version_id,
                    system_element_id: system_element_id,
                    flagValue: resp["map_disable_flag"]
                };

            if ($scope.disabledflag == undefined) {
                $scope.disabledflag = [];
            }

            $scope.disabledflag.push(newFlagValue);
            result = resp["map_disable_flag"];
            applyScope();
            //return resp["map_disable_flag"];  
        });
        }
    // }
    return result;
}

    $scope.getDeployByEnv = function(id, env_id){
        $scope.deployments = [];
        $scope.deployed_sys_element = [];
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        if(id != undefined && id != ''){
            var url_val = '/api/get_deploy_by_env/' + env_id ;
            var getDeployEnvResponse = myService.getAJAXObject(url_val);
            getDeployEnvResponse.done(function(status){
                var DeployList = $.parseJSON(status);
                $scope.deployments = DeployList["environments"];
                getDeployedSystemElement();
                applyScope();
              //  console.log(DeployList);
            });
            handleFailureResponse(getDeployEnvResponse);
        }else{
            $scope.systems = [];
        };
    };

$scope.getRandomSpan = function(){
     return Math.floor((Math.random()*6) + 1);
};

var getSystemElement = function (){
  //  console.log($scope.systemVersionList);
 //   console.log($scope.systemElementList);
    angular.forEach($scope.systemVersionList, function(sys_version){
         //   console.log(sys_version);
            sys_elem = {};
            
            angular.forEach($scope.systemElementList, function(deploy){
                    //    console.log(deploy);
                    //    console.log(sys_version);
                        sys_elem['system_element_name'] = deploy['system_element_name'];
                        sys_elem['system_element_type_name'] = deploy['system_element_type']['system_element_type_name'];
                        sys_elem['system_version_name'] = sys_version['system_version_name'];
                        sys_elem['system_version_id'] = sys_version['system_version_id'];
                        sys_elem['system_element_id'] = deploy['system_element_id'];
                        //console.log(deploy['instances'].length);
                        // if (deploy['instances'].length > 0){ 
                        // sys_elem['instance_name'] = deploy['instances'][0]['instance_name'];
                        // sys_elem['assigned_ip'] = deploy['instances'][0]['assigned_ip'];
                        // sys_elem['instance_state'] = deploy['instances'][0]['instance_state']
                        // }
                        $scope.deployed_sys_element.push(sys_elem);
                        
            });
                           
    });
    //console.log(sys_version['system_version_name']);
   // console.log($scope.deployed_sys_element);
}

$scope.getSystemElementByEnvNew = function (id, env_id){
    //$scope.systemElementList = [];
    $scope.deployed_sys_element = [];
    $scope.loading = true;
    $scope.reqFailed = false;
    $scope.showRepStatus = false;
        if(id != undefined && id != ''){
            var url_val = '/api/get_system_element_by_env_id/' + id + '/' + env_id;
            var getDeployEnvResponse = myService.getAJAXObject(url_val);
            getDeployEnvResponse.done(function(status){
                var DeployList = $.parseJSON(status);
                $scope.deployed_sys_element = DeployList;
               // console.log(DeployList);
                applyScope();
            });
            handleFailureResponse(getDeployEnvResponse);
        }else{
            $scope.systems = [];
        };
};
 
$scope.getSystemElementByEnv = function(id, env_id){
        
        $scope.deployments = [];
        $scope.deployed_sys_element = [];
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
        if(id != undefined && id != ''){
            var url_val = '/api/get_sys_elem_by_env/' + env_id ;
            var getDeployEnvResponse = myService.getAJAXObject(url_val);
            getDeployEnvResponse.done(function(status){
                var DeployList = $.parseJSON(status);
                $scope.deployments = DeployList["environments"];
                
                //console.log(DeployList["environments"][0]);
                var url_val2 = '/api/get_system_element_by_id/' + DeployList["environments"][0]['system']['system_id'] ;

                var getSysResponse = myService.getAJAXObject(url_val2);
                getSysResponse.done(function(status){
                    var systemElementList = $.parseJSON(status);
                    
                    //console.log(systemElementList["system_elements"]);
                    
                    $scope.systemElementList = systemElementList["system_elements"];
                    
                    var url_val3 = '/api/get_system_version_by_id/' + DeployList["environments"][0]['system']['system_id'] ;
                    var getSysResponse1 = myService.getAJAXObject(url_val3);
                    getSysResponse1.done(function(status){
                        var systemVersionList = $.parseJSON(status);
                        $scope.systemVersionList = systemVersionList['system_versions'];
                        //console.log(systemVersionList);
                        getSystemElement();
                        applyScope();
                    });
                    //applyScope();
                    //console.log($scope.deployed_sys_element);
                });
                
            });
            handleFailureResponse(getDeployEnvResponse);
        }else{
            $scope.systems = [];
        };
    };


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
        //  console.log(key + '----' + value);
          $("#alert").removeClass("alert-danger").addClass("alert-success show in");
          $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + ' '+ '</span>');
        });
        $myForm[0].reset(); // reset form data
        delete $scope.instance;
        $('.filter-option').html('--Select--');
        $scope.system_element = []; //reset the system element form
        $scope.systems = [];
        $timeout(function() {
            angular.element('#rm-cmp').triggerHandler('click');
        }, 0);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        var obj = jQuery.parseJSON(jqXHR.responseJSON);
        $(".a-text").remove();
        $.each(obj, function(key,value) {
          $("#alert").removeClass("alert-success").addClass("alert-danger show in");
          $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + '</span>');
        });
    }




    $scope.getSystemElementComponentsById = function(sys_ver_id, sys_ele_id, env_id, instance_id){

        $scope.sys_element_components = [];
        if(instance_id == undefined){
            instance_id = 0;
        }
        var url_val = '/api/get_sys_ele_comp_by_sysverid_syseleid_env/'+ sys_ver_id + '/' + sys_ele_id + '/' + env_id + '/' + instance_id;
        var getSysEleCompResponse = myService.getAJAXObject(url_val, async=false);
        getSysEleCompResponse.done(function(status){
            var sysEleCompList = $.parseJSON(status);
            //$scope.sys_element_components = sysEleCompList["system_element_components"];
            components_list = [];
            angular.forEach(sysEleCompList, function(component){
                comp = {};
                comp['component_name'] = component['system_element_components']['component_version']['component']['component_name'];
                /* var deployment_component_length = Object.keys(component['system_element_components']['deployment_component']).length;*/
                
                if(component['system_element_components']['deployment_component'] == 'Completed'){
                    comp['component_version_name'] = component['system_element_components']['component_version']['component_version_name'];
                }
                else
                {
                    comp['component_version_name'] = '';
                }
               
                 comp['component_short_name'] = component['system_element_components']['component_version']['component']['component_short_name'];
                 comp['component_type_description'] = component['system_element_components']['component_version']['component']['component_type']['component_type_description'];
                 comp['artefact_store_url'] = component['system_element_components']['component_version']['artefact_store_url'];
                 comp['artefact_store_type_desc'] = component['system_element_components']['component_version']['artefact_store_type']['artefact_store_type_desc'];
                 comp['source_code_repository_url'] = component['system_element_components']['component_version']['source_code_repository_url'];
                 comp['source_tag_reference'] = component['system_element_components']['component_version']['source_tag_reference'];
                 comp['stable_flag'] = component['system_element_components']['component_version']['stable_flag'];
                 comp['creation_date'] = component['system_element_components']['component_version']['creation_date'];
                 comp['deployment_type_description'] = component['system_element_components']['component_version']['component']['deployment_type']['deployment_type_description'];
                 comp['linked_ci_flag'] = component['system_element_components']['component_version']['component']['linked_ci_flag'];
                  components_list.push(comp);
            })
            
            $scope.sys_element_components = components_list;

            $scope.sys_ele_in_ver =  uniqueValuesByKey($scope.sys_element_components, 'system_element_id');
            //applyScope();

            /*$timeout(function(){
               $scope.loading = false;
            },5000);*/
        });
        //handleFailureResponse(getSysEleCompResponse);

    };


    // To handle delivery DB api call to get instance list with multi select
    $scope.getInstanceList = function () {

        beforeAJAXCall();
        var url_val = '/api/get/instance_list';
        var getInstanceListResponse = myService.getAJAXObject(url_val);
        getInstanceListResponse.done(function (status) {
            $scope.instanceListApiResponse = $.parseJSON(status);
            applyScope();
        });
        handleFailureResponse(getInstanceListResponse);

        angular.element(document).ready(function () {

            setTimeout(function () {
                $('.selectpicker').selectpicker('refresh');
            }, 2000);
        });
    };
}
]);

