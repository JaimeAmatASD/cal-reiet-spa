# Decisiones

Elecciones de peso con su razón. No errores (eso es `lessons.md`): bifurcaciones donde
se podía ir para dos lados y se eligió uno.

---

## 2026-09-11 — Gemini como modelo que lee el correo

**Contexto**: la parte que entiende el correo la hace n8n con su nodo de IA, y hay que
elegir con qué modelo. Es una llamada por correo que entra, todo el día.
**Alternativas**: Claude, que es lo que se usa para construir el proyecto.
**Elegido**: Gemini, en su versión más barata. Leer un correo y devolver seis campos no
pide un modelo caro, y el volumen es de todos los días.
**Costo aceptado**: ninguno visible mientras respete el contrato. Lo que devuelve está
definido en `docs/contrato-lectura.md` y lo comprueba el sistema al recibirlo: si un
campo llega sin decir de dónde salió, se para y avisa. Cambiar de modelo es cambiar un
nodo, no rehacer nada.
**Se revisa si**: Gemini se equivoca en las veinte peticiones de prueba más de lo que
cuesta la diferencia de precio.

## 2026-09-08 — La hoja de registro no guarda el correo del cliente

**Contexto**: hay que definir las columnas de la hoja donde el sistema anota cada
pedido. La tentación es copiar todo lo que trae el correo, por si acaso.
**Alternativas**: guardar nombre, correo y teléfono, que es lo que haría una hoja hecha
a mano.
**Elegido**: nombre sí; correo y teléfono no. La llave de la fila es el número del hilo,
que lleva de vuelta al correo original en un clic. Para contestarle al cliente está el
buzón; para contar pedidos, esos datos no hacen falta.
**Costo aceptado**: si Egi trabaja mirando la hoja y necesita escribirle a alguien desde
ahí, tiene que ir al buzón. Está anotado como pendiente en `docs/hoja-registro.md`.
**Se revisa si**: Egi dice que le hace falta para trabajar.

## 2026-09 — Telegram como canal interno con los terapeutas

**Contexto**: el corazón del sistema es publicar la petición y capturar quién puede
hacerla. Hoy eso vive en un grupo de WhatsApp.
**Alternativas**: seguir en WhatsApp con la API oficial, que no lee grupos de esta
forma. Automatizar WhatsApp Web con el navegador, que viola los términos de uso y
arriesga el bloqueo del número del hotel.
**Elegido**: Telegram. API oficial y estable, permite botones, y la respuesta llega
estructurada en vez de como texto libre a interpretar.
**Costo aceptado**: hay que mudar de herramienta a un equipo de terapeutas autónomos,
varios de ellos poco técnicos. Ya aceptaron.
**Se revisa si**: el equipo rechaza el cambio en la práctica, o aparece una vía oficial
para grupos de WhatsApp.

## 2026-09 — Google Calendar como fuente de verdad, un calendario por sala

**Contexto**: hoy la sala se codifica con el color del evento y solo aparece escrita en
el parte que Egi manda cada noche por WhatsApp.
**Alternativas**: mantener el color como identificador. Montar una base de datos propia.
**Elegido**: un calendario por recurso. La sala pasa de decoración a estructura.
**Costo aceptado**: hay que migrar los eventos existentes y cambiarle el hábito a quien
crea eventos.
**Se revisa si**: el hotel contrata un producto comercial con agenda propia.

## 2026-09 — Entorno de laboratorio separado

**Contexto**: hace falta probar sin riesgo, y el buzón de producción migra de Hotmail a
Outlook.
**Elegido**: cuenta de Google de pruebas con sus propios calendarios, hoja y bot. El
bloque que lee el correo se construye aislado, para poder cambiar de Gmail a Outlook
reemplazando una pieza.
**Costo aceptado**: el conector de correo se hace dos veces.
**Se revisa si**: se resuelve antes qué buzón corporativo va a usar el hotel.

## 2026-09 — Nada específico de la casa dentro del código

**Contexto**: lo que se construya puede servir para Cal Reiet o para otras casas.
**Elegido**: tratamientos, salas, duraciones, márgenes, textos e idiomas en
configuración. Nada de multi-hotel todavía, que sería sobreingeniería.
**Costo aceptado**: algo más de trabajo inicial.
**Se revisa si**: aparece un segundo hotel de verdad.

