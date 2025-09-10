#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Specify CLI - Specify 專案的設定工具

用法：
    uvx specify-cli.py init <專案名稱>
    uvx specify-cli.py init --here

或全域安裝：
    uv tool install --from specify-cli.py specify-cli
    specify init <專案名稱>
    specify init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import json
from pathlib import Path
from typing import Optional

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# 跨平台鍵盤輸入
import readchar

# 常數
AI_CHOICES = {
    "copilot": "GitHub Copilot",
    "claude": "Claude Code",
    "gemini": "Gemini CLI"
}

# ASCII 藝術橫幅
BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "規格驅動開發工具包"
class StepTracker:
    """追蹤並渲染階層式步驟，不使用表情符號，類似 Claude Code 樹狀輸出。
    透過附加的重新整理回呼支援即時自動重新整理。
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # list of dicts: {key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        # 如果不存在，則新增
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[bold cyan]{self.title}[/bold cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            # 圓圈 (樣式不變)
            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # 整行淺灰色 (待處理)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # 標籤為白色，詳細資訊 (如有) 在括號中為淺灰色
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree



MINI_BANNER = """
╔═╗╔═╗╔═╗╔═╗╦╔═╗╦ ╦
╚═╗╠═╝║╣ ║  ║╠╣ ╚╦╝
╚═╝╩  ╚═╝╚═╝╩╚   ╩ 
"""

def get_key():
    """使用 readchar 以跨平台方式取得單一按鍵。"""
    key = readchar.readkey()
    
    # 方向鍵
    if key == readchar.key.UP:
        return 'up'
    if key == readchar.key.DOWN:
        return 'down'
    
    # Enter/Return 鍵
    if key == readchar.key.ENTER:
        return 'enter'
    
    # Escape 鍵
    if key == readchar.key.ESC:
        return 'escape'
        
    # Ctrl+C
    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key



def select_with_arrows(options: dict, prompt_text: str = "選擇一個選項", default_key: str | None = None) -> str:
    """
    使用方向鍵與 Rich Live 顯示進行互動式選擇。
    
    Args:
        options: 以選項鍵為鍵、描述為值的字典
        prompt_text: 在選項上方顯示的文字
        default_key: 預設開始的選項鍵
        
    Returns:
        選擇的選項鍵
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0
    
    selected_key = None

    def create_selection_panel():
        """建立目前選擇項目高亮顯示的選擇面板。"""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="bright_cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")
        
        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[bright_cyan]{key}: {options[key]}[/bright_cyan]")
            else:
                table.add_row(" ", f"[white]{key}: {options[key]}[/white]")
        
        table.add_row("", "")
        table.add_row("", "[dim]使用 ↑/↓ 導航，Enter 選擇，Esc 取消[/dim]")
        
        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )
    
    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]選擇已取消[/yellow]")
                        raise typer.Exit(1)
                    
                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]選擇已取消[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]選擇失敗。[/red]")
        raise typer.Exit(1)

    # 抑制明確的選擇輸出；追蹤器 / 後續邏輯將回報整合狀態
    return selected_key



console = Console()


