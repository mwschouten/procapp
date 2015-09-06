
app.controller("ProcessingCtrl",function($scope, procService) {

	function setupProc(toDo) {

        $scope.toDo = toDo;


        procService.requestOptions()
            .success(function (result) {
                $scope.commands = result;
                $scope.data = [];
		        $scope.toMake = result[toDo]['result'];
                console.log('Now going to make: ',$scope.toMake)
    			// Get the types of things needed
                $scope.inputs = []
                for (i=0; i<result[toDo].dependencies.length ;i++){
                	var s = result[toDo].dependencies[i]
                	$scope.inputs.push( result[toDo]['settings'][s]['type'])
	                console.log('Dependencies require types : ', s,$scope.inputs)
                } 


                procService.getAll(toDo)
	            .success(function (result) {
	                $scope.data[toDo] = result;
	            })
	            .error(function (error) {
	                $scope.status = 'Unable to load available results: ' + error.message;
	            });

            })
            .error(function (error) {
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
		      console.log("The element " + drag.attr('id') + " has been dropped on " + drop.attr("id") + "!");
    	};
	}

	function listSetup(){
    	$scope.tasklist = []

    	$scope.addToTaskList = function(item) {
    		console.log(item)
    		$scope.tasklist.push([item,$scope.commands[item].settings])
    	}
    	$scope.visible = true;

		$scope.toggle = function() {
		  $scope.visible = !$scope.visible;
		};
    
    }

    function init(){

        console.log('INITIALIZE')
        testDragDrop()
        listSetup()
        setupProc('Add2')
    }                
    init()

    console.log('READY INITIALIZE')
    // $scope.dropped('a','b')
    $scope.commands = procService.showOptions()



});




