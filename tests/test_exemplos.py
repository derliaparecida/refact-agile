import unittest
from codigo.exemplos import validate_instance_properties_type


class TestValidateInstancePropertiesType(unittest.TestCase):
    def test_validate_instance_properties_type_array(self):
        instance = {"base:desempenhado_por": "semantica/globo.com/Pessoa/id1"}
        props_type = {"properties": {"base:desempenhado_por": {"type": "array"}}}
        expected_result = {"base:desempenhado_por": ["semantica/globo.com/Pessoa/id1"]}
        result = validate_instance_properties_type(instance, props_type)
        self.assertEqual(result, expected_result)

    def test_validate_instance_properties_type_string(self):
        instance = {"rdfs:label": "semantically labeled"}
        props_type = {"properties": {"key1": {"type": "string"}}}
        expected_result = {"rdfs:label": "semantically labeled"}
        result = validate_instance_properties_type(instance, props_type)
        self.assertEqual(result, expected_result)

    def test_validate_instance_properties_type_number(self):
        instance = {"same_prop_num": "123"}
        props_type = {"properties": {"same_prop_num": {"type": "number"}}}
        expected_result = {"same_prop_num": 123}
        result = validate_instance_properties_type(instance, props_type)
        self.assertEqual(result, expected_result)

    def test_validate_instance_properties_type_boolean(self):
        instance = {"églobal": "True"}
        props_type = {"properties": {"églobal": {"type": "boolean"}}}
        expected_result = {"églobal": True}
        result = validate_instance_properties_type(instance, props_type)
        self.assertEqual(result, expected_result)

    def test_validate_instance_properties_type_no_change(self):
        instance = {"samekey": "samevalue"}
        props_type = {"properties": {"samekey": {"type": "string"}}}
        expected_result = {"samekey": "samevalue"}
        result = validate_instance_properties_type(instance, props_type)
        self.assertEqual(result, expected_result)

    def test_validate_instance_properties_with_many_types(self):
        instance = {
            "label": "label value",
            "base:desempenhado_por": "samevalue",
            "key3": "123",
            "églobal": True,
        }
        props_type = {
            "properties": {
                "label": {"type": "string"},
                "base:desempenhado_por": {"type": "array"},
                "key3": {"type": "number"},
                "églobal": {"type": "boolean"},
            }
        }
        expected_result = {
            "label": "label value",
            "base:desempenhado_por": ["samevalue"],
            "key3": 123,
            "églobal": True,
        }
        result = validate_instance_properties_type(instance, props_type)
        self.assertEqual(result, expected_result)
