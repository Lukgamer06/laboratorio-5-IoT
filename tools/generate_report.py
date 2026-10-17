from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidencias"
OUTPUT = ROOT / "Informe_Laboratorio_5.pdf"
GITHUB_URL = "https://github.com/Lukgamer06/laboratorio-5-IoT"
DASHBOARD_URL = (
    "http://57.156.67.207:3000/d/lab5-iot-telemetry/"
    "laboratorio-5-iot-7c-telemetria"
)

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
if not FONT_DIR.exists():
    FONT_DIR = Path("/usr/share/fonts/liberation-sans-fonts")
pdfmetrics.registerFont(TTFont("LabSans", str(FONT_DIR / "LiberationSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("LabSans-Bold", str(FONT_DIR / "LiberationSans-Bold.ttf")))

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="LabTitle",
        fontName="LabSans-Bold",
        fontSize=19,
        leading=22,
        textColor=colors.HexColor("#123353"),
        spaceAfter=2 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="LabSubtitle",
        fontName="LabSans",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#526170"),
        spaceAfter=4 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="LabHeading",
        fontName="LabSans-Bold",
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor("#176b78"),
        spaceBefore=2.5 * mm,
        spaceAfter=1.2 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="LabBody",
        fontName="LabSans",
        fontSize=8.4,
        leading=11,
        textColor=colors.HexColor("#202a35"),
        spaceAfter=1.6 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="LabSmall",
        fontName="LabSans",
        fontSize=7.2,
        leading=9,
        textColor=colors.HexColor("#526170"),
        spaceAfter=1 * mm,
    )
)
styles.add(
    ParagraphStyle(
        name="LabNode",
        fontName="LabSans-Bold",
        fontSize=7.1,
        leading=9,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#123353"),
    )
)
styles.add(
    ParagraphStyle(
        name="LabArrow",
        fontName="LabSans-Bold",
        fontSize=13,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#176b78"),
    )
)
styles.add(
    ParagraphStyle(
        name="LabCell",
        fontName="LabSans",
        fontSize=7.4,
        leading=9.2,
        textColor=colors.HexColor("#202a35"),
    )
)
styles.add(
    ParagraphStyle(
        name="LabCellHeader",
        fontName="LabSans-Bold",
        fontSize=7.4,
        leading=9.2,
        textColor=colors.white,
    )
)
styles.add(
    ParagraphStyle(
        name="LabCallout",
        fontName="LabSans",
        fontSize=8.2,
        leading=10.5,
        textColor=colors.HexColor("#202a35"),
    )
)
styles.add(
    ParagraphStyle(
        name="EvidenceCaption",
        fontName="LabSans",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#526170"),
        spaceBefore=1 * mm,
        spaceAfter=3 * mm,
    )
)


def p(text, style="LabBody"):
    return Paragraph(text, styles[style])


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#ccd5dc"))
    canvas.line(15 * mm, 11 * mm, letter[0] - 15 * mm, 11 * mm)
    canvas.setFont("LabSans", 7)
    canvas.setFillColor(colors.HexColor("#667583"))
    canvas.drawString(15 * mm, 7.5 * mm, "Laboratorio 5 · Informe técnico")
    canvas.drawRightString(letter[0] - 15 * mm, 7.5 * mm, str(document.page))
    canvas.restoreState()


def image(path, max_width, max_height):
    item = Image(str(EVIDENCE / path))
    scale = min(max_width / item.imageWidth, max_height / item.imageHeight)
    item.drawWidth = item.imageWidth * scale
    item.drawHeight = item.imageHeight * scale
    return item


story = [
    p("Laboratorio 5 · Telemetría IoT", "LabTitle"),
    p(
        "Informe técnico · Grafana + InfluxDB · mediciones verificadas "
        "el 17 de octubre de 2026 (UTC)",
        "LabSubtitle",
    ),
    p("Arquitectura y protocolo", "LabHeading"),
]

node = lambda text: p(text, "LabNode")
arrow = lambda: p("→", "LabArrow")
flow = Table(
    [[
        node("Sensores simulados<br/>Publicador Python"),
        arrow(),
        node("MQTT<br/>Mosquitto · lab5/sensores"),
        arrow(),
        node("Ingestor Python<br/>Paho MQTT"),
        arrow(),
        node("InfluxDB 2.7<br/>bucket iot_lab5"),
        arrow(),
        node("Grafana 13<br/>dashboard + alerta"),
    ]],
    colWidths=[24 * mm, 5 * mm, 25 * mm, 5 * mm, 24 * mm, 5 * mm, 25 * mm, 5 * mm, 27 * mm],
)
flow.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#edf7fa")),
            ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#edf7fa")),
            ("BACKGROUND", (4, 0), (4, 0), colors.HexColor("#edf7fa")),
            ("BACKGROUND", (6, 0), (6, 0), colors.HexColor("#edf7fa")),
            ("BACKGROUND", (8, 0), (8, 0), colors.HexColor("#edf7fa")),
            ("BOX", (0, 0), (0, 0), 0.7, colors.HexColor("#77a6b7")),
            ("BOX", (2, 0), (2, 0), 0.7, colors.HexColor("#77a6b7")),
            ("BOX", (4, 0), (4, 0), 0.7, colors.HexColor("#77a6b7")),
            ("BOX", (6, 0), (6, 0), 0.7, colors.HexColor("#77a6b7")),
            ("BOX", (8, 0), (8, 0), 0.7, colors.HexColor("#77a6b7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story += [
    flow,
    Spacer(1, 2 * mm),
    p(
        "El publicador Python genera temperatura (°C), humedad (%) e "
        "iluminancia (lux) cada 30 segundos. Publica JSON en "
        "<b>lab5/sensores</b>; el ingestor suscrito transforma esos campos "
        "en puntos de la medición <b>environment</b>. Grafana consulta "
        "InfluxDB mediante Flux. Compose ejecuta InfluxDB, Grafana y ambos "
        "procesos Python; Mosquitto corre como servicio del host de la VM."
    ),
    p("Justificación del protocolo", "LabHeading"),
    p(
        "MQTT usa publish/subscribe: productores y consumidores quedan "
        "desacoplados; basta publicar al broker para que el ingestor reciba "
        "los mensajes sin modificar los sensores. Tiene bajo overhead para "
        "mensajes pequeños y periódicos y permite añadir consumidores. El "
        "proyecto usa QoS 1 para confirmar entrega al broker. InfluxDB está "
        "orientada a métricas indexadas en el tiempo; Flux filtra campos y "
        "agrega ventanas para las visualizaciones."
    ),
    p("Dashboard y alerta", "LabHeading"),
    p(
        "El dashboard <b>Laboratorio 5 - IoT | Telemetría</b> contiene tres "
        "series (temperatura, humedad e iluminancia) y un Stat con la última "
        "temperatura; refresca cada 10 s. Unidades/rangos: °C 0–50, % 0–100 y "
        "lux 0–1000. La regla consulta la última temperatura y alerta si "
        "supera <b>35 °C</b>; evalúa cada minuto, sin espera adicional."
    ),
]

callout = Table(
    [[
        p(
            "<b>Prueba:</b> se publicó por MQTT una muestra sintética de "
            "40 °C. Grafana cambió a <b>Firing</b> con valor 40; se restauró "
            "el publicador y la alerta volvió a <b>Normal</b> tras una lectura "
            "normal. El datasource confirmó: “datasource is working. "
            "3 buckets found”.",
            "LabCallout",
        )
    ]],
    colWidths=[170 * mm],
)
callout.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eaf6ed")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#37864b")),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story += [
    callout,
    Spacer(1, 2 * mm),
    p(
        f'Dashboard: <link href="{DASHBOARD_URL}" color="#176b78">'
        f"{DASHBOARD_URL}</link>",
        "LabSmall",
    ),
    p(
        f'Repositorio público: <link href="{GITHUB_URL}" color="#176b78">'
        f"{GITHUB_URL}</link>",
        "LabSmall",
    ),
    PageBreak(),
    p("Ventana de datos, instalación y entrega", "LabTitle"),
    p("Continuación · tiempos expresados en UTC", "LabSubtitle"),
    p("Ventana de cuatro días e integridad", "LabHeading"),
    p(
        "Consulta Flux con <b>range(start: -4d)</b>. Inicio: "
        "<b>2026-10-13 02:53:35Z</b>; fin: <b>2026-10-17 02:53:35Z</b>. "
        "Primer dato 02:53:44Z y último 02:53:24Z. Se encontraron "
        "<b>3.559 muestras por campo</b> en cada variable. Con publicaciones "
        "nominales cada 30 s se esperarían cerca de 11.520 por campo; los "
        "datos muestran cobertura parcial."
    ),
]

