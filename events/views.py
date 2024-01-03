from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# import razorpay
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt

from .models import Event, Registration
from accounts.models import Profile

# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))




def select_event(request):
    events = Event.objects.all()
    
    parameters = {
        'events': events
    }
    
    return render(request, 'home/event_choice.html', parameters)

def registration(request, slug):
    
    event = Event.objects.get(slug=slug)

    if request.method == "POST":
        name = request.POST.get('name')
        course = request.POST.get('course')
        year = request.POST.get('year')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        day_host = request.POST.get('day_host')

        referral_code = request.POST.get('referral_code')
        registration_type = request.POST.get('registration_type')
        
        other_referral_name = request.POST.get('other_referral_name')
        
        payment_screenshot = request.FILES.get('screenshot')
        referrance_number = request.POST.get('referrance_number')
        
        # Check if user has already registered for this event
        if Registration.objects.filter(email=email).exists():
            messages.error(request, "You have already registered for this event.")
            return redirect('registration', slug=slug)
        
        # if event.ticket_price == 0:
            
    
        new_registration = Registration(
            name = name,
            course = course,
            year = year,
            email = email,
            hosteller_dayScholar = day_host,
            event = event,
            mobile_number = mobile_number,
            referrance_number = referrance_number
        )
        
        # referral_name = Profile.objects.get(referral_code=referral_code),
        # referral_code = referral_code,
        # other_referral_name = other_referral_name,
        
        if referral_code != 'other' and referral_code != 'none':
            new_registration.referral_code = referral_code
            new_registration.referral_name = Profile.objects.get(referral_code=referral_code)
            
        elif referral_code == 'none':
            new_registration.referral_code = referral_code
            
        elif referral_code == 'other':
            new_registration.other_referral_name = other_referral_name
            
        if registration_type == "Group":
            new_registration.registration_type = "Group"
        elif registration_type == "Duo":
            new_registration.registration_type = "Duo"
        else:
            new_registration.registration_type = "Solo"
        
        new_registration.payment_screenshot = payment_screenshot
        
        new_registration.save()
        
        event.total_tickets = event.total_tickets - 1
        event.save()
        
        # Sending Mail
        
        myfile = f"""Thank You For Confirming Your Tickets - Club Literario!

Dear {name},

CONGRATULATIONS! 🎉✨ You have successfully booked your seat in “{event.name}” -one of the prestigious events of GLA University.
You will soon get confirmation of your ticket once reviewed by the Literario Administration.📝

Will keep you mailed the further updates! Have a great day.

For any further uncertainty, please feel welcomed;😊
Mr. Divyanshu Khandelwal: 8273619318
Mr. Priyanshu Gera: 7302068234

Best wishes,
Divyanshu Khandelwal,
Technical Team,
Club Literario
GLA University Mathura."""

        email_subject = f' Tickets Booked For {event.name.title()} ❤️ '
        email_body = myfile
        email_from = 'Club Literario'
        email_to = [email]

        # Send the email
        send_mail(email_subject, email_body, email_from, email_to)


        # ====================================
        
        messages.success(request, "Welcome to the most awaited event of the year! We are glad to have you on board!".title())
       
        return redirect('registration', slug=slug)
    
    referrals = Profile.objects.all()
    
    # currency = 'INR'
    # amount = 9900
        
    # razorpay_order = razorpay_client.order.create(dict(amount=amount,
    #                                                 currency=currency,
    #                                                 payment_capture='0'))

    # # order id of newly created order.
    # razorpay_order_id = razorpay_order['id']
    # callback_url = '/paymenthandler'
    
    # parameters = {
    #     'events': events,
    #     'referrals': referrals,
    # }
    
    # parameters['razorpay_order_id'] = razorpay_order_id
    # parameters['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    # parameters['razorpay_amount'] = amount
    # parameters['currency'] = currency
    # parameters['callback_url'] = callback_url
    
    parameters = {
        'event': event,
        'referrals': referrals,
    }
    
    return render(request, "home/registration.html", parameters)

# @csrf_exempt
# def paymenthandler(request
    
    print("paymenthandler called")
 
    # only accept POST request.
    if request.method == "POST":
        try:
            
            print("POST try entered")
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            print("params_dict created")
            
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            
            print("signature verified")
            if result is not None:
                amount = 9900  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    messages.success(request, "Payment Successful")
                    return redirect('registration')
                except:
 
                    # if there is an error while capturing payment.
                    messages.error(request, "Payment Faliure")
                    return redirect('registration')
            else:
 
                # if signature verification fails.
                messages.error(request, "Payment for signature")
                return redirect('registration')
        except:
 
            # if we don't find the required parameters in POST data
            messages.error(request, "we don't find the required parameters in POST data")
            return redirect('registration')
    else:
       # if other than POST request is made.
        messages.error(request, "other than POST request is made.")
        return redirect('registration')
    
    
# def all_events(request):
#     events = Event.objects.all()
#     return render(request, 'events/all_events.html', {'events': events})


# def event_detail(request, slug):
#     event = get_object_or_404(Event, slug=slug)
#     return render(request, 'events/event_detail.html', {'event': event})