# jd
JD 京东茅台，华为手机 23年 10月   最新可用

# 2023-10-2日最新更新，最新算发解析

抓包分析过程：
# 1.genToken  -to  body 携带参数：{"action":"to","to":"https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D100012043978%26from%3Dapp"}
# 2.jmp -https://divide.jd.com/user_routing?skuId=100012043978&from=app
# 3.divide
# 4.captcha
# 5.POST https://marathon.jd.com/seckillnew/orderService/init.action HTTP/1.1
# 6.提交订单，
  提交接口为：POST https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=100012043978 HTTP/1.1
  提交参数为：               
        "num": ,
        "addressId":
        "yuShou": 
        "isModifyAddress":
        "name": 
        "provinceId":
        "provinceName":
        "cityId": 
        "cityName": 
        "countyId": 
        "countyName": 
        "townId": 
        "townName": 
        "addressDetail": 
        "mobile": 
        "mobileKey": 
        "email": "",
        "invoiceTitle":
        "invoiceContent": 
        "invoicePhone": 
        "invoicePhoneKey": 
        "invoice": 
        "codTimeType": 
        "paymentType": 
        "overseas": 
        "token":
  现在的订单接口已经不需要SK~
  OK 搞定~~
赞助邮箱：2335625964@qq.com  （如果QQ添加失败可以把你的联系方式发送到邮箱，我会加你。)
