

app.service('procService', function ($http) {


    this.set_current_project = function(name){
        this.current = name
    }

    this.get_current_project = function(){
        return this.current
    }

    this.check = function(what,parameters){
        console.log('Check a ',what)
        parameters.project = this.current
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