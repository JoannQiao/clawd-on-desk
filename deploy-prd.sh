#!/bin/bash
set -e

REPO_HTTPS="https://github.com/JoannQiao/fonesquare-prd.git"
REPO_SSH="git@github.com:rullerzhou-afk/clawd-on-desk.git"
BRANCH="gh-pages"
PUBLIC_DIR="public"
TMP_DIR="/tmp/prd-deploy-$$"

echo "📦 准备发布文件..."
mkdir -p "$TMP_DIR"
cp -r "$PUBLIC_DIR"/* "$TMP_DIR/"

echo "🔀 切换到 $BRANCH 分支..."
git stash -q --include-untracked 2>/dev/null || true
git checkout -f "$BRANCH"

echo "🧹 清理旧文件..."
find . -maxdepth 1 -not -name '.git' -not -name '.' -exec rm -rf {} +

echo "📄 复制最新文件..."
cp -r "$TMP_DIR"/* .

echo "📝 提交变更..."
git add -A
if git diff --cached --quiet; then
  echo "✅ 没有变更，无需发布"
else
  git commit -m "deploy: update PRD $(date +%Y-%m-%d_%H:%M)"
  echo "🚀 推送到 GitHub Pages..."
  git remote set-url origin "$REPO_HTTPS"
  git push origin "$BRANCH"
  echo "✅ 发布成功！"
  echo "🔗 https://joannqiao.github.io/fonesquare-prd/"
fi

echo "🔙 恢复工作环境..."
git remote set-url origin "$REPO_SSH"
git checkout -f main
git stash pop -q 2>/dev/null || true

rm -rf "$TMP_DIR"
echo "🎉 完成！"
