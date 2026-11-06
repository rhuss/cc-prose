import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import plugin, { ProsePlugin } from '../.opencode/plugins/prose.js';
import rootEntry from '../index.js';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const expected = fs.readdirSync(path.join(root, 'prose/skills')).sort();

test('V1 registration is idempotent and preserves other skills paths', async () => {
  const hooks = await ProsePlugin({});
  const config = { skills: { paths: ['/existing'] } };
  await hooks.config(config);
  await hooks.config(config);
  assert.deepEqual(config.skills.paths, ['/existing', path.join(root, 'prose/skills')]);
  const v2 = { skills: [] };
  await hooks.config(v2);
  assert.deepEqual(v2, { skills: [] });
});

test('V2 registers all shared files with usable descriptions and real paths', async () => {
  const registered = [];
  await plugin.setup({ skill: { transform: async (callback) => callback({ add: (skill) => registered.push(skill) }) } });
  assert.equal(registered.length, 11);
  assert.deepEqual(registered.map(s => s.id).sort(), expected);
  for (const skill of registered) {
    assert.equal(skill.name, skill.id);
    assert.ok(skill.description.length > 10);
    assert.ok(fs.existsSync(skill.path));
    assert.ok(skill.content.includes('harness guide'));
    assert.ok(!skill.content.startsWith('---'));
  }
  assert.ok(registered.find(s => s.id === 'content-generator').description.includes('Prevents AI patterns'));
});

test('V2 delayed callback rejection does not prevent other registrations', async () => {
  let callback;
  await plugin.setup({ skill: { transform: async (fn) => { callback = fn; } } });
  const errors = [];
  const original = console.error;
  const registered = [];
  console.error = (...args) => errors.push(args);
  try {
    callback({ add: (skill) => { if (skill.id === 'humanizer') throw new Error('host rejection'); registered.push(skill.id); } });
  } finally { console.error = original; }
  assert.equal(registered.length, 10);
  assert.equal(errors.length, 1);
  assert.ok(errors[0][0].includes('humanizer'));
});

test('V1-shaped or absent setup context is harmless', async () => {
  await plugin.setup();
  await plugin.setup({});
  assert.equal(rootEntry, plugin);
});

test('resource paths are independent of the consumer cwd', async () => {
  const cwd = process.cwd();
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'cc-prose-adapter-'));
  const skills = [];
  try {
    process.chdir(temp);
    await plugin.setup({ skill: { transform: async fn => fn({ add: s => skills.push(s) }) } });
    assert.equal(skills.length, 11);
    assert.ok(skills.every(s => s.path.startsWith(path.join(root, 'prose/skills'))));
  } finally { process.chdir(cwd); fs.rmSync(temp, { recursive: true }); }
});
