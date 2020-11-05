from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import product, comment, order
import os, mimetypes
from django.http import StreamingHttpResponse
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
from zeep import Client


#payment variables
MERCHANT = os.getenv('MERCHANT')
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = os.getenv('URL') + 'order/payment_verify'


def Product(req, ID):
    if req.user.is_authenticated:
        paid = req.user.has_product(ID)
    else:
        paid = False
    return render(req, 'course.html', {'product':product.objects.get(id=ID), 'paid':paid, 'products':product.objects.all()})

def list_courses(req):
    return render(req, 'list-courses.html', {'products':product.objects.all()})


@login_required(login_url='login')
def commenting(req):
    if req.method == "POST":
        text = req.POST['text']
        p = product.objects.get(id=int(req.POST['product_id']))
        c = comment(product=p, user=req.user, text=text.encode())
        c.save()
        return redirect('product', ID=p.id)



@login_required(login_url='login')
def download(req, ID):
    #return sendfile(req, product.objects.get(id=ID).File.path)
    if req.user.has_product(ID):
        #file_path = product.objects.get(id=ID).File.path
        #with open(file_path, 'rb') as fh:
        #    response = HttpResponse(fh, content_type="video/mkv")
        #    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        #    return response

        the_file = product.objects.get(id=ID).File.path
        filename = os.path.basename(the_file)
        chunk_size = 10000
        response = StreamingHttpResponse(FileWrapper(open(the_file, 'rb'), chunk_size), content_type=mimetypes.guess_type(the_file)[0])
        response['Content-Length'] = os.path.getsize(the_file)    
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    return HttpResponse('access denied!!')
    


@login_required(login_url='login')
def payment_request(req, ID):
    print(MERCHANT)
    print(CallbackURL)
    p = product.objects.get(id=ID)
    Order = order(product=p, user=req.user)
    result = client.service.PaymentRequest(MERCHANT, p.price, f'user_id:{req.user.id}', req.user.email, req.user.phone, CallbackURL)
    if result.Status == 100:
        Order.Authority = str(result.Authority)
        Order.save()
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        print(result)
        return HttpResponse('Error code: ' + str(result.Status))
        
 
@login_required(login_url='login')
def payment_verify(req):
    Order = order.objects.get(Authority=req.GET.get('Authority'))
    if not Order:
        return redirect('home')
    if not req.user.phone == Order.user.phone:
        return redirect('home')
    result = client.service.PaymentVerification(MERCHANT, req.GET.get('Authority'), Order.product.price)
    if result.Status == 100:
        p = Order.product
        p.download_counter += 1
        p.save()
        Order.paid = True
        Order.RefID = str(result.RefID)
        Order.save()
        return redirect('home')
    else:
        Order.delete()
        return redirect('home')
