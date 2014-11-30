eventApp.directive('dayPicker', function () {                                       
    return {                                                                    
        restrict: 'E',                                                          
        templateUrl: "day_picker.html",                                             
        scope: {                                                                
            'occurrance': '='                                                       
        },                                                                      
        controller: function ($scope) {                      
            $scope.dayClick = function (day_num) {
                $scope.day = day_num; 
            };
        }                                                                       
    }                                                                           
});
