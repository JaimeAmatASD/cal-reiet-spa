# Bitácora

Qué se hizo, cuándo, y qué sigue. Una entrada por sesión de trabajo cerrada.

Se escribe en idioma del dominio, no en técnico: dentro de tres meses esto se lee para
recordar qué pasó, no para revisar código.

---

## 2026-09-22 — Fase 1, paso 5: la fila llega a la hoja dentro del recorrido

**Qué se hizo.** El recorrido va ahora de punta a punta dentro de n8n: entra el correo,
se apartan los avisos automáticos antes de que los lea la IA, se miran las agendas de
las dos salas y la decisión queda anotada en la hoja de registro. Si el mismo cliente
vuelve a escribir, la fila no se duplica: se pone al día.

**Estado.** Terminado el tramo del correo a la fila. Faltan los pedidos reales
anonimizados y el reporte semanal.

**Decisiones.** Ninguna de peso.

**Se rompió algo.** Dos fallos que no daban error y por eso costaron caro, los dos en
`lessons.md`: un día con la sala vacía frenaba el recorrido antes de decidir —justo el
día en que hay hueco—, y las dos salas se miraban a la vez, así que la decisión salía
leyendo solo la Sala 1. Quedó una prueba que mira el archivo del flujo para que no
vuelvan.

**Lo que sigue abierto.** El permiso de Google seguía en modo prueba y caducaba
alrededor del 18; hay que comprobarlo antes de la próxima prueba con correos. Siguen
escritas a mano dentro del flujo las duraciones y los identificadores de las agendas.
`casa.yaml` sigue contradiciéndose con la hora de cierre.

**Próximo paso.** Fase 1, paso 6: veinte pedidos reales anonimizados y medir en cuántos
acierta.

---

## 2026-09-13 — Fase 1, paso 3: del correo a la ficha, de punta a punta

**Qué se hizo.** El recorrido anda entero con correos de verdad del buzón del
laboratorio: llega el correo, se trae la conversación completa, la IA la lee, nuestro
código decide qué hacer y, si hace falta, se mira la agenda de las salas del
laboratorio. Probado con un recibo de Google (sale «derivar», correcto) y con un pedido
inventado al que le faltaba un dato (sale «borrador», correcto). No se manda nada, no
se guarda nada en el correo y no se escribe en ninguna agenda.

**Estado.** Terminado el tramo del correo a la decisión. Falta que la decisión quede
anotada en la hoja.

**Decisiones.** Ninguna de peso. James pasó la IA a Gemini 3.5 Flash Lite. Aprendido de paso:
el regalo de 300 de Google no cubre Gemini, y un proyecto con saldo paga todo lo que
usa, desde la primera consulta, sin parte gratis.

**Se rompió algo.** Tres cosas, las tres en `lessons.md`: n8n vaciaba en silencio el
paquete que le pasa a nuestro código; la conversación llegaba sin el texto de los
correos, así que la IA leía nada; y el archivo del flujo tenía mal el nombre del
casillero de la agenda, que llegaba vacío al importarlo. Además n8n se cayó una vez por
falta de memoria con Chrome abierto. Antes de cargar los arreglos se guardó una copia
de n8n en `~/.n8n/copias/`.

**Lo que queda pendiente.**

1. **El permiso de Google sigue en modo prueba y caduca a los siete días** (montado el
   11, corta alrededor del 18). Hay que pasarlo a producción antes.
2. **Todo lo que entra al buzón pasa por la IA**, también los avisos de Google. Gasta
   saldo y, cuando haya hoja, va a meter filas que no son pedidos.
3. El arreglo que saca el texto de la conversación vive dentro de n8n. Se probó aparte,
   pero no quedó una prueba guardada en el repositorio.
4. **Falta probar en n8n un pedido completo**, el que va a mirar las agendas del
   laboratorio y devuelve horas libres. Las pruebas de hoy no llegaron hasta ahí.
5. **Dentro del flujo hay cosas de la casa escritas a mano**: las duraciones que se le
   pasan a la IA (40, 60, 90) y los id de las agendas de las salas. Contradice la regla
   de que eso vive en configuración. No se tocó.
