import click


from ..click_types import ProviderInfoList, ProviderInfo


@click.argument("client_json", type=click.Path(exists=True, dir_okay=False))
@click.argument("cred_dir", type=click.Path(exists=True, file_okay=False, writable=True))
@click.argument("infos", type=ProviderInfoList())
def credentials(client_json: str, cred_dir: str, infos: list[ProviderInfo]):
    for info in infos:
        ret = input(
            f"We are going to get access token for calendar {info}. (Y/n): ")
        if not (ret == "" or ret == "Y"):
            print("stopping.")
            return
        info.provider.authorize(client_json, cred_dir, info.name)
