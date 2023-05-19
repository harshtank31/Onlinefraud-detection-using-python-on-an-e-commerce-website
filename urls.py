from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
				
				path('',views.Home,name='Home'),
				path('Admin_Login/',views.Admin_Login,name='Admin_Login'),
				path('User_Login/',views.User_Login,name='User_Login'),
				path('User_Registeration/',views.User_Registeration,name='User_Registeration'),
				path('Manage_Products/',views.Manage_Products,name='Manage_Products'),
				path('Add_Product/',views.Add_Product,name='Add_Product'),
				path('ViewProduct/<int:id>',views.ViewProduct,name='ViewProduct'),
				path('Delete_Product/<int:id>',views.Delete_Product,name='Delete_Product'),
				path('Cart/',views.Cart,name='Cart'),
				path('deletecart/<int:id>',views.deletecart,name='deletecart'),
				path('Checkout/',views.Checkout,name='Checkout'),
				path('AddTransaction/',views.AddTransaction,name='AddTransaction'),
				path('Admin_ViewTransaction/',views.Admin_ViewTransaction,name='Admin_ViewTransaction'),
				path('viewTransactionAdmin/<int:id>',views.viewTransactionAdmin,name='viewTransactionAdmin'),
				path('viewTransactionUser/',views.viewTransactionUser,name='viewTransactionUser'),
				path('Security/',views.Security,name='Security'),
				path('Security_OTP/',views.Security_OTP,name='Security_OTP'),
				path('Logout/',views.Logout,name='Logout'),
					
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
