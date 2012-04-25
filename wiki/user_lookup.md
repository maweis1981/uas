

## 1. lookup

lookup user id uri

### URL

[https://api.uas.sdo.com/v1/users/lookup](https://api.uas.sdo.com/v1/users/lookup "users.lookup")


### Parameters ###

Request Parameters  |  Optional     |  Type   |  Description       
-------------|-----------|---------|--------
access_token | False        | String        |  |
tel_number	|	True	| String	|	User's Telephone Number	|
email	|	True	|	String	|	User's Email


### Support Format

JSON

### HTTP Request Method

GET

### Authorization

YES


About Authorization [authorization][1]

### Access Limits

Level: General
Rates Limits: YES


About Rates Limits [Rates Limit][2]

### Response

Just Response Base Profile  

JSON Example


    {
        count: 1,

        offset: 1,

        limit: 1,

        users:[
        {
            "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

            "tel_number": "13812345678",

            "email": "mawei02@snda.com",

            ......
        }
    }






[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"