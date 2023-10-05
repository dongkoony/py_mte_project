import winrm
import json

def get_windows_server_info(host, username, password):
    session = winrm.Session(
        f"https://[IP]:5986/wsman", 
        auth=(username, password)
    )
    
    # OS 정보
    ps_script = """$os = Get-WmiObject -Class Win32_OperatingSystem
    $os.Name
    """
    result = session.run_ps(ps_script)
    os_info = result.status_code, result.std_out.decode().strip()

    # CPU 정보
    ps_script = """$cpu = Get-WmiObject -Class Win32_Processor
    $cpu.Name
    """
    result = session.run_ps(ps_script)
    cpu_info = result.status_code, result.std_out.decode().strip()

    # Memory 정보
    ps_script = """$mem = Get-WmiObject -Class Win32_ComputerSystem
    $mem.TotalPhysicalMemory
    """
    result = session.run_ps(ps_script)
    memory_info = int(result.std_out.decode().strip()) / (1024 ** 3)  # GB로 변환

    return {
        'OS': os_info[1],
        'CPU': cpu_info[1],
        'Total Memory (GB)': memory_info
    }

host_info = get_windows_server_info("43.200.183.3", "Administrator", "%Ym0-?jxBE)h1S5?K$Sgh0qTL4$**c7u")
print(json.dumps(host_info, indent=4))
