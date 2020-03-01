##### Structure:
   1. core - contain core django settings
   2. users - contain user model for admin/receptionist/customers
   3. hotels - contain functionality for hotel management

###### Why Customer data wasn't stored in User table?
> The application is not customer centric, it is receptionist centric. So, the customer is not going to register
            himself before coming to hotel and it would also be complex for receptionist to first create customer and
            then link it to booking table. We can do automatic linking of customer details to user model for future use
            but that is currently unnecessary to the requirements.

> Due to above fact, also assuming that 1 customer would book 1 room. If a customer books multiple room
> in current db design then we are going to need customer data in user model to prevent redundancy in booking table.

######Things that could have been done better with more time
>1. CSS 
>2. Validation on user submitted data. As of now, it is assumed that  user will enter correct data.
>3. Docker implementation. Although I have previously done docker implementation for similar project: https://github.com/Waterbyte/dockerizedLoanSystem
>4. Edit Room and Edit Room Type

#####Reproduction steps:
>1. Create virtualenv
>2. pip install -r requirements.txt
>3. py manage.py migrate
>4. py manage.py loaddata fixture.json
>5. Password for admin and receptionist can be found in notes 