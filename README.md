/auth/register/    
method : POST   
```
sample:
{
    "username" : "test",
    "email" : "test@gmail.com",
    "password" : "testpass1",
    "password2" : "testpass1"
}
```
---
/api/     
/api/videos/  
/api/videos/accessible_videos/  
/api/videos/<video_id:pk>/watch_video/  
/api/comment/    
/api/subscription-types/  
/api/subscriptions/  
/api/subscriptions/purchase_subscription/    
```
{   
    "subscription_type" : 1
}
```
/api/history/  
/api/wallet/charge_wallet/    
```
{   
    "charge" : 1000,
    "renewal" : true
}
```


