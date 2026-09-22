# Lecciones

Una línea por error: categoría y qué hacer distinto. Se agrega cuando algo sale mal, no
cuando sale bien — para eso está `decisions.md`.

Si un bug volvió a pasar, es porque su lección no estaba acá, o estaba escrita como
consejo en vez de como prohibición.

---

## Transversales

- **verificación** — Un test que nunca se vio fallar no prueba nada. Rojo antes que verde.
- **verificación** — Un agente que ablanda un test para que pase destruye el harness entero, y James no puede detectarlo leyendo el diff. Si falla: se arregla el código, o se pregunta.
- **verificación** — Gate verde no significa bueno en un sistema generativo. Protege la estructura, no el texto.
- **verificación** — Nunca declarar terminada una salida generada que nadie leyó. Si no se leyó, se dice "sin revisar".
- **verificación** — Un comando con tubería devuelve el código de salida del ÚLTIMO de la cadena, no del que importa. `npm install -g n8n | tail -25` dio «terminado bien» con la instalación rota y el error enterrado veinte líneas más arriba. Lo que se quiere verificar se redirige a un archivo y se mira el código de salida a mano.
- **verificación** — Que un servicio arranque y conteste no es que esté montado. n8n respondió 200 dos veces y el sistema lo mató por falta de memoria minutos después. Antes de dar por montado un servicio, mirar la memoria libre de la máquina, no solo que el puerto conteste.
- **agentes** — Código enredado frena a los propios agentes: se traban desenredando lo suyo y queman tokens. Los límites de complejidad son plata, no estética.
- **agentes** — Lo que tiene que cumplirse sí o sí va en config o en un hook. Una instrucción en prosa se cumple casi siempre, que no es lo mismo.
- **proceso** — Un boceto que nunca se declaró boceto termina en producción sin que nadie lo haya decidido. Declarar el nivel al empezar.
- **proceso** — Dos intentos y se frena. Un agente dando vueltas en un fix quema tokens y no se puede destrabar desde afuera.
- **contexto** — Lo que debe valer siempre va en CLAUDE.md; lo condicional en un rule o un skill. Si la voz vive en un skill, se prende y apaga sola.
- **contexto** — Un skill vive en un solo lugar. Duplicado en personal y en el repo, uno pisa al otro y editás el que no se carga.
- **contexto** — Los skills del proyecto van en `.claude/skills/`. Una carpeta `skills/` en la raíz no la escanea nadie.
- **contexto** — Un puntero a un skill o a un archivo que no existe es peor que no tener puntero: el agente inventa lo que diría y no hay señal de que falta. Los punteros se verifican cuando se escriben.
- **estructura** — Sin espacios en nombres de carpeta: rompen cualquier script que los toque.

## De este proyecto

- **datos** — Un hueco que se reserva y nunca se libera hace que el sistema rechace trabajo real por reservas fantasma, y falla en silencio. Todo lo que reserva algo necesita su contraparte que lo suelta. Ya pasó en el bot de disponibilidad y pasa hoy a mano en el calendario del hotel.
- **datos** — Al parsear títulos del calendario, `30'` y `60'` son duraciones, no días. `#9` es una habitación, no una fecha. Salió de estrellarse contra los datos reales.
- **datos** — La plantilla de una hoja no es el mensaje que se manda. La petición anotada en `references.md` tenía cuatro campos y ninguna hora; la real tiene cinco líneas, encabezado con el estado de cobro y hora de principio y fin. Pedir los mensajes reales antes de dar por buena una plantilla.
- **datos** — La comilla de los minutos no es siempre el mismo carácter: en la petición va con acento grave y en el parte con comilla tipográfica. A la vista son iguales. Los mensajes los escribe una persona a mano y nada de lo que hay en ellos es consistente: mayúsculas, saltos de línea y espacios cambian de un mensaje a otro.
- **datos** — Un dato confirmado de memoria no es un dato confirmado. Se dio por bueno que la almohadilla era siempre habitación; el calendario mostró el mismo caso escrito sin ella, y resultó que un externo nunca lleva habitación. Antes de cerrar una regla de parseo, mirar la MISMA reserva en las dos fuentes y preguntar por el caso que no encaja.

