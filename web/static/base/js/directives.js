
// app.controller('EditableCtrl', function($scope,$http) {
// // Took all this to main mapcontroller
// });


// On esc event
app.directive('onEsc', function() {
  return function(scope, elm, attr) {
    elm.bind('keydown', function(e) {
      if (e.keyCode === 27) {
        scope.$apply(attr.onEsc);
      }
    });
  };
});

// On enter event
app.directive('onEnter', function() {
  return function(scope, elm, attr) {
    elm.bind('keypress', function(e) {
      if (e.keyCode === 13) {
        scope.$apply(attr.onEnter);
      }
    });
  };
});

// Inline edit directive
app.directive('inlineEdit', function($timeout) {
  return {
    scope: {
      model: '=inlineEdit',
      handleSave: '&onSave',
      handleDelete: '&onDelete',
      handleCancel: '&onCancel'
    },
    link: function(scope, elm, attr) {
      var previousValue;
      
      scope.edit = function() {
        scope.editMode = true;
        previousValue = scope.model;
        
        $timeout(function() {
          elm.find('input')[0].focus();
        }, 0, false);
      };
      scope.save = function() {
        scope.editMode = false;
        scope.handleSave({value: scope.model});
      };
      scope.delete = function() {
        scope.editMode = false;
        scope.model = previousValue;
        scope.handleDelete({value: scope.model});
      };
      scope.cancel = function() {
        scope.editMode = false;
        scope.model = previousValue;
        scope.handleCancel({value: scope.model});
      };
    },
    templateUrl: 'static/base/partials/inline-edit.html'
  };
});



app.directive('hbobject', function () {
    return {
        restrict: 'E',
        templateUrl: 'web/static/base/partials/hbobject.html',
        replace: true,
        scope: {data:'='},
        link: function (scope, element, attrs) {
           console.log('HBOBJECT ',scope)
        }
    }
});





app.directive('hashdropzone', function ($sce) {
    return {
        restrict: 'E',
        templateUrl: '/web/static/base/partials/hashdropzone.html',
        replace: true,
        scope: {name:'=', setting:'=', data:'='},
        link: function (scope, element, attrs) {

          scope.content = scope.setting.type
          scope.my_origin = scope.setting.type

          scope.drop_ok = false
          scope.droppedonme = function(dragEl,dropEl){
            console.log('*** dropped on me ***')

            var drag = angular.element(dragEl);
            var drop = angular.element(dropEl);

            // See if we can replace this by an hbhash
            c = dragEl.getElementsByClassName('hbhash')[0]

            if (typeof c !== "undefined"){
                var src = c.innerText
                scope.drop_ok = true
                // try hbtype as well
                c = dragEl.getElementsByClassName('hbtype')[0]

                if (typeof c !== "undefined"){
                    var tp = c.innerText
                    if (tp !== scope.setting.type){
                      scope.drop_ok=false
                    }
                    console.log('Compare ',tp, scope.setting.type)
                }

                if (scope.drop_ok) {
                  // Keep the copied hbhash!
                  scope.data[drop.attr("settingid")] = src;
                  scope.my_origin = src.substring(0,10)
                  console.log('The element :',dragEl)
                }
                else{
                  scope.setError('Wrong type')
                }
                scope.$apply()            
            }
            console.log("The element " + drag.attr('id') + " has been dropped on " + 
                drop.attr("settingid") + "!");
          }

          scope.setError = function(){
                  scope.data[drop.attr("settingid")] = 'Error';
                  scope.$apply()
                  scipe.drop_ok = false
          }

          scope.show_origin = function(){
            scope.content = scope.my_origin
            // console.log(scope.my_origin)
          }
          scope.show_type = function(){
            scope.content = scope.setting.type
          }

        }
    }
});
