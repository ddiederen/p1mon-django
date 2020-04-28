# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class SerialLive(models.Model):
    timestamp = models.DateTimeField(db_column='TIMESTAMP', primary_key=True, auto_now_add=True)  # Field name made lowercase.
    verbr_kwh_181 = models.FloatField(db_column='VERBR_KWH_181', blank=True, null=True)  # Field name made lowercase.
    verbr_kwh_182 = models.FloatField(db_column='VERBR_KWH_182', blank=True, null=True)  # Field name made lowercase.
    gelvr_kwh_281 = models.FloatField(db_column='GELVR_KWH_281', blank=True, null=True)  # Field name made lowercase.
    gelvr_kwh_282 = models.FloatField(db_column='GELVR_KWH_282', blank=True, null=True)  # Field name made lowercase.
    tariefcode = models.TextField(db_column='TARIEFCODE', blank=True, null=True)  # Field name made lowercase.
    act_verbr_kw_170 = models.FloatField(db_column='ACT_VERBR_KW_170', blank=True, null=True)  # Field name made lowercase.
    act_gelvr_kw_270 = models.FloatField(db_column='ACT_GELVR_KW_270', blank=True, null=True)  # Field name made lowercase.
    verbr_gas_2421 = models.FloatField(db_column='VERBR_GAS_2421', blank=True, null=True)  # Field name made lowercase.
#    record_verwerkt = models.BooleanField(db_column='RECORD_VERWERKT', blank=True, null=True, default=False)

    # return
    def __str__(self):
        """String for representing the Model object."""
        return str(self.timestamp)