from django.db import models

# Create your models here.



class AdminDetails(models.Model):
	username = models.CharField(max_length=100,default=None)
	password = models.CharField(max_length=100,default=None)
	class Meta:
		db_table = 'AdminDetails'

class userDetails(models.Model):
	Username 	= models.CharField(max_length=100,default=None,null=True)
	Password 	= models.CharField(max_length=100,default=None,null=True)
	Name 		= models.CharField(max_length=100,default=None,null=True)
	Age 		= models.CharField(max_length=200,default=None,null=True)
	Phone 		= models.CharField(max_length=100,default=None,null=True)
	Email 		= models.CharField(max_length=100,default=None,null=True)
	Address 		= models.CharField(max_length=100,default=None,null=True)
	Card_Number 	= models.CharField(max_length=100,default=None,null=True)
	cvv 			= models.CharField(max_length=100,default=None,null=True)
	month 			= models.CharField(max_length=100,default=None,null=True)
	year 			= models.CharField(max_length=100,default=None,null=True)
	spending 		= models.CharField(max_length=100,default=None,null=True)
	ip_address =models.CharField(max_length=100,default=None,null=True)
	Country =models.CharField(max_length=100,default=None,null=True)
	Question =models.CharField(max_length=100,default=None,null=True)
	Answer =models.CharField(max_length=100,default=None,null=True)
	Attempts =models.CharField(max_length=100,default=None,null=True)
	OTP =models.CharField(max_length=100,default=None,null=True)
	Permission =models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'userDetails'


class Product(models.Model):
	Product_Image = models.ImageField(upload_to="images/",null=True)
	Product_Name = models.CharField(max_length=100,default=None,null=True)
	Product_Price = models.CharField(max_length=100,default=None,null=True)
	class Meta:
		db_table = 'Product'

class cart(models.Model):
	uid 			= models.CharField(max_length=100,default=None)
	prod_id 		= models.CharField(max_length=100,default=None)
	Prod_name 		= models.CharField(max_length=100,default=None)
	Prod_price 		= models.CharField(max_length=100,default=None)
	Prod_quantity 	= models.IntegerField(max_length=100,default=None)
	Initial_price 	= models.CharField(max_length=100,default=None)

	class Meta:
		db_table = "cart"


class Transaction(models.Model):
	User_Id =models.CharField(max_length=100,default=None,null=True)
	ip_address =models.CharField(max_length=100,default=None,null=True)
	Country =models.CharField(max_length=100,default=None,null=True)
	Spending =models.CharField(max_length=100,default=None,null=True)
	Fraud =models.CharField(max_length=100,default=None,null=True)
	Date =models.CharField(max_length=100,default=None,null=True)

	class Meta:
		db_table = "Transaction"






