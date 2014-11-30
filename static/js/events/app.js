    var eventApp = angular.module('eventApp', []);
    
        function serializeData( data ) {
            if ( ! angular.isObject( data ) ) {
                return( ( data == null ) ? "" : data.toString() );
            }
     
            var buffer = [];
            for ( var name in data ) {
                if ( ! data.hasOwnProperty( name ) ) {
                    continue;
                }
     
                var value = data[ name ];
                buffer.push(
                    encodeURIComponent( name ) +
                    "=" +
                    encodeURIComponent( ( value == null ) ? "" : value )
                );
            }
     
            var source = buffer
                .join( "&" )
                .replace( /%20/g, "+" )
            ;
            return( source );
        }
     
    eventApp.config(['$httpProvider', function($httpProvider) {
        // Set CSRF token for requests
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
     
        // Use urlencoded POST bodies
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
        $httpProvider.defaults.transformRequest.unshift(function(data, _) {
            return serializeData(data);
        });
    }]);
     
    eventApp.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        return $interpolateProvider.endSymbol('$}');
    });
