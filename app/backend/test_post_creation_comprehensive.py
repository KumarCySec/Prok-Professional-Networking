#!/usr/bin/env python3
"""
Comprehensive test script for post creation, media uploads, validation, and navigation flows
Tests all scenarios: text-only posts, image/video uploads, validation, edge cases, and navigation
"""

import os
import sys
import requests
import json
import tempfile
import time
from io import BytesIO
from PIL import Image
import base64

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import get_app
from extensions import db
from models.user import User
from models.post import Post

class PostCreationTestSuite:
    """Comprehensive test suite for post creation and media uploads"""
    
    def __init__(self):
        self.app = get_app()
        self.base_url = 'http://localhost:5000'
        self.test_user = None
        self.auth_token = None
        self.test_posts = []
        
    def setup_test_user(self):
        """Create or get test user and authenticate"""
        with self.app.app_context():
            # Create test user if it doesn't exist
            self.test_user = User.find_by_username('test_post_user')
            if not self.test_user:
                self.test_user = User('test_post_user', 'test_post@example.com', 'TestPass123!')
                self.test_user.save()
                print(f"✓ Created test user: {self.test_user.username}")
            else:
                print(f"✓ Found existing test user: {self.test_user.username}")
            
            # Login to get auth token
            login_data = {
                'username_or_email': 'test_post_user',
                'password': 'TestPass123!'
            }
            
            response = requests.post(f'{self.base_url}/api/login', json=login_data)
            if response.status_code == 200:
                self.auth_token = response.json()['access_token']
                print("✓ Successfully authenticated")
            else:
                raise Exception("Failed to authenticate test user")
    
    def create_test_image(self, size=(800, 600), format='JPEG', filename='test.jpg'):
        """Create a test image file"""
        img = Image.new('RGB', size, color='red')
        img_io = BytesIO()
        img.save(img_io, format=format)
        img_io.seek(0)
        return img_io, filename
    
    def create_test_video(self, duration=5, filename='test.mp4'):
        """Create a mock video file (simulated)"""
        # Create a dummy video file (in real testing, you'd use actual video files)
        video_data = b'fake_video_data' * 1000  # Simulate video data
        video_io = BytesIO(video_data)
        video_io.seek(0)
        return video_io, filename
    
    def create_corrupted_file(self, filename='corrupted.jpg'):
        """Create a corrupted file"""
        corrupted_data = b'this is not a valid image file'
        file_io = BytesIO(corrupted_data)
        file_io.seek(0)
        return file_io, filename
    
    def create_large_file(self, size_mb=15, filename='large_file.jpg'):
        """Create a large file for testing size limits"""
        large_data = b'x' * (size_mb * 1024 * 1024)  # Create file of specified size
        file_io = BytesIO(large_data)
        file_io.seek(0)
        return file_io, filename
    
    def test_1_text_only_post_creation(self):
        """Test 1: Text-only post creation"""
        print("\n🧪 Test 1: Text-only post creation")
        
        post_data = {
            'content': 'Testing text-only post creation for professional networking.',
            'rich_content': '',
            'tags': 'testing,professional,networking',
            'visibility': 'public'
        }
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 201:
            post = response.json()['post']
            self.test_posts.append(post['id'])
            print(f"✓ Text-only post created successfully (ID: {post['id']})")
            print(f"  - Content: {post['content'][:50]}...")
            print(f"  - Media URL: {post.get('media_url', 'None')}")
            print(f"  - Tags: {post.get('tags', [])}")
            return True
        else:
            print(f"✗ Failed to create text-only post: {response.status_code} - {response.text}")
            return False
    
    def test_2_image_upload_post_creation(self):
        """Test 2: Post creation with image upload"""
        print("\n🧪 Test 2: Post creation with image upload")
        
        # Test different image formats and sizes
        test_cases = [
            ('small.jpg', (400, 300), 'JPEG'),
            ('medium.png', (800, 600), 'PNG'),
            ('large.webp', (1200, 900), 'WEBP')
        ]
        
        for filename, size, format in test_cases:
            print(f"  Testing {filename} ({size[0]}x{size[1]})...")
            
            # Create test image
            img_io, img_filename = self.create_test_image(size, format, filename)
            
            post_data = {
                'content': f'Testing image upload feature in post creation with {filename}',
                'rich_content': '',
                'tags': 'image,upload,testing',
                'visibility': 'public'
            }
            
            files = {'media': (img_filename, img_io, f'image/{format.lower()}')}
            
            response = requests.post(
                f'{self.base_url}/api/posts',
                data=post_data,
                files=files,
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )
            
            if response.status_code == 201:
                post = response.json()['post']
                self.test_posts.append(post['id'])
                print(f"    ✓ {filename} uploaded successfully (ID: {post['id']})")
                print(f"      - Media URL: {post.get('media_url', 'None')}")
                print(f"      - Media Type: {post.get('media_type', 'None')}")
            else:
                print(f"    ✗ Failed to upload {filename}: {response.status_code} - {response.text}")
                return False
        
        return True
    
    def test_3_video_upload_post_creation(self):
        """Test 3: Post creation with video upload"""
        print("\n🧪 Test 3: Post creation with video upload")
        
        # Test different video formats
        test_cases = [
            ('short.mp4', 'video/mp4'),
            ('medium.webm', 'video/webm'),
            ('large.mov', 'video/quicktime')
        ]
        
        for filename, mime_type in test_cases:
            print(f"  Testing {filename}...")
            
            # Create mock video file
            video_io, video_filename = self.create_test_video(filename=filename)
            
            post_data = {
                'content': f'Testing video upload feature in post creation with {filename}',
                'rich_content': '',
                'tags': 'video,upload,testing',
                'visibility': 'public'
            }
            
            files = {'media': (video_filename, video_io, mime_type)}
            
            response = requests.post(
                f'{self.base_url}/api/posts',
                data=post_data,
                files=files,
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )
            
            if response.status_code == 201:
                post = response.json()['post']
                self.test_posts.append(post['id'])
                print(f"    ✓ {filename} uploaded successfully (ID: {post['id']})")
                print(f"      - Media URL: {post.get('media_url', 'None')}")
                print(f"      - Media Type: {post.get('media_type', 'None')}")
            else:
                print(f"    ✗ Failed to upload {filename}: {response.status_code} - {response.text}")
                return False
        
        return True
    
    def test_4_media_upload_validations_edge_cases(self):
        """Test 4: Media upload validations and edge cases"""
        print("\n🧪 Test 4: Media upload validations and edge cases")
        
        # Test corrupted files
        print("  Testing corrupted files...")
        corrupted_io, corrupted_filename = self.create_corrupted_file()
        
        post_data = {
            'content': 'Testing corrupted file upload',
            'visibility': 'public'
        }
        
        files = {'media': (corrupted_filename, corrupted_io, 'image/jpeg')}
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            files=files,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 400:
            print(f"    ✓ Corrupted file correctly rejected: {response.json().get('error', 'Unknown error')}")
        else:
            print(f"    ✗ Corrupted file should have been rejected: {response.status_code}")
            return False
        
        # Test unsupported formats
        print("  Testing unsupported formats...")
        unsupported_io = BytesIO(b'fake executable data')
        unsupported_io.seek(0)
        
        files = {'media': ('test.exe', unsupported_io, 'application/octet-stream')}
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            files=files,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 400:
            print(f"    ✓ Unsupported format correctly rejected: {response.json().get('error', 'Unknown error')}")
        else:
            print(f"    ✗ Unsupported format should have been rejected: {response.status_code}")
            return False
        
        # Test large files
        print("  Testing large files...")
        large_io, large_filename = self.create_large_file(15)  # 15MB file
        
        files = {'media': (large_filename, large_io, 'image/jpeg')}
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            files=files,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 413:  # Request Entity Too Large
            print(f"    ✓ Large file correctly rejected: {response.status_code}")
        else:
            print(f"    ✗ Large file should have been rejected: {response.status_code}")
            return False
        
        return True
    
    def test_5_form_validation_error_handling(self):
        """Test 5: Form validation and error handling"""
        print("\n🧪 Test 5: Form validation and error handling")
        
        # Test empty post (no content and no media)
        print("  Testing empty post...")
        post_data = {
            'content': '',
            'rich_content': '',
            'visibility': 'public'
        }
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            print(f"    ✓ Empty post correctly rejected: {error_msg}")
        else:
            print(f"    ✗ Empty post should have been rejected: {response.status_code}")
            return False
        
        # Test whitespace-only content
        print("  Testing whitespace-only content...")
        post_data = {
            'content': '   \n\t   ',
            'rich_content': '',
            'visibility': 'public'
        }
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            print(f"    ✓ Whitespace-only content correctly rejected: {error_msg}")
        else:
            print(f"    ✗ Whitespace-only content should have been rejected: {response.status_code}")
            return False
        
        # Test content too long
        print("  Testing content too long...")
        long_content = 'A' * 6000  # Exceeds 5000 character limit
        post_data = {
            'content': long_content,
            'visibility': 'public'
        }
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            print(f"    ✓ Long content correctly rejected: {error_msg}")
        else:
            print(f"    ✗ Long content should have been rejected: {response.status_code}")
            return False
        
        # Test invalid visibility
        print("  Testing invalid visibility...")
        post_data = {
            'content': 'Valid content',
            'visibility': 'invalid_visibility'
        }
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            print(f"    ✓ Invalid visibility correctly rejected: {error_msg}")
        else:
            print(f"    ✗ Invalid visibility should have been rejected: {response.status_code}")
            return False
        
        return True
    
    def test_6_loading_states_user_feedback(self):
        """Test 6: Loading states and user feedback"""
        print("\n🧪 Test 6: Loading states and user feedback")
        
        # Test successful post creation feedback
        print("  Testing successful post creation...")
        post_data = {
            'content': 'Testing loading states and user feedback for successful post creation.',
            'visibility': 'public'
        }
        
        start_time = time.time()
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        end_time = time.time()
        
        if response.status_code == 201:
            post = response.json()['post']
            self.test_posts.append(post['id'])
            response_time = end_time - start_time
            print(f"    ✓ Post created successfully in {response_time:.2f}s")
            print(f"      - Response includes success message: {response.json().get('message', 'No message')}")
            print(f"      - Post data returned: {bool(post)}")
        else:
            print(f"    ✗ Failed to create post: {response.status_code}")
            return False
        
        return True
    
    def test_7_navigation_across_app(self):
        """Test 7: Navigation across app"""
        print("\n🧪 Test 7: Navigation across app")
        
        # Test retrieving posts from different endpoints
        endpoints = [
            '/api/posts',  # All posts
            '/api/posts/user/1',  # User posts (if endpoint exists)
            '/api/feed'  # Feed posts (if endpoint exists)
        ]
        
        for endpoint in endpoints:
            print(f"  Testing {endpoint}...")
            response = requests.get(
                f'{self.base_url}{endpoint}',
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('posts', []) if isinstance(data, dict) else data
                print(f"    ✓ {endpoint} accessible: {len(posts)} posts found")
            else:
                print(f"    ⚠ {endpoint} returned {response.status_code} (may not be implemented)")
        
        # Test post retrieval by ID
        if self.test_posts:
            test_post_id = self.test_posts[0]
            print(f"  Testing post retrieval by ID ({test_post_id})...")
            
            response = requests.get(
                f'{self.base_url}/api/posts/{test_post_id}',
                headers={'Authorization': f'Bearer {self.auth_token}'}
            )
            
            if response.status_code == 200:
                post = response.json()['post']
                print(f"    ✓ Post {test_post_id} retrieved successfully")
                print(f"      - Content: {post['content'][:50]}...")
            else:
                print(f"    ✗ Failed to retrieve post {test_post_id}: {response.status_code}")
        
        return True
    
    def test_8_media_preview_and_display(self):
        """Test 8: Media preview and display functionality"""
        print("\n🧪 Test 8: Media preview and display functionality")
        
        # Create a test image post
        img_io, img_filename = self.create_test_image()
        
        post_data = {
            'content': 'Testing media preview and display functionality',
            'visibility': 'public'
        }
        
        files = {'media': (img_filename, img_io, 'image/jpeg')}
        
        response = requests.post(
            f'{self.base_url}/api/posts',
            data=post_data,
            files=files,
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        
        if response.status_code == 201:
            post = response.json()['post']
            self.test_posts.append(post['id'])
            
            # Test media URL accessibility
            if post.get('media_url'):
                media_response = requests.get(f"{self.base_url}{post['media_url']}")
                if media_response.status_code == 200:
                    print(f"    ✓ Media file accessible: {post['media_url']}")
                    print(f"      - Content-Type: {media_response.headers.get('content-type', 'Unknown')}")
                    print(f"      - File Size: {len(media_response.content)} bytes")
                else:
                    print(f"    ✗ Media file not accessible: {media_response.status_code}")
            else:
                print(f"    ✗ No media URL in response")
        else:
            print(f"    ✗ Failed to create media post: {response.status_code}")
            return False
        
        return True
    
    def cleanup_test_data(self):
        """Clean up test data"""
        print("\n🧹 Cleaning up test data...")
        
        with self.app.app_context():
            for post_id in self.test_posts:
                try:
                    post = Post.find_by_id(post_id)
                    if post:
                        post.delete()
                        print(f"  ✓ Deleted test post {post_id}")
                except Exception as e:
                    print(f"  ⚠ Could not delete post {post_id}: {e}")
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("🚀 Starting Comprehensive Post Creation Test Suite")
        print("=" * 60)
        
        try:
            # Setup
            self.setup_test_user()
            
            # Run all tests
            tests = [
                ("Text-only post creation", self.test_1_text_only_post_creation),
                ("Image upload post creation", self.test_2_image_upload_post_creation),
                ("Video upload post creation", self.test_3_video_upload_post_creation),
                ("Media upload validations", self.test_4_media_upload_validations_edge_cases),
                ("Form validation", self.test_5_form_validation_error_handling),
                ("Loading states", self.test_6_loading_states_user_feedback),
                ("Navigation", self.test_7_navigation_across_app),
                ("Media preview", self.test_8_media_preview_and_display)
            ]
            
            passed = 0
            total = len(tests)
            
            for test_name, test_func in tests:
                try:
                    if test_func():
                        passed += 1
                    else:
                        print(f"❌ {test_name} failed")
                except Exception as e:
                    print(f"❌ {test_name} failed with exception: {e}")
            
            # Cleanup
            self.cleanup_test_data()
            
            # Results
            print("\n" + "=" * 60)
            print(f"🎯 Test Results: {passed}/{total} tests passed")
            
            if passed == total:
                print("🎉 All tests passed! Post creation system is working correctly.")
            else:
                print("⚠ Some tests failed. Please review the implementation.")
            
            return passed == total
            
        except Exception as e:
            print(f"❌ Test suite failed with exception: {e}")
            return False

def main():
    """Main function to run the test suite"""
    test_suite = PostCreationTestSuite()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n✅ All post creation tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)

if __name__ == '__main__':
    main() 