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


def _validate_predicate(
    predicate_uri,
    object_value,
    class_object,
    class_id,
    instance_uri,
):
    errors = []
    predicate_has_error = False
    template_msg = _(
        "Incorrect value for property ({1}). A value compatible with a ({2}) was expected, but ({0}) was given."
    )
    try:
        predicate_datatype = get_predicate_datatype(class_object, predicate_uri)
    except KeyError:
        template = _(
            "Inexistent property ({0}) in the schema ({1}), used to create instance ({2})"
        )
        msg = template.format(predicate_uri, class_id, instance_uri)
        errors.append(msg)
        predicate_datatype = None
        predicate_has_error = True
    else:
        if predicate_datatype is None:
            try:
                object_ = sparqlfy_object(object_value)
            except InstanceError:
                msg = template_msg.format(
                    object_value, predicate_uri, "owl:ObjectProperty"
                )
                errors.append(msg)
                predicate_has_error = True
        else:
            if is_instance(object_value, predicate_datatype):
                object_ = sparqlfy(object_value, predicate_datatype)
            else:
                msg = template_msg.format(
                    object_value, predicate_uri, predicate_datatype
                )
                errors.append(msg)
                predicate_has_error = True
    return (
        errors,
        not predicate_has_error,
        predicate_datatype,
        locals().get("object_", None),
    )


def _check_unique_value(
    predicate_uri,
    object_,
    class_object,
    class_id,
    instance_uri,
    graph_uri,
    query_params,
    object_value,
):
    errors = []
    if property_must_map_a_unique_value(class_object, predicate_uri):

        async def check():
            if await is_value_already_used(
                instance_uri,
                object_,
                predicate_uri,
                class_object,
                graph_uri,
                query_params,
            ):
                template = _(
                    "The property ({0}) defined in the schema ({1}) must map a unique value. The value provided ({2}) is already used by another instance."
                )
                msg = template.format(predicate_uri, class_id, object_value)
                errors.append(msg)
            return errors

        return check
    return None


def _process_undefined_obligatory_properties(
    class_object, instance_data, class_id, instance_uri
):
    errors = []
    undefined_obligatory_properties = find_undefined_obligatory_properties(
        class_object, instance_data
    )
    template = _(
        "The property ({0}) is obligatory according to the definition of the class ({1}). A value must be provided for this field in order to create or edit ({2})."
    )
    for property_ in undefined_obligatory_properties:
        msg = template.format(property_, class_id, instance_uri)
        errors.append(msg)
    return errors


async def validate_and_return_instance_data(
    instance_uri, instance_data, class_object, graph_uri, query_params
):
    class_id = class_object["id"]
    copy_instance_data = instance_data.copy()
    predicate_object_tuples = unpack_tuples(copy_instance_data)

    errors = []
    unique_checks = []

    for predicate_uri, object_value in predicate_object_tuples:
        if not is_reserved_attribute(predicate_uri):
            pred_errors, valid, predicate_datatype, object_ = _validate_predicate(
                predicate_uri,
                object_value,
                class_object,
                class_id,
                instance_uri,
                graph_uri,
                query_params,
            )
            errors.extend(pred_errors)
            if valid and predicate_datatype is not None:
                check = _check_unique_value(
                    predicate_uri,
                    object_,
                    class_object,
                    class_id,
                    instance_uri,
                    graph_uri,
                    query_params,
                    object_value,
                )
                if check:
                    unique_checks.append(check)

    # Process unique value checks (async)
    for check in unique_checks:
        errors.extend(await check())

    errors.extend(
        _process_undefined_obligatory_properties(
            class_object, instance_data, class_id, instance_uri
        )
    )

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
