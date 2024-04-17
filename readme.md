# 随机合成数据包

## 默认版本：1.20.2

> **注意：** 为了在其他版本中使用本数据包，您需要修改`pack.mcmeta`文件以及对应版本的配方。

## 使用方法

1. **下载release**：
   下载并解压文件后，运行 `rand_recipes.exe`来打乱战利品表。
2. **安装数据包**：
   将生成的`rand_recipes`文件夹整个拖拽进`./save/你的存档/datapacks/`目录下。
3. **激活数据包**：
   如果随机合成没有生效，请在服务端或是客户端管理员键入`/reload`来重新载入数据包。

## 命令参考

- **启用数据包**：
  ```bash
  /datapack enable "file/rand_loot"
  ```
## Todo List

- [ ] 适配更多Minecraft版本，更新`pack.mcmeta`文件以支持至最新的游戏版本。
- [X] 打包python文件。