rows = [
    [p("Inicio (UTC)", "LabCellHeader"), p("Fin (UTC)", "LabCellHeader"), p("Duración", "LabCellHeader")],
    [p("13 oct 21:40:16", "LabCell"), p("13 oct 22:00:55", "LabCell"), p("20 min 38 s", "LabCell")],
    [p("13 oct 22:00:55", "LabCell"), p("16 oct 15:17:35", "LabCell"), p("<b>65 h 16 min 41 s</b>", "LabCell")],
    [p("16 oct 15:27:06", "LabCell"), p("16 oct 16:08:57", "LabCell"), p("41 min 51 s", "LabCell")],
    [p("17 oct 02:26:21", "LabCell"), p("17 oct 02:28:24", "LabCell"), p("2 min 03 s", "LabCell")],
]
gap_table = Table(rows, colWidths=[59 * mm, 59 * mm, 52 * mm], repeatRows=1)
gap_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#176b78")),
            ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#bdcbd3")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f7")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)
story += [
    gap_table,
    Spacer(1, 1 * mm),
    p(
        "Se contaron intervalos consecutivos mayores de 90 s. Los mismos "
        "huecos aparecen en las tres variables porque cada publicación "
        "transporta los tres campos.",
        "LabSmall",
    ),
    p("Problemas encontrados en la VM", "LabHeading"),
    p(
        "• Logs del ingestor registraron timeouts de escritura y fallos DNS "
        "temporales al resolver <b>influxdb</b>. Coinciden con interrupciones "
        "de escritura y el hueco principal de más de 65 h; luego se reanudó "
        "la ingestión."
    ),
    p(
        "• El datasource de Grafana tenía inicialmente URL incompleta "
        "(“URL must contain scheme and host”). Se configuró "
        "<b>http://influxdb:8086</b>, organization y bucket; Save &amp; Test "
        "quedó correcto."
    ),
    p(
        "• El contenedor del publicador figuraba activo aunque su proceso "
        "estaba parado. Se reinició para reanudar MQTT; al final todos los "
        "servicios estaban activos."
    ),
    p(
        "• No hay logs que acrediten error de docker build o instalación de "
        "paquetes. Los fallos comprobados fueron de red/DNS y proceso."
    ),
    p("GitHub y reproducción", "LabHeading"),
    p(
        f'Proyecto publicado: <link href="{GITHUB_URL}" color="#176b78">'
        f"{GITHUB_URL}</link>. La VM original no tenía metadatos Git; se "
        "armó una copia limpia que excluye <b>.env</b> y credenciales. "
        "El repositorio incluye Compose, publicador, ingestor, README, "
        "plantilla .env.example, informe y evidencias."
    ),
    p(
        "Arranque: copiar .env.example a .env, establecer secretos propios "
        "que coincidan con Mosquitto y ejecutar "
        "<b>docker compose up -d --build</b>. Mosquitto debe correr en el "
        "host. Los datos ausentes no se imputan.",
        "LabSmall",
    ),
    PageBreak(),
    p("Anexo · evidencia del dashboard de cuatro días", "LabTitle"),
    p(
        "La línea continua puede ocultar visualmente períodos sin muestras; "
        "la consulta Flux y la tabla de huecos del informe reflejan la "
        "cobertura real.",
        "LabSubtitle",
    ),
    image("lab5-dashboard-4-days.png", 180 * mm, 230 * mm),
    p("Dashboard con rango temporal Last 4 days y las tres variables.", "EvidenceCaption"),
    PageBreak(),
    p("Anexo · conexión y consulta", "LabTitle"),
]

