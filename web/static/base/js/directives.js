
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
        templateUrl: '/static/base/partials/hbobject.html',
        replace: true,
        scope: {data:'='},
        link: function (scope, element, attrs) {

        }
    }
});




