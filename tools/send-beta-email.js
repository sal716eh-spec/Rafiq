/* send-beta-email.js — send the beta relaunch email through Resend.
   Run by the "Beta email" GitHub Action; needs SUPABASE_ACCESS_TOKEN and RESEND_API_KEY.
   The repo is public, so Action logs are public: addresses are always masked,
   and a single recipient is chosen by account id, never by email.

     node tools/send-beta-email.js test <account-id>     one account (the test copy)
     node tools/send-beta-email.js all SEND-TO-ALL        every confirmed account

   The email is supabase/email-templates/beta-relaunch.html; its subject is in the
   comment on the first line, and {{GREETING}} becomes "Assalamu alaykum <name>,". */
const fs = require('fs'), path = require('path');
const REF = 'gaajfahtrbdybjuunfhe';
const TOKEN = process.env.SUPABASE_ACCESS_TOKEN, KEY = process.env.RESEND_API_KEY;
const FROM = 'Rafiq <hello@contact.rafiq-arabic.com>', REPLY_TO = 'feedback@rafiq-arabic.com';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

async function sql(query) {
  const r = await fetch(`https://api.supabase.com/v1/projects/${REF}/database/query`, {
    method: 'POST', headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }) });
  const t = await r.text();
  if (!r.ok) { console.error(`query failed: ${r.status} ${t.slice(0, 300)}`); process.exit(1); }
  return JSON.parse(t);
}
const mask = e => { const [u, d = ''] = String(e || '').split('@'); const [dn, ...tld] = d.split('.');
  const m = s => s.length <= 2 ? s[0] + '*' : s.slice(0, 2) + '***' + s.slice(-1);
  return u.split('+').map(m).join('+') + '@' + m(dn || '') + (tld.length ? '.' + tld.join('.') : ''); };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const file = fs.readFileSync(path.join(__dirname, '..', 'supabase/email-templates/beta-relaunch.html'), 'utf8');
const SUBJECT = file.match(/Subject:\s*([^>]+?)\s*-->/)[1];
const BODY = file.replace(/^<!--[\s\S]*?-->\s*/, '');
// a plain-text copy for mail apps that don't show HTML
const text = html => html.replace(/<li>/g, '• ').replace(/<br>/g, '\n').replace(/<\/(p|li|ul|div|tr)>/g, '\n')
  .replace(/<a [^>]*href="(https[^"]+)"[^>]*>([^<]+)<\/a>/g, '$2: $1').replace(/<[^>]+>/g, '')
  .replace(/&amp;/g, '&').replace(/[ \t]+/g, ' ').replace(/\n\s*\n\s*/g, '\n\n').trim();

async function send(u) {
  const name = (u.name || '').trim().split(/\s+/)[0];
  const html = BODY.replace('{{GREETING}}', esc(name ? `Assalamu alaykum ${name},` : 'Assalamu alaykum,'));
  const r = await fetch('https://api.resend.com/emails', { method: 'POST',
    headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: [u.email], reply_to: REPLY_TO, subject: SUBJECT, html, text: text(html) }) });
  const j = await r.json().catch(() => ({}));
  console.log(`${r.ok ? 'sent' : 'FAILED'}  ${u.id}  ${mask(u.email)}${r.ok ? '' : '  ' + (j.message || r.status)}`);
  return r.ok;
}

(async () => {
  if (!TOKEN || !KEY) { console.error('SUPABASE_ACCESS_TOKEN and RESEND_API_KEY are needed'); process.exit(1); }
  const [cmd, arg] = process.argv.slice(2);
  const cols = `id, email, raw_user_meta_data->>'name' as name`;
  let users;
  if (cmd === 'test') {
    if (!UUID.test(arg || '')) { console.error('give one account id (uuid)'); process.exit(1); }
    users = await sql(`select ${cols} from auth.users where id = '${arg}'`);
  } else if (cmd === 'all') {
    if (arg !== 'SEND-TO-ALL') { console.error('to email everyone, the second input must be SEND-TO-ALL'); process.exit(1); }
    users = await sql(`select ${cols} from auth.users where email_confirmed_at is not null and email is not null order by created_at`);
  } else { console.error('use: test <account-id> | all SEND-TO-ALL'); process.exit(1); }
  if (!users.length) { console.error('no matching accounts'); process.exit(1); }
  console.log(`Subject: ${SUBJECT}\nSending to ${users.length} account(s):`);
  let ok = 0;
  for (const u of users) { if (await send(u)) ok++; await new Promise(r => setTimeout(r, 600)); }  // Resend: 2 a second
  console.log(`${ok} of ${users.length} sent`);
  if (ok < users.length) process.exit(1);
})();
