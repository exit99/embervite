dashboardApp.controller('eventCtrl', function($scope, $rootScope, $timeout) {
    $scope.event_pk = 0;
    $scope.initEvent = function (pk) {
        $timeout(function () {
            $scope.event_pk = pk;
        }, 0);
    }
    $scope.$watch('event_pk', function (new_val, old_val) {
        if (new_val != old_val){
            $rootScope.$broadcast('newEvent', $scope.event_pk)
        }
    });
});

dashboardApp.controller('headerCtrl', function($scope, $http) {
    $scope.$on('newEvent', function(e, data) {
        $http.post("/ev/event-data/", {
            pk: data
        }).success(function(data) {
            $scope.event_data = data
        });
    });
    $scope.checkInvitesSent = function () {
        if (($scope.event_data['invited'] + $scope.event_data['attending'] + $scope.event_data['not_attending']) > 0) {
            return "Invites Sent"
        } else {
            return "Invites will be sent on " + $scope.event_data['invite_date']
        }
    }
});
    
