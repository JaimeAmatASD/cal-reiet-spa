# Referencias

Material previo y de consulta. "Hacé algo como esto".

---

## Del propio proyecto

- **Bot de disponibilidad en Node** — `github.com/JaimeAmatASD/whatsapp-availability-bot`.
  Escucha peticiones y responde si el horario encaja. Reutilizable: el reconocimiento de
  tratamiento, fecha y hora está probado contra los mensajes reales de la casa, y el
  modelo de disponibilidad como horario semanal fijo más excepciones por fecha es el que
  va a usar la fase 6.
  Dos correcciones al portarlo: usa noventa minutos de separación entre sesiones y la
  regla de la casa es quince; y reserva huecos sin liberarlos nunca.

- **Anexo de casos de uso** — dieciséis situaciones reales agrupadas por tipo. Sirve como
  criterio de aceptación de cada fase y como examen para cualquier proveedor externo.

- **Mensajes reales del grupo de terapeutas** (septiembre 2026) — de ahí salen los
  formatos de la petición, la confirmación y el parte del día, que están escritos en
  `docs/convenciones.md`. Es la fuente buena: son los mensajes que se mandan de verdad.

  Ojo: la hoja «Cal Reiet Masajes Asignación» del Drive tiene una plantilla de cuatro
  campos —Masajista, Tratamiento, Dia, Habitacion— que estuvo anotada acá como si fuera
  el formato de la petición. **No lo es.** La petición real tiene cinco líneas, encabezado
  con el estado de cobro y hora exacta de principio y fin. La plantilla de la hoja es
  otra cosa y no se usa como criterio.

  La misma hoja lleva tres columnas más — Terapeutas, Próximo y Contador — que son un
  turno rotativo entre terapeutas. Ese criterio de reparto no está en ningún documento
  del proyecto y no está decidido si se conserva. Hay que resolverlo antes de la fase 5.

- **Hojas de detalle mensual y facturas** (Google Drive) — de ahí sale el catálogo real
  de tratamientos y sus duraciones. Contienen nombres de huéspedes y datos fiscales:
  no se copian al repositorio, se leen y se anonimiza lo que haga falta.

## Externo

- Web del hotel: `calreiet.com`. Catálogo público de tratamientos, que es más corto que
  el catálogo real de la operación.

---

<!-- Referencias nuevas al final -->
