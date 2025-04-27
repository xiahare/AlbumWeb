# 媒体浏览服务器部署说明

## 依赖环境

- Python 3.x
- pip 安装 flask, pillow:
  ```
  pip install flask pillow
  ```

## 启动命令

```
nohup sudo python3 app.py > output.log 2>&1 &
```

默认监听 80 端口，确保没有其他程序占用。

## 使用说明

- 支持手机浏览
- 媒体目录默认在 `media/` 下，上传内容后自动生成缩略图
- 支持中文目录名、文件名映射配置