"""
Script para poblar la base de datos con datos de prueba realistas.
Empresa de jardinería en Málaga capital y alrededores.
Ejecutar con el servidor activo: python seed.py
"""
import requests

BASE_URL = "http://localhost:8000"

# ── Clientes (60) ──────────────────────────────────────────────
CLIENTES = [
    # Málaga capital
    {"name": "Antonio Fernández Ruiz",        "phone": "612001001", "email": "antonio.fernandez@gmail.com",    "address": "Calle Larios 5, Málaga",                          "postal_code": "29005", "notes": "Jardín interior 80m². Riego automático instalado."},
    {"name": "Carmen Jiménez López",           "phone": "612001002", "email": "carmen.jimenez@hotmail.com",     "address": "Avenida de Andalucía 23, Málaga",                  "postal_code": "29006", "notes": "Terraza con jardineras. Visitas quincenales."},
    {"name": "Manuel García Moreno",           "phone": "612001003", "email": "manuel.garcia@gmail.com",        "address": "Calle Tejón y Rodríguez 12, Málaga",               "postal_code": "29007", "notes": "Patio andaluz con naranjos y limoneros."},
    {"name": "Isabel Romero Castillo",         "phone": "612001004", "email": "isabel.romero@outlook.com",      "address": "Paseo del Parque 3, Málaga",                       "postal_code": "29016", "notes": "Jardín comunitario. Contactar con presidenta."},
    {"name": "Francisco Ruiz Medina",          "phone": "612001005", "email": "francisco.ruiz@gmail.com",       "address": "Calle Granada 45, Málaga",                         "postal_code": "29015", "notes": "Requiere tratamiento fitosanitario mensual."},
    {"name": "María Dolores Vega Sánchez",     "phone": "612001006", "email": "lola.vega@gmail.com",            "address": "Calle Alcazabilla 8, Málaga",                      "postal_code": "29015", "notes": "Jardín histórico. Cuidado especial con palmeras."},
    {"name": "José Antonio Morales Torres",    "phone": "612001007", "email": "joseantonio.morales@yahoo.es",   "address": "Avenida Juan XXIII 67, Málaga",                    "postal_code": "29007", "notes": "Chalet con jardín 300m². Cliente VIP."},
    {"name": "Ana Belén Pérez Cortés",         "phone": "612001008", "email": "anabelen.perez@gmail.com",       "address": "Calle Ollerías 34, Málaga",                        "postal_code": "29012", "notes": "Piscina con jardín perimetral."},
    {"name": "Pedro Luis Martín Flores",       "phone": "612001009", "email": "pedro.martin@hotmail.com",       "address": "Calle Victoria 21, Málaga",                        "postal_code": "29012", "notes": "Jardín pequeño. Solo poda trimestral."},
    {"name": "Rosario González Herrera",       "phone": "612001010", "email": "rosario.gonzalez@gmail.com",     "address": "Plaza de la Merced 2, Málaga",                     "postal_code": "29012", "notes": "Macetones en terraza. Riego manual."},
    {"name": "Carlos Navarro Blanco",          "phone": "612001011", "email": "carlos.navarro@empresa.com",     "address": "Calle Molina Lario 15, Málaga",                    "postal_code": "29015", "notes": "Oficinas con jardín exterior 150m²."},
    {"name": "Lucía Ortega Delgado",           "phone": "612001012", "email": "lucia.ortega@gmail.com",         "address": "Avenida de Velázquez 89, Málaga",                  "postal_code": "29004", "notes": "Jardín nuevo, primer año de mantenimiento."},
    {"name": "Rafael Serrano Montoya",         "phone": "612001013", "email": "rafael.serrano@hotmail.com",     "address": "Calle Álamos 7, Málaga",                           "postal_code": "29012", "notes": "Urgencias siempre por teléfono."},
    {"name": "Cristina Muñoz Aguilar",         "phone": "612001014", "email": "cristina.munoz@gmail.com",       "address": "Calle Carretería 56, Málaga",                      "postal_code": "29008", "notes": "Alérgica a pesticidas. Solo productos ecológicos."},
    {"name": "Emilio Reyes Campos",            "phone": "612001015", "email": "emilio.reyes@outlook.com",       "address": "Paseo Marítimo Pablo Ruiz Picasso 12, Málaga",     "postal_code": "29016", "notes": "Terraza frente al mar. Plantas resistentes al salitre."},
    {"name": "Pilar Molina Guerrero",          "phone": "612001016", "email": "pilar.molina@gmail.com",         "address": "Calle Comedias 3, Málaga",                         "postal_code": "29008", "notes": "Patio interior con fuente."},
    {"name": "Andrés Castro Vargas",           "phone": "612001017", "email": "andres.castro@hotmail.com",      "address": "Avenida Cánovas del Castillo 34, Málaga",          "postal_code": "29016", "notes": "Jardín con césped artificial. Solo limpieza."},
    {"name": "Encarnación Gil Rubio",          "phone": "612001018", "email": "encarna.gil@gmail.com",          "address": "Calle San Juan 19, Málaga",                        "postal_code": "29015", "notes": "Mayores. Prefieren mañanas entre 9-12h."},
    {"name": "Joaquín Díaz Peña",              "phone": "612001019", "email": "joaquin.diaz@empresa.es",        "address": "Avenida Sor Teresa Prat 45, Málaga",               "postal_code": "29003", "notes": "Comunidad de vecinos. 4 zonas verdes."},
    {"name": "Marta Torres Gallego",           "phone": "612001020", "email": "marta.torres@gmail.com",         "address": "Calle Madre de Dios 8, Málaga",                    "postal_code": "29013", "notes": "Jardín mediterráneo. Lavanda y romero."},
    # Torremolinos
    {"name": "Juan Carlos Ramos López",        "phone": "612001021", "email": "juancarlos.ramos@gmail.com",     "address": "Avenida Palma de Mallorca 12, Torremolinos",       "postal_code": "29620", "notes": "Hotel boutique. Jardines exteriores 500m²."},
    {"name": "Svetlana Petrova González",      "phone": "612001022", "email": "svetlana.gonzalez@hotmail.com",  "address": "Calle Carmen 34, Torremolinos",                    "postal_code": "29620", "notes": "Apartamento con terraza. Habla español básico."},
    {"name": "Michael Roberts Fernández",      "phone": "612001023", "email": "michael.roberts@gmail.com",      "address": "Avenida Carlota Alessandri 67, Torremolinos",      "postal_code": "29620", "notes": "Residencia extranjero. Habla inglés. Jardín 200m²."},
    {"name": "Inmaculada Herrera Santos",      "phone": "612001024", "email": "inma.herrera@gmail.com",         "address": "Calle Casablanca 5, Torremolinos",                 "postal_code": "29620", "notes": "Chalet con piscina. Visitas mensuales."},
    {"name": "Lars Petersen Rodríguez",        "phone": "612001025", "email": "lars.petersen@outlook.com",      "address": "Calle La Nogalera 23, Torremolinos",               "postal_code": "29620", "notes": "Residencia nórdico. Prefiere plantas autóctonas."},
    {"name": "Dolores Campos Vera",            "phone": "612001026", "email": "dolores.campos@gmail.com",       "address": "Avenida Montemar 89, Torremolinos",                "postal_code": "29620", "notes": "Jardinería ornamental. Rosas y buganvillas."},
    {"name": "Fernando Rueda Molina",          "phone": "612001027", "email": "fernando.rueda@hotmail.com",     "address": "Calle Los Manantiales 12, Torremolinos",           "postal_code": "29620", "notes": "Urbanización privada. Acceso con tarjeta."},
    {"name": "Patricia Estévez Moreno",        "phone": "612001028", "email": "patricia.estevez@gmail.com",     "address": "Paseo Marítimo de Torremolinos 45, Torremolinos",  "postal_code": "29620", "notes": "Bar de playa con jardín trasero."},
    {"name": "Arturo Blanco Jiménez",          "phone": "612001029", "email": "arturo.blanco@empresa.com",      "address": "Calle Bulto 7, Torremolinos",                      "postal_code": "29620", "notes": "Residencia vacacional. Avisar antes de ir."},
    {"name": "Concepción Vargas Ortiz",        "phone": "612001030", "email": "conchi.vargas@gmail.com",        "address": "Avenida Playamar 33, Torremolinos",                "postal_code": "29620", "notes": "Comunidad 3 bloques. Jardines comunes."},
    # Churriana
    {"name": "Sebastián Alcántara Reina",      "phone": "612001031", "email": "sebas.alcantara@gmail.com",      "address": "Calle Real 15, Churriana, Málaga",                 "postal_code": "29004", "notes": "Finca agrícola con zona ornamental."},
    {"name": "Remedios Fuentes Morales",       "phone": "612001032", "email": "remedios.fuentes@hotmail.com",   "address": "Avenida Federico García Lorca 8, Churriana",       "postal_code": "29004", "notes": "Casa rural. Jardín rústico 400m²."},
    {"name": "Bartolomé Luque Carrasco",       "phone": "612001033", "email": "bartolome.luque@gmail.com",      "address": "Calle Arrayanes 23, Churriana, Málaga",            "postal_code": "29004", "notes": "Huerto y jardín ornamental mixto."},
    {"name": "Soledad Prados Guerrero",        "phone": "612001034", "email": "soledad.prados@outlook.com",     "address": "Camino de Churriana 45, Málaga",                   "postal_code": "29004", "notes": "Jardín con olivos centenarios."},
    {"name": "Nicolás Salas Bernal",           "phone": "612001035", "email": "nicolas.salas@gmail.com",        "address": "Calle Palmeral 3, Churriana, Málaga",              "postal_code": "29004", "notes": "Zona residencial nueva. Jardín en desarrollo."},
    {"name": "Amparo Benítez Córdoba",         "phone": "612001036", "email": "amparo.benitez@hotmail.com",     "address": "Calle Mosquera 17, Churriana, Málaga",             "postal_code": "29004", "notes": "Vivienda unifamiliar. Perros en el jardín."},
    {"name": "Gregorio Ponce Espinosa",        "phone": "612001037", "email": "gregorio.ponce@gmail.com",       "address": "Avenida del Aeropuerto 56, Málaga",                "postal_code": "29004", "notes": "Empresa logística. Zonas verdes perimetrales."},
    {"name": "Virtudes Carmona Hidalgo",       "phone": "612001038", "email": "virtudes.carmona@gmail.com",     "address": "Calle Jacarandas 9, Churriana, Málaga",            "postal_code": "29004", "notes": "Jardín con estanque. Precaución con niños."},
    {"name": "Leandro Marín Recio",            "phone": "612001039", "email": "leandro.marin@outlook.com",      "address": "Camino Viejo de Churriana 34, Málaga",             "postal_code": "29004", "notes": "Finca 1000m². Pinos y palmeras."},
    {"name": "Asunción Téllez Rojas",          "phone": "612001040", "email": "asuncion.tellez@gmail.com",      "address": "Calle Olivar 12, Churriana, Málaga",               "postal_code": "29004", "notes": "Jardín clásico andaluz. Azulejos y fuente."},
    # Guadalmar
    {"name": "Rodrigo Espejo Navarro",         "phone": "612001041", "email": "rodrigo.espejo@gmail.com",       "address": "Avenida Guadalmar 23, Málaga",                     "postal_code": "29004", "notes": "Urbanización Guadalmar. Jardín 250m²."},
    {"name": "Milagros Caballero Pedrosa",     "phone": "612001042", "email": "milagros.caballero@hotmail.com", "address": "Calle Marisma 7, Guadalmar, Málaga",               "postal_code": "29004", "notes": "Casa adosada. Jardín delantero y trasero."},
    {"name": "Esteban Montilla Ríos",          "phone": "612001043", "email": "esteban.montilla@gmail.com",     "address": "Calle Pinares 34, Guadalmar, Málaga",              "postal_code": "29004", "notes": "Zona residencial tranquila. Sin urgencias."},
    {"name": "Natividad Pacheco Soto",         "phone": "612001044", "email": "nati.pacheco@outlook.com",       "address": "Avenida del Mar 56, Guadalmar, Málaga",            "postal_code": "29004", "notes": "Primera línea. Jardín con palmeras datileras."},
    {"name": "Ignacio Serrato Medina",         "phone": "612001045", "email": "ignacio.serrato@empresa.com",    "address": "Calle Acacias 8, Guadalmar, Málaga",               "postal_code": "29004", "notes": "Chalet independiente. Piscina y jardín 400m²."},
    {"name": "Rosalía Guerrero Blanco",        "phone": "612001046", "email": "rosalia.guerrero@gmail.com",     "address": "Calle Flamencos 19, Guadalmar, Málaga",            "postal_code": "29004", "notes": "Jardín con aves. Evitar pesticidas."},
    {"name": "Abundio Crespo Aguilera",        "phone": "612001047", "email": "abundio.crespo@hotmail.com",     "address": "Paseo de Guadalmar 45, Málaga",                    "postal_code": "29004", "notes": "Jubilado. Disponible cualquier día."},
    {"name": "Estrella Vidal Fajardo",         "phone": "612001048", "email": "estrella.vidal@gmail.com",       "address": "Calle Gaviotas 3, Guadalmar, Málaga",              "postal_code": "29004", "notes": "Jardín pequeño. Riego por aspersión."},
    {"name": "Obdulio Ríos Peláez",            "phone": "612001049", "email": "obdulio.rios@gmail.com",         "address": "Urbanización Los Almendros 12, Guadalmar, Málaga", "postal_code": "29004", "notes": "Comunidad. Coordinar con administrador."},
    {"name": "Felisa Mendoza Corrales",        "phone": "612001050", "email": "felisa.mendoza@outlook.com",     "address": "Calle Helechos 27, Guadalmar, Málaga",             "postal_code": "29004", "notes": "Jardín botánico privado. Plantas exóticas."},
    # Carretera de Cádiz
    {"name": "Álvaro Suárez Domínguez",        "phone": "612001051", "email": "alvaro.suarez@gmail.com",        "address": "Carretera de Cádiz km 3, Málaga",                  "postal_code": "29006", "notes": "Taller mecánico con zona verde."},
    {"name": "Visitación Cantero Leal",        "phone": "612001052", "email": "visita.cantero@hotmail.com",     "address": "Carretera de Cádiz km 5, Málaga",                  "postal_code": "29006", "notes": "Residencia familiar. Jardín 180m²."},
    {"name": "Timoteo Herrero Baena",          "phone": "612001053", "email": "timoteo.herrero@gmail.com",      "address": "Urbanización El Pinillo, Carretera de Cádiz, Málaga","postal_code": "29006","notes": "Urbanización privada con vigilancia."},
    {"name": "Encarnita Palomo Trujillo",      "phone": "612001054", "email": "encarnita.palomo@gmail.com",     "address": "Carretera de Cádiz km 7, Málaga",                  "postal_code": "29006", "notes": "Restaurante con jardín. Visitas lunes."},
    {"name": "Severino Bravo Marcos",          "phone": "612001055", "email": "severino.bravo@empresa.com",     "address": "Polígono Industrial Carretera de Cádiz, Málaga",   "postal_code": "29006", "notes": "Nave industrial. Solo exterior."},
    {"name": "Adoración Calvo Montero",        "phone": "612001056", "email": "adoracion.calvo@gmail.com",      "address": "Urbanización Cerrado de Calderón, Málaga",         "postal_code": "29006", "notes": "Jardín 350m². Muy exigente con calidad."},
    {"name": "Primitivo Lara Exposito",        "phone": "612001057", "email": "primitivo.lara@hotmail.com",     "address": "Carretera de Cádiz km 9, Málaga",                  "postal_code": "29006", "notes": "Casa de campo. Acceso por camino de tierra."},
    {"name": "Purificación Garrido Cano",      "phone": "612001058", "email": "puri.garrido@gmail.com",         "address": "Avenida Juan Carlos I, Málaga",                    "postal_code": "29006", "notes": "Clínica dental. Jardín de entrada."},
    {"name": "Ildefonso Rubio Morillo",        "phone": "612001059", "email": "ildefonso.rubio@outlook.com",    "address": "Carretera de Cádiz km 11, Málaga",                 "postal_code": "29006", "notes": "Chalet con huerto y jardín ornamental."},
    {"name": "Consuelo Parejo Cintado",        "phone": "612001060", "email": "consuelo.parejo@gmail.com",      "address": "Urbanización Bahía de Málaga, Málaga",             "postal_code": "29006", "notes": "Urbanización frente al mar. 6 zonas verdes."},
]

