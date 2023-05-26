# PRACTICA 3 DE SISTEMAS DISTRIBUIDOS

## Practica 3 de Sistemas distribuidos

### Pasos a seguir para la ejecución de la práctica

1.  Descargar e instalar [Docker](https://docs.docker.com/get-docker/)

2.  Ejecutar los siguientes comandos en una terminal:

    2.1 Crear una red para el contenedor:

    ```bash
    $ docker network create zoo-net
    ```

    2.2 Crear y ejecutar un contenedor con la imagen de Zookeeper:

    ```bash
    $ docker run --rm -d --name zookeeper-server --network zoo-net --network-alias -p zookeeper 2181:2181 zookeeper:3.8.1
    ```

    Al ejecutar los comandos anteriores, el contenedor de Zookeeper se ejecutará en segundo plano. Si desea ingresar a la terminal de Zookeper, ejecute el siguiente comando:

    ```bash
    $ docker run --rm -it --name zookeeper-client --network zoo-net zookeeper:3.8.1 zkCli.sh -server zookeeper
    ```

3.  Ejecutar el siguiente comando para crear una instancia de cliente:

    ```bash
    $ python3 client.py [host] [puerto] [identificador]
    ```

    Donde:

    a. _host_: Dirección IP del host donde se ejecuta el servidor.

    b. _puerto_: Puerto donde se ejecuta el servidor.

    c. _identificador_: Identificador del cliente.

Se pueden ejecutar varias instancias al mismo tiempo, donde la primera en ejecutarse actúa como contador, las demás solo muestran el valor actual de la cuenta. Al interrumpir el proceso del nodo contador, la siguiente instancia se vuelve contadora, y así sucesivamete.

**Recomendación:** Debido a que Zookeeper tiene un retraso al identificar la caída de un nodo, es recomendable esperar aproximádamente 20 segundos luego de la caída del nodo, para interrumpir al siguiente contador, si no se hace, puede ocurrir algun bug.
