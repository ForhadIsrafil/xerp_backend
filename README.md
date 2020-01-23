
#xerp-API (2019)

## Base url: http://127.0.0.1:8000/api/v1/

By using the following endpoint, URL is formed by baseurl + endpoint and API communication is performed.


## Main endpoints

| Endpoint name |  Link  | Method |  Purpose |  
|---|---|---|---|---|---|---|
 
|  SignIn | /signin | POST | For login into system |  
|  Get User Info | /user/<int:user_id> | GET | For user info |   
|  SignUp | /signup | POST | For user registration |   
|  Active Users  | /active-account | POST | Active registered users |   
|  Signout | /signout | POST | Signout users |   
|  Recover password | /forget-password | POST | Get password recovery url email |   
|  Reset Password | /reset-password | POST | Reset lost password |   
|  Change password | /change-password | PATCH | Change user existing password |   
|  Upload | /upload | POST | Upload files |   
|  Update profile | /update-profile | POST | Update user system info |   
|  Create company | /company/create | POST | Create company(name) |   
|  Company info | /company/<int:company_id> | GET | Get company info |   
|  Get companies-user info | /company/user/<int:user_id> | GET | Get company info by user |  
 
|  Get or create companies-user info | /project | POST/GET | Get company info by user |   
|  Get companies-single project info | /project/<int:id> | GET | Get single project info|  
|  Update or Delete companies-user info | /project/<int:id> | PATCH/DELETE | update/delete project info|  
|  Get companies-user info | /company/<int:company_id>/project> | GET | Get single user's project list|  
 
|  Get or create companies-goals info | /goal | POST/GET | Get or create company goal info by user |   
|  Update or Delete companies-user info | /goal/<int:id> | PATCH/DELETE | update/delete goal info by user |   

|  Get or create tasks | /task | POST/GET | Get or create task info |   
|  Update or Delete task info | /task/<int:id> | PATCH/DELETE | Update or Delete task info by user |  
 
|  Create or get task-details | /task-details | POST/GET | Create or get task-details info by user |   
|  Update or Delete task-details | /task-details/<int:id> | PATCH/DELETE | Update or Delete details | 
  
|  Create or get issues | /issue  | POST/GET | Create or get issues by user |   
|  Update or Delete single issues | /issue/<int:id> | PATCH/DELETE | Update or Delete issues by user |  
 
|  Create or get issue-details | /issue-details | POST/GET | Create or get issues-details |   
|  Update or Delete issue-details | /issue-details/<int:id> | PATCH/DELETE | Update or Delete issues-details | 
  
|  Create or get task-issue-resulation | /task-issue-resulation | POST/GET | Create or get task-issue-resulation by user |   
|  Update or Delete task-issue-resulation | /task-issue-resulation/<int:id> | PATCH/DELETE | Update or Delete task-issue-resulation by user | 
  
|  Create or get license | /license | POST/GET | Create or get license by user |   
|  Update or Delete single license | /license/<int:id> | PATCH/DELETE | Update or Delete single license by user |
   
|  Create or get department-model-permission | /department-model-permission | POST/GET | Create or get department-model-permission |   
|  Update or Delete department-model-permission | /department-model-permission/<int:id> | PATCH/DELETE | Update or Delete department-model-permission by user | 
  
|  Create or get department-role-model-permission | /department-role-model-permission | POST/GET | Create or get department-role-model-permission by user |   
|  Update or Delete department-role-model-permission | /department-role-model-permission/<int:id> | PATCH/DELETE | Update or Delete department-role-model-permission by user |
   
|  Un-follow tasks | /task-unfollow/<int:task_id> | DELETE | Un-follow tasks by user |  
|  CRUD DepartmentRoleModelPermission | /department-role-model-permission-crud/<int:user_id> | POST/GET/PATCH/DELETE | DepartmentRoleModelPermission by user |   
|  Get get-user-permissions | /get-user-permissions | GET | Get get-user-permissions by super-user |   
|  Update-user-permission | /update-user-permission | POST | Update-user-permission by super-user |   

  
 
##### Sample response list for Whole project:

1. HTTP_201_CREATED
2. HTTP_400_BAD_REQUEST
3. HTTP_401_UNAUTHORIZED
4. HTTP_403_FORBIDDEN
5. HTTP_415_UNSUPPORTED_MEDIA_TYPE
6. HTTP_409_CONFLICT
7. HTTP_404_NOT_FOUND
8. HTTP_204_NO_CONTENT
9. HTTP_500_INTERNAL_SERVER_ERROR
10. HTTP_200_OK



### HTTP REQUEST :  **POST  /signin**

###### params
```json
{
    "email":"knzd@phpbb.uu.gl",
    "password":"123456"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| email       | true | |
| password    | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 13,
    "first_name": "Mr",
    "last_name": "lota",
    "full_name": "Mr lota",
    "email": "lota@eyeemail.com",
    "is_active": true,
    "token": "88b956d724e9bee71f5bf24d0b4effa2a4361658",
    "image_url": null,
    "is_2f_auth_enabled": false,
    "authy_id": "156854986",
    "company": {
        "id": 11,
        "name": "lota",
        "address": null
    },
    "department": 6
}
```

### HTTP REQUEST :  **GET  /user/<int:user_id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "user_id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |



###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 13,
    "first_name": "Mr",
    "last_name": "lota",
    "full_name": "Mr lota",
    "email": "lota@eyeemail.com",
    "is_active": true,
    "token": "88b956d724e9bee71f5bf24d0b4effa2a4361658",
    "image_url": null,
    "is_2f_auth_enabled": false,
    "authy_id": "156854986",
    "company": {
        "id": 11,
        "name": "lota",
        "address": null
    },
    "department": 6
}
```

### HTTP REQUEST :  **POST  /signup**

###### params

```json
{ 
	"email":"lota@eyeemail.com",
	"password":"123456", 
	"first_name":"Mr", 
	"last_name":"lota",
	"cellphone": "01558191553",
	"company_name": "lota"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| email        | true | |
| password     | true | |
| first_name   | true | |
| last_name    | true | |
| cellphone    | true | |
| company_name | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 2,
    "email": "yuyeyan@tech5group.com",
    "first_name": "Mr",
    "last_name": "yuyeyan"
}
```

### HTTP REQUEST :  **POST  /active-account**

###### params
```json
{
	"security_code":"a7N58"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| security_code | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 13,
    "first_name": "Mr",
    "last_name": "lota",
    "full_name": "Mr lota",
    "email": "lota@eyeemail.com",
    "is_active": true,
    "token": "88b956d724e9bee71f5bf24d0b4effa2a4361658",
    "image_url": null,
    "is_2f_auth_enabled": false,
    "authy_id": "156854986",
    "company": {
        "id": 11,
        "name": "lota",
        "address": null
    },
    "department": 6
}
```

### HTTP REQUEST :  **POST  /signout**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
}
```
 
### HTTP REQUEST :  **POST  /forget-password**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
  "email": "knzd@phpbb.uu.gl"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| email       | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "email": "knzd@phpbb.uu.gl",
    "security_code": "ZEZmA"
}
```

### HTTP REQUEST :  **POST  /reset-password**

###### params
```json
{
	"security_code": "oeriut",
	"password": "123456"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| security_code  | true | |
| password       | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
}
```

### HTTP REQUEST :  **PATCH  /change-password**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"new_password": "123456"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| new_password | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
}
``` 

### HTTP REQUEST :  **POST  /upload**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"file": "image.jpg"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| file        | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "link" : 'https://s3.amazonaws.com/1-bucket_name/asjgf65465safsf'
}
``` 

### HTTP REQUEST :  **POST  /update-profile**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"first_name": "abc",
	"last_name": "def"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| first_name  | true | |
| last_name   | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "first_name": "Mr",
    "last_name": "yuyeyan",
    "full_name": "Mr yuyeyan",
    "email": "knzd@phpbb.uu.gl",
    "is_active": true,
    "token": "a061e8c31f11c1b2ecb0cc94f25b9f26cdaa53cb",
    "image_url": null
}
``` 

### HTTP REQUEST :  **POST  /company/create**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": "1",
	"name": "company"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| name        | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": "1",
	"user_id": "1",
	"name": "company"
}
``` 
    
### HTTP REQUEST :  **GET  /company/<int:company_id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"company_id": "1"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| company_id  | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": "1",
	"user_id": "1",
	"name": "company"
}
``` 

