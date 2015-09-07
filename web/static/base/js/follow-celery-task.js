angular.module('datarefresh', [])

// .directive('followCeleryTask', ['$timeout', '$http', function ($timeout, $http) {
//     return {
//         restrict: 'E',
//         // template: '<div> {{workon}} {{percentage}}  <progressbar value="percentage">{{percentage}}</progressbar></div>',
//         template: '<div> <progressbar value="percentage">{{percentage}}</progressbar></div>',
//         replace: true,
//         scope: {task:'='},
//         link: function (scope, element, attrs) {

//             console.log('Now the status update value is : ', scope.task)

//             var isRunning = true;
//             var percentage = 0

//             scope.percent = 'banaan'
//             scope.workon = ''

//             console.log('ATTRS',attrs)
//             console.log('SCOPE',scope)

//             function successFunction(data) {
//               if (data !== undefined && isRunning) {
//                 // percentage = data.process_percent;
//                 scope.workon = data.workon;
//                 scope.percentage = data.process_percent
//                 console.log('DATA',data)
//                 try {
//                   if (angular.equals(data,'"SUCCESS"')) {
//                     isRunning = false;
//                     scope.workon='Done'
//                     scope.percentage=100
//                   }
//                 }
//                 catch (error) {
//                   console.log('ERROR ',error);
//                 }
//               }

//               // Set the watch interval here
//               if (isRunning) {
//                 $timeout(function () { refreshFromUrl(scope.task); }, 5000);
//               }
//             }

//             function refreshFromUrl(task_to_follow) {
//               $http.get('task_status/'+task_to_follow).success(function (data, status, headers, config) {
//                 successFunction(data);
//               })
//               .error(function (data, status, headers, config) {
//                 console.log('ERROR ',data);
//               });
//             }

//             console.log('')
//             scope.$watch( scope.task, function (value) {
//                 if (value !== undefined && value !== 'banaan') 
//                 {
//                   isRunning = true;
//                   console.log('Change to ',scope.task)
//                   refreshFromUrl(attrs.task);
//                 }

//             }); 

//             scope.$on('$destroy', function () {
//                 isRunning = false;
//             });
//         }
//     }
// }])

.directive('celeryTaskControl', ['$timeout', '$http', function ($timeout, $http) {
    return {
        restrict: 'E',
        // template: '<div> {{workon}} {{percentage}}  <progressbar value="percentage">{{percentage}}</progressbar></div>',
        template: ' <div>\
                    <div class="col-md-3" ng-hide=running> \
                    <button class="btn btn-warning btn-block" type="button" ng-click=fnc(1)> {{name}} </button>\
                    </div>\
                    <div class="col-md-3" ng-hide=running> \
                    {{workon}}\
                    </div>\
                    <div class="col-md-3" ng-show=running>\
                      <button class="btn btn-danger btn-block" type="button" ng-click=fnc(-1)> Cancel </button>\
                    </div>\
                    <div class="col-md-6" ng-if=running>\
                      <div> <progressbar value="percentage">{{percentage}}</progressbar></div>\
                    </div>\
                    </div> ',
        replace: true,
        scope: {fnc:'=', running:'=',name:'=',workon:'='},
        // scope: {fnc:'=',running:'=',name:'='},
        link: function (scope, element, attrs) {

            var isRunning = true;
            var percentage = 0
            // console.log('scope.fnc : ',scope.fnc)
            // console.log('scope.running : ',scope.running)
            // console.log('scope.name :',scope.name)
            scope.percent = 'banaan'
            scope.workon = ''


            function successFunction(data) {
              if (data !== undefined && isRunning) {
                // percentage = data.process_percent;
                scope.workon = data.workon
                scope.percentage = data.process_percent
                try {
                  if (angular.equals(data.status,'FINISHED')) {
                    isRunning = false;
                    scope.workon='Done'
                    scope.percentage=100
                    scope.running = undefined
                  }
                }
                catch (error) {
                  console.log('ERROR ',error);
                }
              }

              // Set the watch interval here
              if (isRunning) {
                $timeout(function () { refreshFromUrl(scope.running); }, 500);
              }
            }

            function refreshFromUrl(task_to_follow) {
              $http.get('task_status/'+task_to_follow)
              .success(function (data, status, headers, config) {
                successFunction(data);
              })
              .error(function (data, status, headers, config) {
                console.log('ERROR ',data);
              });
            }

            console.log('scope running : ',scope.running)

            scope.$watch( function() { return scope.running; }, function (value) {
              console.log('value: ',value)
                if (value !== undefined && value !== 'banaan') 
                {
                  isRunning = true;
                  refreshFromUrl(value);
                }
            }); 

            scope.$on('$destroy', function () {
                isRunning = false;
            });

            console.log('scope : ',scope)
        }
    }
}]);
