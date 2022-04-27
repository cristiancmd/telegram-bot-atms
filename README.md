## Demo:

![ezgif com-gif-maker](https://user-images.githubusercontent.com/18334127/165627990-01a634b5-8d8d-450f-b54a-176a7d94e74d.gif)


## Requerimiento:

Implementar un bot en Telegram que permita a un usuario consultar los cajeros automáticos próximos.

El bot deberá poseer dos comandos:

1. Link: Lista cajeros de la firma ‘Link’.

2. Banelco: Lista cajeros de la firma ‘Banelco’.

La información sobre los cajeros habilitados se debe obtener del dataset gratuito publicado por el Gobierno de la Ciudad: https://data.buenosaires.gob.ar/dataset/cajeros-automaticos

El bot debe cumplir las siguientes especificaciones:


- Los comandos deberán ser ‘case insensitive’

- Las coordinadas de los usuarios deberán solicitarse mediante la API de Telegram. Evitar
que el usuario tenga que ingresar a “mano” sus coordenadas.

- Se deben listar los 3 cajeros más cercanos a menos de 500m de distancia al usuario
(distancia geográfica directa al usuario, sin considerar calles).

- Solo se tendrán en cuenta cajeros automáticos dentro de CABA.

- De cada cajero se debe indicar su dirección y su respectivo banco.

- El algoritmo de búsqueda de los cajeros cercanos deberá implementar una solución con
complejidad temporal (O grande) mejor que lineal en el caso promedio. Idealmente agregar una pequeña explicación de porqué esta se cumple en la solución presentada.

  
  
  
Agregar en la respuesta del bot la imagen de un mapa indicando la posición del usuario y de los 3 cajeros listados. Para esto recomendamos el uso de algún servicio gratuito para la generación del mapa con sus respectivos marcadores.

  
Los cajeros en promedio pueden abastecer alrededor de 100 extracciones por recarga.

- En caso de existir 3 cajeros en el rango, el 70% de las personas extrae dinero del cajero
más cercano, 20% del segundo y 10% del tercero.

- En caso de existir 2 cajeros en el rango, el 70% de las personas extrae dinero del cajero más cercano y el 30% del segundo.

- En caso de existir solo un cajero en el rango, todas las personas extraen de este.

- Los cajeros son reabastecidos de lunes a viernes a las 8 de la mañana.

  

Asumiendo que cada vez que alguien consulta la API es siempre con la intención de realizar una extracción y utilizando la información previa, tratar de estimar la cantidad de extracciones restantes disponibles en un cajero electrónico y evitar que aparezca en el listado si sospechamos que ya no se pueden realizar extracciones.

El sistema tiene que ser resistente a reinicios y caídas, sin perder la información almacenada.