6. **El horario de las salas no coincide consigo mismo**: `casa.yaml` dice que cierran a
   las 19:00, pero su propio comentario habla de 17:30. Va en la pregunta 1 a Egi. No se
   tocó.

**Sobre la petición a terapeutas.** James preguntó cuánto falta para que salga. El texto
ya lo arma nuestro código, probado. Faltan tres cosas: probar el pedido completo en n8n,
un lugar donde una persona elija la hora, y un paso que llame a nuestro código con esa
hora. Mandarla sola al grupo es fase 5. Hacerlo antes de la hoja sería adelantar fase:
lo decide James.

**Próximo paso.** Fase 1, paso 5: escribir la fila en la hoja de registro.

---

## 2026-09-11 — n8n ya entra al buzón del laboratorio

**Qué se hizo.** James montó el permiso de Google para la cuenta del laboratorio y lo
enchufó a n8n. Con eso quedó comprobado lo que hacía falta comprobar: **n8n lee el buzón
del laboratorio**. Sacó un correo de prueba de verdad, no simulado.

De paso quedaron habilitados los tres servicios que el proyecto va a usar —correo, hoja
y calendario— aunque por ahora solo se pide permiso para **leer** el correo. Ni enviar,
ni borrar, ni modificar. El sistema redacta y no envía, así que no hace falta más.

Hubo un tropiezo: Google devolvía «acceso denegado» porque la aplicación estaba en modo
prueba y no tenía ni un usuario de prueba dado de alta. Se agregó la cuenta del
laboratorio y funcionó.

**Estado.** El permiso funciona y el correo entra. El primer flujo todavía no está
guardado ni probado con un correo nuevo de verdad.

**Decisiones.** Una, en `decisions.md`: Gemini como modelo que lee el correo, por
precio. El contrato de lo que tiene que devolver no cambia.

**Se rompió algo.** No.

**Lo que hay que arreglar antes de seguir, y por qué.**

1. **La aplicación está en modo prueba y Google corta el permiso cada siete días.** La
   fase 1 existe para medir semanas seguidas. Tal como está, el lunes siguiente el
   sistema aparece muerto sin que nadie haya tocado nada. Hay que pasarla a producción.
2. **El sistema recibe un mensaje, y necesita la conversación entera.** La regla del
   proyecto es leer el hilo completo, porque el cliente da la duración tres correos
   atrás y no la repite. Falta el paso que pide la conversación completa antes de
   mandársela al modelo.
3. **Falta nuestro código en el medio.** El dibujo del flujo va del modelo a la hoja
   directo. Entre los dos tiene que estar el programa que ya existe: es el que descarta
   lo que la casa no ofrece, el que no da por buena una suposición, el que deriva las
   consultas de salud y el que arma la fila de la hoja.

**Próximo paso.** Que el flujo detecte un correo nuevo de verdad, y encadenar las cinco
piezas hasta la hoja.

---

## 2026-09-08 — Fase 1, paso 2: las columnas de la hoja de registro

**Qué se hizo.** Quedó definida la hoja donde el sistema anota cada pedido, que es el
instrumento de medición de toda la fase 1: de ahí salen los tres números con los que se
decide si el proyecto sigue —cuántos pedidos entran, cuántos se caen y cuánto se tarda
en contestar—. Son veintiuna columnas. Dieciocho las llena el sistema con lo que entendió
del correo; las cuatro últimas las llena una persona mientras la reserva avanza: cuándo
se contestó, en qué terminó y una nota. El encabezado está listo para pegar en la hoja,
en `docs/hoja-registro.md`.

El sistema ya devuelve la fila armada, con las columnas en orden, en la misma respuesta
que da hoy. Cuando el flujo esté montado, no hay que traducir nada: lo que sale se pega
en la hoja.

Una consulta que menciona salud deja fila igual —para que se pueda contar— pero esa fila
lleva solo el número de hilo, cuándo entró y que se derivó. Ni el nombre. Está probado
con una prueba que falla si alguna vez se filtra algo.

**Estado.** Terminado y probado: cincuenta y tres pruebas, siete nuevas. La hoja todavía
no existe en la cuenta del laboratorio: crearla es de la próxima sesión y necesita a
James con la cuenta abierta.

