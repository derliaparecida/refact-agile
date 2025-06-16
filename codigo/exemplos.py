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
# código original
def validate_instance_properties_type(instance, props_type):
    for k, v in instance.items():
        if k in props_type["properties"]:
            if props_type["properties"][k]["type"] == "array":
                if not isinstance(v, list):
                    instance[k] = [v]
            elif props_type["properties"][k]["type"] == "string":
                if not isinstance(v, str):
                    instance[k] = str(v)
            elif props_type["properties"][k]["type"] == "number":
                if not isinstance(v, int):
                    instance[k] = int(v)
            elif props_type["properties"][k]["type"] == "boolean":
                if not isinstance(v, bool):
                    instance[k] = bool(v)

    return instance


# código refatorado
def validate_instance_properties_type_ref(instance, props_type):
    type_converters = {
        "array": lambda v: v if isinstance(v, list) else [v],
        "string": lambda v: v if isinstance(v, str) else str(v),
        "number": lambda v: v if isinstance(v, int) else int(v),
        "boolean": lambda v: v if isinstance(v, bool) else bool(v),
    }
    for k, v in instance.items():
        if k in props_type["properties"]:
            prop_type = props_type["properties"][k]["type"]
            if prop_type in type_converters:
                instance[k] = type_converters[prop_type](v)
    return instance
