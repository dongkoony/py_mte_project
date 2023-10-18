# Move To EC2, Migration To EC2

## 현 프로젝트의  목표
```
1. SSH 서버 접속 후 서버 정보 추출
2. 추출 정보를 S3 Bucket에 Json 포멧으로 자동 저장
3. S3 Bucket Json 포멧을 가지고 테라폼 템플릿 다운로드
4. 마이그레이션을 희망하는 서버를 손 쉽게 IaC로 인프라 구축
5. 모든 접근은 웹 페이지를 사용할 것 이며, AWS S3 Bucket에 정적 호스팅 후,
   도메인을 https AWS Cloudfront에 접근 시킨 후 원활한 환경을 구성
```

## 현재 프로젝트 진행 상황
```
테스트용 컴파일(Gui)환경을 사용하여 테스트 중이며,
서버 IP, SSH Port, User ID, User Password & Key Pair를 사용해여, 서버 접근 후 정보 추출(Json)
Json 포멧을 S3 Bucket에 Auto Save 하며, IaC Terraform 다운로드 누를 시 Sample Terraform Template는 다운로드 됨.
```


## Directory Drawing
```
├─backend
│  ├─static           # 백엔드와 관련된 정적 파일들 저장
│  ├─models           # 데이터베이스 모델 또는 데이터 처리 관련 코드
│  ├─views            # 애플리케이션의 뷰 함수나 API 엔드포인트 코드
│  ├─utils            # 유틸리티 및 보조 함수
│  ├─templates        # 템플릿 파일 (Jinja2 등의 템플릿 엔진을 사용할 경우)
│  └─__pycache__
└─frontend
   ├─js               # 자바스크립트 파일들
   ├─css              # 스타일시트 파일들
   ├─images           # 이미지 리소스
   └─index.html       # 주요 시작 페이지
``` 

