from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Company, CompanyMembershipRequest


class CompanyManagementTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="itadmin",
            email="admin@corp.com",
            password="adminpassword123",
            role=User.ROLE_ADMIN,
        )
        self.employee = User.objects.create_user(
            username="emp1",
            email="emp1@corp.com",
            password="emppassword123",
            role=User.ROLE_EMPLOYEE,
        )
        self.admin_client = Client()
        self.admin_client.force_login(self.admin)

        self.employee_client = Client()
        self.employee_client.force_login(self.employee)

    def test_admin_can_setup_company_name_address_and_code(self):
        url = reverse("accounts:company_manage")
        data = {
            "name": "Acme Technologies",
            "address": "123 Tech Blvd, Suite 400",
            "code": "CMP-ACME99",
        }
        response = self.admin_client.post(url, data)
        self.assertRedirects(response, url)

        company = Company.objects.filter(code="CMP-ACME99").first()
        self.assertIsNotNone(company)
        self.assertEqual(company.name, "Acme Technologies")
        self.assertEqual(company.address, "123 Tech Blvd, Suite 400")
        self.assertEqual(company.admin, self.admin)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.company, company)

    def test_admin_can_regenerate_company_code(self):
        company = Company.objects.create(
            name="Alpha Corp",
            address="456 Silicon Rd",
            code="CMP-ORIGINAL",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        url = reverse("accounts:company_regenerate_code")
        response = self.admin_client.post(url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertNotEqual(json_data["code"], "CMP-ORIGINAL")

        company.refresh_from_db()
        self.assertEqual(company.code, json_data["code"])

    def test_employee_can_join_company_by_code(self):
        company = Company.objects.create(
            name="Beta Ltd",
            address="789 Market St",
            code="CMP-BETAX1",
            admin=self.admin,
        )
        join_url = reverse("accounts:employee_join_company")
        response = self.employee_client.post(join_url, {"company_code": "CMP-BETAX1"})
        self.assertRedirects(response, join_url)

        membership_req = CompanyMembershipRequest.objects.filter(
            company=company, user=self.employee, request_type=CompanyMembershipRequest.TYPE_JOIN
        ).first()
        self.assertIsNotNone(membership_req)
        self.assertEqual(membership_req.status, CompanyMembershipRequest.STATUS_PENDING)

    def test_invalid_company_code_rejected_with_error(self):
        join_url = reverse("accounts:employee_join_company")
        response = self.employee_client.post(
            join_url,
            {"company_code": "NONEXISTENT-CODE"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data["success"])

    def test_admin_can_accept_join_request(self):
        company = Company.objects.create(
            name="Gamma Inc",
            address="100 Innovation Way",
            code="CMP-GAMMA",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        req = CompanyMembershipRequest.objects.create(
            company=company,
            user=self.employee,
            request_type=CompanyMembershipRequest.TYPE_JOIN,
            status=CompanyMembershipRequest.STATUS_PENDING,
        )

        review_url = reverse("accounts:company_request_review", kwargs={"pk": req.pk, "action": "accept"})
        response = self.admin_client.post(review_url)
        self.assertRedirects(response, reverse("accounts:company_manage"))

        req.refresh_from_db()
        self.assertEqual(req.status, CompanyMembershipRequest.STATUS_APPROVED)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.company, company)

    def test_admin_can_reject_join_request(self):
        company = Company.objects.create(
            name="Delta Inc",
            address="200 Broadway",
            code="CMP-DELTA",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        req = CompanyMembershipRequest.objects.create(
            company=company,
            user=self.employee,
            request_type=CompanyMembershipRequest.TYPE_JOIN,
            status=CompanyMembershipRequest.STATUS_PENDING,
        )

        review_url = reverse("accounts:company_request_review", kwargs={"pk": req.pk, "action": "reject"})
        response = self.admin_client.post(review_url)
        self.assertRedirects(response, reverse("accounts:company_manage"))

        req.refresh_from_db()
        self.assertEqual(req.status, CompanyMembershipRequest.STATUS_REJECTED)
        self.employee.refresh_from_db()
        self.assertIsNone(self.employee.company)

    def test_employee_can_request_leave_and_admin_approves(self):
        company = Company.objects.create(
            name="Epsilon Global",
            address="500 5th Ave",
            code="CMP-EPSILON",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        self.employee.company = company
        self.employee.save()

        leave_url = reverse("accounts:employee_leave_company")
        response = self.employee_client.post(leave_url)
        self.assertRedirects(response, reverse("accounts:employee_join_company"))

        leave_req = CompanyMembershipRequest.objects.filter(
            company=company,
            user=self.employee,
            request_type=CompanyMembershipRequest.TYPE_LEAVE,
            status=CompanyMembershipRequest.STATUS_PENDING,
        ).first()
        self.assertIsNotNone(leave_req)

        review_url = reverse("accounts:company_request_review", kwargs={"pk": leave_req.pk, "action": "accept"})
        response = self.admin_client.post(review_url)
        self.assertRedirects(response, reverse("accounts:company_manage"))

        leave_req.refresh_from_db()
        self.assertEqual(leave_req.status, CompanyMembershipRequest.STATUS_APPROVED)
        self.employee.refresh_from_db()
        self.assertIsNone(self.employee.company)

    def test_employee_leave_request_rejected_by_admin(self):
        company = Company.objects.create(
            name="Zeta Logistics",
            address="600 Harbor Way",
            code="CMP-ZETA",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        self.employee.company = company
        self.employee.save()

        leave_req = CompanyMembershipRequest.objects.create(
            company=company,
            user=self.employee,
            request_type=CompanyMembershipRequest.TYPE_LEAVE,
            status=CompanyMembershipRequest.STATUS_PENDING,
        )

        review_url = reverse("accounts:company_request_review", kwargs={"pk": leave_req.pk, "action": "reject"})
        response = self.admin_client.post(review_url)
        self.assertRedirects(response, reverse("accounts:company_manage"))

        leave_req.refresh_from_db()
        self.assertEqual(leave_req.status, CompanyMembershipRequest.STATUS_REJECTED)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.company, company)

    def test_admin_accept_join_request_ajax_returns_member_data(self):
        company = Company.objects.create(
            name="Theta Tech",
            address="700 Innovation Loop",
            code="CMP-THETA",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        req = CompanyMembershipRequest.objects.create(
            company=company,
            user=self.employee,
            request_type=CompanyMembershipRequest.TYPE_JOIN,
            status=CompanyMembershipRequest.STATUS_PENDING,
        )

        review_url = reverse("accounts:company_request_review", kwargs={"pk": req.pk, "action": "accept"})
        response = self.admin_client.post(review_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["request_type"], "join")
        self.assertIn("member", json_data)
        self.assertEqual(json_data["member"]["username"], self.employee.username)
        self.assertEqual(json_data["member"]["id"], self.employee.pk)

    def test_admin_can_add_member_directly(self):
        company = Company.objects.create(
            name="Omega Labs",
            address="800 Discovery Blvd",
            code="CMP-OMEGA",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()

        add_url = reverse("accounts:company_add_member")
        response = self.admin_client.post(
            add_url,
            {"identifier": self.employee.username},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["member"]["username"], self.employee.username)

        self.employee.refresh_from_db()
        self.assertEqual(self.employee.company, company)

    def test_admin_can_remove_member(self):
        company = Company.objects.create(
            name="Sigma Systems",
            address="900 Enterprise Dr",
            code="CMP-SIGMA",
            admin=self.admin,
        )
        self.admin.company = company
        self.admin.save()
        self.employee.company = company
        self.employee.save()

        remove_url = reverse("accounts:company_remove_member", kwargs={"pk": self.employee.pk})
        response = self.admin_client.post(remove_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])

        self.employee.refresh_from_db()
        self.assertIsNone(self.employee.company)

    def test_csrf_failure_view(self):
        from accounts.views import csrf_failure_view
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post("/accounts/company/", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        response = csrf_failure_view(request, reason="CSRF token from POST incorrect.")
        self.assertEqual(response.status_code, 403)
        import json
        data = json.loads(response.content.decode("utf-8"))
        self.assertTrue(data["csrf_failed"])
        self.assertTrue(len(data["csrf_token"]) > 0)
