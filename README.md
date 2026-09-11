# Cal Reiet — gestor de reservas del spa

Automatización de la gestión de reservas de tratamientos del departamento de Wellbeing
de Cal Reiet.

## Estado

Fase 1 — medir sin tocar nada. Entorno de laboratorio, sin contacto con la operación
real del hotel.

## Cómo correrlo

Para ver el recorrido completo —entra un correo, sale una petición para el grupo de
terapeutas— sin conectarse a nada:

```bash
source .venv/bin/activate
python ver_recorrido.py
```

Los correos y la agenda son inventados y la parte que entiende el correo viene grabada,
así que da siempre lo mismo. No manda nada ni toca ningún calendario.

La batería de pruebas:

```bash
pytest
```

### Cómo lo llama n8n

n8n corre en JavaScript y esto es Python. Se hablan por línea de comandos: entra un
JSON, sale un JSON. Dos comandos:

```bash
echo '{"pedido": {...}, "agenda": [...]}'                | python src/cli.py procesar
echo '{"ficha": {...}, "inicio": "12:15", "salas": [...]}' | python src/cli.py peticion
```

`procesar` dice qué hacer con un pedido. Si no le pasás la agenda del día, contesta
`falta_agenda` con la fecha: n8n la busca en el calendario y vuelve a llamar.

`peticion` escribe el bloque para el grupo de terapeutas, con la hora que eligió una
persona entre las libres.

Si algo falla sale `{"error": ...}` y el programa termina con código distinto de cero.

### Cómo arrancar n8n

n8n vive en esta misma máquina, al lado del código, porque el puente entre los dos es
por línea de comandos y eso pide que compartan máquina.

```bash
NODE_OPTIONS=--max-old-space-size=768 n8n start
```

El editor queda en http://localhost:5678. Pide Node 24.

**Antes de arrancarlo hay que cerrar Steam.** La máquina tiene 3,6 GB de memoria, n8n
pide unos 600 MB, y con Steam abierto no entra: el sistema lo mata a los pocos minutos.
Medido el 2026-09-08: con Steam cerrado, n8n se mantiene en 498 MB y quedan 1,1 GB
libres. El techo de memoria del comando está puesto a propósito, para que n8n se frene
solo en vez de que lo mate el sistema.

Mientras n8n corra en esta máquina, el sistema solo mide con la máquina encendida.

### El permiso de Google

n8n entra al buzón del laboratorio con un permiso de Google que está montado desde el
11 de septiembre de 2026. Dónde vive cada cosa:

- El proyecto se llama `cal-reiet-lab`, en la cuenta del laboratorio.
- La clave está **solo** dentro de n8n, en su almacén cifrado. No está en el
  repositorio y no tiene que estarlo.
- Por ahora el permiso es **solo de lectura del correo**. Ni enviar, ni borrar, ni
  modificar: el sistema redacta borradores y no envía.

Si alguna vez hay que rehacerlo, la dirección de retorno es exactamente
`http://localhost:5678/rest/oauth2-credential/callback`.

## Entorno de laboratorio

Todo el desarrollo ocurre contra una cuenta de Google de prueba, separada de las
cuentas del hotel. Los datos de clientes se anonimizan antes de entrar.

Copiá `.env.example` a `.env` y completá los valores. `.env` nunca se commitea.

## Documentación

- `docs/bitacora.md` — qué se hizo y cuándo
- `docs/decisions.md` — por qué se hizo así
- `docs/lessons.md` — errores que no hay que recometer
- `docs/convenciones.md` — el formato exacto de la petición, la confirmación y el parte
- `docs/contrato-lectura.md` — qué tiene que devolver la parte de IA, y qué se le pide
- `docs/references.md` — material previo y de consulta
