// Vercel Serverless Function - Open Graph image extractor
const https = require('https');
const http = require('http');

module.exports = async function handler(req, res) {
  const url = req.query.url;
  if (!url) { res.status(400).json({ error: 'Missing url' }); return; }
  
  try {
    const imgUrl = await extractOgImage(url);
    if (imgUrl) {
      res.status(200).json({ image: imgUrl });
    } else {
      res.status(200).json({ image: null });
    }
  } catch (e) {
    res.status(200).json({ image: null });
  }
};

function fetch(url) {
  return new Promise((resolve, reject) => {
    const proto = url.startsWith('https') ? https : http;
    const req = proto.get(url, {
      timeout: 5000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

async function extractOgImage(url) {
  try {
    const html = await fetch(url);
    // Try Twitter card first
    const twImg = html.match(/<meta\s+name=["']twitter:image["']\s+content=["']([^"']+)["']/i);
    if (twImg) return twImg[1];
    // Try og:image
    const ogImg = html.match(/<meta\s+property=["']og:image["']\s+content=["']([^"']+)["']/i);
    if (ogImg) return ogImg[1];
    // Try article:image
    const artImg = html.match(/<meta\s+property=["']article:image["']\s+content=["']([^"']+)["']/i);
    if (artImg) return artImg[1];
    return null;
  } catch (e) {
    return null;
  }
}
