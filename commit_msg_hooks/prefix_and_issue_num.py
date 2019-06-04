import sys
import io
import pathlib
import re


def main():
    """
    return
    1 ... Failed
    0 ... Succeed
    """
    error_list = []
    # これがないと出力がcp932になって文字化けします
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    branch_valid_format = 'branch_type/#00/hogehoge'
    commit_valid_format = 'prefix/hogehoge'
    branch_type_list = [
        'feature/',
        'fix/',
        'release/',
        'hotfix/',
    ]
    prefix_list = [
        'fix/',
        'update/',
        'add/',
        'remove/',
    ]

    print(pathlib.Path(__file__))
    return 1

    git_dir = pathlib.Path(__file__).parents[1]/'.git'
    commit_msg_file = pathlib.Path(git_dir/'COMMIT_EDITMSG')
    commit_msg = commit_msg_file.read_text(encoding='utf-8')
    head = pathlib.Path(git_dir/'HEAD').read_text(encoding='utf-8')

    # ブランチ名チェック
    # イシュー番号付与チェック
    issue_num = re.search(r'#\d{1,}/', head)
    if issue_num is None:
        error_list.append(0)
    else:
        issue_num, found_pos = issue_num.group()[0:-1], issue_num.span()[0]
        # ブランチタイプチェック
        branch_type = head[head.rfind('/', 0, found_pos-1)+1:found_pos]
        if branch_type not in branch_type_list:
            error_list.append(1)

    # コミットメッセージチェック
    # プレフィックスチェック
    prefix = commit_msg[0:commit_msg.find('/')+1]
    if prefix not in prefix_list:
        error_list.append(2)

    # コミットメッセージ書き換え
    if not error_list:
        rewrite_msg = f'[{prefix[0:-1]}]{issue_num} '
        commit_msg_file.write_text(commit_msg.replace(prefix, rewrite_msg), encoding='utf-8')
    else:
        error_msg = [
            'ブランチ名にイシュー番号が付与されていません。\n'
            f'"{branch_valid_format}"の書式で番号を付与してください。',

            'ブランチ名にタイプが付与されていないか間違っています。\n'
            f'"{branch_valid_format}"の書式でブランチタイプを付与してください。\n'
            '使用できる種類は以下の通りです。\n'
            f'{branch_type_list}',

            'コミットメッセージにプレフィックスが付与されていないか間違っています。\n'
            f'"{commit_valid_format}"の書式でプレフィックスを付与してください。\n'
            '使用できる種類は以下の通りです。\n'
            f'{prefix_list}',
        ]
        for error_num in error_list:
            print(error_msg[error_num])

    return int(bool(error_list))


if __name__ == '__main__':
    sys.exit(main())
