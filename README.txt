Ceci est une copie de
http://wiki.openstreetmap.org/wiki/Servers/analyse.openstreetmap.fr

Elle a été un peu nettoyée de dépendances d'accès en dur, et utilise
l'api.openstreetmap.fr au lieu de l'api officielle.


Bidouillé par sly sylvain at letuffe point org

Voilà un exemple de fichier vhost pour apache :
<VirtualHost *:80>

        ServerName analyser.openstreetmap.fr
        DocumentRoot /data/project/analyser/www/
        RewriteEngine On
        RewriteRule ^/$ /cgi-bin/index.py [R,L]

        Alias /results/ /data/work/analyser/

        ScriptAlias /cgi-bin/ /data/project/analyser/cgi-bin/
        <Directory /data/project/analyser/cgi-bin/>
                AllowOverride None
                Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
                Order allow,deny
                Allow from all
        </Directory>

        ErrorLog /var/log/apache2/analyser-error.log
        LogLevel warn
        CustomLog /var/log/apache2/analyser-access.log combined

</VirtualHost>

