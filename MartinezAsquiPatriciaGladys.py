from netmiko import ConnectHandler

# ─────────────────────────────────────────────
# Datos del estudiante
# ─────────────────────────────────────────────
print("=" * 55)
print("  Nombre   : PATRICIA MARTINEZ")
print("  Carrera  : Telecomunicaciones")
print("  Modalidad: Semipresencial")
print("=" * 55)

# ─────────────────────────────────────────────
# IP de la máquina virtual por teclado
# ─────────────────────────────────────────────
host_ip = input("\nIngrese la dirección IP de la máquina virtual: ")

# ─────────────────────────────────────────────
# Diccionario de conexión (Parte A)
# ─────────────────────────────────────────────
device = {
    "device_type": "cisco_ios",
    "host": host_ip,
    "username": "cisco",
    "password": "cisco123!",
    "port": 22
}

# ─────────────────────────────────────────────
# Conexión SSH al router con manejo de excepciones (Parte B)
# ─────────────────────────────────────────────
try:
    sshCli = ConnectHandler(**device)
    print("Conexión establecida correctamente")
except Exception as e:
    print("Error conexión:", e)
    raise SystemExit("No se pudo continuar sin conexión.")

# ─────────────────────────────────────────────
# PARTE C — Obtención de información del dispositivo
# ─────────────────────────────────────────────

# Hostname actual
output = sshCli.send_command("show running-config | include hostname")
print("\n[hostname actual]\n", output)

# Interfaces
output = sshCli.send_command("show ip interface brief")
print("\n[show ip interface brief - antes de configurar]\n", output)

# Versión de IOS
output = sshCli.send_command("show version")
print("\n[show version]\n", output)

# ─────────────────────────────────────────────
# PARTE D y configuración adicional del router
# ─────────────────────────────────────────────
config_commands = [
    # Hostname
    'hostname R_MARTINEZ',

    # Banner
    'banner motd # Acceso autorizado solamente. Prohibido el ingreso no autorizado. #',

    # Clave enable
    'enable secret cisco123',

    # Línea de consola
    'line console 0',
    'password cisco123',
    'login',
    'exit',

    # Líneas VTY 0 4
    'line vty 0 4',
    'password cisco123',
    'login',
    'transport input ssh',
    'exit',

    # Encriptación de claves
    'service password-encryption',

    # Loopback0 — requerida por la guía del examen (10.10.10.1/32)
    'interface Loopback0',
    'ip address 10.10.10.1 255.255.255.255',
    'description LOOPBACK_NETMiko',
    'no shutdown',
    'exit',

    # Loopback 1 → quinta dirección de 172.10.10.0/24 = 172.10.10.5
    'interface loopback 1',
    'ip address 172.10.10.5 255.255.255.0',
    'description LOOPBACK1',
    'no shutdown',
    'exit',

    # Loopback 2 → tercera dirección de 172.10.20.0/24 = 172.10.20.3
    'interface loopback 2',
    'ip address 172.10.20.3 255.255.255.0',
    'description LOOPBACK2',
    'no shutdown',
    'exit',

    # Interfaz física — enlace hacia R2 (ajustar nombre de interfaz según la VM real)
    'interface GigabitEthernet0/0',
    'ip address 10.10.10.2 255.255.255.252',
    'description ENLACE_R2',
    'no shutdown',
    'exit',

    # Ruta estática hacia 172.16.20.0/24 vía 10.10.10.1
    'ip route 172.16.20.0 255.255.255.0 10.10.10.1',
]

output = sshCli.send_config_set(config_commands)
print("\n[Configuración aplicada]\n", output)

# ─────────────────────────────────────────────
# Verificaciones finales
# ─────────────────────────────────────────────

# Interfaces creadas (después de configurar)
output = sshCli.send_command("show ip interface brief")
print("\n[show ip interface brief - después de configurar]\n", output)

# Tabla de enrutamiento
output = sshCli.send_command("show ip route")
print("\n[show ip route]\n", output)

# Running config completa
output = sshCli.send_command("show running-config")
print("\n[show running-config]\n", output)

sshCli.disconnect()
print("\nConexión cerrada.")
