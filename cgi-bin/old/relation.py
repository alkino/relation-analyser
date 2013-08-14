#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Yoann ARNAUD <yarnaud@crans.org> 2009                      ##
##                                                                       ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

cache = "/home/osmose/www/tools/relation_analyser/cache/"

import sys, os, cgi, commands, re

print "Content-type: text/html;charset=utf-8"
print ""

#commands.getstatusoutput("touch /tmp/toto")
#print str(os.environ)

import mega_relation_analyser

form=cgi.FieldStorage()
NumRelation = form.getvalue("NumRelation")
#NumRelation = "84434"

print u"<?xml version=""1.0"" encoding=""UTF-8""?>"
print u"<html>"
print u"<head>"
print u"  <title>Analyse de la relation " + NumRelation + u"</title>"
print u"</head>"
print u"<body>"

print "<p>"
print "<b>Lecture des ways :</b>"
print "</p>"
sys.stdout.flush()
print "<p>"
try:
    w = mega_relation_analyser.GetWaysForRelation(str(NumRelation), "<br/>", cache)
except:
    print "<br/>"
    print "La relation n'existe pas"
    print u"</body>"
    print u"</html>"
    sys.exit(0)
print "</p>"

#print "<p>"
#print "<b>Save ways :</b>"
#print "</p>"
#sys.stdout.flush()
#f = open(cache+"relation-"+str(NumRelation)+".way","w").write(repr(w))

print "<p>"
print "<b>Jonction des ways :</b>"
print "</p>"
sys.stdout.flush()
w = mega_relation_analyser.JoinWays(w)

print "<p>"
print "<b>Projection Mercator :</b>"
print "</p>"
sys.stdout.flush()
w2 = mega_relation_analyser.WaysToMercator(w)

print "<p>"
print u"<b>Vérification de la relation (ouverture):</b>".encode("utf8")
print "</p>"
sys.stdout.flush()
c = mega_relation_analyser.WaysCheck(w)

#if c:
#    print "<p>"
#    print u"<b>Écriture du fichier poly :</b>".encode("utf8")
#    print "</p>"
#    sys.stdout.flush()
#    r = mega_relation_analyser.WaysToPoly(w, cache+"relation-"+str(NumRelation), open(cache+"relation-"+str(NumRelation)+".poly","w"))

print "<p>"
print u"<b>Vérification de la relation (auto-intersection):</b>".encode("utf8")
print "</p>"
sys.stdout.flush()
nod2 = []
for way in w:
    com = "java -classpath jts:/usr/share/java/jts.jar EssaiJts \"LINESTRING ("
    com += ",".join([str(x[2]) + " " + str(x[1]) for x in way])
    com += ")\""
    s, o = commands.getstatusoutput(com)
    o = o.split("\n")[0].strip()
    
    ReAllPoints = re.compile("[\(,][^\(,\)]*[\),]")

    for point in ReAllPoints.findall(o):
        #print point
        #print point[1:-1]
        lon, lat = point[1:-1].strip().split(" ")
        lat = float(lat)
        lon = float(lon)
        nod2.append((lat,lon))

print "<p>"
print u"<b>Écriture du fichier nod :</b>".encode("utf8")
print "</p>"
sys.stdout.flush()
f = open(cache+"relation-"+str(NumRelation)+".nod", "w")
for way in w:
    if way[0][0] <> way[-1][0]:
        f.write(" ".join(way[0])+"\n")
        f.write(" ".join(way[-1])+"\n")
f.close()

print "<p>"
print u"<b>Écriture du fichier nod2 :</b>".encode("utf8")
print "</p>"
sys.stdout.flush()
f = open(cache+"relation-"+str(NumRelation)+".nod2", "w")
for lon, lat in nod2:
    f.write("0 " + str(lon) + " " + str(lat)+"\n")
f.close()

print "<p>"
print u"<b>Écriture du fichier SVG :</b>".encode("utf8")
print "</p>"
sys.stdout.flush()
mega_relation_analyser.MakeSvg(w, w2, NumRelation)

print "<p>"
print u"<b>Écriture du fichier GPX</b>".encode("utf8")
print "</p>"
sys.stdout.flush()
mega_relation_analyser.WaysToGpx(w, open(cache+"relation-"+str(NumRelation)+".gpx","w"))


#print "<p>"
#print u"<b>Écriture du fichier name :</b>".encode("utf8")
#print "</p>"
#sys.stdout.flush()
#lines = mega_relation_analyser.GetLinesFromApi("relation/"+str(NumRelation))
#lines = [x for x in lines if 'k="name"' in x]
#if lines:
#    open(cache+"relation-"+str(NumRelation)+".name", "w").write(lines[0].split('"')[3].encode("utf8"))
#else:
#    open(cache+"relation-"+str(NumRelation)+".name", "w")


print "<p>"
print "<b>Conversion en PNG :</b>"
print "</p>"
sys.stdout.flush()
r = commands.getstatusoutput("inkscape --without-gui --file="+cache+"relation-"+str(NumRelation)+".svg --export-png="+cache+"relation-"+str(NumRelation)+".png --export-width=1000")

## Simplification ##

#print u"<b>Création du SVG simplifié :</b>".encode("utf8")
#sys.stdout.flush()
#w = mega_relation_analyser.SimplifyWays(w)
#w2 = mega_relation_analyser.WaysToMercator(w)
#mega_relation_analyser.MakeSvg(w, w2, NumRelation)

## Redirection ##

print "<script type=\"text/javascript\">"
print "window.location = \"relation_result.py?NumRelation="+str(NumRelation)+"\""
print "</script>"

print u"</body>"
print u"</html>"
