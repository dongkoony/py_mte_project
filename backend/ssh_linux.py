import paramiko
import json
import os
from jinja2 import Environment, FileSystemLoader

# 템플릿 디렉터리 설정
TEMPLATE_DIR = r"C:\project\MTE-Project\backend\templates"

# Jinja2 환경 설정
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def get_server_info(host, port, username, password=None, key_path=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # 서버 연결
    try:
        if key_path:
            private_key = paramiko.RSAKey.from_private_key_file(key_path)
            client.connect(host, port=port, username=username, pkey=private_key)
        else:
            client.connect(host, port=port, username=username, password=password)
    except Exception as e:
        raise Exception(f"SSH 연결 오류: {str(e)}")
    
    # OS 정보 가져오기
    stdin, stdout, stderr = client.exec_command('uname -a')
    os_info = stdout.read().decode().strip()

    # CPU 정보 가져오기
    stdin, stdout, stderr = client.exec_command('lscpu')
    cpu_info = stdout.read().decode().split("\n")
    cpu_details = {line.split(":")[0].strip(): line.split(":")[1].strip() for line in cpu_info if line}

    # Memory 정보 가져오기
    stdin, stdout, stderr = client.exec_command('free -h')
    memory_info = stdout.read().decode().split("\n")[1].split()
    memory_info = {
        'total': memory_info[1],
        'used': memory_info[2],
        'free': memory_info[3]
    }

    # Disk 정보 가져오기
    stdin, stdout, stderr = client.exec_command('df -h')
    disk_info = stdout.read().decode().split("\n")[1:-1]
    disks_info = [{'filesystem': disk.split()[0], 'size': disk.split()[1], 'used': disk.split()[2], 'available': disk.split()[3]} for disk in disk_info]

    # 연결 종료
    client.close()

    # 결과 반환
    result = {
        'OS': os_info,
        'CPU': cpu_details,
        'Memory': memory_info,
        'Disks': disks_info
    }

    return result

def get_terraform_template(host_info):
    # 템플릿 파일 확인
    template_path = os.path.join(TEMPLATE_DIR, 'ec2_template.tf.j2')
    if not os.path.exists(template_path):
        raise Exception(f"템플릿 파일이 {template_path} 에 없습니다.")

    # 템플릿 불러오기
    template = env.get_template('ec2_template.tf.j2')

    # 필요한 데이터 추출 및 변환
    data_extracted = {
        "os_name": host_info["OS"].split()[0],  # OS 이름
        "cpu_model": host_info["CPU"]["Model name"]  # CPU 모델 이름
    }

    # 템플릿 적용 및 반환
    return template.render(data_extracted)
