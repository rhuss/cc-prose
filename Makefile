.PHONY: validate install uninstall sync-humanizer help

MARKETPLACE := prose-plugin-development
PLUGIN := prose@$(MARKETPLACE)
HUMANIZER_SOURCE := ~/.claude/skills/humanizer/SKILL.md

validate:
	claude plugin validate ./
	claude plugin validate ./prose/

install:
	@# Remove existing plugin if installed
	@claude plugin rm $(PLUGIN) 2>/dev/null || true
	@# Remove existing marketplace if installed
	@claude plugin marketplace rm $(MARKETPLACE) 2>/dev/null || true
	@# Add marketplace
	@claude plugin marketplace add ./ && echo "Marketplace added."
	@# Install plugin
	claude plugin install $(PLUGIN)

uninstall:
	@echo "Removing plugin..."
	@claude plugin rm $(PLUGIN) 2>/dev/null || echo "Plugin not installed"
	@echo "Removing marketplace..."
	@claude plugin marketplace rm $(MARKETPLACE) 2>/dev/null || echo "Marketplace not installed"

sync-humanizer:
	@if [ -f "$(HUMANIZER_SOURCE)" ]; then \
		cp "$(HUMANIZER_SOURCE)" prose/skills/humanizer/SKILL.md; \
		echo "Humanizer synced from $(HUMANIZER_SOURCE)"; \
	else \
		echo "Error: Humanizer source not found at $(HUMANIZER_SOURCE)"; \
		exit 1; \
	fi

help:
	@echo "Available targets:"
	@echo "  validate       - Validate plugin manifests"
	@echo "  install        - Install or update plugin (idempotent)"
	@echo "  uninstall      - Remove plugin and marketplace"
	@echo "  sync-humanizer - Sync humanizer skill from ~/.claude/skills/humanizer"