class BannerGroup(TyperGroup):
    """在說明前顯示橫幅的自訂群組。"""
    
    def format_help(self, ctx, formatter):
        # 在說明前顯示橫幅
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Specify 規格驅動開發專案的設定工具",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """顯示 ASCII 藝術橫幅。"""
    # 使用不同顏色建立漸層效果
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]
    
    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)
    
    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """未提供子指令時顯示橫幅。"""
    # 只有在沒有子指令且沒有說明旗標時顯示橫幅
    # (說明由 BannerGroup 處理)
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]執行 'specify --help' 取得使用資訊[/dim]"))
        console.print()


def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """執行 shell 指令並選擇性擷取輸出。"""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]執行指令時發生錯誤：[/red] {' '.join(cmd)}")
            console.print(f"[red]結束代碼：[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]錯誤輸出：[/red] {e.stderr}")
            raise
        return None


def check_tool(tool: str, install_hint: str) -> bool:
    """檢查工具是否已安裝。"""
    if shutil.which(tool):
        return True
    else:
        console.print(f"[yellow]⚠️  找不到 {tool}[/yellow]")
        console.print(f"   安裝方式：[cyan]{install_hint}[/cyan]")
        return False


def is_git_repo(path: Path | None = None) -> bool:
    """檢查指定路徑是否在 git 儲存庫內。"""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # 使用 git 指令檢查是否在工作樹內
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """在指定路徑初始化 git 儲存庫。
    quiet: 如果為 True 則抑制控制台輸出 (追蹤器處理狀態)
    """
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]正在初始化 git 儲存庫...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "來自 Specify 範本的初始提交"], check=True, capture_output=True)
        if not quiet:
            console.print("[green]✓[/green] Git 儲存庫初始化完成")
        return True
        
    except subprocess.CalledProcessError as e:
        if not quiet:
            console.print(f"[red]初始化 git 儲存庫時發生錯誤：[/red] {e}")
        return False
    finally:
        os.chdir(original_cwd)


def download_template_from_github(ai_assistant: str, download_dir: Path, *, verbose: bool = True, show_progress: bool = True):
    """使用 HTTP 請求從 GitHub 下載最新的範本發布版本。
    回傳 (zip_path, metadata_dict)
    """
    repo_owner = "lazyjerry"
    repo_name = "spec-kit"
    
    if verbose:
        console.print("[cyan]正在取得最新發布版本資訊...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    try:
        response = httpx.get(api_url, timeout=30, follow_redirects=True)
        response.raise_for_status()
        release_data = response.json()
    except httpx.RequestError as e:
        if verbose:
            console.print(f"[red]取得發布版本資訊時發生錯誤：[/red] {e}")
        raise typer.Exit(1)
    
    # 尋找指定 AI 助理的範本資產
    pattern = f"spec-kit-template-{ai_assistant}"
    matching_assets = [
        asset for asset in release_data.get("assets", [])
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]
    
    if not matching_assets:
        if verbose:
            console.print(f"[red]錯誤：[/red] 找不到 AI 助理 '{ai_assistant}' 的範本")
            console.print(f"[yellow]可用資產：[/yellow]")
            for asset in release_data.get("assets", []):
                console.print(f"  - {asset['name']}")
        raise typer.Exit(1)
    
    # 使用第一個匹配的資產
    asset = matching_assets[0]
    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]
    
    if verbose:
        console.print(f"[cyan]找到範本：[/cyan] {filename}")
        console.print(f"[cyan]大小：[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]發布版本：[/cyan] {release_data['tag_name']}")
    
    # 下載檔案
    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]正在下載範本...[/cyan]")
    
    try:
        with httpx.stream("GET", download_url, timeout=30, follow_redirects=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    # 沒有 content-length 標頭，無進度條下載
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        # 顯示進度條
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("正在下載...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        # 靜默下載循環
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    
    except httpx.RequestError as e:
        if verbose:
            console.print(f"[red]下載範本時發生錯誤：[/red] {e}")
        if zip_path.exists():
            zip_path.unlink()
        raise typer.Exit(1)
    if verbose:
        console.print(f"已下載：{filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata


def download_and_extract_template(project_path: Path, ai_assistant: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None) -> Path:
    """下載最新發布版本並解壓縮以建立新專案。
    回傳 project_path。如果提供追蹤器則使用 (鍵值：fetch、download、extract、cleanup)
    """
    current_dir = Path.cwd()
    
    # 步驟：fetch + download 合併
    if tracker:
        tracker.start("fetch", "正在聯繫 GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None)
        )
        if tracker:
            tracker.complete("fetch", f"發布版本 {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "下載範本")
            tracker.complete("download", meta['filename'])  # 已在輔助函數內下載完成
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]下載範本時發生錯誤：[/red] {e}")
        raise
    
    if tracker:
        tracker.add("extract", "解壓縮範本")
        tracker.start("extract")
    elif verbose:
        console.print("正在解壓縮範本...")
    
    try:
        # 只有在不使用目前目錄時才建立專案目錄
        if not is_current_dir:
            project_path.mkdir(parents=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 列出 ZIP 中的所有檔案以供除錯
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} 項目")
            elif verbose:
                console.print(f"[cyan]ZIP 包含 {len(zip_contents)} 項目[/cyan]")
            
            # 對於目前目錄，先解壓縮到暫存位置
            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)
                    
                    # 檢查解壓縮的內容
                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"暫存 {len(extracted_items)} 項目")
                    elif verbose:
                        console.print(f"[cyan]解壓縮 {len(extracted_items)} 項目到暫存位置[/cyan]")
                    
                    # 處理 GitHub 樣式的 ZIP，包含單一根目錄
                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "展平巢狀目錄")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]發現巢狀目錄結構[/cyan]")
                    
                    # 複製內容到目前目錄
                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]合併目錄：[/yellow] {item.name}")
                                # 遞迴複製目錄內容
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]覆寫檔案：[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]範本檔案已合併到目前目錄[/cyan]")
            else:
                # 直接解壓縮到專案目錄 (原始行為)
                zip_ref.extractall(project_path)
                
                # 檢查解壓縮的內容
                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} 頂層項目")
                elif verbose:
                    console.print(f"[cyan]解壓縮 {len(extracted_items)} 項目到 {project_path}：[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'目錄' if item.is_dir() else '檔案'})")
                
                # 處理 GitHub 樣式的 ZIP，包含單一根目錄
                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    # 將內容向上移動一層
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"
                    # 將巢狀目錄內容移動到暫存位置
                    shutil.move(str(nested_dir), str(temp_move_dir))
                    # 移除現在空的專案目錄
                    project_path.rmdir()
                    # 將暫存目錄重新命名為專案目錄
                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "展平巢狀目錄")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]已展平巢狀目錄結構[/cyan]")
                    
    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]解壓縮範本時發生錯誤：[/red] {e}")
        # 如果已建立且非目前目錄，則清理專案目錄
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "移除暫存檔案")
        # 清理下載的 ZIP 檔案
        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"已清理：{zip_path.name}")
    
    return project_path


@app.command()
def init(
    project_name: str = typer.Argument(None, help="新專案目錄的名稱 (使用 --here 時為選用)"),
    ai_assistant: str = typer.Option(None, "--ai", help="要使用的 AI 助理：claude、gemini 或 copilot"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="跳過 AI 代理工具 (如 Claude Code) 的檢查"),
    no_git: bool = typer.Option(False, "--no-git", help="跳過 git 儲存庫初始化"),
    here: bool = typer.Option(False, "--here", help="在目前目錄初始化專案，而非建立新目錄"),
):
    """
    從最新範本初始化新的 Specify 專案。
    
    此指令將會：
    1. 檢查必要工具是否已安裝（git 為選用）
    2. 讓你選擇 AI 助理（Claude Code、Gemini CLI 或 GitHub Copilot）
    3. 從 GitHub 下載適當的範本
    4. 將範本解壓縮到新專案目錄或目前目錄
    5. 初始化新的 git 儲存庫（如果未使用 --no-git 且無現有儲存庫）
    6. 選擇性設定 AI 助理指令
    
    範例：
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai gemini
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init --here --ai claude
        specify init --here
    """
    # 首先顯示橫幅
    show_banner()
    
    # 驗證參數
    if here and project_name:
        console.print("[red]錯誤：[/red] 不能同時指定專案名稱和 --here 旗標")
        raise typer.Exit(1)
    
    if not here and not project_name:
        console.print("[red]錯誤：[/red] 必須指定專案名稱或使用 --here 旗標")
        raise typer.Exit(1)
    
    # 決定專案目錄
    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()
        
        # 檢查目前目錄是否有任何檔案
        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]警告：[/yellow] 目前目錄不是空的（{len(existing_items)} 個項目）")
            console.print("[yellow]範本檔案將與現有內容合併，可能會覆寫現有檔案[/yellow]")
            
            # 詢問確認
            response = typer.confirm("你想要繼續嗎？")
            if not response:
                console.print("[yellow]操作已取消[/yellow]")
                raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        # 檢查專案目錄是否已存在
        if project_path.exists():
            console.print(f"[red]錯誤：[/red] 目錄 '{project_name}' 已存在")
            raise typer.Exit(1)
    
    console.print(Panel.fit(
        "[bold cyan]Specify 專案設定[/bold cyan]\n"
        f"{'在目前目錄初始化：' if here else '建立新專案：'} [green]{project_path.name}[/green]"
        + (f"\n[dim]Path: {project_path}[/dim]" if here else ""),
        border_style="cyan"
    ))
    
    # 只有在可能需要時才檢查 git (非 --no-git)
    git_available = True
    if not no_git:
        git_available = check_tool("git", "https://git-scm.com/downloads")
        if not git_available:
            console.print("[yellow]找不到 Git - 將跳過儲存庫初始化[/yellow]")

    # AI 助理選擇
    if ai_assistant:
        if ai_assistant not in AI_CHOICES:
            console.print(f"[red]錯誤：[/red] 無效的 AI 助理 '{ai_assistant}'。請從以下選擇：{', '.join(AI_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # 使用方向鍵選擇介面
        selected_ai = select_with_arrows(
            AI_CHOICES, 
            "選擇你的 AI 助理：", 
            "copilot"
        )
    
    # 除非忽略，否則檢查代理工具
    if not ignore_agent_tools:
        agent_tool_missing = False
        if selected_ai == "claude":
            if not check_tool("claude", "安裝方式：https://docs.anthropic.com/en/docs/claude-code/setup"):
                console.print("[red]錯誤：[/red] Claude Code 專案需要 Claude CLI")
                agent_tool_missing = True
        elif selected_ai == "gemini":
            if not check_tool("gemini", "安裝方式：https://github.com/google-gemini/gemini-cli"):
                console.print("[red]錯誤：[/red] Gemini 專案需要 Gemini CLI")
                agent_tool_missing = True
        # GitHub Copilot 檢查不需要，因為通常在支援的 IDE 中可用
        
        if agent_tool_missing:
            console.print("\n[red]缺少必要的 AI 工具！[/red]")
            console.print("[yellow]提示：[/yellow] 使用 --ignore-agent-tools 跳過此檢查")
            raise typer.Exit(1)
    
    # 下載並設定專案
    # 新的樹狀進度 (無表情符號)；包含較早的子步驟
    tracker = StepTracker("初始化 Specify 專案")
    # 允許抑制舊版標題的旗標
    # sys._specify_tracker_active = True  # 註解掉，因為這不是標準屬性
    # 在即時渲染前記錄為已完成的預先步驟
    tracker.add("precheck", "檢查必要工具")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "選擇 AI 助理")
    tracker.complete("ai-select", f"{selected_ai}")
    for key, label in [
        ("fetch", "取得最新發布版本"),
        ("download", "下載範本"),
        ("extract", "解壓縮範本"),
        ("zip-list", "檔案內容"),
        ("extracted-summary", "解壓縮摘要"),
        ("cleanup", "清理"),
        ("git", "初始化 git 儲存庫"),
        ("final", "完成")
    ]:
        tracker.add(key, label)

    # 使用 transient 讓即時樹狀圖被最終靜態渲染取代 (避免重複輸出)
    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            download_and_extract_template(project_path, selected_ai, here, verbose=False, tracker=tracker)

            # Git 步驟
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "偵測到現有儲存庫")
                elif git_available:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "已初始化")
                    else:
                        tracker.error("git", "初始化失敗")
                else:
                    tracker.skip("git", "git 不可用")
            else:
                tracker.skip("git", "--no-git 旗標")

            tracker.complete("final", "專案準備就緒")
        except Exception as e:
            tracker.error("final", str(e))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            # 強制最終渲染
            pass

    # 最終靜態樹狀圖 (確保在 Live 上下文結束後可見完成狀態)
    console.print(tracker.render())
    console.print("\n[bold green]專案準備就緒。[/bold green]")
    
    # 框起來的「下一步」區塊
    steps_lines = []
    if not here:
        steps_lines.append(f"1. [bold green]cd {project_name}[/bold green]")
        step_num = 2
    else:
        steps_lines.append("1. 你已經在專案目錄中了！")
        step_num = 2

    if selected_ai == "claude":
        steps_lines.append(f"{step_num}. 在 Visual Studio Code 中開啟並開始使用 Claude Code 的 / 指令")
        steps_lines.append("   - 在任何檔案中輸入 / 查看可用指令")
        steps_lines.append("   - 使用 /specify 建立規格")
        steps_lines.append("   - 使用 /plan 建立實作計畫")
        steps_lines.append("   - 使用 /tasks 產生任務")
    elif selected_ai == "gemini":
        steps_lines.append(f"{step_num}. 使用 Gemini CLI 的 / 指令")
        steps_lines.append("   - 執行 gemini /specify 建立規格")
        steps_lines.append("   - 執行 gemini /plan 建立實作計畫")
        steps_lines.append("   - 查看 GEMINI.md 了解所有可用指令")
    elif selected_ai == "copilot":
        steps_lines.append(f"{step_num}. 在 Visual Studio Code 中開啟並使用 GitHub Copilot 的 [bold cyan]/specify[/]、[bold cyan]/plan[/]、[bold cyan]/tasks[/] 指令")

    step_num += 1
    steps_lines.append(f"{step_num}. 更新 [bold magenta]CONSTITUTION.md[/bold magenta]，加入你專案的不可妥協原則")

    steps_panel = Panel("\n".join(steps_lines), title="下一步", border_style="cyan", padding=(1,2))
    console.print()  # 空行
    console.print(steps_panel)
    
    # 已依使用者要求移除告別訊息


@app.command()
def check():
    """檢查所有必要工具是否已安裝。"""
    show_banner()
    console.print("[bold]正在檢查 Specify 需求...[/bold]\n")
    
    # 嘗試連接 GitHub API 檢查網路連線
    console.print("[cyan]正在檢查網路連線...[/cyan]")
    try:
        response = httpx.get("https://api.github.com", timeout=5, follow_redirects=True)
        console.print("[green]✓[/green] 網路連線可用")
    except httpx.RequestError:
        console.print("[red]✗[/red] 無網路連線 - 下載範本時需要網路")
        console.print("[yellow]請檢查您的網路連線[/yellow]")
    
    console.print("\n[cyan]選用工具：[/cyan]")
    git_ok = check_tool("git", "https://git-scm.com/downloads")
    
    console.print("\n[cyan]選用 AI 工具：[/cyan]")
    claude_ok = check_tool("claude", "安裝方式：https://docs.anthropic.com/en/docs/claude-code/setup")
    gemini_ok = check_tool("gemini", "安裝方式：https://github.com/google-gemini/gemini-cli")
    
    console.print("\n[green]✓ Specify CLI 準備就緒！[/green]")
    if not git_ok:
        console.print("[yellow]建議安裝 git 以進行儲存庫管理[/yellow]")
    if not (claude_ok or gemini_ok):
        console.print("[yellow]建議安裝 AI 助理以獲得最佳體驗[/yellow]")


def main():
    app()


if __name__ == "__main__":
    main()
