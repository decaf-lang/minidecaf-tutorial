## 运行步骤

1. 安装 gitbook：
```bash
npm install gitbook-cli -g
```

如果环境里没有 `npm` 则需要先安装 `npm`

2. 进入本项目根目录

3. 安装 gitbook：

```bash
gitbook install
```

这一步通常会出现类似如下报错：
```bash
Installing GitBook 3.2.3
/usr/local/lib/node_modules/gitbook-cli/node_modules/npm/node_modules/graceful-fs/polyfills.js:287
      if (cb) cb.apply(this, arguments)
                 ^

TypeError: cb.apply is not a function
    at /usr/local/lib/node_modules/gitbook-cli/node_modules/npm/node_modules/graceful-fs/polyfills.js:287:18
    at FSReqCallback.oncomplete (fs.js:169:5)
```

此时进入该代码文件，将62至64行的如下代码删去，然后重新运行 `gitbook install` 即可：
```js
  fs.stat = statFix(fs.stat)
  fs.fstat = statFix(fs.fstat)
  fs.lstat = statFix(fs.lstat)
```

4. 在本地构建文档：

```bash
gitbook build
```

完成后可以在 `_book/index` 访问该文档，**但无法点击文档内项目进行跳转**。

此时可运行如下命令：
```bash
sed -i "s/if(m)for(n/if(false)for(n/g" _book/gitbook/theme.js
```

再次打开文档后就可以跳转了。

## 常见问题

1. Q: `gitbook build`生成的_book下html在左侧栏无法跳转菜单

A:

在导出的文件夹目录下找到gitbook->theme.js文件.找到下面的代码搜索 if(m)for(n.handler&& 

将if(m)改成if(false) 

再次打开_book下的index.html页面，确认能够跳转页面。

### 如果有其他奇奇怪怪的问题

由于 [gitbook-cli](https://github.com/GitbookIO/gitbook) 的开发及维护已经废止，如果有其他奇奇怪怪的问题的话，可以尝试使用修复了 gitbook-cli 的最后版本中的一些 bug 的 [gitbook-ng](https://www.npmjs.com/package/@gitbook-ng/gitbook/v/3.3.6)。
