myApp.controller('envSetSitController',function($scope, $interval, myService){
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


    if(document.hasFocus()){
        PageVisible = true;
    }
    else{
        PageVisible = false;
    } 

    var polling_store_num = '';
    var polling_domain = '';

    $scope.onLoading = function(){
        $scope.loading = true;
        $scope.show = false;
    }
    var interfaceUpStatus = function(selector){
        $(selector).removeClass("svg-red svg-yellow svg-grey").addClass("svg-green");
    }
    var interfaceDownStatus = function(selector){
        $(selector).removeClass("svg-green svg-yellow svg-grey").addClass("svg-red");
    }
    var interfaceNAStatus = function(selector){
        $(selector).removeClass("svg-green svg-red svg-grey").addClass("svg-yellow");
    }
    var updateStoppingStatus = function(selector){
        $(selector + " .action").text("stopping");
        $(selector + " .status").text("stopping").removeClass("bgred bggreen").addClass("bgyellow");
    }
    var updateStartingStatus = function(selector){
        $(selector + " .action").text("starting");
        $(selector + " .status").text("starting").removeClass("bgred bggreen").addClass("bgyellow");
    }
    var updateSvgStatus = function(selector, status){
        if(status == "running"){
            interfaceUpStatus(selector);
        }else if(status == "stopped"){
            interfaceDownStatus(selector);
            return false;
        }else{
            interfaceNAStatus(selector);
        }
    }
    var updateInterfaceStatus = function(data){
        $.each(data, function(client, services){
            var domain = client.split('-')
            $.each(services, function(service, status){
                switch (domain[0]) {
                    case "soc":
                        var plato25_ftp_status = data["plato-leg"]["ftp"];
                        var soc_ftp_status = status;
                        if(plato25_ftp_status == "running" && soc_ftp_status == "running"){
                            interfaceUpStatus("." + client + "2plato-leg" );
                        }else if (plato25_ftp_status == "stopped" && soc_ftp_status == "stopped"){
                            interfaceDownStatus("." + client + "2plato-leg" );
                        }else{
                            interfaceNAStatus("." + client + "2plato-leg" );
                        }
                        break;
                    case "aristotle":
                        updateSvgStatus(".aristotle2solar7-sok", status);
                        updateSvgStatus(".aristotle2solar7-fin", status);
                        updateSvgStatus(".aristotle2solar7-aus", status);
                        updateSvgStatus(".plato-leg2aristotle", status);
                        break;
                    case "plato":
                        if(domain[1] == 'aus') {
                            updateSvgStatus(".plato7-aus2solar7-aus", status);
                            updateSvgStatus(".soc-aus2plato7-aus", status);
                        }else if (domain[1] == 'fin'){
                            updateSvgStatus(".plato7-fin2solar7-fin", status);
                            updateSvgStatus(".soc-fin2plato7-fin", status);
                        }
                }
            });
        });
    }
//    var updateInterfaceStatus= function(domain, status){
//        if(domain == "aristotle"){
//            if(!$scope.$$phase) {
//                if(status == "running"){
//                    $("#aristotle2sok").removeClass("svg-red").addClass("svg-green");
//                }else {
//                    $("#aristotle2sok").removeClass("svg-green").addClass("svg-red");
//                }
//            }
//        }
//    }
    var checkAndUpdateStatus = function(data, fromInterface, toInterface){
        var fromInterfaceStatus = data[fromInterface];
        var toInterfaceStatus = data[toInterface];
        if(fromInterfaceStatus == "up" && toInterfaceStatus == "up"){
            interfaceUpStatus("." + fromInterface + "2" + toInterface);
        }else if(fromInterfaceStatus == "down" || toInterfaceStatus == "down"){
            interfaceDownStatus("." + fromInterface + "2" + toInterface);
        }else{
            interfaceNAStatus("." + fromInterface + "2" + toInterface);
        }
    }
    var updatePingInterface = function(data){
        checkAndUpdateStatus(data, 'on-premise-soa-a-admin', 'azure-soa-a-admin');
        checkAndUpdateStatus(data, 'on-premise-soa-a-admin', 'nordics-ebs');
        checkAndUpdateStatus(data, 'azure-soa-a-admin', 'jda-wms');
        checkAndUpdateStatus(data, 'azure-soa-d-admin', 'jda-wms');
        checkAndUpdateStatus(data, 'azure-mft-admin', 'jda-wms');
        checkAndUpdateStatus(data, 'aristotle', 'on-premise-soa-a');
    }
    var updateServiceStatus = function (domain, store, data){
        //console.log(data);
        var domain_part = domain.split("-")[0]
        var id;
        $.each(data, function(client, services){
            if (domain_part == "soc"){
                id = "#" + domain + "-" + client;
            }else if( domain == "aristotle"){
                id = "#aristotle"
            }else {
                id = "#" + domain
            }
            $.each(services, function(service, status){
                if ( status == "running" ){
                    $(id + " ." + service + " .status").text("running").removeClass("bgred bgyellow").addClass("bggreen");
                    $(id + " ." + service + " .action").text("stop");
                } else if ( status == "stopped" ){
                    $(id + " ." + service + " .status").text("stopped").removeClass("bggreen bgyellow").addClass("bgred");
                    $(id + " ." + service + " .action").text("start");
                }else if ( status == "starting" || status == "stopping"){
                    $(id + " ." + service + " .status").text(status).removeClass("bggreen bgred").addClass("bgyellow");
                    $(id + " ." + service + " .action").text(status);
                }else{
                    $(id + " ." + service + " .status").text("NA").removeClass("bggreen bgred").addClass("bgyellow");
                    $(id + " ." + service + " .action").text("NA");
                }
            });

        });

    }

// Handle get Store and client service status Click

    $scope.getServiceStatus = function(domain, $store){
        polling_store_num = $store;
        polling_domain = domain;
        var url_val = 'data/'+ domain + $store;
        $scope.updateStatus();
        var serviceStatusResponse = myService.getAJAXObject(url_val);
        serviceStatusResponse.done(function(status){
            var status_object = $.parseJSON(status);
            updateServiceStatus(domain, $store,status_object);
        });
        serviceStatusResponse.fail(function(req, status, err){
            if (status ==  "timeout"){
                 //$scope.reqFailed = true;
                 //$scope.errMsg = "Time out Error"
            }else if( status ==  "error"){
                 //$scope.reqFailed = true;
                // $scope.errMsg = "Requested Service Data not found"
            }
        });
    }

    // Handle Service start/stop Click
    $scope.startStopService = function($client, $service, region){
        var service_url;
        var server_client = $client.split("-");
        var client = server_client[2];
        var selector = "#" + $client;

        var value = $(selector + " ." + $service + " .action").text();

        if( value == "stop" ){
            updateStoppingStatus(selector + " ." + $service);
            service_url = "service/socrates/" + region + "/" + $service + "/stop/" + client

        }else if(value == "start"){
            updateStartingStatus(selector + " ." + $service);
            service_url = "service/socrates/" + region + "/" + $service + "/start/" + client
        }
        if(value == "start" || value == "stop"){
            myService.getResponse(service_url, function(status){
               // console.log(status);
            });
        }
    }

    // Plato Service start/Stop Click Handler
    $scope.handlePlatoClick = function(plato_region, service){
        var selector = "#" + plato_region
        var url_val;
        var value = $(selector + " ." + service + " .action").text();
        if( value == "stop" ){
            updateStoppingStatus(selector + " ." + service );
            url_val = "service/plato/" + plato_region + "/" + service + "/stop";
        }else if(value == "start"){
            updateStartingStatus(selector + " ." + service);
            url_val = "service/plato/" + plato_region + "/" + service + "/start";
        }
        if(value == "start" || value == "stop"){
            myService.getResponse(url_val, function(status){
               // console.log(status);
            });
        }
    }

    // Aristotle click handler
    $scope.handleAristoClick = function(domain, service){
        var selector = "#" + domain
        var url_val;
        var value = $(selector + " ." + service + " .action").text();
        if( value == "stop" ){
            updateStoppingStatus(selector + " ." + service);
            url_val = "service/aristotle/" + service + "/stop/49";
        }else if(value == "start"){
            updateStartingStatus(selector + " ." + service);
            url_val = "service/aristotle/" + service + "/start/49";
        }
        if(value == "start" || value == "stop"){
            myService.getResponse(url_val, function(status){
               // console.log(status);
            });
        }
    }

    // Solar7 Service start/Stop Click Handler
    $scope.handleSolar7Click = function(solar7_region, service){
        var selector = "#" + solar7_region
        var url_val;
        var value = $(selector + " ." + service + " .action").text();
        if( value == "stop" ){
            updateStoppingStatus(selector + " ." + service);
            url_val = "service/solar7/" + solar7_region + "/" + service + "/stop";
        }else if(value == "start"){
            updateStartingStatus(selector + " ." + service);
            url_val = "service/solar7/" + solar7_region + "/" + service + "/start";
        }
        if(value == "start" || value == "stop"){
            myService.getResponse(url_val, function(status){
               // console.log(status);
            });
        }
    }


    var getStoreServiceStatus = function(domain, $store_num){
        if(PageVisible){
            polling_store_num = $store_num;
            polling_domain = domain;
            var store_service_url = 'data/'+ domain + $store_num ;
            myService.getResponse(store_service_url, function(status){
                updateServiceStatus(domain,$store_num,status);
            });
        }
    }

    // Update the Server/client server status at an interval
    var promise;
    $scope.updateStatus = function(){
        if ( angular.isDefined(promise) ) return;
        promise = $interval(function(){
            if (polling_store_num != "" ){
                getStoreServiceStatus(polling_domain,polling_store_num);
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
    // start the get service status process for the currently watching store
//    var promise = $interval(function(){
//        if (polling_store_num != "" ){
//        var url_val = '/service/socrates/' + polling_store_num + '/status';
//        var serviceStatusResponse = myService.getAJAXObject(url_val);
//        serviceStatusResponse.done(function(status){
//            console.log(status);
//        });
//        }
//    },120000);

// update ping and interface status
    var pingInterface = $interval(function(){
      //  console.log(PageVisible);
        if(PageVisible){
            var store_service_url = 'status/interface';
            var url_val = 'static/data/ping';
            var pingStatusResponse = myService.getAJAXObject(url_val);
            var serviceStatusResponse = myService.getAJAXObject(store_service_url);
            serviceStatusResponse.done(function(status){
                var status_object = $.parseJSON(status);
                updateInterfaceStatus(status_object);
                $scope.$apply(function(){
                    $scope.loading = false;
                    $scope.show = true;
                });
            });
            pingStatusResponse.done(function(data){
                var status = $.parseJSON(data);
                updatePingStatus(status);
                //console.log(status);
            });
        }
    },5000);

function updatePingStatus(data){
    $.each(data, function(client, status){
        if (status == "up"){
            $("#" + client ).removeClass("bgred").addClass("bggreen");
            if(client.split("-")[2] == 'store'){
                $("." + client ).removeClass("bgred").addClass("bggreen");
            }
        } else if (status == "down"){
            $("#" + client ).removeClass("bggreen").addClass("bgred");
            if(client.split("-")[2] == 'store'){
                $("." + client ).removeClass("bggreen").addClass("bgred");
            }
        }

    });
    updatePingInterface(data);
 }

//// update interface-details
//    var promise = $interval(function(){
//        store_service_url = '../static/data/aristotle49.json';
//        myService.getResponse(store_service_url, function(status){
//            updateServiceStatus('aristotle',$store_num,status);
//        });
//        }
//    },120000);

//    var promise = $interval(function(){
//            update_mountdetail(polling_store_num);
//    },600000);

    var cancel = function(){
        $interval.cancel(promise);
    }
//	myService.getResponse('/getstore/list', function(stores){
//        $.each(stores, function(key, store){
//            getStoreServiceStatus(store);
//        });
//	});

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
    // To handle delivery DB api call
    $scope.getApiDetails = function(model){
        //beforeAJAXCall();
        var url_val = '/api/get/' + model;
        var getApiDetailsResponse = myService.getAJAXObject(url_val);
        getApiDetailsResponse.done(function(status){
            $scope.apiResponse = $.parseJSON(status);
            $scope.$apply(function(){
                $scope.show = true;
                $scope.loading = false;
                $scope.initLoading = false;
            });
        });
        getApiDetailsResponse.fail(function(req, status, err){
            $scope.$apply(function(){
              $scope.loading = false;
              $scope.initLoading = false;
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

    $scope.getSystem = function(){

        //beforeAJAXCall();
        var url_val = '/api/get/system';
        var getSystemResponse = myService.getAJAXObject(url_val);
        getSystemResponse.done(function(status){
            $scope.systemResponse = $.parseJSON(status);
            $scope.systems = $scope.systemResponse["systems"];
           // console.log($scope.systems);
            $scope.$apply(function(){
                $scope.show = true;
                $scope.loading = false;
                $scope.initLoading = false;
            });
        });
        getSystemResponse.fail(function(req, status, err){
            $scope.$apply(function(){
              $scope.loading = false;
              $scope.initLoading = false;
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


    var links = $('a[role="button"]');
    links.on('show.bs.tab', function(e){
        $('a[aria-expanded="true"]').addClass("active");
        $('a[aria-expanded="false"]').removeClass("active");
    });
    var $myForm = $('.my-form')
    $myForm.click(function(event){
        $(".alert").removeClass("alert-success alert-danger show in");
    });
    $myForm.submit(function(event){
        $(".alert").removeClass("alert-success alert-danger show in");
        event.preventDefault()
        var $formData = $(this).serialize()
        var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
        $.ajax({ method: "POST", url: $thisURL, data: $formData, success: handleFormSuccess, error: handleFormError, })
    });

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
    };

    function handleFormError(jqXHR, textStatus, errorThrown){
        var obj = jQuery.parseJSON(jqXHR.responseJSON);
        $(".a-text").remove();
        $.each(obj, function(key,value) {
          $("#alert").removeClass("alert-success").addClass("alert-danger show in");
          $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + '</span>');
        });
    };
});

