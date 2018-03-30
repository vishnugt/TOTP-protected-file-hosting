Simple app to host files from your server protected with TOTP passwords


Requirements:

Flask==0.10.1
pyotp>=0
flask_login>=0


Instructions and commands:

docker run -d -p 5101:5000 -v /var/lib/deluge/Downloads:/var/lib/deluge/Downloads -it flaskapp

5000 from your container to 5101 of your host
-v flag to map directory 

docker ps
docker stop 
docker build -t flaskapp .
