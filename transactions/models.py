from django.db import models


class RawTransaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    transaction_date = models.DateField()
    transaction_time = models.TimeField(max_length=255)
    transaction_qty = models.IntegerField()
    store_id = models.IntegerField()
    store_location = models.CharField(max_length=255)
    product_id = models.IntegerField()
    unit_price = models.FloatField()
    product_category = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    product_detail = models.CharField(max_length=255)

    class Meta:
        db_table = "raw_transaction"
        app_label = "transactions"
