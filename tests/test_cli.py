import os

from click.testing import CliRunner
from cli.deposit import main
from cli import deposit


def test_deposit(monkeypatch):
    # monkeypatch get_mnemonic
    def get_mnemonic(language, words_path, entropy=None):
        return "fakephrase"

    monkeypatch.setattr(deposit, "get_mnemonic", get_mnemonic)

    runner = CliRunner()
    inputs = ['1', 'english', 'MyPassword', 'MyPassword', os.getcwd(), 'fakephrase']
    data = '\n'.join(inputs)
    result = runner.invoke(main, input=data)
    assert result.exit_code == 0
