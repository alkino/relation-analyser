#! /usr/bin/env python
#-*- coding: utf-8 -*-

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

def run():
    
    import cgi, sys, os
    import lib_analyse
    
    if len(sys.argv)>=2:
        relid = sys.argv[1]
        force = True
    else:
        relid = cgi.FieldStorage()["relid"].value
        try:
            force = cgi.FieldStorage()["force"].value == "1"
        except:
            force = False
            
    if 'HTTP_ACCEPT_LANGUAGE' in os.environ:
        lg = os.environ['HTTP_ACCEPT_LANGUAGE'].split(',')[0]
        if not (lg.find('-') < 0):
            lg = lg.split('-')[0]
            
    lib_analyse.analyser(relid, force, lg)

if __name__=="__main__":
    print "Content-Type: text/html; charset=utf-8"
    print
            
    try:
        run()
        print "OK"
    except:
        raise
        print "NOK"