## 2026-09 — Python para el código propio

**Contexto**: dos piezas van fuera de los nodos de n8n como código propio y probado:
el buscador de huecos y la máquina de estados.
**Alternativas**: Node, que es el lenguaje de n8n y el del bot de disponibilidad que
figura en `references.md` como reutilizable.
**Elegido**: Python. El precedente propio pesa más: `hotel-bot-mvp` ya resuelve una
máquina de estados en cuarenta y cuatro líneas de diccionarios y tiene una batería de
tests con pytest. Se copia un patrón ya probado en vez de inventar uno.
**Costo aceptado**: el bot de disponibilidad hay que portarlo, no copiarlo. Igual había
que corregirle dos cosas al portarlo, así que se reescribe de todos modos.
**Se revisa si**: aparece la necesidad de correr estas piezas dentro de un nodo de n8n.

## 2026-09 — La configuración de la casa en YAML, un solo archivo

**Contexto**: la regla es que el sistema se pueda montar en otra casa cambiando un
archivo. Tratamientos, duraciones, salas, márgenes, textos e idiomas van ahí.
**Alternativas**: TOML y JSON, que Python lee sin instalar nada. JSON además es lo que
habla n8n.
**Elegido**: YAML, en `config/casa.yaml`. Es el único de los tres que una persona no
programadora puede editar sin romperlo: admite comentarios y no lleva llaves ni comillas.
Quien va a mantener el catálogo de tratamientos es Egi, no un programador.
**Costo aceptado**: una dependencia (PyYAML), y que la sangría importa.
**Se revisa si**: el archivo deja de editarse a mano y pasa a generarse desde otro lado.

## 2026-09 — El cobro se marca a mano y es lo que habilita la confirmación

**Contexto**: faltaba definir qué separa una reserva ASIGNADA de una CONFIRMADA. El
glosario ya decía que no son lo mismo, pero no decía qué las separa.
**Alternativas**: automatizar el cobro, o integrarse con lo que use el hotel para
facturar.
**Elegido**: ninguna de las dos. El sistema no toca dinero ni se entera de si se pagó.
Alguien marca «cobrado» a mano, y esa marca es la única que destraba el paso a
CONFIRMADA. En la fase 1 es una casilla de la hoja; en la fase 5 es un botón.
**Costo aceptado**: si nadie marca la casilla, la reserva no se confirma. Es un paso
manual que se puede olvidar, y es deliberado: preferimos que se frene antes que
confirmar algo sin cobrar.
**Consecuencia que hay que construir sí o sí**: esto genera reservas esperando pago.
El sistema no las suelta — ver la decisión siguiente — pero sí tiene que mostrarlas.
Si nadie las ve, el spa termina rechazando trabajo real por huecos ocupados por
reservas fantasma, y falla en silencio. Ya pasó dos veces: en el bot de disponibilidad
y hoy a mano en el calendario del hotel. Ver `lessons.md`.
**Se revisa si**: el hotel adopta un cobro en línea del que el sistema pueda enterarse
sin intervención.

## 2026-09 — El sistema avisa de las reservas impagas, pero no las suelta

**Contexto**: para liberar el hueco hacía falta saber cuándo vence una reserva sin pagar.
La documentación hablaba de un plazo de doce horas como si fuera una regla.
**Alternativas**: un plazo fijo tras el cual el sistema suelta solo; o un plazo variable
según cuánto falte para el tratamiento, si el cliente está alojado, o la temporada.
**Elegido**: ninguna regla automática, porque no existe. Lo decide Egi caso por caso.
El sistema cuenta las horas configuradas y muestra la reserva en una lista de avisos.
Soltarla es siempre una acción humana.
**Costo aceptado**: un hueco puede quedar bloqueado indefinidamente si nadie mira la
lista. Se acepta porque el criterio real depende de cosas que el sistema no ve.
**Consecuencia**: la lista de reservas esperando cobro deja de ser un extra y pasa a ser
obligatoria. Es lo único que separa este diseño del fallo silencioso de `lessons.md`.
**Se revisa si**: aparece un criterio que Egi termine aplicando siempre igual. Entonces
sí se puede automatizar, y recién ahí.

## 2026-09-08 — La configuración en YAML, la ficha en JSON, y el catálogo aparte

