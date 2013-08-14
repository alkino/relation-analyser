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


import sys, os, cgi, commands

print "Content-type: text/html;charset=utf-8"
print ""

form=cgi.FieldStorage()
NumRelation = form.getvalue("NumRelation")

print u"<?xml version=""1.0"" encoding=""UTF-8""?>"
print u"<html>"
print u"<head>"
print u"  <title>Analyse de la relation " + NumRelation + u"</title>"
print u"</head>"
print u"<body>"

## Javascript
print "<!-- Par Aurelien Jacobs -->"
print "<script language=\"javascript\">"
print "function openJOSM(left, bottom, right, top, objtype, objid) {"
print "  var frame = document.getElementById(\"josm_frame\");"
print "  var url = 'http://localhost:8111/load_and_zoom?left=' + left +"
print "            '&bottom=' + bottom +"
print "            '&right=' + right +"
print "            '&top=' + top;"
print "  if (objtype && objid) {"
print "    url += '&select=' + objtype + objid;"
print "  }"
print "  frame.src = url;"
print "}"
print "</script>"
print "<script language=\"javascript\">"
print "function openURL(url) {"
print "  var frame = document.getElementById(\"josm_frame\");"
print "  frame.src = url;"
print "}"
print "</script>"
print "<iframe id=\"josm_frame\" style=\"width:0px; height:0px; border: 0px\"></iframe>"

#print_retry = False

if "relation-"+NumRelation+".png" in os.listdir("../cache"):
    name = open("../cache/relation-"+NumRelation+".name").read()
    print "<h1>Analyse de la relation " + str(NumRelation) + " ("+name+") :</h1>"
    
    lines = open("../cache/relation-"+NumRelation+".nod").readlines()
    lines2 = open("../cache/relation-"+NumRelation+".nod2").readlines()
    n_mbrs = open("../cache/relation-"+NumRelation+".mbrs").readlines()[0]
    
    print "<p>%s membres</p>"%n_mbrs

    if not lines and not lines2:
        print "<p><b><font color=\"blue\"> La relation est correcte</font></b></p>"
    if lines:
        print "<p><b><font color=\"red\"> La relation est ouverte !</font></b></p>"
    if lines2:
        print "<p><b><font color=\"green\"> La relation s'auto-intersecte !</font></b></p>"
    f = '../cache/relation-'+NumRelation+'.png'
    print '<a href="'+f+'"><img src="'+f+'" width="30%"/></a><br/><br/>'
    
    if lines:
        print u"<h2>Liste des Nodes non reliés :</h2>".encode("utf8")
        print "<ul>"
        for line in lines:
            line = line.strip().split(" ")
            potlatch = "<a href=\"http://www.openstreetmap.org/edit?lat=" + line[1] + "&lon=" + line[2]  +"&zoom=17\">Potlatch</a>"
            josm = "<a href=\"javascript:openJOSM(" + str(float(line [2])-0.003)  + ", " + str(float(line [1])-0.003)  + ", " + str(float(line [2])+0.003)  + ", " + str(float(line [1])+0.003)  + ", 'node', " + line[0]  + ")\">JOSM</a>"
            print "<li> " + line[0] + " : " + potlatch + " " + josm + " </li>"
        print "</ul>"
#        print_retry = True
    
    if lines2:
        print u"<h2>Liste des intersections :</h2>".encode("utf8")
        print "<ul>"
        for line in lines2:
            line = line.strip().split(" ")
            potlatch = "<a href=\"http://www.openstreetmap.org/edit?lat=" + line[1] + "&lon=" + line[2]  +"&zoom=17\">Potlatch</a>"
            josm = "<a href=\"javascript:openJOSM(" + str(float(line [2])-0.002)  + ", " + str(float(line [1])-0.002)  + ", " + str(float(line [2])+0.002)  + ", " + str(float(line [1])+0.002)  + ")\">JOSM</a>"
            print "<li> " + potlatch + " " + josm + " </li>"
        print "</ul>"
#        print_retry = True
    
#    if print_retry:
    print "<a href=\"relation.py?NumRelation=" + NumRelation + "\">Recommencer l'analyse</a>"
    
    print u"<h2>Fichiers liés :</h2>".encode("utf8")
    exts = [".gpx",".svg"]
    for fichier in os.listdir("../cache"):
        print "<ul>"
        for ext in exts:
            if fichier.startswith("relation-"+ NumRelation) and fichier.endswith(ext):
                print "<li> <a href=\"../cache/"+fichier+"\">"+fichier+"</a> </li>"
        print "</ul>"

print u"</body>"
print u"</html>"
