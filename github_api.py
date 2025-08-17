"""
GitHub API integration for fetching contribution data
"""

import requests
from datetime import datetime, timedelta
import json

class GitHubAPI:
    def __init__(self, username, token=None):
        self.username = username
        self.token = token
        self.headers = {}
        
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_contributions(self):
        """
        Fetch GitHub contributions for the last year.
        Returns a list of dictionaries with date and contribution count.
        """
        # GitHub doesn't provide a direct API for contribution graph
        # We'll use the GraphQL API to get contribution data
        
        if not self.token:
            # Fallback to mock data if no token provided
            return self._generate_mock_contributions()
        
        try:
            # GraphQL query for contributions
            query = """
            query($username: String!) {
                user(login: $username) {
                    contributionsCollection {
                        contributionCalendar {
                            totalContributions
                            weeks {
                                contributionDays {
                                    contributionCount
                                    date
                                }
                            }
                        }
                    }
                }
            }
            """
            
            response = requests.post(
                'https://api.github.com/graphql',
                json={'query': query, 'variables': {'username': self.username}},
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract contributions
                contributions = []
                weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
                
                for week in weeks:
                    for day in week['contributionDays']:
                        contributions.append({
                            'date': day['date'],
                            'count': day['contributionCount']
                        })
                
                # Get last 365 days
                return contributions[-365:]
            else:
                print(f"Error fetching GitHub data: {response.status_code}")
                return self._generate_mock_contributions()
                
        except Exception as e:
            print(f"Error fetching GitHub contributions: {e}")
            return self._generate_mock_contributions()
    
    def _generate_mock_contributions(self):
        """
        Generate mock contribution data for testing.
        Creates a realistic-looking contribution pattern.
        """
        import random
        
        contributions = []
        today = datetime.now()
        
        for i in range(365):
            date = today - timedelta(days=i)
            
            # Create realistic patterns
            # Weekends typically have fewer contributions
            is_weekend = date.weekday() in [5, 6]
            
            # Base probability of contributions
            if is_weekend:
                base_prob = 0.3
            else:
                base_prob = 0.7
            
            # Determine if there are contributions
            if random.random() < base_prob:
                # Generate contribution count with realistic distribution
                # Most days have 1-5 contributions, some have more
                weights = [0.3, 0.25, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01]
                counts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                
                count = random.choices(counts, weights=weights)[0]
                
                # Occasionally have high contribution days
                if random.random() < 0.05:
                    count = random.randint(10, 20)
            else:
                count = 0
            
            contributions.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
        
        # Reverse to have oldest first
        contributions.reverse()
        
        return contributions