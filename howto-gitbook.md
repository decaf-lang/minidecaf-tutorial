## install gitbook
npm install gitbook-cli -g

## cd this DIR
## install plugins of gitbook
gitbook install

## build book
gitbook build

## get help info
gitbook help

## QA
### `gitbook build`生成的_book下html无法跳转问题

在新版本的gitbook使用gitbook build生成的html在左侧栏是无法跳转菜单的。

#### 解决_book下html无法跳转

在导出的文件夹目录下找到gitbook->theme.js文件.找到下面的代码搜索 if(m)for(n.handler&& 

将if(m)改成if(false) 

再次打开_book下的index.html页面，确认能够跳转页面。