# ── Empleados (19, 70% hombres = 13H + 6M) ────────────────────
EMPLEADOS = [
    # Hombres (13)
    {"name": "Miguel Ángel Torres Ruiz",    "phone": "623001001", "email": "miguel.torres@jardineria.com",   "role": "Encargado",  "speciality": "Gestión de equipos y planificación",    "hire_date": "2018-03-01"},
    {"name": "David Fernández Castillo",    "phone": "623001002", "email": "david.fernandez@jardineria.com", "role": "Jardinero",  "speciality": "Poda y mantenimiento general",          "hire_date": "2019-05-15"},
    {"name": "Javier Ruiz Moreno",          "phone": "623001003", "email": "javier.ruiz@jardineria.com",     "role": "Jardinero",  "speciality": "Sistemas de riego",                    "hire_date": "2019-09-01"},
    {"name": "Alejandro García López",      "phone": "623001004", "email": "alejandro.garcia@jardineria.com","role": "Jardinero",  "speciality": "Céspedes y siembra",                   "hire_date": "2020-02-10"},
    {"name": "Pablo Martín Sánchez",        "phone": "623001005", "email": "pablo.martin@jardineria.com",    "role": "Jardinero",  "speciality": "Tratamientos fitosanitarios",           "hire_date": "2020-06-01"},
    {"name": "Sergio Jiménez Vega",         "phone": "623001006", "email": "sergio.jimenez@jardineria.com",  "role": "Jardinero",  "speciality": "Poda de palmeras y árboles",           "hire_date": "2021-01-15"},
    {"name": "Raúl Morales Blanco",         "phone": "623001007", "email": "raul.morales@jardineria.com",    "role": "Jardinero",  "speciality": "Jardinería ornamental",                "hire_date": "2021-04-01"},
    {"name": "Iván Navarro Cortés",         "phone": "623001008", "email": "ivan.navarro@jardineria.com",    "role": "Jardinero",  "speciality": "Mantenimiento general",                "hire_date": "2021-07-01"},
    {"name": "Marcos Díaz Herrera",         "phone": "623001009", "email": "marcos.diaz@jardineria.com",     "role": "Jardinero",  "speciality": "Diseño paisajístico",                  "hire_date": "2022-03-01"},
    {"name": "Adrián Ramos González",       "phone": "623001010", "email": "adrian.ramos@jardineria.com",    "role": "Jardinero",  "speciality": "Riego tecnificado y automatización",   "hire_date": "2022-06-15"},
    {"name": "Óscar Serrano Campos",        "phone": "623001011", "email": "oscar.serrano@jardineria.com",   "role": "Jardinero",  "speciality": "Poda y setos",                         "hire_date": "2023-01-10"},
    {"name": "Rubén Ortega Delgado",        "phone": "623001012", "email": "ruben.ortega@jardineria.com",    "role": "Auxiliar",   "speciality": "Limpieza y mantenimiento básico",      "hire_date": "2023-06-01"},
    {"name": "Hugo Molina Reyes",           "phone": "623001013", "email": "hugo.molina@jardineria.com",     "role": "Auxiliar",   "speciality": "Apoyo en trabajos generales",          "hire_date": "2024-02-01"},
    # Mujeres (6)
    {"name": "Laura Sánchez Peña",          "phone": "623001014", "email": "laura.sanchez@jardineria.com",   "role": "Encargada",  "speciality": "Diseño floral y jardinería ornamental", "hire_date": "2019-03-01"},
    {"name": "Marta Gómez Vargas",          "phone": "623001015", "email": "marta.gomez@jardineria.com",     "role": "Jardinera",  "speciality": "Plantas aromáticas y medicinales",     "hire_date": "2020-09-01"},
    {"name": "Nuria Castro Fuentes",        "phone": "623001016", "email": "nuria.castro@jardineria.com",    "role": "Jardinera",  "speciality": "Jardines mediterráneos",               "hire_date": "2021-05-15"},
    {"name": "Beatriz Romero Aguilar",      "phone": "623001017", "email": "beatriz.romero@jardineria.com",  "role": "Jardinera",  "speciality": "Tratamientos ecológicos",              "hire_date": "2022-01-10"},
    {"name": "Silvia Muñoz Carrasco",       "phone": "623001018", "email": "silvia.munoz@jardineria.com",    "role": "Jardinera",  "speciality": "Mantenimiento de comunidades",         "hire_date": "2023-03-01"},
    {"name": "Elena Prados Lara",           "phone": "623001019", "email": "elena.prados@jardineria.com",    "role": "Auxiliar",   "speciality": "Apoyo general y atención al cliente",  "hire_date": "2024-04-01"},
]

