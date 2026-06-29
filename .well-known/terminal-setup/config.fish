# Fish Shell Config
# Location: ~/.config/fish/config.fish

# Environment
set -gx HOMEBREW_NO_AUTO_UPDATE 1
set -gx HOMEBREW_BOTTLE_DOMAIN "https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
set -gx HOMEBREW_API_DOMAIN "https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
fish_add_path /Users/cs/.mimocode/bin

if status is-interactive
    # Starship — Ghostty only
    if test "$TERM_PROGRAM" = "ghostty"
        set -gx STARSHIP_CONFIG ~/.config/starship-nerd.toml
        starship init fish | source
    end

    # zoxide (smart cd)
    zoxide init fish | source

    # fzf (fuzzy finder)
    fzf --fish | source

    # eza / lsd date format (yyyy/mm/dd HH:MM:SS)
    function eza --wraps=eza
        command eza --time-style='+%Y/%m/%d %H:%M:%S' $argv
    end
    function lsd --wraps=lsd
        command lsd --date='+%Y/%m/%d %H:%M:%S' $argv
    end
end
