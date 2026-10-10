# Meta Quest Homes — 22 entornos para exploración 3D

Colección documentada de **22 entornos Home atribuidos a Meta/Oculus**, extraídos como escenas estáticas **glTF 2.0 / GLB**, con archivos fuente, métricas técnicas y vistas renderizadas del interior y del exterior del modelo.

Pensada para inspección en herramientas 3D, análisis de composición espacial y comparación de entornos de realidad virtual.

> **Proyecto independiente, sin afiliación con Meta.** La colección corresponde a las 22 entradas del catálogo **Root** de Quest Home Switcher, versión `homes-v2.0.0`. Los paquetes utilizados son adaptaciones comunitarias de contenido atribuido a Meta/Oculus por ese catálogo. No se han verificado como APK históricos originales ni constituyen una lista exhaustiva de todos los Homes publicados por Meta.

## Galería

**Izquierda: interior. Derecha: exterior del modelo.** Las imágenes son renders estáticos en Blender de las escenas extraídas, no capturas del visor. En las vistas exteriores se ocultaron fondos envolventes y algunos elementos de fondo para mostrar la geometría principal.

### Classic Home · Cyber City · Winter Lodge · Desert Terrace · Space Station · Quest Dome

![Vistas interiores y exteriores de Classic Home, Cyber City, Winter Lodge, Desert Terrace, Space Station y Quest Dome](docs/images/Meta_Homes_Views_01.jpg)

### Mogu Hall · Crystal Atrium · Mountain Study · Studio · Blue Hill Gold Mine · Cascadia

![Vistas interiores y exteriores de Mogu Hall, Crystal Atrium, Mountain Study, Studio, Blue Hill Gold Mine y Cascadia](docs/images/Meta_Homes_Views_02.jpg)

### Futurescape · Lakeside Peak · Oceanarium · Paradiso · Polar Village · Storybook

![Vistas interiores y exteriores de Futurescape, Lakeside Peak, Oceanarium, Paradiso, Polar Village y Storybook](docs/images/Meta_Homes_Views_03.jpg)

### Abstraction · Bubbles · Rockquarry · Meta Horizon Terrace

![Vistas interiores y exteriores de Abstraction, Bubbles, Rockquarry y Meta Horizon Terrace](docs/images/Meta_Homes_Views_04.jpg)

Las cámaras son aproximaciones para inspección. Los materiales, la iluminación y los efectos pueden diferir de la experiencia original. Los renders utilizaron copias con texturas reducidas a un máximo de 512 px; esa reducción de las vistas previas no modifica los GLB distribuidos. Algunas caras exteriores no estaban diseñadas para verse desde fuera del entorno.

## Contenido y organización

Este paquete de documentación incluye el README, las cuatro láminas renderizadas y el catálogo en CSV y JSON. **Los modelos y las escenas fuente se descargan por separado**; los archivos binarios no están incluidos en el paquete de documentación.

| Ruta propuesta | Contenido |
|---|---|
| `README.md` | Presentación, galería e instrucciones |
| `docs/images/` | Cuatro láminas con 44 vistas |
| `catalog/catalog_and_metrics.csv` | Tabla de métricas para análisis |
| `catalog/catalog_and_metrics.json` | Métricas, hashes y reportes de extracción |
| `models/<id>.glb` | Modelo estático individual, añadido por separado |
| `sources/<id>_source_scene.zip` | Escena fuente individual, añadida por separado |

Los nombres `<id>` se indican en la tabla siguiente. El repositorio puede alojar la documentación y enlazar los binarios desde su sección de descargas; los enlaces de distribución deben añadirse cuando esos archivos estén publicados. Este README no presupone que los binarios ya estén disponibles en el repositorio.

## Entornos y métricas

La extracción registrada suma **9.249.150 triángulos** y **5.689.359 vértices**. Los recuentos corresponden a las instancias de geometría exportadas; no son una medición de draw calls ni de rendimiento en el visor.

| Home | Identificador | Triángulos | GLB (MB) |
|---|---|---:|---:|
| Abstraction | `abstraction` | 100,552 | 36.5 |
| Blue Hill Gold Mine | `blue-hill-gold-mine` | 675,264 | 344.1 |
| Bubbles | `bubbles` | 55,776 | 3.6 |
| Cascadia | `cascadia` | 355,529 | 229.4 |
| Classic Home | `classic-home` | 104,942 | 105.0 |
| Crystal Atrium | `crystal-atrium` | 312,029 | 264.3 |
| Cyber City | `cyber-city` | 584,044 | 145.1 |
| Desert Terrace | `desert-terrace` | 388,700 | 137.9 |
| Futurescape | `futurescape` | 542,405 | 180.6 |
| Lakeside Peak | `lakeside-peak` | 454,241 | 878.9 |
| Meta Horizon Terrace | `meta-horizon-terrace` | 520,347 | 500.7 |
| Mogu Hall | `mogu-hall` | 210,479 | 131.6 |
| Mountain Study | `mountain-study` | 225,018 | 251.8 |
| Oceanarium | `oceanarium` | 1,643,555 | 123.7 |
| Paradiso | `paradiso` | 175,246 | 151.3 |
| Polar Village | `polar-village` | 549,111 | 204.0 |
| Quest Dome | `quest-dome` | 251,308 | 58.3 |
| Rockquarry | `rockquarry` | 138,090 | 170.1 |
| Space Station | `space-station` | 376,181 | 79.7 |
| Storybook | `storybook` | 850,670 | 75.5 |
| Studio | `studio` | 420,067 | 241.9 |
| Winter Lodge | `winter-lodge` | 315,596 | 110.4 |

