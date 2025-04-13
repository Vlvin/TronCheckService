from tronpy import Tron

from ._types import AccountData_DTO


client = Tron(network="shasta")


def get_address_energy(client: Tron, address: str) -> int:
    resource: dict[str, any] = client.get_account_resource(address)
    energy_limit: int = resource.get("EnergyLimit", 0)
    energy_used: int = resource.get("EnergyUsed", 0)
    return energy_limit - energy_used


def get_address_data(address: str) -> AccountData_DTO:
    return AccountData_DTO(
        address=address,
        bandwidth=client.get_bandwidth(address),
        energy=get_address_energy(client, address),
        trx=client.get_account_balance(address),
    )


def is_base58_address(address: str) -> bool:
    if len(address) == 0:
        return False
    return address[0] == "T"


def is_hex_address(address: str) -> bool:
    return not is_base58_address(address)
