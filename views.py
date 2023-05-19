from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db import connection
from django.db.models import Sum
import math
import socket
import geocoder
import pycountry
from requests import get
import json
from django.db.models import Avg
import datetime
from datetime import date
from django.urls import reverse
import requests

# Create your views here.


def Home(request):
	return render(request,"Home.html",{})


def Admin_Login(request):
	if request.method == "POST":
		A_username = request.POST['aname']
		A_password = request.POST['apass']
		if AdminDetails.objects.filter(username = A_username,password = A_password).exists():
			ad = AdminDetails.objects.get(username=A_username, password=A_password)
			print('d')
			messages.info(request,'Admin login is Sucessfull')
			request.session['type_id'] = 'Admin'
			request.session['UserType'] = 'Admin'
			request.session['login'] = "Yes"
			return redirect("/")
		else:
			print('y')
			messages.error(request, 'Error wrong username/password')
			return render(request, "Admin_Login.html", {})
	else:
		return render(request, "Admin_Login.html", {})

def User_Login(request):
	if request.method == "POST":
		C_name = request.POST['username']
		C_password = request.POST['password']
		if userDetails.objects.filter(Username=C_name,Password=C_password).exists():
			users = userDetails.objects.all().filter(Username=C_name,Password=C_password)
			messages.info(request,C_name +' logged in')
			request.session['UserId'] = users[0].id
			request.session['type_id'] = 'User'
			request.session['UserType'] = C_name
			request.session['login'] = "Yes"
			return redirect('/')
		else:
			messages.info(request, 'Please Register')
			return redirect("/User_Registeration")
	else:
		return render(request,'User_Login.html',{})

def User_Registeration(request):
	if request.method == "POST":
		Name= request.POST['name']
		Age= request.POST['age']
		Phone= request.POST['phone']
		Email= request.POST['email']
		Address= request.POST['address']
		Card_Number= request.POST['cardnum']
		cvv= request.POST['cvv']
		month= request.POST['month']
		year= request.POST['year']
		Question= request.POST['question']
		Answer= request.POST['answer']
		Username= request.POST['Username']
		Password= request.POST['Password']
		url = 'http://ipinfo.io/json'
		response = get(url)
		data = json.loads(response.text)
		country = data['country']
		ip = data['ip']
		print("ip:", ip)
		print("country:", country)
		Attempts = 3
		obj = userDetails(
			Name=Name
			,Age=Age
			,Phone=Phone
			,Email=Email
			,Address=Address
			,Card_Number=Card_Number
			,cvv=cvv
			,month=month
			,year=year
			,Country=country
			,ip_address=ip
			,Question=Question
			,Answer=Answer
			,Username=Username
			,Password=Password
			,Attempts=Attempts)
		obj.save()
		messages.info(request,Name+"Registered")
		return redirect('/User_Login')
	else:
		return render(request,"User_Registeration.html",{})



def Manage_Products(request):
	data = Product.objects.all()
	return render(request,"Manage_Products.html",{'data':data})

def Add_Product(request):
	if request.method == "POST":
		P_name = request.POST['name']
		P_price = request.POST['price']
		P_image = request.FILES['image']
		obj = Product(Product_Image=P_image
					,Product_Name=P_name
					,Product_Price=P_price)
		obj.save()
		messages.info(request,"Product Added")
		return redirect("/Manage_Products/")
	else:
		return render(request,"Add_Product.html",{})

def ViewProduct(request,id):
	details = Product.objects.filter(id = id)
	return render(request,"ViewProduct.html",{'details':details})

def Delete_Product(request,id):
	delcomp = Product.objects.get(id=id) 
	delcomp.delete()
	return redirect('/Manage_Products/')


