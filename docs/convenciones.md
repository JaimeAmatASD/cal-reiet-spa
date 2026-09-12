# Convenciones de los mensajes

Los formatos exactos de lo que hoy se manda a mano al grupo de terapeutas y del parte
del día siguiente. El sistema tiene que producir esto mismo: el equipo ya lee estos
bloques de un vistazo, y cambiarles la forma cuesta más de lo que vale.

Salieron de leer los mensajes reales del grupo de septiembre de 2026, no de una
plantilla. **Los nombres de los ejemplos están cambiados. Los formatos son literales.**

---

## La petición

Cinco líneas. La segunda solo aparece si el cliente pidió preferencia.

```
PETICIÓN A Espera de pago
Terapeuta Mujer
Holistic 60`
Laura Prats (Ext)
Wednesday, 9 September⋅12:15 – 13:15
```

Línea por línea:

1. **Encabezado.** Dice el estado de cobro. Se han visto dos formas: `Petición` a secas
   y `PETICIÓN A Espera de pago`. Qué decide cuál no está resuelto — ver los huecos del
   final.
2. **Preferencia de terapeuta.** Solo si la hay. Si el cliente no dijo nada esta línea
   no existe, y no se le pregunta.
3. **Tratamiento y duración.** Nombre, espacio, minutos, y una comilla detrás. La
   comilla son minutos.
4. **Cliente.** El nombre, y detrás **una de dos cosas, nunca las dos**: la habitación
   con almohadilla —`#3`— si está alojado, o `(Ext)` si es externo.
   **Un externo NUNCA lleva número de habitación** (confirmado por James, 8 de
   septiembre de 2026). Si ves un número junto a un externo, no es una habitación y no
   se interpreta como tal.
5. **Día y hora.** Día de la semana y fecha en inglés, el separador `⋅`, y la hora de
   principio y fin: `12:15 – 13:15`.

Tres reglas que no se ven en el bloque pero que salen de mirarlo:

- **La petición lleva hora exacta, de principio a fin.** Nunca sale con una franja ni
  con «por la tarde». Eso significa que la hora se elige ANTES de que la petición salga,
  y para elegirla hay que mirar la agenda.
- **No lleva sala.** Quién la da y dónde se resuelve después. La sala aparece en el parte.
- **Una petición por persona.** Un pedido para dos personas son dos peticiones con el
  mismo bloque, no una que diga «para dos». Cada una se lleva su terapeuta y su sala,
  y las dos van a la misma hora.

## La respuesta del terapeuta

Quien puede contesta **citando el bloque entero** y agregando `Puedo` debajo, a veces
con un emoji. No se contesta con un «yo» suelto: el bloque se repite.

## La confirmación

Egi devuelve el mismo bloque una tercera vez, con `Confirmación` en el encabezado:

```
Confirmación A espera de pago
Terapeuta Mujer
Holistic 60`
Laura Prats (Ext)
Wednesday, 9 September⋅12:15 – 13:15
```

El bloque es idéntico las tres veces. Es lo que permite seguir un pedido dentro de un
hilo de cien mensajes.

## El parte del día

Se manda la noche anterior. **Agrupado por terapeuta**, no por sala ni por hora.

```
### Treatments by Therapist – 8 September 2026

*Nadia*

* 11:00–12:30 — Holistic 90’ — Ingrid Sørbø #3 — *Room 1*
* 12:45–14:15 — DT 90’ — Elsa Riu #4 — *Room 1*
* 14:30–15:30 — Holistic 60’ — Laura Prats #2 (External) — *Room 1*

*Bea*

* 11:00–12:30 — Holistic 90’ — Tone Vik #3 — *Room 2*
* 14:30–15:30 — Holistic 60’ — Laura Prats #2 (External) — *Room 2*
* 16:00–17:30 — Reintegration 90’ — Dara Sallent (External) — *Room 2*
```

Cada línea: hora de principio y fin, tratamiento con duración, cliente con habitación
y con `(External)` si lo es, y la sala al final.

Un mismo cliente puede aparecer dos veces a la misma hora en dos salas distintas: eso
es un pedido para dos personas, no un error.

## Ojo con los detalles que rompen cosas

Los mensajes los escribe una persona a mano y no son consistentes. El sistema tiene que
**producir siempre la forma canónica de arriba**, pero cualquier cosa que los lea tiene
que aguantar estas variaciones, que están todas vistas en mensajes reales:

- **La comilla de los minutos no es siempre la misma.** En la petición se escribe con
  acento grave — `60\`` — y en el parte con comilla tipográfica — `90’`. Son dos
  caracteres distintos y a la vista son casi iguales.
