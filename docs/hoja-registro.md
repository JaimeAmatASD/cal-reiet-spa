# La hoja de registro

Una fila por pedido. Es el instrumento de medición de la fase 1: el sistema lee el
buzón y anota, sin tocar la operación. De esta hoja salen los tres números con los que
se decide si el proyecto sigue: **cuántos pedidos entran**, **cuántos se caen** y
**cuánto se tarda en contestar**.

Las columnas no se cambian a la ligera: la hoja las tiene fijas y el reporte semanal
las lee por nombre.

## La fila de encabezado

Se pega tal cual en la primera fila de la hoja, en este orden:

```
pedido	entrado_en	leido_en	canal	idioma	cliente	habitacion	duracion	fecha	franja	personas	preferencia	lectura	falta	a_confirmar	accion	motivo	estado	respondido_en	desenlace	nota
```

## Qué es cada columna

### Las que llena el sistema

| Columna | Qué lleva |
|---|---|
| `pedido` | El número del hilo de correo. Es la llave: nunca se repite, y sirve para volver al correo original |
| `entrado_en` | Cuándo llegó el pedido |
| `leido_en` | Cuándo lo leyó el sistema. La distancia entre estas dos dice cuánto tarda la máquina |
| `canal` | Por dónde entró: buzón, formulario, telegram |
| `idioma` | En el que escribió el cliente |
| `cliente` | Su nombre |
| `habitacion` | Vacío si no se aloja en el hotel |
| `duracion` | Minutos que pidió |
| `fecha` | El día que pidió |
| `franja` | Mañana o tarde |
| `personas` | Para cuántas |
| `preferencia` | De sexo del terapeuta, si la dijo |
| `lectura` | Cómo salió la lectura del correo: `completo`, `incompleto` o `derivar` |
| `falta` | Qué datos no dio el cliente |
| `a_confirmar` | Qué datos dedujimos nosotros y hay que confirmarle |
| `accion` | Qué hizo el sistema con el pedido: derivar, borrador, elegir_hora, sin_hueco |
| `motivo` | Por qué se derivó, cuando se derivó |
| `estado` | Arranca en `SOLICITADA` y de ahí lo mueve una persona |

### Las que llena una persona, a mano

El sistema las deja vacías y no las vuelve a tocar.

| Columna | Qué lleva |
|---|---|
| `respondido_en` | Cuándo salió la respuesta al cliente. Con `entrado_en` da el número que quiere Petra: cuánto se tarda en contestar |
| `desenlace` | REALIZADA, CAÍDA, CANCELADA o SIN COBERTURA. Es lo que dice cuántos se pierden |
| `nota` | Cualquier cosa que haga falta explicar |

La columna `estado` usa el vocabulario cerrado del proyecto: SOLICITADA, EN HOLD,
ASIGNADA, CONFIRMADA, REALIZADA, CAÍDA, CANCELADA, SIN COBERTURA. En la fase 1 se mueve
a mano; en la fase 5 la mueve el sistema.

## Cuando el cliente vuelve a escribir

Una fila por pedido, no por correo. Si el cliente contesta en la misma conversación, el
pedido se vuelve a leer entero y **su fila se pone al día**: lo que antes faltaba ahora
puede estar, y la lectura pasa de `incompleto` a `completo`. No se abre otra fila.

Al ponerla al día **no se pisa** lo que es de la persona que lleva la reserva: `estado`,
`respondido_en`, `desenlace` y `nota`. `entrado_en` tampoco cambia: es la hora del
primer correo de la conversación, no la del último.

Queda un caso sin cubrir: si la conversación empezó como una pregunta suelta y después
se volvió reserva, `estado` queda vacío, porque solo se escribe al crear la fila. Hay
que ponerle `SOLICITADA` a mano.

## Lo que la hoja NO guarda, a propósito

- **El correo y el teléfono del cliente.** Para contestarle está el buzón; para contar
  pedidos no hacen falta. Una hoja que se comparte es peor sitio para guardarlos que el
  buzón del que salieron. El número de hilo lleva de vuelta al correo original.
- **Nada de una consulta que menciona salud.** Esa fila lleva el número de hilo, cuándo
  entró, el canal y que se derivó por salud. Ni el nombre, ni qué pidió, ni el idioma.
  Son datos de categoría especial y el único sitio donde pueden quedarse es el buzón.
  Ver `docs/contrato-lectura.md`.

## Pendiente de decidir

- Si Egi necesita ver el correo del cliente en la hoja para trabajar cómoda. Hoy no se
  escribe. Si hiciera falta, se agrega una columna y se anota por qué.
