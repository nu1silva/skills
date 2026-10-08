/**
 * inspect_page.js
 * Usage: node inspect_page.js <url> [username] [password] [output_path]
 *
 * Navigates to a URL (optionally logging in), then extracts all interactive
 * elements: buttons, links, forms, inputs, selects, textareas.
 * Outputs a structured JSON report.
 */

const { chromium } = require('playwright');
const fs = require('fs');

const [,, url, username, password, outputPath = '/tmp/inspection.json'] = process.argv;

if (!url) {
  console.error('Usage: node inspect_page.js <url> [username] [password] [output_path]');
  process.exit(1);
}

const USER_SELECTORS = [
  'input[name="username"]', 'input[name="email"]', 'input[name="user"]',
  'input[type="email"]', 'input[id*="user"]', 'input[id*="email"]',
  'input[placeholder*="user" i]', 'input[placeholder*="email" i]',
];
const PASS_SELECTORS = [
  'input[name="password"]', 'input[type="password"]',
  'input[id*="pass"]', 'input[placeholder*="pass" i]',
];

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  const page = await context.newPage();

  console.error(`Navigating to: ${url}`);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });

  // --- Optional login ---
  if (username && password) {
    let filledUser = false, filledPass = false;
    for (const sel of USER_SELECTORS) {
      if (await page.locator(sel).count() > 0) {
        await page.locator(sel).first().fill(username);
        filledUser = true; break;
      }
    }
    for (const sel of PASS_SELECTORS) {
      if (await page.locator(sel).count() > 0) {
        await page.locator(sel).first().fill(password);
        filledPass = true; break;
      }
    }
    if (filledUser && filledPass) {
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {}),
        page.keyboard.press('Enter'),
      ]);
      await page.waitForTimeout(2000);
      console.error('Logged in successfully.');
    } else {
      console.error('Warning: Could not find login fields.');
    }
  }

  // --- Extract interactive elements ---
  const data = await page.evaluate(() => {
    const clean = (str) => (str || '').replace(/\s+/g, ' ').trim().substring(0, 200);
    const rect = (el) => {
      const r = el.getBoundingClientRect();
      return { x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height) };
    };
    const visible = (el) => {
      const s = getComputedStyle(el);
      return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
    };

    // Buttons
    const buttons = Array.from(document.querySelectorAll('button, input[type="button"], input[type="submit"], input[type="reset"], [role="button"]'))
      .filter(visible)
      .map(el => ({
        tag: el.tagName.toLowerCase(),
        text: clean(el.innerText || el.value || el.getAttribute('aria-label')),
        type: el.getAttribute('type') || null,
        id: el.id || null,
        name: el.getAttribute('name') || null,
        disabled: el.disabled || false,
        position: rect(el),
      }));

    // Links
    const links = Array.from(document.querySelectorAll('a[href]'))
      .filter(visible)
      .map(el => ({
        text: clean(el.innerText || el.getAttribute('aria-label')),
        href: el.href,
        target: el.getAttribute('target') || null,
        id: el.id || null,
      }));

    // Forms
    const forms = Array.from(document.querySelectorAll('form')).map(form => ({
      id: form.id || null,
      name: form.getAttribute('name') || null,
      action: form.action || null,
      method: form.method || 'get',
      fields: Array.from(form.querySelectorAll('input, select, textarea'))
        .filter(visible)
        .map(el => ({
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute('type') || null,
          name: el.getAttribute('name') || null,
          id: el.id || null,
          placeholder: clean(el.getAttribute('placeholder')),
          label: (() => {
            if (el.id) {
              const lbl = document.querySelector(`label[for="${el.id}"]`);
              if (lbl) return clean(lbl.innerText);
            }
            const parent = el.closest('label');
            if (parent) return clean(parent.innerText);
            return null;
          })(),
          required: el.required || false,
          value: el.type === 'password' ? '***' : clean(el.value),
          options: el.tagName.toLowerCase() === 'select'
            ? Array.from(el.options).map(o => ({ value: o.value, text: clean(o.text) }))
            : null,
        })),
    }));

    // Standalone inputs (not inside a form)
    const standaloneInputs = Array.from(document.querySelectorAll('input, select, textarea'))
      .filter(el => !el.closest('form') && visible(el))
      .map(el => ({
        tag: el.tagName.toLowerCase(),
        type: el.getAttribute('type') || null,
        name: el.getAttribute('name') || null,
        id: el.id || null,
        placeholder: clean(el.getAttribute('placeholder')),
        required: el.required || false,
      }));

    return { buttons, links, forms, standaloneInputs };
  });

  const report = {
    url: page.url(),
    title: await page.title(),
    capturedAt: new Date().toISOString(),
    summary: {
      totalButtons: data.buttons.length,
      totalLinks: data.links.length,
      totalForms: data.forms.length,
      totalStandaloneInputs: data.standaloneInputs.length,
    },
    buttons: data.buttons,
    links: data.links,
    forms: data.forms,
    standaloneInputs: data.standaloneInputs,
  };

  fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
  console.error(`Report saved to: ${outputPath}`);
  console.log(JSON.stringify(report, null, 2));

  await browser.close();
})().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});