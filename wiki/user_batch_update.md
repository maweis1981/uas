

## 10. users batch update

Update Users Information

### URL

[https://api.uas.sdo.com/v1/users/update](https://api.uas.sdo.com/v1/users/update  "users.update")


### Parameters
Request Parameters  |  Optional  |  Type   |  Description  
--------|----------|-----------|--------------
accessToken			|  False	 |  String |  
userData            |  True	     |  String |  User's Data in JSON Format  
count 				|  int       |  int    |  how many users you batch update .  

### Support Format

JSON

### HTTP Request Method

POST

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