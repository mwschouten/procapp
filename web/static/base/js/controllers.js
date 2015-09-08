
app.controller("ProcessingCtrl",function($scope, procService) {

	function setupProc(toDo) {

        $scope.toDo = toDo;
        $scope.results = []; // list of results like we are making
        $scope.input = {}; // All necessary input types get a list here
        $scope.parameters = {};
        $scope.error=false;
        $scope.checked_ok = false;
        $scope.thing_to_make = false;

        procService.requestOptions()
            .success(function (result) {
                $scope.commands = result;
                console.log(result)
                console.log(toDo)
		        $scope.toMake = result[toDo]['result'];
                console.log('Now going to make: ',$scope.toMake)

                $scope.commandToDo = result[toDo];
                $scope.dependencies = []
                $scope.othersettings = []

                console.log('BANAAN')
                console.log(result[toDo])
                console.log(result[toDo].settings)

                console.log(result[toDo].settings.length)
                for (var i=0; i<result[toDo].settings.length ;i++){
                    console.log(i)
                    $scope.othersettings.push( result[toDo].settings[i].name)
                }


    			// Get the types of things needed
                var inputs = []
                for (var i=0; i<result[toDo].dependencies.length ;i++){
                	var s = result[toDo].dependencies[i]
                    $scope.dependencies.push(s)
                	if (inputs.indexOf(s) >= 0){
                        inputs.push( result[toDo]['settings'][s]['type'])
    	                console.log('Dependencies require types : ', s,inputs)
                    }
                } 
                $scope.inputs = inputs;

                // Get previous results
                procService.getAll({hb_taskname:toDo})
	            .success(function (result) {
                    $scope.error=false
	                $scope.results = result.results;
	            })
	            .error(function (error) {
                    $scope.error=true
	                $scope.status = 'Unable to load available results: ' + error.message;
	            });

                // Get inputs 
                // TODO make loop
                procService.getAll({resulttype:'data'})
                .success(function (result) {
                    $scope.error=false
                    $scope.input['data'] = result.results;
                })
                .error(function (error) {
                    $scope.error=true
                    $scope.status = 'Unable to load available results: ' + error.message;
                });


            })
            .error(function (error) {
                $scope.error=true
                $scope.status = 'Unable to load processing options: ' + error.message;
            });

        // procService.getAll('data')
        //     .success(function (result) {
        //         $scope.data['data'] = result;
        //     })
        //     .error(function (error) {
        //         $scope.status = 'Unable to load available results: ' + error.message;
        //     });

    }

    function testDragDrop(){
		$scope.dropped = function(dragEl, dropEl) {
	      	// this is your application logic, do whatever makes sense
		      var drag = angular.element(dragEl);
		      var drop = angular.element(dropEl);

            // See if we can replace this by an hbhash
              c = dragEl.getElementsByClassName('hbhash')[0]
              if (typeof c !== "undefined"){
                var src = c.innerText
                console.log('Found a hb hash ',src)
                $scope.parameters[drop.attr("settingid")] = src;
                $scope.$apply()            
              }

              console.log("The element " + drag.attr('id') + " has been dropped on " + 
                drop.attr("settingid") + "!");
         
    	};
	}

	function listSetup(){
    	$scope.tasklist = []

    	$scope.addToTaskList = function(item) {
    		// console.log(item)
    		$scope.tasklist.push([item,$scope.commands[item].settings])
    	}
    	$scope.visible = true;

		$scope.toggle = function() {
		  $scope.visible = !$scope.visible;
		};
    
    }

    $scope.check = function(){
        console.log('Go check')
        console.log('Go check', $scope.parameters)
        procService.check( $scope.toDo, $scope.parameters)
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


    $scope.run = function(){
        console.log('Go check', $scope.thing_to_make)
        procService.run( $scope.thing_to_make)
                .success(function (result) {
                    if (result.hasOwnProperty('error')){
                        $scope.error=true
                        $scope.status = result.error
                        console.log('Set error!')
                    }   
                    else{
                        $scope.rundata = result;
                }
                })
                .error(function (error) {
                    $scope.error=true
                    $scope.status = 'Unable to submit: ' + error.message;
                });
    }


    function init(){

        console.log('INITIALIZE')
        testDragDrop()
        listSetup()
        setupProc('Add')
    }                
    init()

    console.log('READY INITIALIZE')
    // $scope.dropped('a','b')
    $scope.commands = procService.showOptions()



});




