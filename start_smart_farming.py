#!/usr/bin/env python3
"""
Smart Farming Complete Startup Script
Starts all services and provides comprehensive status monitoring
"""

import subprocess
import threading
import time
import os
import sys
import requests
import psutil
from datetime import datetime

class SmartFarmingManager:
    def __init__(self):
        self.services = {
            'streamlit': {
                'port': 8501,
                'process': None,
                'url': 'http://localhost:8501',
                'command': [sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.port', '8501'],
                'name': '🌾 Streamlit Frontend'
            },
            'web_api': {
                'port': 5000,
                'process': None,
                'url': 'http://localhost:5000',
                'command': [sys.executable, 'web_app.py'],
                'name': '🌐 Flask Web API'
            },
            'sms_chatbot': {
                'port': 5001,
                'process': None,
                'url': 'http://localhost:5001',
                'command': [sys.executable, 'twilio_chatbot.py'],
                'name': '📱 SMS Chatbot'
            }
        }
        
    def check_port_available(self, port):
        """Check if a port is available"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                return False, conn.pid
        return True, None
    
    def kill_port_process(self, port):
        """Kill process using a specific port"""
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    process = psutil.Process(conn.pid)
                    process.terminate()
                    time.sleep(2)
                    if process.is_running():
                        process.kill()
                    print(f"   ❌ Killed process {conn.pid} using port {port}")
                    return True
        except Exception as e:
            print(f"   ⚠️  Error killing process on port {port}: {e}")
        return False
    
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        print("🔍 Checking Dependencies...")
        
        required_files = [
            'app.py',
            'web_app.py', 
            'twilio_chatbot.py',
            'database.py',
            'crop_recommendation_model.pkl',
            'data/market_prices.csv'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"   ❌ Missing files: {', '.join(missing_files)}")
            return False
        else:
            print("   ✅ All required files present")
        
        # Check Python packages
        required_packages = ['streamlit', 'flask', 'twilio', 'pandas', 'scikit-learn', 'numpy']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"   ❌ Missing packages: {', '.join(missing_packages)}")
            print(f"   💡 Install with: pip install {' '.join(missing_packages)}")
            return False
        else:
            print("   ✅ All required packages installed")
        
        return True
    
    def start_service(self, service_name, service_config):
        """Start a single service"""
        try:
            # Check if port is available
            available, pid = self.check_port_available(service_config['port'])
            if not available:
                print(f"   ⚠️  Port {service_config['port']} in use by PID {pid}")
                if self.kill_port_process(service_config['port']):
                    time.sleep(2)
            
            # Start the service
            print(f"   🚀 Starting {service_config['name']}...")
            process = subprocess.Popen(
                service_config['command'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            service_config['process'] = process
            time.sleep(3)  # Give service time to start
            
            # Check if service started successfully
            if process.poll() is None:  # Process is still running
                print(f"   ✅ {service_config['name']} started successfully")
                print(f"      URL: {service_config['url']}")
                return True
            else:
                print(f"   ❌ {service_config['name']} failed to start")
                stdout, stderr = process.communicate()
                if stderr:
                    print(f"      Error: {stderr.decode()[:200]}...")
                return False
                
        except Exception as e:
            print(f"   ❌ Error starting {service_config['name']}: {e}")
            return False
    
    def check_service_health(self, service_name, service_config):
        """Check if a service is healthy"""
        try:
            if service_config['process'] and service_config['process'].poll() is None:
                # Try to make a health check request
                if service_name == 'streamlit':
                    # Streamlit doesn't have a standard health endpoint
                    response = requests.get(service_config['url'], timeout=5)
                    return response.status_code == 200
                else:
                    # Flask services should have /health endpoints
                    health_url = service_config['url'] + '/health'
                    response = requests.get(health_url, timeout=5)
                    return response.status_code == 200
            return False
        except Exception:
            return False
    
    def start_all_services(self):
        """Start all services"""
        print("🚀 Starting Smart Farming Assistant")
        print("=" * 60)
        
        # Check dependencies first
        if not self.check_dependencies():
            print("❌ Dependency check failed. Please resolve issues before starting.")
            return False
        
        print("\\n📋 Starting Services...")
        
        success_count = 0
        for service_name, service_config in self.services.items():
            if self.start_service(service_name, service_config):
                success_count += 1
        
        print(f"\\n📊 Service Status: {success_count}/{len(self.services)} started successfully")
        
        if success_count == len(self.services):
            print("\\n🎉 All services started successfully!")
            self.display_service_info()
            return True
        else:
            print("\\n⚠️  Some services failed to start")
            return False
    
    def display_service_info(self):
        """Display information about running services"""
        print("\\n🌟 Smart Farming Assistant - Service Information")
        print("=" * 60)
        
        print("📱 Main Application:")
        print(f"   • Streamlit Frontend: {self.services['streamlit']['url']}")
        print("   • Login with default accounts:")
        print("     - Admin: admin@smartfarm.com / admin123")
        print("     - Agent: agent@smartfarm.com / agent123")
        
        print("\\n🔗 API Endpoints:")
        print(f"   • Web API: {self.services['web_api']['url']}")
        print(f"   • Market Prices: {self.services['web_api']['url']}/api/market-prices")
        print(f"   • Crop Recommendation: {self.services['web_api']['url']}/api/crop-recommendation")
        
        print("\\n📱 SMS Integration:")
        print(f"   • SMS Chatbot: {self.services['sms_chatbot']['url']}")
        print(f"   • Twilio Phone: +15855399486")
        print("   • SMS Commands: HELP, PRICE [crop], RECOMMEND, LISTINGS")
        
        print("\\n🛠️ Admin Features:")
        print("   • User Management")
        print("   • Market Price Updates") 
        print("   • System Analytics")
        print("   • Broadcast Notifications")
        
        print("\\n👥 User Roles:")
        print("   • Farmers: Crop recommendations, listings, offers")
        print("   • Buyers: Browse crops, make offers, market data")
        print("   • Agents: Help farmers, manage listings")
        print("   • Admin: Full system access")
    
    def monitor_services(self):
        """Monitor running services"""
        print("\\n🔍 Monitoring Services (Press Ctrl+C to stop)...")
        
        try:
            while True:
                print(f"\\n⏰ {datetime.now().strftime('%H:%M:%S')} - Service Status:")
                
                all_healthy = True
                for service_name, service_config in self.services.items():
                    is_healthy = self.check_service_health(service_name, service_config)
                    status = "🟢 Healthy" if is_healthy else "🔴 Down"
                    print(f"   {service_config['name']}: {status}")
                    
                    if not is_healthy:
                        all_healthy = False
                
                if all_healthy:
                    print("   ✅ All services running normally")
                else:
                    print("   ⚠️  Some services need attention")
                
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\\n\\n🛑 Monitoring stopped by user")
            self.stop_all_services()
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\\n🛑 Stopping all services...")
        
        for service_name, service_config in self.services.items():
            if service_config['process']:
                try:
                    service_config['process'].terminate()
                    time.sleep(2)
                    if service_config['process'].poll() is None:
                        service_config['process'].kill()
                    print(f"   ✅ {service_config['name']} stopped")
                except Exception as e:
                    print(f"   ⚠️  Error stopping {service_config['name']}: {e}")
        
        print("\\n✅ All services stopped successfully!")
    
    def run(self):
        """Main run method"""
        try:
            if self.start_all_services():
                self.monitor_services()
        except KeyboardInterrupt:
            print("\\n\\n🛑 Shutdown initiated by user")
            self.stop_all_services()
        except Exception as e:
            print(f"\\n❌ Unexpected error: {e}")
            self.stop_all_services()

def main():
    """Main function"""
    print("🌾 Smart Farming Assistant - Complete Startup")
    print("=" * 50)
    print("🔧 Initializing Smart Farming Manager...")
    
    manager = SmartFarmingManager()
    manager.run()

if __name__ == "__main__":
    main()
