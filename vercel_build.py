import os
import shutil
import subprocess
import sys

def run_command(command):
    try:
        subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e}")
        return False

def main():
    print("Starting Vercel build process...")
    
    # Create vercel_build directory
    vercel_build_dir = os.path.join(os.path.dirname(__file__), 'vercel_build')
    if not os.path.exists(vercel_build_dir):
        os.makedirs(vercel_build_dir)
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install Python dependencies")
        sys.exit(1)
    
    # Install frontend dependencies and build
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    if os.path.exists(frontend_dir):
        print("Building frontend...")
        os.chdir(frontend_dir)
        if not run_command("npm install"):
            print("Failed to install frontend dependencies")
            sys.exit(1)
        if not run_command("npm run build"):
            print("Failed to build frontend")
            sys.exit(1)
        os.chdir('..')
        
        # Copy frontend build to vercel_build
        frontend_build_dir = os.path.join(frontend_dir, 'build')
        if os.path.exists(frontend_build_dir):
            print("Copying frontend build files...")
            dest_dir = os.path.join(vercel_build_dir, 'frontend')
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(frontend_build_dir, dest_dir)
    
    # Create API endpoints
    print("Creating API endpoints...")
    api_endpoints = [
        '/api/chat',
        '/api/customer-context',
        '/api/products/search',
        '/api/inventory/check',
        '/api/promotions',
        '/api/orders',
        '/api/payment/process',
        '/api/analytics/dashboard',
        '/api/webhook/whatsapp',
        '/api/webhook/telegram',
        '/api/messaging/status',
        '/api/messaging/setup',
        '/api/telegram/webhook'
    ]
    
    for endpoint in api_endpoints:
        endpoint_dir = os.path.join(vercel_build_dir, endpoint.lstrip('/'))
        os.makedirs(endpoint_dir, exist_ok=True)
        
        # Create index.py for each endpoint
        with open(os.path.join(endpoint_dir, 'index.py'), 'w') as f:
            f.write('''from app import app

def handler(event, context):
    return app(event, context)''')
    
    print("Vercel build completed successfully!")

if __name__ == "__main__":
    main()
