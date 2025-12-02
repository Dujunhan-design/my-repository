# 测试代码：基础输出 + 标识同步来源
def test_github_sync_basic():
    """验证 Cursor 同步到 GitHub 的基础测试函数"""
    print("="*30)
    print("✅ 测试代码运行成功！")
    print(f"📌 仓库地址：https://github.com/Dujunhan-design/my-repository")
    print(f"⏰ 运行时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*30)

# 执行测试
if __name__ == "__main__":
    test_github_sync_basic()