def Cart(request):

	if request.method == "POST":
		user_id = request.session['UserId']
		print('Userid: ',user_id)
		prod_id = request.POST['Product_id']
		print('Productid: ',prod_id)
		quantity = request.POST['quantity']
		# count = []
		prod_data = Product.objects.filter(id=prod_id)
		for i in prod_data:
			Prod_name = i.Product_Name
			price = i.Product_Price

			#details=cart.objects.all().
		if cart.objects.filter(uid=user_id,prod_id=prod_id).exists():
			CartDetails = cart.objects.filter(uid=user_id,prod_id=prod_id)
			cid = CartDetails[0].id
			print('cid: ',cid)
			Qnt = CartDetails[0].Prod_quantity
			print('Qnt: ',Qnt)
			Cprice = CartDetails[0].Prod_price
			print('Cprice: ',Cprice)
			prodquantity = int(Qnt) + int(quantity)
			print('New quantity: ',prodquantity)
			ProdPrice = int(Cprice) + int(price)
			print(ProdPrice)
			TotalPrice = int(price) * int(prodquantity)
			print('TotalPrice: ',TotalPrice)
			cart.objects.filter(id=cid).update(Prod_quantity=prodquantity,Prod_price=TotalPrice)
			#details = cart.objects.all().filter(uid=user_id)
			#return render(request,'cart1.html',{'details':details})
		else:
			TotalPrice = int(price) * int(quantity)
			print('quantity: ',quantity)
			print('TotalPrice: ',TotalPrice)
			objects = cart(uid=user_id,prod_id =prod_id,Prod_name=Prod_name,Prod_price=TotalPrice,Prod_quantity=quantity,Initial_price=price)
			objects.save()
		CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
		CartTotal = CT['Prod_price__sum']
		print(CT)
		print(CartTotal)
		count = cart.objects.filter(uid=user_id)
		print(count)
		count = len(count)
		print(count)		
		details = cart.objects.all().filter(uid=user_id)
		return render(request,'Cart.html',{'details':details,'CartTotal':CartTotal})
	else:
		user_id = request.session['UserId']
		CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
		CartTotal = CT['Prod_price__sum']
		print(CT)
		print(CartTotal)
		count = cart.objects.filter(uid=user_id)
		print(count)
		count = len(count)
		print(count)
		if count == 0:
			print("Cart is empty")

		details = cart.objects.all().filter(uid=user_id)
		return render(request,'Cart.html',{'details':details,'CartTotal':CartTotal,'count':count})

def deletecart(request,id):
	cart.objects.filter(id=id).delete()
	return redirect('/Cart')

def Checkout(request):
	user_id = request.session['UserId']
	CT = cart.objects.filter(uid=user_id).aggregate(Sum('Prod_price'))
	quantity =  cart.objects.filter(uid=user_id).aggregate(Sum('Prod_quantity'))
	print(quantity)
	quantity = quantity['Prod_quantity__sum']
	print(quantity)
	carts = []
	quant = []
	CartTotal = CT['Prod_price__sum']
	print(CT)
	print(CartTotal)
	CartTotal = int(CartTotal)
	print(CartTotal)
	quant.append(quantity)
	carts.append(CartTotal)
	print(carts)
	info = userDetails.objects.all().filter(id=user_id)
	details = cart.objects.all().filter(uid=user_id)
	return render(request,'Checkout.html',{'details':details,'carts':carts,'quant':quant,'info':info,'CartTotal':CartTotal})

def AddTransaction(request):
	if request.method == "POST":
		total = request.POST['total']
		request.session['total'] = total
		print(str(total))
		total = int(total)
		# thirty_percent = total*0.3
		# print(int(thirty_percent))
		# amount = int(total) + int(thirty_percent)
		# print('Amount :'+str(amount))
		user_id = request.session['UserId']
		details = userDetails.objects.filter(id = user_id)
		for i in details:
			User_country = details[0].Country
			print("User_country :" + str(User_country))
			Question = details[0].Question
			email = details[0].Email
		url = 'http://ipinfo.io/json'
		response = get(url)
		data = json.loads(response.text)
		country = data['country']
		ip = data['ip']
		print("ip:", ip)
		print("country:", country)
		today = date.today()
		if userDetails.objects.filter(id=user_id,Permission="Blocked"):
			messages.info(request,"You are blocked cannot place an order")
		else:
			if Transaction.objects.filter(User_Id=user_id).exists():
				import random
				number = random.randint(100, 999)
				print(number)
				userDetails.objects.filter(id = user_id).update(OTP=number)
				result = Transaction.objects.all().filter(User_Id=user_id).aggregate(Avg('Spending'))
				average_spending = result['Spending__avg']
				print("average_spending :"+str(average_spending))
				thirty_percent = int(average_spending)*0.3
				print("thirty_percent :"+str(thirty_percent))
				CheckAmount = int(average_spending) + int(thirty_percent)
				print("CheckAmount :" + str(CheckAmount))
				if total >= CheckAmount or User_country != country:
					# return redirect(reverse('Security') + '?ip=' + ip + '&country=' + str(country) + '&total=' + str(total) + '&today='+ str(today))
					url = "https://smail.azurewebsites.net/Email.aspx?Title=OTP Verification&emailid={email}&Sub=TestSubject&Msg=OTP  is {OTP}.".format(OTP=number,email = email)
					res = requests.post(url)
					return render(request,"Security.html",{'Question':Question})
					# obj = Transaction(User_Id=user_id
					# 					,ip_address=ip
					# 					,Country=country
					# 					,Spending=total
					# 					,Fraud="YES"
					# 					,Date=today)
					# obj.save()
					# messages.info(request,"Order Placed")
				else:
					obj = Transaction(User_Id=user_id
										,ip_address=ip
										,Country=country
										,Spending=total
										,Date=today)
					messages.info(request,"Order Placed")
					obj.save()
			else:
				obj = Transaction(User_Id=user_id
										,ip_address=ip
										,Country=country
										,Spending=total
										,Date=today)
				obj.save()
				messages.info(request,"Order Placed")
			cart.objects.all().filter(uid=user_id).delete()
			return redirect('/')
		return redirect('/')
	else:
		return render(request,"Checkout.html",{})

