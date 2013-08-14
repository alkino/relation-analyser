    var layers={};
    var layersPois={};

    //-----------------------------------
    function initMap() {
            
      map = new OpenLayers.Map ("map", {
        controls:[
          new OpenLayers.Control.Navigation(),
          new OpenLayers.Control.PanZoomBar(),
          new OpenLayers.Control.LayerSwitcher(),
          new OpenLayers.Control.MousePosition(),
	        new OpenLayers.Control.Attribution()],

	      maxExtent: new OpenLayers.Bounds(-20037508,-20037508,20037508,20037508),
	      maxResolution: 156543,
	  
	      numZoomLevels: 20,
	      units: 'm',
	      displayProjection: new OpenLayers.Projection("EPSG:4326")
      });

      var layerMapnik = new OpenLayers.Layer.OSM.Mapnik("Mapnik");
      map.addLayer(layerMapnik);
      
      var layerTilesAtHome = new OpenLayers.Layer.OSM.Osmarender("Osmarender");
      map.addLayer(layerTilesAtHome);

      var lonLat = new OpenLayers.LonLat(2, 47).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
      map.setCenter(lonLat, 6);
      resizeMap();
      
      var rel_id = $('relid').value;
      if (rel_id != '') {
        startAnalyse(1);
      } 

    }

    //-----------------------------------
    function addPolyToMap(ref) {
      var now = Date.parse(new Date());
      var layer = new OpenLayers.Layer.GML("Relation " + ref, "../results/" + ref + ".osm?" + now,
        { format: OpenLayers.Format.OSM,
	        style: { strokeColor: "blue",
	                 strokeWidth: 3,
	                 strokeOpacity: 0.5,
	                 fillOpacity: 0.2,
                   fillColor: "lightblue",
                   pointRadius: 6
	               },
	        projection: new OpenLayers.Projection("EPSG:4326"),
	        displayInLayerSwitcher: false
	      });	      

      layer.events.register("loadend", layer, function() {
        if (this.features.length) {
          var extent;
	  extent = this.features[0].geometry.getBounds();
          for (var i = 1; i < this.features.length; i++) {
            extent.extend(this.features[i].geometry.getBounds());
          }
          if (extent) {
            this.map.zoomToExtent(extent);
          }
        }
      });

      map.addLayer(layer);
      layer.loadGML();
      layers['poly'] = layer;
    }
    
    //------------------------------------
    function delPolyToMap() {
      if ('poly' in layers) {
        map.removeLayer(layers['poly']);
        delete (layers['poly']);
      }
    }
    
    //------------------------------------
    function addPoisToMap(test,ref) {
      pois = new OpenLayers.Layer.DynPoi(test, {
        location:"../results/" + ref + "-" + test + ".txt",
        projection: new OpenLayers.Projection("EPSG:4326"),
        displayInLayerSwitcher: false
      } );
      layersPois[test] = pois;
      pois.loadText();
      map.addLayer(layersPois[test]);
    }
    
    //------------------------------------
    function delAllPoisToMap() {
      for (test in layersPois) {
        map.removeLayer(layersPois[test]);
      }
      layersPois = {};
    }

    //------------------------------------
    function resizeMap() {
      
      var centre = map.getCenter();
      var zoom   = map.getZoom();
      
      var globalWidth  = 800;
      var globalHeight = 600;
      if (parseInt(navigator.appVersion)>3) {
        if (navigator.appName=="Netscape") {
          globalWidth  = window.innerWidth;
          globalHeight = window.innerHeight;
        }
        if (navigator.appName.indexOf("Microsoft")!=-1) {
          globalWidth  = document.body.offsetWidth-22;
      	  globalHeight = document.body.offsetHeight-8;
      	}
      }
      //var globalWidth  = document.getElementById('incFrameBg').style.offsetWidth;
      //var globalHeight = document.getElementById('incFrameBg').style.offsetHeight;
    
      var divHGH = document.getElementById('haut_gauche_haut').style;
      var divHGB = document.getElementById('haut_gauche_bas').style;
      var divHD  = document.getElementById('haut_droite').style;
      var divmap = document.getElementById('map').style;
      
      var p = 60/100;
      var border_width = 3;
      var h1 = 25;
      var h2 = 100;
      var W = Math.round(globalWidth * p);
      
      divHGH.width  = W + "px";
      divHGH.height = h1 + "px";
      divHGH.left   = "0px";
      divHGH.top    = "0px";
      
      divHGB.width  = divHGH.width;
      divHGB.height = h2 + "px";
      divHGB.left   = "0px";
      divHGB.top    =  (h1 + border_width) + "px";

      divHD.width = (globalWidth - W - (3 * border_width)) + "px";
      divHD.left = (W + border_width) + "px";
      divHD.height = (h1 + h2 + border_width) + "px";
      divHD.top   = "0px";
      
      divmap.top = (h1 + h2 + (3 * border_width)) + "px";

      map.setCenter(centre, zoom);
      
    }

    //-----------------------------------
    function startAnalyse(force) {
      
      var rel_id = $('relid').value;     
      
      if (rel_id == ""){
        return;
      }
      
      disableBut()
      delPolyToMap();
      delAllPoisToMap();

      var myReq = new XMLHttpRequest();
      
      if (myReq) {
        myReq.onreadystatechange = function (evnt) { if(myReq.readyState == 4) { loadResults(); } }
        if (force) {
            myReq.open('GET', '../cgi-bin/analyse.py?force=1&relid=' + rel_id, true);
        } else {
            myReq.open('GET', '../cgi-bin/analyse.py?force=0&relid=' + rel_id, true);
        }
        myReq.setRequestHeader("Cache-Control", "no-store, no-cache");
        myReq.send(null);
        $('haut_gauche_bas').innerHTML = 'Analyse en cours...';
        $('haut_droite').innerHTML = 'Analyse en cours...';
      }  
    }

    //-----------------------------------
    function loadResults() {

      var rel_id = $('relid').value;

      if (rel_id == ""){
        return;
      }

      disableBut();
      delPolyToMap();
      delAllPoisToMap();

      // frame de gauche
      var myReq = new XMLHttpRequest();
      myReq.open("GET", '../results/' + rel_id + '-res-g.html', false); 
      myReq.setRequestHeader("Cache-Control", "no-store, no-cache");
      myReq.send(null); 
      document.getElementById('haut_gauche_bas').innerHTML = myReq.responseText;
      
      // frame de droite
      var myReq = new XMLHttpRequest();
      myReq.open("GET", '../results/' + rel_id + '-res-d.html', false); 
      myReq.setRequestHeader("Cache-Control", "no-store, no-cache");
      myReq.send(null); 
      $('haut_droite').innerHTML = myReq.responseText;
      
      // polygone
      addPolyToMap(rel_id);
      
      // Pois
      var ColInput = $('haut_gauche_bas').getElementsByTagName("input");
      for (var i = 0; i < ColInput.length; ++i) {
        var el = ColInput[i];
        if (el.type == 'checkbox') {
          addPoisToMap(el.id,rel_id)
          el.checked = 1;
        }
      }

      //Buttons
      enableBut()
 
    }
    
    //----------------------------------
    function Toogle_Chk(test) {
      if ($(test).checked) {
        layersPois[test].setVisibility(1);
      } else  {
        layersPois[test].setVisibility(0);
      }
    }
    
    //----------------------------------
    function checkEnter(e){
      var characterCode;
      if(e && e.which) {
        e = e;
        characterCode = e.which; //netscape
      } else {
        e = event;
        characterCode = e.keyCode; //IE
      }
      if(characterCode == 13){ //if enter key
        startAnalyse(1);
      }
    }

    //----------------------------------
    function disableBut(){
      $('relid').disabled = true;
      $('Button1').disabled = true;
      $('Button2').disabled = true;
    }
    function enableBut(){
      $('relid').disabled = false;
      $('Button1').disabled = false;
      $('Button2').disabled = false;
    }
