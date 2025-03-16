from django.db import models
import requests, json, decimal
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.
class Currency(models.Model):
    symbol= models.CharField(max_length=10, primary_key= True)
    usd_value= models.DecimalField(max_digits=10, decimal_places=2,default=1)

    def __str__(self) -> str:
        return self.symbol
class Transaction(models.Model):
    origin_currency =             models.ForeignKey("Currency",on_delete=models.CASCADE, related_name='origin_currency')
    destination_currency =        models.ForeignKey("Currency",on_delete=models.CASCADE, related_name='destination_currency')
    original_currency_values =    models.DecimalField(max_digits=10,decimal_places=2)
    destination_currency_values = models.DecimalField(max_digits=10,decimal_places=2)
    commission =                  models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    exchange_date  =              models.DateTimeField(auto_now_add=True)


class CurrencyHistory(models.Model):
    symbol    =   models.ForeignKey("Currency",on_delete=models.CASCADE)
    usd_value = models.DecimalField(max_digits=10,decimal_places=6,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
def save(self, *args, **kwargs):
    # extend your save logic here
    self.usd_value= self.get_value()
    super(CurrencyHistory, self).save(*args, **kwargs)
    
    def get_value(self) :
        api_url= f'https://economia.awesomeapi.com.br/last/{self.symbol}-USD'
        response= requests.get(api_url).content
        json_data = json.loads(response)
        usd_ask_value= json_data[f'{self.symbol}USD']['ask']
        decimal_value= decimal.Decimal(usd_ask_value)
        return decimal_value

class Currencybalance(models.Model):
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    shared_portfolio = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0),MaxValueValidator(1)])
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usd_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)


def __str__(self) -> str:
    return f"{self.currency.symbol} {self.value}" 

@property
def usd_balance(self):
     current_usd_rate = CurrencyHistory.objects.create(symbol=self.currency)
     usd_rate = current_usd_rate.usd_value * self.value
     return usd_rate


  

class ExchangeGoal(models.Model):
    origin_balance         = models.ForeignKey('CurrencyBalance', on_delete=models.CASCADE, related_name='exchange_goal')
    destination_currency   = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='exchange_goal')
    initial_value          = models.DecimalField(max_digits=10, decimal_places=2)
    threshold              = models.DecimalField(max_digits=5, decimal_places=2)
    created_at             = models.DateTimeField(auto_now_add=True)
    executed_at            = models.DateTimeField(null=True, blank=True)
    completed              = models.BooleanField(default=False)
    transaction            = models.OneToOneField('Transaction', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def percentage(self):
        return self.threshold * 100
    
    @property
    def increase(self):
        return self.threshold * self.origin_balance.value
    @property
    def difference_initial_value(self):
       return self.origin_balance.usd_value - self.initial_value
    @property
    def percentage_difference(self):
       return self.difference_initial_value/self.initial_value * 100
