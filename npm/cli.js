#!/usr/bin/env node
'use strict';

const { spawnSync, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const VERSION = require('./package.json').version;

const USAGE = `imprint ${VERSION} — AI 原生 · 印刷级中文 PDF 生成器
用法:
  imprint <input.md> [options]      Markdown 进，出版社级 PDF 出
  imprint --new <template>          从模板起稿 (report/book/resume/techdoc/letter)
  imprint --list-themes             查看全部主题
  imprint --theme <name> <input.md> 指定主题渲染
  imprint --report <file.json>      导出 0-100 印刷级质检报告

示例:
  imprint 论文.md
  imprint 论文.md --theme academic --out 论文.pdf
  imprint --new report && imprint report.md

文档: https://github.com/263311487-ux/imprint-pdf
`;

function fail(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function findPython() {
  for (const p of ['python3', 'python']) {
    try {
      execFileSync(p, ['-c', 'import sys; assert sys.version_info >= (3, 10)'], { stdio: 'ignore' });
      return p;
    } catch {
      /* try next */
    }
  }
  return null;
}

function resolveExecutable(name) {
  const dirs = (process.env.PATH || '').split(path.delimiter);
  for (const d of dirs) {
    if (!d) continue;
    const candidate = path.join(d, name);
    try {
      if (fs.statSync(candidate).isFile()) return candidate;
    } catch {
      /* not here */
    }
  }
  return null;
}

function run(cmd, args) {
  const r = spawnSync(cmd, args, { stdio: 'inherit' });
  return r.error ? null : (r.status ?? 0);
}

function moduleInstalled(py) {
  try {
    execFileSync(py, ['-c', 'import imprint'], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function externalImprintExists() {
  const exe = resolveExecutable('imprint');
  if (!exe) return false;
  try {
    return fs.realpathSync(exe) !== fs.realpathSync(__filename);
  } catch {
    return true;
  }
}

function installImprint() {
  const py = findPython();
  if (!py) {
    fail('未找到 Python 3.10+。请先安装: https://www.python.org/downloads/');
  }
  const tryInstall = (args, env, n = 3) => {
    for (let i = 0; i < n; i++) {
      try {
        execFileSync(py, args, { stdio: 'inherit', env: { ...process.env, ...env } });
        return true;
      } catch {
        if (i < n - 1) console.error('  安装失败，重试中...');
      }
    }
    return false;
  };
  // 1) PyPI 官方源
  if (tryInstall(['-m', 'pip', 'install', '--quiet', '--user', 'imprint-pdf'])) return py;
  if (tryInstall(['-m', 'pip', 'install', '--quiet', '--user', '--break-system-packages', 'imprint-pdf'])) return py;
  // 2) 国内镜像（对 CN 用户更稳）
  if (tryInstall(['-m', 'pip', 'install', '--quiet', '--user', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple', 'imprint-pdf'])) return py;
  if (tryInstall(['-m', 'pip', 'install', '--quiet', '--user', '--break-system-packages', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple', 'imprint-pdf'])) return py;
  // 3) GitHub 源兜底（HTTP/1.1 避免 HTTP2 framing 错误）
  const git = 'git+https://github.com/263311487-ux/imprint-pdf.git';
  if (tryInstall(['-m', 'pip', 'install', '--quiet', '--user', git], { GIT_HTTP_VERSION: 'HTTP/1.1' })) return py;
  if (tryInstall(['-m', 'pip', 'install', '--quiet', '--user', '--break-system-packages', git], { GIT_HTTP_VERSION: 'HTTP/1.1' })) return py;
  fail('自动安装失败，请手动执行: python3 -m pip install --user imprint-pdf');
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(USAGE);
    process.exit(1);
  }
  if (args.includes('--help') || args.includes('-h')) {
    console.log(USAGE);
    process.exit(0);
  }
  if (args.includes('--version') || args.includes('-v')) {
    console.log(`imprint ${VERSION}`);
    process.exit(0);
  }

  // 1) 外部已安装的 Python CLI（排除本包装自身）
  if (externalImprintExists()) {
    const code = run('imprint', args);
    if (code !== null) process.exit(code);
  }

  // 2) 当前 Python 环境里已有 imprint 模块
  const py = findPython();
  if (py && moduleInstalled(py)) {
    const code = run(py, ['-m', 'imprint', ...args]);
    process.exit(code ?? 1);
  }

  // 3) 首次运行：自动安装引擎
  console.error('未检测到 imprint 引擎，正在自动安装（仅首次需要）...');
  const installed = installImprint();
  const code = run(installed, ['-m', 'imprint', ...args]);
  process.exit(code ?? 1);
}

main();
