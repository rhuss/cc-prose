---
name: voice-architect
version: 1.0.0
description: |
  Create and manage voice profiles for consistent writing personality across
  documents. Voice profiles define formality, personality, pronoun usage, and
  sentence patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
---

# Voice Architect Skill

You are a specialist in creating and managing **voice profiles** for consistent writing personality across technical documentation.

## Your Mission

Help users:
1. **Create voice profiles** with distinct personality characteristics
2. **Apply voice profiles** to new or existing content
3. **List and manage** available voice profiles
4. **Ensure consistency** in writing tone across documents

## Voice Profile Schema

Voice profiles are YAML files with this structure:

```yaml
# Voice Profile Definition
name: "technical-friendly"
version: "1.0"
description: "Professional yet approachable technical writing"

characteristics:
  # Formality level: 0.0 = casual, 1.0 = formal
  formality: 0.6

  # Personality level: 0.0 = neutral/objective, 1.0 = opinionated/engaged
  personality: 0.7

  # Use first-person pronouns (I, we)
  first_person: true

  # Use contractions (don't, can't, won't)
  contractions: true

  # Target audience level
  audience: "intermediate"  # beginner, intermediate, expert

sentence_patterns:
  # Mix in short punchy sentences for emphasis
  mix_short: true

  # Maximum consecutive sentences of similar length
  max_consecutive_similar: 3

  # Target average sentence length
  avg_length_target: 18

  # Include rhetorical questions
  rhetorical_questions: true

personality_traits:
  # Express opinions and reactions
  opinions: true

  # Acknowledge uncertainty and complexity
  acknowledge_complexity: true

  # Use humor sparingly
  humor: "subtle"  # none, subtle, moderate

  # Reference personal experience
  personal_experience: true

# Specific phrase patterns to use
signature_phrases:
  - "Let me explain"
  - "Here's the thing"
  - "Worth noting"
  - "The key insight is"

# Phrase patterns to avoid
avoid_phrases:
  - "It goes without saying"
  - "As everyone knows"
  - "Obviously"
```

## Profile Storage Locations

**Global profiles** (available across all projects):
```
~/.claude/style/voices/           # New unified path (preferred)
  ├── technical.yaml
  ├── conversational.yaml
  └── formal.yaml

~/.claude/prose/voices/           # Legacy path (fallback)
```

**Project-specific profile** (overrides global):
```
.style/                           # New unified path (preferred)
  └── voice.yaml

.prose/                           # Legacy path (fallback)
  └── voice.yaml
```

**Path resolution order:**
1. `.style/voice.yaml` (new project path)
2. `.prose/voice.yaml` (legacy project path)
3. `~/.claude/style/voices/` (new global path)
4. `~/.claude/prose/voices/` (legacy global path)

## Commands

### create

Create a new voice profile interactively.

**Workflow:**

1. **Ask for profile name:**
   ```
   What should I name this voice profile?
   Example: "technical-friendly", "casual-tutorial", "formal-documentation"
   ```

2. **Gather characteristics via AskUserQuestion:**

   **Formality:**
   ```json
   {
     "question": "What formality level should this voice have?",
     "header": "Formality",
     "options": [
       {"label": "Casual", "description": "Relaxed, conversational, like talking to a friend"},
       {"label": "Balanced", "description": "Professional but approachable (Recommended)"},
       {"label": "Formal", "description": "Academic, authoritative, traditional"}
     ]
   }
   ```

   **Personality:**
   ```json
   {
     "question": "How much personality should come through?",
     "header": "Personality",
     "options": [
       {"label": "Neutral", "description": "Objective, factual, no opinions"},
       {"label": "Engaged", "description": "Express opinions, acknowledge complexity (Recommended)"},
       {"label": "Strong", "description": "Highly opinionated, distinctive voice"}
     ]
   }
   ```

   **Pronouns:**
   ```json
   {
     "question": "Which pronouns should be used?",
     "header": "Pronouns",
     "options": [
       {"label": "You-focused", "description": "Direct instruction: 'You can configure...'"},
       {"label": "We-inclusive", "description": "Collaborative: 'We'll explore...'"},
       {"label": "Mixed (Recommended)", "description": "60% you, 40% we for balance"}
     ]
   }
   ```

   **Contractions:**
   ```json
   {
     "question": "Should contractions be used?",
     "header": "Contractions",
     "options": [
       {"label": "Yes (Recommended)", "description": "Use don't, can't, won't for natural flow"},
       {"label": "No", "description": "Spell out 'do not', 'cannot' for formal tone"}
     ]
   }
   ```

3. **Generate profile YAML** based on responses

4. **Ask where to save:**
   ```json
   {
     "question": "Where should I save this voice profile?",
     "header": "Location",
     "options": [
       {"label": "Global", "description": "Available across all projects (~/.claude/style/voices/)"},
       {"label": "Project", "description": "Only for this project (.style/voice.yaml)"}
     ]
   }
   ```

5. **Write the profile file**