**Decisiones.** Una, en `decisions.md`: la hoja no guarda el correo ni el teléfono del
cliente. El nombre sí. La llave de la fila es el número del hilo, que lleva de vuelta al
correo original, y una hoja que se comparte es peor sitio para guardar contactos que el
buzón del que salieron.

**Se rompió algo.** No.

**Lo que hay que preguntar.** Si Egi trabaja mirando la hoja y necesita el correo del
cliente ahí para escribirle. Hoy no está.

**Próximo paso.** Crear la hoja en la cuenta del laboratorio con ese encabezado, y armar
el primer flujo en n8n: detecta correo nuevo, lo entiende, escribe la fila.

---

## 2026-09-08 — Dónde vive n8n: acá por ahora, con fecha de mudanza

**Qué se hizo.** Se cerró la duda que dejó abierta la sesión anterior. n8n se queda en
esta máquina de momento: se cerró Steam, que se comía media memoria, y n8n arrancó y
aguantó más de diez minutos sin moverse de los 500 MB, con 1 GB libre de sobra. La vez
pasada moría justo en esa franja. El editor responde, la batería de pruebas pasa entera
y el pedido de ejemplo entra y sale bien por la puerta que usa n8n.

**Estado.** n8n corriendo y estable en esta máquina. El primer flujo sigue sin armar.

**Decisiones.** Una, en `decisions.md`. Y trae fecha de caducidad: mientras n8n viva
acá, el sistema solo escucha el buzón con esta máquina encendida y sin Steam. Sirve para
construir y probar, no para medir semanas seguidas, que es exactamente lo que pide la
fase 1. Cuando llegue el momento de medir de verdad, la mudanza va a una máquina
alquilada de unos 5 € al mes con n8n y el código juntos dentro, y no a n8n contratado
como servicio: puestos juntos, el puente entre las dos piezas no se toca; separados,
hay que rehacerlo y abrirlo a internet.

**Se rompió algo.** No.

**Lo que hay que saber.** Steam quedó cerrado. Hay que cerrarlo cada vez que se arranque
n8n, y está anotado en el `README.md` junto al comando. El disco está al 92%.

**Próximo paso.** El primer flujo en n8n: que detecte un correo nuevo en el buzón del
laboratorio y escriba la fila en la hoja.

---

## 2026-09-08 — El laboratorio en pie: n8n corriendo y el enchufe con el código

**Qué se hizo.** Se montó n8n en la máquina y quedó corriendo. Y se construyó la puerta
por la que n8n le habla a nuestro código: le manda el pedido, recibe la respuesta.
Probada llamándola igual que la va a llamar n8n.

Antes de eso se leyó el calendario real del hotel —solo leer, ni un evento tocado— y se
contrastó el buscador de huecos contra dos días de verdad. **Acierta.** El 9 de
septiembre, con la reserva de las 10:00 ya puesta, el buscador ofrecía la Sala 1 desde
las 11:45; Egi puso a la clienta a las 12:15, dentro de lo propuesto. Y el 8, que estaba
lleno, dice que un tratamiento de 90 no entraba en ningún lado, que es lo que pasó.

De leer el calendario salieron cosas que no sabíamos: los calendarios por sala **ya
existen** (buena parte de la fase 3 estaba hecha y no figuraba), hay un tratamiento y
una duración que faltaban —Foot Reflex de 50 minutos—, el número de INV va en el título
y las dos reservas de un pedido para dos personas comparten el mismo. Todo en
`convenciones.md`.

**Estado.** n8n instalado y funcionando, pero **la máquina no lo aguanta**. Arrancó,
sirvió, y el sistema lo mató por falta de memoria a los pocos minutos. Son 3,6 GB de RAM
en total y con el navegador abierto quedan 400 MB libres. Antes de seguir hay que
decidir dónde vive n8n: en esta máquina cerrando cosas, o en otro lado. El primer flujo
todavía no está armado.

**Decisiones.** Dos, en `decisions.md`. n8n le habla a nuestro código por línea de
comandos, sin servidor ni dependencias nuevas —el costo es que n8n tiene que correr en
la misma máquina—. Y un cliente externo nunca lleva número de habitación: son
excluyentes.