**Contexto**: al construir la lectura de correos hacía falta decidir el formato de dos
cosas distintas que hasta ahora se trataban como una: los archivos que edita una
persona, y el dato que se pasan las piezas del sistema entre sí.
**Alternativas**: todo en JSON, que es lo que habla n8n y no necesita dependencia.
**Elegido**: separar por quién escribe cada cosa. La configuración sigue en YAML porque
la escribe Egi: admite comentarios y los textos de los correos son párrafos de varias
líneas, que en JSON quedan como una sola línea larga con saltos escritos a mano. La
ficha, que la escribe el sistema y la lee n8n, va en JSON: formato rígido y sin
ambigüedad. Además el catálogo de tratamientos sale a su propio archivo,
`config/tratamientos.yaml`, porque es lo que más se toca y quien lo mantiene no tiene
por qué pasar por delante del resto de la configuración.
**Costo aceptado**: esto revisa la decisión de "un solo archivo" de más arriba. Ahora
son dos, y `src/casa.py` los junta al cargar. Y YAML adivina tipos: en una lista de
idiomas lee `no` (noruego) como "falso", y una hora suelta como 10:30 como el número
630. Por eso la configuración se valida al cargar y revienta con un mensaje que dice
qué línea mirar, en vez de fallar tres pasos más adelante sin que se note.
**Se revisa si**: la configuración deja de editarse a mano y pasa a generarse.

## 2026-09-08 — Un dato deducido no cuenta como dato

**Contexto**: la lectura de un correo devuelve campos que el cliente escribió y campos
que hubo que interpretar. "El viernes" es una fecha, pero es una fecha que pusimos
nosotros.
**Alternativas**: darlo por bueno y seguir, que es lo que haría cualquiera con prisa.
**Elegido**: cada campo lleva de dónde salió — dicho, deducido o historial — y un campo
deducido nunca cierra la ficha. Aunque estén los cuatro datos, si alguno se dedujo la
ficha sale incompleta y el borrador se lo confirma al cliente en el mismo correo en que
le pregunta lo que falta.
**Costo aceptado**: alguna vuelta de correo de más cuando la deducción era correcta.
Se acepta porque el error contrario —agendar sobre una suposición— cuesta una sala
bloqueada, un terapeuta movido y un cliente que llega el día que no era.
**Se revisa si**: se mide cuántas deducciones acierta y el número es alto de verdad.

## 2026-09-08 — Una consulta con datos de salud no se guarda en ningún sitio

**Contexto**: algunos clientes cuentan lesiones, embarazos o tratamientos médicos al
pedir un masaje. Son datos de categoría especial bajo el RGPD y el proyecto además
tiene la ficha de salud explícitamente fuera de alcance.
**Alternativas**: guardar la ficha marcada como sensible y restringir quién la ve.
**Elegido**: no guardar nada. De ese correo queda una anotación con el número de hilo,
la hora y una nota de que lo tiene que atender una persona. Ni el nombre, ni la
dirección, ni una palabra del texto. El correo se queda en el buzón, que es donde ya
estaba, y quien lo atienda lo busca por ese número.
**Costo aceptado**: quien abre el aviso no sabe de qué va hasta que va al buzón.
**Cómo se sostiene**: la detección no depende solo de la IA. Hay una lista de palabras
en `casa.yaml` que dispara igual aunque la IA no haya visto la señal, y una prueba que
comprueba que ninguna palabra del correo terminó guardada. Prefiere derivar de más.
**Se revisa si**: nunca por comodidad. Solo si cambia el marco legal.

## 2026-09-08 — El recorrido del pedido termina en la petición armada, no enviada

**Contexto**: hacía falta decidir dónde corta el trabajo de «que el correo llegue hasta
Telegram». El circuito completo va del buzón al grupo de terapeutas y atraviesa tres
fases distintas del plan.
**Alternativas**: llegar hasta escribir la fila en la hoja de registro, que cerraría el
paso 5 de la fase 1. O llegar hasta mandar el mensaje de verdad, que es la fase 5 y
necesita el bot montado.
**Elegido**: el recorrido termina con la petición redactada y lista. No se manda. Entra
un pedido, se entiende, se mira la agenda, salen las horas libres, una persona elige una
y sale el bloque de cinco líneas listo para pegar en el grupo.
**Costo aceptado**: alguien copia y pega el mensaje a mano hasta la fase 5. Es
exactamente lo que se hace hoy, así que no empeora nada.
**Se revisa si**: se monta el bot de Telegram antes de lo previsto.