- **El encabezado cambia de mayúsculas.** `PETICIÓN A Espera de pago` y
  `Confirmación A espera de pago`: la misma palabra con mayúscula y con minúscula.
- **Los saltos de línea se pierden.** Se ha visto `Holistic 90\`Sian (ext)` todo en una
  línea, sin espacio, donde deberían ser dos.
- **`(Ext)` y `(External)`** son lo mismo.

## Los títulos del calendario

Leídos del calendario real el 8 de septiembre de 2026. Hay un calendario por sala
—«Sala de masajes 1» y «Sala de masajes 2»— y los eventos los crea Egi a mano.

La forma, cuando se cumple:

```
[INV 2626] [*notas] <Tratamiento> <minutos>` <Cliente> <#habitación | (Ext)> con <Terapeuta> - <quién>
```

Ejemplos reales, con los nombres cambiados:

```
Holistic 90`Ingrid Sorbo #3 con Nadia- Egi
DT90`Elsa Riu #4 con Nadia -
INV 2626 Californian 90` Marido Dara Sallent con Bea - Egi
* notas Holistic 60` Laura Prats (Ext) con Bea - Egi
Foot Reflex 50`Elsa Riu #4 con Nadia - Egi
Holistic90' Tone Vik #3 con Bea -Ana
```

Lo que hay que saber:

- **El terapeuta va DENTRO del título**, detrás de un «con». Es lo que la fase 3 tiene
  que sacar de ahí y convertir en invitado del evento.
- **El número de INV va delante**, y solo en los externos. Coincide con el glosario.
  Se ha visto `INV`, `Inv` e `inv`.
- **Las dos peticiones de un mismo pedido comparten el número de INV.** Un masaje para
  dos personas son dos eventos, uno en cada sala, a la misma hora y con el mismo INV.
  El INV es del pedido, no de la persona.
- **`*notas` o `* notas`** delante marca que el evento tiene algo escrito en la
  descripción.
- **El final, detrás del guión, es quién lo gestionó.** A veces está vacío.
- **La comilla de los minutos tiene TRES formas**, no dos: acento grave en el
  calendario y en la petición, comilla tipográfica en el parte, y apóstrofo recto en
  algún título suelto. Y a veces no hay espacio antes del número: `DT90\`` y
  `Holistic90'`.

**La descripción del evento lleva datos personales.** Se ha visto un correo y un
teléfono de cliente ahí dentro. Cualquier cosa que lea el calendario tiene que quedarse
**solo con la hora de inicio, la hora de fin y la sala**, y tirar el resto en el
momento. El buscador de huecos no necesita nada más.

## Lo que sabemos del catálogo real

De los mensajes y del calendario salen **cinco tratamientos y tres duraciones**. NO es
el catálogo completo y no se carga en `config/tratamientos.yaml` hasta que Egi mande el
suyo. Queda acá como constancia de que existe y de cómo se escribe.

- Holistic — 60 y 90 minutos
- DT (Deep Tissue) — 90
- Californian — 90
- Reintegration — 90
- Foot Reflex — 50

**Ojo con los 40 minutos.** El catálogo provisional que hay hoy en el repositorio ofrece
40, 60 y 90. En dos días de calendario real no aparece ningún 40, y sí aparece un 50 que
el catálogo provisional no tiene. Los 40 son probablemente inventados.

## Lo que sabemos del horario

Solo lo que se deduce de dos días de mensajes, que no alcanza:

- El tratamiento más temprano visto empieza a las **10:00**.
- El más tardío termina a las **17:30**.

O sea que las salas abren a las 10:00 o antes, y cierran a las 17:30 o después. La hora
exacta no la sabemos y hace falta para buscar huecos.

<!-- Convenciones nuevas al final -->
