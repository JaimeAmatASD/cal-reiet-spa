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
- **agentes** — Código enredado frena a los propios agentes: se traban desenredando lo suyo y queman tokens. Los límites de complejidad son plata, no estética.
- **agentes** — Lo que tiene que cumplirse sí o sí va en config o en un hook. Una instrucción en prosa se cumple casi siempre, que no es lo mismo.
- **proceso** — Un boceto que nunca se declaró boceto termina en producción sin que nadie lo haya decidido. Declarar el nivel al empezar.
- **proceso** — Dos intentos y se frena. Un agente dando vueltas en un fix quema tokens y no se puede destrabar desde afuera.
- **contexto** — Lo que debe valer siempre va en CLAUDE.md; lo condicional en un rule o un skill. Si la voz vive en un skill, se prende y apaga sola.
- **contexto** — Un skill vive en un solo lugar. Duplicado en personal y en el repo, uno pisa al otro y editás el que no se carga.
- **contexto** — Los skills del proyecto van en `.claude/skills/`. Una carpeta `skills/` en la raíz no la escanea nadie.
- **estructura** — Sin espacios en nombres de carpeta: rompen cualquier script que los toque.

## De este proyecto

- **datos** — Un hueco que se reserva y nunca se libera hace que el sistema rechace trabajo real por reservas fantasma, y falla en silencio. Todo lo que reserva algo necesita su contraparte que lo suelta. Ya pasó en el bot de disponibilidad y pasa hoy a mano en el calendario del hotel.
- **datos** — Al parsear títulos del calendario, `30'` y `60'` son duraciones, no días. `#9` es una habitación, no una fecha. Salió de estrellarse contra los datos reales.

<!-- completar: los errores que te hagan perder una tarde -->

---

## Categorías en uso

`verificación` · `agentes` · `proceso` · `contexto` · `estructura` · `datos`
