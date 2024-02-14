# 2. Cifrado simétrico
encriptar:
openssl aes-256-cbc -a -salt -pbkdf2 -in secrets.txt -out secrets.txt.enc
(siendo secrets.txt el mensaje original y secrets.txt.enc el nombre del mensaje encriptado)
desencriptar:
openssl aes-256-cbc -d -a -pbkdf2 -in secrets.txt.enc -out secrets.txt.new
(siendo secrets.txt.enc el mensaje encriptado y secrets.txt.new el mensaje sin encriptar)
## ¿Cómo has transferido la clave de cifrado a tu compañero? ¿Era un canal seguro?
Se la he dicho, le ha gustado. Es un canal medianamente seguro (el de al lado estaba a lo suyo).
## ¿Cuál es el principal inconveniente de este método?
El de al lado puede ser un chismoso.
## ¿Cómo puede solucionarse?
Pasando la clave simétrica por un mecanismo de cifrado asimétrico.

# Encadenamiento
## Descarga la imagen que encontrarás más abajo y cífrala con AES y modos ECB y CBC
openssl aes-256-ecb -a -salt -pbkdf2 -in secrets.txt -out secrets.txt.enc
openssl aes-256-ecb -d -a -pbkdf2 -in secrets.txt.enc -out secrets.txt.new
openssl aes-256-cbc -a -salt -pbkdf2 -in secrets.txt -out secrets.txt.enc
openssl aes-256-cbc -d -a -pbkdf2 -in secrets.txt.enc -out secrets.txt.new
## Compara los resultados: ¿qué observas? ¿Por qué ocurre esto?
No hay diferencia en ninguno de los casos.
Incluso se puede cifrar un jpg como txt, y descifrar de txt a jpg y sigue funcionando.
