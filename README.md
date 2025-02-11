# Scooter Reservation Platform – Django, Stripe, Django-Allauth

**A scooter reservation platform with user authentication, booking system, and admin management.**

**Features:**
- Scooter Listings & Booking: Users can browse scooters, view details, and book them.
- Secure Payments: Reservations confirmed via Stripe Checkout, with race condition handling to prevent double bookings.
- User Authentication: Implemented Django-Allauth for registration, login, email verification, password management.
- Custom User Model: Includes an email-based user model with an attached UserProfile model.
- User Dashboard: Users can look up past & manage upcoming reservations, change email/password, and log out.
- Admin Panel: Staff can add/edit/delete scooters, manage all reservations, and access user dashboards.
- Access Control: Normal users can only access their own dashboard, while staff can access any user’s dashboard.
- Testing: Simple tests cover core views and functionalities.