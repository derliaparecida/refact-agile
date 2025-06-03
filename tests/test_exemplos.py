import pytest
import json
from unittest.mock import patch

from codigo.exemplos import (
    validate_and_return_instance_data,
    InstanceError,
)


@pytest.mark.asyncio
async def test_validate_success():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/birthDate": "16/10/1854",
        "http://personpedia.com/birthPlace": "http://personpedia.com/Dublin",
        "http://personpedia.com/occupation": "writer",
    }
    class_obj = mock_schema(
        {
            "http://personpedia.com/birthDate": "string",
            "http://personpedia.com/birthPlace": "string_uri",
            "http://personpedia.com/occupation": "string",
        },
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    result = await validate_and_return_instance_data(
        "http://personpedia.com/Person/OscarWilde",
        instance_data,
        class_obj,
        "http://personpedia.com/",
        {},
    )
    assert result == instance_data


@pytest.mark.asyncio
async def test_validate_raises_due_to_wrong_boolean():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/isAlive": "0",
    }
    class_obj = mock_schema(
        {
            "http://personpedia.com/isAlive": "boolean",
        },
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    with pytest.raises(InstanceError) as excinfo:
        await validate_and_return_instance_data(
            "http://personpedia.com/Person/OscarWilde",
            instance_data,
            class_obj,
            None,
            None,
        )
    error = json.loads(str(excinfo.value))
    assert "Incorrect value for property" in error[0]


@pytest.mark.asyncio
async def test_validate_multiple_errors():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/isAlive": "http://personpedia.com/TheImportanceOfBeingEarnest",
        "http://personpedia.com/deathAge": "Irish",
        "http://personpedia.com/hasNationality": 46,
        "http://personpedia.com/wroteBook": "true",
    }
    class_obj = mock_schema(
        {
            "http://personpedia.com/isAlive": "boolean",
            "http://personpedia.com/deathAge": "integer",
            "http://personpedia.com/hasNationality": "string",
            "http://personpedia.com/wroteBook": "string_uri",
        },
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    with pytest.raises(InstanceError) as excinfo:
        await validate_and_return_instance_data(
            "http://personpedia.com/Person/OscarWilde",
            instance_data,
            class_obj,
            None,
            None,
        )
    error = json.loads(str(excinfo.value))
    assert len(error) == 4
    assert all("Incorrect value for property" in e for e in error)


@pytest.mark.asyncio
async def test_validate_unique_value_error():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/email": "oscar@wilde.com",
    }
    class_obj = mock_schema(
        {"http://personpedia.com/email": "string"},
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    with patch(
        "codigo.exemplos.property_must_map_a_unique_value", return_value=True
    ), patch("codigo.exemplos.is_value_already_used", return_value=True):
        with pytest.raises(InstanceError) as excinfo:
            await validate_and_return_instance_data(
                "http://personpedia.com/Person/OscarWilde",
                instance_data,
                class_obj,
                None,
                None,
            )
        error = json.loads(str(excinfo.value))
        assert any("must map a unique value" in e for e in error)


@pytest.mark.asyncio
async def test_validate_missing_required_property():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/name": "Oscar Wilde",
    }
    class_obj = mock_schema(
        {
            "http://personpedia.com/name": "string",
            "http://personpedia.com/birthDate": "string",
        },
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    with patch(
        "codigo.exemplos.find_undefined_obligatory_properties",
        return_value=["http://personpedia.com/birthDate"],
    ):
        with pytest.raises(InstanceError) as excinfo:
            await validate_and_return_instance_data(
                "http://personpedia.com/Person/OscarWilde",
                instance_data,
                class_obj,
                None,
                None,
            )
        error = json.loads(str(excinfo.value))
        assert any("is obligatory" in e for e in error)


@pytest.mark.asyncio
async def test_validate_inexistent_property():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/unknown": "foo",
    }
    class_obj = mock_schema(
        {"http://personpedia.com/name": "string"},
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    with patch("codigo.exemplos.get_predicate_datatype", side_effect=KeyError):
        with pytest.raises(InstanceError) as excinfo:
            await validate_and_return_instance_data(
                "http://personpedia.com/Person/OscarWilde",
                instance_data,
                class_obj,
                None,
                None,
            )
        error = json.loads(str(excinfo.value))
        assert any("Inexistent property" in e for e in error)


@pytest.mark.asyncio
async def test_validate_all_types():
    instance_data = {
        "@context": {"personpedia": "http://personpedia.com/"},
        "http://personpedia.com/flag": True,
        "http://personpedia.com/age": 42,
        "http://personpedia.com/name": "Oscar",
        "http://personpedia.com/uri": "http://personpedia.com/uri",
        "http://personpedia.com/array": ["a", "b"],
    }
    class_obj = mock_schema(
        {
            "http://personpedia.com/flag": "boolean",
            "http://personpedia.com/age": "integer",
            "http://personpedia.com/name": "string",
            "http://personpedia.com/uri": "string_uri",
            "http://personpedia.com/array": "array_string_uri",
        },
        id="http://personpedia.com/Person",
        context=instance_data["@context"],
    )
    result = await validate_and_return_instance_data(
        "http://personpedia.com/Person/OscarWilde", instance_data, class_obj, None, None
    )
    assert result == instance_data


def mock_schema(properties, id, context=None):
    return {"id": id, "context": context or {}, "properties": properties}
