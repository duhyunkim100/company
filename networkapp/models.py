from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="기업명", default="미정")
    category = models.CharField(max_length=255, verbose_name="종목", default="기타")
    main_product = models.CharField(max_length=255, verbose_name="주요제품", default="정보 없음")

    def __str__(self):
        return self.name

class Transaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="transactions")
    partner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="partners")
    transaction_type = models.CharField(max_length=50, verbose_name="거래처 구분", choices=[("구매처", "구매처"), ("판매처", "판매처")])

    def __str__(self):
        return f"{self.company.name} - {self.partner.name} ({self.transaction_type})"
