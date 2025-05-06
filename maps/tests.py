from django.test import TestCase
from django.contrib.auth.models import User
from .models import Map
from rest_framework.test import APIClient
import json

class MapTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client = APIClient()
        self.client.login(username='testuser', password='pass')

        self.sample_layout = [
            ["R", "R", "#"],
            ["R", "#", "R"],
            ["R", "R", "R"]
        ]
        self.map = Map.objects.create(name='TestMap', owner=self.user, layout=self.sample_layout, public=True)

    def test_map_creation(self):
        self.assertEqual(Map.objects.count(), 1)
        self.assertEqual(self.map.name, 'TestMap')

    def test_get_all_maps(self):
        response = self.client.get('/api/maps/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_single_map(self):
        response = self.client.get(f'/api/maps/?id={self.map.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'TestMap')

    def test_update_map(self):
        updated_layout = [
            ["R", "R", "R"],
            ["#", "#", "#"],
            ["R", "R", "R"]
        ]
        response = self.client.put('/api/maps/', {
            'id': self.map.id,
            'layout': json.dumps(updated_layout),
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_map(self):
        response = self.client.delete('/api/maps/', {'id': self.map.id}, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Map.objects.count(), 0)

    def test_path_exists(self):
        response = self.client.get(f'/api/navigate/?map_id={self.map.id}&row_s=0&col_s=0&row_e=2&col_e=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['path_exists'])

    def test_path_blocked(self):
        # Completely blocked layout
        self.map.layout = [
            ["R", "#", "#"],
            ["#", "#", "#"],
            ["#", "#", "R"]
        ]
        self.map.save()
        response = self.client.get(f'/api/navigate/?map_id={self.map.id}&row_s=0&col_s=0&row_e=2&col_e=2')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['path_exists'])
