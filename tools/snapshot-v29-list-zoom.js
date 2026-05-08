const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new', args: ['--no-sandbox','--window-size=1500,1000']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1500, height: 1000, deviceScaleFactor: 2 });
  await page.goto('http://localhost:8090/FoneSquare-PRD-v2.html', { waitUntil:'networkidle0', timeout:30000 });
  await new Promise(r => setTimeout(r, 800));

  const shell = await page.$('.wf-prototype-shell[data-init-view="list"]');
  if (shell) {
    // find the table inside
    const table = await shell.$('.wf-table-list');
    if (table) {
      await table.scrollIntoView();
      await new Promise(r => setTimeout(r, 300));
      await page.screenshot({ path: '/tmp/prd-v29-list-table.png', clip: await table.boundingBox() });
      console.log('list table screenshot ok');
    } else {
      console.log('table not found, taking full shell');
      await shell.scrollIntoView();
      await new Promise(r => setTimeout(r, 200));
      await page.screenshot({ path: '/tmp/prd-v29-list-table.png', clip: await shell.boundingBox() });
    }
  }
  await browser.close();
  console.log('done');
})().catch(err => { console.error(err); process.exit(1); });
