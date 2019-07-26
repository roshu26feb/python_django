myApp.controller("esmtAdminCtrl", function ($scope, $http, $timeout, myService) {
   
   // initialize and get all component type list on load 
    $scope.init = function () {
        $scope.getLinkedItemsChoice('component_type_id');
        //'component_id'
    };

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
    }
    // Show loading
    $scope.onLoading = function () {
        $scope.initLoading = true;
        $scope.show = false;
    }

    // Handle Failure response
    var handleFailureResponse = function (resp) {
        resp.fail(function (req, status, err) {
            $scope.$apply(function () {
                $scope.initLoading = false;
            });
            if (status == "timeout") {
                $scope.$apply(function () {
                    $scope.reqFailed = true;
                    $scope.errMsg = "Time out Error"
                });
            } else if (status == "error") {
                $scope.$apply(function () {
                    $scope.reqFailed = true;
                    $scope.errMsg = err;
                });
            }
        });
    };
    // Initialize values
    var initializeApiCall = function (initialSortType) {
        $scope.sortType = initialSortType;
        if (initialSortType == "active") {
            $scope.sortReverse = true;
        } else {
            $scope.sortReverse = false;
        };
        $scope.search = '';
        $scope.loading = true;
        $scope.reqFailed = false;
        $scope.showRepStatus = false;
    };

    $scope.getSystemById = function (id) {
        if (id != undefined) {
            $scope.sortType1 = "creation_date";
            $scope.sortReverse1 = false;
            $scope.search = '';
            $scope.loading = true;
            $scope.reqFailed = false;
            $scope.showRepStatus = false;
            var url_val = '/api/get_system_by_id/' + id + '/';
            var getSystemsResponse = myService.getAJAXObject(url_val);
            getSystemsResponse.done(function (status) {
                var syslist = $.parseJSON(status);
                $scope.systems = syslist["systems"][0];
                applyScope();
            });
            handleFailureResponse(getSystemsResponse);
        } else {
            $scope.systems = [];
        };
    };

    $scope.getUserById = function (id) {
        if (id != undefined && id != '') {
            var url_val = '/api/get_user_by_id/' + id + '/';
            var getUserResponse = myService.getAJAXObject(url_val);
            getUserResponse.done(function (status) {
                var userResp = $.parseJSON(status);
                $scope.users = userResp["users"][0];
                //Uncheck all the check boxed
                $("input").prop("checked", false);
                userRoles = [];
                $.each($scope.users["user_roles"], function (key, value) {
                    userRoles.push(value.role.role_id);
                });
                // check only the roles pertaining to the user
                $("input[value=" + userRoles.join('], [value=') + "]").prop("checked", true);
                applyScope();
            });
            handleFailureResponse(getUserResponse);
        } else {
            $scope.users = [];
        };
    };

    // Handle Get Get Linked Item Api Call
    $scope.getLinkedItemsChoice = function (link) {
        var url_val = '/api/get_linked_item/' + link;
        var getLinkedItemsResponse = myService.getAJAXObject(url_val);
        getLinkedItemsResponse.done(function (status) {
            $scope.linkedItems = $.parseJSON(status);
            applyScope();
        });
        handleFailureResponse(getLinkedItemsResponse);
    };

    // Handle Get Get Linked items for component by component type ID Api Call
    $scope.getLinkedItemsComponentType = function (link) {
      // console.log(link['key']);
        var url_val = '/api/get_comp_by_comptype_id/' + link['key'];
        var getLinkedItemsResponse = myService.getAJAXObject(url_val);
        getLinkedItemsResponse.done(function (status) {
           
           $scope.CompItems = $.parseJSON(status);
            applyScope();
        });
        handleFailureResponse(getLinkedItemsResponse);
    };

    $scope.getApiDetails = function (model) {
        if (model) {
            if (model == "parameter") {
                initializeApiCall("active");
            } else {
                initializeApiCall(model + "_name");
            };
            var url_val = '/api/get/' + model;
            var getApiDetailsResponse = myService.getAJAXObject(url_val);
            getApiDetailsResponse.done(function (status) {
                $scope.apiResponse = $.parseJSON(status);
                applyScope();
            });
            handleFailureResponse(getApiDetailsResponse);
        } else {
            $scope.apiResponse = undefined;
        };
    };
    $scope.updateLink = function (linkedElement) {
        angular.forEach(linkedElement, function (value, key) {
            if (key == 'component_type') {
                linkedElement["link_name"] = key;
                linkedElement["link_value"] = value.component_type_description;
            } else if (key == 'component') {
                linkedElement["link_name"] = key;
                linkedElement["link_value"] = value.component_name;
            } else if (key == 'component_vesion') {
                linkedElement["link_name"] = key;
                linkedElement["link_value"] = value.component_version_name;
            };
            //console.log(linkedElement);
        });
    };
    getLink = function (params) {
        for (li in params["linked_element"]) {
            return li;
        };
    };
    populateParam = function (params) {
        //console.log(params);
        var link = getLink(params);
        //$scope.getLinkedItemsChoice(link + "_id");
        $scope.p = {
            "paramDispName": params["parameter_name"],
            "paramInternalName": params["parameter_internal_name"],
            "mandatory": params["mandatory"].toString().toLowerCase(),
            "active": params["active"].toString().toLowerCase(),
            "paramType": params["parameter_type"]["parameter_type_id"].toString(),
            "link": {
                "key": link + "_id",
                "value": link.charAt(0).toUpperCase() + link.slice(1)
            },
        }

        if (params["linked_element"]["component"] != undefined) {
            $scope.p["linked_item"] = {
                "key": params["linked_element"][link][link + "_id"],
            }

        }
        
        /*  "linked_item": {
               // "key": params["linked_element"][link][link + "_id"]
               "key": ''
            }
            */

        paramTypeSelect(params["parameter_type"]["parameter_type"], params["parameter_values"])
        //console.log($scope.p)
    };
    // Handle Get parameter By ID API call
    $scope.getParameterById = function (id) {
        //console.log("Parameter ID" + id);
        if (id != undefined) {
            $scope.loading = true;
            $scope.reqFailed = false;
            $scope.showRepStatus = false;
            var url_val = '/api/get_parameter/' + id + '/';
            var getParameterByIdResponse = myService.getAJAXObject(url_val);
            getParameterByIdResponse.done(function (status) {
                var paramList = $.parseJSON(status);
                $scope.parameters = paramList["parameters"][0];
                if (paramList["parameters"][0]['linked_element']['component'] != undefined) {
                    $scope.component_type_id = { value: paramList["parameters"][0]['linked_element']['component']['component_type']['component_type_description'], key: paramList["parameters"][0]['linked_element']['component']['component_type']['component_type_id'] };
                } else {
                    $scope.component_type_id = { value: paramList["parameters"][0]['linked_element']['component_type']['component_type_description'], key: paramList["parameters"][0]['linked_element']['component_type']['component_type_id'] };
                }

                $scope.getLinkedItemsComponentType($scope.component_type_id);
               // console.log( $scope.component_type_id );
                populateParam($scope.parameters);
                applyScope();
            });
            handleFailureResponse(getParameterByIdResponse);
        } else {
            $scope.parameters = [];
        };
    };

    paramTypeSelect = function (paramType, paramValue = []) {
        //console.log(paramType);
        //console.log(paramValue);
        if (paramType.toUpperCase().indexOf("LIST") != -1) {
            $scope.paramValues = []
            if (paramValue.length != 0) {
                angular.forEach(paramValue, function (values) {
                    $scope.paramValues.push({
                        'value': values["parameter_value"]
                    });
                });
            } else {
                $scope.paramValues.push({
                    'name': 'name-1'
                });
            };
            $scope.freeText = false;
            $scope.number = false;
        } else if (paramType.toUpperCase().indexOf("FREE") != -1) {
            $scope.paramValues = undefined;
            if (paramValue.length != 0) {
                angular.forEach(paramValue, function (values) {
                    //.match(/\(([^)]+)\)/)[1])
                    $scope.textSize = parseInt(values["parameter_value"]);
                });
            };
            $scope.freeText = true;
            $scope.number = false;
        } else if (paramType.toUpperCase().indexOf("NUMBER") != -1) {
            $scope.paramValues = undefined;
            $scope.freeText = false;
            if (paramValue.length != 0) {
                angular.forEach(paramValue, function (values) {
                    limit = values["parameter_value"].match(/\(([^)]+)\)/)[1];
                    $scope.numMin = parseInt(limit.split(',')[0]);
                    $scope.numMax = parseInt(limit.split(',')[1]);
                });
            };
            $scope.number = true;
        } else {
            $scope.paramValues = [];
            $scope.freeText = false;
            $scope.number = false;
        };
    };

    $scope.addParameterValues = function (paramType) {
        paramType = $("#id_parameter_type option:selected").text();
        //console.log($scope.p);
        $scope.paramTypeName = paramType
        //console.log("Text: " + $scope.paramTypeName);
        paramTypeSelect(paramType);
    };
    $scope.removeParamValue = function (index) {
        if (index === -1) {
            $scope.paramValues = [];
        } else {
            $scope.paramValues.splice(index, 1);
        }
    };
    $scope.addNewParamValue = function (Index) {
        var newValueNo = $scope.paramValues.length;
        $scope.paramValues.push({
            'name': 'value-' + newValueNo
        });
    };
    //call Instance Update
    $scope.callUpdate = function (parameter_id) {
        if (parameter_id != undefined && parameter_id != '') {
            $(location).attr('href', '/esmt_admin/parameter_update/' + parameter_id)
        }
    };

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
        var obj = jQuery.parseJSON(jqXHR.responseJSON);
        $(".a-text").remove();
        $.each(obj, function (key, value) {
            $("#alert").removeClass("alert-danger").addClass("alert-success show in");
            $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + ' ' + '</span>');
        });
        $myForm[0].reset(); // reset form data
        $('.filter-option').html('--Select--');
        $scope.system_element = []; //reset the system element form
        $scope.systems = [];
        $timeout(function () {
            angular.element('#rm-cmp').triggerHandler('click');
        }, 0);
    }

    function handleFormError(jqXHR, textStatus, errorThrown) {
        var obj = jQuery.parseJSON(jqXHR.responseJSON);
        //var obj = jqXHR.responseJSON;
        $(".a-text").remove();
        $.each(obj, function (key, value) {
            $("#alert").removeClass("alert-success").addClass("alert-danger show in");
            $(".alert-text").append('<span class="a-text"><strong>' + key + '</strong>' + ':' + value + '</span>');
        });
    }
    $scope.refDataTableHead = function (ref) {
        switch (ref) {
            case "component_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Component Type Description'
                }];
                break;
            case "parameter_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Parameter Type'
                }];
                break;
            case "host_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Host Name'
                }];
                break;
            case "infrastructure_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Infrastructure Type Name'
                }];
                break;
            case "disk_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Disk Type Description'
                }, {
                    'head': 'Min Size'
                }, {
                    'head': 'Max Size'
                }];
                break;
            case "method_creation_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Name'
                }, {
                    'head': 'Description'
                }];
                break;
            case "deployment_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Deployment Type Description'
                }];
                break;
            case "artefact_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Artefact Store Type Description'
                }];
                break;
            case "environment_subscription_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Environment Subscription Type Name'
                }];
                break;
            case "environment_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Environment Subscription Type Name'
                }, {
                    'head': 'Environment Type Name'
                }, {
                    'head': 'Environment Type Short Name'
                }, {
                    'head': 'Identifier'
                }];
                break;
            case "environment_data_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Environment Data Type Name'
                }];
                break;
            case "status":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Status Type'
                }, {
                    'head': 'Status Description'
                }];
                break;
            case "environment_use":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Environment Use Name'
                }, {
                    'head': 'Environment Use Short Name'
                }];
                break;
            case "system_network_set":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Network Set Name'
                }, {
                    'head': 'Network Set Short Name'
                }];
                break;
            case "system_element_type":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'System Element Type Name'
                }, {
                    'head': 'System Element Type Short Name'
                }];
                break;
            case "host_region":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Host Region Name'
                }, {
                    'head': 'Host Region Description'
                }];
                break;
            case "host_site":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Host Site Name'
                }, {
                    'head': 'Host Site Description'
                }];
                break;
            case "host_subscription":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Host Subscription Key'
                }, {
                    'head': 'Host Subscription Description'
                }];
                break;
            case "network_set":
                $scope.refDataHead = [{
                    'head': 'ID'
                }, {
                    'head': 'Network Set Name'
                }, {
                    'head': 'Subnet'
                }, {
                    'head': 'IP Range Start'
                }, {
                    'head': 'IP Range End'
                }];
                break;
            default:
                //console.log("Default");
        };
        //console.log($scope.refDataHead);
    };
    $scope.links = [{
            "key": "component_type_id",
            "value": "Component Type"
        },
        {
            "key": "component_id",
            "value": "Component"
        },
        {
            "key": "component_version_id",
            "value": "Component Version"
        }
    ];



    // ESMT-922 Handle Get Get Linked items for fully automated component by component type ID  Api Call
    $scope.getLinkedItemsComponentTypeFA = function (link) {
     //   console.log(link['key']);
        var url_val = '/api/get_comp_by_comptype_id_FA/' + link['key'];
        var getLinkedItemsResponse = myService.getAJAXObject(url_val);
        getLinkedItemsResponse.done(function (status) {
           
           $scope.CompItems = $.parseJSON(status);
            applyScope();
        });
        handleFailureResponse(getLinkedItemsResponse);
    };

});