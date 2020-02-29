"# hotel_management" 

Structure:
    Core - contain core django settings
    users - contain user model for admin/receptionist/customers
    hotels - contain functionality for hotel management

Question: Why Customer data wasn't stored in User table?
Answer:     The application is not customer centric, it is receptionist centric. So, the customer is not going to register
            himself before coming to hotel and it would also be complex for receptionist to first create customer and
            then link it to booking table. We can do automatic linking of customer details to user model for future use
            but that is currently unnecessary to the requirements.

