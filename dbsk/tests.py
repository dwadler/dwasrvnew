# from django.core.urlresolvers import reverse
from clcdbsk.views import no_root_page
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from .forms import VolunteerCreateForm
from .models import Volunteer
from .views import login, start_page


# models test
class VolunteerTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="dadler", email="dadler@christwoodstock.org", password="dwa12457"

        )
        print(f"{self.user}")

    def test_login(self):
        # Create an instance of a GET request.
        request = self.factory.get("/dbsk")

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = login(request)
        # Use this syntax for class-based views.
        #        response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_start_page(self):
        # Create an instance of a GET request.
        request = self.factory.get("/dbsk")

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = start_page(request)
        # Use this syntax for class-based views.
        #        response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_no_root_page(self):
        # Create an instance of a GET request.
        request = self.factory.get("/dbsk")

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = no_root_page(request)
        # Use this syntax for class-based views.
        #        response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 404)

    def create_volunteer(self, firstname="David", lastname="Adler", phone1='845-594-2721'):
        return Volunteer.objects.create(firstname=firstname, lastname=lastname, phone1=phone1)

    def test_volunteer_creation(self):
        w = self.create_volunteer()
        self.assertTrue(isinstance(w, Volunteer))
        self.assertEqual(w.__str__(), w.firstname + " " + w.lastname + " - " + w.phone1)
        r = w.get_absolute_url()
        print(f"{r=}")
        self.assertEqual(w.get_absolute_url(), '/dbsk/volunteer')

    def test_valid_form(self):
        w = Volunteer.objects.create(firstname="David", lastname="Adler", phone1='845-594-2721', archive='N')
        data = {'lastname': w.lastname, 'firstname': w.firstname, 'phone1': w.phone1, 'archive': w.archive}
        form = VolunteerCreateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        w = Volunteer.objects.create(firstname="David", lastname="Adler", phone1='')
        data = {'lastname': w.lastname, 'firstname': w.firstname, }
        form = VolunteerCreateForm(data=data)
        self.assertFalse(form.is_valid())
