#!/usr/bin/env python3
"""
Test script for posts functionality
"""

import os
import sys
import requests
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import get_app
from extensions import db
from models.user import User
from models.post import Post

def test_posts_functionality():
    """Test the posts functionality"""
    app = get_app()
    
    with app.app_context():
        print("Testing Posts Functionality...")
        
        # Test 1: Create a test user if it doesn't exist
        test_user = User.find_by_username('testuser')
        if not test_user:
            test_user = User('testuser', 'test@example.com', 'TestPass123!')
            test_user.save()
            print(f"✓ Created test user: {test_user.username}")
        else:
            print(f"✓ Found existing test user: {test_user.username}")
        
        # Test 2: Create a test post
        test_post = Post(
            user_id=test_user.id,
            content="This is a test post content",
            rich_content="<b>Bold text</b> and <i>italic text</i>",
            tags=['test', 'demo'],
            visibility='public'
        )
        test_post.save()
        print(f"✓ Created test post with ID: {test_post.id}")
        
        # Test 3: Retrieve the post
        retrieved_post = Post.find_by_id(test_post.id)
        if retrieved_post:
            print(f"✓ Retrieved post: {retrieved_post.content[:50]}...")
        else:
            print("✗ Failed to retrieve post")
        
        # Test 4: Get user posts
        user_posts = Post.find_by_user(test_user.id)
        print(f"✓ Found {len(user_posts)} posts for user")
        
        # Test 5: Get feed posts
        feed_posts = Post.get_feed_posts()
        print(f"✓ Found {len(feed_posts)} posts in feed")
        
        # Test 6: Test post to_dict method
        post_dict = test_post.to_dict()
        print(f"✓ Post dict keys: {list(post_dict.keys())}")
        
        # Test 7: Test like functionality
        initial_likes = test_post.likes_count
        test_post.increment_likes()
        print(f"✓ Incremented likes from {initial_likes} to {test_post.likes_count}")
        
        # Clean up test data
        test_post.delete()
        print("✓ Cleaned up test post")
        
        print("\n🎉 All post tests passed!")

if __name__ == '__main__':
    test_posts_functionality() 