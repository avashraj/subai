const http = require('http');
const corsProxy = require('cors-anywhere');

// Listen on a specific IP address and port
const host = '0.0.0.0';
const port = 8080;

// Start the CORS proxy server
corsProxy.createServer({
  originWhitelist: [],  // Allow all origins for development
  requireHeader: ['origin', 'x-requested-with'],
  removeHeaders: ['cookie', 'cookie2'],
}).listen(port, host, () => {
  console.log(`CORS Anywhere is running on ${host}:${port}`);
});
