"""Modeller for dispatching tasks."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Literal,
    Mapping,
    Optional,
    Type,
    Union,
    cast,
)

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from bitfount.config import BITFOUNT_STORAGE_PATH
from bitfount.federated.aggregators.secure import SecureAggregator
from bitfount.federated.authorisation_checkers import (
    _IDENTITY_VERIFICATION_METHODS_MAP,
    IdentityVerificationMethod,
    _SignatureBasedAuthorisation,
    check_identity_verification_method,
)
from bitfount.federated.encryption import _RSAEncryption
from bitfount.federated.exceptions import PodResponseError, RSAKeyError
from bitfount.federated.helper import (
    _check_and_update_pod_ids,
    _create_message_service,
    _get_idp_url,
)
from bitfount.federated.keys_setup import RSAKeyPair, _get_modeller_keys
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.monitoring import task_monitor_context
from bitfount.federated.transport.base_transport import _run_func_and_listen_to_mailbox
from bitfount.federated.transport.identity_verification.oidc import (
    _OIDCAuthFlowChallengeHandler,
    _OIDCDeviceCodeHandler,
)
from bitfount.federated.transport.identity_verification.saml import (
    _SAMLChallengeHandler,
)
from bitfount.federated.transport.identity_verification.types import (
    _HasWebServer,
    _ResponseHandler,
)
from bitfount.federated.transport.message_service import (
    _BitfountMessageType,
    _MessageService,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.types import _TaskRequestMessageGenerator
from bitfount.hub.api import BitfountHub
from bitfount.hub.authentication_flow import _get_auth_environment
from bitfount.hub.exceptions import PodDoesNotExistError
from bitfount.hub.helper import _default_bitfounthub, _get_pod_public_keys

if TYPE_CHECKING:
    from bitfount.federated.protocols.base import BaseProtocolFactory


logger = _get_federated_logger(__name__)


class _Modeller:
    """Dispatches tasks to pods and runs the modeller side of the provided protocol.

    ```python title="Example usage:"
    import bitfount as bf

    modeller=bf.Modeller(
        protocol=bf.FederatedAveraging(...),
    )
    modeller.run(pod_identifiers=["bitfount/example-pod-1", "bitfount/example-pod-2"])
    ```

    Args:
        protocol: The protocol to use for the task.
        message_service: The message service to use for communication with pods.
            Defaults to None, in which case a new message service will be created.
        bitfounthub: Hub instance for Bitfount Hub communication. Defaults to None,
            in which case a new `BitfountHub` instance will be created.
        pod_public_key_paths: Optional. Mapping of pod identifiers to public
            key files for existing pod public keys. Expired or non-existent
            keys will be downloaded from the Hub.
        identity_verification_method: The identity verification method to use.
            Defaults to OIDC_DEVICE_CODE.
        private_key: This modeller's private key either as an `RSAPrivateKey`
            instance or a path to a private key file. If a non-key-based identity
            verification method is used, this is ignored. Defaults to None.
        idp_url: URL of identity provider, used for the SAML Identity
            Verification Method.

    Attributes:
        protocol: The protocol to use for the task.

    Raises:
        ValueError: If key-based identity verification is selected but no
            private key is provided.
    """

    def __init__(
        self,
        protocol: BaseProtocolFactory,
        message_service: Optional[_MessageService] = None,
        bitfounthub: Optional[BitfountHub] = None,
        pod_public_key_paths: Optional[Mapping[str, Path]] = None,
        identity_verification_method: Union[
            str, IdentityVerificationMethod
        ] = IdentityVerificationMethod.DEFAULT,
        private_key: Optional[Union[RSAPrivateKey, Path]] = None,
        idp_url: Optional[str] = None,
    ):
        self.protocol = protocol
        self._hub = _default_bitfounthub(hub=bitfounthub)
        self._message_service = (
            message_service
            if message_service is not None
            else _create_message_service(session=self._hub.session)
        )
        self._pod_public_key_paths: Mapping[str, Path] = pod_public_key_paths or dict()

        self._identity_verification_method: IdentityVerificationMethod = (
            check_identity_verification_method(identity_verification_method)
        )

        self._private_key = _Modeller._process_private_key(
            private_key, self._identity_verification_method, self._hub
        )

        self._idp_url: Optional[str]
        if self._identity_verification_method == IdentityVerificationMethod.SAML:
            # We also need to set the idp_url based on the environment if using SAML
            self._idp_url = idp_url if idp_url is not None else _get_idp_url()
        else:
            self._idp_url = None

    @staticmethod
    def _process_private_key(
        private_key: Optional[Union[RSAPrivateKey, Path]],
        identity_verification_method: IdentityVerificationMethod,
        hub: BitfountHub,
    ) -> Optional[RSAPrivateKey]:
        # NOTE: This method is static to avoid the risk of it being called during
        #       _Modeller initialisation before the identity_verification_method
        #       or hub attributes have been set.
        # Fail out fast if not using key-based authorisation
        if identity_verification_method != IdentityVerificationMethod.KEYS:
            if private_key:
                logger.warning(
                    f"Private key provided but identity verification method "
                    f'"{identity_verification_method.value}" was chosen. '
                    f"Private key will be ignored."
                )
            return None

        username = hub.username

        if isinstance(private_key, Path):
            # Load private key file if needed
            logger.debug(
                f"Loading private key for modeller {username} from {str(private_key)}"
            )
            private_key = _RSAEncryption.load_private_key(private_key)
            public_key = private_key.public_key()
        elif private_key is None:
            # Generate/load stored keys
            logger.info(
                f"No keys provided for modeller {username}; loading/generating keys"
            )
            key_pair = _Modeller._get_modeller_keys(username)
            private_key = key_pair.private
            public_key = key_pair.public
        elif isinstance(private_key, RSAPrivateKey):
            # Just use private key as is
            public_key = private_key.public_key()
        else:
            # Must be invalid type
            raise TypeError(
                f"Error processing private key; expected a Path, RSAPrivateKey"
                f" or None, got {type(private_key)}"
            )

        # Validate against registered public key or register if not already present
        logger.debug(
            f"Checking hub for registered modeller public key for modeller {username}"
        )
        registered_public_key: Optional[RSAPublicKey] = hub.get_user_public_key()
        # Register public key if not already done
        if registered_public_key is None:
            logger.info(f"Registering public key for modeller {username}")
            hub.register_user_public_key(public_key)
        # If key already registered, make sure it matches the one we expect
        elif _RSAEncryption.public_keys_equal(public_key, registered_public_key):
            logger.debug(f"Public key already registered for modeller {username}")
        # Otherwise, handle the case where the registered key and current key don't
        # match
        else:  # keys unequal
            logger.error(
                f"Public key already registered for modeller {username} but does"
                f" not match local public key."
            )
            raise RSAKeyError(
                f"Registered and stored modeller public keys mismatch, please use"
                f" previously created key or delete the key for user {username}"
                f" on Bitfount Hub"
            )

        return private_key

    @staticmethod
    def _get_modeller_key_storage_path(username: str) -> Path:
        """Get the appropriate storage directory for the modeller keys."""
        # NOTE: We explicitly construct the storage path (rather than relying on
        #       the user_storage_path from the hub/session) to guarantee that the
        #       key storage location is explicitly linked to the username and avoids
        #       using `_default`.
        return Path(BITFOUNT_STORAGE_PATH / username / "modeller" / "keys")

    @staticmethod
    def _get_modeller_keys(username: str) -> RSAKeyPair:
        """Load existing modeller keys or generate new ones.

        Args:
            username: The user to generate/load the keys for.

        Returns:
            The loaded/generated keys.
        """
        key_storage_path = _Modeller._get_modeller_key_storage_path(username)
        keys = _get_modeller_keys(key_storage_path)
        return keys

    async def _send_task_requests(
        self,
        pod_identifiers: Iterable[str],
        project_id: Optional[str],
        run_on_new_data_only: bool = False,
    ) -> _ModellerMailbox:
        """Sends task requests to pods.

        Args:
            pod_identifiers: The group of pods to run the task with.
            project_id: Project Id the task belongs to.
            run_on_new_data_only: Whether to run the task on new datapoints only.
                Defaults to False.

        Returns:
            The created ModellerMailbox for the task.
        """
        # Load pod public keys
        loaded_pod_public_keys: Dict[str, RSAPublicKey] = _get_pod_public_keys(
            pod_identifiers=pod_identifiers,
            hub=self._hub,
            pod_public_key_paths=self._pod_public_key_paths,
        )

        task_request_msg_gen = self._get_task_request_msg_gen()
        # Send task requests to chosen pods. We haven't attached a handler for the
        # responses yet but this is handled below. There is no issue due to the
        # fact that the listening task hasn't been started yet, and the inherent
        # handler backoff.
        modeller_mailbox: _ModellerMailbox = await _ModellerMailbox.send_task_requests(
            serialized_protocol=self.protocol.dump(),
            pod_public_keys=loaded_pod_public_keys,
            task_request_msg_gen=task_request_msg_gen,
            message_service=self._message_service,
            project_id=project_id,
            run_on_new_data_only=run_on_new_data_only,
        )

        return modeller_mailbox

    def _get_task_request_msg_gen(self) -> _TaskRequestMessageGenerator:
        """Construct correct TaskRequestMessageGenerator object for the auth type."""
        authorization_checker_cls = _IDENTITY_VERIFICATION_METHODS_MAP[
            self._identity_verification_method
        ]

        if self._identity_verification_method == IdentityVerificationMethod.KEYS:
            authorization_checker_cls = cast(
                Type[_SignatureBasedAuthorisation], authorization_checker_cls
            )
            assert isinstance(self._private_key, RSAPrivateKey)  # nosec[assert_used]
            return authorization_checker_cls.create_task_request_message_generator(
                self._private_key
            )
        else:
            return authorization_checker_cls.create_task_request_message_generator()

    async def _modeller_run(
        self,
        modeller_mailbox: _ModellerMailbox,
        pod_identifiers: Iterable[str],
        require_all_pods: bool = False,
        response_handler: Optional[_ResponseHandler] = None,
    ) -> Union[Literal[False], Optional[Any]]:
        """Waits for pod responses and handles any who don't respond in time.

        Runs the modeller side of the protocol if some pods accepted the task.
        """
        # If additional response handling is specified, we call the handler
        if response_handler:
            await response_handler.handle(modeller_mailbox)

        # Process job accept/reject
        await modeller_mailbox.process_task_request_responses()

        # Fail-fast if no pods accepted the task request.
        if not modeller_mailbox.accepted_worker_mailboxes:
            logger.error(
                "No workers with which to train. "
                "Please ensure you have sent task requests at least some of "
                "which have been accepted."
            )
            return False

        # Otherwise run the protocol
        unaccepted_worker_ids = set(pod_identifiers).difference(
            set(modeller_mailbox.accepted_worker_mailboxes)
        )
        if unaccepted_worker_ids:
            unaccepted_worker_msg = (
                f"Pods {', '.join(unaccepted_worker_ids)} "
                "rejected task request or failed to respond. "
            )
            if require_all_pods:
                raise PodResponseError(
                    unaccepted_worker_msg
                    + "Task requires all pods accept the task request."
                )
            else:
                logger.warning(
                    unaccepted_worker_msg + "Continuing task without these pods ..."
                )

        await modeller_mailbox.send_task_start_message()

        return await self._run_modeller_protocol(modeller_mailbox)

    async def _run_modeller_protocol(
        self,
        modeller_mailbox: _ModellerMailbox,
    ) -> Optional[Any]:
        """Runs the modeller-side of the protocol."""
        protocol = self.protocol.modeller(mailbox=modeller_mailbox)
        # Run the task
        result = await protocol.run()
        return result

    async def run_async(
        self,
        pod_identifiers: Iterable[str],
        require_all_pods: bool,
        project_id: Optional[str] = None,
        run_on_new_data_only: bool = False,
    ) -> Union[Literal[False], Optional[Any]]:
        """Runs the modeller's task with a set of pods.

        Will send a task request before commencing the task itself and only pods that
        accept the task request will be used.

        Args:
            pod_identifiers: The identifiers for the pods to run the task on.
            require_all_pods: Only run task if all pods are online.
            project_id: Project Id the task belongs to. Defaults to None.
            run_on_new_data_only: Whether to run the task on new datapoints only.
                Defaults to False.

        Returns:
            Whatever the protocol's return value is.

        Raises:
            PodResponseError: If require_all_pods is True and at least one
                pod_identifier rejects or fails to respond to the task request.
        """
        try:
            # We do this early to give any handler components time to spin up
            response_handler = self._get_response_handler()

            logger.info("Sending task requests...")
            modeller_mailbox: _ModellerMailbox = await self._send_task_requests(
                pod_identifiers, project_id, run_on_new_data_only
            )

            with task_monitor_context(
                hub=self._hub,
                task_id=modeller_mailbox.task_id,
                sender_id=modeller_mailbox.mailbox_id,
            ):
                run_result: Union[
                    Literal[False], Optional[Any]
                ] = await _run_func_and_listen_to_mailbox(
                    self._modeller_run(
                        modeller_mailbox=modeller_mailbox,
                        pod_identifiers=pod_identifiers,
                        require_all_pods=require_all_pods,
                        response_handler=response_handler,
                    ),
                    modeller_mailbox,
                )
                modeller_mailbox.delete_all_handlers(_BitfountMessageType.LOG_MESSAGE)

                logger.info("Task complete")
                return run_result
        except PodDoesNotExistError as e:
            logger.exception(e)
            logger.error("Aborted task request.")
            return False
        finally:
            # Stop any response handler web servers that may be running still
            try:
                # noinspection PyUnboundLocalVariable
                await cast(_HasWebServer, response_handler).stop_server()
            except NameError:
                logger.warning("Tried to shutdown non-existent response handler")
            except AttributeError:
                # Didn't have a stop_server() method
                pass

    def _get_response_handler(self) -> Optional[_ResponseHandler]:
        """Construct a response handler for additional task messages if required.

        This may spin-up web servers if the response handler requires it. It is
        the responsibility of the handler to shut these down when no longer needed.
        """
        response_handler: Optional[_ResponseHandler] = None

        # SAML
        if self._identity_verification_method == IdentityVerificationMethod.SAML:
            logger.debug("Setting up SAML challenge listener")
            # If SAML is used, the url is set in the modeller init
            self._idp_url = cast(str, self._idp_url)
            response_handler = _SAMLChallengeHandler(self._idp_url)

        # OIDC_ACF_PKCE
        elif (
            self._identity_verification_method
            == IdentityVerificationMethod.OIDC_ACF_PKCE
        ):
            auth_env = _get_auth_environment()
            logger.debug(
                f"Setting up OIDC Authorization Code Flow challenge listener against "
                f"{auth_env.name} authorization environment."
            )
            response_handler = _OIDCAuthFlowChallengeHandler(
                auth_domain=auth_env.auth_domain
            )

        # OIDC_DEVICE_CODE
        elif (
            self._identity_verification_method
            == IdentityVerificationMethod.OIDC_DEVICE_CODE
        ):
            auth_env = _get_auth_environment()
            response_handler = _OIDCDeviceCodeHandler(auth_domain=auth_env.auth_domain)

        # Start web server if needed
        # cast()s are needed to allow mypy to infer this as reachable
        if isinstance(cast(_HasWebServer, response_handler), _HasWebServer):
            # Start response handler web server in background as it takes some time
            cast(_HasWebServer, response_handler).start_server()

        return response_handler

    def _serialize(self, model_out: Union[str, os.PathLike]) -> None:
        """Save any models to file.

        Save any algorithms which have models to the filename specified. If there is
        more than one algorithm with a model, the model name will be be appended with a
        number, starting from 1.

        Args:
            model_out: The path to save the model out to.
        """
        model_algorithms = [i for i in self.protocol.algorithms if hasattr(i, "model")]

        for i, algo in enumerate(model_algorithms, start=1):
            model_out = (
                f"{str(model_out)}_{i}" if len(model_algorithms) > 1 else str(model_out)
            )
            try:
                algo.model.serialize(model_out)  # type: ignore[attr-defined] # Reason: Captured by try clause  # noqa: B950
                logger.info(f'Model saved successfully to "{model_out}"')
            except Exception as e:
                logger.exception(e)

    def run(
        self,
        pod_identifiers: Iterable[str],
        require_all_pods: bool = False,
        model_out: Optional[Union[Path, str]] = None,
        project_id: Optional[str] = None,
        run_on_new_data_only: bool = False,
    ) -> Union[Literal[False], Optional[Any]]:
        """Runs the modeller's task with a set of pods.

        Will send a task request before commencing the task itself and only pods
        that accept the task request will be used.

        Args:
            pod_identifiers: The identifiers for the pods to run the task on.
            require_all_pods: Only run task if all pods are online.
            model_out: If specified, path to save the model out to.
            project_id: Project_id the task belongs to.
            run_on_new_data_only: Whether to run the task on new datapoints only.
                Defaults to False.

        Returns:
            Whatever the protocol's return value is.

        Raises:
            PodResponseError: If require_all_pods is True and at least one
                pod_identifier rejects or fails to respond to the task request.
        """
        pod_identifiers = _check_and_update_pod_ids(pod_identifiers, self._hub)

        # We need to pass the `SecureShare` parameters to the
        # model when SecureAggregation is in use.
        # First we check the protocol's model and aggregators.
        # if steps_between_parameter_updates is 1, then we do
        # the clipping at the 'SecureShare' level.
        if (
            hasattr(self.protocol, "aggregator")
            and isinstance(self.protocol.aggregator, SecureAggregator)  # type: ignore[attr-defined] # Reason: see below # noqa: B950
        ) and (
            hasattr(self.protocol, "steps_between_parameter_updates")
            and self.protocol.steps_between_parameter_updates != 1  # type: ignore[attr-defined] # Reason: see below # noqa: B950
        ):
            if any(hasattr(algo, "model") for algo in self.protocol.algorithms):
                logger.warning(
                    "SecureAggregation in use. We recommend normalization "
                    "of continuous features prior to training."
                )

            # Show warning to user if using custom models that
            # they might have to implement clipping in their custom model.
            if any(
                hasattr(algo, "model")
                and isinstance(algo.model, BitfountModelReference)  # type: ignore[attr-defined] # Reason: see below # noqa: B950
                for algo in self.protocol.algorithms
            ):
                logger.warning(
                    "You are using a custom model with Secure Aggregation."
                    "We recommend clipping the model parameters."
                )

            # Mypy: hasattr check on the protocol aggregator, model and steps.
            # Pass the `SecureShare` parameters to the model for clipping
            for algo in self.protocol.algorithms:
                if hasattr(algo, "model"):
                    algo.model.param_clipping = {  # type: ignore[attr-defined] # Reason: see above # noqa: B950
                        "prime_q": self.protocol.aggregator._secure_share.prime_q,  # type: ignore[attr-defined] # Reason: see above # noqa: B950
                        "precision": self.protocol.aggregator._secure_share.precision,  # type: ignore[attr-defined] # Reason: see above # noqa: B950
                        "num_workers": len(pod_identifiers),
                    }
        result = asyncio.run(
            self.run_async(
                pod_identifiers, require_all_pods, project_id, run_on_new_data_only
            )
        )
        if model_out and result is not False:
            self._serialize(model_out)
        return result
