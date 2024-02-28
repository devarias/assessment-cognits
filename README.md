# Assessment Cognits


This README provides guidelines for the Assessment API.

# Content
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running](#running)
- [Routes and Methods](#routes-and-methods)
  - [Customers Routes](#customer-routes)
- [Status Codes](#status-codes)
- [Request exampless](#request-examples)
- [Branches](#branches)
- [Built With](#built-with)
- [Contributors](#contributors)

<br />
To implement this RESTful API you have to follow some instructions and requirements to use it.

# Prerequisites

* `nodejs` => v18.0.0
* `npm` => v8.19.4
* `python` => v3.11
* `pip` => v24.0
* `boto3` => v1.34.50
* `botocore` => v1.34.50
* `pyjwt` => v2.8.0

# Installation

* `git clone https://github.com/devarias/assessment-cognits`
* `cd assessment-cognits`
* `npm install`
* Make sure you have set your AWS Credentials in `~/.aws/credentials`
* Set the env variable JWT_KEY with the following command `npx sst secrets set JWT_KEY {variable_value}` 
* Everything is installed and ready to run.

# Running

* `npm run dev`
  * This command will deploy the infrastructure as a local environment, and it will show the api url to make requests.
* `npm run remove`
  * This command will delete the infrastructure deployed.

# Routes and Methods

* ## Customer Routes

| Route                                  |  Method  | Description                               |
| -------------------------------------- | :------: | ----------------------------------------- |
| `{apiUrl}/{stage}/customers`           |  `get`   | To get all the data of the customers      |
| `{apiUrl}/{stage}/customers`           |  `post`  | To create a new customer                  |
| `{apiUrl}/{stage}/customers/{id}`      | `delete` | To delete an existing customer            |
| `{apiUrl}/{stage}/customers/{id}`      |  `get`   | To get the data about a specific customer |
| `{apiUrl}/{stage}/customers/{id}`      |  `put`   | To update an existing customer            |
| `{apiUrl}/{stage}/customers/{id}/image`|  `post`  | To upload a image of an existing customer |
<br />

# Status Codes

| HTTP Status Code |                                     Description                                     |
| :--------------: | :---------------------------------------------------------------------------------: |
|      `200`       |             Successfully response by a `get` method used in an endpoint             |
|      `201`       |            Successfully response by a `post` method used in an endpoint             |
|      `400`       | Response by a `get`, `post` or `put` method used in an endpoint with an specific id |
|      `404`       | Response by a `get`, `post` or `put` method used in an endpoint with an specific id |
<br />

# Request examples

* Get one customer
```
curl --location '{baseUrlDev}/customers/{id}' \
--header 'Authorization: {token}'
```
* Get all customers with filters, querystring parameters are optional
```
curl --location '{baseUrlDev}/customers?postalCode=value&firstName=value&lastName=value&country=value&city=value' \
--header 'Authorization: {token}'
```
* Create one customer
```
curl --location '{baseUrlDev}/customers' \
--header 'Authorization: {token}' \
--header 'Content-Type: application/json' \
--data '{
    "city": "string",
    "firstName": "string",
    "lastName": "string",
    "country": "string",
    "postalCode": "string",
    "customerId": "string"
}'
```
* Update one customer
```
curl --location '{baseUrlDev}/customers/{id}' \
--header 'Authorization: {token}' \
--header 'Content-Type: application/json' \
--data '{
    "city": "string",
    "firstName": "string",
    "lastName": "string",
    "country": "string",
    "postalCode": "string",
    "customerId": "string"
}'
```
* Delete one customer
```
curl --location --request DELETE '{baseUrlDev}/customers/{id}' \
--header 'Authorization: {token}'
```
* Upload image for a customer
```
curl --location '{baseUrlDev}/customers/{id}/image' \
--header 'Authorization: {token}' \
--header 'Content-Type: image/jpeg' \
--data 'image.jpeg'
```


# Branches

* `dev` => development environment
* `uat` => uat environment for QA
* `main` => production environment

# Built With

  * NodeJS
  * Python 3.11
  * boto3
  * CDK
  * SST.dev
  * npm
  * AWS

# Contributors

<div align='center'>
  <div>
    <table>
      <tr>
        <td valign="top" align='center'>
          <a href="https://github.com/devarias" target="_blank">
            <p>David Arias Fuentes</p>
            <img alt="github_page" src="https://avatars.githubusercontent.com/u/61300552?v=4" height="80" width="80"/>
          </a>
          <br />
          <a href="https://www.linkedin.com/in/devarias/" target="_blank" rel="noopener noreferrer">
            <img src="https://img.icons8.com/plasticine/100/000000/linkedin.png" width="35" />
          </a>
        </td>
      </tr>
    </table>
  </div>
</div>