## 2026-09-08 — El sistema pone las horas libres sobre la mesa; elegir es de una persona

**Contexto**: los mensajes reales muestran que la petición sale con hora exacta de
principio y fin, nunca con una franja. Alguien tiene que elegir esa hora.
**Alternativas**: que el sistema elija sola la mejor. Es tentador y es la mitad de la
fase 4.
**Elegido**: el sistema calcula qué horas están libres y las muestra. La elección es
humana. El criterio de cuál conviene —pegar el tratamiento a una reserva existente antes
que abrir una cita suelta— es el criterio de Egi, y para darlo por bueno ella tiene que
ver propuestas y decir si son las que habría elegido. Eso cierra la fase 4, no esta.
**Costo aceptado**: un paso manual por cada petición.
**Se revisa si**: Egi valida las propuestas automáticas y coinciden con las suyas.

## 2026-09-08 — La agenda entra antes de la fase 4, partida en dos

**Contexto**: el plan ponía el buscador de huecos en la fase 4 y la petición en la 5.
Pero la petición lleva hora exacta, así que sin agenda no hay petición posible. Y James
además avisó que va a haber un Telegram para la spa manager donde ella pide tratamientos
sobre la marcha, y ahí también necesita ver agenda y disponibilidad.
**Alternativas**: sacar la petición sin hora, con la franja, y acordar la hora después
por mensaje. Es lo que a veces pasa hoy, pero no es lo que muestran los mensajes reales.
**Elegido**: adelantar la mitad mecánica de la fase 4 — leer la agenda del día y calcular
qué horas quedan libres, con los quince minutos a cada lado — y dejar para la fase 4 la
mitad que necesita criterio. Se parte por dónde está el juicio humano, no por dificultad.
**Costo aceptado**: se rompe la regla de «un chat, una fase». Se acepta porque el corte
es limpio y porque la parte adelantada no necesita que nadie valide nada.
**Se revisa si**: la mitad mecánica resulta no ser separable de la del criterio.

## 2026-09-08 — La parte que entiende el correo no es código propio

**Contexto**: la ficha recibe la lectura del correo ya hecha. Faltaba decidir quién la
hace: n8n con su nodo de IA, o código nuestro llamando al modelo.
**Alternativas**: escribir la llamada al modelo en Python. Permitiría correr el recorrido
entero sin n8n, pero pide una dependencia nueva y una credencial, y duplica algo que n8n
ya hace.
**Elegido**: la lectura la hace n8n. Nosotros escribimos dos cosas: el contrato exacto de
lo que tiene que devolver, y las instrucciones que n8n le pone al modelo. Más una lectura
de mentira para poder correr el recorrido entero en las pruebas sin llamar a nadie.
**Costo aceptado**: el recorrido completo de verdad no se puede correr fuera de n8n.
**Se revisa si**: n8n deja de ser el orquestador, o el nodo de IA se queda corto.

## 2026-09-08 — Lo que entra al circuito es un pedido, no un correo

**Contexto**: va a haber un Telegram para la spa manager, donde ella carga un tratamiento
sobre la marcha y de ahí sale la petición. Es una segunda puerta al mismo circuito.
**Alternativas**: construirlo alrededor del correo y ya se verá. Es más rápido hoy y
obliga a rehacerlo cuando aparezca la segunda puerta.
**Elegido**: la entrada del circuito es un pedido, sin importar de dónde venga. De ahí
para adelante el camino es el mismo: se entiende, se mira la agenda, sale la petición.
Hoy solo se construye la puerta del buzón; la de ella queda para cuando toque.
**Costo aceptado**: una pieza más de la que haría falta si solo hubiera correo.
**Se revisa si**: se decide que el Telegram de la spa manager no va.

## 2026-09-08 — La preferencia de terapeuta se guarda si la dicen, pero no obliga

