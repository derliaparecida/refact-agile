# Primeiro exemplo para refatorar
import json


def format_response(instances, search_fields):
    search_fields_dotfy = []
    for i in search_fields:
        search_fields_dotfy.append(
            i.replace(".", "_dot_")
        )  # Observação 5: Pode ser uma list comprehension.
    hits = instances.get("hits", [])
    total = instances["total"][
        "value"
    ]  # Observação 4: Pode causar erro se a chave não existir.
    if not hits:
        return [], total

    bindings = []
    for hit in hits:
        id = hit.get("id")
        title = hit.get(
            "source"
        )  # Observação 4: Pode ser None, mas o código assume que é um dicionário.
        binding_title = {
            "subject": {"type": "str", "value": id.replace("_dot_", ".")},
        }
        for i in title:  # Observação 3: Nome `i` não é descritivo.
            if (
                i == "http://www_dot_w3_dot_org/2000/01/rdf-schema#label"
            ):  # Observação 10: Lógica dependente de strings.
                dict_predicates = {
                    "label": {
                        "type": "literal",
                        "value": title[i],
                    }
                }
                binding_title.update(dict_predicates)
            if (
                type(title[i]) == list
            ):  # Observação 6: Lógica confusa para manipular listas.
                list_dict = []  # Observação 3: Nome `list_dict` não é descritivo.
                for valor_predicado in title[i]:
                    if "a" in valor_predicado:
                        list_dict.append(valor_predicado["a"])
                    else:
                        list_dict.append(valor_predicado)

                if len(list_dict) > 1:
                    title[i] = (
                        list_dict  # Observação 9: Modifica diretamente `title[i]`.
                    )
                else:
                    title[i] = list_dict[0]
            dict_predicates = {
                i.replace("_dot_", "."): {
                    "type": "literal",
                    "value": title[i],
                }
            }
            if i in search_fields_dotfy:
                binding_title.update(dict_predicates)

        bindings.append(binding_title)

    return bindings, total


# ex: 2


class ValidationContext:
    def __init__(self, instance_uri, class_schema, class_id, graph_uri, query_params):
        self.instance_uri = instance_uri
        self.class_schema = class_schema
        self.class_id = class_id
        self.graph_uri = graph_uri
        self.query_params = query_params


def _validate_property(property_uri, property_value, context: ValidationContext):
    errors = []
    property_has_error = False
    try:
        property_datatype = get_predicate_datatype(context.class_schema, property_uri)
    except KeyError:
        msg = f"Inexistent property ({property_uri}) in the schema ({context.class_id}), used to create instance ({context.instance_uri})"
        errors.append(msg)
        property_datatype = None
        property_has_error = True
    else:
        if property_datatype is None:
            try:
                validated_value = sparqlfy_object(property_value)
            except InstanceError:
                msg = f"Incorrect value for property ({property_value}). A value compatible with a (owl:ObjectProperty) was expected, but ({property_value}) was given."
                errors.append(msg)
                property_has_error = True
        else:
            if is_instance(property_value, property_datatype):
                validated_value = sparqlfy(property_value, property_datatype)
            else:
                msg = f"Incorrect value for property ({property_uri}). A value compatible with a ({property_datatype}) was expected, but ({property_value}) was given."
                errors.append(msg)
                property_has_error = True
        if not property_has_error:
            if property_must_map_a_unique_value(context.class_schema, property_uri):
                return errors, validated_value, True
    return errors, locals().get("validated_value", None), False


def _validate_required_properties(context: ValidationContext, instance_data):
    errors = []
    missing_required_properties = find_undefined_obligatory_properties(
        context.class_schema, instance_data
    )
    template = _(
        "The property ({0}) is obligatory according to the definition of the class ({1}). A value must be provided for this field in order to create or edit ({2})."
    )
    for property_ in missing_required_properties:
        msg = template.format(property_, context.class_id, context.instance_uri)
        errors.append(msg)
    return errors


def _validate_all_properties(property_value_tuples, context: ValidationContext):
    errors = []
    unique_value_checks = []
    for property_uri, property_value in property_value_tuples:
        if not is_reserved_attribute(property_uri):
            prop_errors, validated_value, needs_unique = _validate_property(
                property_uri, property_value, context
            )
            errors.extend(prop_errors)
            if needs_unique and validated_value is not None:
                unique_value_checks.append((property_uri, validated_value))
    return errors, unique_value_checks


async def _process_unique_value_checks(unique_value_checks, context: ValidationContext):
    errors = []
    for property_uri, validated_value in unique_value_checks:
        if await is_value_already_used(
            context.instance_uri,
            validated_value,
            property_uri,
            context.class_schema,
            context.graph_uri,
            context.query_params,
        ):
            template = _(
                "The property ({0}) defined in the schema ({1}) must map a unique value. The value provided ({2}) is already used by another instance."
            )
            msg = template.format(property_uri, context.class_id, validated_value)
            errors.append(msg)
    return errors


async def validate_and_return_instance_data(
    instance_uri: str,
    instance_data: dict,
    class_schema: dict,
    graph_uri: str,
    query_params: dict,
) -> dict:
    """
    Valida os dados de um ID conforme o schema da classe e retorna, se os dados são válidos.
    Lança InstanceError com detalhes caso haja erros de validação.
    """
    class_id = class_schema["id"]
    context = ValidationContext(
        instance_uri, class_schema, class_id, graph_uri, query_params
    )
    instance_data_copy = instance_data.copy()
    property_value_tuples = unpack_tuples(instance_data_copy)

    errors, unique_value_checks = _validate_all_properties(
        property_value_tuples, context
    )
    errors += await _process_unique_value_checks(unique_value_checks, context)
    errors.extend(_validate_required_properties(context, instance_data))

    if errors:
        error_msg = json.dumps(errors)
        raise InstanceError(error_msg)
    return instance_data


# funções auxiliares para o exemplo acima
class InstanceError(Exception):
    pass


_ = lambda s: s  # i18n


def unpack_tuples(data):
    return [
        (k, v)
        for k, v in data.items()
        if not k.startswith("@") and not k.startswith("_")
    ]


def is_reserved_attribute(attr):
    return attr.startswith("@") or attr.startswith("_")


def get_predicate_datatype(class_obj, predicate_uri):
    return class_obj["properties"].get(predicate_uri)


def is_instance(value, datatype):
    if datatype == "boolean":
        return value in [True, False]
    if datatype == "integer":
        return isinstance(value, int)
    if datatype == "string":
        return isinstance(value, str)
    if datatype == "string_uri":
        return isinstance(value, str) and value.startswith("http")
    if datatype == "array_string_uri":
        return isinstance(value, list) and all(isinstance(v, str) for v in value)
    return False


def sparqlfy_object(value):
    if isinstance(value, str):
        return value
    raise InstanceError("Valor não pode ser convertido")


def sparqlfy(value, datatype):
    return value


def property_must_map_a_unique_value(class_obj, predicate_uri):
    return False


async def is_value_already_used(*args, **kwargs):
    return False


def find_undefined_obligatory_properties(class_obj, instance_data):
    return []
