#Errors:

## 1. Uniform Error Response

### Response

JSON Example


    {
        "error":  {

            "message": "(#401) Error Message",

            "type": "Exception Type",

            "code": 401
        }
    }

Exceptions:

| --------------------------------|  
|  code  |  message    |  type  |  
|  401   |  Forbidden  |  Auth  |  
|  701   |  Over Limits|  Rates |  
...




[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"
