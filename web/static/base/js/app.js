
var app = angular.module('TSXCatalogue', 
        // ['ngCookies','ngRoute','leaflet-directive','datarefresh','ui.bootstrap',])
        ['ngCookies','ngRoute','leaflet-directive','datarefresh','ui.bootstrap','lvl.directives.dragdrop'])
 

app.config([
    '$httpProvider',
    '$interpolateProvider',
    function($httpProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('{{');
        $interpolateProvider.endSymbol('}}');
        //~ $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    }]);

app.run([
    '$http',
    '$cookies',
    function($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);

// set routing
app.config(function ($routeProvider) {

    $routeProvider
        .when('/',{ redirectTo: '/start'})
    
        // .when('/locations',
        //     {controller: 'MapLocCtrl',
        //      templateUrl: 'static/base/partials/map_locations.html'
        //     })
        // .when('/search',
        //     {controller: 'MapCatalogueCtrl',
        //      templateUrl: 'static/base/partials/catalogue.html'
        //     })
        // .when('/reports',
        //     {controller: 'MapLocationsCtrl',
        //      templateUrl: 'static/base/partials/locations.html'
        //     })
        .when('/start',
            {controller: 'ProcessingCtrl',
             templateUrl: 'web/static/base/partials/start.html'
            })

        .when('/test',
            {controller: 'MainCtrl',
             templateUrl: 'web/static/base/partials/start3.html'
            })

        .otherwise({ redirectTo: '/test'});
});
console.log('app setup done')


