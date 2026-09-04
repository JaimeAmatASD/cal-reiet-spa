# Decisiones

Elecciones de peso con su razón. No errores (eso es `lessons.md`): bifurcaciones donde
se podía ir para dos lados y se eligió uno.

---

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

---

<!-- Decisiones nuevas al final -->
