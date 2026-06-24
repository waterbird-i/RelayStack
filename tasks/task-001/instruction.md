# 修复非标准 Markdown 代码块

真实来源：`comate-stack-fe` commit `f3db1e98df`。

目标：修复 `DevOpsMarkdown.tsx` 里的 `fixCodeBlockMarkers`。

要求：

1. 保留“移除 fenced code block 前置空格”的能力。
2. 支持把下面这种非标准写法改成标准多行代码块：

````text
```console.log(1)
```
````

改写后应等价于：

````text
```
console.log(1)
```
````

完成后运行：

```bash
bash test.sh
```
