from indy import wallet
import time
import pytest


class MyVar:
    wallet_name = ""


@pytest.mark.asyncio
async def setup_function():
    MyVar.wallet_name = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
    print("AAAAAAAAAAA")
    await wallet.create_wallet("pool", MyVar.wallet_name, None, None, None)
    pass


@pytest.mark.asyncio
async def test_sample():
    print("BBBBBBBBBB")
    await wallet.delete_wallet(MyVar.wallet_name, None)


@pytest.mark.asyncio
async def teardown_function(capfd):
    with open("temp.log", "w") as log:
        content = capfd.readouterr()
        log.write(content[0])
        log.write(content[1])
        print(content[1])