# @MatchViajes

BOT de Telegram hecho en python que permite cargar viajes que vas a hacer para que otras personas lo vean y se sumen para compartir gastos.
Para encontrarlo en Telegram en el buscador ingresar el usuario @MatchViajesBOT

## Registro

Para empezar a usarlo el BOT detecta si el ID de Telegram del usuario ya esta registrado o no en la Base de Datos, si no está registrado te pide los siguientes datos: Nombre, Apellido, Mail y Telefono

## Iniciar

Enviando el comado /start se inicia el bot y luego para ver las opciones que ofrece ingresar el comando /menu

![menu](https://user-images.githubusercontent.com/64671460/173840069-fb38d549-251d-46e1-b5df-1df7777eddfd.jpg)

Como se ve en la imagen tenemos dos funciones, "Cargar Viaje" y "Ver Viajes"

## Cargar Viaje

Esta opcion te permite cargar el viaje que vas a hacer de forma muy sencilla pidiendo solo el recorrido que vas a hacer, la fecha y alguna aclaracion.

### Recorrido

Por el momento el BOT solo permite 2 recorridos que son de CABA a Tandil y de Tandil a CABA. Estas dos opciones aparecen en pantalla y al clickear una de ellas pasa automaticamente al siguiente paso que es cargar la fecha del viaje

### Fecha

Aqui se despliega un teclado interactivo donde el usuario puede elegir la fecha como se ve en la imagen.

![fecha](https://user-images.githubusercontent.com/64671460/173843138-f640a5f9-b636-4e6f-9412-d7d90b51ea7a.jpg)

### Aclaraciones

En esta seccion podemos ingresar todas las aclaraciones que queremos hacer sobre el viaje. Desde donde salis, la hora de salida, etc.

### Confirmacion

Antes de confirmar el viaje el BOT te deja revisar los datos ingresados y editarlos si es necesario. Una vez confirmado el viaje queda guardado y si aparece una persona que se quiere sumar el BOT te manda un mensaje por Telegram con el numero de telefono de la persona que se quiere sumar.

![confirmar](https://user-images.githubusercontent.com/64671460/173844091-76b2b799-0267-4b00-9061-cf0ae22bc13d.jpg)

## Ver Viajes

Esta opcion permite ver todos los viajes que hay cargados en el BOT para cada recorrido. Clickeando en la opcion que te sirve automaticamente se envia un mensaje al conductor con tu numero de telefono y luego será el quien se comunique con vos para confirmar si te acepta o no como pasajero. 

![ver](https://user-images.githubusercontent.com/64671460/173846804-a79c6e67-fa68-42d4-b9bb-c5a9c0ad3537.jpg)