**Se rompió algo.** Tres veces, y ninguna del proyecto. La versión de n8n publicada ese
mismo día venía rota. n8n 2.x pide Node 24 y la máquina tenía la 22. Y un error propio:
se encadenó el comando de instalación con otro y el sistema devolvió el resultado del
segundo, así que una instalación fallida se reportó como terminada bien. Anotado en
`lessons.md`.

**Efecto colateral que hay que saber.** Instalar Node 24 movió el Node por defecto de la
máquina de la 22 a la 24, porque el default apuntaba a «la última LTS». Si algo depende
de la 22, hay que fijarlo.

**Tres avisos.** El disco quedó en 6,8 GB libres, al 94%. n8n avisa que correrlo fuera
de un contenedor está en desuso: las versiones futuras van a pedir Docker. Y la máquina
tiene 3,6 GB de RAM, que no alcanzan para n8n con el navegador abierto.

**Próximo paso.** Decidir dónde corre n8n. Recién después, el primer flujo.

---

## 2026-09-08 — El recorrido completo: de un correo a una petición

**Qué se hizo.** El pedido ya hace el camino entero. Entra un correo, se entiende qué
pidió, se mira la agenda del día, salen las horas en las que cabe el tratamiento, una
persona elige una, y sale la petición escrita como se manda hoy al grupo. El sistema
redacta y espera: no manda nada, no toca ningún calendario.

Se puede ver corriendo `python ver_recorrido.py`, que lo cuenta paso a paso con cinco
casos y sin conectarse a nada.

Tres piezas nuevas. **La agenda**, que recibe lo ocupado de un día y devuelve dónde cabe
el tratamiento, dejando los quince minutos libres a cada lado y buscando tantas salas a
la vez como personas tenga el pedido —un masaje para dos son dos salas a la misma hora—.
**La petición**, que escribe el bloque exacto que hoy se manda a mano. Y **el circuito**,
que junta todo y decide qué sigue: derivar, redactar borrador, pedir la agenda, ofrecer
horas, o avisar que ese día no entra y decir qué sí entraría.

**De dónde salió el formato.** James pasó mensajes reales del grupo. Lo que estaba
anotado como formato de la petición no era el que se usa: la plantilla de la hoja del
Drive tiene cuatro campos y ninguna hora, y la petición real tiene cinco líneas, un
encabezado con el estado de cobro, una línea de preferencia de terapeuta que aparece
solo a veces, y la hora de principio y fin. Todo eso está ahora en `convenciones.md`,
incluidos los detalles que rompen cosas: la comilla de los minutos no es el mismo
carácter en la petición que en el parte.

Se escribió además el contrato de la parte que entiende el correo, con las instrucciones
que n8n le pone al modelo.

**Estado.** Terminado y probado: cuarenta pruebas, incluida una que recorre todo el
camino de punta a punta. Tres avisos. Los correos y la agenda de prueba son inventados,
no reales anonimizados. El horario de las salas y dónde corta la mañana están puestos
provisionales, deducidos de dos días de mensajes, y los tiene que confirmar Egi. Y el
catálogo sigue diciendo «masaje»: en la petición sale «Massage 60`» donde debería decir
«Holistic 60`».

**Decisiones.** Seis, en `decisions.md`. Las de peso: el recorrido termina con la
petición armada y sin enviar; la hora la elige una persona entre las libres, porque
elegir sola es criterio de Egi y eso cierra la fase 4; se adelanta la mitad mecánica del
buscador de huecos, porque sin agenda no hay petición posible; y lo que entra al
circuito es un pedido y no un correo, para que el Telegram de la spa manager entre por
la misma puerta.

**Se rompió algo.** No. Pero el `CLAUDE.md` mandaba a un skill que no existe en la
máquina, y era donde tenían que estar estos formatos. El puntero ahora va a
`docs/convenciones.md`. Queda la lección anotada.

**Lo que sigue abierto.** El borrador al cliente todavía deja el hueco
`[COMPLETAR A MANO]` donde tendría que decir qué hay libre ese día: ahora la agenda
existe y se puede llenar, pero cuando falta la duración no se sabe de qué tratamiento
mostrar huecos. Y un cliente externo con habitación asignada sale como alojado, porque
el sistema solo sabe si trajo habitación o no.

