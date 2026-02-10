"""
API Service Layer
Handles all backend communication
"""

import requests
from typing import Dict, Any, Optional, List
from config.settings import API_BASE_URL


class APIService:
    """Service for API communication"""
    
    def __init__(self, token: Optional[str] = None):
        self.base_url = API_BASE_URL
        self.token = token
        self.headers = {'Content-Type': 'application/json'}
        if token:
            self.headers['Authorization'] = f'Token {token}'
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.headers['Authorization'] = f'Token {token}'
    
    # Auth endpoints
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user"""
        url = f'{self.base_url}/auth/login/'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register new user"""
        url = f'{self.base_url}/auth/register/'
        data = {'username': username, 'email': email, 'password': password}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def logout(self) -> Dict[str, Any]:
        """Logout user"""
        url = f'{self.base_url}/auth/logout/'
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    # Dataset endpoints
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """Upload CSV file"""
        url = f'{self.base_url}/upload/'
        with open(file_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': self.headers.get('Authorization', '')}
            response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Get dataset by ID"""
        url = f'{self.base_url}/datasets/{dataset_id}/'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, dataset_id: int) -> Dict[str, Any]:
        """Get dataset summary"""
        url = f'{self.base_url}/summary/{dataset_id}/'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get upload history"""
        url = f'{self.base_url}/history/'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def download_pdf(self, dataset_id: int) -> bytes:
        """Download PDF report"""
        url = f'{self.base_url}/datasets/{dataset_id}/download_pdf/'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content
    
    def delete_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Delete dataset"""
        url = f'{self.base_url}/datasets/{dataset_id}/'
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json() if response.text else {}


# Singleton instance
api_service = APIService()