# ── Tareas para marzo-abril 2026 (15) ──────────────────────────
TAREAS = [
    {"title": "Mantenimiento jardín mensual",         "description": "Poda de setos, corte de césped y revisión de riego", "date": "2026-03-18", "start_time": "09:00:00", "end_time": "12:00:00", "status": "pendiente",    "priority": "alta",  "client_idx": 0,  "employee_idxs": [1, 2], "notes": "Cliente VIP. Llevar herramienta de poda eléctrica."},
    {"title": "Instalación riego automatizado",       "description": "Instalar sistema de riego por goteo en jardín trasero", "date": "2026-03-19", "start_time": "08:00:00", "end_time": "14:00:00", "status": "pendiente",    "priority": "alta",  "client_idx": 6,  "employee_idxs": [2, 9], "notes": "Confirmar plano del jardín antes de ir."},
    {"title": "Poda de palmeras",                     "description": "Poda y limpieza de 4 palmeras datileras", "date": "2026-03-20", "start_time": "07:30:00", "end_time": "13:00:00", "status": "pendiente",    "priority": "alta",  "client_idx": 43, "employee_idxs": [5, 1], "notes": "Llevar arnés y equipo de altura."},
    {"title": "Tratamiento fitosanitario",            "description": "Aplicación de tratamiento contra cochinilla en jardín", "date": "2026-03-21", "start_time": "08:00:00", "end_time": "10:00:00", "status": "pendiente",    "priority": "media", "client_idx": 13, "employee_idxs": [4],    "notes": "Cliente solicita solo productos ecológicos."},
    {"title": "Siembra de césped",                    "description": "Resembrado de zonas deterioradas por el invierno", "date": "2026-03-24", "start_time": "09:00:00", "end_time": "13:00:00", "status": "pendiente",    "priority": "media", "client_idx": 11, "employee_idxs": [3, 12],"notes": "Temperatura mínima 15ºC para sembrar."},
    {"title": "Limpieza zonas verdes comunidad",      "description": "Mantenimiento trimestral de zonas comunes", "date": "2026-03-25", "start_time": "08:00:00", "end_time": "15:00:00", "status": "pendiente",    "priority": "media", "client_idx": 29, "employee_idxs": [6, 7, 12], "notes": "Coordinar con el administrador de fincas."},
    {"title": "Diseño jardín mediterráneo",           "description": "Replantación con lavanda, romero y plantas autóctonas", "date": "2026-03-26", "start_time": "09:00:00", "end_time": "14:00:00", "status": "pendiente",    "priority": "media", "client_idx": 19, "employee_idxs": [13, 15],"notes": "Traer catálogo de plantas para que elija el cliente."},
    {"title": "Revisión sistema de riego averiado",   "description": "Detectar y reparar fuga en ramal principal", "date": "2026-03-27", "start_time": "10:00:00", "end_time": "12:00:00", "status": "pendiente",    "priority": "alta",  "client_idx": 2,  "employee_idxs": [2],    "notes": "URGENTE. Cliente sin riego desde hace 3 días."},
    {"title": "Mantenimiento hotel Torremolinos",     "description": "Mantenimiento integral jardines hotel boutique", "date": "2026-04-02", "start_time": "07:00:00", "end_time": "14:00:00", "status": "pendiente",    "priority": "alta",  "client_idx": 20, "employee_idxs": [0, 1, 6],"notes": "Acceso por entrada de servicio. Pedir a recepción."},
    {"title": "Poda setos y arbustos",                "description": "Poda de formación de setos perimetrales", "date": "2026-04-03", "start_time": "09:00:00", "end_time": "13:00:00", "status": "pendiente",    "priority": "baja",  "client_idx": 51, "employee_idxs": [10],   "notes": "Herramienta eléctrica imprescindible."},
    {"title": "Plantación jardín nuevo",              "description": "Primera plantación en jardín de obra nueva", "date": "2026-04-07", "start_time": "08:00:00", "end_time": "15:00:00", "status": "pendiente",    "priority": "media", "client_idx": 34, "employee_idxs": [3, 14, 15], "notes": "Jardín nuevo. Llevar plano del proyecto."},
    {"title": "Control de malas hierbas finca",       "description": "Aplicación de herbicida y limpieza manual", "date": "2026-04-08", "start_time": "08:00:00", "end_time": "12:00:00", "status": "pendiente",    "priority": "baja",  "client_idx": 38, "employee_idxs": [7, 12], "notes": "Finca grande. Llevar mochila pulverizadora."},
    {"title": "Revisión anual jardín botánico",       "description": "Revisión completa y plan de mantenimiento anual", "date": "2026-04-09", "start_time": "10:00:00", "end_time": "13:00:00", "status": "pendiente",    "priority": "media", "client_idx": 49, "employee_idxs": [9, 14], "notes": "Plantas exóticas. Llevar guía de especies."},
    {"title": "Mantenimiento comunidad Guadalmar",    "description": "Visita mensual zonas verdes urbanización", "date": "2026-04-14", "start_time": "08:00:00", "end_time": "14:00:00", "status": "pendiente",    "priority": "media", "client_idx": 48, "employee_idxs": [6, 7, 11], "notes": "6 zonas verdes. Empezar por la entrada principal."},
    {"title": "Tratamiento preventivo primavera",     "description": "Abonado y tratamiento preventivo de plagas primaveral", "date": "2026-04-15", "start_time": "09:00:00", "end_time": "11:00:00", "status": "pendiente",    "priority": "baja",  "client_idx": 55, "employee_idxs": [4, 16], "notes": "Inicio de temporada de plagas. Tratamiento preventivo."},
]

