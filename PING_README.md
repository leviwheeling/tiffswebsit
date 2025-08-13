# Duncan Family Dentistry Site Ping Monitor

This directory contains scripts to automatically ping duncanfamilydental.com every 10 minutes to keep the site active and prevent it from going to sleep on hosting platforms like Render.

## Files Created

### 1. `ping_site.py` - Standalone Ping Script
A standalone Python script that runs independently and pings the site every 10 minutes.

**Features:**
- Logs all ping attempts with timestamps
- Tracks success/failure statistics
- Graceful shutdown handling (Ctrl+C)
- Prevents multiple instances from running
- Creates log files for monitoring
- 30-second timeout for requests

### 2. `ping_service.py` - FastAPI Background Service
An async background service that can be integrated into the existing FastAPI application.

**Features:**
- Runs as a background task within FastAPI
- Async HTTP requests using aiohttp
- Statistics endpoint at `/ping-stats`
- Automatic startup/shutdown with the FastAPI app

### 3. `main_with_ping.py` - Updated FastAPI App
A version of the main FastAPI application that includes the integrated ping service.

### 4. `start_ping.sh` - Convenience Script
A shell script to easily start the standalone ping monitor with dependency checking.

## Usage Options

### Option 1: Standalone Script (Recommended for separate monitoring)

```bash
# Make sure you're in the project directory
cd /Users/leviwheeling/duncan-family-dentistry

# Activate virtual environment (if using one)
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the ping script
python3 ping_site.py

# Or use the convenience script
./start_ping.sh
```

### Option 2: Integrated with FastAPI (Recommended for production)

```bash
# Replace your current main.py with the ping-enabled version
cp main_with_ping.py app/main.py

# Or manually integrate the changes from main_with_ping.py into your existing main.py

# Install additional dependencies
pip install aiohttp

# Run your FastAPI app as usual
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Check ping statistics at: http://localhost:8000/ping-stats
```

### Option 3: Production Deployment

For production deployment on platforms like Render:

1. Update your `requirements.txt` to include the new dependencies
2. Use the integrated FastAPI version (`main_with_ping.py`)
3. The ping service will automatically start when your app deploys
4. Monitor statistics via the `/ping-stats` endpoint

## Monitoring

### Standalone Script
- Logs are written to `ping_site.log`
- Console output shows real-time status
- Statistics are logged every 10 pings
- PID file prevents multiple instances

### FastAPI Integration
- Check `/ping-stats` endpoint for current statistics
- Logs are integrated with FastAPI logs
- Service starts/stops with the main application

## Log Output Examples

```
2024-01-10 10:30:00,123 - INFO - 🚀 Starting Duncan Family Dentistry site monitor...
2024-01-10 10:30:00,124 - INFO - Target URL: https://duncanfamilydental.com
2024-01-10 10:30:00,125 - INFO - Ping interval: 600 seconds (10.0 minutes)
2024-01-10 10:30:01,256 - INFO - ✅ Ping #1 successful - Status: 200 - Response time: 1.13s
2024-01-10 10:40:01,789 - INFO - ✅ Ping #2 successful - Status: 200 - Response time: 0.89s
```

## Statistics Endpoint

When using the FastAPI integration, you can check ping statistics at `/ping-stats`:

```json
{
  "total_pings": 25,
  "successful": 24,
  "failed": 1,
  "success_rate": 96.0,
  "running": true
}
```

## Troubleshooting

### Common Issues

1. **Permission denied on shell script**
   ```bash
   chmod +x start_ping.sh
   ```

2. **Missing dependencies**
   ```bash
   pip install requests aiohttp
   ```

3. **Multiple instances running**
   - The standalone script prevents this automatically
   - Check for `ping_site.pid` file

4. **FastAPI integration not working**
   - Ensure you've copied the startup/shutdown event handlers
   - Check that `ping_service.py` is in the same directory
   - Verify aiohttp is installed

### Stopping the Service

- **Standalone**: Press Ctrl+C or send SIGTERM
- **FastAPI**: The service stops when the FastAPI app shuts down

## Customization

You can modify the following parameters in either script:

- `SITE_URL` / `site_url`: The URL to ping (default: https://duncanfamilydental.com)
- `PING_INTERVAL` / `ping_interval`: Time between pings in seconds (default: 600 = 10 minutes)
- `TIMEOUT` / `timeout`: Request timeout in seconds (default: 30)

## Security Notes

- The scripts use a proper User-Agent header
- Requests include standard browser headers
- No sensitive information is logged
- The ping service respects the site's robots.txt and normal rate limiting
