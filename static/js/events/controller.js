    eventApp.controller('eventCtrl', function($scope) {
        $scope.occurance = OCCURANCE;
    });
    
    eventApp.controller('addMemberCtrl', function($scope, $timeout) {
        $scope.selected_members = {};
        $scope.invited = 0;
        $scope.updateSelected = function (id) {
            updateCount();
        }; 

        $scope.initMember = function (pk) {
            $scope.selected_members[pk] = (EVENT_MEMBERS.indexOf(pk) != -1) ? true : false;
            updateCount();
        };
        
        function updateCount () {
           var count = 0;
            for (key in $scope.selected_members) {
                if ($scope.selected_members[key]) count++;
            }
            $scope.invited = count;
        }
});