# ── Ausencias de verano (pendientes de aprobar) ────────────────
AUSENCIAS = [
    {"employee_idx": 1,  "absence_type": "vacaciones", "start_date": "2026-07-01", "end_date": "2026-07-14", "reason": "Vacaciones verano - primera quincena julio"},
    {"employee_idx": 2,  "absence_type": "vacaciones", "start_date": "2026-07-15", "end_date": "2026-07-31", "reason": "Vacaciones verano - segunda quincena julio"},
    {"employee_idx": 3,  "absence_type": "vacaciones", "start_date": "2026-08-01", "end_date": "2026-08-14", "reason": "Vacaciones verano - primera quincena agosto"},
    {"employee_idx": 4,  "absence_type": "vacaciones", "start_date": "2026-08-15", "end_date": "2026-08-31", "reason": "Vacaciones verano - segunda quincena agosto"},
    {"employee_idx": 5,  "absence_type": "vacaciones", "start_date": "2026-07-01", "end_date": "2026-07-21", "reason": "Vacaciones verano 3 semanas"},
    {"employee_idx": 6,  "absence_type": "vacaciones", "start_date": "2026-08-03", "end_date": "2026-08-21", "reason": "Vacaciones verano"},
    {"employee_idx": 7,  "absence_type": "vacaciones", "start_date": "2026-07-06", "end_date": "2026-07-17", "reason": "Vacaciones con familia"},
    {"employee_idx": 8,  "absence_type": "vacaciones", "start_date": "2026-08-10", "end_date": "2026-08-28", "reason": "Vacaciones verano"},
    {"employee_idx": 9,  "absence_type": "vacaciones", "start_date": "2026-07-20", "end_date": "2026-08-07", "reason": "Vacaciones verano"},
    {"employee_idx": 10, "absence_type": "vacaciones", "start_date": "2026-08-03", "end_date": "2026-08-14", "reason": "Vacaciones verano"},
    {"employee_idx": 14, "absence_type": "vacaciones", "start_date": "2026-07-13", "end_date": "2026-07-24", "reason": "Vacaciones verano"},
    {"employee_idx": 15, "absence_type": "vacaciones", "start_date": "2026-08-17", "end_date": "2026-08-28", "reason": "Vacaciones verano"},
    {"employee_idx": 16, "absence_type": "vacaciones", "start_date": "2026-07-27", "end_date": "2026-08-07", "reason": "Vacaciones verano"},
    {"employee_idx": 17, "absence_type": "vacaciones", "start_date": "2026-08-03", "end_date": "2026-08-21", "reason": "Vacaciones verano"},
]

