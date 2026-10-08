# Mensaje para el cliente (borrador: tú decides si lo envías)

Pega el texto de abajo en WhatsApp con el enlace de la vista previa. No afirma nada que el sitio no cumpla y pide **solo** lo indispensable. El sitio **no está publicado**.

## Texto

> Hola. Ya está lista la vista previa de la página de Comercializadora Robles (todavía no está publicada):
> [ENLACE DE LA VISTA PREVIA]
>
> Tiene su lista de productos (202), buscador y «Mi lista» para mandar el pedido por WhatsApp. Te pido solo tres cosas para terminarla:
>
> 1. **Precios.** En las capturas de la lista no venía la columna de precio. Para cada producto: monto, si incluye IVA y hasta qué fecha vale. Sin eso la página dice «te damos el precio por WhatsApp».
> 2. **Confirmar estos datos:** Cloralex de 750 ml · varilla en pulgadas · sellador Del Toro (¿es el mismo de 18 kg?) · pegapiso Ade1000 · picos y palas Truper.
> 3. **Fotos** de los productos que más vendes (cemento, varilla, carretillas, herramienta), tomadas por ustedes con luz de día y fondo liso.
>
> Lo del dominio (.com, .net o .mx) no depende de ti: reviso cuál está disponible y te aviso.
> También te dejo lo necesario para abrir la página de Facebook.

## Lo que se hace con la respuesta

| Si responde | Se hace | Dónde |
|---|---|---|
| Precios | Se cargan con unidad, IVA y vigencia | `datos/catalogo.csv` o `herramientas/editor-catalogo.html` |
| Supuestos | Se corrige el nombre o se quita la nota | `datos/catalogo.csv` |
| Fotos | Se guardan como `<id>.webp` | `src/img/productos/` |

Luego `python3 scripts/build.py` y se manda la vista previa corregida (una sola ronda de cambios).
