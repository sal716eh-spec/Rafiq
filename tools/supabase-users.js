/* supabase-users.js — list recent accounts, or delete chosen ones (Management API,
   secret SUPABASE_ACCESS_TOKEN). Run by the "Supabase users" GitHub Action.
   The repo is public, so Action logs are public: emails are always masked.

     node tools/supabase-users.js list [days]      accounts created in the last N days (default 3)
     node tools/supabase-users.js delete id1,id2   delete these accounts (max 5) and their rows
     node tools/supabase-users.js reset-preview    who a beta reset would wipe (changes nothing)
     node tools/supabase-users.js reset RESET-BETA wipe progress + onboarding answers for them
     node tools/supabase-users.js signout SIGN-OUT-ALL  end every session on every device
                                                   (with SIGN_IN_AGAIN_BEFORE in auth.js)

   The beta reset keeps accounts that were created or onboarded today (UK time):
   they've already seen the current app. For everyone else it deletes their rows
   in every table with a user_id (progress, profile = onboarding answers, …)
   except 'settings', whose migrated_v2 flag stops old browser data re-importing. */
const REF = 'gaajfahtrbdybjuunfhe';
const TOKEN = process.env.SUPABASE_ACCESS_TOKEN;
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

async function sql(query) {
  const r = await fetch(`https://api.supabase.com/v1/projects/${REF}/database/query`, {
    method: 'POST', headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }) });
  const t = await r.text();
  if (!r.ok) { console.error(`query failed: ${r.status} ${t.slice(0, 300)}`); process.exit(1); }
  return JSON.parse(t);
}
// yo***7+te***@gm***.com
const mask = e => { const [u, d = ''] = String(e || '').split('@'); const [dn, ...tld] = d.split('.');
  const m = s => s.length <= 2 ? s[0] + '*' : s.slice(0, 2) + '***' + s.slice(-1);
  return u.split('+').map(m).join('+') + '@' + m(dn || '') + (tld.length ? '.' + tld.join('.') : ''); };

// public tables with a user_id column (progress etc.), so a deleted account leaves nothing behind
async function userTables() {
  return (await sql(`select table_name from information_schema.columns
                     where table_schema='public' and column_name='user_id'`)).map(r => r.table_name);
}

(async () => {
  if (!TOKEN) { console.error('SUPABASE_ACCESS_TOKEN is not set'); process.exit(1); }
  const [cmd, arg] = process.argv.slice(2);
  if (cmd === 'list') {
    const days = Math.max(1, Math.min(60, parseInt(arg, 10) || 3));
    const tables = await userTables();
    const rows = await sql(`select id, email, created_at, email_confirmed_at, last_sign_in_at from auth.users
                            where created_at > now() - interval '${days} days' order by created_at`);
    const total = (await sql('select count(*)::int as n from auth.users'))[0].n;
    console.log(`${total} accounts in total; ${rows.length} created in the last ${days} day(s):`);
    for (const u of rows) {
      let n = 0;
      for (const t of tables) n += (await sql(`select count(*)::int as n from public."${t}" where user_id='${u.id}'`))[0].n;
      console.log(`${u.id}  ${mask(u.email)}  created ${u.created_at.slice(0, 16)}  ` +
                  `confirmed ${u.email_confirmed_at ? 'yes' : 'no'}  last sign-in ${(u.last_sign_in_at || '—').slice(0, 16)}  rows ${n}`);
    }
    return;
  }
  if (cmd === 'delete') {
    const ids = String(arg || '').split(',').map(s => s.trim()).filter(Boolean);
    if (!ids.length || ids.length > 5 || !ids.every(i => UUID.test(i))) { console.error('give 1-5 account ids (uuids), comma-separated'); process.exit(1); }
    const list = ids.map(i => `'${i}'`).join(',');
    const found = await sql(`select id, email from auth.users where id in (${list})`);
    if (found.length !== ids.length) { console.error(`only ${found.length} of ${ids.length} ids exist; nothing deleted`); process.exit(1); }
    for (const t of await userTables()) {
      const r = await sql(`with d as (delete from public."${t}" where user_id in (${list}) returning 1) select count(*)::int as n from d`);
      if (r[0].n) console.log(`${t}: ${r[0].n} rows deleted`);
    }
    await sql(`delete from auth.users where id in (${list})`);
    found.forEach(u => console.log(`deleted ${u.id}  ${mask(u.email)}`));
    return;
  }
  if (cmd === 'reset-preview' || cmd === 'reset') {
    if (cmd === 'reset' && arg !== 'RESET-BETA') { console.error('to wipe, the second input must be RESET-BETA'); process.exit(1); }
    const tables = (await userTables()).filter(t => t !== 'settings');
    const today = `(date_trunc('day', now() at time zone 'Europe/London') at time zone 'Europe/London')`;
    const pcols = (await sql(`select column_name from information_schema.columns
                              where table_schema='public' and table_name='profiles'`)).map(r => r.column_name);
    const pAt = pcols.includes('created_at') ? 'coalesce(p.created_at, p.updated_at)' : 'p.updated_at';
    const rows = await sql(`select u.id, u.email, u.created_at, ${pAt} as onboarded_at, p.onboarded,
                              (u.created_at >= ${today} or coalesce(${pAt} >= ${today}, false)) as keep
                            from auth.users u left join public.profiles p on p.user_id = u.id order by u.created_at`);
    console.log(`Today (UK) starts ${(await sql(`select ${today} as t`))[0].t}. Tables wiped: ${tables.join(', ')}`);
    const wipe = [];
    for (const u of rows) {
      let n = 0;
      for (const t of tables) n += (await sql(`select count(*)::int as n from public."${t}" where user_id='${u.id}'`))[0].n;
      console.log(`${u.keep ? 'KEEP ' : 'RESET'}  ${u.id}  ${mask(u.email)}  created ${String(u.created_at).slice(0, 16)}  ` +
                  `onboarded ${u.onboarded_at ? String(u.onboarded_at).slice(0, 16) : 'no'}  rows ${n}`);
      if (!u.keep) wipe.push(u);
    }
    console.log(`${wipe.length} to reset, ${rows.length - wipe.length} kept`);
    if (cmd === 'reset-preview' || !wipe.length) return;
    const list = wipe.map(u => `'${u.id}'`).join(',');
    for (const t of tables) {
      const r = await sql(`with d as (delete from public."${t}" where user_id in (${list}) returning 1) select count(*)::int as n from d`);
      console.log(`${t}: ${r[0].n} rows deleted`);
    }
    console.log('reset done');
    return;
  }
  if (cmd === 'signout') {
    if (arg !== 'SIGN-OUT-ALL') { console.error('to sign everyone out, the second input must be SIGN-OUT-ALL'); process.exit(1); }
    const r = await sql(`with d as (delete from auth.sessions returning 1) select count(*)::int as n from d`);
    const t = await sql(`with d as (delete from auth.refresh_tokens returning 1) select count(*)::int as n from d`);
    console.log(`${r[0].n} sessions and ${t[0].n} refresh tokens ended; everyone signs in again`);
    return;
  }
  console.error('use: list [days] | delete id1,id2 | reset-preview | reset RESET-BETA | signout SIGN-OUT-ALL'); process.exit(1);
})();
