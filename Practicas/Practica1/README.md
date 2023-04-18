# Práctica 1: Despliegue de servicio ownCloud

<!-- TOC -->
  * [Arquitectura cloud propuesta](#arquitectura-cloud-propuesta)
  * [Arquitectura cloud implementada](#arquitectura-cloud-implementada)
    * [Redes](#redes)
    * [Volúmenes](#volúmenes)
    * [HAProxy](#haproxy)
    * [OwnCloud](#owncloud)
    * [MySQL](#mysql)
    * [phpMyAdmin](#phpmyadmin)
    * [Redis](#redis)
    * [OpenLDAP](#openldap)
  * [Pruebas realizadas](#pruebas-realizadas)
<!-- TOC -->

## Arquitectura cloud propuesta
En un escenario real, se propondría una arquitectura en cloud con los siguientes elementos:
* 2 a 4 servidores de aplicación
* Un cluster de dos servidores de BDs.
* Almacenamiento en un servidor NFS.
* Autenticación a través de servicio LDAP.
* Servicio Redis para bloque de ficheros.
* Balanceador de carga HAproxy. 
 
Este diagrama representaría la arquitectura propuesta:
![](img/diagrama.png)

## Arquitectura cloud implementada
Para abordar la solución de esta arquitectura cloud se va a utilizar docker compose.
Se ha creado un fichero bash [build.sh](build.sh) para facilitar el despliegue de los servicios que vamos a implentar 
para abordar la solución. Se ejecutaría como se indica a continuación:

``` bash
./build.sh
```

A continuación vamos a proceder a explicar en detalle los servicios implementados, redes y volúmenes.

### Redes
Se ha creado una red virtual interna en la cual van a estar interconectados todos los servicios. El único servicio que
va a tener acceso desde el exterior es el HAProxy. Esto nos proporcionará seguridad a nuestra solución.

### Volúmenes
Por cada servicio se ha creado un volumen local para tener persistencia de datos.

### HAProxy
HAProxy es un software libre que actúa como balanceador de carga (load balancer) ofreciendo alta disponibilidad, 
balanceo de carga y proxy para comunicaciones TCP y HTTP. Está pensado especialmente para balanceadores de tipo Layer7. 
HAProxy utiliza técnicas de arquitecturas de SO para ofrecer un gran rendimiento.
* **Imagen de docker utilizada:**
  * haproxy:2.7
* **Numero de instancias:**
  * 1
* **Archivos de configuración:**
  * [haproxy.cfg](haproxy/haproxy.cfg): El archivo haproxy.cfg es el archivo de configuración principal de HAProxy. Es un archivo de texto plano que contiene la configuración de HAProxy en formato legible por humanos. Este archivo se utiliza para definir los servidores y los puertos que HAProxy debe escuchar, así como para definir las reglas de balanceo de carga.
* **Puertos de acceso:**
  * IP:80
* **URL de estadísticas:**
  * IP:80/haproxy?stats
* **Configuración adicional:**
  * No se requiere, se levanta el servicio configurado.

### OwnCloud
ownCloud es una plataforma de almacenamiento en la nube de código abierto que permite a los usuarios almacenar 
y sincronizar archivos en línea. Es una alternativa a servicios de almacenamiento en la nube como Dropbox o Google Drive.
ownCloud se puede instalar en un servidor privado o en un proveedor de alojamiento web.
* **Imagen de docker utilizada:**
  * owncloud/server:10.12.0
* **Numero de instancias:**
  * 2, ofreciendo el mismo servicio
* **Archivos de configuración:**
  * No hay.
* **Puertos de acceso:**
  * Solo en la red virtual interna
* **Configuración adicional:**
  * Integrar Owncloud con un servicio de LDAP existente: https://www.youtube.com/watch?v=Jd0JImHj3fk

### MySQL
MySQL es un sistema de gestión de bases de datos relacional de código abierto. Es utilizado por muchas aplicaciones web 
y es una de las bases de datos más populares en la web. MySQL es un software cliente-servidor que se ejecuta en un 
servidor dedicado y se comunica con los clientes a través del protocolo MySQL.
* **Imagen de docker utilizada:**
  * mysql:8.0
* **Numero de instancias:**
  * 2, master y slave
* **Archivos de configuración:**
  * Master:
    * [mysql.conf.cnf](mysql/master/mysql.conf.cnf)
    * [mysql_master.env](mysql/master/mysql_master.env)
  * Slave:
    * [mysql.conf.cnf](mysql/slave/mysql.conf.cnf)
    * [mysql_slave.env](mysql/slave/mysql_slave.env)
* **Puertos de acceso:**
  * Solo en la red virtual interna
* **Configuración adicional:**
  * No se requiere, se levanta el servicio configurado.

### phpMyAdmin
phpMyAdmin es una herramienta de software libre escrita en PHP destinada a manejar la administración de MySQL a través 
de la Web. phpMyAdmin es una herramienta muy popular y se utiliza para administrar bases de datos MySQL. Con phpMyAdmin, 
los usuarios pueden crear y eliminar bases de datos, tablas y campos, así como agregar y eliminar usuarios y establecer 
permisos.
* **Imagen de docker utilizada:**
  * phpmyadmin:5
* **Numero de instancias:**
  * 1
* **Archivos de configuración:**
  * No hay.
* **Puertos de acceso:**
  * IP:8080
* **Configuración adicional:**
  * No se requiere, se levanta el servicio configurado.

### Redis
Redis es una base de datos en memoria de código abierto y almacenamiento en caché que se utiliza como base de datos, 
caché y agente de mensajes. Redis admite una amplia variedad de estructuras de datos, incluidas cadenas, hashes, 
listas, conjuntos y mapas ordenados. Redis también admite la replicación maestro-esclavo y la partición horizontal.
* **Imagen de docker utilizada:**
  * redis:7
* **Numero de instancias:**
  * 1
* **Archivos de configuración:**
  * No hay.
* **Puertos de acceso:**
  * Solo en la red virtual interna
* **Configuración adicional:**
  * No se requiere, se levanta el servicio configurado.

### OpenLDAP
OpenLDAP es una implementación libre del protocolo LDAP (Lightweight Directory Access Protocol) que se utiliza para 
acceder y mantener información distribuida sobre una red organizacional. OpenLDAP es una herramienta muy popular y 
se utiliza para autenticar usuarios y almacenar información de directorio.
* **Imagen de docker utilizada:**
  * bitnami/openldap:2.5
* **Numero de instancias:**
  * 1
* **Archivos de configuración:**
  * No hay.
* **Puertos de acceso:**
  * Solo en la red virtual interna
* **Configuración adicional:**
  * No se requiere, se levanta el servicio configurado.

## Pruebas realizadas
Se ha probado el correcto funcionamiento con Docker Desktop en Windows 11 22H2 con WSL2 con Ubuntu 22.04 LTS