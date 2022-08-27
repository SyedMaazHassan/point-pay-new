from dashboard.models import UserInfo, Voucher
from django.utils import timezone
from datetime import datetime
from payment.models import Account
import cv2
import os

def id_card_generate(organization_logo, organization_abbr, department, fee_price,user_full_name,user_profile_pic,roll_num,issue_date,expiry_date): 
    from django.conf import settings
    from django.core.files.base import ContentFile

    background_img_path = os.path.join(settings.BASE_DIR, "static", "card-bg.jpeg")
    bg = cv2.imread(background_img_path)
    #organization_logo = cv2.imread('logo.jpg')
    x,y,w,h = 40,20,200,200
    bg[y:y+h, x:x+w] = cv2.resize(organization_logo, (w,h))

    # Put some text
    #uni = "NED UET"
    org, font, scale, color, thick = (270,100), cv2.FONT_HERSHEY_TRIPLEX , 2, 0, 5
    cv2.putText(bg, organization_abbr, org, font, scale, color, thick)

    #dept = "CIS Department "
    org, font, scale, color, thick = (270,200), cv2.FONT_HERSHEY_TRIPLEX, 1.5,0, 2
    cv2.putText(bg, department, org, font, scale, color, thick)


    #name = ""
    org, font, scale, color, thick = (40,550), cv2.FONT_HERSHEY_COMPLEX_SMALL , 2,(255,255,255), 3
    cv2.putText(bg, user_full_name, org, font, scale, color, thick)


    #issue_date = "May 01 2021"
    org, font, scale, color, thick = (40,610), cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255), 2
    cv2.putText(bg, issue_date, org, font, scale, color, thick)

    #amount = "Rs. 600"
    org, font, scale, color, thick = (40,400), cv2.FONT_HERSHEY_TRIPLEX , 3,0, 5
    cv2.putText(bg, fee_price, org, font, scale, color, thick)



    org, font, scale, color, thick = (650,550), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255), 2
    cv2.putText(bg, 'EXP DATE:', org, font, scale, color, thick)


    #exp_date = "May 30/21"
    org, font, scale, color, thick = (650,600), cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255), 2
    cv2.putText(bg, expiry_date, org, font, scale, color, thick)



    org, font, scale, color, thick = (1000,550), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255), 2
    cv2.putText(bg, 'FROM:', org, font, scale, color, thick)



    org, font, scale, color, thick = (1000,600), cv2.FONT_HERSHEY_COMPLEX , 1,(255,255,255), 2
    cv2.putText(bg, "PointPay", org, font, scale, color, thick)


    #user_profile_pic= cv2.imread('download.png')
    x,y,w,h = 900,40,300,300
    bg[y:y+h, x:x+w] = cv2.resize(user_profile_pic, (w,h))

    #roll_num = "CS-18180"
    org, font, scale, color, thick = (970,400),cv2.FONT_HERSHEY_TRIPLEX,1,0,2
    cv2.putText(bg, roll_num, org, font, scale, color, thick)
    

    random_name = generateRandomCode() + ".jpg"
    # cv2.imwrite(complete_path_to_save, bg)
    ret, buf = cv2.imencode('.jpg', bg)
    content = ContentFile(buf.tobytes())
    
    return {
        "name": random_name,
        "content": content
    }


def getUser(user):
    user_info_query = UserInfo.objects.filter(user=user)
    return user_info_query.first()

def getUserByUid(uid):
    user = UserInfo.objects.filter(uid = uid)
    return user.first()

def getAccountByUser(user):
    try:
        return Account.objects.get(user = user)
    except:
        raise Exception("Student account not found")

def getAccountByOrg(organization):
    try:
        return Account.objects.get(organization = organization)
    except:
        raise Exception("Organization account not found")



def getVoucherByCode(code, user):
    if not code:
        raise Exception("Voucher code is missing!")

    if not user:
        raise Exception("Accessor not provided")

    voucher = Voucher.objects.filter(code = code).first()
    if not voucher:
        raise Exception("Invalid voucher")

    if voucher.organization_id != user.organization_id:
        raise Exception("You can pay vouchers of only your university")

    return voucher
    

def isVoucherAlreadyCreated(user):
    current_date = timezone.now()
    print(current_date.month, current_date.year)
    current_voucher = Voucher.objects.filter(
        organization=user.organization,
        month=current_date.month,
        year=current_date.year
    ).order_by("-created_at")
    return current_voucher.first()


def generateRandomCode():
    from random import randint
    length = 10
    """
    This function will return a string of random
    alphanumeric code of given length (integer)
    """
    CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, length):
        index = randint(0, len(CHAR) - 1)
        code += CHAR[index]
    return code