def Admin_ViewTransaction(request):
	details = userDetails.objects.all()
	return render(request,"Admin_ViewTransaction.html",{'details':details})

def viewTransactionAdmin(request,id):
	details = Transaction.objects.all().filter(User_Id=id)
	return render(request,"viewTransactionAdmin.html",{'details':details})

def viewTransactionUser(request):
	user_id = request.session['UserId']
	details = Transaction.objects.all().filter(User_Id=user_id)
	return render(request,"viewTransactionUser.html",{'details':details})

def Security(request):
	if request.method == "POST":
		answer =  request.POST['answer']
		total1 =  request.session['total']
		print("Total :"+str(total1))
		user_id = request.session['UserId']
		details = userDetails.objects.filter(id=user_id)
		for i in details:
			Question = details[0].Question
			Answer = details[0].Answer
			Attempts = int(details[0].Attempts)
		url = 'http://ipinfo.io/json'
		response = get(url)
		data = json.loads(response.text)
		country = data['country']
		ip = data['ip']
		print("ip:", ip)
		print("country:", country)
		today = date.today()
		if answer != Answer and 0 < Attempts <= 3:
			Attempts = Attempts - 1
			userDetails.objects.filter(id=user_id).update(Attempts=Attempts)
			# return redirect(reverse('Security') + '?ip=' + ip + '&country=' + str(country) + '&total=' + str(total) + '&today='+ str(today))
			return render(request,"Security.html",{'ip':ip,'Question':Question})
		elif answer == Answer and Attempts < 0:
			messages.info(request,"You have attempted 3 times user is blocked")
			userDetails.objects.filter(id = user_id).update(Permission="Blocked")
		elif answer == Answer and 0 < Attempts <= 3:
			obj = Transaction(User_Id=user_id,Spending=total1,ip_address=ip,Country=country,Date=today)
			obj.save()
			messages.info(request,"Order Placed")
			cart.objects.all().filter(uid=user_id).delete()
			userDetails.objects.filter(id =user_id).update(Attempts="3")
			return redirect('/')
		else:
			messages.info(request,"Answer doesnt match or you have tried more than 3 times")
			userDetails.objects.filter(id = user_id).update(Permission="Blocked")
			return redirect('/')
		return render(request,"Security.html",{'Question':Question,'ip':ip})
	else:
		user_id = request.session['UserId']
		details = userDetails.objects.filter(id=user_id)
		for i in details:
			Question = details[0].Question
			Answer = details[0].Answer
			Attempts = int(details[0].Attempts)
		return render(request,"Security.html",{'Question':Question})

def Security_OTP(request):
	if request.method == "POST":
		answer =  request.POST['answer']
		total1 =  request.session['total']
		print("Total :"+str(total1))
		user_id = request.session['UserId']
		details = userDetails.objects.filter(id=user_id)
		for i in details:
			Question = details[0].Question
			OTP = details[0].OTP
			print("OTP is :"+str(OTP))
			Attempts = int(details[0].Attempts)
		url = 'http://ipinfo.io/json'
		response = get(url)
		data = json.loads(response.text)
		country = data['country']
		ip = data['ip']
		print("ip:", ip)
		print("country:", country)
		today = date.today()
		if answer != OTP and 0 < Attempts <= 3:
			Attempts = Attempts - 1
			userDetails.objects.filter(id=user_id).update(Attempts=Attempts)
			# return redirect(reverse('Security') + '?ip=' + ip + '&country=' + str(country) + '&total=' + str(total) + '&today='+ str(today))
			return render(request,"Security.html",{'ip':ip,'Question':Question})
		elif answer == OTP and Attempts < 0:
			messages.info(request,"You have attempted 3 times user is blocked")
			userDetails.objects.filter(id = user_id).update(Permission="Blocked")
		elif answer == OTP and 0 < Attempts <= 3:
			obj = Transaction(User_Id=user_id,Spending=total1,ip_address=ip,Country=country,Date=today)
			obj.save()
			messages.info(request,"Order Placed")
			cart.objects.all().filter(uid=user_id).delete()
			userDetails.objects.filter(id =user_id).update(Attempts="3")
			return redirect('/')
		else:
			messages.info(request,"Answer doesnt match or you have tried more than 3 times")
			userDetails.objects.filter(id = user_id).update(Permission="Blocked")
			return redirect('/')
		return render(request,"Security.html",{'Question':Question,'ip':ip})
	else:
		user_id = request.session['UserId']
		details = userDetails.objects.filter(id=user_id)
		for i in details:
			Question = details[0].Question
			Answer = details[0].Answer
			Attempts = int(details[0].Attempts)
		return render(request,"Security.html",{'Question':Question})


def Logout(request):
	Session.objects.all().delete()
	return redirect("/")