pair = Table(
    [[
        image("lab5-datasource.png", 83 * mm, 112 * mm),
        image("lab5-query-4-days.png", 83 * mm, 112 * mm),
    ]],
    colWidths=[87 * mm, 87 * mm],
)
pair.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
captions = Table(
    [[
        p("Datasource: Save &amp; Test confirma conexión y buckets.", "EvidenceCaption"),
        p("Grafana Explore: consulta Flux con ventana de cuatro días.", "EvidenceCaption"),
    ]],
    colWidths=[87 * mm, 87 * mm],
)
story += [Spacer(1, 12 * mm), pair, captions, PageBreak(), p("Anexo · prueba de alerta", "LabTitle")]

alerts = Table(
    [[
        image("lab5-alert-normal.png", 83 * mm, 112 * mm),
        image("lab5-alert-firing.png", 83 * mm, 112 * mm),
    ]],
    colWidths=[87 * mm, 87 * mm],
)
alerts.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
alert_captions = Table(
    [[
        p("Regla en estado Normal tras recuperar telemetría.", "EvidenceCaption"),
        p("Regla Firing al recibir el valor controlado de 40 °C.", "EvidenceCaption"),
    ]],
    colWidths=[87 * mm, 87 * mm],
)
story += [Spacer(1, 12 * mm), alerts, alert_captions]

document = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=letter,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=12 * mm,
    bottomMargin=16 * mm,
    title="Informe Laboratorio 5 - Telemetría IoT",
)
document.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
