init:
	git config core.hooksPath .github/hooks
	chmod +x .github/hooks/commit-msg .github/hooks/post-checkout
	@echo "✓ Git hooks configured successfully"
