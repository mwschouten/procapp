
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

app.controller('MapController',function ( $scope,
        leafletBoundsHelpers, 
        leafletData) {

    function init_frame(){
      console.log('INITIALIZE MAP FRAME')
      
      $scope.amsterdam =  { lat: 52.6, lng: 5.7, zoom: 6 }
      $scope.layers = {baselayers: BASELAYERS}
      $scope.controls ={draw: {circle: false, polyline: false}} 
      $scope.aoi = {}
      // angular.extend($scope, {
      //     amsterdam: { lat: 52.6, lng: 5.7, zoom: 6 },
      //     layers: {baselayers: BASELAYERS},
      //     controls: {
      //         draw: {circle: false, polyline: false},
      //     },
      //     aoi: {}
      // });
      

      console.log('Controls: ', $scope.controls)
      leafletData.getMap().then(function(map) {
        var drawnItems = $scope.controls.edit.featureGroup;
        map.on('draw:created', function (e) {
            var layer = e.layer;      
            $scope.aoi =  e.layer.toGeoJSON()
            $scope.updateMap()
        });               
      });
    };

  init_frame()

});
