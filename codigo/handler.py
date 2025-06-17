# -*- coding: utf-8 -*-
# Stubs for undefined references
class BrainiakRequestHandler:
    pass


DEFAULT_PARAMS = None


class HTTPError:
    pass


INSTANCE_PARAMS = None


class InstanceError:
    pass


class InvalidParam:
    pass


LIST_PARAMS = None


class LazyObject:
    pass


class ParamDict:
    pass


class RequiredParamMissing:
    pass


SHORTEN = None


class SchemaNotFound:
    pass


def _(*args, **kwargs):
    return None


def apply_patch(*args, **kwargs):
    return None


def body_params(*args, **kwargs):
    return None


def build_class_url(*args, **kwargs):
    return None


def build_instance_key(*args, **kwargs):
    return None


def build_schema_url_for_instance(*args, **kwargs):
    return None


def cache(*args, **kwargs):
    return None


def class_name(*args, **kwargs):
    return None


def content_type_profile(*args, **kwargs):
    return None


def context_name(*args, **kwargs):
    return None


def create_instance_elasticsearch(*args, **kwargs):
    return None


def delete_instance_es(*args, **kwargs):
    return None


def dict(*args, **kwargs):
    return None


def edit_instance(*args, **kwargs):
    return None


def ex(*args, **kwargs):
    return None


def get_instance(*args, **kwargs):
    return None


def get_instance_data_from_patch_list(*args, **kwargs):
    return None


def get_instance_from_db(*args, **kwargs):
    return None


def get_instance_from_es(*args, **kwargs):
    return None


def get_json_request_as_dict(*args, **kwargs):
    return None


def get_logger(*args, **kwargs):
    return None


def instance_exists_es(*args, **kwargs):
    return None


def int(*args, **kwargs):
    return None


def is_rdf_type_invalid(*args, **kwargs):
    return None


def isinstance(*args, **kwargs):
    return None


def list(*args, **kwargs):
    return None


def normalize_all_uris_recursively(*args, **kwargs):
    return None


def request_duration(*args, **kwargs):
    return None


def schema_resource(*args, **kwargs):
    return None


def schema_resource_es(*args, **kwargs):
    return None


def self(*args, **kwargs):
    return None


def set(*args, **kwargs):
    return None


def settings(*args, **kwargs):
    return None


def sorted(*args, **kwargs):
    return None


def str(*args, **kwargs):
    return None


# -*- coding: utf-8 -*-
import re
from contextlib import contextmanager
import time


logger = LazyObject(get_logger)


class ListServiceParams(ParamDict):
    """Customize parameters for services with pagination"""

    optionals = LIST_PARAMS


@contextmanager
def safe_params(valid_params=None, body_params=None):
    try:
        yield
    except InvalidParam as ex:
        msg = _(f"Argument {ex} is not supported.")
        if valid_params is not None:
            params_msg = ", ".join(
                sorted(set(list(valid_params.keys()) + list(DEFAULT_PARAMS.keys())))
            )
            msg += _(" The supported querystring arguments are: {0}.").format(
                params_msg
            )
        else:
            params_msg = ", ".join(sorted(DEFAULT_PARAMS.keys()))
            msg += _(" The supported querystring arguments are: {0}.").format(
                params_msg
            )

        if body_params is not None:
            body_msg = ", ".join(body_params)
            msg += _(" The supported body arguments are: {0}.").format(body_msg)
        raise HTTPError(400, log_message=msg)
    except RequiredParamMissing as ex:
        msg = _(f"Required parameter ({ex}) was not given.")
        raise HTTPError(400, log_message=str(msg))


def get_uri_without_id(request_uri):
    if request_uri.endswith("/"):
        request_uri = request_uri[:-1]

    request_uri = request_uri.split("?")[0]
    request_uri_last_arg = request_uri.split("/")[-1]
    uuid_regex = re.compile(
        r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
    )
    request_uri_without_id = request_uri

    if re.match(uuid_regex, request_uri_last_arg):
        request_uri_without_id = "/".join(request_uri.split("/")[:-1])
    elif request_uri_last_arg.isdigit():
        request_uri_without_id = "/".join(request_uri.split("/")[:-1])

    return request_uri_without_id


