import paramiko
import json
import os
import boto3
from jinja2 import Environment, FileSystemLoader

# S3 bucket Auto Save
def save_data_to_s3(data, bucket_name, s3_key):
    s3 = boto3.client('s3')
    formatted_data = json.dumps(data, indent=4)
    s3.put_object(Body=formatted_data, Bucket=bucket_name, Key=s3_key)

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
    """
    주어진 호스트 정보를 사용하여 Jinja2 템플릿을 렌더링하고 테라폼 코드를 반환한다.
    
    Args:
    - host_info (dict): 호스트의 OS, CPU 등의 정보가 포함된 딕셔너리
    
    Returns:
    - str: 렌더링된 테라폼 코드
    """
    # 템플릿 불러오기
    try:
        template = env.get_template('ec2_template.tf.j2')
    except Exception as e:
        raise Exception(f"템플릿 파일 로딩 중 오류 발생: {str(e)}")

    # 필요한 데이터 추출하기
    cpu_model = host_info.get("CPU", {}).get("Model name", "t2.micro")  # default to t2.micro if not found
    os_name = host_info.get("OS", "").split()[0]  # OS 이름

    # 아래의 코드는 host_info의 내용을 확인하기 위한 코드입니다.
    # 실제 배포나 실행에서는 제거해야 합니다.
    print("Host Info:", host_info)

    # 템플릿 적용하고 반환하기
    return template.render(cpu_model=cpu_model, os_name=os_name)