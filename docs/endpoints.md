## Public Endpoints
**Careerfair Employers**
`GET /v2/string:careerfair_id/anon_user/employers`
**Version**
`GET /careertalk/version`

## Private Endpointes
All private enpoints require properly signed JWT by CareerTalk.
####  Career fairs Actions

**Employers and Like data**
`GET /v2/<string:careerfair_id>/employers`
**Top5**
`GET /v2/<string:careerfair_id>/top5`

####  Users Actions
**Register User**
`POST /v2/register/student/user`
**Like Careerfair Employer**
`POST /v2/like/<string:careerfair_id>/<string:employer_id>`

## Endpoint Details

### Careerfair Actions
**1. Anonymous Careerfair Employers**
`GET /v2/string:careerfair_id/anon_user/employers`
Required: Nothing
Sample JSON
```
{
    "companies": [
        {
            "careerfair_id": "d9ed6bcd-81ac-4dae-97d5-f0793859994b",
            "degree_requirements": [
                "BS"
            ],
            "employer": {
                "company_url": "2imgroup.com",
                "description": null,
                "found_year": null,
                "hq_city": null,
                "id": "c9e2a6df-817c-423a-932f-8c6b383d471e",
                "logo_url": "default_employer.png",
                "name": "2IM Group, LLC"
            },
            "hiring_majors": [
                "Civil"
            ],
            "hiring_types": [
                "INT",
                "FT"
            ],
            "id": "d6bd1bf8-ed8b-4e0a-8840-557fd854a5be",
            "tables": [],
            "visa_support": "no"
        },
        .
        .
        .
    ],
    "fair": {
        "address": "725 West Roosevelt Road",
        "city": "Chicago",
        "date": "02/13/2019",
        "description": null,
        "end_time": "4:00 PM",
        "id": "d9ed6bcd-81ac-4dae-97d5-f0793859994b",
        "location": "UIC Forum",
        "map_url": null,
        "name": "UIC 2019 Engineering & Computer Science Career Fair",
        "num_of_employers": 104,
        "organization_id": "fa8d282d-1b8a-4a71-b913-200d5c5c0750",
        "other_organization": null,
        "start_time": "12:00 PM",
        "zipcode": "60608"
    },
    "num_of_companies": 104
}
```
**2. Careerfair Employers For Loggedin User**
`GET GET /v2/<string:careerfair_id>/employers`
Required: JWT Token 
Sample JSON
```
{
  "companies": [
    {
      "id": "d6bd1bf8-ed8b-4e0a-8840-557fd854a5be",   
      "careerfair_id": "d9ed6bcd-81ac-4dae-97d5-f0793859994b", 
      "degree_requirements": [
        "BS"
      ], 
      "employer": {
        "company_url": "2imgroup.com", 
        "description": null, 
        "found_year": null, 
        "hq_city": null, 
        "id": "c9e2a6df-817c-423a-932f-8c6b383d471e", 
        "logo_url": "default_employer.png", 
        "name": "2IM Group, LLC"
      }, 
      "hiring_majors": [
        "Civil"
      ], 
      "hiring_types": [
        "INT", 
        "FT"
      ], 
      "is_liked": false, 
      "tables": [], 
      "visa_support": "no"
    }, 
    .
    .
    .
    "fair": {
        "address": "725 West Roosevelt Road",
        "city": "Chicago",
        "date": "02/13/2019",
        "description": null,
        "end_time": "4:00 PM",
        "id": "d9ed6bcd-81ac-4dae-97d5-f0793859994b",
        "location": "UIC Forum",
        "map_url": null,
        "name": "UIC 2019 Engineering & Computer Science Career Fair",
        "num_of_employers": 104,
        "organization_id": "fa8d282d-1b8a-4a71-b913-200d5c5c0750",
        "other_organization": null,
        "start_time": "12:00 PM",
        "zipcode": "60608"
    },
    "num_of_companies": 104

```

### User Actions
**1. Register User**
`POST /v2/register/student/user`
Headers Required:
- email
- given_name
- family_name
- picture
- google_id


This endpoint will return an user information. When the user does not exist the server will create an user and store in the database, otherwise, it will just return the user information.

Sample JSON
```
{
    'personal_email': "some@email.com",
    'google_id': "somegoogleid",
    'profile_url': "some/url.JPG",
    'registered_on': "some utc date time",
    'first_name': "pikachu",
    'last_name': "detective",
    'middle_name': "some middle_name"
    'id': "Primary Key"
}

```


**2. Like Careerfair Employer (Togle)**
`POST /v2/like/<string:careerfair_id>/<string:employer_id>`
Required: JWT Token
This enpoint will toggles the "Like" data. If a student like the employer, this will create "Like" data in the database. If the user hits "like" again, it will remove the like data from the database.

Returns: Some messages




## New endpoints
- get me
- get user by id
- get current career fairs
- get employers by selected fair
- get employer by id
- get my favorites
- toggle like
- save note by employer id
- get top 5 employers


### Sample Fairs
```
[
 {
  address: String!
  city: String!
  date: String!
  description: String!
  end_time: String!
  id: Int!
  location: String!
  map_url: String!
  name: String!
  num_of_employers: Int!
  organization_id: Int!
  start_time: String!
  zipcode: String!
 }
]
```






### Sample Employer
```
{
  careerfair_id: 1,
  degree_requirements: ['BS', 'MS'],
  hiring_majors: ['CS'],
  hiring_types: ['INT', 'FT'],
  tables: [1, 2],
  visa_support: 'no',
  isLiked: true,
  isNote: false,
  likeCount: 35,
  employer: {
    company_url: 'actico.com',
    description: null,
    found_year: null,
    hq_city: null,
    id: 10,
    logo_url: 'default_employer.png',
    name: 'ACTICO'
  }
};
```