// Vercel function - returns news as JSONP (callback=renderNews)
module.exports = async (req, res) => {
  const https = require('https');
  const category = req.query.category || '';
  let url = 'https://aihot.virxact.com/api/public/items?mode=selected&take=60';
  if (category) url += '&category=' + category;
  
  try {
    const data = await new Promise((resolve, reject) => {
      https.get(url, {
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
    res.status(200).send('window.renderNews(' + JSON.stringify(data) + ');');
  } catch(e) {
    res.setHeader('Content-Type', 'application/javascript');
    res.status(200).send('window.renderNews({items:[]});');
  }
};
