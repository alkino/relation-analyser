Ceci est une copie de
http://wiki.openstreetmap.org/wiki/Servers/analyse.openstreetmap.fr

Bidouillé par sly sylvain at letuffe point org

Voilà un exemple de fichier vhost pour apache :
```apacheconf
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
```

Et pour `nginx` :

```nginx
	server {
		listen 80;
		server_name localhost;
		server_name_in_redirect off;
		root <PATH/TO/CODE>;
		rewrite ^/$ /cgi-bin/index.py;

		location ~ \.py$ {
			include uwsgi_params;
			uwsgi_pass 127.0.0.1:9000;
			uwsgi_modifier1 9;
		}
	}
```

Couplé avec un fichier de configuration pour `uwsgi`:
```
[uwsgi]
plugins = cgi
socket = 127.0.0.1:9000
cgi = <PATH/TO/CODE>
cgi-helper = .py=python2
```
