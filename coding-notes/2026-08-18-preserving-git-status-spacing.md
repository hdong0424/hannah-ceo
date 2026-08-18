# 保留 Git Status 中有意义的空格

**Date:** 2026-08-18  
**Topic:** Python, Git, debugging, tests

## 我们想完成什么

Coffee Cadence 的 Python 工具需要读取 `git status --short`，并把 working-tree 状态原样放进 evidence packet。

这个输出必须可信，因为 AI 会根据它判断哪些文件已经 staged、哪些文件只是修改但尚未 staged。

## 出现了什么问题

测试修改了 `README.md`，但没有 stage。Git 的原始输出应该是：

```text
 M README.md
```

测试却发现 evidence packet 中显示：

```text
M README.md
```

第一眼看起来只少了一个空格，但这个空格是 Git 状态格式的一部分。

## 证据如何帮助我们找到原因

`git status --short` 使用前两列表示文件状态：

- 第一列表示 staging area，也就是已经 `git add` 的变化。
- 第二列表示 working tree，也就是尚未 stage 的变化。

因此：

- `M  README.md` 表示修改已经 staged。
- ` M README.md` 表示修改尚未 staged。

Python 函数使用了：

```python
result.stdout.strip()
```

`strip()` 会删除字符串开头和结尾的 whitespace，所以它错误地删除了 Git 输出开头有意义的空格。

## 解决方法

我们把它改为：

```python
result.stdout.rstrip()
```

`rstrip()` 只删除字符串结尾的 whitespace，因此可以去掉 Git 输出最后的换行，同时保留开头的状态列。

修改后，八个 Coffee Cadence 测试全部通过。

## 为什么这个修复是正确的

这个修复没有重新解释或重建 Git 状态，而是尽可能保留 Git 提供的原始证据。Coffee Cadence 可以继续准确区分 staged 和 unstaged changes。

## 下次要记住什么

- Whitespace 不一定只是排版，有时它属于数据格式。
- 在清理 command output 之前，要先理解开头和结尾字符是否有意义。
- 测试不仅检查程序是否运行，也可以发现信息在处理过程中是否被改变。
- 对需要忠实保留格式的输出，`rstrip()` 可能比 `strip()` 更安全，但仍要根据具体数据决定。
