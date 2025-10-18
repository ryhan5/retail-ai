const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Install frontend dependencies and build
console.log('Installing frontend dependencies...');
execSync('cd frontend && npm install && npm run build', { stdio: 'inherit' });

// Install Python dependencies
console.log('Installing Python dependencies...');
if (process.platform === 'win32') {
  execSync('pip install -r requirements.txt', { stdio: 'inherit' });
} else {
  execSync('pip3 install -r requirements.txt', { stdio: 'inherit' });
}

// Create vercel_build directory
const vercelBuildDir = path.join(__dirname, 'vercel_build');
if (!fs.existsSync(vercelBuildDir)) {
  fs.mkdirSync(vercelBuildDir);
}

// Copy frontend build files
console.log('Copying frontend build files...');
const frontendBuildDir = path.join(__dirname, 'frontend', 'build');
if (fs.existsSync(frontendBuildDir)) {
  const copyRecursiveSync = (src, dest) => {
    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    const isDirectory = exists && stats.isDirectory();
    
    if (isDirectory) {
      if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest);
      }
      fs.readdirSync(src).forEach(childItemName => {
        copyRecursiveSync(
          path.join(src, childItemName),
          path.join(dest, childItemName)
        );
      });
    } else {
      fs.copyFileSync(src, dest);
    }
  };
  
  copyRecursiveSync(frontendBuildDir, vercelBuildDir);
}

// Create API endpoints
console.log('Creating API endpoints...');
const apiRoutes = [
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
];

apiRoutes.forEach(route => {
  const endpointDir = path.join(vercelBuildDir, route);
  if (!fs.existsSync(endpointDir)) {
    fs.mkdirSync(endpointDir, { recursive: true });
  }
  
  const indexPath = path.join(endpointDir, 'index.py');
  const content = `from app import app

def handler(event, context):
    return app(event, context)`;
    
  fs.writeFileSync(indexPath, content);
});

console.log('Vercel build completed successfully!');