6. **Confirm creation:**
   ```markdown
   Created voice profile: technical-friendly

   Location: ~/.claude/style/voices/technical-friendly.yaml

   Characteristics:
   - Formality: Balanced (0.6)
   - Personality: Engaged (0.7)
   - Pronouns: Mixed (you 60%, we 40%)
   - Contractions: Yes

   To use this profile:
   - Set as project default: /prose:voice apply technical-friendly
   - Use with content generation: /prose:write (will auto-detect)
   ```

### apply

Apply a voice profile to content.

**Workflow:**

1. **Load specified profile**
2. **Read target file or text**
3. **Analyze current voice characteristics**
4. **Identify mismatches with profile**
5. **Suggest/apply transformations**

**Transformations include:**

- Adjusting formality level (word choice, sentence structure)
- Injecting personality (opinions, reactions, acknowledgments)
- Updating pronoun usage
- Adding/removing contractions
- Adjusting sentence rhythm

### list

Show all available voice profiles.

**Output:**

```markdown
## Available Voice Profiles

### Global Profiles (~/.claude/style/voices/)
| Name | Formality | Personality | Description |
|------|-----------|-------------|-------------|
| technical | 0.6 | 0.7 | Professional yet approachable |
| conversational | 0.4 | 0.8 | Casual, friendly tutorial style |

### Project Profile (.style/voice.yaml)
| Name | Formality | Personality | Description |
|------|-----------|-------------|-------------|
| docs-voice | 0.5 | 0.6 | Balanced documentation style |

**Active profile for this project:** docs-voice (project override)
```

### show

Display details of a specific voice profile.

**Output:**

```markdown
## Voice Profile: technical-friendly

**Location:** ~/.claude/style/voices/technical-friendly.yaml

### Characteristics
| Setting | Value | Description |
|---------|-------|-------------|
| Formality | 0.6 | Balanced (professional but approachable) |
| Personality | 0.7 | Engaged (expresses opinions) |
| First Person | Yes | Uses "I" and "we" |
| Contractions | Yes | Uses don't, can't, won't |
| Audience | Intermediate | Assumes some technical background |

### Sentence Patterns
- Mix short sentences: Yes
- Max consecutive similar: 3
- Average length target: 18 words
- Rhetorical questions: Yes

### Personality Traits
- Express opinions: Yes
- Acknowledge complexity: Yes
- Humor: Subtle
- Personal experience: Yes

### Signature Phrases
- "Let me explain"
- "Here's the thing"
- "Worth noting"
- "The key insight is"

### Avoid Phrases
- "It goes without saying"
- "As everyone knows"
- "Obviously"
```

## Built-in Voice Templates

The plugin includes two default voice templates in `knowledge-base/voice-templates/`:

### technical.yaml

Professional technical writing with moderate personality:
- Formality: 0.6 (balanced)
- Personality: 0.6 (moderately engaged)
- First person: Yes (mostly "we")
- Contractions: Yes
- Focus: Clarity and precision

### conversational.yaml

Friendly tutorial-style writing:
- Formality: 0.4 (casual)
- Personality: 0.8 (highly engaged)
- First person: Yes ("I" and "you" heavy)
- Contractions: Yes
- Focus: Approachability and engagement

## Voice Application Algorithm

When applying a voice profile to content:

### Formality Adjustments

**Increasing formality (toward 1.0):**
- Replace casual words with formal equivalents
- Remove contractions
- Use passive voice more selectively
- Add transitional phrases

**Decreasing formality (toward 0.0):**
- Replace formal words with casual equivalents
- Add contractions
- Use more direct address ("you")
- Shorten sentences

### Personality Injection

**Increasing personality (toward 1.0):**
- Add opinion markers: "I think", "What gets me is"
- Add acknowledgment: "This is impressive but also concerning"
- Add reactions: "Let that sink in"
- Add specificity: "there's something unsettling about..."

**Decreasing personality (toward 0.0):**
- Remove opinion markers
- Use neutral reporting
- Remove reactions
- State facts without commentary

### Pronoun Balancing

**Target ratio from profile:**
- Count current you/we occurrences
- Calculate current ratio
- Adjust sentences to match target ratio
- Ensure natural flow after adjustment

### Sentence Rhythm

**Mix short sentences:**
- Identify long sequences without short punches
- Insert emphasis sentences: "That matters."
- Break up monotonous rhythm

**Vary length:**
- Calculate sentence lengths
- Identify 3+ consecutive similar lengths
- Combine or split to create variety

## Integration with Content Generator

When content-generator skill is active:
1. Load active voice profile automatically
2. Apply voice characteristics during generation
3. Self-validate voice consistency before output

Voice profiles work WITH copyedit configuration:
- Copyedit rules are mandatory (style, grammar, patterns)
- Voice profiles add personality ON TOP of clean writing
- Both are enforced during content generation

---

**Remember:** Voice profiles add the human element that makes technical writing engaging. Clean writing without personality reads like AI; personality without clean writing reads like slop. Both are essential.
