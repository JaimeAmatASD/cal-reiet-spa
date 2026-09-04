# Bitácora

Qué se hizo, cuándo, y qué sigue. Una entrada por sesión de trabajo cerrada.

Se escribe en idioma del dominio, no en técnico: dentro de tres meses esto se lee para
recordar qué pasó, no para revisar código.

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
terapeutas. Se escribió un anexo de casos de uso reales para acompañar el borrador de
requerimientos de Egi.

**Estado.** Terminado. El flujo está validado.

**Decisiones.** Telegram como canal interno, Google Calendar como fuente de verdad,
entorno de laboratorio separado de la operación. Ver `decisions.md`.

**Próximo paso.** Fase 1, paso 1: montar el entorno de laboratorio.

---

<!-- Entradas nuevas arriba de esta línea, más recientes primero -->
