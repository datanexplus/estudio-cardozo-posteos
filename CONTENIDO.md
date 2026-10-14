# Cómo se arma el contenido de Estudio Cardozo

Este archivo es la guía que siguen las tareas programadas (y cualquiera que arme un lote a mano).
El manual de marca completo está en Claude Design: https://claude.ai/artifact/DtwikwBgPQJwyKGAoH8UvF

## El estudio

- Estudio contable familiar en Cipolletti, Río Negro, desde 1993. Abierto al público desde 2007.
- Azucena Cardozo: contadora, fundadora y titular. Franco Cardozo: contador con formación en ingeniería en sistemas (no decir "ingeniero").
- Servicios: contabilidad, impuestos y sueldos. Foco en monotributistas y responsables inscriptos, más comercios con empleados. Clientes sobre todo en Río Negro y Neuquén.
- No ofrece inversiones ni cripto. No tiene sitio web (no usar estudiocardozo.com).
- Contacto: WhatsApp +54 9 299 570-8455 · Fray Santa María de Oro 985, Cipolletti · lunes a viernes de 9 a 15 h.

## Voz

- Voseo rioplatense, formal y cercano. Como un contador de confianza que explica, no un organismo que notifica.
- Una idea por pieza. Títulos de hasta 8 palabras, en oración normal (no Title Case).
- Sin jerga: si aparece un término técnico, se explica en la misma frase. El organismo es **ARCA** (ex AFIP).
- Emojis: uno o dos por texto, funcionales (📍 📲 📅). Nunca en las imágenes.
- Nunca prometer resultados impositivos ni usar miedo como gancho.
- Cierre de cada texto:
  ```
  ¿Dudas con tu caso? Escribinos por WhatsApp.
  📍 Fray Santa María de Oro 985, Cipolletti
  ```
- Hashtags: 3 a 5, siempre `#Cipolletti #AltoValle` + 1 a 3 del tema (`#Monotributo`, `#Sueldos`, `#IVA`, `#IngresosBrutos`, `#Neuquen`…).

## Qué se publica cada mes

Martes y jueves a las 10:15 (mejor horario de la cuenta), más recordatorios puntuales. Entre 8 y 10 posteos por mes.

| Cuándo | Qué | Plantilla |
|---|---|---|
| Día 1 (o primer hábil) | Calendario del mes: monotributo, IVA, IIBB Río Negro y Neuquén, Convenio Multilateral, F931/cargas sociales, autónomos | `calendario` |
| Primera semana | Sueldos de Comercio (CCT 130/75): aumento o escala vigente del mes | `dato` o `novedad` |
| 1 o 2 días hábiles antes de cada vencimiento fuerte | Recordatorio (monotributo, IVA, IIBB) | `dato` |
| Una vez por semana | Explicado simple: una duda frecuente | `explicado` (alternar fondo `light` y `dark`) |
| Cuando sale | Novedad normativa ya publicada en el Boletín Oficial | `novedad` |
| Fechas anuales | Recategorización (enero y julio), Ganancias y Bienes Personales (junio), aguinaldo (junio y diciembre), vacaciones, cierre de año | la que corresponda |

## Fuentes (verificar SIEMPRE antes de publicar un dato)

Fuentes oficiales, en este orden:
1. **ARCA — Agenda de vencimientos**: https://seti.afip.gob.ar/av/seleccionVencimientos.do y https://www.arca.gob.ar/vencimientos/
2. **Boletín Oficial** (prórrogas y resoluciones generales): https://www.boletinoficial.gob.ar
3. **Agencia de Recaudación Tributaria de Río Negro**: calendario anual por resolución (2026: Res. ART 889/2025).
4. **Dirección Provincial de Rentas de Neuquén**: calendario anual de Ingresos Brutos.
5. **Comisión Arbitral del Convenio Multilateral**: https://www.ca.gob.ar
6. **FAECYS** (escalas de Comercio, CCT 130/75): https://www.faecys.org.ar

Secundarias para cruzar (nunca como única fuente): Blog del Contador, Econoblog, Errepar.

Reglas:
- Un dato que no se pudo confirmar en una fuente oficial **no se publica**. Se deja afuera y se avisa en el resumen.
- Si el vencimiento cae feriado o fin de semana, pasa al día hábil siguiente: chequear feriados del año.
- Cada posteo con dato lleva la fuente en el texto ("Fuente: calendario de vencimientos de ARCA").

## Formato de un lote

Un lote por mes en `posteos/AAAA-MM/lote.json`. Las imágenes se generan con:

```
python3 tools/build.py posteos/AAAA-MM/lote.json
```

```json
{
  "mes": "2026-11",
  "posteos": [
    {
      "id": "01-calendario-noviembre",
      "fecha": "2026-11-02T10:15:00",
      "redes": ["instagram", "facebook", "gmb"],
      "template": "calendario",
      "kicker": "Vencimientos · Noviembre",
      "title": "Lo que vence en noviembre",
      "rows": [{"fecha": "20", "que": "Monotributo", "detalle": "Cuota mensual, todas las terminaciones"}],
      "nota": "Fuente: ARCA y ART Río Negro.",
      "cta": "Escribinos por WhatsApp",
      "texto": "Texto del posteo…",
      "hashtags": "#Monotributo #Cipolletti #AltoValle",
      "alt": "Descripción de la imagen para accesibilidad"
    }
  ]
}
```

Campos por plantilla:
- `explicado`: `theme` (light|dark), `kicker`, `title`, `intro`, `items` (máx. 3), `cta`.
- `dato`: `kicker`, `title`, `cifra`, `unidad`, `body`, `fuente`, `cta`.
- `calendario`: `kicker`, `title`, `rows` (máx. 6: `fecha`, `que`, `detalle`), `nota`, `cta`.
- `novedad`: `kicker`, `title`, `items` (Qué cambia / A quién afecta / Qué tenés que hacer), `fuente`, `cta`.
- `historia`: `frase` (opcional). Va como historia de Instagram y Facebook, sin texto.

En `items`, `intro` y `body` se puede usar `<b>…</b>` para negrita. Nada más de HTML.

## Publicación en Metricool

- Marca: Estudio Cardozo, blogId `7426547`, zona horaria America/Buenos_Aires.
- Imagen: `https://raw.githubusercontent.com/datanexplus/estudio-cardozo-posteos/main/posteos/AAAA-MM/<id>.png` (hacer push antes de programar).
- Instagram + Facebook en un solo posteo (`instagramData.type` POST o STORY). Google va aparte como `gmbData.type: "publication"`, solo texto y sin hashtags.
- Los lotes de las tareas programadas se cargan como **borrador** (`draft: true`) con fecha y hora: Franco los revisa y los programa desde Metricool.