### HTTP REQUEST :  **GET  /company/user/<int:user_id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": "1"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id  | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
[
    {
        "id": 1,
        "name": "company",
        "user_id": 1
    }
]
``` 

### HTTP REQUEST :  **POST  /project**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"company": 6,
	"start_date":"2019-08-27",
	"end_date":"2019-09-27",
	"text":"Planning, research & development",
	"name": "Project One"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| text        | true | |
| start_date  | true | |
| end_date    | true | |
| name        | true | |
| company     | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 8,
    "start_date": "2019-08-27",
    "end_date": "2019-09-27",
    "text": "Planning, research & development",
    "name": "Project One"
}
``` 

### HTTP REQUEST :  **GET  /project**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{

}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "start_date": "2019-05-23",
            "end_date": "2019-07-26",
            "text": "project__1"
        }
    ]
}
``` 

### HTTP REQUEST :  **GET  /company/<int:company_id>/project**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{

}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "start_date": "2019-05-23",
            "end_date": "2019-07-26",
            "text": "project__1"
        }
    ]
}
```

### HTTP REQUEST :  **PATCH  /project/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"text": "project....__1",
	"start_date": "2019-05-23",
	"end_date": "2019-07-26",
	"name": "Project Title"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| text          | true | |
| start_date    | true | |
| end_date      | true | |
| id            | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{    
    "id": 1,
	"text": "project....__1 updated",
	"start_date": "2019-05-23",
	"end_date": "2019-07-26",
	"name": "Project Title"
}
``` 

### HTTP REQUEST :  **DELETE  /project/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /goal**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"name": "Goal Title",
	"details": "Goal description",
	"project": 1,
	"start_date": "2019-05-23",
	"end_date": "2019-07-26"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| project          | true | |
| start_date       | true | |
| end_date         | true | |
| name             | true | |
| details          | false| |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 2,
    "project": 1,
    "name": "Goal Title",
    "details": "Goal Description",
    "start_date": "2019-05-23",
    "end_date": "2019-07-26"
}
``` 
### HTTP REQUEST :  **GET  /goal**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Goal Title",
            "details": "Goal Description",
            "project": 1,
            "start_date": "2019-05-23",
            "end_date": "2019-07-26"
        }
    ]
}
``` 

### HTTP REQUEST :  **GET  /goal/project/<int:project_id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Goal Title",
            "details": "Goal Description",
            "project": 1,
            "start_date": "2019-05-23",
            "end_date": "2019-07-26"
        }
    ]
}
```

### HTTP REQUEST :  **PATCH  /goal/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"name": "Goal Title Changed",
	"details": "Goal Description changed",
	"start_date": "2019-06-27",
	"end_date": "2019-08-27",
	"last_updated_by": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| last_updated_by  | true | |
| id               | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 2,
    "project": 1,
    "name": "Goal Title Changed",
    "details": "Goal Description changed",
    "start_date": "2019-05-23",
    "end_date": "2019-07-26"
}
``` 

### HTTP REQUEST :  **DELETE  /goal/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /task**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"goal": 2,
	"owner": 1,
	"start_date": "2019-05-23",
	"end_date": "2019-07-26"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| goal          | true | |
| owner         | true | |
| start_date    | true | |
| end_date      | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 8,
    "status": true,
    "priority": true,
    "goal": 2,
    "owner": 1,
    "start_date": "2019-05-23",
    "end_date": "2019-07-26"
}
``` 
### HTTP REQUEST :  **GET  /task**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 8,
            "status": true,
            "priority": true,
            "goal": 2,
            "owner": 1,
            "start_date": "2019-05-23",
            "end_date": "2019-07-26"
        }
    ]
}
``` 

### HTTP REQUEST :  **GET  /task/goal/<int:goal_id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 8,
            "status": true,
            "priority": true,
            "goal": 2,
            "owner": 1,
            "start_date": "2019-05-23",
            "end_date": "2019-07-26"
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /task/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"goal": 2,
	"owner": 1,
	"start_date": "2019-05-23",
	"end_date": "2019-07-26"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| goal        | true | |
| owner       | true | |
| start_date  | true | |
| id          | true | |


###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 8,
    "status": true,
    "priority": true,
    "goal": 2,
    "owner": 1,
    "start_date": "2019-05-23",
    "end_date": "2019-07-26"
}
``` 

