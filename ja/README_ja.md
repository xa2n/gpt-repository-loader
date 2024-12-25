gpt-repository-loader は、Git リポジトリの内容をテキスト形式に変換するコマンドラインツールです。ファイルの構造とファイルの内容を保持したまま変換します。生成された出力は、AI 言語モデルが解釈できるため、コードレビューやドキュメント生成など、さまざまなタスクのためにリポジトリの内容を処理することが可能になります。

**コントリビューティング**

このツールの構築に関する背景情報は、こちらにあります。主に GPT がこのツールの構築を行うという精神のもと、あらゆる問題提起やプルリクエストを歓迎します。GPT-4 に素早くアクセスするために、ChatGPT Plus の使用をお勧めします。

**始め方**

gpt-repository-loader を使い始めるには、次の手順に従ってください。

1. システムに Python 3 がインストールされていることを確認してください。
2. gpt-repository-loader リポジトリをクローンまたはダウンロードしてください。
3. ターミナルでリポジトリのルートディレクトリに移動してください。
4. 次のコマンドで gpt-repository-loader を実行してください。
    
    ```bash
    python gpt_repository_loader.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]
    
    ```
    
    `/path/to/git/repository` を処理したい Git リポジトリのパスに置き換えてください。オプションとして、`-p` でプリアンブルファイルを指定したり、`-o` で出力ファイルを指定したりできます。指定しない場合、デフォルトの出力ファイルは現在のディレクトリに `output.txt` という名前で作成されます。
    

このツールは、リポジトリのテキスト表現を含む `output.txt` ファイルを生成します。このファイルは、AI 言語モデルやその他のテキストベースの処理タスクへの入力として使用できます。

**テストの実行**

gpt-repository-loader のテストを実行するには、次の手順に従ってください。

1. システムに Python 3 がインストールされていることを確認してください。
2. ターミナルでリポジトリのルートディレクトリに移動してください。
3. 次のコマンドでテストを実行してください。
    
    ```bash
    python -m unittest test_gpt_repository_loader.py
    
    ```
    

これで、テストハーネスが gpt-repository-loader プロジェクトに追加されました。ターミナルで `python -m unittest test_gpt_repository_loader.py` コマンドを実行することで、テストを実行できます。
