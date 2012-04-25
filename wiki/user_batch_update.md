

## 10. users batch update

Update Users Information

### URL

[https://api.uas.sdo.com/v1/users/update](https://api.uas.sdo.com/v1/users/update  "users.update")


### Parameters
Request Parameters  |  Optional  |  Type   |  Description  
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

        "uid": "87c09c8c-8b82-4e9f-a982-ec577074db4b",

        "name": "Tom",

        "gender": "Male",

        ......

        ####end base Profile####

        "blood": "O"  ,

        "marry": "YES"  ,

        tel_numbers:[
            {
                "tel_number":  "13512345678",

                "tel_type": "work",

                ......

            },{
                "tel_number":  "13588888888",

                "tel_type": "home",

                ......

            }
        ],

        avatars:[],

        ring_tones:[],

        locations:[],

        ...
    }