### HTTP REQUEST :  **DELETE  /task/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /task-details**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"task": 8,
	"comment": "comments...",
	"path": ""

}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task          | true | |
| comment       | true | |
| path          | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "task": "8",
    "comment": "task comment__1",
    "path": null
}
``` 
### HTTP REQUEST :  **GET  /task-details**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "task": 8,
            "comment": "task comment__1",
            "path": null
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /task-details/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"task": 1,
	"comment": "comment updated...."
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task        | true | |
| comment     | true | |
| id          | true | |



###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "task": 8,
    "comment": "comment updated....",
    "path": null
}
``` 

### HTTP REQUEST :  **DELETE  /task-details/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /issue**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "title": "issue___1",
    "description": "issue details.....",
    "path": null,
    "classification": "",
    "task": 1,
    "project": 1,
    "updated_by": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| title           | true | |
| description     | true | |
| path            | true | |
| classification  | true | |
| task            | true | |
| project         | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "title": "issue___1",
    "description": "issue details.....",
    "path": null,
    "classification": "",
    "task": "8",
    "project": "1",
    "updated_by": 1
}
``` 
### HTTP REQUEST :  **GET  /issue**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "issue___1",
            "description": "issue details.....",
            "path": null,
            "classification": "",
            "task": 8,
            "project": 1,
            "updated_by": 1
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /issue/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "title": "title......................................",
    "description": "desssssssssssss",
    "path": null,
    "classification": "",
    "task": 8,
    "project": 1,
    "updated_by": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| title          | true | |
| description    | true | |
| path           | true | |
| classification | true | |
| task           | true | |
| project        | true | |
| id             | true | |



###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "title": "title......................................",
    "description": "desssssssssssss",
    "path": null,
    "classification": "",
    "task": 8,
    "project": 1,
    "updated_by": 1
}
``` 

### HTTP REQUEST :  **DELETE  /issue/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /issue-details**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "task": 8,
    "comment": "issue-details comments",
    "path": ""

}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task           | true | |
| comment        | true | |
| path           | true | |



###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "task": "8",
    "comment": "issue-details comments"
}
``` 
### HTTP REQUEST :  **GET  /issue-details**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "task": 8,
            "comment": "issue-details comments"
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /issue-details/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "task": 8,
    "comment": "update comment...",
    "path": ""
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task       | true | |
| comment    | true | |
| path       | true | |
| id         | true | |




###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "task": 8,
    "comment": "update comment..."
}
``` 

### HTTP REQUEST :  **DELETE  /issue-details/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 


### HTTP REQUEST :  **POST  /task-issue-resulation**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{

    "task": 8,
    "comment": "/task-issue-resulation comment _______1",
    "path": "",
    "updated_by": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task           | true | |
| comment        | true | |
| path           | true | |
| updated_by     | true | |



###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "task": "8",
    "comment": "/task-issue-resulation comment _______1",
    "path": null,
    "updated_by": 1
}
``` 
### HTTP REQUEST :  **GET  /task-issue-resulation**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "task": 8,
            "comment": "/task-issue-resulation comment _______1",
            "path": null,
            "updated_by": 1
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /task-issue-resulation/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "task": 8,
    "comment": "/task-issue-resulation comment _______updated__1",
    "path": "",
    "updated_by": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task       | true | |
| comment    | true | |
| path       | true | |
| updated_by | true | |
| id         | true | |




###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "task": 8,
    "comment": "/task-issue-resulation comment _______updated__1",
    "path": "",
    "updated_by": 1
}
``` 

### HTTP REQUEST :  **DELETE  /task-issue-resulation/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /license**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "company": 1,
    "model": "model name..."
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| company     | true | |
| model       | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "company": 1,
    "model": "model name..."
}
``` 
### HTTP REQUEST :  **GET  /license**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "company": 1,
            "model": "model name..."
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /license/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "company": 1,
    "model": "model name...updated"
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| company  | true | |
| model    | true | |
| id       | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "company": 1,
    "model": "model name...updated"
}
``` 