# ── Trabajos con incidencias (15) ──────────────────────────────
TRABAJOS_CON_INCIDENCIAS = [
    {
        "task_idx": 0,
        "started_at": "2026-03-18T09:05:00",
        "status": "completado",
        "notes": "Trabajo realizado correctamente. Seto en buen estado.",
        "checklist": [
            {"description": "Poda seto perimetral",         "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Corte de césped",              "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Revisión sistema de riego",    "is_done": True,  "has_incident": True,  "incident_notes": "Aspersor sector 3 obstruido. Sustituido en el acto."},
            {"description": "Recogida de residuos",         "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 3,
        "started_at": "2026-03-21T08:10:00",
        "status": "completado",
        "notes": "Tratamiento aplicado. Se detectó plaga más extensa de lo previsto.",
        "checklist": [
            {"description": "Inspección visual de plantas",   "is_done": True,  "has_incident": True,  "incident_notes": "Plaga de cochinilla extendida a 3 plantas adicionales no previstas."},
            {"description": "Aplicación de tratamiento",      "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Revisión de drenaje",            "is_done": True,  "has_incident": True,  "incident_notes": "Drenaje parcialmente bloqueado por raíces. Requiere intervención próxima visita."},
            {"description": "Informe al cliente",             "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 7,
        "started_at": "2026-03-27T10:15:00",
        "status": "completado",
        "notes": "Fuga localizada y reparada. Riego funcionando al 100%.",
        "checklist": [
            {"description": "Localización de la fuga",       "is_done": True,  "has_incident": True,  "incident_notes": "Fuga en T de unión principal. Tubo dañado por raíz de árbol cercano."},
            {"description": "Reparación del ramal",          "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Prueba de presión",             "is_done": True,  "has_incident": True,  "incident_notes": "Presión baja en sector 2. Se recomienda revisión de la bomba."},
            {"description": "Comprobación general",          "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 2,
        "started_at": "2026-03-20T07:35:00",
        "status": "incompleto",
        "notes": "Trabajo suspendido por viento fuerte. Reprogramar para día sin viento.",
        "checklist": [
            {"description": "Preparación equipo de altura",  "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Poda palmera 1",                "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Poda palmera 2",                "is_done": False, "has_incident": True,  "incident_notes": "Trabajo suspendido por rachas de viento superiores a 40km/h. Riesgo para el operario."},
            {"description": "Poda palmera 3 y 4",            "is_done": False, "has_incident": True,  "incident_notes": "Pendiente de reprogramar. Palmeras 3 y 4 sin podar."},
        ]
    },
    {
        "task_idx": 4,
        "started_at": "2026-03-24T09:10:00",
        "status": "completado",
        "notes": "Siembra completada. Riego de arranque aplicado.",
        "checklist": [
            {"description": "Preparación del terreno",       "is_done": True,  "has_incident": True,  "incident_notes": "Terreno más compactado de lo esperado. Necesitó escarificado adicional no presupuestado."},
            {"description": "Aplicación de sustrato",        "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Siembra de semillas",           "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Riego de arranque",             "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 5,
        "started_at": "2026-03-25T08:05:00",
        "status": "completado",
        "notes": "Limpieza general completada. Incidencia con vandalismo detectada.",
        "checklist": [
            {"description": "Zona 1 - entrada principal",    "is_done": True,  "has_incident": True,  "incident_notes": "Grafiti en muro de jardín. Notificado a la administración."},
            {"description": "Zona 2 - piscina comunitaria",  "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Zona 3 - aparcamiento",         "is_done": True,  "has_incident": True,  "incident_notes": "Alcorque de árbol dañado por vehículo. Requiere reposición de bordillo."},
            {"description": "Recogida y limpieza final",     "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 6,
        "started_at": "2026-03-26T09:20:00",
        "status": "completado",
        "notes": "Diseño aprobado por el cliente. Plantación completada.",
        "checklist": [
            {"description": "Presentación diseño al cliente", "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Preparación del terreno",        "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Plantación lavanda y romero",    "is_done": True,  "has_incident": True,  "incident_notes": "2 plantas de lavanda llegaron con raíz dañada. Sustituidas por romero. Cliente informado."},
            {"description": "Riego y abonado inicial",        "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 1,
        "started_at": "2026-03-19T08:15:00",
        "status": "incompleto",
        "notes": "Instalación parcial. Falta conexión a programador. Segunda visita necesaria.",
        "checklist": [
            {"description": "Trazado de tuberías",           "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Instalación goteros sector 1",  "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Instalación goteros sector 2",  "is_done": True,  "has_incident": True,  "incident_notes": "Presión insuficiente en sector 2. Requiere bomba de presión adicional no incluida en presupuesto."},
            {"description": "Conexión a programador",        "is_done": False, "has_incident": True,  "incident_notes": "Programador incompatible con instalación existente. Solicitar nuevo presupuesto."},
        ]
    },
    {
        "task_idx": 8,
        "started_at": "2026-04-02T07:10:00",
        "status": "completado",
        "notes": "Hotel satisfecho con el resultado. Contrato renovado.",
        "checklist": [
            {"description": "Jardín entrada hotel",          "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Piscina y zona relax",          "is_done": True,  "has_incident": True,  "incident_notes": "Palmera junto a piscina con síntomas de picudo rojo. Notificado a gerencia. Requiere tratamiento urgente."},
            {"description": "Zona restaurante exterior",     "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Parking y accesos",             "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 9,
        "started_at": "2026-04-03T09:05:00",
        "status": "completado",
        "notes": "Poda realizada. Seto en perfectas condiciones.",
        "checklist": [
            {"description": "Poda seto frontal",             "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Poda seto lateral derecho",     "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Poda seto lateral izquierdo",   "is_done": True,  "has_incident": True,  "incident_notes": "Nido de pájaros encontrado en el seto. Poda aplazada en esa zona hasta que el nido sea abandonado."},
            {"description": "Recogida de restos",            "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 10,
        "started_at": "2026-04-07T08:20:00",
        "status": "completado",
        "notes": "Jardín plantado según proyecto. Cliente muy satisfecho.",
        "checklist": [
            {"description": "Replanteo según proyecto",      "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Plantación árboles",            "is_done": True,  "has_incident": True,  "incident_notes": "Árbol de la esquina NE no entraba en el hoyo por tubería de agua. Reubicado 50cm al norte."},
            {"description": "Plantación arbustos",           "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Instalación riego provisional", "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 11,
        "started_at": "2026-04-08T08:10:00",
        "status": "completado",
        "notes": "Control completado. Finca en buen estado general.",
        "checklist": [
            {"description": "Tratamiento zona norte",        "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Tratamiento zona sur",          "is_done": True,  "has_incident": True,  "incident_notes": "Invasión de cañas en lindero sur. Requiere tratamiento específico de erradicación."},
            {"description": "Limpieza manual accesos",       "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Inspección perímetro",          "is_done": True,  "has_incident": True,  "incident_notes": "Valla perimetral dañada en tramo oeste. Notificado al propietario."},
        ]
    },
    {
        "task_idx": 12,
        "started_at": "2026-04-09T10:10:00",
        "status": "completado",
        "notes": "Revisión completa realizada. Plan anual entregado al cliente.",
        "checklist": [
            {"description": "Inventario de especies",        "is_done": True,  "has_incident": True,  "incident_notes": "3 plantas exóticas con signos de estrés hídrico. Revisar programación de riego."},
            {"description": "Estado sanitario general",      "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Revisión sistema de riego",     "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Elaboración plan anual",        "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 13,
        "started_at": "2026-04-14T08:05:00",
        "status": "completado",
        "notes": "Mantenimiento mensual completado sin incidencias graves.",
        "checklist": [
            {"description": "Zona 1 entrada",                "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Zona 2 piscina",                "is_done": True,  "has_incident": True,  "incident_notes": "Sistema de riego zona 2 desconfigurado por corte eléctrico. Reprogramado."},
            {"description": "Zonas 3, 4 y 5",               "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Zona 6 aparcamiento",           "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
    {
        "task_idx": 14,
        "started_at": "2026-04-15T09:05:00",
        "status": "completado",
        "notes": "Tratamiento preventivo aplicado correctamente.",
        "checklist": [
            {"description": "Inspección visual previa",      "is_done": True,  "has_incident": True,  "incident_notes": "Primeros indicios de pulgón en rosales. Tratamiento intensificado."},
            {"description": "Aplicación abono",              "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Tratamiento preventivo plagas", "is_done": True,  "has_incident": False, "incident_notes": None},
            {"description": "Informe cliente",               "is_done": True,  "has_incident": False, "incident_notes": None},
        ]
    },
]


def seed():
    print("🌱 Iniciando carga de datos de prueba...\n")

    # ── Clientes ───────────────────────────────────────────────
    print("👤 Creando 60 clientes...")
    ids_clientes = []
    for c in CLIENTES:
        r = requests.post(f"{BASE_URL}/clients/", json=c)
        if r.status_code == 201:
            ids_clientes.append(r.json()["id"])
            print(f"   ✅ {c['name']}")
        else:
            print(f"   ❌ {c['name']} — {r.status_code}")
            ids_clientes.append(None)

    # ── Empleados ──────────────────────────────────────────────
    print(f"\n👷 Creando {len(EMPLEADOS)} empleados...")
    ids_empleados = []
    for e in EMPLEADOS:
        r = requests.post(f"{BASE_URL}/employees/", json=e)
        if r.status_code == 201:
            ids_empleados.append(r.json()["id"])
            print(f"   ✅ {e['name']}")
        else:
            print(f"   ❌ {e['name']} — {r.status_code}")
            ids_empleados.append(None)

    # ── Tareas ─────────────────────────────────────────────────
    print(f"\n📅 Creando {len(TAREAS)} tareas...")
    ids_tareas = []
    for t in TAREAS:
        client_id    = ids_clientes[t["client_idx"]]
        employee_ids = [ids_empleados[i] for i in t["employee_idxs"] if ids_empleados[i]]

        if not client_id:
            print(f"   ⚠️  {t['title']} — cliente no disponible")
            ids_tareas.append(None)
            continue

        payload = {
            "title":        t["title"],
            "description":  t["description"],
            "date":         t["date"],
            "start_time":   t["start_time"],
            "end_time":     t["end_time"],
            "status":       t["status"],
            "priority":     t["priority"],
            "client_id":    client_id,
            "employee_ids": employee_ids,
            "notes":        t["notes"],
        }
        r = requests.post(f"{BASE_URL}/tasks/", json=payload)
        if r.status_code == 201:
            ids_tareas.append(r.json()["id"])
            print(f"   ✅ {t['title']}")
        else:
            print(f"   ❌ {t['title']} — {r.status_code}")
            ids_tareas.append(None)

    # ── Trabajos con incidencias ───────────────────────────────
    print(f"\n📋 Creando {len(TRABAJOS_CON_INCIDENCIAS)} trabajos con incidencias...")
    for w in TRABAJOS_CON_INCIDENCIAS:
        task_id = ids_tareas[w["task_idx"]]
        if not task_id:
            print("   ⚠️  Trabajo — tarea no disponible")
            continue

        payload = {
            "task_id":        task_id,
            "started_at":     w["started_at"],
            "status":         w["status"],
            "notes":          w["notes"],
            "checklist_items": [
                {
                    "description":    item["description"],
                    "is_done":        item["is_done"],
                    "has_incident":   item["has_incident"],
                    "incident_notes": item["incident_notes"],
                }
                for item in w["checklist"]
            ]
        }
        r = requests.post(f"{BASE_URL}/jobs/", json=payload)
        if r.status_code == 201:
            n_incidencias = sum(1 for i in w["checklist"] if i["has_incident"])
            print(f"   ✅ Trabajo tarea #{task_id} · {n_incidencias} incidencia(s)")
        else:
            print(f"   ❌ Trabajo tarea #{task_id} — {r.status_code}")

    # ── Ausencias ──────────────────────────────────────────────
    print(f"\n🏖️  Creando {len(AUSENCIAS)} solicitudes de vacaciones...")
    for a in AUSENCIAS:
        emp_id = ids_empleados[a["employee_idx"]]
        if not emp_id:
            continue
        payload = {
            "employee_id":  emp_id,
            "absence_type": a["absence_type"],
            "start_date":   a["start_date"],
            "end_date":     a["end_date"],
            "reason":       a["reason"],
        }
        r = requests.post(f"{BASE_URL}/absences/", json=payload)
        emp_nombre = EMPLEADOS[a["employee_idx"]]["name"]
        if r.status_code == 201:
            print(f"   ✅ {emp_nombre} · {a['start_date']} → {a['end_date']}")
        else:
            print(f"   ❌ {emp_nombre} — {r.status_code}")

    print("\n🌿 Base de datos poblada correctamente.")
    print(f"   👤 {len(CLIENTES)} clientes")
    print(f"   👷 {len(EMPLEADOS)} empleados")
    print(f"   📅 {len(TAREAS)} tareas")
    print(f"   📋 {len(TRABAJOS_CON_INCIDENCIAS)} trabajos con incidencias")
    print(f"   🏖️  {len(AUSENCIAS)} solicitudes de vacaciones pendientes")


if __name__ == "__main__":
    seed()