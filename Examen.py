import netmiko
from netmiko import ConnectHandler
# ─────────────────────────────────────────────
# Datos del estudiante
# ─────────────────────────────────────────────
print("=" * 55)
print("  Nombre   : PATRICIA MARTINEZ")
print("  Carrera  : Telecomunicaciones")
print("  Modalidad: Online")
print("=" * 55)
# ─────────────────────────────────────────────
# IP de la máquina virtual por teclado
# ─────────────────────────────────────────────
host_ip = input("\nIngrese la dirección IP de la máquina virtual: ")
# ─────────────────────────────────────────────
# Conexión SSH al router
# ─────────────────────────────────────────────
sshCli = ConnectHandler(
    device_type='cisco_ios',
    host=host_ip,
    port=22,
    username='cisco',
    password='cisco123!'
)
# ─────────────────────────────────────────────
# Configuración básica del router
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
]
output = sshCli.send_config_set(config_commands)
print("\n[Configuración aplicada]\n", output)
# ─────────────────────────────────────────────
# Verificaciones
# ─────────────────────────────────────────────
# Interfaces creadas
output = sshCli.send_command("show ip interface brief")
print("\n[show ip interface brief]\n", output)
# Tabla de enrutamiento
output = sshCli.send_command("show ip route")
print("\n[show ip route]\n", output)
# Running config
output = sshCli.send_command("show running-config")
print("\n[show running-config]\n", output)
sshCli.disconnect()
print("\nConexión cerrada.")
