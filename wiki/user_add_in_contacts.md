

## user add contact

User add contact  

### URL

[https://api.uas.sdo.com/v1/user/{uid}/add_contact](https://api.uas.sdo.com/v1/user/{uid}/add_contact  "user.add_contact")


### Parameters
Request Parameters  |  Optional  |  Type   |  Description  
--------|----------|-----------|--------------
accessToken			|  False	 |  String |  
uid            |  True	     |  String |  user's uid in our system
tel_number            |  True	     |  String |  user's telephone number
email            |  True	     |  String |   user's email

uid, tel_number, email at least has one
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

JSON Example


    {

    	"code": 200,  

		"message": "successful"  
		
	}




[1]: http://auth.uas.sdo.com/how_to_auth "如何登录授权"
[2]: http://auth.uas.sdo.com/about_rates "访问频度限制"