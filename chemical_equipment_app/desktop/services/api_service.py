"""
API Service - Fixed Version
Handles all backend communication
"""

import requests
from typing import Dict, List, Optional
import os


class APIService:
    """Service for API communication"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.token = None
        self.user = None
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
    
    def get_headers(self) -> Dict:
        """Get request headers with auth"""
        headers = {
            'Content-Type': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def login(self, username: str, password: str) -> Dict:
        """Login user"""
        try:
            url = f"{self.base_url}/auth/login/"
            data = {
                'username': username,
                'password': password
            }
            
            print(f"Login request to: {url}")
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get('token')
                self.user = result.get('user')
                print(f"Login successful: {self.user}")
                return result
            else:
                error_msg = response.json().get('error', 'Invalid credentials')
                raise Exception(f"Login failed: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server. Make sure Django backend is running.")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout. Server may be overloaded.")
        except Exception as e:
            if 'Login failed' in str(e):
                raise
            raise Exception(f"Login error: {str(e)}")
    
    def register(self, username: str, email: str, password: str) -> Dict:
        """Register new user"""
        try:
            url = f"{self.base_url}/auth/register/"
            data = {
                'username': username,
                'email': email,
                'password': password
            }
            
            print(f"Register request to: {url}")
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 201:
                result = response.json()
                self.token = result.get('token')
                self.user = result.get('user')
                print(f"Registration successful: {self.user}")
                return result
            else:
                error_data = response.json()
                # Extract error messages
                errors = []
                for field, messages in error_data.items():
                    if isinstance(messages, list):
                        errors.extend(messages)
                    else:
                        errors.append(str(messages))
                error_msg = '; '.join(errors)
                raise Exception(f"Registration failed: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server. Make sure Django backend is running.")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout. Server may be overloaded.")
        except Exception as e:
            if 'Registration failed' in str(e):
                raise
            raise Exception(f"Registration error: {str(e)}")
    
    def logout(self):
        """Logout user"""
        self.token = None
        self.user = None
    
    def get_history(self) -> List[Dict]:
        """Get upload history"""
        try:
            url = f"{self.base_url}/history/"
            headers = self.get_headers()
            
            print(f"Fetching history from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                history = response.json()
                print(f"History loaded: {len(history)} datasets")
                return history
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please login again.")
            else:
                raise Exception(f"Failed to load history: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout")
        except Exception as e:
            if 'Unauthorized' in str(e) or 'Failed to load' in str(e):
                raise
            raise Exception(f"History error: {str(e)}")
    
    def get_dataset(self, dataset_id: int) -> Dict:
        """Get dataset details with all data"""
        try:
            url = f"{self.base_url}/datasets/{dataset_id}/"
            headers = self.get_headers()
            
            print(f"Fetching dataset from: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                dataset = response.json()
                print(f"Dataset loaded: {dataset.get('filename')} with {len(dataset.get('data', []))} records")
                return dataset
            elif response.status_code == 404:
                raise Exception(f"Dataset #{dataset_id} not found")
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please login again.")
            else:
                raise Exception(f"Failed to load dataset: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout. Dataset may be large.")
        except Exception as e:
            if 'not found' in str(e) or 'Unauthorized' in str(e) or 'Failed to load' in str(e):
                raise
            raise Exception(f"Dataset error: {str(e)}")

    def get_summary(self, dataset_id: int) -> Dict:
        """Get dataset summary statistics"""
        try:
            url = f"{self.base_url}/summary/{dataset_id}/"
            headers = self.get_headers()
            
            print(f"Fetching summary from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                summary = response.json()
                return summary
            elif response.status_code == 404:
                raise Exception(f"Dataset #{dataset_id} not found")
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please login again.")
            else:
                raise Exception(f"Failed to load summary: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout")
        except Exception as e:
            if 'not found' in str(e) or 'Unauthorized' in str(e) or 'Failed to load' in str(e):
                raise
            raise Exception(f"Summary error: {str(e)}")
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """Delete dataset"""
        try:
            url = f"{self.base_url}/datasets/{dataset_id}/"
            headers = self.get_headers()
            
            print(f"Deleting dataset: {url}")
            response = requests.delete(url, headers=headers, timeout=10)
            
            if response.status_code == 204:
                print(f"Dataset {dataset_id} deleted")
                return True
            elif response.status_code == 404:
                raise Exception(f"Dataset #{dataset_id} not found")
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please login again.")
            else:
                raise Exception(f"Failed to delete dataset: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server")
        except requests.exceptions.Timeout:
            raise Exception("Request timeout")
        except Exception as e:
            if 'not found' in str(e) or 'Unauthorized' in str(e) or 'Failed to delete' in str(e):
                raise
            raise Exception(f"Delete error: {str(e)}")
    
    def upload_dataset(self, file_path: str) -> Dict:
        """Upload dataset file"""
        try:
            # Use dedicated upload endpoint (expects multipart "file")
            url = f"{self.base_url}/upload/"
            
            # Check file exists
            if not os.path.exists(file_path):
                raise Exception(f"File not found: {file_path}")
            
            # Check file size (50 MB limit)
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:
                raise Exception("File too large. Maximum size: 50 MB")
            
            # Prepare headers (no Content-Type for multipart)
            headers = {}
            if self.token:
                headers['Authorization'] = f'Token {self.token}'
            
            # Prepare file
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'text/csv')}
                
                print(f"Uploading {filename} ({file_size} bytes) to: {url}")
                response = requests.post(
                    url,
                    headers=headers,
                    files=files,
                    timeout=60
                )
            
            if response.status_code == 201:
                result = response.json()
                print(f"Upload successful: {result.get('filename')}")
                return result
            elif response.status_code == 400:
                # Backend returns {"error": "..."} for CSV validation issues
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Invalid file format')
                except Exception:
                    error_msg = 'Invalid file format'
                raise Exception(f"Invalid file: {error_msg}")
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please login again.")
            elif response.status_code == 413:
                raise Exception("File too large")
            else:
                raise Exception(f"Upload failed: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server")
        except requests.exceptions.Timeout:
            raise Exception("Upload timeout. File may be too large.")
        except Exception as e:
            if 'File not found' in str(e) or 'too large' in str(e) or 'Invalid file' in str(e) or 'Unauthorized' in str(e) or 'Upload failed' in str(e):
                raise
            raise Exception(f"Upload error: {str(e)}")

    def download_pdf(self, dataset_id: int) -> bytes:
        """Download PDF report for a dataset"""
        try:
            url = f"{self.base_url}/datasets/{dataset_id}/download_pdf/"
            headers = self.get_headers()
            
            print(f"Downloading PDF from: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.content
            elif response.status_code == 404:
                raise Exception(f"Dataset #{dataset_id} not found")
            elif response.status_code == 401:
                raise Exception("Unauthorized. Please login again.")
            else:
                raise Exception(f"Failed to download PDF: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server")
        except requests.exceptions.Timeout:
            raise Exception("Download timeout")
        except Exception as e:
            if 'not found' in str(e) or 'Unauthorized' in str(e) or 'Failed to download' in str(e):
                raise
            raise Exception(f"Download error: {str(e)}")


# Global instance
api_service = APIService()
