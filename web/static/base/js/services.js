// Data service serves the data retrieved from DB as well as the filter parameters
app.service('dataService', function ($http, $rootScope) {
    // Data retrieved from DB
    var data = {};
    var filter = {};
    var map = {};
    var footprints = {};
    var dataCollection = {type:"FeatureCollection", features:[]};
    var fullNumImages = {}

    // $rootScope.$on('filterChanged', filterData);

    initData();
    initFilter();

    return {
        notes:function () {
            // This exposed private data
            return data;
        },
        setData:function ( searchresults, nrImagesFound) {
            // This is a public function that modifies private data
            data['searchresults'] = searchresults;
            data['framedata'] = [];
            for (var i=0;i< data.searchresults.features.length;i++){
                var datestrings = data.searchresults.features[i].properties.dates;
                data.framedata.push( data.searchresults.features[i].properties);
            }
                filterData();
            data['nrImagesFound'] = nrImagesFound;
        },
        
        requestOptions: function(){
            return $http({
                url:  "/api/options/",
                method: "GET",
            }).success(function(jsonData){
                // make results available
                console.log('Succesfully queried options');
                // console.log(data)
                // We put the search results in data service!!!

                // // Also applying filter right away here
                // for (var i=0;i< data.searchresults.features.length;i++){
                //     var datestrings = data.searchresults.features[i].properties.dates;
                //     data.framedata.push(data.searchresults.features[i].properties);
                // }
                //     filterData();
            })
        },
        
        getData: function(){
            return data
        },
        getFilter:function(){
            return filter;
        },
        getAOI:function(){
            return filter.aoi;
        },
        updateAOI:function(what){
            filter.aoi = what;
        },
        data:function (){
            return data;
        },
        fullNumImages:function(){
            return fullNumImages;
        },
        footprints:function(){
            return footprints;
        }
    }
 });

app.service('procService', function ($http) {
    this.status = 'Probeer eens wat';
    this.requestOptions =  function(par){
            console.log('Do requestoptions',par)
            return $http({
                url:  "/api/options/",
                method: "GET",
            }).success(function(jsonData){
                // make results available
                console.log('Succesfully queried options');
                console.log(jsonData)
                this.options = jsonData
            })
    }

    this.showOptions = function(){
        console.log('Show options')
        return this.options
    }
});