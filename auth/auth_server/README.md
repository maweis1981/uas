Auth Server:

    Clients :
    Scopes:
    Users:
    Tokens:

Application Developer Flow:

/auth/reg  : register a user as developer,
/auth/create create an application,

/oauth/auth : client identifier & response type -> get access token

/oauth/token :  request the access token for user & application via much more method
                grant_type & refresh token ./etc


store the access token in your application,
access the api with access token.

APIs Server:
    Write a decorators to check the access token is valid.