**Cinco cosas que hay que preguntarle a Egi**, hoy en `preguntas-para-egi.md`: qué
decide el encabezado de la petición, a qué hora abren y cierran las salas, dónde corta
la mañana, el catálogo real con precios, y si el turno rotativo se conserva.

**Próximo paso.** Enchufar los cables: el buzón y el bot de Telegram ya existen.

---

## 2026-09-08 — Fase 1, pasos 4 y 5: entender un correo y dejar una ficha

**Qué se hizo.** El sistema ya lee un correo de un cliente —la conversación entera, no
el último mensaje— y saca una ficha con lo que pidió: cuánto quiere que dure, qué día,
si por la mañana o por la tarde, y para cuántas personas. La ficha dice una de tres
cosas: que están los cuatro datos, que falta alguno, o que eso lo tiene que mirar una
persona. Cada dato lleva anotado si lo dijo el cliente, si lo dedujimos nosotros o si
salió de un mensaje anterior; lo deducido no se da por bueno y se le confirma. Cuando
falta algo, se redacta un borrador de respuesta en el idioma en que escribió el cliente,
con todo lo que falta preguntado en un solo correo y las tres duraciones puestas
delante. El sistema redacta, no envía: el borrador espera a que una persona lo mire.

Las consultas que mencionan salud salen derivadas y no se guarda una palabra de ellas.

Se llenaron los dos archivos de configuración: el de la casa y el del catálogo. El
catálogo está marcado como provisional dentro del propio archivo y los precios están
vacíos a propósito, esperando a Egi. En cuanto escriba las cifras, aparecen solas en
los correos.

**Estado.** Terminado y probado con ocho correos de ejemplo. Dos avisos: los correos de
prueba son inventados, no reales anonimizados; y donde el borrador tiene que decir qué
hay libre ese día deja un hueco marcado para completar a mano, porque buscar huecos es
la fase 4.

**Decisiones.** El catálogo pasa a su propio archivo; un dato deducido no cierra una
ficha; una consulta con datos de salud no se guarda en ningún sitio. Ver `decisions.md`.

**Se rompió algo.** No.

**Cambio de alcance.** El plan decía que estos pasos eran el correo del formulario, con
reglas y sin IA, y que el correo escrito a mano iba después. James pidió el correo
escrito a mano. Queda hecho ese, y el del formulario sin tocar.

**Próximo paso.** Sustituir los correos de ejemplo por veinte reales anonimizados y
mirar en cuántos acierta.

---

## 2026-09-04 — Fase 1, paso 1 (parcial): esqueleto del repositorio

**Qué se hizo.** El proyecto se sacó de la carpeta de descargas y quedó como
repositorio propio en `~/cal-reiet-spa`. Se montó el esqueleto de carpetas para
empezar a programar: el archivo de configuración de la casa, el lugar de las dos
piezas de código propio, y la batería de pruebas funcionando en vacío. Se eligió
Python y YAML. El catálogo de tratamientos quedó marcado como pendiente de Egi.

**Estado.** Terminado el esqueleto. El paso 1 NO está cerrado: falta n8n corriendo,
la cuenta de Google de pruebas, los tres calendarios, la hoja y el bot de Telegram.

**Decisiones.** Python por el precedente de `hotel-bot-mvp`; YAML para que la
configuración la pueda editar alguien que no programa. Ver `decisions.md`.

**Se rompió algo.** No.

**Próximo paso.** Montar el entorno de laboratorio: cuenta de Google de pruebas y
n8n corriendo.

---

## 2026-09-04 — Fase 0, entendimiento

**Qué se hizo.** Se mapeó el circuito completo de reserva tal como funciona hoy, con
Egi. Quedaron cerradas las tres ramas de excepción, la regla de los quince minutos entre
tratamientos, y el plazo de doce horas para soltar una reserva sin pagar. Se documentaron
las convenciones de títulos del calendario y el protocolo de peticiones del grupo de
terapeutas.

**Estado.** Terminado. El flujo está validado.

**Decisiones.** Telegram como canal interno, Google Calendar como fuente de verdad,
entorno de laboratorio separado de la operación. Ver `decisions.md`.

**Próximo paso.** Fase 1, paso 1: montar el entorno de laboratorio.

---

<!-- Entradas nuevas arriba de esta línea, más recientes primero -->
