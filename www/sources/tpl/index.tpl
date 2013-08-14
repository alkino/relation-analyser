<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>

<head>
  <title>~title~</title>
  <meta http-equiv="Content-type" content="text/html;charset=UTF-8">
  <link rel="stylesheet" type="text/css" href="../www/sources/css/styles.css">
  <script type="text/javascript" src="../www/ol/OpenLayers.js"></script>
  <script type="text/javascript" src="../www/sources/js/OpenStreetMap.js"></script>
  <script type="text/javascript" src="../www/sources/js/DynPoi.js"></script>
  <script type="text/javascript" src="../www/sources/js/analyser.js"></script>
</head>

<body onload="initMap();"  onresize="resizeMap();" style="margin:0;padding:0;">

  <iframe style="display:none" id="hiddenIframe" name="hiddenIframe"></iframe>
  
  <div id="haut_gauche_haut" name="haut_gauche_haut">
    <input id="relid" type="text" onKeyPress="checkEnter(event)" value="~relid~" size="8" />
    <input type="button" id="Button1" name="Button1" value="!! ~button.analyse~ !!" onClick="startAnalyse(1)" />
    <input type="button" id="Button2" name="Button2" value="!! ~button.cache~ !!" onClick="startAnalyse(0)" />
  </div>
  
  <div id="haut_gauche_bas" name="haut_gauche_bas">
  </div>
  
  <div id="haut_droite" name="haut_droite">
  </div>
  
  <div id="map">
  </div>
  
  <div id="bas">
  <a href="http://www.openstreetmap.fr">OSM France</a> - <a href="http://www.openstreetmap.org">OSM</a>
  </div>
  
</body>
</html>

