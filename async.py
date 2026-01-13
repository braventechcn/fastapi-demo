## 示例对比：同步与异步任务执行

# 同步版本（阻塞）
import time

def sync_task(name, delay):
    print(f"{name}: 开始")
    time.sleep(delay)  # 阻塞操作
    print(f"{name}: 结束")
    return f"{name}完成"

# 执行顺序：一个接一个
print("=====同步任务开始=====")
result1 = sync_task("任务1", 2)
result2 = sync_task("任务2", 1)
print([result1, result2])
print("=====同步任务结束=====")

# 异步版本（非阻塞）
import asyncio

async def async_task(name, delay):
    print(f"{name}: 开始")
    await asyncio.sleep(delay)  # 非阻塞等待
    print(f"{name}: 结束")
    return f"{name}完成"

async def main():
    # 并发执行
    print("=====异步任务开始=====")
    task1 = asyncio.create_task(async_task("任务1", 2))
    task2 = asyncio.create_task(async_task("任务2", 1))
    
    results = await asyncio.gather(task1, task2) # 
    print(results)
    print("=====异步任务结束=====")

# 运行异步函数
asyncio.run(main())