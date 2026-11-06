// Register the same on-disk skills in OpenCode V1 and V2. No writing policy lives here.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const skillsDirectory = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../prose/skills');

// Read only the scalar fields required by native skill discovery. This is not a
// general YAML parser: all maintained skills use plain/quoted or folded strings.
function metadata(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)([\s\S]*)$/);
  if (!match) throw new Error('missing SKILL.md frontmatter');
  const fields = {};
  let current;
  for (const line of match[1].split(/\r?\n/)) {
    const field = line.match(/^([\w-]+):\s*(.*)$/);
    if (field) {
      current = field[1];
      fields[current] = /^[>|][-+]?$/.test(field[2]) ? '' : field[2];
    } else if (current && /^\s+/.test(line)) {
      fields[current] += ` ${line.trim()}`;
    }
  }
  for (const key of ['name', 'description']) {
    fields[key] = (fields[key] || '').trim().replace(/^(["'])([\s\S]*)\1$/, '$2');
    if (!fields[key]) throw new Error(`missing ${key}`);
  }
  return { ...fields, content: match[2] };
}

export const ProsePlugin = async () => ({
  config: async (config) => {
    // V2 uses a different config shape and is registered by setup below.
    if (Array.isArray(config.skills)) return;
    config.skills ??= {};
    config.skills.paths ??= [];
    if (!config.skills.paths.includes(skillsDirectory)) config.skills.paths.push(skillsDirectory);
  },
});

async function setup(ctx) {
  // V1 can also call default.setup with a context lacking V2 skill transforms.
  if (typeof ctx?.skill?.transform !== 'function') return;
  const skills = [];
  try {
    for (const entry of fs.readdirSync(skillsDirectory, { withFileTypes: true })) {
      if (!entry.isDirectory() || entry.name.startsWith('.')) continue;
      const skillPath = path.join(skillsDirectory, entry.name, 'SKILL.md');
      try {
        const { name, description, content } = metadata(fs.readFileSync(skillPath, 'utf8'));
        if (name !== entry.name) throw new Error('name must match skill directory');
        skills.push({ id: name, name, description, path: skillPath, content });
      } catch (error) {
        console.error(`[prose] Cannot register ${skillPath}; repair or reinstall cc-prose:`, error);
      }
    }
    await ctx.skill.transform((draft) => {
      for (const skill of skills) {
        try {
          draft.add(skill);
        } catch (error) {
          // A host can invoke this callback later; contain each rejection here.
          console.error(`[prose] Skill ${skill.id} rejected by OpenCode; check host version and reinstall:`, error);
        }
      }
    });
  } catch (error) {
    console.error('[prose] Skill registration failed; check installation and OpenCode version:', error);
  }
}

export default { id: 'prose', server: ProsePlugin, setup };
