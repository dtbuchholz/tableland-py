from pytest import raises
from regex import match

from tableland import (
    Database,
    get_registry_address,
    get_table_parts_from_name,
    get_validator_base_uri,
    get_validator_polling_config,
)

# Note: these tests assume you have a fresh instance of Local Tableland running
# in the background: https://docs.tableland.xyz/local-tableland

private_key = "59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"
db = Database(
    private_key=private_key,
    provider_uri="http://localhost:8545",
)
table_name: str

# ____________________________________Successes________________________________________
# _______________________________Create, read, write___________________________________


def test_read() -> None:
    data = db.read("select * from healthbot_31337_1")

    assert data == [{"counter": 1}]


def test_create() -> None:
    global table_name

    prefix = "my_table"
    statement = f"create table {prefix} (id int, val text)"
    data = db.create(statement)

    assert data["owner"] == db.get_signer_address()
    statement_with_chain_id = f"create table {prefix}_31337 (id int, val text)"
    assert data["statement"].lower() == statement_with_chain_id

    table_id = data["table_id"]
    table_name = f"{prefix}_31337_{table_id}"


def test_write() -> None:
    global table_name

    statement = f"insert into {table_name} values (1, 'hello')"
    data = db.write(statement)

    assert data["caller"] == db.get_signer_address()
    assert data["is_owner"] is True
    assert data["statement"] == statement


# ____________________________________Successes________________________________________
# _____________________________________Helpers_________________________________________


def test_get_signer_address() -> None:

    data = db.get_signer_address()

    assert data == "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"


def test_get_chain_id() -> None:

    data = db.get_chain_id()

    assert data == 31337


def test_get_table_info() -> None:

    data = db.get_table_info(1)

    assert data["name"] == "healthbot_31337_1"
    assert data["schema"]["columns"][0] == {"name": "counter", "type": "integer"}


def test_get_owner() -> None:
    owner = db.get_owner(1)

    assert owner == "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"


def test_get_table_parts_from_name() -> None:

    data = get_table_parts_from_name("healthbot_31337_1")

    assert data["prefix"] == "healthbot"
    assert data["chain_id"] == 31337
    assert data["table_id"] == 1


def test_get_registry_address() -> None:
    registry_address = get_registry_address(31337)

    assert registry_address == "0xe7f1725e7734ce288f8367e1bb143e90bb3f0512"


def test_get_validator_base_uri() -> None:
    registry_address = get_validator_base_uri(31337)

    assert registry_address == "http://localhost:8080/api/v1/"


def test_get_validator_polling_config() -> None:
    config = get_validator_polling_config(31337)

    assert config == {"timeout": 5000, "interval": 1_500}


# _____________________________________Failures________________________________________
# _______________________________Create, read, write___________________________________


def test_read_invalid_table() -> None:
    with raises(
        Exception,
        match=r"no such table",
    ):
        db.read("select * from fake_31337_1234567890")


def test_write_invalid_table() -> None:
    statement = "insert into fake_31337_1234567890 values (1, 'hello')"
    with raises(
        Exception,
        match=r"reverted with custom error 'Unauthorized\(\)'",
    ):
        db.write(statement)


def test_write_invalid_name() -> None:
    statement = "insert into my_table values (1, 'hello')"
    with raises(
        Exception,
        match=r"invalid table name format",
    ):
        db.write(statement)


def test_write_invalid_data() -> None:
    global table_name

    statement = f"insert into {table_name} values (1, 'hello', 'erroneous')"
    write_event = db.write(statement)
    tx_hash = write_event["transaction_hash"]
    receipt = db.get_receipt(tx_hash)
    regex = r"db query execution failed"
    assert match(regex, str(receipt["error"])) is not None


# _____________________________________Failures________________________________________
# _____________________________________Helpers_________________________________________


def test_get_owner_invalid_table() -> None:

    with raises(
        Exception,
        match=r"OwnerQueryForNonexistentToken",
    ):
        db.get_owner(1234567890)


def test_get_table_info_invalid() -> None:

    with raises(
        Exception,
        match=r"table not found",
    ):
        db.get_table_info(1234567890)


def test_get_registry_address_invalid() -> None:

    with raises(
        Exception,
        match=r"chain ID not found",
    ):
        get_registry_address(1234567890)


def test_get_validator_base_uri_invalid() -> None:

    with raises(
        Exception,
        match=r"chain ID not found",
    ):
        get_validator_base_uri(1234567890)


def test_get_validator_polling_config_invalid() -> None:

    with raises(
        Exception,
        match=r"chain ID not found",
    ):
        get_validator_polling_config(1234567890)
