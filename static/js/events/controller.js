    eventApp.controller('eventCtrl', function($scope) {
        $scope.occurance = OCCURANCE;
    });
    
    eventApp.controller('addMemberCtrl', function($scope) {
        $scope.invited = 0;
        $scope.selected_members = {};
        $scope.updateSelected = function (id) {
            $scope.selected_members[id] = !$scope.selected_members[id];
            var count = 0;
            for (key in $scope.selected_members) {
                if ($scope.selected_members[key]) count++;
            }
            $scope.invited = count;
        }; 
    });
