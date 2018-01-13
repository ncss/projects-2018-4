(function(){
  var wrapper = document.createElement('div');
  var mapElm = document.createElement('div');
  var map, infoWindow, marker;

  wrapper.appendChild(mapElm)

  wrapper.className = "wrapper";
  mapElm.className = "map";

  function initMap() {

    map = new google.maps.Map(mapElm, {
      center: {lat: -34.397, lng: 150.644},
      zoom: 6
    });
    marker = new google.maps.Marker({
        position: {lat: -34.397, lng: 150.644},
        map: map,
        title: 'Where da meme at'
    });

    infoWindow = new google.maps.InfoWindow;
  }

  wrapper.onclick = function(){
    wrapper.style.opacity = '0';
    setTimeout(function(){
      document.body.removeChild(wrapper);
    }, 400);
  }
  mapElm.onclick = function(e){
    e.stopPropagation();
  }

  function OpenMap(lat, lng){
    document.body.appendChild(wrapper);

    lat = lat.toFixed(0);
    lng = lng.toFixed(0);
    marker.setMap(null);

    marker = new google.maps.Marker({
        position: {lat: parseFloat(lat), lng: parseFloat(lng)},
        map: map,
        title: 'Where da meme at'
    });
    map.panTo({lat: parseFloat(lat), lng: parseFloat(lng)});

    setTimeout(function(){
      wrapper.style.display = "block";
      wrapper.style.opacity = "1";
    }, 0)
  }

  window.map = {
    open: OpenMap,
  }
  window.initMap = initMap;
})()