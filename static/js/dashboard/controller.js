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
            $scope.event_data = data;
        });
    });
    $scope.checkInvitesSent = function () {
        return checkSent($scope.event_data) ? "Invites Sent" : "Invites will be sent on " + $scope.event_data['invite_date']
});

dashboardApp.controller('guestListCtrl', function($scope, $http, $timeout) {
    $scope.$on('newEvent', function(e, data) {
        var pk = data[0],
            event_data = data[1]
        $http.post("/ev/event-member-data/", {
            pk: pk
        }).success(function(data) {
            $scope.event_members = data;
            $scope.event_data = event_data;
        });
    });
    $scope.checkStatus = function (pk, state) {
        if ($scope.event_members) {
            if (Object.keys($scope.event_members).indexOf(pk.toString()) != -1) {
                console.log(state);
                console.log($scope.event_members);
                return $scope.event_members[pk] == state;
            }
            return false
        }
    }
});

function checkSent(data) {
    return (data['invited'] + data['attending'] + data['not_attending']) > 0
}
    
