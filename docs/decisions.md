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

---

<!-- Decisiones nuevas al final -->
