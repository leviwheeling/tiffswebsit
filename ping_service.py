"""
Background Ping Service for FastAPI Integration
Can be imported and used as a background task within the FastAPI application.
"""

import asyncio
import aiohttp
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class BackgroundPingService:
    """Background service to ping the site at regular intervals."""
    
    def __init__(self, 
                 site_url: str = "https://duncanfamilydental.com",
                 ping_interval: int = 600,  # 10 minutes
                 timeout: int = 30):
        self.site_url = site_url
        self.ping_interval = ping_interval
        self.timeout = timeout
        self.running = False
        self.task: Optional[asyncio.Task] = None
        self.ping_count = 0
        self.success_count = 0
        self.failure_count = 0
        
    async def ping_site(self) -> bool:
        """Send an async ping request to the site."""
        try:
            headers = {
                "User-Agent": "Duncan Family Dentistry Site Monitor/1.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
            
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                logger.info(f"Pinging {self.site_url}...")
                start_time = datetime.now()
                
                async with session.get(self.site_url, headers=headers) as response:
                    end_time = datetime.now()
                    response_time = (end_time - start_time).total_seconds()
                    
                    self.ping_count += 1
                    
                    if response.status == 200:
                        self.success_count += 1
                        logger.info(f"✅ Background ping #{self.ping_count} successful - "
                                  f"Status: {response.status} - Response time: {response_time:.2f}s")
                        return True
                    else:
                        self.failure_count += 1
                        logger.warning(f"⚠️ Background ping #{self.ping_count} returned status {response.status}")
                        return False
                        
        except asyncio.TimeoutError:
            self.failure_count += 1
            logger.error(f"❌ Background ping #{self.ping_count} timed out after {self.timeout}s")
            return False
            
        except aiohttp.ClientError as e:
            self.failure_count += 1
            logger.error(f"❌ Background ping #{self.ping_count} client error: {str(e)}")
            return False
            
        except Exception as e:
            self.failure_count += 1
            logger.error(f"❌ Background ping #{self.ping_count} unexpected error: {str(e)}")
            return False
    
    async def _ping_loop(self):
        """Main ping loop that runs in the background."""
        logger.info("🚀 Starting background ping service...")
        logger.info(f"Target URL: {self.site_url}")
        logger.info(f"Ping interval: {self.ping_interval} seconds ({self.ping_interval/60} minutes)")
        
        # Initial ping
        await self.ping_site()
        
        while self.running:
            try:
                # Log stats every 10 pings
                if self.ping_count > 0 and self.ping_count % 10 == 0:
                    self.log_stats()
                
                await asyncio.sleep(self.ping_interval)
                
                if self.running:  # Check if we're still supposed to be running
                    await self.ping_site()
                    
            except asyncio.CancelledError:
                logger.info("Background ping service cancelled")
                break
            except Exception as e:
                logger.error(f"Unexpected error in background ping loop: {str(e)}")
                await asyncio.sleep(60)  # Wait a minute before retrying
        
        logger.info("🛑 Background ping service stopped")
    
    def start(self):
        """Start the background ping service."""
        if self.running:
            logger.warning("Background ping service is already running")
            return
            
        self.running = True
        self.task = asyncio.create_task(self._ping_loop())
        logger.info("Background ping service started")
    
    async def stop(self):
        """Stop the background ping service."""
        if not self.running:
            logger.warning("Background ping service is not running")
            return
            
        self.running = False
        
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            
        self.log_stats()
        logger.info("Background ping service stopped")
    
    def get_stats(self) -> dict:
        """Return current statistics."""
        if self.ping_count == 0:
            success_rate = 0
        else:
            success_rate = (self.success_count / self.ping_count) * 100
            
        return {
            "total_pings": self.ping_count,
            "successful": self.success_count,
            "failed": self.failure_count,
            "success_rate": success_rate,
            "running": self.running
        }
    
    def log_stats(self):
        """Log current statistics."""
        stats = self.get_stats()
        logger.info(
            f"📊 Background Ping Stats - Total: {stats['total_pings']}, "
            f"Success: {stats['successful']}, "
            f"Failed: {stats['failed']}, "
            f"Success Rate: {stats['success_rate']:.1f}%"
        )

# Global instance for use in FastAPI app
ping_service = BackgroundPingService()

# FastAPI integration functions
async def start_ping_service():
    """Start the ping service when the FastAPI app starts."""
    ping_service.start()

async def stop_ping_service():
    """Stop the ping service when the FastAPI app shuts down."""
    await ping_service.stop()

def get_ping_stats() -> dict:
    """Get current ping statistics."""
    return ping_service.get_stats()
