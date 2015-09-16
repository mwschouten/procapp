

app.service('projectService', function ($http) {
    this.requestProjects =  function(){
            console.log('Do request projects')
            return $http({
                url:  "/api/projects/",
                method: "GET",
            }).success(function(result){
                // make results available
                console.log('Succesfully queried projects');
                console.log(result)
                this.active = result.result
                this.current = this.active[0]

            })
    }

    this.set_current = function(name){
        this.current = name
    }

    this.get_active = function(){
        return this.active
    }
    this.get_current = function(){
        return this.current
    }
});

app.service('procService', function ($http, projectService) {
    this.status = 'Probeer eens wat';

    this.requestOptions =  function(){
            console.log('Do request options')
            return $http({
                url:  "/api/options/",
                method: "GET",
            }).success(function(jsonData){
                // make results available
                console.log('Succesfully queried options');
                this.options = jsonData
            })
    }

    this.getAll = function(what){
            console.log('Set to make ',what)
            this.result=[]
            return $http({
                url:  "/api/results/",
                method: "GET",
                params: what
            }).success(function(jsonData){
                // make results available
                console.log('Succesfully queried all results for :',what);
                console.log(jsonData.results)
                this.result = jsonData
            })
    }

    this.showOptions = function(){
        console.log('Show options')
        return this.options
    }


    this.check = function(what,parameters){
        console.log('Check a ',what)
        parameters.project = projectService.current
        console.log('Check with project: ',parameters.project)
            
            this.result=[]
            return $http({
                url:  "/api/check/"+what,
                method: "GET",
                params: parameters
            }).success(function(jsonData){
                // make results available
                console.log('Succesfully checked :',what,parameters);
                console.log(jsonData)
                this.result = jsonData
            })
    }


    this.run = function(what){
        console.log('Check a ',what)
            this.result=[]
            return $http({
                url:  "/api/run/"+what.result.hash,
                method: "GET",
            }).success(function(jsonData){
                // make results available
                console.log('Succesfully submitted :',what);
                console.log('Data returned: ',jsonData)
                // this.result=jsonData
                
            })
    }
});