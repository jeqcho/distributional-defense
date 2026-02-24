#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

submodules=(
    "reference/phantom-transfer-persona-vector:ft"
    "reference/LLS-phantom-transfer:main"
    "reference/LLS-subliminal-learning:main"
    "reference/subliminal-learning-persona-vectors:main"
)

for entry in "${submodules[@]}"; do
    path="${entry%%:*}"
    branch="${entry##*:}"
    echo "========== $path (branch: $branch) =========="

    cd "$REPO_ROOT/$path"

    git fetch origin
    behind=$(git rev-list --count HEAD..origin/"$branch" 2>/dev/null || echo 0)
    ahead=$(git rev-list --count origin/"$branch"..HEAD 2>/dev/null || echo 0)

    if [ "$behind" -eq 0 ] && [ "$ahead" -eq 0 ]; then
        echo "  Already up to date."
        cd "$REPO_ROOT"
        continue
    fi

    echo "  $behind commit(s) behind, $ahead commit(s) ahead of origin/$branch"

    if [ "$behind" -gt 0 ]; then
        echo "  Pulling from origin/$branch..."
        if ! git merge origin/"$branch"; then
            echo ""
            echo "  *** CONFLICT in $path ***"
            echo "  Resolve conflicts in: $REPO_ROOT/$path"
            echo "  Then re-run this script."
            exit 1
        fi
    fi

    if [ "$ahead" -gt 0 ] || [ "$behind" -gt 0 ]; then
        new_ahead=$(git rev-list --count origin/"$branch"..HEAD 2>/dev/null || echo 0)
        if [ "$new_ahead" -gt 0 ]; then
            echo "  Pushing to origin/$branch..."
            git push origin HEAD:"$branch"
        fi
    fi

    echo "  Done."
    cd "$REPO_ROOT"
done

echo ""
echo "========== Staging submodule pointers =========="
cd "$REPO_ROOT"
for entry in "${submodules[@]}"; do
    path="${entry%%:*}"
    git add "$path"
done
echo "All submodule pointers staged."
echo ""
git submodule status
