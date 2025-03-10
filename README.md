# Scooter Reservation Platform

**A scooter rental reservation platform with user authentication, booking system, and admin management. | Django, Stripe, Django-Allauth**

## **Setup & Installation**
When you download and clone the repository to your IDE, please run these commands to make sure everything is ready to use and works well.
1. python -m venv venv
2. source venv/bin/activate (on Linux/macOS, on Windows; venv\Scripts\Activate)
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py create_db_objects
6. python manage.py runserver
7. stripe listen --forward-to http://localhost:8000/reservations/stripe_webhook/  (If you have different port for localhost, please adjust it)

**Features:**
- Scooter Listings & Booking: Users can browse scooters, view details, and book them.
- Secure Payments: Reservations confirmed via Stripe Checkout, with race condition handling to prevent double bookings.
- User Authentication: Implemented Django-Allauth for registration, login, email verification, password management.
- Custom User Model: Includes an email-based user model with an attached UserProfile model.
- User Dashboard: Users can look up past & manage upcoming reservations, change email/password, and log out.
- Admin Panel: Staff can add/edit/delete scooters, manage all reservations, and access user dashboards.
- Access Control: Normal users can only access their own dashboard, while staff can access any user’s dashboard.
- Testing: Simple tests cover core views and functionalities.
- Database fill: Custom create_db_objects command, populates the database with test data, including users, scooters, reservations and a superuser account.
