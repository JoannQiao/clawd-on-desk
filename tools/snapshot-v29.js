const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    args: ['--no-sandbox','--window-size=1500,1000']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1500, height: 1000, deviceScaleFactor: 1 });
  await page.goto('http://localhost:8090/FoneSquare-PRD-v2.html', { waitUntil:'networkidle0', timeout:30000 });
  await new Promise(r => setTimeout(r, 800));

  // 1) 列表页原型
  const listShell = await page.$('.wf-prototype-shell[data-init-view="list"]');
  if (listShell) {
    await listShell.scrollIntoView();
    await new Promise(r => setTimeout(r, 300));
    await page.screenshot({ path: '/tmp/prd-v29-list.png', clip: await listShell.boundingBox() });
    console.log('list screenshot ok');
  } else { console.log('list shell NOT FOUND'); }

  // 2) 详情页原型 - 依次截 5 个 Tab
  const detailShell = await page.$('.wf-prototype-shell[data-init-view="detail"]');
  if (detailShell) {
    const tabs = ['basic','kyc','quota','sales','log'];
    for (const t of tabs) {
      await page.evaluate((tabKey) => {
        const shell = document.querySelector('.wf-prototype-shell[data-init-view="detail"]');
        if (!shell) return;
        const tab = shell.querySelector('[data-tab="' + tabKey + '"]');
        if (tab) tab.click();
      }, t);
      await new Promise(r => setTimeout(r, 200));
      await detailShell.scrollIntoView();
      await new Promise(r => setTimeout(r, 200));
      await page.screenshot({ path: '/tmp/prd-v29-detail-' + t + '.png', clip: await detailShell.boundingBox() });
      console.log('detail-' + t + ' screenshot ok');
    }
  } else { console.log('detail shell NOT FOUND'); }

  await browser.close();
  console.log('all done');
})().catch(err => { console.error(err); process.exit(1); });
