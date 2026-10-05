# Peticiones de prueba

Las veinte peticiones de la fase 1, paso 6. Solo `real-01` es un pedido real
anonimizado; las `inventado-*` las escribimos nosotros, a pedido de James, para
no esperar a juntar los reales. Miden menos: quien las escribió sabe qué busca
el sistema.

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

## Cómo se prueba el recorrido entero

Con n8n andando y los flujos «Cal Reiet - del correo a la hoja» y «Cal Reiet -
probador del recorrido» encendidos:

    python src/probador_recorrido.py            # todos
    python src/probador_recorrido.py real-01    # uno solo

Cada pedido entra al recorrido del buzón como si hubiera llegado un correo: lo lee
la IA, se miran las agendas de las salas y se escribe la fila en la hoja del
laboratorio. Sale una línea por pedido: si llegó a la hoja y qué hizo el sistema, o
dónde se cortó. No manda correos. Cada pedido gasta una lectura de la IA.

Las filas de prueba llevan el número de pedido empezando por `prueba-`. Si el mismo
pedido se prueba otra vez, su fila se pone al día en vez de duplicarse. Hay que
borrarlas de la hoja antes de contar pedidos reales.
