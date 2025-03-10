from datetime import timedelta, date

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import transaction

from scooters.models import Scooter
from reservations.models import Reservation


User = get_user_model()


class Command(BaseCommand):
    help = "Fill the database with objects, create superuser and user accounts."

    @transaction.atomic
    def handle(self, *args, **options):
        if (
            User.objects.filter(email='admin@gmail.com').exists() or
            Scooter.objects.filter(registration_number='TEST111').exists() or
            Reservation.objects.filter(startdate=date.today() - timedelta(days=5), payment_status=True).exists()
            ):
            self.stdout.write('\033[33m>>>>>>>\033[0m')
            self.stdout.write('There are already some objects in the database.')
            self.stdout.write('\033[33m>>>>>>>\033[0m')
            return
        
        self.stdout.write('\033[33m>>>>>>>\033[0m')
        self.create_users()
        self.stdout.write('\033[33m>>>>>>>\033[0m')
        self.stdout.write('Superuser account created')
        self.stdout.write('\033[33m>>>>>>>\033[0m')
        self.create_scooters()
        self.stdout.write('Scooters created')
        self.stdout.write('\033[33m>>>>>>>\033[0m')
        self.create_reservations()
        self.stdout.write('Reservations created')
        self.stdout.write('\033[33m>>>>>>>\033[0m')


    def create_users(self):
        superuser = User.objects.create_superuser(
            email = 'admin@gmail.com',
            first_name = 'Admin',
            last_name = 'Test',
            phone_number = '+48444555666',
            password='admin'
        )
        superuser.save()
        
        test_user1 = User.objects.create_user(
            email = 'user1@gmail.com',
            first_name = 'user1',
            last_name = 'test',
            phone_number = '+48222111333',
        )
        test_user1.set_password('user')
        test_user1.save()
        
        test_user2 = User.objects.create_user(
            email = 'user2@gmail.com',
            first_name = 'user2',
            last_name = 'test',
            phone_number = '+48666888555'
        )
        test_user2.set_password('user')
        test_user2.save()

        test_user3 = User.objects.create_user(
            email = 'user3@gmail.com',
            first_name = 'user3',
            last_name = 'test',
            phone_number = '+48996443221',
        )
        test_user3.set_password('user')
        test_user3.save()
        self.stdout.write('\n\033[33mSuperuser created:\033[0m\n\033[92memail:\033[0m admin@gmail.com\n\033[92mpassword:\033[0m admin\n\nTest Users created:\nemail: user(1-3)@gmail.com\npassword: user')


    def create_scooters(self):
        img_path = 'images/scooters/KK 215G/peguot.jpg'
        with open(img_path, "rb") as img_file:
            for i in range(1, 4):
                scooter = Scooter.objects.create(
                    brand = str(i)+'Kymco',
                    scooter_model = 'Agility',
                    capacity = 50,
                    year = 2015 + i,
                    registration_number = 'TEST11'+str(i),
                    available = True if i % 2 == 1 else False,
                    image = File(img_file, name='peugot.jpg'),
                    daily_price = 100,
                    weekly_price = 300,
                    monthly_price = 1000,
                    deposit_amount = 200*i,
                )


    def create_reservations(self):
        reservation1 = Reservation.objects.create(
            userprofile = User.objects.filter(email='user1@gmail.com').first().userprofile,
            scooter = Scooter.objects.filter(registration_number='TEST111').first(),
            start_date = date.today() - timedelta(days=5),
            end_date = date.today() - timedelta(days=3),
            payment_status = True,
        )
        reservation2 = Reservation.objects.create(
            userprofile = User.objects.filter(email='user2@gmail.com').first().userprofile,
            scooter = Scooter.objects.filter(registration_number='TEST111').first(),
            start_date = date.today() - timedelta(days=20),
            end_date = date.today() - timedelta(days=15),
            payment_status = True,
        )
        reservation3 = Reservation.objects.create(
            userprofile = User.objects.filter(email='user3@gmail.com').first().userprofile,
            scooter = Scooter.objects.filter(registration_number='TEST113').first(),
            start_date = date.today() - timedelta(days=12),
            end_date = date.today() - timedelta(days=9),
            payment_status = True,
        )
        reservation4 = Reservation.objects.create(
            userprofile = User.objects.filter(email='admin@gmail.com').first().userprofile,
            scooter = Scooter.objects.filter(registration_number='TEST111').first(),
            start_date = date.today() - timedelta(days=60),
            end_date = date.today() - timedelta(days=50),
            payment_status = True,
        )
