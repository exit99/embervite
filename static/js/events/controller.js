    eventApp.controller('eventCtrl', function($scope) {
        $scope.occurance = OCCURANCE;
    });
    
    eventApp.controller('addMemberCtrl', function($scope) {
        $scope.invited = 0;
        $scope.selected_members = {};
        $scope.updateSelected = function (id) {
            $scope.selected_members[id] = !$scope.selected_members[id]
        }; 
    });