### HTTP REQUEST :  **DELETE  /license/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /department-model-permission**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "department": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| department      | true | |
| model           | true | |
| permission      | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "model": 1,
    "permission": 1
}
``` 
### HTTP REQUEST :  **GET  /department-model-permission**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "department": 1,
            "model": 1,
            "permission": 1
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /department-model-permission/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{

    "department": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| department  | true | |
| model       | true | |
| permission  | true | |
| id          | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **DELETE  /department-model-permission/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /department-role-model-permission**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| department      | true | |
| role            | true | |
| model           | true | |
| permission      | true | |


###### output

### possible response list:

1. HTTP_201_CREATED ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
``` 
### HTTP REQUEST :  **GET  /department-role-model-permission**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "department": 1,
            "role": 1,
            "model": 1,
            "permission": 1
        }
    ]
}
``` 

### HTTP REQUEST :  **PATCH  /department-role-model-permission/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
    "id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 2
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| department  | true | |
| role        | true | |
| model       | true | |
| permission  | true | |
| id          | true | |

###### output

### possible response list:

1. HTTP_200_OK ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **DELETE  /department-role-model-permission/<int:id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| id          | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **DELETE  /task-unfollow/<int:task_id>**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"task_id": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| task_id     | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **POST  /department-role-model-permission-crud**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| department  | true | |
| role        | true | |
| model       | true | |
| permission  | true | |


###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **GET  /department-role-model-permission-crud**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| department  | true | |
| role        | true | |
| model       | true | |
| permission  | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **PATCH  /department-role-model-permission-crud**   [ONLY MADE BY SUPER ADMIN]

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| department  | true | |
| role        | true | |
| model       | true | |
| permission  | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **DELETE  /department-role-model-permission-crud**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "department": 1,
    "role": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| department  | true | |
| role        | true | |
| model       | true | |
| permission  | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 


### HTTP REQUEST :  **POST  /user-model-permission-crud**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| model       | true | |
| permission  | true | |


###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "user": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **GET  /user-model-permission-crud**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| model       | true | |
| permission  | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "user": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **PATCH  /user-model-permission-crud**   [ONLY MADE BY SUPER ADMIN]

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| model       | true | |
| permission  | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "id": 1,
    "user": 1,
    "model": 1,
    "permission": 1
}
``` 

### HTTP REQUEST :  **DELETE  /user-model-permission-crud**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 1,
    "model": 1,
    "permission": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| model       | true | |
| permission  | true | |

###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{

}
``` 

### HTTP REQUEST :  **GET  /get-user-permissions**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"app_id": 1,
	"user_id": 8,
	"department_id": 7
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id     | true | |
| department  | true | |
| app_id      | true | |


###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json
{
    "models_permissions": [
        {
            "model": 4,
            "model_name": "User",
            "permission": 1,
            "permission_name": "View",
            "allow": true
        },
        {
            "model": 8,
            "model_name": "UserAWSBucketInfo",
            "permission": 1,
            "permission_name": "View",
            "allow": false
        },
        {
            "model": 23,
            "model_name": "Company",
            "permission": 1,
            "permission_name": "View",
            "allow": true
        },
        {
            "model": 11,
            "model_name": "Project",
            "permission": 1,
            "permission_name": "View",
            "allow": true
        }
    ]

}
``` 

### HTTP REQUEST :  **POST  /update-user-permission**

###### header
```
{
   "Authorization":"Token fd303bef03c9a1e199041854d1230c50ebff0735"      
}
```

###### params
```json
{
	"user_id": 8,
	"model_id": 13,
	"permission_id": 1,
	"allow": 1
}
```

| parameter | is required | comment |
| :---------: | :---: | :-----------: | :-------: | :----------- |
| user_id        | true | |
| model_id       | true | |
| permission_id  | true | |
| allow          | true | |


###### output

### possible response list:

1. HTTP_204_NO_CONTENT ----- success
2. HTTP_400_BAD_REQUEST ----- Required fields not given 

``` json

``` 

