BASE_URL = 'http://127.0.0.1:8000'
BASELAYERS = {
    mapbox2: {
        name: 'Light',
        type: 'xyz',
        url: 'https://a.tiles.mapbox.com/v3/{layerId}/{z}/{x}/{y}.png',
        layerParams: {
            key: '007b9471b4c74da4a6ec7ff43552b16f',
            layerId: 'mwschouten.ka65g9el'
        }
    },

    osm: {
        name: 'OpenStreetMap',
        url: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        type: 'xyz'
    },
}

app.controller("HeaderCtrl",function($scope) {


    function init(){
        console.log('***START HEADER CONTROLLER""')
        $scope.current_project = 'Test project'
    
        // procService.requestOptions()
        //     .success(function (result) {
        //         $scope.commands = result;
        //         setupProc('AddM')
        //     })
        //     .error(function (error) {
        //         $scope.error=true
        //         $scope.status = 'Unable to load processing options: ' + error.message;
        //     });
    }
                
    init()
    console.log('READY INITIALIZE HEADER')
});




app.controller("ProcessingCtrl",function($scope, procService,projectService,  leafletBoundsHelpers, leafletData) {


	function switch_todo(toDo) {

        $scope.do_new = false
        $scope.error=false;

        $scope.toDo = toDo;
        $scope.current = []
        $scope.parameters = {};

        $scope.results = []; // list of results like we are making
        $scope.input = {}; // All necessary input types get a list here

        // $scope.checked_ok = false;
        $scope.thing_to_make = false;
        $scope.toMake = $scope.commands[toDo]['result'];

        console.log('Now going to make: ',$scope.toMake)

        $scope.commandToDo = $scope.commands[toDo];


        // Collect settings not-dependency
        $scope.othersettings = []
        var obj = $scope.commandToDo.settings
        for (var p in obj) {
            if( obj.hasOwnProperty(p) && $scope.dependencies.indexOf(p)==-1) {
                console.log('Property :',p)
                $scope.othersettings.push(p)
            } 
        }              
        console.log('OTHER SEETINGS: ',$scope.othersettings)
        // Collect dependencies (dependencies - names of them)
        // Get the types of things needed (inputs)
        $scope.dependencies = []
        var inputs = []
        for (var i=0; i<$scope.commandToDo.dependencies.length ;i++){
        	var s = $scope.commandToDo.dependencies[i]
            var t = $scope.commandToDo['settings'][s]['type']
            $scope.dependencies.push(s)           
        	if (inputs.indexOf(t) < 0){
                inputs.push( t )
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
        for (var i=0; i<$scope.inputs.length ;i++){
            var checktype= $scope.inputs[i]
            procService.getAll({resulttype:checktype})
            .success(function (result) {
                $scope.error=false
                $scope.input[checktype] = result.results;
            })
            .error(function (error) {
                $scope.error=true
                $scope.status = 'Unable to load available results: ' + error.message;
            });
        }
    }            
    

    $scope.check = function(){
        // Check the current settings with the api of the processing server
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


    $scope.submit = function(){
        // send in the curent hash (based on settings) for processing
        console.log('Go check', $scope.thing_to_make)
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
                            setupProc($scope.toDo)
                        }
                    }
                })
                .error(function (error) {
                    $scope.error=true
                    $scope.status = 'Unable to submit: ' + error.message;
                });
    };


    $scope.switch_todo = function(item){
        console.log('Switch to',item)
        setupProc(item)
    }

    $scope.switch_project = function(item){
        console.log('Switch to',item)
        projectService.set_current(item)
        $scope.current_project = item
        setupProc( $scope.toDo)   
    }

    function init_frame(){
        console.log('INITIALIZE')
        // testDragDrop()
        // listSetup()
    
        angular.extend($scope, {
            amsterdam: { lat: 52.6, lng: 5.7, zoom: 6 },
            layers: {baselayers: BASELAYERS},
            controls: {
                draw: {
                    circle: false,
                    polyline: false,
                },
            },
            aoi: {}
        });

        // console.log(JSON.stringify(layer.toGeoJSON()));
        console.log('Controls: ', $scope.controls)
        leafletData.getMap().then(function(map) {
          var drawnItems = $scope.controls.edit.featureGroup;
          map.on('draw:created', function (e) {
            var layer = e.layer;      
            $scope.aoi =  e.layer.toGeoJSON()
            $scope.updateMap()
          });               

          $scope.searchresults = {features:[]}
        });
    }

    function init_projects(){
        projectService.requestProjects()
            .success(function (result) {

                $scope.active_projects = result.result
                $scope.current_project = result.result[0]

            })
            .error(function (error) {
                    $scope.error=true
                    $scope.status = 'Unable to load projects: ' + error.message;
            });
    }


    function init_procoptions(){
        procService.requestOptions()
        .success(function (result) {
            $scope.commands = result;
            return result
        })
        .error(function (error) {
            $scope.error=true
            $scope.status = 'Unable to load processing options: ' + error.message;
        });
    }
  
    init_projects()
        .success(function (result){
            switch_project( $scope.current_project)
        })

    init_procoptions()
        .success(function (result){
            switch_todo( $scope.current_todo)
        })

    console.log('READY INITIALIZE')
    // $scope.dropped('a','b')
    $scope.commands = procService.showOptions()



});




