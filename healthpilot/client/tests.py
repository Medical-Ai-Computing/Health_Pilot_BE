# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from django.contrib.auth.models import User


# class PaymentTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass'
#         )
#         self.free_membership = 'Free'
#         self.premium_membership = 'Premium'

#     def test_create_payment(self):
#         self.client.force_authenticate(user=self.user)
#         data = {
#             'membership_type': self.premium_membership,
#             'payment_method': 'paypal',
#             'amount': 100.00,
#             'transaction_id': '1234abcd'
#         }
#         url = reverse('payment')
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['membership'], self.premium_membership)
#         self.assertEqual(response.data['payment_method'], 'paypal')
#         self.assertEqual(response.data['amount'], 100.00)
#         self.assertEqual(response.data['transaction_id'], '1234abcd')

#     def test_update_membership_status(self):
#         self.client.force_authenticate(user=self.user)
#         data = {
#             'membership_type': self.premium_membership,
#             'payment_method': 'bank_transfer',
#             'amount': 200.00,
#             'transaction_id': '5678efgh'
#         }
#         url = reverse('payment')
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(self.user.membership_type, self.free_membership)
#         response = self.client.patch(url, {'membership_type': self.premium_membership}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.user.membership_type, self.premium_membership)