**Contexto**: los mensajes reales llevan una línea de «Terapeuta Mujer» que la ficha no
capturaba. Es un dato que va en la petición.
**Alternativas**: hacerlo el quinto dato obligatorio y preguntárselo a todo el mundo en
el borrador.
**Elegido**: se guarda si el cliente lo dice y sale en la petición; si no lo dice, no se
pregunta y la ficha cierra igual. La mayoría no tiene preferencia y no vale una vuelta de
correo de más para todos.
**Costo aceptado**: algún cliente con preferencia que no la escribió va a recibir el
terapeuta que toque.
**Se revisa si**: se ve que la preferencia aparece más veces de las que se supone.


## 2026-09-08 — n8n vive en esta máquina, y se muda cuando haya que medir en serio

**Contexto**: n8n se instaló y el sistema lo mató por falta de memoria a los pocos
minutos. Había que decidir dónde vive antes de armar ningún flujo.
**Alternativas**: contratar n8n como servicio en la nube, unos 20-25 € al mes, cero
mantenimiento; o alquilar una máquina chica en internet, unos 5 € al mes, con n8n y
nuestro código juntos dentro.
**Elegido**: por ahora, esta máquina. Cerrando Steam entra: n8n pide unos 600 MB y
quedan 1,1 GB libres. Se midió y aguantó más de diez minutos con la memoria plana.
Cuesta cero y no obliga a rehacer nada. La razón de fondo la puso James: mientras se
está construyendo, tener todo en una máquina propia da más control —se ve, se toca y se
corrige sin depender de nadie—. La nube se contempla más adelante, no se descarta.
**Costo aceptado**: dos. Mientras n8n viva acá, el sistema solo escucha el buzón con
esta máquina encendida y sin Steam, así que sirve para construir y probar, no para
medir semanas seguidas. Y la fase 1 es precisamente medir: los números que va a mirar
Petra necesitan que esto esté escuchando siempre.
**Consecuencia**: la mudanza no es opcional, es un paso más adelante en el calendario.
Cuando llegue, va a una máquina alquilada con n8n y el código juntos, no a n8n como
servicio: así el puente por línea de comandos no se toca. Contratar n8n en la nube
obligaría a rehacer ese puente como servicio web abierto a internet.
**Se revisa si**: empieza la medición de verdad, o esta máquina deja de aguantar.

## 2026-09-08 — n8n le habla a nuestro código por línea de comandos

**Contexto**: n8n corre en JavaScript y las piezas propias están en Python. Había que
decidir cómo se hablan, y la respuesta condiciona dónde puede correr n8n.
**Alternativas**: montar nuestro código como un servicio web al que n8n le pregunta, lo
que pide una dependencia nueva, un puerto abierto y algo que lo mantenga vivo. O
reescribir la lógica dentro de los nodos, que tira las pruebas y rompe la decisión de
que el buscador de huecos va como código propio y probado.
**Elegido**: línea de comandos. n8n manda un JSON por la entrada y recibe otro por la
salida. Sin servidor, sin puerto y sin dependencias nuevas. Es `src/cli.py`, con dos
comandos: `procesar` y `peticion`.
**Costo aceptado**: n8n tiene que correr en la misma máquina que el código. Si algún día
se muda a la nube, esto hay que rehacerlo como servicio web. Se acepta porque el
laboratorio es local y porque la alternativa cuesta hoy y quizá nunca haga falta.
**Consecuencia**: el recorrido va en dos llamadas, no en una. La primera devuelve
`falta_agenda` con la fecha, n8n va a buscar la agenda al calendario, y vuelve a llamar.
Es así porque hasta que no se lee el correo no se sabe de qué día traer la agenda.
**Se revisa si**: n8n pasa a correr en otra máquina o en la nube.

## 2026-09-08 — Un cliente externo nunca lleva número de habitación

**Contexto**: en los mensajes reales aparecía `Julia #2 (External)`, y se había dado por
bueno que la almohadilla era siempre habitación. Eso hacía que un externo pudiera llevar
las dos cosas.
**Elegido**: son excluyentes. O habitación, o `(Ext)`, nunca las dos. Confirmado por
James. El número que acompaña a ese externo no es una habitación; la hipótesis es que
sean dos personas, porque esa reserva ocupa las dos salas a la misma hora con el mismo
número de INV, pero no está confirmado y el sistema no lo interpreta.
**Costo aceptado**: si la IA no consigue sacar la habitación de un huésped alojado, ese
cliente sale como externo en la petición.
**Se revisa si**: Egi dice qué es ese número.


---

<!-- Decisiones nuevas al final -->
