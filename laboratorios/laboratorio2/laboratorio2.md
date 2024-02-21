# 1. Base 64

# 2. Cripto asimétrica

## ¿Por qué el comando anterior te pide una contraseña? ¿Para qué sirve?
Sirve para poder ver la clave privada.

## ¿Qué significa el 4096?, ¿y aes256?
La clave privada tiene 4096 bits.

aes256 es un método para cifrar.

## 2.1. Firma de archivos
Para firmar:

openssl dgst -sha256 -sign [fichero con clave privada del emisor] -out [fichero firmado] [fichero a firmar]

Para comprobar la firma:

openssl dgst -sha256 -verify [fichero con clave publica del emisor] -signature [fichero firmado] [fichero a firmar]

Devuelve Verified OK o Verification Failure

# 3. RSA: fundamentos
PREGUNTAR CÓMO SE HACE
