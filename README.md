# 8.1 启动项目
```sh
uvicorn app.main:app --reload
```

# 8.2 测试Agent能力
# 场景1：简单计算
```sh
Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8000/api/v1/agent/invoke" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"query": "计算一下 15 * (23 + 17) 等于多少？"}'
```
# 场景2：复合任务
```sh
Invoke-RestMethod -Method POST `
  -Uri "http://localhost:8000/api/v1/agent/invoke" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"query": "现在几点了？然后告诉我这个时间加上2小时30分钟是什么时间？"}'
```

http://localhost:8000/docs#/