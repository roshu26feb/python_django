myApp.controller('UserController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',
        function ($scope, $rootScope, $location, AuthenticationService) {


            $scope.checkUser = function () {
                var userDetails = AuthenticationService.getCredentials();
                if (userDetails) {
                    var userDetails = AuthenticationService.parseJwt(userDetails);
                    $scope.userIsLogin = true;
                    $scope.userName = userDetails['identity']['userName'];
                    $scope.userDisplayName = userDetails['identity']['userDisplayName'];
                    var current_time = new Date().getTime() / 1000;
	                if (current_time > userDetails.exp) { 
                        $(location).attr('href', '/login');/* expired */ }
                }
                else {
                    $(location).attr('href', '/login');
                }
            }




        }]);