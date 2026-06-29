# env.fish — add ~/.local/bin to PATH
# Location: ~/.local/bin/env.fish

if not contains "$HOME/.local/bin" $PATH
    # Prepending path in case a system-installed binary needs to be overridden
    set -x PATH "$HOME/.local/bin" $PATH
end
