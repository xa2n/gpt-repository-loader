#!/usr/bin/env python3

import fnmatch
import os
import sys

def get_ignore_list(ignore_file_path):
    """
    .gptignore ファイルから無視するファイルのパターンリストを取得する関数。

    Args:
        ignore_file_path: .gptignore ファイルのパス。

    Returns:
        無視するファイルのパターンリスト。
    """
    ignore_list = []
    with open(ignore_file_path, "r") as ignore_file:
        for line in ignore_file:
            # Windows の場合、パスの区切り文字を / から \ に変換する
            if sys.platform == "win32":
                line = line.replace("/", "\\")
            ignore_list.append(line.strip())
    return ignore_list

def should_ignore(file_path, ignore_list):
    """
    指定されたファイルパスが無視リストに含まれているかどうかを判定する関数。

    Args:
        file_path: 判定するファイルパス。
        ignore_list: 無視するファイルのパターンリスト。

    Returns:
        ファイルパスが無視リストに含まれている場合は True、そうでない場合は False。
    """
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def process_repository(repo_path, ignore_list, output_file):
    """
    リポジトリを走査し、無視リストにないファイルのパスと内容を出力ファイルに書き込む関数。

    Args:
        repo_path: リポジトリのパス。
        ignore_list: 無視するファイルのパターンリスト。
        output_file: 出力ファイルオブジェクト。
    """
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            # リポジトリルートからの相対パスを取得
            relative_file_path = os.path.relpath(file_path, repo_path)

            # 無視リストに含まれていない場合のみ処理
            if not should_ignore(relative_file_path, ignore_list):
                with open(file_path, "r", errors="ignore") as file:
                    contents = file.read()
                # ファイルパスと内容の区切りとして ---- を書き込む
                output_file.write("-" * 4 + "\n")
                # ファイルパスを書き込む
                output_file.write(f"{relative_file_path}\n")
                # ファイルの内容を書き込む
                output_file.write(f"{contents}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python git_to_text.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]"
        )
        sys.exit(1)

    # リポジトリのパスを取得
    repo_path = sys.argv[1]
    # .gptignore ファイルのパスを設定
    ignore_file_path = os.path.join(repo_path, ".gptignore")
    # Windows の場合、パスの区切り文字を / から \ に変換する
    if sys.platform == "win32":
        ignore_file_path = ignore_file_path.replace("/", "\\")

    # .gptignore ファイルが存在しない場合、カレントディレクトリの .gptignore を使用する
    if not os.path.exists(ignore_file_path):
        # try and use the .gptignore file in the current directory as a fallback.
        # 現在のディレクトリにある .gptignore ファイルをフォールバックとして使用してみてください。
        HERE = os.path.dirname(os.path.abspath(__file__))
        ignore_file_path = os.path.join(HERE, ".gptignore")

    # プリアンブルファイルのパスを取得
    preamble_file = None
    if "-p" in sys.argv:
        preamble_file = sys.argv[sys.argv.index("-p") + 1]

    # 出力ファイルのパスを取得（デフォルトは output.txt）
    output_file_path = "output.txt"
    if "-o" in sys.argv:
        output_file_path = sys.argv[sys.argv.index("-o") + 1]

    # .gptignore ファイルが存在する場合は、無視リストを取得
    if os.path.exists(ignore_file_path):
        ignore_list = get_ignore_list(ignore_file_path)
    else:
        ignore_list = []

    # 出力ファイルを開く
    with open(output_file_path, "w") as output_file:
        # プリアンブルファイルが存在する場合は、その内容を出力ファイルに書き込む
        if preamble_file:
            with open(preamble_file, "r") as pf:
                preamble_text = pf.read()
                output_file.write(f"{preamble_text}\n")
        # プリアンブルファイルが存在しない場合は、デフォルトのプリアンブルを出力ファイルに書き込む
        else:
            output_file.write(
                "The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context.\n"
            )
        # リポジトリを処理して、ファイルパスと内容を出力ファイルに書き込む
        process_repository(repo_path, ignore_list, output_file)
    # 出力ファイルの末尾に --END-- を書き込む
    with open(output_file_path, "a") as output_file:
        output_file.write("--END--")
    print(f"Repository contents written to {output_file_path}.")
