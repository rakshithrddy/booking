# BookMyCab - Booking app

Simply booking app created with Pyton, Flask frame with Relational Database.

## Table of Content

* [Technologies](#technologies)
* [Setup](#setup)
* [Configurations](#configurations)
* [Usage](#usages)
  * [api](#api-endpoints)
  * [pages](#pages)
* [Calculations](#calculations)
  * [Distance](#distance)
  * [Pricing](#pricing)

### Technologies

* Python 3.7
* Flask
* HTML 5
* JavaScript
* Sqlite
* Stripe payment gateway.

### Setup

```
$ pip install -r requirements.txt
```

### Configurations

* Environment Variables
  * **SECRET_KEY** = Set SECRET_KEY to custom and highly secure value.
  * **STRIPE_PUBLIC_KEY** = Set STRIPE_PUBLIC_KEY provided by Stripe.
  * **STRIPE_SECRET_KEY** = Set STRIPE_SECRET_KEY provided by Stripe.

### Usages

#### API Endpoints

* /api/driver/<int:id> -> Returns the driver object with id as a unique identifier. 
  * **GET** Method
  * Returns Json data if successful.
    
    ```json
      {
          "id": 1,
          "name": "Sam",
          "about": "I am an Astronaut",
          "language": "English",
          "cost_per_km": 12
      }
    ```

* /api/driver -> To create a new driver object.
  
  * **POST** method.
  * Mandatory Fields: name
  * Returns a json data with ID field if successful.
    ```json
    {
       "name": "Sam",
       "about": "I am an Astronaut",
       "language": "English",
       "cost_per_km": 12
    }
    ```

* /api/driver/<int:id>  -> To update the details of the existing driver.
  * **Allowed** **modifications**: **about, language, Cost per km**.
  * **PUT** Method.
  * Returns a json data if successful.
    ```json
    {
       "about": "I am an Astronaut",
       "language": "Hindi",
       "cost_per_km": 20
    }
    ```

### Pages

#### /
The home page or index page takes in 4 fields namely:
* Trip Type
* Depart From
* Depart To
* Departure Date

The **trip type** is by default One way. **Depart from** is always fixed to Bangalore.
**Depart To** is a list of options from which a customer can choose from. **Departure Date**
give a date picker options.
**Departure Date** raise an error if the customer picks the older dates to book.

#### /driver_select
The driver select page has 3 fields.
* Language
* Driver with price
* Car

**Language** is a list of options with 3 languages namely Kannada, Hindi and English. 
When a customer chooses a language the **driver with price** will be populated with the drivers
who knows the language.
**Driver with price** field displays Driver name and price the driver charges per km.
**Car** field allows to choose car type. By default the car name is fixed.

#### /book
Book page has 2 fields.
* Pick Up Address
* Pick Up Time
**Pick Up Address** field takes in specific place name within the city.
**Pick Up Time** field takes in time in hours:min AM:PM format.

### /confirm
Displays all the details of the booking process.
Ones the book button is clicked the page is forwarded to **strip** payment gate.

### /thanks
If the payment is confirmed thanks page will be rendered. 
Ones the payment is confirmed all the booking details will be committed to the database and 
a unique ticked ID will be generated.

## Calculations

### Distance
The distance is **calculated based on Latitude and longitude of all the major cities in India. Since the **Trip Type** is **One Way** the distance is fixed.
Note: The distance can have an error rate of 0.5%.

#### Pricing

The pricing of trip is based on the **distance** and the **cost per km** put up by the driver.
```text
    Cost per km: 15 rs
    Distance from Bangalore to Mumbai: 850 kms
    Total Trip Cost: 850 * 15 = 12,750 Rs
```
Note: Pricing is set to **operationally optimized** meaning the return trip charges are not considered.