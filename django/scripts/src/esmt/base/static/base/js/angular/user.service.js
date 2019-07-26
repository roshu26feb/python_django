
myApp.service('AuthenticationService',
    function ($http, $cookies, $rootScope, $timeout) {
        var service = {};


        service.getCredentials = function () {
            // console.log($cookies.get('access_token'));
            return $cookies.get('access_token');

        };


        service.checkPermissions = function (page) {
            var userCredentials = this.getCredentials();
           
            var permissionArray = [];
            if(userCredentials){ 
            // var cleanUserDetails = userCredentials.replace(/'/g, '"'); 
                var decodeJWT = this.parseJwt(userCredentials);
                // console.log(decodeJWT);
                // userDetails = JSON.parse(cleanUserDetails);
                 const permissions = decodeJWT['identity']['userPermission'];
                 angular.forEach(permissions, function (permission) {
                     if(permission.buisnessProcess === page){
                         permissionArray.push(permission)
                     }
                 });
             }
            
             return permissionArray ;
         };

         service.parseJwt = function(token) { 
             var base64Url = token.split('.')[1]; 
             var base64 = base64Url.replace('-', '+').replace('_', '/'); 
             return JSON.parse(window.atob(base64));
         };

        return service;
    });
