.PHONY: validate install uninstall check-upstream reinstall help

MARKETPLACE := prose-plugin-development
PLUGIN := prose@$(MARKETPLACE)

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

reinstall: uninstall install

check-upstream:
	@bash scripts/check-upstream-changes.sh

help:
	@echo "Available targets:"
	@echo "  validate        - Validate plugin manifests"
	@echo "  install         - Install or update plugin (idempotent)"
	@echo "  uninstall       - Remove plugin and marketplace"
	@echo "  reinstall       - Full reinstall (uninstall + install)"
	@echo "  check-upstream  - Check for upstream humanizer changes (non-destructive)"
	@echo ""
	@echo "To merge upstream changes, use the /update-humanizer Claude Code command."
