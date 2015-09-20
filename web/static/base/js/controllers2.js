// app.controller("ProcessingCtrl",function($scope, procService) {

// 	function init(){
// 		// Set up for working
// 		$scope.toDo = []
// 		$scope.available_commands = []
// 		$scope.current_command.needs = {'dependencies':[],'settings':[]}


// 	}




// app.service('remoteCommandModel', function ($http){


// {"Add": {"version": "0.1","settings": {"a": {"default": "None","type": "<type 'float'>","mandatory": true},"b": {"default": "None","type": "<type 'float'>","mandatory": true}},"dependencies": [],"result": "data","longname": "Add two numbers","name": "Add"},"Add2": {"version": "0.1","settings": {"a": {"default": "None","type": "data","mandatory": true},"b": {"default": "None","type": "data","mandatory": true}},"dependencies": ["a","b"],"result": "data","longname": "Add two stored numbers","name": "Add2"}}

app.factory('getFromAPI', function($http) {
  var promise=[];
  var myService = {
    async: function(url) {
      if ( !promise[url] ) {
      	console.log('URL ',url)
        // $http returns a promise, which has a then function, which also returns a promise
        promise[url] = $http.get(url).then(function (response) {
          // The then function here is an opportunity to modify the response
          console.log('HTTP response ',response);
          // The return value gets picked up by the then in the controller.
          return response.data;
        });
      }
      // Return the promise to the controller
      return promise[url];
    }
  };
  return myService;
});



app.controller('MainCtrl', function( getFromAPI ,$scope,procService) {



  // $scope.action = function(a){
  //   console.log('selected ',a)
  // }

  getData = function(url,fld,what,callback) {
    // Call the async method and then do stuff with what is returned inside our own then function
    getFromAPI.async(url).then(function(d) {
      if (what){ 
        $scope[fld] = d[what];
      }
      else{ 
        $scope[fld] = d;
      }
      
      if (callback){
        callback()
      }
    });
  };


  // API connections
  function init(){
    $scope.commands = []
    $scope.do_new = true
    $scope.current_project = ''
    
    console.log('Init MainCtrl')
    getData('/api/options','commands')
    getData('/api/projects','projects','result')
  }

  $scope.setProject = function (project){
    console.log('Set project now to :',project)
    procService.set_current_project(project)
    $scope.project_active = project;

    getData('api/results/?project__name='+project,'results','results')

  }


  // Set the current command to execute (from the available tasks)
  $scope.setTodo = function (todo){
    console.log('Set active command now to :',todo)
    $scope.do_new = true
    $scope.parameters = {};
    $scope.command_active = todo
    $scope.command_needs = {dependencies:{},settings:{}}    
    $scope.command_needs_yesno = {dependencies:false,settings:false}
    $scope.command_needs_types = {}
	  for (var name in todo.settings) {

	    if (todo.settings.hasOwnProperty(name)) {
        // add this one to deps or settings?
  			var addto = (todo.dependencies.indexOf(name)>-1)? 'dependencies' : 'settings'
        var type = todo.settings[name].type
        // add, and make that one true (there is one or more)
        $scope.command_needs[addto][name] = todo.settings[name]
        $scope.command_needs_yesno[addto] = true
        $scope.command_needs_types[type] = true
	    }
	  }
  }


   
  $scope.check = function(){
      // Check the current settings with the api of the processing server
      console.log('Go check', $scope.parameters)
      procService.check( $scope.command_active.name, $scope.parameters)
              .success(function (result) {
                  if (result.hasOwnProperty('error')){
                      $scope.error=true
                      $scope.status = result.error
                      console.log('Set error!')
                  }   
                  else{
                      $scope.thing_to_make = result;
                      $scope.checked_ok=true
                      $scope.error=false
              }
              })
              .error(function (error) {
                  $scope.error=true
                  $scope.status = 'Unable to check: ' + error.message;
              });
  }



    $scope.submit = function(){
      // send in the curent hash (based on settings) for processing
      console.log('Go run', $scope.thing_to_make)
      procService.run($scope.thing_to_make)
              .success(function (result) {
                  if (result.hasOwnProperty('error')){
                      $scope.error=true
                      $scope.status = result.error
                      console.log('Set error!')
                  }   
                  else{
                      if (result.result==true){
                          // $scope.thing_to_make.status='Success'
                          console.log('****RESET***')
                          $scope.setProject($scope.project_active)
                      }
                  }
              })
      .error(function (error) {
          $scope.error=true
          $scope.status = 'Unable to submit: ' + error.message;
      })
    };




  init()

}); <!-- end of controller -->



