
app.controller("ProcessingCtrl",function($scope, procService) {

	function setupProc() {
        procService.requestOptions()
            .success(function (result) {
                $scope.commands = result;
            })
            .error(function (error) {
                $scope.status = 'Unable to load processing options: ' + error.message;
            });
    }

    function init(){

        console.log('INITIALIZE')
        setupProc()
    }                
    init()

    console.log('READY INITIALIZE')

    $scope.commands = procService.showOptions()



});




