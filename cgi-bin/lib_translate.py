#! /usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Yoann Arnaud <yarnaud@crans.org> 2010                      ##
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

import os

class translator():
    
        def __init__(self, lg):
            self.folder = "/data/project/api.openstreetmap.fr/web/analyse/www/sources/lang"
            self.DefLang = "fr"            
            self.ChargerDic(lg)
        
        def ChargerDic(self, lg):
            FileLoc = os.path.join(self.folder,lg)
            if not os.path.exists(FileLoc):
                FileLoc = os.path.join(self.folder,self.DefLang)
            L = open(FileLoc).readlines()
            L = [ l.strip().decode("utf8") for l in L ]
            L = [ l.split(u'::') for l in L if (l<>u'' and l[0]<>u"#") ]
            self.Dic = {}
            for l in L:
                self.Dic[l[0].strip()] = l[1].strip()
            return self.Dic
        
        def TanslatePage(self, page):
            for key in self.Dic:
                page = page.replace("~" + key + "~",self.Dic[key])
            return page
        
        def TranslateKey(self, key):
            if key in self.Dic and self.Dic[key] <> "":
                return self.Dic[key]
            else:
                return u"--No-Translation--"
            
