# Peticiones de prueba

Las veinte peticiones reales **anonimizadas** de la fase 1, paso 6.

Antes de que un correo entre acá se le cambian nombre, mail y teléfono. Son
datos de personas y la cuenta del laboratorio es personal.

Datos reales sin anonimizar van en `datos-reales/`, que está en el `.gitignore`
y no se commitea nunca.

## Cómo es cada pedido

Un `.yaml` por pedido, con tres cosas:

- `hilo` — el correo o la conversación, ya anonimizada.
- `recibido` — el día en que entró el correo (`AAAA-MM-DD`). Hace falta para que
  «el jueves» se entienda como se entendía ese día. Si falta, se toma hoy.
- `espera` — lo que sacaría una persona: `salida`, `idioma`, `habitacion`,
  `duracion`, `fecha`, `franja`, `personas`. Solo se compara lo que esté anotado.

## Cómo se mide

Con n8n andando y el flujo «Cal Reiet - probador de lecturas» encendido:

    python src/probador.py

Cada pedido pasa por la misma IA y las mismas instrucciones que el recorrido del
buzón, y sale una línea por pedido: bien, o qué campo falló y qué leyó en su
lugar. No manda correos ni toca la hoja. Cada pedido gasta una lectura de la IA.
