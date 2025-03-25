import os
import django
import pandas as pd

# Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_network.settings")
django.setup()

from networkapp.models import Company, Transaction

# CSV 데이터 로드 (기업 정보 저장)
csv_file = "C:/Users/kdh15/OneDrive/바탕 화면/두현/undata/company_info.csv"
df_csv = pd.read_csv(csv_file, dtype=str)

for _, row in df_csv.iterrows():
    company, created = Company.objects.get_or_create(
        name=row["기업명"],  # 기업명
        category=row["종목"],  # 종목
        main_product=row["주요제품"]  # 주요제품
    )
print("기업 정보 로드 완료!")

# 엑셀 데이터 로드 (거래 관계 저장)
excel_file = "C:/Users/kdh15/OneDrive/바탕 화면/두현/undata/undata.xlsx"
df_excel = pd.read_excel(excel_file, sheet_name=0, dtype=str)
df_excel = df_excel[["기업명", "거래처구분", "TXPL_NM"]].dropna()

for _, row in df_excel.iterrows():
    company_name = row["기업명"]
    partner_name = row["TXPL_NM"]
    transaction_type = row["거래처구분"]

    # 기업 정보가 DB에 있는지 확인 후 가져오기 (없으면 생성 X)
    company = Company.objects.filter(name=company_name).first()
    partner = Company.objects.filter(name=partner_name).first()

    if company and partner:
        Transaction.objects.get_or_create(
            company=company,
            partner=partner,
            transaction_type=transaction_type
        )

print("거래 관계 데이터 로드 완료!")
