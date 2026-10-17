# Laboratorio 5: monitoreo IoT con Grafana e InfluxDB

## Arquitectura

El publicador Python genera medidas de temperatura, humedad e iluminancia y las
envía al broker Mosquitto por MQTT. El ingestor Python consume el topic
`lab5/sensores` y escribe los campos en InfluxDB. Grafana consulta el bucket
`iot_lab5` para mostrar la telemetría y evaluar alertas.

```text
publisher (Python) -> Mosquitto (MQTT) -> ingestor (Python) -> InfluxDB -> Grafana
```

Docker Compose inicia InfluxDB, Grafana, el publicador y el ingestor. Mosquitto
es un servicio del host y debe estar escuchando en el puerto `1883`.

## Puesta en marcha

Prerequisitos: Docker Engine con Docker Compose, Mosquitto escuchando en el
host en `1883` y un usuario/contraseña MQTT configurados en el broker.

```bash
cp .env.example .env
# Editar .env con credenciales fuertes y que coincidan con Mosquitto.
docker compose up -d --build
docker compose ps
docker compose logs -f grafana influxdb ingestor publisher
```

Para detener el laboratorio:

```bash
docker compose down
```

La configuración privada de InfluxDB y MQTT vive en `.env`; nunca publiques
ese archivo ni pegues sus valores en README, capturas o issues. El repositorio
incluye solamente `.env.example` con valores de reemplazo. `.gitignore` excluye
`.env`.

## Despliegue en una VM Linux

1. Instala Docker Engine y el plugin Docker Compose y habilita el servicio
   Mosquitto del host en el puerto `1883`.
2. Copia/clonea el repositorio a la VM, crea `.env` desde `.env.example` y
   reemplaza cada valor de ejemplo por uno propio.
3. Ejecuta `docker compose up -d --build` y confirma `docker compose ps`.
4. Abre TCP `3000` para Grafana solo a las redes necesarias. No expongas
   InfluxDB (`8086`) ni MQTT (`1883`) públicamente sin restricciones.
5. Cambia la contraseña inicial de Grafana inmediatamente después del primer
   inicio de sesión. Las credenciales y tokens no forman parte del repositorio.

El publicador/ingestor resuelven el broker mediante `host.docker.internal`;
Compose añade el mapeo host-gateway para Linux. El broker MQTT debe permitir
conexiones desde la red Docker y usar las mismas credenciales de `.env`.

## Grafana e InfluxDB

- Grafana: <http://57.156.67.207:3000>
- Datasource: `influxdb`, InfluxDB 2.x con Flux.
- URL interna: `http://influxdb:8086`.
- Organization: `unab`.
- Bucket: `iot_lab5`.
- El token se guarda como dato seguro del datasource; no incluirlo en capturas
  ni en el control de versiones.

El dashboard **Laboratorio 5 - IoT | Telemetría** está en:

<http://57.156.67.207:3000/d/lab5-iot-telemetry/laboratorio-5-iot-7c-telemetria>

## Informe

El PDF de dos páginas de informe técnico, seguido por el anexo fotográfico,
está en [Informe_Laboratorio_5.pdf](./Informe_Laboratorio_5.pdf). Incluye
arquitectura/protocolo, resultado de alerta, cobertura real de cuatro días,
huecos medidos y problemas observados durante la instalación.

Incluye:

1. Temperatura en °C, rango de 0 a 50.
2. Humedad en porcentaje, rango de 0 a 100.
3. Iluminancia en lux, rango de 0 a 1000.
4. Stat con la última temperatura recibida.

Los umbrales visuales son verde para valores normales, amarillo para
advertencia y rojo para condición crítica.

## Alerta de temperatura

La regla **Laboratorio 5 - Temperatura sobre 35 °C** consulta el último valor
de temperatura y entra en estado de alerta cuando supera 35 °C. Se evalúa cada
minuto, sin período de espera adicional (`for: 0s`).

Para probarla, se pausó temporalmente el publicador normal y se publicó por MQTT
una medición sintética de 40 °C. Grafana mostró el estado `Firing` (API:
`Alerting`) con valor `40`; después se restauró el publicador y la regla volvió
a `Normal` al llegar una lectura normal. El publicador queda activo al terminar
la prueba.

## Evidencias

Las capturas generadas durante la validación están en `evidencias/`:

- `lab5-datasource.png`: datasource y resultado de **Save & test**.
- `lab5-dashboard.png`: las tres series y el panel Stat.
- `lab5-dashboard-4-days.png`: las tres series en la ventana de cuatro días.
- `lab5-query-4-days.png`: consulta Flux y resultado en Grafana Explore para cuatro días.
- `Consulta_InfluxDB_4_dias.flux`: consulta Flux reproducible usada para graficar.
- `lab5-alert-normal.png`: regla en estado normal.
- `lab5-alert-firing.png`: regla activa con la medición de 40 °C.

La consulta de cuatro días encontró 3.559 muestras por campo entre
2026-10-13 02:53:35Z y 2026-10-17 02:53:35Z. Se observaron interrupciones de
20 min 38 s, 65 h 16 min 41 s, 41 min 51 s y 2 min 03 s. No se interpolan
mediciones ausentes; véase el informe complementario local.

## Repositorio

Código, README sin secretos, `.env.example`, PDF y evidencias:
<https://github.com/Lukgamer06/laboratorio-5-IoT>

## Seguridad

- Cambia la contraseña predeterminada de Grafana antes de un uso compartido o
  una exposición pública.
- Limita mediante firewall/NSG el acceso a Grafana (`3000`), InfluxDB (`8086`)
  y MQTT (`1883`).
- Mantén `.env` fuera del control de versiones y rota las credenciales si se
  han compartido.
- No hay un contact point ni una política de notificación configurados; la
  regla se evalúa en Grafana, pero no envía notificaciones externas.
