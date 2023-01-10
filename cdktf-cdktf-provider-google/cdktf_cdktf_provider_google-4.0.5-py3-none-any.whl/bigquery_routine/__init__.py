'''
# `google_bigquery_routine`

Refer to the Terraform Registory for docs: [`google_bigquery_routine`](https://www.terraform.io/docs/providers/google/r/bigquery_routine).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class BigqueryRoutine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutine",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine google_bigquery_routine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        definition_body: builtins.str,
        routine_id: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryRoutineArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        determinism_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        return_table_type: typing.Optional[builtins.str] = None,
        return_type: typing.Optional[builtins.str] = None,
        routine_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryRoutineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine google_bigquery_routine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: The ID of the dataset containing this routine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#dataset_id BigqueryRoutine#dataset_id}
        :param definition_body: The body of the routine. For functions, this is the expression in the AS clause. If language=SQL, it is the substring inside (but excluding) the parentheses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#definition_body BigqueryRoutine#definition_body}
        :param routine_id: The ID of the the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#routine_id BigqueryRoutine#routine_id}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#arguments BigqueryRoutine#arguments}
        :param description: The description of the routine if defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#description BigqueryRoutine#description}
        :param determinism_level: The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#determinism_level BigqueryRoutine#determinism_level}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#id BigqueryRoutine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imported_libraries: Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#imported_libraries BigqueryRoutine#imported_libraries}
        :param language: The language of the routine. Possible values: ["SQL", "JAVASCRIPT"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#language BigqueryRoutine#language}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#project BigqueryRoutine#project}.
        :param return_table_type: Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION". If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specificed in return table type, at query time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#return_table_type BigqueryRoutine#return_table_type}
        :param return_type: A JSON schema for the return type. Optional if language = "SQL"; required otherwise. If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switche d the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#return_type BigqueryRoutine#return_type}
        :param routine_type: The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#routine_type BigqueryRoutine#routine_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#timeouts BigqueryRoutine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2907b22fd5759f80f01d9a798bd9243e19ca0351d15c29df9e7188765463bb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryRoutineConfig(
            dataset_id=dataset_id,
            definition_body=definition_body,
            routine_id=routine_id,
            arguments=arguments,
            description=description,
            determinism_level=determinism_level,
            id=id,
            imported_libraries=imported_libraries,
            language=language,
            project=project,
            return_table_type=return_table_type,
            return_type=return_type,
            routine_type=routine_type,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryRoutineArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2f7b7e522041c1c1697cfcfa536631bc1cfa7a3cabacfb64101917df161953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#create BigqueryRoutine#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#delete BigqueryRoutine#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#update BigqueryRoutine#update}.
        '''
        value = BigqueryRoutineTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDeterminismLevel")
    def reset_determinism_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeterminismLevel", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportedLibraries")
    def reset_imported_libraries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportedLibraries", []))

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetReturnTableType")
    def reset_return_table_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnTableType", []))

    @jsii.member(jsii_name="resetReturnType")
    def reset_return_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnType", []))

    @jsii.member(jsii_name="resetRoutineType")
    def reset_routine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutineType", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> "BigqueryRoutineArgumentsList":
        return typing.cast("BigqueryRoutineArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryRoutineTimeoutsOutputReference":
        return typing.cast("BigqueryRoutineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryRoutineArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryRoutineArguments"]]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="definitionBodyInput")
    def definition_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="determinismLevelInput")
    def determinism_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "determinismLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importedLibrariesInput")
    def imported_libraries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "importedLibrariesInput"))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTableTypeInput")
    def return_table_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTableTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTypeInput")
    def return_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="routineIdInput")
    def routine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routineTypeInput")
    def routine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["BigqueryRoutineTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BigqueryRoutineTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cff6501d249d313195601eb0155a486bc666a5130267ed188b34597a9120d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dc1a7651b96c5805768f65a324ea3fe93b73bec617531eb89306824fed756f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1fe9fce40933e824b293541ae4dbf9c7a6ff9b60a5124e9e520b694d75863a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="determinismLevel")
    def determinism_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "determinismLevel"))

    @determinism_level.setter
    def determinism_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c06c0054e7c9287f11395cd43c2831b2490713e5d9218d8673782c56513f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "determinismLevel", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b9ae5cedf8ed9cf1237b3cdafba9e13758ee2969944857ba0b924094b18480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="importedLibraries")
    def imported_libraries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "importedLibraries"))

    @imported_libraries.setter
    def imported_libraries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca70e3ab22159138a552ed5dfab0ad617a9f2c90486d548d639355521234316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importedLibraries", value)

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb466cec21a70820e16993f74aaa4fc83135e8c435d324743de5fd62cec3c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea935470f466b88c554aa3a1c68c913ad61210ae9f767d0983dbe1a9791020d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="returnTableType")
    def return_table_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnTableType"))

    @return_table_type.setter
    def return_table_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f386d1f2a423fa4f83385360c86c5f2f668863c7ef569e4ab10bbf596eb7ce86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnTableType", value)

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19dcd29628a6e63a26bcdf14d68286ed8d81823633606bf61ef5e4d9136ce45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value)

    @builtins.property
    @jsii.member(jsii_name="routineId")
    def routine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineId"))

    @routine_id.setter
    def routine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef251932690f5699123951b0376e05d9a98d1d93e562668d7157209fc0c994eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineId", value)

    @builtins.property
    @jsii.member(jsii_name="routineType")
    def routine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineType"))

    @routine_type.setter
    def routine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa97bed511a2af66722dec9a27b5d425c27c91b732d681081a1f23b34d4f627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineArguments",
    jsii_struct_bases=[],
    name_mapping={
        "argument_kind": "argumentKind",
        "data_type": "dataType",
        "mode": "mode",
        "name": "name",
    },
)
class BigqueryRoutineArguments:
    def __init__(
        self,
        *,
        argument_kind: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param argument_kind: Defaults to FIXED_TYPE. Default value: "FIXED_TYPE" Possible values: ["FIXED_TYPE", "ANY_TYPE"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#argument_kind BigqueryRoutine#argument_kind}
        :param data_type: A JSON schema for the data type. Required unless argumentKind = ANY_TYPE. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switched the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#data_type BigqueryRoutine#data_type}
        :param mode: Specifies whether the argument is input or output. Can be set for procedures only. Possible values: ["IN", "OUT", "INOUT"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#mode BigqueryRoutine#mode}
        :param name: The name of this argument. Can be absent for function return argument. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#name BigqueryRoutine#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4093181fcf2153183e3c0bb280c5a75c627cf219dbf5a94805810747de6b863)
            check_type(argname="argument argument_kind", value=argument_kind, expected_type=type_hints["argument_kind"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if argument_kind is not None:
            self._values["argument_kind"] = argument_kind
        if data_type is not None:
            self._values["data_type"] = data_type
        if mode is not None:
            self._values["mode"] = mode
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def argument_kind(self) -> typing.Optional[builtins.str]:
        '''Defaults to FIXED_TYPE. Default value: "FIXED_TYPE" Possible values: ["FIXED_TYPE", "ANY_TYPE"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#argument_kind BigqueryRoutine#argument_kind}
        '''
        result = self._values.get("argument_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the data type.

        Required unless argumentKind = ANY_TYPE.
        ~>**NOTE**: Because this field expects a JSON string, any changes to the string
        will create a diff, even if the JSON itself hasn't changed. If the API returns
        a different value for the same schema, e.g. it switched the order of values
        or replaced STRUCT field type with RECORD field type, we currently cannot
        suppress the recurring diff this causes. As a workaround, we recommend using
        the schema as returned by the API.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#data_type BigqueryRoutine#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the argument is input or output. Can be set for procedures only. Possible values: ["IN", "OUT", "INOUT"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#mode BigqueryRoutine#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this argument. Can be absent for function return argument.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#name BigqueryRoutine#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryRoutineArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineArgumentsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394f50ac062eae259f62e3cbec03f7fde8dd3d23be78d901e287170529947e1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BigqueryRoutineArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daae335688e57a471d89556aac00b4b5cf4c19a9afe75d383ca3ce12f7a3903f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryRoutineArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b1d97fe5dcaa34a14a26f60c631b2d04d0c78c3fd8c770b7bb32761a9e1c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de12b0d1762dc09778b15d6b66c4c60887babdf9f8ae36eafaeb5e756a973ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2096fea36d81f589dd47424fd3cb36078fbd62420a6383edd8094b201495e335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0643f02e04976e372885b752322a8ae556fb84b0bf559994f30cc27fc0c071a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BigqueryRoutineArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineArgumentsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e17216ae6df5d3ea3c19c330c5e2219ed23f41176b34c2c53a50bcf9de21d90c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArgumentKind")
    def reset_argument_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgumentKind", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="argumentKindInput")
    def argument_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argumentKindInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="argumentKind")
    def argument_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argumentKind"))

    @argument_kind.setter
    def argument_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded13f20c2b223b64d2dfae878c44f9a29e733d93854d49c132d5dccfaea324c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argumentKind", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d006d33913b888ff2345034d41cce0fe63cc1343f413b28c7d63bd33c2e092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a97a429799e3e11213d26274d23df35684697c2081f208e335c294dd593a5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40aba7b888b901d13374dcc479a4fae84b493840563d353e3ad6f5b8c491f64b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BigqueryRoutineArguments, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigqueryRoutineArguments, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigqueryRoutineArguments, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8045903ed5067a0787eeca695263f314090aa68a4c8713116caf2d0b6166418a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset_id": "datasetId",
        "definition_body": "definitionBody",
        "routine_id": "routineId",
        "arguments": "arguments",
        "description": "description",
        "determinism_level": "determinismLevel",
        "id": "id",
        "imported_libraries": "importedLibraries",
        "language": "language",
        "project": "project",
        "return_table_type": "returnTableType",
        "return_type": "returnType",
        "routine_type": "routineType",
        "timeouts": "timeouts",
    },
)
class BigqueryRoutineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        dataset_id: builtins.str,
        definition_body: builtins.str,
        routine_id: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        determinism_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        return_table_type: typing.Optional[builtins.str] = None,
        return_type: typing.Optional[builtins.str] = None,
        routine_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BigqueryRoutineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: The ID of the dataset containing this routine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#dataset_id BigqueryRoutine#dataset_id}
        :param definition_body: The body of the routine. For functions, this is the expression in the AS clause. If language=SQL, it is the substring inside (but excluding) the parentheses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#definition_body BigqueryRoutine#definition_body}
        :param routine_id: The ID of the the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#routine_id BigqueryRoutine#routine_id}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#arguments BigqueryRoutine#arguments}
        :param description: The description of the routine if defined. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#description BigqueryRoutine#description}
        :param determinism_level: The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#determinism_level BigqueryRoutine#determinism_level}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#id BigqueryRoutine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imported_libraries: Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#imported_libraries BigqueryRoutine#imported_libraries}
        :param language: The language of the routine. Possible values: ["SQL", "JAVASCRIPT"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#language BigqueryRoutine#language}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#project BigqueryRoutine#project}.
        :param return_table_type: Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION". If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specificed in return table type, at query time. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#return_table_type BigqueryRoutine#return_table_type}
        :param return_type: A JSON schema for the return type. Optional if language = "SQL"; required otherwise. If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switche d the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#return_type BigqueryRoutine#return_type}
        :param routine_type: The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"]. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#routine_type BigqueryRoutine#routine_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#timeouts BigqueryRoutine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BigqueryRoutineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5867934d3302d0c9e8d42e3e8b8cde5ee6b6c0909bdc5cfb590963f5e45bc1c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument routine_id", value=routine_id, expected_type=type_hints["routine_id"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument determinism_level", value=determinism_level, expected_type=type_hints["determinism_level"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument imported_libraries", value=imported_libraries, expected_type=type_hints["imported_libraries"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument return_table_type", value=return_table_type, expected_type=type_hints["return_table_type"])
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument routine_type", value=routine_type, expected_type=type_hints["routine_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "definition_body": definition_body,
            "routine_id": routine_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if arguments is not None:
            self._values["arguments"] = arguments
        if description is not None:
            self._values["description"] = description
        if determinism_level is not None:
            self._values["determinism_level"] = determinism_level
        if id is not None:
            self._values["id"] = id
        if imported_libraries is not None:
            self._values["imported_libraries"] = imported_libraries
        if language is not None:
            self._values["language"] = language
        if project is not None:
            self._values["project"] = project
        if return_table_type is not None:
            self._values["return_table_type"] = return_table_type
        if return_type is not None:
            self._values["return_type"] = return_type
        if routine_type is not None:
            self._values["routine_type"] = routine_type
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this routine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#dataset_id BigqueryRoutine#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition_body(self) -> builtins.str:
        '''The body of the routine.

        For functions, this is the expression in the AS clause.
        If language=SQL, it is the substring inside (but excluding) the parentheses.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#definition_body BigqueryRoutine#definition_body}
        '''
        result = self._values.get("definition_body")
        assert result is not None, "Required property 'definition_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_id(self) -> builtins.str:
        '''The ID of the the routine.

        The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#routine_id BigqueryRoutine#routine_id}
        '''
        result = self._values.get("routine_id")
        assert result is not None, "Required property 'routine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#arguments BigqueryRoutine#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the routine if defined.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#description BigqueryRoutine#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def determinism_level(self) -> typing.Optional[builtins.str]:
        '''The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#determinism_level BigqueryRoutine#determinism_level}
        '''
        result = self._values.get("determinism_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#id BigqueryRoutine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imported_libraries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#imported_libraries BigqueryRoutine#imported_libraries}
        '''
        result = self._values.get("imported_libraries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''The language of the routine. Possible values: ["SQL", "JAVASCRIPT"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#language BigqueryRoutine#language}
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#project BigqueryRoutine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_table_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION".

        If absent, the return table type is inferred from definitionBody at query time in each query
        that references this routine. If present, then the columns in the evaluated table result will
        be cast to match the column types specificed in return table type, at query time.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#return_table_type BigqueryRoutine#return_table_type}
        '''
        result = self._values.get("return_table_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_type(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the return type.

        Optional if language = "SQL"; required otherwise.
        If absent, the return type is inferred from definitionBody at query time in each query
        that references this routine. If present, then the evaluated result will be cast to
        the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON
        string, any changes to the string will create a diff, even if the JSON itself hasn't
        changed. If the API returns a different value for the same schema, e.g. it switche
        d the order of values or replaced STRUCT field type with RECORD field type, we currently
        cannot suppress the recurring diff this causes. As a workaround, we recommend using
        the schema as returned by the API.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#return_type BigqueryRoutine#return_type}
        '''
        result = self._values.get("return_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routine_type(self) -> typing.Optional[builtins.str]:
        '''The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"].

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#routine_type BigqueryRoutine#routine_type}
        '''
        result = self._values.get("routine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryRoutineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#timeouts BigqueryRoutine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryRoutineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryRoutineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#create BigqueryRoutine#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#delete BigqueryRoutine#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#update BigqueryRoutine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e618f69c17f3c34395c5961a6bb52fe58f02eb8a4f6aa4e15914d9aab1126b36)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#create BigqueryRoutine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#delete BigqueryRoutine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/bigquery_routine#update BigqueryRoutine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryRoutineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f417a409e286a0657c58b14103f0e825579b71849e59e2e9c2561f03b0dae7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49832ac97c7792c9b6e8a089deecb0abc521777bf908f63d8554d8527f5364d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f183c21ee83c902ca1e36da441d035a3f526cb4e637b3e9a1d1990192aa52a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee97ad1a1bdba96b955a3ec3490a29b43651d4a7e08e366dfb221c357700c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BigqueryRoutineTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BigqueryRoutineTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BigqueryRoutineTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fe6991b9e5283efbe33558311dd2aba87f477b3cceef104ec5e7f139e9829e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BigqueryRoutine",
    "BigqueryRoutineArguments",
    "BigqueryRoutineArgumentsList",
    "BigqueryRoutineArgumentsOutputReference",
    "BigqueryRoutineConfig",
    "BigqueryRoutineTimeouts",
    "BigqueryRoutineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d2907b22fd5759f80f01d9a798bd9243e19ca0351d15c29df9e7188765463bb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    definition_body: builtins.str,
    routine_id: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    determinism_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    return_table_type: typing.Optional[builtins.str] = None,
    return_type: typing.Optional[builtins.str] = None,
    routine_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryRoutineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2f7b7e522041c1c1697cfcfa536631bc1cfa7a3cabacfb64101917df161953(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cff6501d249d313195601eb0155a486bc666a5130267ed188b34597a9120d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dc1a7651b96c5805768f65a324ea3fe93b73bec617531eb89306824fed756f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1fe9fce40933e824b293541ae4dbf9c7a6ff9b60a5124e9e520b694d75863a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c06c0054e7c9287f11395cd43c2831b2490713e5d9218d8673782c56513f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b9ae5cedf8ed9cf1237b3cdafba9e13758ee2969944857ba0b924094b18480(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca70e3ab22159138a552ed5dfab0ad617a9f2c90486d548d639355521234316(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb466cec21a70820e16993f74aaa4fc83135e8c435d324743de5fd62cec3c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea935470f466b88c554aa3a1c68c913ad61210ae9f767d0983dbe1a9791020d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f386d1f2a423fa4f83385360c86c5f2f668863c7ef569e4ab10bbf596eb7ce86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19dcd29628a6e63a26bcdf14d68286ed8d81823633606bf61ef5e4d9136ce45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef251932690f5699123951b0376e05d9a98d1d93e562668d7157209fc0c994eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa97bed511a2af66722dec9a27b5d425c27c91b732d681081a1f23b34d4f627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4093181fcf2153183e3c0bb280c5a75c627cf219dbf5a94805810747de6b863(
    *,
    argument_kind: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394f50ac062eae259f62e3cbec03f7fde8dd3d23be78d901e287170529947e1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daae335688e57a471d89556aac00b4b5cf4c19a9afe75d383ca3ce12f7a3903f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b1d97fe5dcaa34a14a26f60c631b2d04d0c78c3fd8c770b7bb32761a9e1c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de12b0d1762dc09778b15d6b66c4c60887babdf9f8ae36eafaeb5e756a973ca7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2096fea36d81f589dd47424fd3cb36078fbd62420a6383edd8094b201495e335(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0643f02e04976e372885b752322a8ae556fb84b0bf559994f30cc27fc0c071a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17216ae6df5d3ea3c19c330c5e2219ed23f41176b34c2c53a50bcf9de21d90c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded13f20c2b223b64d2dfae878c44f9a29e733d93854d49c132d5dccfaea324c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d006d33913b888ff2345034d41cce0fe63cc1343f413b28c7d63bd33c2e092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a97a429799e3e11213d26274d23df35684697c2081f208e335c294dd593a5f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40aba7b888b901d13374dcc479a4fae84b493840563d353e3ad6f5b8c491f64b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8045903ed5067a0787eeca695263f314090aa68a4c8713116caf2d0b6166418a(
    value: typing.Optional[typing.Union[BigqueryRoutineArguments, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5867934d3302d0c9e8d42e3e8b8cde5ee6b6c0909bdc5cfb590963f5e45bc1c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_id: builtins.str,
    definition_body: builtins.str,
    routine_id: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    determinism_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    return_table_type: typing.Optional[builtins.str] = None,
    return_type: typing.Optional[builtins.str] = None,
    routine_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BigqueryRoutineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e618f69c17f3c34395c5961a6bb52fe58f02eb8a4f6aa4e15914d9aab1126b36(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f417a409e286a0657c58b14103f0e825579b71849e59e2e9c2561f03b0dae7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49832ac97c7792c9b6e8a089deecb0abc521777bf908f63d8554d8527f5364d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f183c21ee83c902ca1e36da441d035a3f526cb4e637b3e9a1d1990192aa52a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee97ad1a1bdba96b955a3ec3490a29b43651d4a7e08e366dfb221c357700c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fe6991b9e5283efbe33558311dd2aba87f477b3cceef104ec5e7f139e9829e(
    value: typing.Optional[typing.Union[BigqueryRoutineTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
