// Vercel function that returns news data as JS variable assignment
module.exports = async (req, res) => {
  const https = require('https');
  try {
    const data = await new Promise((resolve, reject) => {
      https.get('https://aihot.virxact.com/api/public/items?mode=selected&take=20', {
        headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' }
      }, (res2) => {
        let body = '';
        res2.on('data', chunk => body += chunk);
        res2.on('end', () => {
          try { resolve(JSON.parse(body)); }
          catch(e) { reject(e); }
        });
      }).on('error', reject);
    });
    res.setHeader('Content-Type', 'application/javascript');
    res.setHeader('Cache-Control', 's-maxage=300');
    res.status(200).send('window.__newsData=' + JSON.stringify(data) + ';');
  } catch(e) {
    res.setHeader('Content-Type', 'application/javascript');
    res.status(200).send('window.__newsData=[];');
  }
};
