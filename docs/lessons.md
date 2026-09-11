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

<!-- completar: los errores que te hagan perder una tarde -->

---

## Categorías en uso

`verificación` · `agentes` · `proceso` · `contexto` · `estructura` · `datos`