class InstanceHandlerES(BrainiakRequestHandler):

    SUPPORTED_METHODS = list(BrainiakRequestHandler.SUPPORTED_METHODS) + [
        "PURGE"
    ]  # type: ignore

    async def purge(self, context_name, class_name, instance_id):
        if settings.ENABLE_CACHE:
            optional_params = INSTANCE_PARAMS
            with safe_params(optional_params):
                self.query_params = await ParamDict(
                    self,
                    context_name=context_name,
                    class_name=class_name,
                    instance_id=instance_id,
                    **optional_params,
                )
            path = build_instance_key(self.query_params)
            await cache.purge_by_path(path, False)
        else:
            raise HTTPError(
                405,
                log_message=_(
                    "Cache is disabled (Brainaik's settings.ENABLE_CACHE is set to False)"
                ),
            )

    async def get(self, context_name, class_name, instance_id):
        requests_uri_without_id = self.get_uri_without_id(self.request.uri)
        with request_duration.labels(
            method=self.request.method, endpoint=requests_uri_without_id
        ).time():
            optional_params = INSTANCE_PARAMS
            with safe_params(optional_params):
                self.query_params = await ParamDict(
                    self,
                    context_name=context_name,
                    class_name=class_name,
                    instance_id=instance_id,
                    **optional_params,
                )
            # if context_name == "glb":
            #     self.query_params["class_uri"] = f"http://semantica.exemplo.com/{class_name}"
            #     self.query_params["instance_uri"] = f"http://semantica.exemplo.com/{class_name}/{instance_id}"
            response = await get_instance_from_es(self.query_params)

            if response is None:
                error_message = "Instance ({0}) of class ({1}) in graph ({2}) was not found.".format(
                    self.query_params["instance_uri"],
                    self.query_params["class_uri"],
                    self.query_params["graph_uri"],
                )
                raise HTTPError(404, log_message=error_message)

            response_meta = response["meta"]
            response = response["body"]

            if self.query_params["expand_uri"] == "0":
                response = normalize_all_uris_recursively(response, mode=SHORTEN)

            self.add_cache_headers(response_meta)
            self.finalize(response)

    async def patch(self, context_name, class_name, instance_id):
        requests_uri_without_id = self.get_uri_without_id(self.request.uri)
        with request_duration.labels(
            method=self.request.method, endpoint=requests_uri_without_id
        ).time():
            valid_params = INSTANCE_PARAMS
            with safe_params(valid_params):
                self.query_params = await ParamDict(
                    self,
                    context_name=context_name,
                    class_name=class_name,
                    instance_id=instance_id,
                    **valid_params,
                )
            del context_name
            del class_name
            del instance_id

        patch_list = get_json_request_as_dict(self.request.body)

        # Retrieve original data ES
        self.query_params["expand_object_properties"] = "0"
        instance_data = await get_instance_from_es(self.query_params)

        if instance_data is not None:
            instance_data = instance_data["body"]
            instance_data.pop("http://www.w3.org/1999/02/22-rdf-syntax-ns#type", None)

            changed_data = apply_patch(instance_data, patch_list)
            instance = await edit_instance(self.query_params, changed_data)
            status = 200

            # Clear cache
            await cache.purge_an_instance(self.query_params["instance_uri"])
            await cache.purge_collections(self.query_params["class_uri"])

            if instance and settings.NOTIFY_BS_EVENTS:
                self.query_params["instance_uri"] = instance_data["@id"]
                await self._notify_bs_events(action="PUT", instance_data=instance)

            self.finalize(status)
        else:
            # Creating a new instance from patch list
            instance_data = get_instance_data_from_patch_list(patch_list)
            instance_data = normalize_all_uris_recursively(instance_data)

            rdf_type_error = is_rdf_type_invalid(self.query_params, instance_data)
            if rdf_type_error:
                raise HTTPError(400, log_message=rdf_type_error)

            instance_uri, instance_id = await create_instance_elasticsearch(
                self.query_params, instance_data, self.query_params["instance_uri"]
            )
            resource_url = self.request.full_url()
            status = 201
            self.set_header("location", resource_url)
            self.set_header("X-Brainiak-Resource-URI", instance_uri)

            await cache.purge_an_instance(self.query_params["instance_uri"])
            await cache.purge_collections(self.query_params["class_uri"])

            self.query_params["expand_object_properties"] = "1"
            instance_data2 = await get_instance_from_db(self.query_params)

            if instance_data2 and settings.NOTIFY_BS_EVENTS:
                self.query_params["instance_uri"] = instance_data2["@id"]
                await self._notify_bs_events(action="PUT", instance_data=instance_data2)

            self.finalize(status)

    async def put(self, context_name, class_name, instance_id):
        requests_uri_without_id = self.get_uri_without_id(self.request.uri)
        with request_duration.labels(
            method=self.request.method, endpoint=requests_uri_without_id
        ).time():
            valid_params = INSTANCE_PARAMS
            with safe_params(valid_params):
                self.query_params = await ParamDict(
                    self,
                    context_name=context_name,
                    class_name=class_name,
                    instance_id=instance_id,
                    **valid_params,
                )
            url_call = f"{self.request.uri}"
            del context_name
            del class_name
            del instance_id

            instance_data = get_json_request_as_dict(self.request.body)
            instance_data = normalize_all_uris_recursively(instance_data)
            logger.info(
                "Inicial Edit instance send PUT ES: {0} with data {1}:".format(
                    url_call, instance_data
                )
            )
            rdf_type_error = is_rdf_type_invalid(self.query_params, instance_data)
            if rdf_type_error:
                raise HTTPError(400, log_message=rdf_type_error)

            # Elasticsearch
            try:
                if not await instance_exists_es(self.query_params):
                    try:
                        schema = await schema_resource_es.get_cached_schema(
                            self.query_params
                        )
                    except SchemaNotFound:
                        schema = None
                    if schema is None:
                        msg = _("Class {0} doesn't exist in graph {1}.")
                        raise HTTPError(
                            404,
                            log_message=msg.format(
                                self.query_params["class_uri"],
                                self.query_params["graph_uri"],
                            ),
                        )

                    instance_uri_es, instance_id_es, instance_data_es = (
                        await create_instance_elasticsearch(
                            self.query_params,
                            instance_data,
                            self.query_params["instance_uri"],
                        )
                    )

                    resource_url = self.request.full_url()
                    status = 201
                    self.set_header("location", resource_url)
                    self.set_header("X-Brainiak-Resource-URI", instance_uri_es)

                else:
                    instance_data_es = await edit_instance(
                        self.query_params, instance_data
                    )
                    status = 200

            except InstanceError as ex:
                raise HTTPError(400, log_message=str(ex))
            except SchemaNotFound as ex:
                raise HTTPError(404, log_message=str(ex))

            if instance_data_es and settings.NOTIFY_BS_EVENTS:
                await self._notify_bs_events(
                    action="PUT", instance_data=instance_data_es
                )
            time.sleep(
                1
            )  # Para sincronizar e dar tempo de enviar a notificação para o BSEVENTS, foi necessário colocar esse time.sleep
            await cache.purge_an_instance(self.query_params["instance_uri"])
            await cache.purge_collections(self.query_params["class_uri"])

            self.query_params["expand_object_properties"] = "1"

            self.finalize(status)

    async def delete(self, context_name, class_name, instance_id):
        requests_uri_without_id = self.get_uri_without_id(self.request.uri)
        with request_duration.labels(
            method=self.request.method, endpoint=requests_uri_without_id
        ).time():
            valid_params = INSTANCE_PARAMS
            with safe_params(valid_params):
                self.query_params = await ParamDict(
                    self,
                    context_name=context_name,
                    class_name=class_name,
                    instance_id=instance_id,
                    **valid_params,
                )
            del context_name
            del class_name
            del instance_id

        deleted = await delete_instance_es(self.query_params)
        if deleted:
            response = 204
            if settings.NOTIFY_BS_EVENTS:
                await self._notify_bs_events(action="DELETE")
            time.sleep(
                1
            )  # Para sincronizar e dar tempo de enviar a notificação para o BSEVENTS, foi necessário colocar esse time.sleep
            await cache.purge_an_instance(self.query_params["instance_uri"])
            await cache.purge_collections(self.query_params["class_uri"])
        else:
            msg = _("Instance ({0}) of class ({1}) in graph ({2}) was not found.")
            error_message = msg.format(
                self.query_params["instance_uri"],
                self.query_params["class_uri"],
                self.query_params["graph_uri"],
            )
            raise HTTPError(404, log_message=error_message)
        self.finalize(response)

    def finalize(self, response):
        # FIXME: handle uniformly cache policy
        # Meanwhile we do not have a consitent external cache handling policy
        # this avoids a client (such as chrome browser) caching a resource for ever
        self.set_header("Cache-control", "no-cache")
        self.set_header("max-age", "0")

        if isinstance(response, dict):
            self.write(response)
            class_url = build_class_url(self.query_params)
            schema_url = build_schema_url_for_instance(self.query_params, class_url)
            header_value = content_type_profile(schema_url)
            self.set_header("Content-Type", header_value)
        elif isinstance(response, int):  # status code
            self.set_status(response)
            # A call to finalize() was removed from here! -- rodsenra 2013/04/25
