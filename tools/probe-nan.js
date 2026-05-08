// Headless probe: open the PRD, switch through detail/add views, log any NaN occurrences.
const { execSync } = require('child_process');

(async () => {
  // Use Chrome's headless mode with --dump-dom (snapshot only — no JS interaction).
  // Then evaluate the page once to print rendered DOM containing "NaN".
  const url = 'http://127.0.0.1:8090/FoneSquare-PRD-v2.html';
  const cdp = require('child_process');
  // We use puppeteer-core dynamically if installed, else fallback to chrome --dump-dom.
  let pup;
  try { pup = require('puppeteer-core'); } catch (_) {}
  if (!pup) {
    console.log('[fallback] puppeteer-core not installed, using chrome --dump-dom (after JS) ...');
    const out = execSync(
      `'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --headless=new --no-sandbox --disable-gpu --virtual-time-budget=4000 --dump-dom "${url}"`,
      { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 }
    );
    const re = /[^>\s][^>]{0,40}NaN[^<]{0,40}/g;
    const hits = out.match(re) || [];
    console.log('hits:', hits.length);
    hits.slice(0, 25).forEach((h, i) => console.log('  ' + i + ':', h.replace(/\s+/g, ' ').trim()));
    process.exit(0);
  }
  const browser = await pup.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.waitForTimeout(1500);
  const probe = async (sel) => {
    if (sel) await page.click(sel);
    await page.waitForTimeout(800);
    const html = await page.content();
    const re = /[^>\s][^>]{0,40}NaN[^<]{0,40}/g;
    return html.match(re) || [];
  };
  console.log('# list view (default):', JSON.stringify((await probe()).slice(0, 10)));
  console.log('# detail view:',         JSON.stringify((await probe('a[data-page="page-web-merchant-detail"]')).slice(0, 10)));
  console.log('# add view:',            JSON.stringify((await probe('a[data-page="page-web-merchant-add"]')).slice(0, 10)));
  await browser.close();
})();
