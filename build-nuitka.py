"""
make executable
"""
import subprocess
import platform
import sys
import os
import shutil

def Make_exe():
    # 絶対パスを使用
    current_dir = os.getcwd()
    resources_dir = os.path.join(current_dir, "icons")

    # # Windows
    # if platform.system() == "Windows":
        # print(f"Didn't work on Windows\nRefer to readme for details\n")
        # sys.exit()

    # Windows
    if platform.system() == "Windows":
        ico_path = os.path.join(resources_dir, "cpg.ico")
        if not os.path.exists(ico_path):
            print(f"Error: {ico_path} not found.")
            return 1

    # Windows用Nuitkaコマンド
    # Windows
    if platform.system() == "Windows":

        ico_path = os.path.join(resources_dir, "cpg.ico")
        if not os.path.exists(ico_path):
            print(f"Error: {ico_path} not found.")
            return 1

        # Windows用Nuitkaコマンド - 文字列として構築
        cmd = (
            f"python.exe -m nuitka "
            f"--onefile "
            f"--show-progress "
            f"--windows-disable-console "
            f"--windows-icon-from-ico=\"{ico_path}\" "
            f"--windows-console-mode=disable "
            f"--include-data-dir=\"{resources_dir}\"=icons "
            f"--include-package=tkinter "  # tkinter
            f"--enable-plugin=tk-inter "   # tk-inter
            f"--output-dir=\"{current_dir}\\dist\" "
            f"--output-filename=cpg-win.exe "  # 出力ファイル名を直接指定
            f"main.py"
        )

        print(f"実行コマンド: {cmd}")

        # コマンド実行 - シェルモードで文字列として渡す
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # コンパイル結果確認
        if result.returncode != 0:
            print("エラー出力:")
            print(result.stderr)
            print(f"コマンド実行に失敗しました。")
            return result.returncode

        # 成功した場合、生成された実行ファイルを探してリネーム
        print("コンパイル成功! 実行ファイルを検索してリネームします...")

        # 可能性のある場所を検索
        potential_exe_locations = [
            os.path.join(current_dir, "dist", "main.exe"),
            os.path.join(current_dir, "main.dist", "main.exe"),
        ]

        found_exe = None
        for exe_path in potential_exe_locations:
            if os.path.exists(exe_path):
                found_exe = exe_path
                print(f"生成された実行ファイルを発見: {found_exe}")
                break

        if not found_exe:
            print("自動検索で実行ファイルが見つかりません。手動で探します...")
            find_cmd = "dir /s /b *.exe"
            find_result = subprocess.run(
                find_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            print("検索結果:")
            print(find_result.stdout)

            # 検索結果から適切な.exeを使用
            if find_result.stdout.strip():
                for line in find_result.stdout.strip().split('\n'):
                    if "main.exe" in line and ("dist" in line or ".dist" in line):
                        found_exe = line.strip()
                        print(f"見つかった実行ファイル: {found_exe}")
                        break

        # 実行ファイルが見つかったら移動とリネーム
        if found_exe:
            target_exe_name = "cpg-win.exe"
            # 直接distディレクトリに保存
            target_exe_path = os.path.join(current_dir, "dist", target_exe_name)

            # 対象ディレクトリがなければ作成
            os.makedirs(os.path.dirname(target_exe_path), exist_ok=True)

            # 既存のターゲットがあれば削除
            if os.path.exists(target_exe_path):
                print(f"既存の {target_exe_path} を削除します")
                os.remove(target_exe_path)

            # コピーして移動
            print(f"実行ファイルを移動: {found_exe} -> {target_exe_path}")
            try:
                shutil.copy2(found_exe, target_exe_path)
                print(f"移動成功! 生成された実行ファイル: {target_exe_path}")
            except Exception as e:
                print(f"移動失敗: {e}")


    # macOS
    elif platform.system() == "Darwin":
        icns_path = os.path.join(resources_dir, "cpg.icns")
        if not os.path.exists(icns_path):
            print(f"Error: {icns_path} not found.")
            return 1

        print(f"アイコンファイルパス: {icns_path}")

        # .appを生成するコマンド
        cmd = (
            f"python3 -m nuitka "
            #f"--onefile "
            f"--standalone "
            f"--macos-create-app-bundle "
            f"--macos-app-name=cpg-mac "
            f"--macos-app-mode=gui "
            f"--macos-app-icon={icns_path} "
            f"--include-data-dir={resources_dir}=icons "
            f"--enable-plugin=tk-inter "
            f"--output-dir={current_dir}/dist "
            f"--lto=yes "
            f"main.py"
        )

        print(f"実行コマンド: {cmd}")

        # コマンド実行
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # コンパイル結果確認
        if result.returncode != 0:
            print("エラー出力:")
            print(result.stderr)
            print(f"コマンド実行に失敗しました。")
            return result.returncode

        # 成功した場合、生成されたアプリを探して正しい名前にリネーム
        print("コンパイル成功! アプリを検索してリネームします...")

        # 可能性のある場所を検索
        potential_app_locations = [
            os.path.join(current_dir, "dist", "main.app"),
            os.path.join(current_dir, "main.dist", "main.app"),
            os.path.join(current_dir, "dist", "cpg-mac.app"),
        ]

        found_app = None
        for app_path in potential_app_locations:
            if os.path.exists(app_path):
                found_app = app_path
                print(f"生成されたアプリを発見: {found_app}")
                break

        if not found_app:
            print("自動検索でアプリが見つかりません。手動で探します...")
            find_result = subprocess.run(
                "find . -name '*.app'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            print("検索結果:")
            print(find_result.stdout)

            # 検索結果から最初の.appを使用
            if find_result.stdout.strip():
                found_app = find_result.stdout.strip().split('\n')[0]
                print(f"見つかったアプリ: {found_app}")

        # アプリが見つかったらリネーム
        if found_app:
            target_app_name = "cpg-mac.app"
            target_app_path = os.path.join(os.path.dirname(found_app), target_app_name)

            # 既存のターゲットがあれば削除
            if os.path.exists(target_app_path):
                print(f"既存の {target_app_path} を削除します")
                subprocess.run(f"rm -rf '{target_app_path}'", shell=True)

            # リネーム
            print(f"アプリをリネーム: {found_app} -> {target_app_path}")
            rename_result = subprocess.run(
                f"mv '{found_app}' '{target_app_path}'",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            if rename_result.returncode == 0:
                print(f"リネーム成功! 生成されたアプリ: {target_app_path}")
            else:
                print("リネーム失敗:")
                print(rename_result.stderr)

        else:
            print("アプリが見つかりませんでした。コンパイルは成功しましたが、.appファイルが生成されなかった可能性があります。")

    return 0

if __name__=="__main__":
    sys.exit(Make_exe())