Consulta el [catálogo CSV](catalog/catalog_and_metrics.csv) o el [catálogo JSON](catalog/catalog_and_metrics.json) para los hashes SHA-256, nombres de paquetes, límites espaciales y reportes de carga.

## Abrir un modelo

### Blender

1. Descarga el archivo `<id>.glb` del entorno que quieras explorar.
2. Impórtalo mediante **File → Import → glTF 2.0**.
3. Inspecciona los objetos de la escena y sus materiales. Si el encuadre aparece desmesurado, selecciona la geometría principal: algunos entornos incluyen skyboxes o vértices auxiliares muy alejados.

Los GLB contienen las texturas utilizadas por la exportación. No necesitas un visor Quest ni acceso root para abrirlos.

### Unity

Utiliza un importador compatible con glTF 2.0 y con los materiales/extensiones presentes en el archivo. Después de importar, revisa transparencias, materiales unlit y orientación de las caras.

La exportación no crea automáticamente colliders, navegación, interacciones ni animaciones funcionales. Estos componentes requieren reconstrucción dentro del proyecto.

### Escena fuente

El archivo `<id>_source_scene.zip` conserva la escena interna extraída del paquete. **No es un proyecto de Blender ni de Unity listo para abrir.** Sirve para consultar los recursos originales de esa escena y desarrollar conversiones adicionales.

Los paquetes completos de extracción también pueden contener `apk_assets`, propiedades y metadatos auxiliares. Esos recursos adicionales no deben suponerse incluidos en el ZIP individual de escena fuente.

## Qué conserva la exportación

- Colocación de la geometría con transformaciones globales aplicadas.
- Coordenadas UV0/UV1, colores de vértice y texturas PNG utilizadas por el modelo.
- Tintes, modos de transparencia y marcas de doble cara cuando fueron interpretados por el extractor.
- Trazabilidad del paquete y de la escena mediante hashes y reportes del catálogo.

## Limitaciones conocidas

- **Escenas estáticas:** las animaciones no se convierten en pistas glTF reproducibles. Los recursos de animación, esqueletos, VAT y otros datos se conservan en los archivos fuente cuando existen.
- **Materiales aproximados:** los shaders originales y su iluminación no se reproducen exactamente. La mezcla aditiva no queda representada fielmente por los materiales glTF estándar.
- **Mapas empaquetados:** ciertas texturas normales/ORM requieren la interpretación específica del shader original.
- **Lightmaps:** los PNG derivados de lightmaps HDR incorporan exposición y mapeo tonal; no representan radiancia HDR sin procesar.
- **Normales:** su reconstrucción depende de la aplicación importadora.
- **Oceanarium y Storybook:** en sus exportaciones estáticas las texturas decodificadas se limitaron a 1024 px por dimensión máxima mediante remuestreo nearest para ajustarse a la memoria disponible. Las texturas comprimidas originales permanecen en las escenas fuente.
- **Elementos omitidos:** los reportes de carga identifican componentes clasificados como UI/gizmos u otros elementos no decodificados. Una exportación correcta no implica recuperación completa de la lógica del entorno.
- **Comparación histórica:** las fechas y versiones de estos paquetes adaptados no deben usarse como fechas de lanzamiento de los diseños originales.

## Validación y uso en investigación

Durante la extracción se comprobaron los hashes SHA-256 de los APK y las escenas internas contra el catálogo, las referencias de imágenes, los límites de buffers y accessors, los índices de triángulos y las longitudes de los GLB. El archivo agregado de los 22 modelos se recuperó posteriormente con el mismo SHA-256 y superó la comprobación CRC de sus entradas.

Estas comprobaciones evalúan integridad y consistencia de los archivos. **No demuestran equivalencia visual o funcional con la ejecución nativa en Quest.**

Para un análisis reproducible, registra el identificador del Home, el hash del GLB, la versión del importador y cualquier modificación posterior. Separa las observaciones de diseño de los artefactos de conversión. Los límites espaciales del catálogo incluyen fondos y geometría auxiliar; no equivalen a superficie transitable ni a dimensiones de una habitación.

## Procedencia técnica

- Catálogo de origen: [Quest Home Switcher — homes-v2.0.0](https://github.com/nikitat21/Quest-Home-Switcher/releases/tag/homes-v2.0.0), conjunto Root.
- Código de referencia: [Quest Home Switcher](https://github.com/nikitat21/Quest-Home-Switcher), revisión `6e6e74dc3a55faa1d0eb3815b994ece5f9982815`.
- Extractor de referencia: [Quest Home Editor](https://github.com/nikitat21/Quest-Home-Editor), revisión `fd95db7415fbf63032961db8df07dc5f01207831`.
- Decodificación ASTC: [ARM astc-encoder](https://github.com/ARM-software/astc-encoder), etiqueta `4.8.0`.
- Instantánea de extracción documentada: **4 de octubre de 2026**.

La extracción utilizó ajustes para referencias JSON numéricas representadas como cadenas, carga diferida de texturas y aplicación de transformaciones antes de exportar. El paquete independiente de herramientas contiene los scripts, el parche del extractor y las instrucciones de reproducción.

## Atribución y derechos

Los nombres, diseños, modelos, texturas y demás recursos de terceros mantienen sus respectivos titulares y condiciones. La inclusión en este catálogo no concede una licencia sobre los assets ni atribuye su autoría al mantenedor del repositorio. No se declara una licencia abierta global para el conjunto.

Conserva la atribución y las licencias de las herramientas de origen. La documentación distingue el trabajo de extracción y análisis del diseño de los entornos atribuidos a Meta/Oculus.
