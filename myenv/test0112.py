from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.pretty import pprint
from rich.text import Text
import time
import datetime

# ---------------------- 配置信息（可直接修改） ----------------------
COMPANY_NAME = "智元机器人"
DEPARTMENT = "流程IT与质量运营部"
TEST_ENV = "生产预发布环境"  # 测试环境标识
TEST_VERSION = "V1.0.0"      # 测试版本

# 初始化控制台（核心美化工具）
console = Console()

# ---------------------- 待测试的示例函数（适配业务场景） ----------------------
def str_to_semicolon(words: list) -> str:
    """
    将字符串列表用分号分隔拼接（适配智元机器人业务场景）
    :param words: 字符串列表（如人员/流程名称）
    :return: 分号分隔的字符串
    """
    if not isinstance(words, list):
        raise TypeError("输入必须是列表类型")
    return ";".join([str(word).strip() for word in words])

def validate_process_code(code: str) -> bool:
    """
    验证流程编码是否符合智元机器人规范（示例业务函数）
    规范：以AG-开头，后接6位数字
    :param code: 流程编码
    :return: 是否符合规范
    """
    if not isinstance(code, str):
        return False
    return code.startswith("AG-") and len(code) == 8 and code[3:].isdigit()

# ---------------------- 美化的测试执行逻辑 ----------------------
def run_beautiful_tests():
    """执行测试并输出美观的结果（包含智元机器人定制信息）"""
    # 获取精准的测试时间
    test_start_time = datetime.datetime.now()
    test_start_str = test_start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 精确到毫秒

    # 1. 输出定制化标题（彩色+边框+公司信息）
    title_text = Text()
    title_text.append(f"✨ {COMPANY_NAME} 自动化测试套件 ✨\n", style="bold magenta")
    title_text.append(f"部门：{DEPARTMENT} | 测试版本：{TEST_VERSION}", style="bold cyan")
    console.print(title_text)
    console.rule(f"[bold yellow]测试开始时间：{test_start_str}[/bold yellow]")

    # 2. 带进度条的测试执行过程（替换为业务相关用例）
    test_cases = [
        ("流程编码验证-合规AG-123456", lambda: validate_process_code("AG-123456") is True),
        ("流程编码验证-不合规AG-12345", lambda: validate_process_code("AG-12345") is False),
        ("流程编码验证-非AG开头123456", lambda: validate_process_code("123456") is False),
        ("字符串拼接-流程人员列表", lambda: str_to_semicolon(["流程IT组", "质量运营组", "智元机器人核心组"]) == "流程IT组;质量运营组;智元机器人核心组"),
        ("字符串拼接-空列表边界值", lambda: str_to_semicolon([]) == ""),
    ]

    # 初始化进度条
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        expand=False
    ) as progress:
        task = progress.add_task("执行测试用例", total=len(test_cases))

        # 存储测试结果（用于后续表格展示）
        test_results = []
        for case_name, test_func in test_cases:
            progress.update(task, description=f"测试中: {case_name}")
            time.sleep(0.4)  # 模拟测试耗时（增强视觉效果）
            
            # 执行测试并捕获结果
            try:
                result = test_func()
                status = "[bold green]✅ 通过[/bold green]" if result else "[bold red]❌ 失败[/bold red]"
                error_msg = ""
            except Exception as e:
                status = "[bold red]❌ 失败[/bold red]"
                error_msg = f"[red]异常: {type(e).__name__} - {e}[/red]"
            
            test_results.append([case_name, status, error_msg])
            progress.advance(task)

    # 3. 输出测试结果表格（新增公司/部门水印）
    console.rule("[bold cyan]📝 测试结果汇总（智元机器人 流程IT与质量运营部）[/bold cyan]")
    table = Table(show_header=True, header_style="bold blue", title=f"【{COMPANY_NAME}】测试结果表")
    table.add_column("测试用例名称", width=35)
    table.add_column("测试状态", width=12)
    table.add_column("备注/异常信息", width=40)

    for case_name, status, error_msg in test_results:
        table.add_row(case_name, status, error_msg)
    console.print(table)

    # 4. 输出测试总结（包含完整时间信息）
    test_end_time = datetime.datetime.now()
    test_duration = (test_end_time - test_start_time).total_seconds()
    passed = len([r for r in test_results if "✅" in r[1]])
    total = len(test_results)
    
    summary_content = f"""[bold]🏢 公司：{COMPANY_NAME}
📌 部门：{DEPARTMENT}
🗓️  测试日期：{test_start_time.strftime('%Y-%m-%d')}
⏰ 测试开始：{test_start_str}
⏱️  测试结束：{test_end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
⌛ 测试耗时：{test_duration:.3f} 秒
📊 测试统计：总计 {total} 用例 | 通过 {passed} | 失败 {total-passed}
✅ 通过率：{passed/total*100:.1f}%
🌐 测试环境：{TEST_ENV}
🔖 测试版本：{TEST_VERSION}[/bold]"""
    
    summary_panel = Panel(
        summary_content,
        title="[bold yellow]📋 测试总结报告[/bold yellow]",
        border_style="green" if passed == total else "red",
        expand=False
    )
    console.print(summary_panel)

    # 5. 输出环境信息（美化格式）
    console.rule("[bold cyan]🔧 测试环境详情[/bold cyan]")
    env_info = {
        "公司标识": COMPANY_NAME,
        "所属部门": DEPARTMENT,
        "测试环境": TEST_ENV,
        "测试版本": TEST_VERSION,
        "Python版本": f"{sys.version.split()[0]}",
        "执行时间戳": int(test_start_time.timestamp()),
        "核心测试函数": ["validate_process_code", "str_to_semicolon"]
    }
    console.print("[bold]环境信息详情：[/bold]")
    pprint(env_info, expand_all=True, console=console)

# ---------------------- 系统依赖与主函数入口 ----------------------
import sys
if __name__ == "__main__":
    # 安装依赖提示（首次运行时自动安装）
    try:
        import rich
    except ImportError:
        console.print("[bold yellow]⚠️  检测到未安装 rich 库，正在自动安装...[/bold yellow]")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
        from rich.console import Console
        console = Console()

    # 执行定制化美化测试
    run_beautiful_tests()