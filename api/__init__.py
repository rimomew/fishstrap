"""API clients and HTTP utilities for PyFishstrap"""

import asyncio
import aiohttp
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode

from ..paths import Paths
import platform


def get_user_agent() -> str:
    """Get the user agent string for HTTP requests"""
    from .. import __version__
    
    system_info = f"{platform.system()}/{platform.release()}"
    python_version = f"Python/{platform.python_version()}"
    
    return f"{Paths.PROJECT_NAME}/{__version__} ({system_info}; {python_version})"


class HttpClient:
    """HTTP client for making API requests"""
    
    _session: Optional[aiohttp.ClientSession] = None
    _timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=30)
    _headers: Dict[str, str] = {}
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize the HTTP client with default headers"""
        cls._headers = {
            'User-Agent': get_user_agent(),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    
    @classmethod
    async def get_session(cls) -> aiohttp.ClientSession:
        """Get or create an aiohttp session"""
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession(
                timeout=cls._timeout,
                headers=cls._headers
            )
        return cls._session
    
    @classmethod
    async def close_session(cls) -> None:
        """Close the aiohttp session"""
        if cls._session and not cls._session.closed:
            await cls._session.close()
            cls._session = None
    
    @classmethod
    async def get(cls, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Make a GET request and return the response text"""
        try:
            session = await cls.get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"GET {url} failed with status {response.status}")
                    return None
        except Exception as e:
            print(f"GET {url} failed: {e}")
            return None
    
    @classmethod
    async def get_json(cls, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make a GET request and return the JSON response"""
        try:
            session = await cls.get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"GET JSON {url} failed with status {response.status}")
                    return None
        except Exception as e:
            print(f"GET JSON {url} failed: {e}")
            return None
    
    @classmethod
    async def post(cls, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Make a POST request and return the response text"""
        try:
            session = await cls.get_session()
            async with session.post(url, data=data, json=json_data) as response:
                if response.status in [200, 201]:
                    return await response.text()
                else:
                    print(f"POST {url} failed with status {response.status}")
                    return None
        except Exception as e:
            print(f"POST {url} failed: {e}")
            return None
    
    @classmethod
    async def post_json(cls, url: str, json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make a POST request and return the JSON response"""
        try:
            session = await cls.get_session()
            async with session.post(url, json=json_data) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    print(f"POST JSON {url} failed with status {response.status}")
                    return None
        except Exception as e:
            print(f"POST JSON {url} failed: {e}")
            return None


class RoValraClient:
    """Client for RoValra API (https://www.rovalra.com/)"""
    
    BASE_URL = "https://api.rovalra.com"
    
    @classmethod
    async def get_servers(cls, datacenter: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get list of servers from RoValra"""
        url = f"{cls.BASE_URL}/servers"
        params = {}
        if datacenter:
            params['datacenter'] = datacenter
        
        return await HttpClient.get_json(url, params=params)
    
    @classmethod
    async def get_datacenters(cls) -> Optional[List[str]]:
        """Get list of available datacenters"""
        url = f"{cls.BASE_URL}/datacenters"
        response = await HttpClient.get_json(url)
        if response and 'datacenters' in response:
            return response['datacenters']
        return None
    
    @classmethod
    async def get_geolocation(cls, ip: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get geolocation information"""
        url = f"{cls.BASE_URL}/geolocation"
        params = {}
        if ip:
            params['ip'] = ip
        
        return await HttpClient.get_json(url, params=params)
    
    @classmethod
    async def get_server_info(cls, server_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific server"""
        url = f"{cls.BASE_URL}/servers/{server_id}"
        return await HttpClient.get_json(url)


class RobloxClient:
    """Client for Roblox API"""
    
    BASE_URL = "https://www.roblox.com"
    API_URL = "https://api.roblox.com"
    GAMES_URL = "https://games.roblox.com"
    
    @classmethod
    async def get_user(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user information"""
        url = f"{cls.API_URL}/users/{user_id}"
        return await HttpClient.get_json(url)
    
    @classmethod
    async def get_game_details(cls, universe_id: int) -> Optional[Dict[str, Any]]:
        """Get game details"""
        url = f"{cls.GAMES_URL}/v1/games?universeIds={universe_id}"
        response = await HttpClient.get_json(url)
        if response and 'data' in response and len(response['data']) > 0:
            return response['data'][0]
        return None
    
    @classmethod
    async def get_universe_id(cls, place_id: int) -> Optional[int]:
        """Get universe ID from place ID"""
        url = f"{cls.API_URL}/places/{place_id}/universe-id"
        response = await HttpClient.get_json(url)
        if response and 'universeId' in response:
            return response['universeId']
        return None
    
    @classmethod
    async def get_thumbnail(cls, target_id: int, size: str = "420x420", format: str = "png") -> Optional[str]:
        """Get thumbnail URL for a game or asset"""
        url = f"{cls.API_URL}/thumbnails/resolve"
        data = {
            'targetId': target_id,
            'size': size,
            'format': format
        }
        response = await HttpClient.post_json(url, json_data=data)
        if response and 'imageUrl' in response:
            return response['imageUrl']
        return None


class GitHubClient:
    """Client for GitHub API"""
    
    BASE_URL = "https://api.github.com"
    
    @classmethod
    async def get_latest_release(cls, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get the latest release from a GitHub repository"""
        url = f"{cls.BASE_URL}/repos/{owner}/{repo}/releases/latest"
        return await HttpClient.get_json(url)
    
    @classmethod
    async def get_release_assets(cls, owner: str, repo: str, release_id: int) -> Optional[List[Dict[str, Any]]]:
        """Get assets for a specific release"""
        url = f"{cls.BASE_URL}/repos/{owner}/{repo}/releases/{release_id}"
        response = await HttpClient.get_json(url)
        if response and 'assets' in response:
            return response['assets']
        return None
    
    @classmethod
    async def get_release_by_tag(cls, owner: str, repo: str, tag: str) -> Optional[Dict[str, Any]]:
        """Get a release by its tag name"""
        url = f"{cls.BASE_URL}/repos/{owner}/{repo}/releases/tags/{tag}"
        return await HttpClient.get_json(url)


# Initialize HTTP client on module load
HttpClient.initialize()
