var myApp = angular.module('myApp',['ngCookies']);

myApp.service('APIInterceptor', function() {
  var service = this;
  service.request = function(config) {
    return config;
  };
  service.responseError = function(response) {
    return response;
  };
});
   

myApp.config(function($interpolateProvider){
		$interpolateProvider.startSymbol('(~');
		$interpolateProvider.endSymbol('~)');
});

myApp.config(['$httpProvider', function($httpProvider ) {
    //initialize get if not there
    if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};
    }
    //disable IE ajax request caching
    $httpProvider.defaults.headers.get['If-Modified-Since'] = 'Mon, 26 Jul 1997 05:00:00 GMT';
    // extra
    $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
    $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'; 
    //$httpProvider.interceptors.push('myHttpResponseInterceptor'); 
    $httpProvider.interceptors.push('APIInterceptor');

   /* $httpProvider.interceptors.push(['$q', '$location',  function ($q, $location) {
    return {
        'request': function (config) {
          console.log('reqest intercepter');

            config.headers = config.headers || {};
          //  if ($localStorage.token) {
            //    config.headers.Authorization = 'Bearer ' + $localStorage.token;
            } //
            return config;
        },
        'responseError': function (response) {
          console.log('responce intercepter');
          if (response.status === 401 || response.status === 403) {
                $location.path('/login');
            }
            return $q.reject(response);
        }
    };
 }]); */
}]);

 /*myApp.factory('myHttpResponseInterceptor',['$q','$location',function($q,$location){
  return {
    response: function(response){
      console.log('test');
      return promise.then(
        function success(response) {
        return response;
      },
      function error(response) {
        if(response.status === 401){
          console.log('test1');
          $location.path('/signin');
          return $q.reject(response);
        }
        else{
          return $q.reject(response); 
        }
      });
    },
    request: function(response){
      console.log('test');
      return promise.then(
        function success(response) {
        return response;
      },
      function error(response) {
        if(response.status === 401){
          console.log('test1');
          $location.path('/signin');
          return $q.reject(response);
        }
        else{
          return $q.reject(response); 
        }
      });
    },
  }
}]);
*/
// Custom service to perform AJAX request
myApp.factory('myService',function($http){
    return {
        getAJAXObject: function($url_val, async=true){
            return $.ajax({cache: false, url: $url_val, dataType: "text" , async: async});
            },
        getResponse: function($url, successCallBack){
            $http({method: 'GET', url: $url }).
            then(
                function(response){
                    successCallBack(response.data);
                }
            );
        }
    }
});

myApp.run(function($rootScope) {
    //Call Deployment Request
    $rootScope.requestDeployment = function(sys_element_id, system_version){
      if(sys_element_id != undefined && sys_element_id != '' && system_version != undefined && system_version != ''){
          $(location).attr('href','/deployment/deployment_request/' + sys_element_id + "/" + system_version) 
      }
    };

    $rootScope.requestMapInstance = function(env_id, sys_id, sys_element_id ){
      //alert("dbhdbvshj");
      if(env_id != undefined && env_id != '' && sys_id != undefined && sys_id != '' &&sys_element_id != undefined && sys_element_id != '' ){
          $(location).attr('href','/env/map_instance/' + env_id + "/" + sys_id + "/" + sys_element_id);
      }
      
    };

  });

// Custom filters
myApp.filter('num', function() {
    return function(input) {
      return parseInt(input, 10);
    };
});
myApp.filter('percentSplit', function() {
    return function(input) {
      var numval = input.split("%")
      return numval[0];
    };
});
myApp.filter("rawHtml", ['$sce', function($sce) {
  return function(htmlCode){
    return $sce.trustAsHtml(htmlCode);
  }
}]);
myApp.filter('formatDate', function() {
    return function (object) {
        var array = [];
        angular.forEach(object, function (sv) {
            var date = new Date(sv.creation_date)
            sv.creation_date = date.getTime();  
            array.push(sv);
        });
        return array;
    };
});
myApp.filter('splitDate', function($filter) {
  return function(input){
    var date = new Date(input)
    var date_time = date.getTime();
    return $filter('date')(date_time, 'yyyy-dd-MM')
  }
});

myApp.filter('splitTime', function($filter) {
  return function(input){
    var date = new Date(input)
    var date_time = date.getTime();
    return $filter('date')(date_time, 'HH:mm:ss')

  }
});
myApp.filter('titleCase', function() {
    return function(input) {
      input = input.replace(/_/g, ' ')+ 's:' || '';
      return input.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    };
});
var uniqueValuesByKey = function(collection, keyname) {
          var output = [],
              keys = [];

          angular.forEach(collection, function(item) {
              var key = item[keyname];
              if(keys.indexOf(key) === -1) {
                  keys.push(key);
                  //output.push(item);
                  output.push(key);
              }
          });
    return output;
};


   


  