- **estructura** — n8n 2 trae apagados de fábrica el paso que ejecuta un comando y el que vigila archivos. Justo el primero es el puente con nuestro código. No avisa al arrancar: falla después, al abrir el flujo, diciendo que no reconoce el paso. Lo que un programa trae desactivado por seguridad se comprueba ANTES de diseñar encima.
- **verificación** — `pkill -f` con un patrón que aparece en el propio comando mata la orden que lo lanzó. El reinicio se dio por hecho y n8n había quedado caído. Al matar por patrón, comprobar después que lo que querías levantar está levantado. Volvió a pasar el 2026-09-13 con `kill $(pgrep -f "n8n start")`: el `pgrep` se encontró a sí mismo y la orden se cortó a la mitad, antes de la copia de seguridad. Sacar el número de proceso en una orden y matarlo en otra.
- **estructura** — n8n 2 vacía `Buffer` dentro de las expresiones `{{ }}`. `Buffer.from(...)` falla y el trozo sale como texto vacío, sin error a la vista: el comando mandó nada y nuestro código contestó «no es un JSON válido». Dentro de n8n se usa su propia función, `.base64Encode()`. Lo que anda en Node suelto no se da por bueno dentro del sandbox de n8n: se mira la vista previa del comando ya resuelto.
- **datos** — El paso de Gmail que trae un hilo, en modo simplificado, trae remitente, asunto y un resumen, pero no el texto. Además entrega un ítem por mensaje, no un hilo con lista de mensajes. El paso siguiente buscaba esa lista, no la encontró y armó un hilo vacío: el modelo leyó nada y todo salió «derivar», sin un error. Se pide el correo completo y el texto se saca de cada parte. Un «derivar» con todos los campos vacíos es síntoma de entrada vacía, no de un correo raro.
- **estructura** — Un flujo de n8n escrito a mano con un nombre de parámetro equivocado (`calendarId` en vez de `calendar`) se importa sin quejarse y deja el casillero vacío. Los flujos se exportan desde n8n; no se escriben a mano.
- **verificación** — Gemini decía «demasiadas consultas» y la causa real, más abajo en el mismo error, era «se acabó el saldo». Esperar o espaciar las pruebas no habría arreglado nada. El título de un error no es el diagnóstico: se lee el mensaje entero antes de proponer una salida.
- **agentes** — n8n lanzado como tarea de fondo de la sesión de Claude se apaga cuando la máquina anda corta de memoria, porque la sesión corta sus tareas. Se lanza aparte, desprendido de la sesión (`setsid nohup`), o lo arranca James en su propia terminal.
- **datos** — Antes de plantear una duda para Egi, buscarla en `convenciones.md`. Se estuvo por preguntar en qué idioma va la petición al grupo y ya estaba escrito: siempre en inglés.
- **estructura** — En n8n, un paso que devuelve cero cosas frena el recorrido sin error: la corrida figura «terminada bien» y no pasa nada más. Las agendas de las salas vacías ese día cortaban el flujo antes de decidir y de anotar la fila, justo el caso en que hay hueco. Los pasos que pueden venir vacíos se marcan para seguir igual (`alwaysOutputData`). Una corrida «bien» se confirma mirando hasta qué paso llegó, no el estado.
- **estructura** — En n8n, dos ramas que salen del mismo paso no corren a la par: termina todo el recorrido por la primera antes de empezar la segunda. Las agendas de las dos salas estaban en ramas paralelas y, una vez que la primera dejó de cortarse, la decisión salió leyendo solo la sala 1, sin error (el paso siguiente toma la sala que falta como vacía). Lo que tiene que juntarse antes de seguir va en fila, y los pasos de más adelante se marcan para correr una sola vez (`executeOnce`).

<!-- completar: los errores que te hagan perder una tarde -->

---

## Categorías en uso

`verificación` · `agentes` · `proceso` · `contexto` · `estructura` · `datos`
