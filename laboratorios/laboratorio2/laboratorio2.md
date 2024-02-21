# 1. Base 64

# 2. Cripto asimétrica

## ¿Por qué el comando anterior te pide una contraseña? ¿Para qué sirve?
Sirve para poder ver la clave privada.

## ¿Qué significa el 4096?, ¿y aes256?
La clave privada tiene 4096 bits.
aes256 es un método para cifrar.

## 2.1. Firma de archivos
openssl dgst -sha256 -sign [clave_adecuada] -out [fichero_firma] [texto_en_claro]
openssl dgst -sha256 -verify [clave_adecuada] -signature [fichero_firma] [texto_en_claro]
PREGUNTAR CÓMO SE HACE

# 3. RSA: fundamentos
PREGUNTAR CÓMO SE HACE
