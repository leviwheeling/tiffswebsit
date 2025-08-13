#!/usr/bin/env python3
"""
Site Ping Script for Duncan Family Dentistry
Pings duncanfamilydental.com every 10 minutes to keep the site active.
"""

import requests
import time
import logging
from datetime import datetime
import sys
import signal
import os

# ── LOGGING SETUP ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ping_site.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ── CONFIGURATION ────────────────────────────────────────────────────────────
SITE_URL = "https://duncanfamilydental.com"
PING_INTERVAL = 600  # 10 minutes in seconds
TIMEOUT = 30  # Request timeout in seconds
USER_AGENT = "Duncan Family Dentistry Site Monitor/1.0"

class SitePinger:
    """Handles pinging the website at regular intervals."""
    
    def __init__(self):
        self.running = True
        self.ping_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def ping_site(self):
        """Send a ping request to the site."""
        try:
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
            
            logger.info(f"Pinging {SITE_URL}...")
            response = requests.get(
                SITE_URL, 
                timeout=TIMEOUT,
                headers=headers,
                allow_redirects=True
            )
            
            self.ping_count += 1
            
            if response.status_code == 200:
                self.success_count += 1
                logger.info(f"✅ Ping #{self.ping_count} successful - Status: {response.status_code} - Response time: {response.elapsed.total_seconds():.2f}s")
                return True
            else:
                self.failure_count += 1
                logger.warning(f"⚠️ Ping #{self.ping_count} returned status {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            self.failure_count += 1
            logger.error(f"❌ Ping #{self.ping_count} timed out after {TIMEOUT}s")
            return False
            
        except requests.exceptions.ConnectionError as e:
            self.failure_count += 1
            logger.error(f"❌ Ping #{self.ping_count} connection error: {str(e)}")
            return False
            
        except Exception as e:
            self.failure_count += 1
            logger.error(f"❌ Ping #{self.ping_count} unexpected error: {str(e)}")
            return False
    
    def get_stats(self):
        """Return current statistics."""
        if self.ping_count == 0:
            success_rate = 0
        else:
            success_rate = (self.success_count / self.ping_count) * 100
            
        return {
            "total_pings": self.ping_count,
            "successful": self.success_count,
            "failed": self.failure_count,
            "success_rate": success_rate
        }
    
    def log_stats(self):
        """Log current statistics."""
        stats = self.get_stats()
        logger.info(
            f"📊 Stats - Total: {stats['total_pings']}, "
            f"Success: {stats['successful']}, "
            f"Failed: {stats['failed']}, "
            f"Success Rate: {stats['success_rate']:.1f}%"
        )
    
    def run(self):
        """Main loop to ping the site every 10 minutes."""
        logger.info("🚀 Starting Duncan Family Dentistry site monitor...")
        logger.info(f"Target URL: {SITE_URL}")
        logger.info(f"Ping interval: {PING_INTERVAL} seconds ({PING_INTERVAL/60} minutes)")
        logger.info("Press Ctrl+C to stop")
        
        # Initial ping
        self.ping_site()
        
        while self.running:
            try:
                # Log stats every 10 pings
                if self.ping_count > 0 and self.ping_count % 10 == 0:
                    self.log_stats()
                
                logger.info(f"⏰ Waiting {PING_INTERVAL} seconds until next ping...")
                time.sleep(PING_INTERVAL)
                
                if self.running:  # Check if we're still supposed to be running
                    self.ping_site()
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying
        
        # Final stats
        logger.info("🛑 Shutting down site monitor...")
        self.log_stats()
        logger.info("👋 Goodbye!")

def main():
    """Main entry point."""
    # Create PID file to prevent multiple instances
    pid_file = "ping_site.pid"
    
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            old_pid = f.read().strip()
        logger.warning(f"PID file exists with PID {old_pid}. Another instance may be running.")
        
        # Try to check if the process is actually running
        try:
            os.kill(int(old_pid), 0)  # This will raise an exception if process doesn't exist
            logger.error("Another instance is already running. Exiting.")
            sys.exit(1)
        except (OSError, ValueError):
            logger.info("Old PID file found but process is not running. Removing stale PID file.")
            os.remove(pid_file)
    
    # Write current PID
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    
    try:
        pinger = SitePinger()
        pinger.run()
    finally:
        # Clean up PID file
        if os.path.exists(pid_file):
            os.remove(pid_file)

if __name__ == "__main__":
    main()
