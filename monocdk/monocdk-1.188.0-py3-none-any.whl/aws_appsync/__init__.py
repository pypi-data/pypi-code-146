'''
# AWS AppSync Construct Library

The `@aws-cdk/aws-appsync` package contains constructs for building flexible
APIs that use GraphQL.

```python
import monocdk as appsync
```

## Example

### DynamoDB

Example of a GraphQL API with `AWS_IAM` [authorization](#authorization) resolving into a DynamoDb
backend data source.

GraphQL schema file `schema.graphql`:

```gql
type demo {
  id: String!
  version: String!
}
type Query {
  getDemos: [ demo! ]
}
input DemoInput {
  version: String!
}
type Mutation {
  addDemo(input: DemoInput!): demo
}
```

CDK stack file `app-stack.ts`:

```python
api = appsync.GraphqlApi(self, "Api",
    name="demo",
    schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
    authorization_config=appsync.aws_appsync.AuthorizationConfig(
        default_authorization=appsync.aws_appsync.AuthorizationMode(
            authorization_type=appsync.AuthorizationType.IAM
        )
    ),
    xray_enabled=True
)

demo_table = dynamodb.Table(self, "DemoTable",
    partition_key=appsync.aws_dynamodb.Attribute(
        name="id",
        type=dynamodb.AttributeType.STRING
    )
)

demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)

# Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
demo_dS.create_resolver(
    type_name="Query",
    field_name="getDemos",
    request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
    response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
)

# Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
demo_dS.create_resolver(
    type_name="Mutation",
    field_name="addDemo",
    request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
        appsync.PrimaryKey.partition("id").auto(),
        appsync.Values.projecting("input")),
    response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
)
```

### Aurora Serverless

AppSync provides a data source for executing SQL commands against Amazon Aurora
Serverless clusters. You can use AppSync resolvers to execute SQL statements
against the Data API with GraphQL queries, mutations, and subscriptions.

```python
# Build a data source for AppSync to access the database.
# api: appsync.GraphqlApi
# Create username and password secret for DB Cluster
secret = rds.DatabaseSecret(self, "AuroraSecret",
    username="clusteradmin"
)

# The VPC to place the cluster in
vpc = ec2.Vpc(self, "AuroraVpc")

# Create the serverless cluster, provide all values needed to customise the database.
cluster = rds.ServerlessCluster(self, "AuroraCluster",
    engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
    vpc=vpc,
    credentials={"username": "clusteradmin"},
    cluster_identifier="db-endpoint-test",
    default_database_name="demos"
)
rds_dS = api.add_rds_data_source("rds", cluster, secret, "demos")

# Set up a resolver for an RDS query.
rds_dS.create_resolver(
    type_name="Query",
    field_name="getDemosRds",
    request_mapping_template=appsync.MappingTemplate.from_string("""
          {
            "version": "2018-05-29",
            "statements": [
              "SELECT * FROM demos"
            ]
          }
          """),
    response_mapping_template=appsync.MappingTemplate.from_string("""
            $utils.toJson($utils.rds.toJsonObject($ctx.result)[0])
          """)
)

# Set up a resolver for an RDS mutation.
rds_dS.create_resolver(
    type_name="Mutation",
    field_name="addDemoRds",
    request_mapping_template=appsync.MappingTemplate.from_string("""
          {
            "version": "2018-05-29",
            "statements": [
              "INSERT INTO demos VALUES (:id, :version)",
              "SELECT * WHERE id = :id"
            ],
            "variableMap": {
              ":id": $util.toJson($util.autoId()),
              ":version": $util.toJson($ctx.args.version)
            }
          }
          """),
    response_mapping_template=appsync.MappingTemplate.from_string("""
            $utils.toJson($utils.rds.toJsonObject($ctx.result)[1][0])
          """)
)
```

### HTTP Endpoints

GraphQL schema file `schema.graphql`:

```gql
type job {
  id: String!
  version: String!
}

input DemoInput {
  version: String!
}

type Mutation {
  callStepFunction(input: DemoInput!): job
}
```

GraphQL request mapping template `request.vtl`:

```json
{
  "version": "2018-05-29",
  "method": "POST",
  "resourcePath": "/",
  "params": {
    "headers": {
      "content-type": "application/x-amz-json-1.0",
      "x-amz-target":"AWSStepFunctions.StartExecution"
    },
    "body": {
      "stateMachineArn": "<your step functions arn>",
      "input": "{ \"id\": \"$context.arguments.id\" }"
    }
  }
}
```

GraphQL response mapping template `response.vtl`:

```json
{
  "id": "${context.result.id}"
}
```

CDK stack file `app-stack.ts`:

```python
api = appsync.GraphqlApi(self, "api",
    name="api",
    schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql"))
)

http_ds = api.add_http_data_source("ds", "https://states.amazonaws.com",
    name="httpDsWithStepF",
    description="from appsync to StepFunctions Workflow",
    authorization_config=appsync.aws_appsync.AwsIamConfig(
        signing_region="us-east-1",
        signing_service_name="states"
    )
)

http_ds.create_resolver(
    type_name="Mutation",
    field_name="callStepFunction",
    request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
    response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
)
```

### Amazon OpenSearch Service

AppSync has builtin support for Amazon OpenSearch Service (successor to Amazon
Elasticsearch Service) from domains that are provisioned through your AWS account. You can
use AppSync resolvers to perform GraphQL operations such as queries, mutations, and
subscriptions.

```python
import monocdk as opensearch

# api: appsync.GraphqlApi


user = iam.User(self, "User")
domain = opensearch.Domain(self, "Domain",
    version=opensearch.EngineVersion.OPENSEARCH_1_2,
    removal_policy=RemovalPolicy.DESTROY,
    fine_grained_access_control=opensearch.aws_opensearchservice.AdvancedSecurityOptions(master_user_arn=user.user_arn),
    encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(enabled=True),
    node_to_node_encryption=True,
    enforce_https=True
)
ds = api.add_open_search_data_source("ds", domain)

ds.create_resolver(
    type_name="Query",
    field_name="getTests",
    request_mapping_template=appsync.MappingTemplate.from_string(JSON.stringify({
        "version": "2017-02-28",
        "operation": "GET",
        "path": "/id/post/_search",
        "params": {
            "headers": {},
            "query_string": {},
            "body": {"from": 0, "size": 50}
        }
    })),
    response_mapping_template=appsync.MappingTemplate.from_string("""[
            #foreach($entry in $context.result.hits.hits)
            #if( $velocityCount > 1 ) , #end
            $utils.toJson($entry.get("_source"))
            #end
          ]""")
)
```

## Custom Domain Names

For many use cases you may want to associate a custom domain name with your
GraphQL API. This can be done during the API creation.

```python
import monocdk as acm
import monocdk as route53

# hosted zone and route53 features
# hosted_zone_id: str
zone_name = "example.com"


my_domain_name = "api.example.com"
certificate = acm.Certificate(self, "cert", domain_name=my_domain_name)
api = appsync.GraphqlApi(self, "api",
    name="myApi",
    domain_name=acm.aws_appsync.DomainOptions(
        certificate=certificate,
        domain_name=my_domain_name
    )
)

# hosted zone for adding appsync domain
zone = route53.HostedZone.from_hosted_zone_attributes(self, "HostedZone",
    hosted_zone_id=hosted_zone_id,
    zone_name=zone_name
)

# create a cname to the appsync domain. will map to something like xxxx.cloudfront.net
route53.CnameRecord(self, "CnameApiRecord",
    record_name="api",
    zone=zone,
    domain_name=my_domain_name
)
```

## Schema

Every GraphQL Api needs a schema to define the Api. CDK offers `appsync.Schema`
for static convenience methods for various types of schema declaration: code-first
or schema-first.

### Code-First

When declaring your GraphQL Api, CDK defaults to a code-first approach if the
`schema` property is not configured.

```python
api = appsync.GraphqlApi(self, "api", name="myApi")
```

CDK will declare a `Schema` class that will give your Api access functions to
define your schema code-first: `addType`, `addToSchema`, etc.

You can also declare your `Schema` class outside of your CDK stack, to define
your schema externally.

```python
schema = appsync.Schema()
schema.add_type(appsync.ObjectType("demo",
    definition={"id": appsync.GraphqlType.id()}
))
api = appsync.GraphqlApi(self, "api",
    name="myApi",
    schema=schema
)
```

See the [code-first schema](#Code-First-Schema) section for more details.

### Schema-First

You can define your GraphQL Schema from a file on disk. For convenience, use
the `appsync.Schema.fromAsset` to specify the file representing your schema.

```python
api = appsync.GraphqlApi(self, "api",
    name="myApi",
    schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphl"))
)
```

## Imports

Any GraphQL Api that has been created outside the stack can be imported from
another stack into your CDK app. Utilizing the `fromXxx` function, you have
the ability to add data sources and resolvers through a `IGraphqlApi` interface.

```python
# api: appsync.GraphqlApi
# table: dynamodb.Table

imported_api = appsync.GraphqlApi.from_graphql_api_attributes(self, "IApi",
    graphql_api_id=api.api_id,
    graphql_api_arn=api.arn
)
imported_api.add_dynamo_db_data_source("TableDataSource", table)
```

If you don't specify `graphqlArn` in `fromXxxAttributes`, CDK will autogenerate
the expected `arn` for the imported api, given the `apiId`. For creating data
sources and resolvers, an `apiId` is sufficient.

## Authorization

There are multiple authorization types available for GraphQL API to cater to different
access use cases. They are:

* API Keys (`AuthorizationType.API_KEY`)
* Amazon Cognito User Pools (`AuthorizationType.USER_POOL`)
* OpenID Connect (`AuthorizationType.OPENID_CONNECT`)
* AWS Identity and Access Management (`AuthorizationType.AWS_IAM`)
* AWS Lambda (`AuthorizationType.AWS_LAMBDA`)

These types can be used simultaneously in a single API, allowing different types of clients to
access data. When you specify an authorization type, you can also specify the corresponding
authorization mode to finish defining your authorization. For example, this is a GraphQL API
with AWS Lambda Authorization.

```python
import monocdk as lambda_
# auth_function: lambda.Function


appsync.GraphqlApi(self, "api",
    name="api",
    schema=appsync.Schema.from_asset(path.join(__dirname, "appsync.test.graphql")),
    authorization_config=lambda.aws_appsync.AuthorizationConfig(
        default_authorization=lambda.aws_appsync.AuthorizationMode(
            authorization_type=appsync.AuthorizationType.LAMBDA,
            lambda_authorizer_config=lambda.aws_appsync.LambdaAuthorizerConfig(
                handler=auth_function
            )
        )
    )
)
```

## Permissions

When using `AWS_IAM` as the authorization type for GraphQL API, an IAM Role
with correct permissions must be used for access to API.

When configuring permissions, you can specify specific resources to only be
accessible by `IAM` authorization. For example, if you want to only allow mutability
for `IAM` authorized access you would configure the following.

In `schema.graphql`:

```gql
type Mutation {
  updateExample(...): ...
    @aws_iam
}
```

In `IAM`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "appsync:GraphQL"
      ],
      "Resource": [
        "arn:aws:appsync:REGION:ACCOUNT_ID:apis/GRAPHQL_ID/types/Mutation/fields/updateExample"
      ]
    }
  ]
}
```

See [documentation](https://docs.aws.amazon.com/appsync/latest/devguide/security.html#aws-iam-authorization) for more details.

To make this easier, CDK provides `grant` API.

Use the `grant` function for more granular authorization.

```python
# api: appsync.GraphqlApi
role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
)

api.grant(role, appsync.IamResource.custom("types/Mutation/fields/updateExample"), "appsync:GraphQL")
```

### IamResource

In order to use the `grant` functions, you need to use the class `IamResource`.

* `IamResource.custom(...arns)` permits custom ARNs and requires an argument.
* `IamResouce.ofType(type, ...fields)` permits ARNs for types and their fields.
* `IamResource.all()` permits ALL resources.

### Generic Permissions

Alternatively, you can use more generic `grant` functions to accomplish the same usage.

These include:

* grantMutation (use to grant access to Mutation fields)
* grantQuery (use to grant access to Query fields)
* grantSubscription (use to grant access to Subscription fields)

```python
# api: appsync.GraphqlApi
# role: iam.Role


# For generic types
api.grant_mutation(role, "updateExample")

# For custom types and granular design
api.grant(role, appsync.IamResource.of_type("Mutation", "updateExample"), "appsync:GraphQL")
```

## Pipeline Resolvers and AppSync Functions

AppSync Functions are local functions that perform certain operations onto a
backend data source. Developers can compose operations (Functions) and execute
them in sequence with Pipeline Resolvers.

```python
# api: appsync.GraphqlApi


appsync_function = appsync.AppsyncFunction(self, "function",
    name="appsync_function",
    api=api,
    data_source=api.add_none_data_source("none"),
    request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
    response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
)
```

AppSync Functions are used in tandem with pipeline resolvers to compose multiple
operations.

```python
# api: appsync.GraphqlApi
# appsync_function: appsync.AppsyncFunction


pipeline_resolver = appsync.Resolver(self, "pipeline",
    api=api,
    data_source=api.add_none_data_source("none"),
    type_name="typeName",
    field_name="fieldName",
    request_mapping_template=appsync.MappingTemplate.from_file("beforeRequest.vtl"),
    pipeline_config=[appsync_function],
    response_mapping_template=appsync.MappingTemplate.from_file("afterResponse.vtl")
)
```

Learn more about Pipeline Resolvers and AppSync Functions [here](https://docs.aws.amazon.com/appsync/latest/devguide/pipeline-resolvers.html).

## Code-First Schema

CDK offers the ability to generate your schema in a code-first approach.
A code-first approach offers a developer workflow with:

* **modularity**: organizing schema type definitions into different files
* **reusability**: simplifying down boilerplate/repetitive code
* **consistency**: resolvers and schema definition will always be synced

The code-first approach allows for **dynamic** schema generation. You can generate your schema based on variables and templates to reduce code duplication.

### Code-First Example

To showcase the code-first approach. Let's try to model the following schema segment.

```gql
interface Node {
  id: String
}

type Query {
  allFilms(after: String, first: Int, before: String, last: Int): FilmConnection
}

type FilmNode implements Node {
  filmName: String
}

type FilmConnection {
  edges: [FilmEdge]
  films: [Film]
  totalCount: Int
}

type FilmEdge {
  node: Film
  cursor: String
}
```

Above we see a schema that allows for generating paginated responses. For example,
we can query `allFilms(first: 100)` since `FilmConnection` acts as an intermediary
for holding `FilmEdges` we can write a resolver to return the first 100 films.

In a separate file, we can declare our object types and related functions.
We will call this file `object-types.ts` and we will have created it in a way that
allows us to generate other `XxxConnection` and `XxxEdges` in the future.

```python
import monocdk as appsync
pluralize = require("pluralize")

args = {
    "after": appsync.GraphqlType.string(),
    "first": appsync.GraphqlType.int(),
    "before": appsync.GraphqlType.string(),
    "last": appsync.GraphqlType.int()
}

Node = appsync.InterfaceType("Node",
    definition={"id": appsync.GraphqlType.string()}
)
FilmNode = appsync.ObjectType("FilmNode",
    interface_types=[Node],
    definition={"film_name": appsync.GraphqlType.string()}
)

def generate_edge_and_connection(base):
    edge = appsync.ObjectType(f"{base.name}Edge",
        definition={"node": base.attribute(), "cursor": appsync.GraphqlType.string()}
    )
    connection = appsync.ObjectType(f"{base.name}Connection",
        definition={
            "edges": edge.attribute(is_list=True),
            "pluralize(base.name)": base.attribute(is_list=True),
            "total_count": appsync.GraphqlType.int()
        }
    )
    return {"edge": edge, "connection": connection}
```

Finally, we will go to our `cdk-stack` and combine everything together
to generate our schema.

```python
# dummy_request: appsync.MappingTemplate
# dummy_response: appsync.MappingTemplate


api = appsync.GraphqlApi(self, "Api",
    name="demo"
)

object_types = [Node, FilmNode]

film_connections = generate_edge_and_connection(FilmNode)

api.add_query("allFilms", appsync.ResolvableField(
    return_type=film_connections.connection.attribute(),
    args=args,
    data_source=api.add_none_data_source("none"),
    request_mapping_template=dummy_request,
    response_mapping_template=dummy_response
))

api.add_type(Node)
api.add_type(FilmNode)
api.add_type(film_connections.edge)
api.add_type(film_connections.connection)
```

Notice how we can utilize the `generateEdgeAndConnection` function to generate
Object Types. In the future, if we wanted to create more Object Types, we can simply
create the base Object Type (i.e. Film) and from there we can generate its respective
`Connections` and `Edges`.

Check out a more in-depth example [here](https://github.com/BryanPan342/starwars-code-first).

## GraphQL Types

One of the benefits of GraphQL is its strongly typed nature. We define the
types within an object, query, mutation, interface, etc. as **GraphQL Types**.

GraphQL Types are the building blocks of types, whether they are scalar, objects,
interfaces, etc. GraphQL Types can be:

* [**Scalar Types**](https://docs.aws.amazon.com/appsync/latest/devguide/scalars.html): Id, Int, String, AWSDate, etc.
* [**Object Types**](#Object-Types): types that you generate (i.e. `demo` from the example above)
* [**Interface Types**](#Interface-Types): abstract types that define the base implementation of other
  Intermediate Types

More concretely, GraphQL Types are simply the types appended to variables.
Referencing the object type `Demo` in the previous example, the GraphQL Types
is `String!` and is applied to both the names `id` and `version`.

### Directives

`Directives` are attached to a field or type and affect the execution of queries,
mutations, and types. With AppSync, we use `Directives` to configure authorization.
CDK provides static functions to add directives to your Schema.

* `Directive.iam()` sets a type or field's authorization to be validated through `Iam`
* `Directive.apiKey()` sets a type or field's authorization to be validated through a `Api Key`
* `Directive.oidc()` sets a type or field's authorization to be validated through `OpenID Connect`
* `Directive.cognito(...groups: string[])` sets a type or field's authorization to be validated
  through `Cognito User Pools`

  * `groups` the name of the cognito groups to give access

To learn more about authorization and directives, read these docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/security.html).

### Field and Resolvable Fields

While `GraphqlType` is a base implementation for GraphQL fields, we have abstractions
on top of `GraphqlType` that provide finer grain support.

### Field

`Field` extends `GraphqlType` and will allow you to define arguments. [**Interface Types**](#Interface-Types) are not resolvable and this class will allow you to define arguments,
but not its resolvers.

For example, if we want to create the following type:

```gql
type Node {
  test(argument: string): String
}
```

The CDK code required would be:

```python
field = appsync.Field(
    return_type=appsync.GraphqlType.string(),
    args={
        "argument": appsync.GraphqlType.string()
    }
)
type = appsync.InterfaceType("Node",
    definition={"test": field}
)
```

### Resolvable Fields

`ResolvableField` extends `Field` and will allow you to define arguments and its resolvers.
[**Object Types**](#Object-Types) can have fields that resolve and perform operations on
your backend.

You can also create resolvable fields for object types.

```gql
type Info {
  node(id: String): String
}
```

The CDK code required would be:

```python
# api: appsync.GraphqlApi
# dummy_request: appsync.MappingTemplate
# dummy_response: appsync.MappingTemplate

info = appsync.ObjectType("Info",
    definition={
        "node": appsync.ResolvableField(
            return_type=appsync.GraphqlType.string(),
            args={
                "id": appsync.GraphqlType.string()
            },
            data_source=api.add_none_data_source("none"),
            request_mapping_template=dummy_request,
            response_mapping_template=dummy_response
        )
    }
)
```

To nest resolvers, we can also create top level query types that call upon
other types. Building off the previous example, if we want the following graphql
type definition:

```gql
type Query {
  get(argument: string): Info
}
```

The CDK code required would be:

```python
# api: appsync.GraphqlApi
# dummy_request: appsync.MappingTemplate
# dummy_response: appsync.MappingTemplate

query = appsync.ObjectType("Query",
    definition={
        "get": appsync.ResolvableField(
            return_type=appsync.GraphqlType.string(),
            args={
                "argument": appsync.GraphqlType.string()
            },
            data_source=api.add_none_data_source("none"),
            request_mapping_template=dummy_request,
            response_mapping_template=dummy_response
        )
    }
)
```

Learn more about fields and resolvers [here](https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference-overview.html).

### Intermediate Types

Intermediate Types are defined by Graphql Types and Fields. They have a set of defined
fields, where each field corresponds to another type in the system. Intermediate
Types will be the meat of your GraphQL Schema as they are the types defined by you.

Intermediate Types include:

* [**Interface Types**](#Interface-Types)
* [**Object Types**](#Object-Types)
* [**Enum Types**](#Enum-Types)
* [**Input Types**](#Input-Types)
* [**Union Types**](#Union-Types)

#### Interface Types

**Interface Types** are abstract types that define the implementation of other
intermediate types. They are useful for eliminating duplication and can be used
to generate Object Types with less work.

You can create Interface Types ***externally***.

```python
node = appsync.InterfaceType("Node",
    definition={
        "id": appsync.GraphqlType.string(is_required=True)
    }
)
```

To learn more about **Interface Types**, read the docs [here](https://graphql.org/learn/schema/#interfaces).

#### Object Types

**Object Types** are types that you declare. For example, in the [code-first example](#code-first-example)
the `demo` variable is an **Object Type**. **Object Types** are defined by
GraphQL Types and are only usable when linked to a GraphQL Api.

You can create Object Types in two ways:

1. Object Types can be created ***externally***.

   ```python
   api = appsync.GraphqlApi(self, "Api",
       name="demo"
   )
   demo = appsync.ObjectType("Demo",
       definition={
           "id": appsync.GraphqlType.string(is_required=True),
           "version": appsync.GraphqlType.string(is_required=True)
       }
   )

   api.add_type(demo)
   ```

   > This method allows for reusability and modularity, ideal for larger projects.
   > For example, imagine moving all Object Type definition outside the stack.

   `object-types.ts` - a file for object type definitions

   ```python
   import monocdk as appsync
   demo = appsync.ObjectType("Demo",
       definition={
           "id": appsync.GraphqlType.string(is_required=True),
           "version": appsync.GraphqlType.string(is_required=True)
       }
   )
   ```

   `cdk-stack.ts` - a file containing our cdk stack

   ```python
   # api: appsync.GraphqlApi

   api.add_type(demo)
   ```
2. Object Types can be created ***externally*** from an Interface Type.

   ```python
   node = appsync.InterfaceType("Node",
       definition={
           "id": appsync.GraphqlType.string(is_required=True)
       }
   )
   demo = appsync.ObjectType("Demo",
       interface_types=[node],
       definition={
           "version": appsync.GraphqlType.string(is_required=True)
       }
   )
   ```

   > This method allows for reusability and modularity, ideal for reducing code duplication.

To learn more about **Object Types**, read the docs [here](https://graphql.org/learn/schema/#object-types-and-fields).

#### Enum Types

**Enum Types** are a special type of Intermediate Type. They restrict a particular
set of allowed values for other Intermediate Types.

```gql
enum Episode {
  NEWHOPE
  EMPIRE
  JEDI
}
```

> This means that wherever we use the type Episode in our schema, we expect it to
> be exactly one of NEWHOPE, EMPIRE, or JEDI.

The above GraphQL Enumeration Type can be expressed in CDK as the following:

```python
# api: appsync.GraphqlApi

episode = appsync.EnumType("Episode",
    definition=["NEWHOPE", "EMPIRE", "JEDI"
    ]
)
api.add_type(episode)
```

To learn more about **Enum Types**, read the docs [here](https://graphql.org/learn/schema/#enumeration-types).

#### Input Types

**Input Types** are special types of Intermediate Types. They give users an
easy way to pass complex objects for top level Mutation and Queries.

```gql
input Review {
  stars: Int!
  commentary: String
}
```

The above GraphQL Input Type can be expressed in CDK as the following:

```python
# api: appsync.GraphqlApi

review = appsync.InputType("Review",
    definition={
        "stars": appsync.GraphqlType.int(is_required=True),
        "commentary": appsync.GraphqlType.string()
    }
)
api.add_type(review)
```

To learn more about **Input Types**, read the docs [here](https://graphql.org/learn/schema/#input-types).

#### Union Types

**Union Types** are a special type of Intermediate Type. They are similar to
Interface Types, but they cannot specify any common fields between types.

**Note:** the fields of a union type need to be `Object Types`. In other words, you
can't create a union type out of interfaces, other unions, or inputs.

```gql
union Search = Human | Droid | Starship
```

The above GraphQL Union Type encompasses the Object Types of Human, Droid and Starship. It
can be expressed in CDK as the following:

```python
# api: appsync.GraphqlApi

string = appsync.GraphqlType.string()
human = appsync.ObjectType("Human", definition={"name": string})
droid = appsync.ObjectType("Droid", definition={"name": string})
starship = appsync.ObjectType("Starship", definition={"name": string})
search = appsync.UnionType("Search",
    definition=[human, droid, starship]
)
api.add_type(search)
```

To learn more about **Union Types**, read the docs [here](https://graphql.org/learn/schema/#union-types).

### Query

Every schema requires a top level Query type. By default, the schema will look
for the `Object Type` named `Query`. The top level `Query` is the **only** exposed
type that users can access to perform `GET` operations on your Api.

To add fields for these queries, we can simply run the `addQuery` function to add
to the schema's `Query` type.

```python
# api: appsync.GraphqlApi
# film_connection: appsync.InterfaceType
# dummy_request: appsync.MappingTemplate
# dummy_response: appsync.MappingTemplate


string = appsync.GraphqlType.string()
int = appsync.GraphqlType.int()
api.add_query("allFilms", appsync.ResolvableField(
    return_type=film_connection.attribute(),
    args={"after": string, "first": int, "before": string, "last": int},
    data_source=api.add_none_data_source("none"),
    request_mapping_template=dummy_request,
    response_mapping_template=dummy_response
))
```

To learn more about top level operations, check out the docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/graphql-overview.html).

### Mutation

Every schema **can** have a top level Mutation type. By default, the schema will look
for the `ObjectType` named `Mutation`. The top level `Mutation` Type is the only exposed
type that users can access to perform `mutable` operations on your Api.

To add fields for these mutations, we can simply run the `addMutation` function to add
to the schema's `Mutation` type.

```python
# api: appsync.GraphqlApi
# film_node: appsync.ObjectType
# dummy_request: appsync.MappingTemplate
# dummy_response: appsync.MappingTemplate


string = appsync.GraphqlType.string()
int = appsync.GraphqlType.int()
api.add_mutation("addFilm", appsync.ResolvableField(
    return_type=film_node.attribute(),
    args={"name": string, "film_number": int},
    data_source=api.add_none_data_source("none"),
    request_mapping_template=dummy_request,
    response_mapping_template=dummy_response
))
```

To learn more about top level operations, check out the docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/graphql-overview.html).

### Subscription

Every schema **can** have a top level Subscription type. The top level `Subscription` Type
is the only exposed type that users can access to invoke a response to a mutation. `Subscriptions`
notify users when a mutation specific mutation is called. This means you can make any data source
real time by specify a GraphQL Schema directive on a mutation.

**Note**: The AWS AppSync client SDK automatically handles subscription connection management.

To add fields for these subscriptions, we can simply run the `addSubscription` function to add
to the schema's `Subscription` type.

```python
# api: appsync.GraphqlApi
# film: appsync.InterfaceType


api.add_subscription("addedFilm", appsync.Field(
    return_type=film.attribute(),
    args={"id": appsync.GraphqlType.id(is_required=True)},
    directives=[appsync.Directive.subscribe("addFilm")]
))
```

To learn more about top level operations, check out the docs [here](https://docs.aws.amazon.com/appsync/latest/devguide/real-time-data.html).
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

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    Expiration as _Expiration_505df041,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    ResourceProps as _ResourceProps_9b554c0f,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_certificatemanager import ICertificate as _ICertificate_c7bbdc16
from ..aws_cognito import IUserPool as _IUserPool_5e500460
from ..aws_dynamodb import ITable as _ITable_24826f7e
from ..aws_elasticsearch import IDomain as _IDomain_0b3cf46c
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_opensearchservice import IDomain as _IDomain_cb64a2bc
from ..aws_rds import IServerlessCluster as _IServerlessCluster_8ed6177c
from ..aws_secretsmanager import ISecret as _ISecret_22fb8757


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.AddFieldOptions",
    jsii_struct_bases=[],
    name_mapping={"field": "field", "field_name": "fieldName"},
)
class AddFieldOptions:
    def __init__(
        self,
        *,
        field: typing.Optional["IField"] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The options to add a field to an Intermediate Type.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            # field: appsync.Field
            
            add_field_options = appsync.AddFieldOptions(
                field=field,
                field_name="fieldName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c4b5ba5ddc105148a19797b94b8291a268f45937207f8edc4fddc44c7a4146)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field is not None:
            self._values["field"] = field
        if field_name is not None:
            self._values["field_name"] = field_name

    @builtins.property
    def field(self) -> typing.Optional["IField"]:
        '''(experimental) The resolvable field to add.

        This option must be configured for Object, Interface,
        Input and Union Types.

        :default: - no IField

        :stability: experimental
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional["IField"], result)

    @builtins.property
    def field_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the field.

        This option must be configured for Object, Interface,
        Input and Enum Types.

        :default: - no fieldName

        :stability: experimental
        '''
        result = self._values.get("field_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddFieldOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ApiKeyConfig",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "expires": "expires", "name": "name"},
)
class ApiKeyConfig:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expires: typing.Optional[_Expiration_505df041] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration for API Key authorization in AppSync.

        :param description: (experimental) Description of API key. Default: - 'Default API Key created by CDK'
        :param expires: (experimental) The time from creation time after which the API key expires. It must be a minimum of 1 day and a maximum of 365 days from date of creation. Rounded down to the nearest hour. Default: - 7 days rounded down to nearest hour
        :param name: (experimental) Unique name of the API Key. Default: - 'DefaultAPIKey'

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_appsync as appsync
            
            # expiration: monocdk.Expiration
            
            api_key_config = appsync.ApiKeyConfig(
                description="description",
                expires=expiration,
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231f3250183cc31a44bfd28a36a4194a41f06c1dfd7be8b83343308f4d6c7445)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if expires is not None:
            self._values["expires"] = expires
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of API key.

        :default: - 'Default API Key created by CDK'

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expires(self) -> typing.Optional[_Expiration_505df041]:
        '''(experimental) The time from creation time after which the API key expires.

        It must be a minimum of 1 day and a maximum of 365 days from date of creation.
        Rounded down to the nearest hour.

        :default: - 7 days rounded down to nearest hour

        :stability: experimental
        '''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[_Expiration_505df041], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Unique name of the API Key.

        :default: - 'DefaultAPIKey'

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.AppsyncFunctionAttributes",
    jsii_struct_bases=[],
    name_mapping={"function_arn": "functionArn"},
)
class AppsyncFunctionAttributes:
    def __init__(self, *, function_arn: builtins.str) -> None:
        '''(experimental) The attributes for imported AppSync Functions.

        :param function_arn: (experimental) the ARN of the AppSync function.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            appsync_function_attributes = appsync.AppsyncFunctionAttributes(
                function_arn="functionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db829bb9d3941cda1e447de3022cc090de917aca302df8a954fd679ecea9b423)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''(experimental) the ARN of the AppSync function.

        :stability: experimental
        '''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncFunctionAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Assign(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.Assign"):
    '''(experimental) Utility class representing the assigment of a value to an attribute.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        assign = appsync.Assign("attr", "arg")
    '''

    def __init__(self, attr: builtins.str, arg: builtins.str) -> None:
        '''
        :param attr: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b3c4b5913e45e95b058dfcfd2c40d9b4e51dfc1b9c20e9e937a48d07d054e0)
            check_type(argname="argument attr", value=attr, expected_type=type_hints["attr"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        jsii.create(self.__class__, self, [attr, arg])

    @jsii.member(jsii_name="putInMap")
    def put_in_map(self, map: builtins.str) -> builtins.str:
        '''(experimental) Renders the assignment as a map element.

        :param map: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__412d93a11445bd2d219e7628787a1cdeedf090de56d31c720935defb7cdaf3b8)
            check_type(argname="argument map", value=map, expected_type=type_hints["map"])
        return typing.cast(builtins.str, jsii.invoke(self, "putInMap", [map]))

    @jsii.member(jsii_name="renderAsAssignment")
    def render_as_assignment(self) -> builtins.str:
        '''(experimental) Renders the assignment as a VTL string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderAsAssignment", []))


class AttributeValues(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.AttributeValues",
):
    '''(experimental) Specifies the attribute value assignments.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "Api",
            name="demo",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
            authorization_config=appsync.aws_appsync.AuthorizationConfig(
                default_authorization=appsync.aws_appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.IAM
                )
            ),
            xray_enabled=True
        )
        
        demo_table = dynamodb.Table(self, "DemoTable",
            partition_key=appsync.aws_dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
        
        # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
        demo_dS.create_resolver(
            type_name="Query",
            field_name="getDemos",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )
        
        # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
        demo_dS.create_resolver(
            type_name="Mutation",
            field_name="addDemo",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                appsync.PrimaryKey.partition("id").auto(),
                appsync.Values.projecting("input")),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )
    '''

    def __init__(
        self,
        container: builtins.str,
        assignments: typing.Optional[typing.Sequence[Assign]] = None,
    ) -> None:
        '''
        :param container: -
        :param assignments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d382ab11578ec047f1a85108822bfe1eb552059c762eefa1fee55544e326a31c)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument assignments", value=assignments, expected_type=type_hints["assignments"])
        jsii.create(self.__class__, self, [container, assignments])

    @jsii.member(jsii_name="attribute")
    def attribute(self, attr: builtins.str) -> "AttributeValuesStep":
        '''(experimental) Allows assigning a value to the specified attribute.

        :param attr: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432b5187af9b456765e04f46081a3db17e0ac0f39665f59fa6b1f1b126ff860f)
            check_type(argname="argument attr", value=attr, expected_type=type_hints["attr"])
        return typing.cast("AttributeValuesStep", jsii.invoke(self, "attribute", [attr]))

    @jsii.member(jsii_name="renderTemplate")
    def render_template(self) -> builtins.str:
        '''(experimental) Renders the attribute value assingments to a VTL string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderTemplate", []))

    @jsii.member(jsii_name="renderVariables")
    def render_variables(self) -> builtins.str:
        '''(experimental) Renders the variables required for ``renderTemplate``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderVariables", []))


class AttributeValuesStep(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.AttributeValuesStep",
):
    '''(experimental) Utility class to allow assigning a value to an attribute.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        # assign: appsync.Assign
        
        attribute_values_step = appsync.AttributeValuesStep("attr", "container", [assign])
    '''

    def __init__(
        self,
        attr: builtins.str,
        container: builtins.str,
        assignments: typing.Sequence[Assign],
    ) -> None:
        '''
        :param attr: -
        :param container: -
        :param assignments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feee645b88bff9ed76fe8f2d7fb48c1ee81f6e4788e59d2770b8c3633ddcc167)
            check_type(argname="argument attr", value=attr, expected_type=type_hints["attr"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument assignments", value=assignments, expected_type=type_hints["assignments"])
        jsii.create(self.__class__, self, [attr, container, assignments])

    @jsii.member(jsii_name="is")
    def is_(self, val: builtins.str) -> AttributeValues:
        '''(experimental) Assign the value to the current attribute.

        :param val: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72dfec8500382f9b4a10831734f75973c88cbadc038eabc6b94b4af305dd655d)
            check_type(argname="argument val", value=val, expected_type=type_hints["val"])
        return typing.cast(AttributeValues, jsii.invoke(self, "is", [val]))


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.AuthorizationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "additional_authorization_modes": "additionalAuthorizationModes",
        "default_authorization": "defaultAuthorization",
    },
)
class AuthorizationConfig:
    def __init__(
        self,
        *,
        additional_authorization_modes: typing.Optional[typing.Sequence[typing.Union["AuthorizationMode", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_authorization: typing.Optional[typing.Union["AuthorizationMode", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Configuration of the API authorization modes.

        :param additional_authorization_modes: (experimental) Additional authorization modes. Default: - No other modes
        :param default_authorization: (experimental) Optional authorization configuration. Default: - API Key authorization

        :stability: experimental
        :exampleMetadata: infused

        Example::

            api = appsync.GraphqlApi(self, "Api",
                name="demo",
                schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
                authorization_config=appsync.aws_appsync.AuthorizationConfig(
                    default_authorization=appsync.aws_appsync.AuthorizationMode(
                        authorization_type=appsync.AuthorizationType.IAM
                    )
                ),
                xray_enabled=True
            )
            
            demo_table = dynamodb.Table(self, "DemoTable",
                partition_key=appsync.aws_dynamodb.Attribute(
                    name="id",
                    type=dynamodb.AttributeType.STRING
                )
            )
            
            demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
            
            # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
            demo_dS.create_resolver(
                type_name="Query",
                field_name="getDemos",
                request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
                response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
            )
            
            # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
            demo_dS.create_resolver(
                type_name="Mutation",
                field_name="addDemo",
                request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                    appsync.PrimaryKey.partition("id").auto(),
                    appsync.Values.projecting("input")),
                response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
            )
        '''
        if isinstance(default_authorization, dict):
            default_authorization = AuthorizationMode(**default_authorization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f848df7434aeebf6be81eb6719f92a928024a60b10ddf122117f892ce385af3c)
            check_type(argname="argument additional_authorization_modes", value=additional_authorization_modes, expected_type=type_hints["additional_authorization_modes"])
            check_type(argname="argument default_authorization", value=default_authorization, expected_type=type_hints["default_authorization"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_authorization_modes is not None:
            self._values["additional_authorization_modes"] = additional_authorization_modes
        if default_authorization is not None:
            self._values["default_authorization"] = default_authorization

    @builtins.property
    def additional_authorization_modes(
        self,
    ) -> typing.Optional[typing.List["AuthorizationMode"]]:
        '''(experimental) Additional authorization modes.

        :default: - No other modes

        :stability: experimental
        '''
        result = self._values.get("additional_authorization_modes")
        return typing.cast(typing.Optional[typing.List["AuthorizationMode"]], result)

    @builtins.property
    def default_authorization(self) -> typing.Optional["AuthorizationMode"]:
        '''(experimental) Optional authorization configuration.

        :default: - API Key authorization

        :stability: experimental
        '''
        result = self._values.get("default_authorization")
        return typing.cast(typing.Optional["AuthorizationMode"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthorizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.AuthorizationMode",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_type": "authorizationType",
        "api_key_config": "apiKeyConfig",
        "lambda_authorizer_config": "lambdaAuthorizerConfig",
        "open_id_connect_config": "openIdConnectConfig",
        "user_pool_config": "userPoolConfig",
    },
)
class AuthorizationMode:
    def __init__(
        self,
        *,
        authorization_type: "AuthorizationType",
        api_key_config: typing.Optional[typing.Union[ApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_authorizer_config: typing.Optional[typing.Union["LambdaAuthorizerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        open_id_connect_config: typing.Optional[typing.Union["OpenIdConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        user_pool_config: typing.Optional[typing.Union["UserPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Interface to specify default or additional authorization(s).

        :param authorization_type: (experimental) One of possible four values AppSync supports. Default: - ``AuthorizationType.API_KEY``
        :param api_key_config: (experimental) If authorizationType is ``AuthorizationType.API_KEY``, this option can be configured. Default: - name: 'DefaultAPIKey' | description: 'Default API Key created by CDK'
        :param lambda_authorizer_config: (experimental) If authorizationType is ``AuthorizationType.LAMBDA``, this option is required. Default: - none
        :param open_id_connect_config: (experimental) If authorizationType is ``AuthorizationType.OIDC``, this option is required. Default: - none
        :param user_pool_config: (experimental) If authorizationType is ``AuthorizationType.USER_POOL``, this option is required. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            api = appsync.GraphqlApi(self, "Api",
                name="demo",
                schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
                authorization_config=appsync.aws_appsync.AuthorizationConfig(
                    default_authorization=appsync.aws_appsync.AuthorizationMode(
                        authorization_type=appsync.AuthorizationType.IAM
                    )
                ),
                xray_enabled=True
            )
            
            demo_table = dynamodb.Table(self, "DemoTable",
                partition_key=appsync.aws_dynamodb.Attribute(
                    name="id",
                    type=dynamodb.AttributeType.STRING
                )
            )
            
            demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
            
            # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
            demo_dS.create_resolver(
                type_name="Query",
                field_name="getDemos",
                request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
                response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
            )
            
            # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
            demo_dS.create_resolver(
                type_name="Mutation",
                field_name="addDemo",
                request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                    appsync.PrimaryKey.partition("id").auto(),
                    appsync.Values.projecting("input")),
                response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
            )
        '''
        if isinstance(api_key_config, dict):
            api_key_config = ApiKeyConfig(**api_key_config)
        if isinstance(lambda_authorizer_config, dict):
            lambda_authorizer_config = LambdaAuthorizerConfig(**lambda_authorizer_config)
        if isinstance(open_id_connect_config, dict):
            open_id_connect_config = OpenIdConnectConfig(**open_id_connect_config)
        if isinstance(user_pool_config, dict):
            user_pool_config = UserPoolConfig(**user_pool_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37fd6e5348ae8cdad8e885cafe8fb4f61ae31174630831c10bd199a2362b959)
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument api_key_config", value=api_key_config, expected_type=type_hints["api_key_config"])
            check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
            check_type(argname="argument open_id_connect_config", value=open_id_connect_config, expected_type=type_hints["open_id_connect_config"])
            check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_type": authorization_type,
        }
        if api_key_config is not None:
            self._values["api_key_config"] = api_key_config
        if lambda_authorizer_config is not None:
            self._values["lambda_authorizer_config"] = lambda_authorizer_config
        if open_id_connect_config is not None:
            self._values["open_id_connect_config"] = open_id_connect_config
        if user_pool_config is not None:
            self._values["user_pool_config"] = user_pool_config

    @builtins.property
    def authorization_type(self) -> "AuthorizationType":
        '''(experimental) One of possible four values AppSync supports.

        :default: - ``AuthorizationType.API_KEY``

        :see: https://docs.aws.amazon.com/appsync/latest/devguide/security.html
        :stability: experimental
        '''
        result = self._values.get("authorization_type")
        assert result is not None, "Required property 'authorization_type' is missing"
        return typing.cast("AuthorizationType", result)

    @builtins.property
    def api_key_config(self) -> typing.Optional[ApiKeyConfig]:
        '''(experimental) If authorizationType is ``AuthorizationType.API_KEY``, this option can be configured.

        :default: - name: 'DefaultAPIKey' | description: 'Default API Key created by CDK'

        :stability: experimental
        '''
        result = self._values.get("api_key_config")
        return typing.cast(typing.Optional[ApiKeyConfig], result)

    @builtins.property
    def lambda_authorizer_config(self) -> typing.Optional["LambdaAuthorizerConfig"]:
        '''(experimental) If authorizationType is ``AuthorizationType.LAMBDA``, this option is required.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("lambda_authorizer_config")
        return typing.cast(typing.Optional["LambdaAuthorizerConfig"], result)

    @builtins.property
    def open_id_connect_config(self) -> typing.Optional["OpenIdConnectConfig"]:
        '''(experimental) If authorizationType is ``AuthorizationType.OIDC``, this option is required.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("open_id_connect_config")
        return typing.cast(typing.Optional["OpenIdConnectConfig"], result)

    @builtins.property
    def user_pool_config(self) -> typing.Optional["UserPoolConfig"]:
        '''(experimental) If authorizationType is ``AuthorizationType.USER_POOL``, this option is required.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("user_pool_config")
        return typing.cast(typing.Optional["UserPoolConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuthorizationMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_appsync.AuthorizationType")
class AuthorizationType(enum.Enum):
    '''(experimental) enum with all possible values for AppSync authorization type.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "Api",
            name="demo",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
            authorization_config=appsync.aws_appsync.AuthorizationConfig(
                default_authorization=appsync.aws_appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.IAM
                )
            ),
            xray_enabled=True
        )
        
        demo_table = dynamodb.Table(self, "DemoTable",
            partition_key=appsync.aws_dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
        
        # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
        demo_dS.create_resolver(
            type_name="Query",
            field_name="getDemos",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )
        
        # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
        demo_dS.create_resolver(
            type_name="Mutation",
            field_name="addDemo",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                appsync.PrimaryKey.partition("id").auto(),
                appsync.Values.projecting("input")),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )
    '''

    API_KEY = "API_KEY"
    '''(experimental) API Key authorization type.

    :stability: experimental
    '''
    IAM = "IAM"
    '''(experimental) AWS IAM authorization type.

    Can be used with Cognito Identity Pool federated credentials

    :stability: experimental
    '''
    USER_POOL = "USER_POOL"
    '''(experimental) Cognito User Pool authorization type.

    :stability: experimental
    '''
    OIDC = "OIDC"
    '''(experimental) OpenID Connect authorization type.

    :stability: experimental
    '''
    LAMBDA = "LAMBDA"
    '''(experimental) Lambda authorization type.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.AwsIamConfig",
    jsii_struct_bases=[],
    name_mapping={
        "signing_region": "signingRegion",
        "signing_service_name": "signingServiceName",
    },
)
class AwsIamConfig:
    def __init__(
        self,
        *,
        signing_region: builtins.str,
        signing_service_name: builtins.str,
    ) -> None:
        '''(experimental) The authorization config in case the HTTP endpoint requires authorization.

        :param signing_region: (experimental) The signing region for AWS IAM authorization.
        :param signing_service_name: (experimental) The signing service name for AWS IAM authorization.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            api = appsync.GraphqlApi(self, "api",
                name="api",
                schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql"))
            )
            
            http_ds = api.add_http_data_source("ds", "https://states.amazonaws.com",
                name="httpDsWithStepF",
                description="from appsync to StepFunctions Workflow",
                authorization_config=appsync.aws_appsync.AwsIamConfig(
                    signing_region="us-east-1",
                    signing_service_name="states"
                )
            )
            
            http_ds.create_resolver(
                type_name="Mutation",
                field_name="callStepFunction",
                request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
                response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf50fd1171074e0c8e2cd82d65775d36b74bda43f87437414522135d3b916380)
            check_type(argname="argument signing_region", value=signing_region, expected_type=type_hints["signing_region"])
            check_type(argname="argument signing_service_name", value=signing_service_name, expected_type=type_hints["signing_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "signing_region": signing_region,
            "signing_service_name": signing_service_name,
        }

    @builtins.property
    def signing_region(self) -> builtins.str:
        '''(experimental) The signing region for AWS IAM authorization.

        :stability: experimental
        '''
        result = self._values.get("signing_region")
        assert result is not None, "Required property 'signing_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_service_name(self) -> builtins.str:
        '''(experimental) The signing service name for AWS IAM authorization.

        :stability: experimental
        '''
        result = self._values.get("signing_service_name")
        assert result is not None, "Required property 'signing_service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsIamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.BaseAppsyncFunctionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
    },
)
class BaseAppsyncFunctionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
    ) -> None:
        '''(experimental) the base properties for AppSync Functions.

        :param name: (experimental) the name of the AppSync Function.
        :param description: (experimental) the description for this AppSync Function. Default: - no description
        :param request_mapping_template: (experimental) the request mapping template for the AppSync Function. Default: - no request mapping template
        :param response_mapping_template: (experimental) the response mapping template for the AppSync Function. Default: - no response mapping template

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            # mapping_template: appsync.MappingTemplate
            
            base_appsync_function_props = appsync.BaseAppsyncFunctionProps(
                name="name",
            
                # the properties below are optional
                description="description",
                request_mapping_template=mapping_template,
                response_mapping_template=mapping_template
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437cd7588080049d00ffa12e64d0b9283690d742bedea2f3ae376e2b5de9da16)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name of the AppSync Function.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description for this AppSync Function.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional["MappingTemplate"]:
        '''(experimental) the request mapping template for the AppSync Function.

        :default: - no request mapping template

        :stability: experimental
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional["MappingTemplate"], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional["MappingTemplate"]:
        '''(experimental) the response mapping template for the AppSync Function.

        :default: - no response mapping template

        :stability: experimental
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional["MappingTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseAppsyncFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BaseDataSource(
    _Construct_e78e779f,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_appsync.BaseDataSource",
):
    '''(experimental) Abstract AppSync datasource implementation.

    Do not use directly but use subclasses for concrete datasources

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # dummy_request: appsync.MappingTemplate
        # dummy_response: appsync.MappingTemplate
        
        info = appsync.ObjectType("Info",
            definition={
                "node": appsync.ResolvableField(
                    return_type=appsync.GraphqlType.string(),
                    args={
                        "id": appsync.GraphqlType.string()
                    },
                    data_source=api.add_none_data_source("none"),
                    request_mapping_template=dummy_request,
                    response_mapping_template=dummy_response
                )
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["BackedDataSourceProps", typing.Dict[builtins.str, typing.Any]],
        *,
        type: builtins.str,
        dynamo_db_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.DynamoDBConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        elasticsearch_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.ElasticsearchConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        http_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.HttpConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        lambda_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.LambdaConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_search_service_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.OpenSearchServiceConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        relational_database_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.RelationalDatabaseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param type: (experimental) the type of the AppSync datasource.
        :param dynamo_db_config: (experimental) configuration for DynamoDB Datasource. Default: - No config
        :param elasticsearch_config: (deprecated) configuration for Elasticsearch data source. Default: - No config
        :param http_config: (experimental) configuration for HTTP Datasource. Default: - No config
        :param lambda_config: (experimental) configuration for Lambda Datasource. Default: - No config
        :param open_search_service_config: (experimental) configuration for OpenSearch data source. Default: - No config
        :param relational_database_config: (experimental) configuration for RDS Datasource. Default: - No config

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ada652827c62a80544a99a875a0d6add183d4724e27756d693413d167292ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        extended = ExtendedDataSourceProps(
            type=type,
            dynamo_db_config=dynamo_db_config,
            elasticsearch_config=elasticsearch_config,
            http_config=http_config,
            lambda_config=lambda_config,
            open_search_service_config=open_search_service_config,
            relational_database_config=relational_database_config,
        )

        jsii.create(self.__class__, self, [scope, id, props, extended])

    @jsii.member(jsii_name="createFunction")
    def create_function(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
    ) -> "AppsyncFunction":
        '''(experimental) creates a new appsync function for this datasource and API using the given properties.

        :param name: (experimental) the name of the AppSync Function.
        :param description: (experimental) the description for this AppSync Function. Default: - no description
        :param request_mapping_template: (experimental) the request mapping template for the AppSync Function. Default: - no request mapping template
        :param response_mapping_template: (experimental) the response mapping template for the AppSync Function. Default: - no response mapping template

        :stability: experimental
        '''
        props = BaseAppsyncFunctionProps(
            name=name,
            description=description,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

        return typing.cast("AppsyncFunction", jsii.invoke(self, "createFunction", [props]))

    @jsii.member(jsii_name="createResolver")
    def create_resolver(
        self,
        *,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union["CachingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence["IAppsyncFunction"]] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
    ) -> "Resolver":
        '''(experimental) creates a new resolver for this datasource and API using the given properties.

        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        '''
        props = BaseResolverProps(
            field_name=field_name,
            type_name=type_name,
            caching_config=caching_config,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

        return typing.cast("Resolver", jsii.invoke(self, "createResolver", [props]))

    @builtins.property
    @jsii.member(jsii_name="ds")
    def ds(self) -> "CfnDataSource":
        '''(experimental) the underlying CFN data source resource.

        :stability: experimental
        '''
        return typing.cast("CfnDataSource", jsii.get(self, "ds"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of the data source.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="api")
    def _api(self) -> "IGraphqlApi":
        '''
        :stability: experimental
        '''
        return typing.cast("IGraphqlApi", jsii.get(self, "api"))

    @_api.setter
    def _api(self, value: "IGraphqlApi") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8de15a2db1e815bf851adec5a0ea508d6103ed1905e54ed9a1cb260966dbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "api", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def _service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "serviceRole"))

    @_service_role.setter
    def _service_role(self, value: typing.Optional[_IRole_59af6f50]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6ec40ecd72f76ba4438036f7cad4e938af94241b98bca9eadd7c45704c31b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRole", value)


class _BaseDataSourceProxy(BaseDataSource):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseDataSource).__jsii_proxy_class__ = lambda : _BaseDataSourceProxy


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.BaseDataSourceProps",
    jsii_struct_bases=[],
    name_mapping={"api": "api", "description": "description", "name": "name"},
)
class BaseDataSourceProps:
    def __init__(
        self,
        *,
        api: "IGraphqlApi",
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Base properties for an AppSync datasource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            # graphql_api: appsync.GraphqlApi
            
            base_data_source_props = appsync.BaseDataSourceProps(
                api=graphql_api,
            
                # the properties below are optional
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae5bedb607ee01f50ce0f93bb0aa849e62481c6b4eb21263326d28ddef301b9)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def api(self) -> "IGraphqlApi":
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast("IGraphqlApi", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.BaseResolverProps",
    jsii_struct_bases=[],
    name_mapping={
        "field_name": "fieldName",
        "type_name": "typeName",
        "caching_config": "cachingConfig",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
    },
)
class BaseResolverProps:
    def __init__(
        self,
        *,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union["CachingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence["IAppsyncFunction"]] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
    ) -> None:
        '''(experimental) Basic properties for an AppSync resolver.

        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Build a data source for AppSync to access the database.
            # api: appsync.GraphqlApi
            # Create username and password secret for DB Cluster
            secret = rds.DatabaseSecret(self, "AuroraSecret",
                username="clusteradmin"
            )
            
            # The VPC to place the cluster in
            vpc = ec2.Vpc(self, "AuroraVpc")
            
            # Create the serverless cluster, provide all values needed to customise the database.
            cluster = rds.ServerlessCluster(self, "AuroraCluster",
                engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
                vpc=vpc,
                credentials={"username": "clusteradmin"},
                cluster_identifier="db-endpoint-test",
                default_database_name="demos"
            )
            rds_dS = api.add_rds_data_source("rds", cluster, secret, "demos")
            
            # Set up a resolver for an RDS query.
            rds_dS.create_resolver(
                type_name="Query",
                field_name="getDemosRds",
                request_mapping_template=appsync.MappingTemplate.from_string("""
                      {
                        "version": "2018-05-29",
                        "statements": [
                          "SELECT * FROM demos"
                        ]
                      }
                      """),
                response_mapping_template=appsync.MappingTemplate.from_string("""
                        $utils.toJson($utils.rds.toJsonObject($ctx.result)[0])
                      """)
            )
            
            # Set up a resolver for an RDS mutation.
            rds_dS.create_resolver(
                type_name="Mutation",
                field_name="addDemoRds",
                request_mapping_template=appsync.MappingTemplate.from_string("""
                      {
                        "version": "2018-05-29",
                        "statements": [
                          "INSERT INTO demos VALUES (:id, :version)",
                          "SELECT * WHERE id = :id"
                        ],
                        "variableMap": {
                          ":id": $util.toJson($util.autoId()),
                          ":version": $util.toJson($ctx.args.version)
                        }
                      }
                      """),
                response_mapping_template=appsync.MappingTemplate.from_string("""
                        $utils.toJson($utils.rds.toJsonObject($ctx.result)[1][0])
                      """)
            )
        '''
        if isinstance(caching_config, dict):
            caching_config = CachingConfig(**caching_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82c10d3fa82355396b4b487e2da6c7e5bfabddbfd5d9a96f827f92fc45092ec)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument caching_config", value=caching_config, expected_type=type_hints["caching_config"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_name": field_name,
            "type_name": type_name,
        }
        if caching_config is not None:
            self._values["caching_config"] = caching_config
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template

    @builtins.property
    def field_name(self) -> builtins.str:
        '''(experimental) name of the GraphQL field in the given type this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''(experimental) name of the GraphQL type this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caching_config(self) -> typing.Optional["CachingConfig"]:
        '''(experimental) The caching configuration for this resolver.

        :default: - No caching configuration

        :stability: experimental
        '''
        result = self._values.get("caching_config")
        return typing.cast(typing.Optional["CachingConfig"], result)

    @builtins.property
    def pipeline_config(self) -> typing.Optional[typing.List["IAppsyncFunction"]]:
        '''(experimental) configuration of the pipeline resolver.

        :default:

        - no pipeline resolver configuration
        An empty array | undefined sets resolver to be of kind, unit

        :stability: experimental
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.List["IAppsyncFunction"]], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional["MappingTemplate"]:
        '''(experimental) The request mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional["MappingTemplate"], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional["MappingTemplate"]:
        '''(experimental) The response mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional["MappingTemplate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseResolverProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.BaseTypeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_list": "isList",
        "is_required": "isRequired",
        "is_required_list": "isRequiredList",
    },
)
class BaseTypeOptions:
    def __init__(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Base options for GraphQL Types.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        :option: isRequiredList - is this attribute a non-nullable list
        :exampleMetadata: infused

        Example::

            api = appsync.GraphqlApi(self, "Api",
                name="demo"
            )
            demo = appsync.ObjectType("Demo",
                definition={
                    "id": appsync.GraphqlType.string(is_required=True),
                    "version": appsync.GraphqlType.string(is_required=True)
                }
            )
            
            api.add_type(demo)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a62a9572878684cde53bd79baa23d3ce75a82e76d1b31c0131d69a9f98a8f4)
            check_type(argname="argument is_list", value=is_list, expected_type=type_hints["is_list"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument is_required_list", value=is_required_list, expected_type=type_hints["is_required_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_list is not None:
            self._values["is_list"] = is_list
        if is_required is not None:
            self._values["is_required"] = is_required
        if is_required_list is not None:
            self._values["is_required_list"] = is_required_list

    @builtins.property
    def is_list(self) -> typing.Optional[builtins.bool]:
        '''(experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type].

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required(self) -> typing.Optional[builtins.bool]:
        '''(experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type!

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required_list(self) -> typing.Optional[builtins.bool]:
        '''(experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]!

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_required_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CachingConfig",
    jsii_struct_bases=[],
    name_mapping={"ttl": "ttl", "caching_keys": "cachingKeys"},
)
class CachingConfig:
    def __init__(
        self,
        *,
        ttl: _Duration_070aa057,
        caching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) CachingConfig for AppSync resolvers.

        :param ttl: (experimental) The TTL in seconds for a resolver that has caching enabled. Valid values are between 1 and 3600 seconds.
        :param caching_keys: (experimental) The caching keys for a resolver that has caching enabled. Valid values are entries from the $context.arguments, $context.source, and $context.identity maps. Default: - No caching keys

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_appsync as appsync
            
            # duration: monocdk.Duration
            
            caching_config = appsync.CachingConfig(
                ttl=duration,
            
                # the properties below are optional
                caching_keys=["cachingKeys"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b85095182209411ec213c9887a34eeac0c3086ac918c64aa9610ea1662001dd)
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument caching_keys", value=caching_keys, expected_type=type_hints["caching_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ttl": ttl,
        }
        if caching_keys is not None:
            self._values["caching_keys"] = caching_keys

    @builtins.property
    def ttl(self) -> _Duration_070aa057:
        '''(experimental) The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

        :stability: experimental
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(_Duration_070aa057, result)

    @builtins.property
    def caching_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The caching keys for a resolver that has caching enabled.

        Valid values are entries from the $context.arguments, $context.source, and $context.identity maps.

        :default: - No caching keys

        :stability: experimental
        '''
        result = self._values.get("caching_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CachingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApiCache(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnApiCache",
):
    '''A CloudFormation ``AWS::AppSync::ApiCache``.

    The ``AWS::AppSync::ApiCache`` resource represents the input of a ``CreateApiCache`` operation.

    :cloudformationResource: AWS::AppSync::ApiCache
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_api_cache = appsync.CfnApiCache(self, "MyCfnApiCache",
            api_caching_behavior="apiCachingBehavior",
            api_id="apiId",
            ttl=123,
            type="type",
        
            # the properties below are optional
            at_rest_encryption_enabled=False,
            transit_encryption_enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_caching_behavior: builtins.str,
        api_id: builtins.str,
        ttl: jsii.Number,
        type: builtins.str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::ApiCache``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_caching_behavior: Caching behavior. - *FULL_REQUEST_CACHING* : All requests are fully cached. - *PER_RESOLVER_CACHING* : Individual resolvers that you specify are cached.
        :param api_id: The GraphQL API ID.
        :param ttl: TTL in seconds for cache entries. Valid values are 1–3,600 seconds.
        :param type: The cache instance type. Valid values are. - ``SMALL`` - ``MEDIUM`` - ``LARGE`` - ``XLARGE`` - ``LARGE_2X`` - ``LARGE_4X`` - ``LARGE_8X`` (not available in all regions) - ``LARGE_12X`` Historically, instance types were identified by an EC2-style value. As of July 2020, this is deprecated, and the generic identifiers above should be used. The following legacy instance types are available, but their use is discouraged: - *T2_SMALL* : A t2.small instance type. - *T2_MEDIUM* : A t2.medium instance type. - *R4_LARGE* : A r4.large instance type. - *R4_XLARGE* : A r4.xlarge instance type. - *R4_2XLARGE* : A r4.2xlarge instance type. - *R4_4XLARGE* : A r4.4xlarge instance type. - *R4_8XLARGE* : A r4.8xlarge instance type.
        :param at_rest_encryption_enabled: At-rest encryption flag for cache. You cannot update this setting after creation.
        :param transit_encryption_enabled: Transit encryption flag when connecting to cache. You cannot update this setting after creation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84cdfa82f8a00d54b852478e6dca196494ef6e27ea8753d1488137e7a5084bd1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiCacheProps(
            api_caching_behavior=api_caching_behavior,
            api_id=api_id,
            ttl=ttl,
            type=type,
            at_rest_encryption_enabled=at_rest_encryption_enabled,
            transit_encryption_enabled=transit_encryption_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8aff2fce593096fdf95c82192af7d32fc14bd55cc5c8a06154f4517ea0453a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2bfb2ac9948e9fda22ff0bd7ce79ffd32a655acde3125efc21fd9cd67923bc)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiCachingBehavior")
    def api_caching_behavior(self) -> builtins.str:
        '''Caching behavior.

        - *FULL_REQUEST_CACHING* : All requests are fully cached.
        - *PER_RESOLVER_CACHING* : Individual resolvers that you specify are cached.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-apicachingbehavior
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiCachingBehavior"))

    @api_caching_behavior.setter
    def api_caching_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce7ff4041a1ae1111843e0ee8d3cba8fb207cda3b154dc0c72baff2d9ffcf7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiCachingBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The GraphQL API ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf1a0e916b7b0c74d551bfab209057efb424e6c1c43eca8a15752384e81d84b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        '''TTL in seconds for cache entries.

        Valid values are 1–3,600 seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-ttl
        '''
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114083910e6a9df2fee43dc42e9767b117a48f81594e07378a375d1095ee2e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The cache instance type. Valid values are.

        - ``SMALL``
        - ``MEDIUM``
        - ``LARGE``
        - ``XLARGE``
        - ``LARGE_2X``
        - ``LARGE_4X``
        - ``LARGE_8X`` (not available in all regions)
        - ``LARGE_12X``

        Historically, instance types were identified by an EC2-style value. As of July 2020, this is deprecated, and the generic identifiers above should be used.

        The following legacy instance types are available, but their use is discouraged:

        - *T2_SMALL* : A t2.small instance type.
        - *T2_MEDIUM* : A t2.medium instance type.
        - *R4_LARGE* : A r4.large instance type.
        - *R4_XLARGE* : A r4.xlarge instance type.
        - *R4_2XLARGE* : A r4.2xlarge instance type.
        - *R4_4XLARGE* : A r4.4xlarge instance type.
        - *R4_8XLARGE* : A r4.8xlarge instance type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f507cf5618125723d74b80c438669bd10f3206628ffe638a64430a1d391229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="atRestEncryptionEnabled")
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''At-rest encryption flag for cache.

        You cannot update this setting after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-atrestencryptionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "atRestEncryptionEnabled"))

    @at_rest_encryption_enabled.setter
    def at_rest_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7839cdbcff7bebd705ae658d2f6b76a54caed43046501cae192f20ea83f064df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "atRestEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionEnabled")
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Transit encryption flag when connecting to cache.

        You cannot update this setting after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-transitencryptionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "transitEncryptionEnabled"))

    @transit_encryption_enabled.setter
    def transit_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e2ab3c9c706ef5ff8a1054f3379e3f1531b8066995f14f21f72d0b0bbf4ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionEnabled", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnApiCacheProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_caching_behavior": "apiCachingBehavior",
        "api_id": "apiId",
        "ttl": "ttl",
        "type": "type",
        "at_rest_encryption_enabled": "atRestEncryptionEnabled",
        "transit_encryption_enabled": "transitEncryptionEnabled",
    },
)
class CfnApiCacheProps:
    def __init__(
        self,
        *,
        api_caching_behavior: builtins.str,
        api_id: builtins.str,
        ttl: jsii.Number,
        type: builtins.str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApiCache``.

        :param api_caching_behavior: Caching behavior. - *FULL_REQUEST_CACHING* : All requests are fully cached. - *PER_RESOLVER_CACHING* : Individual resolvers that you specify are cached.
        :param api_id: The GraphQL API ID.
        :param ttl: TTL in seconds for cache entries. Valid values are 1–3,600 seconds.
        :param type: The cache instance type. Valid values are. - ``SMALL`` - ``MEDIUM`` - ``LARGE`` - ``XLARGE`` - ``LARGE_2X`` - ``LARGE_4X`` - ``LARGE_8X`` (not available in all regions) - ``LARGE_12X`` Historically, instance types were identified by an EC2-style value. As of July 2020, this is deprecated, and the generic identifiers above should be used. The following legacy instance types are available, but their use is discouraged: - *T2_SMALL* : A t2.small instance type. - *T2_MEDIUM* : A t2.medium instance type. - *R4_LARGE* : A r4.large instance type. - *R4_XLARGE* : A r4.xlarge instance type. - *R4_2XLARGE* : A r4.2xlarge instance type. - *R4_4XLARGE* : A r4.4xlarge instance type. - *R4_8XLARGE* : A r4.8xlarge instance type.
        :param at_rest_encryption_enabled: At-rest encryption flag for cache. You cannot update this setting after creation.
        :param transit_encryption_enabled: Transit encryption flag when connecting to cache. You cannot update this setting after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_api_cache_props = appsync.CfnApiCacheProps(
                api_caching_behavior="apiCachingBehavior",
                api_id="apiId",
                ttl=123,
                type="type",
            
                # the properties below are optional
                at_rest_encryption_enabled=False,
                transit_encryption_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d55a5bb56c62477c5e22957bb380ccacb31106fa2c989d2291f95befc788e31)
            check_type(argname="argument api_caching_behavior", value=api_caching_behavior, expected_type=type_hints["api_caching_behavior"])
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument at_rest_encryption_enabled", value=at_rest_encryption_enabled, expected_type=type_hints["at_rest_encryption_enabled"])
            check_type(argname="argument transit_encryption_enabled", value=transit_encryption_enabled, expected_type=type_hints["transit_encryption_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_caching_behavior": api_caching_behavior,
            "api_id": api_id,
            "ttl": ttl,
            "type": type,
        }
        if at_rest_encryption_enabled is not None:
            self._values["at_rest_encryption_enabled"] = at_rest_encryption_enabled
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled

    @builtins.property
    def api_caching_behavior(self) -> builtins.str:
        '''Caching behavior.

        - *FULL_REQUEST_CACHING* : All requests are fully cached.
        - *PER_RESOLVER_CACHING* : Individual resolvers that you specify are cached.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-apicachingbehavior
        '''
        result = self._values.get("api_caching_behavior")
        assert result is not None, "Required property 'api_caching_behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The GraphQL API ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ttl(self) -> jsii.Number:
        '''TTL in seconds for cache entries.

        Valid values are 1–3,600 seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-ttl
        '''
        result = self._values.get("ttl")
        assert result is not None, "Required property 'ttl' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The cache instance type. Valid values are.

        - ``SMALL``
        - ``MEDIUM``
        - ``LARGE``
        - ``XLARGE``
        - ``LARGE_2X``
        - ``LARGE_4X``
        - ``LARGE_8X`` (not available in all regions)
        - ``LARGE_12X``

        Historically, instance types were identified by an EC2-style value. As of July 2020, this is deprecated, and the generic identifiers above should be used.

        The following legacy instance types are available, but their use is discouraged:

        - *T2_SMALL* : A t2.small instance type.
        - *T2_MEDIUM* : A t2.medium instance type.
        - *R4_LARGE* : A r4.large instance type.
        - *R4_XLARGE* : A r4.xlarge instance type.
        - *R4_2XLARGE* : A r4.2xlarge instance type.
        - *R4_4XLARGE* : A r4.4xlarge instance type.
        - *R4_8XLARGE* : A r4.8xlarge instance type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''At-rest encryption flag for cache.

        You cannot update this setting after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-atrestencryptionenabled
        '''
        result = self._values.get("at_rest_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Transit encryption flag when connecting to cache.

        You cannot update this setting after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apicache.html#cfn-appsync-apicache-transitencryptionenabled
        '''
        result = self._values.get("transit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiCacheProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApiKey(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnApiKey",
):
    '''A CloudFormation ``AWS::AppSync::ApiKey``.

    The ``AWS::AppSync::ApiKey`` resource creates a unique key that you can distribute to clients who are executing GraphQL operations with AWS AppSync that require an API key.

    :cloudformationResource: AWS::AppSync::ApiKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_api_key = appsync.CfnApiKey(self, "MyCfnApiKey",
            api_id="apiId",
        
            # the properties below are optional
            api_key_id="apiKeyId",
            description="description",
            expires=123
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_id: builtins.str,
        api_key_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        expires: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::ApiKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: Unique AWS AppSync GraphQL API ID for this API key.
        :param api_key_id: The API key ID.
        :param description: Unique description of your API key.
        :param expires: The time after which the API key expires. The date is represented as seconds since the epoch, rounded down to the nearest hour.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1745329398fb4f72199eca022835c6074caedd37e668df16abdb9a9b4e5d6984)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApiKeyProps(
            api_id=api_id,
            api_key_id=api_key_id,
            description=description,
            expires=expires,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3e339ada370820eb79a9f5e8ebd75e18d38367f6c11141a2faf024238f9cfa)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73cebfa9b7770aae191eeae939b654d51bcdc1e07df730452c5f0c3cb5fb4304)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApiKey")
    def attr_api_key(self) -> builtins.str:
        '''The API key.

        :cloudformationAttribute: ApiKey
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApiKey"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the API key, such as ``arn:aws:appsync:us-east-1:123456789012:apis/graphqlapiid/apikey/apikeya1bzhi`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''Unique AWS AppSync GraphQL API ID for this API key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae2c70284c80b8245add8dc7d84cdad15a74d6ec15562a15eb093de677bad9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeyId")
    def api_key_id(self) -> typing.Optional[builtins.str]:
        '''The API key ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-apikeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyId"))

    @api_key_id.setter
    def api_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7c008d27865ff54024321b431c9eb907868226f0dbc6b157b9749a0bcf4372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Unique description of your API key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a2bb63e3ecc8b090e43a5f3cc1d2c299dcc4a65dcf136a08bd6c505db1e65a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="expires")
    def expires(self) -> typing.Optional[jsii.Number]:
        '''The time after which the API key expires.

        The date is represented as seconds since the epoch, rounded down to the nearest hour.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-expires
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expires"))

    @expires.setter
    def expires(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__216fb64032d083c12ae64ef1684d526682f7781e6cf09789f6919cce5ee13a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expires", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnApiKeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "api_key_id": "apiKeyId",
        "description": "description",
        "expires": "expires",
    },
)
class CfnApiKeyProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        api_key_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        expires: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnApiKey``.

        :param api_id: Unique AWS AppSync GraphQL API ID for this API key.
        :param api_key_id: The API key ID.
        :param description: Unique description of your API key.
        :param expires: The time after which the API key expires. The date is represented as seconds since the epoch, rounded down to the nearest hour.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_api_key_props = appsync.CfnApiKeyProps(
                api_id="apiId",
            
                # the properties below are optional
                api_key_id="apiKeyId",
                description="description",
                expires=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9caca502fddf7e46a2b754450e9d49003c66dbdeaa9688d5d905c8a1c7a664)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument api_key_id", value=api_key_id, expected_type=type_hints["api_key_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expires", value=expires, expected_type=type_hints["expires"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
        }
        if api_key_id is not None:
            self._values["api_key_id"] = api_key_id
        if description is not None:
            self._values["description"] = description
        if expires is not None:
            self._values["expires"] = expires

    @builtins.property
    def api_id(self) -> builtins.str:
        '''Unique AWS AppSync GraphQL API ID for this API key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_id(self) -> typing.Optional[builtins.str]:
        '''The API key ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-apikeyid
        '''
        result = self._values.get("api_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Unique description of your API key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expires(self) -> typing.Optional[jsii.Number]:
        '''The time after which the API key expires.

        The date is represented as seconds since the epoch, rounded down to the nearest hour.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-apikey.html#cfn-appsync-apikey-expires
        '''
        result = self._values.get("expires")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDataSource(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnDataSource",
):
    '''A CloudFormation ``AWS::AppSync::DataSource``.

    The ``AWS::AppSync::DataSource`` resource creates data sources for resolvers in AWS AppSync to connect to, such as Amazon DynamoDB , AWS Lambda , and Amazon OpenSearch Service . Resolvers use these data sources to fetch data when clients make GraphQL calls.

    :cloudformationResource: AWS::AppSync::DataSource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_data_source = appsync.CfnDataSource(self, "MyCfnDataSource",
            api_id="apiId",
            name="name",
            type="type",
        
            # the properties below are optional
            description="description",
            dynamo_db_config=appsync.CfnDataSource.DynamoDBConfigProperty(
                aws_region="awsRegion",
                table_name="tableName",
        
                # the properties below are optional
                delta_sync_config=appsync.CfnDataSource.DeltaSyncConfigProperty(
                    base_table_ttl="baseTableTtl",
                    delta_sync_table_name="deltaSyncTableName",
                    delta_sync_table_ttl="deltaSyncTableTtl"
                ),
                use_caller_credentials=False,
                versioned=False
            ),
            elasticsearch_config=appsync.CfnDataSource.ElasticsearchConfigProperty(
                aws_region="awsRegion",
                endpoint="endpoint"
            ),
            http_config=appsync.CfnDataSource.HttpConfigProperty(
                endpoint="endpoint",
        
                # the properties below are optional
                authorization_config=appsync.CfnDataSource.AuthorizationConfigProperty(
                    authorization_type="authorizationType",
        
                    # the properties below are optional
                    aws_iam_config=appsync.CfnDataSource.AwsIamConfigProperty(
                        signing_region="signingRegion",
                        signing_service_name="signingServiceName"
                    )
                )
            ),
            lambda_config=appsync.CfnDataSource.LambdaConfigProperty(
                lambda_function_arn="lambdaFunctionArn"
            ),
            open_search_service_config=appsync.CfnDataSource.OpenSearchServiceConfigProperty(
                aws_region="awsRegion",
                endpoint="endpoint"
            ),
            relational_database_config=appsync.CfnDataSource.RelationalDatabaseConfigProperty(
                relational_database_source_type="relationalDatabaseSourceType",
        
                # the properties below are optional
                rds_http_endpoint_config=appsync.CfnDataSource.RdsHttpEndpointConfigProperty(
                    aws_region="awsRegion",
                    aws_secret_store_arn="awsSecretStoreArn",
                    db_cluster_identifier="dbClusterIdentifier",
        
                    # the properties below are optional
                    database_name="databaseName",
                    schema="schema"
                )
            ),
            service_role_arn="serviceRoleArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dynamo_db_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.DynamoDBConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        elasticsearch_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.ElasticsearchConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        http_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.HttpConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        lambda_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.LambdaConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_search_service_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.OpenSearchServiceConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        relational_database_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.RelationalDatabaseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::DataSource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: Unique AWS AppSync GraphQL API identifier where this data source will be created.
        :param name: Friendly name for you to identify your AppSync data source after creation.
        :param type: The type of the data source. - *AWS_LAMBDA* : The data source is an AWS Lambda function. - *AMAZON_DYNAMODB* : The data source is an Amazon DynamoDB table. - *AMAZON_ELASTICSEARCH* : The data source is an Amazon OpenSearch Service domain. - *AMAZON_OPENSEARCH_SERVICE* : The data source is an Amazon OpenSearch Service domain. - *NONE* : There is no data source. This type is used when you wish to invoke a GraphQL operation without connecting to a data source, such as performing data transformation with resolvers or triggering a subscription to be invoked from a mutation. - *HTTP* : The data source is an HTTP endpoint. - *RELATIONAL_DATABASE* : The data source is a relational database.
        :param description: The description of the data source.
        :param dynamo_db_config: AWS Region and TableName for an Amazon DynamoDB table in your account.
        :param elasticsearch_config: AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account. As of September 2021, Amazon Elasticsearch Service is Amazon OpenSearch Service . This property is deprecated. For new data sources, use *OpenSearchServiceConfig* to specify an OpenSearch Service data source.
        :param http_config: Endpoints for an HTTP data source.
        :param lambda_config: An ARN of a Lambda function in valid ARN format. This can be the ARN of a Lambda function that exists in the current account or in another account.
        :param open_search_service_config: AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.
        :param relational_database_config: Relational Database configuration of the relational database data source.
        :param service_role_arn: The AWS Identity and Access Management service role ARN for the data source. The system assumes this role when accessing the data source. Required if ``Type`` is specified as ``AWS_LAMBDA`` , ``AMAZON_DYNAMODB`` , ``AMAZON_ELASTICSEARCH`` , or ``AMAZON_OPENSEARCH_SERVICE`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e431d54ec028379c69f90936ec4cf0f9985c93757792a0a189198ca63dd3417)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataSourceProps(
            api_id=api_id,
            name=name,
            type=type,
            description=description,
            dynamo_db_config=dynamo_db_config,
            elasticsearch_config=elasticsearch_config,
            http_config=http_config,
            lambda_config=lambda_config,
            open_search_service_config=open_search_service_config,
            relational_database_config=relational_database_config,
            service_role_arn=service_role_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8989352e31e20213df451568da1421d13a2c2cd4bce0cb24f318832301db7912)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7e31af7eb72e51701963db17729da8ea28eb791981047c21e22712decf43b8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDataSourceArn")
    def attr_data_source_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the API key, such as ``arn:aws:appsync:us-east-1:123456789012:apis/graphqlapiid/datasources/datasourcename`` .

        :cloudformationAttribute: DataSourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataSourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''Friendly name for you to identify your AWS AppSync data source after creation.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''Unique AWS AppSync GraphQL API identifier where this data source will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c65343426b168d311f189fbb09cf8e90d100020a734269e7eaa5b70031c5c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Friendly name for you to identify your AppSync data source after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe9b37238ec27282392ce35c07aa903de923c4cd651150cc57c21307d499e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the data source.

        - *AWS_LAMBDA* : The data source is an AWS Lambda function.
        - *AMAZON_DYNAMODB* : The data source is an Amazon DynamoDB table.
        - *AMAZON_ELASTICSEARCH* : The data source is an Amazon OpenSearch Service domain.
        - *AMAZON_OPENSEARCH_SERVICE* : The data source is an Amazon OpenSearch Service domain.
        - *NONE* : There is no data source. This type is used when you wish to invoke a GraphQL operation without connecting to a data source, such as performing data transformation with resolvers or triggering a subscription to be invoked from a mutation.
        - *HTTP* : The data source is an HTTP endpoint.
        - *RELATIONAL_DATABASE* : The data source is a relational database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbb29468a31f6c1178b0b8b1473a9192bcbb80367b00bf7c8d29fbf5e8e01f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d4d032ca0587858e15d01722950d5c8f508a8cfc582a3cf651013db7bb0497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dynamoDbConfig")
    def dynamo_db_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.DynamoDBConfigProperty", _IResolvable_a771d0ef]]:
        '''AWS Region and TableName for an Amazon DynamoDB table in your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-dynamodbconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.DynamoDBConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "dynamoDbConfig"))

    @dynamo_db_config.setter
    def dynamo_db_config(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.DynamoDBConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f4efecdb8ceeb7045c9ec8b1fc10409c55514aac08172ee8e032a0b61fe19e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamoDbConfig", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchConfig")
    def elasticsearch_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.ElasticsearchConfigProperty", _IResolvable_a771d0ef]]:
        '''AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.

        As of September 2021, Amazon Elasticsearch Service is Amazon OpenSearch Service . This property is deprecated. For new data sources, use *OpenSearchServiceConfig* to specify an OpenSearch Service data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-elasticsearchconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.ElasticsearchConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "elasticsearchConfig"))

    @elasticsearch_config.setter
    def elasticsearch_config(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.ElasticsearchConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a36bef672a8de25f720628b763e637aec206e5ddd474f98a49813bde94d7e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticsearchConfig", value)

    @builtins.property
    @jsii.member(jsii_name="httpConfig")
    def http_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.HttpConfigProperty", _IResolvable_a771d0ef]]:
        '''Endpoints for an HTTP data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-httpconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.HttpConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "httpConfig"))

    @http_config.setter
    def http_config(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.HttpConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f59db87bddc78318d2a5982aca0be01132630bca4e430094b06743060da9b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpConfig", value)

    @builtins.property
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.LambdaConfigProperty", _IResolvable_a771d0ef]]:
        '''An ARN of a Lambda function in valid ARN format.

        This can be the ARN of a Lambda function that exists in the current account or in another account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-lambdaconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.LambdaConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "lambdaConfig"))

    @lambda_config.setter
    def lambda_config(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.LambdaConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39c10684ed637eeee09f1da0f73604586c6acc7bc158aab11224473627a4d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaConfig", value)

    @builtins.property
    @jsii.member(jsii_name="openSearchServiceConfig")
    def open_search_service_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.OpenSearchServiceConfigProperty", _IResolvable_a771d0ef]]:
        '''AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-opensearchserviceconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.OpenSearchServiceConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "openSearchServiceConfig"))

    @open_search_service_config.setter
    def open_search_service_config(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.OpenSearchServiceConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2825b54c35598c2171e9332b4a1b2d55c336ec02e8d4a7ed6e06a9fd994b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openSearchServiceConfig", value)

    @builtins.property
    @jsii.member(jsii_name="relationalDatabaseConfig")
    def relational_database_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.RelationalDatabaseConfigProperty", _IResolvable_a771d0ef]]:
        '''Relational Database configuration of the relational database data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-relationaldatabaseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.RelationalDatabaseConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "relationalDatabaseConfig"))

    @relational_database_config.setter
    def relational_database_config(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.RelationalDatabaseConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556d03654260bac78a94ad054991337eb8c28ceadcb2e0c2d96f163d86b3bde5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relationalDatabaseConfig", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management service role ARN for the data source.

        The system assumes this role when accessing the data source.

        Required if ``Type`` is specified as ``AWS_LAMBDA`` , ``AMAZON_DYNAMODB`` , ``AMAZON_ELASTICSEARCH`` , or ``AMAZON_OPENSEARCH_SERVICE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-servicerolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0d09146ba59b68e772788e4bba9fac807dbc42daed968db2ef1a2b7eacffc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.AuthorizationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_type": "authorizationType",
            "aws_iam_config": "awsIamConfig",
        },
    )
    class AuthorizationConfigProperty:
        def __init__(
            self,
            *,
            authorization_type: builtins.str,
            aws_iam_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.AwsIamConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``AuthorizationConfig`` property type specifies the authorization type and configuration for an AWS AppSync http data source.

            ``AuthorizationConfig`` is a property of the `AWS AppSync DataSource HttpConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html>`_ property type.

            :param authorization_type: The authorization type that the HTTP endpoint requires. - *AWS_IAM* : The authorization type is Signature Version 4 (SigV4).
            :param aws_iam_config: The AWS Identity and Access Management settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-authorizationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                authorization_config_property = appsync.CfnDataSource.AuthorizationConfigProperty(
                    authorization_type="authorizationType",
                
                    # the properties below are optional
                    aws_iam_config=appsync.CfnDataSource.AwsIamConfigProperty(
                        signing_region="signingRegion",
                        signing_service_name="signingServiceName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b04dfa1d3d91eafb88eb48c7ef694b6cbd4533734a9ce44a5c8efab25e52af5)
                check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
                check_type(argname="argument aws_iam_config", value=aws_iam_config, expected_type=type_hints["aws_iam_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "authorization_type": authorization_type,
            }
            if aws_iam_config is not None:
                self._values["aws_iam_config"] = aws_iam_config

        @builtins.property
        def authorization_type(self) -> builtins.str:
            '''The authorization type that the HTTP endpoint requires.

            - *AWS_IAM* : The authorization type is Signature Version 4 (SigV4).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-authorizationconfig.html#cfn-appsync-datasource-authorizationconfig-authorizationtype
            '''
            result = self._values.get("authorization_type")
            assert result is not None, "Required property 'authorization_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def aws_iam_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.AwsIamConfigProperty", _IResolvable_a771d0ef]]:
            '''The AWS Identity and Access Management settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-authorizationconfig.html#cfn-appsync-datasource-authorizationconfig-awsiamconfig
            '''
            result = self._values.get("aws_iam_config")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.AwsIamConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.AwsIamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "signing_region": "signingRegion",
            "signing_service_name": "signingServiceName",
        },
    )
    class AwsIamConfigProperty:
        def __init__(
            self,
            *,
            signing_region: typing.Optional[builtins.str] = None,
            signing_service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``AwsIamConfig`` property type to specify ``AwsIamConfig`` for a AWS AppSync authorizaton.

            ``AwsIamConfig`` is a property of the `AWS AppSync DataSource AuthorizationConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig-authorizationconfig.html>`_ resource.

            :param signing_region: The signing Region for AWS Identity and Access Management authorization.
            :param signing_service_name: The signing service name for AWS Identity and Access Management authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-awsiamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                aws_iam_config_property = appsync.CfnDataSource.AwsIamConfigProperty(
                    signing_region="signingRegion",
                    signing_service_name="signingServiceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51d025a9f69b375ff9c14b4025695a09b43cad87f47cc54b86afe2abdccc82cb)
                check_type(argname="argument signing_region", value=signing_region, expected_type=type_hints["signing_region"])
                check_type(argname="argument signing_service_name", value=signing_service_name, expected_type=type_hints["signing_service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if signing_region is not None:
                self._values["signing_region"] = signing_region
            if signing_service_name is not None:
                self._values["signing_service_name"] = signing_service_name

        @builtins.property
        def signing_region(self) -> typing.Optional[builtins.str]:
            '''The signing Region for AWS Identity and Access Management authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-awsiamconfig.html#cfn-appsync-datasource-awsiamconfig-signingregion
            '''
            result = self._values.get("signing_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signing_service_name(self) -> typing.Optional[builtins.str]:
            '''The signing service name for AWS Identity and Access Management authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-awsiamconfig.html#cfn-appsync-datasource-awsiamconfig-signingservicename
            '''
            result = self._values.get("signing_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsIamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.DeltaSyncConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_table_ttl": "baseTableTtl",
            "delta_sync_table_name": "deltaSyncTableName",
            "delta_sync_table_ttl": "deltaSyncTableTtl",
        },
    )
    class DeltaSyncConfigProperty:
        def __init__(
            self,
            *,
            base_table_ttl: builtins.str,
            delta_sync_table_name: builtins.str,
            delta_sync_table_ttl: builtins.str,
        ) -> None:
            '''Describes a Delta Sync configuration.

            :param base_table_ttl: The number of minutes that an Item is stored in the data source.
            :param delta_sync_table_name: The Delta Sync table name.
            :param delta_sync_table_ttl: The number of minutes that a Delta Sync log entry is stored in the Delta Sync table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                delta_sync_config_property = appsync.CfnDataSource.DeltaSyncConfigProperty(
                    base_table_ttl="baseTableTtl",
                    delta_sync_table_name="deltaSyncTableName",
                    delta_sync_table_ttl="deltaSyncTableTtl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__002fefce098119d7807f102bfb8fa5cb58a916dfea56d346c62a00b9f2229787)
                check_type(argname="argument base_table_ttl", value=base_table_ttl, expected_type=type_hints["base_table_ttl"])
                check_type(argname="argument delta_sync_table_name", value=delta_sync_table_name, expected_type=type_hints["delta_sync_table_name"])
                check_type(argname="argument delta_sync_table_ttl", value=delta_sync_table_ttl, expected_type=type_hints["delta_sync_table_ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "base_table_ttl": base_table_ttl,
                "delta_sync_table_name": delta_sync_table_name,
                "delta_sync_table_ttl": delta_sync_table_ttl,
            }

        @builtins.property
        def base_table_ttl(self) -> builtins.str:
            '''The number of minutes that an Item is stored in the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html#cfn-appsync-datasource-deltasyncconfig-basetablettl
            '''
            result = self._values.get("base_table_ttl")
            assert result is not None, "Required property 'base_table_ttl' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def delta_sync_table_name(self) -> builtins.str:
            '''The Delta Sync table name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html#cfn-appsync-datasource-deltasyncconfig-deltasynctablename
            '''
            result = self._values.get("delta_sync_table_name")
            assert result is not None, "Required property 'delta_sync_table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def delta_sync_table_ttl(self) -> builtins.str:
            '''The number of minutes that a Delta Sync log entry is stored in the Delta Sync table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-deltasyncconfig.html#cfn-appsync-datasource-deltasyncconfig-deltasynctablettl
            '''
            result = self._values.get("delta_sync_table_ttl")
            assert result is not None, "Required property 'delta_sync_table_ttl' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeltaSyncConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.DynamoDBConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_region": "awsRegion",
            "table_name": "tableName",
            "delta_sync_config": "deltaSyncConfig",
            "use_caller_credentials": "useCallerCredentials",
            "versioned": "versioned",
        },
    )
    class DynamoDBConfigProperty:
        def __init__(
            self,
            *,
            aws_region: builtins.str,
            table_name: builtins.str,
            delta_sync_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.DeltaSyncConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            versioned: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``DynamoDBConfig`` property type specifies the ``AwsRegion`` and ``TableName`` for an Amazon DynamoDB table in your account for an AWS AppSync data source.

            ``DynamoDBConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param aws_region: The AWS Region.
            :param table_name: The table name.
            :param delta_sync_config: The ``DeltaSyncConfig`` for a versioned datasource.
            :param use_caller_credentials: Set to ``TRUE`` to use AWS Identity and Access Management with this data source.
            :param versioned: Set to TRUE to use Conflict Detection and Resolution with this data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                dynamo_dBConfig_property = appsync.CfnDataSource.DynamoDBConfigProperty(
                    aws_region="awsRegion",
                    table_name="tableName",
                
                    # the properties below are optional
                    delta_sync_config=appsync.CfnDataSource.DeltaSyncConfigProperty(
                        base_table_ttl="baseTableTtl",
                        delta_sync_table_name="deltaSyncTableName",
                        delta_sync_table_ttl="deltaSyncTableTtl"
                    ),
                    use_caller_credentials=False,
                    versioned=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67f8bcd36bc52d321d0e2ef8d97d7f1d4747fe5cd92c0f4c75efc16a9cb62e93)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument delta_sync_config", value=delta_sync_config, expected_type=type_hints["delta_sync_config"])
                check_type(argname="argument use_caller_credentials", value=use_caller_credentials, expected_type=type_hints["use_caller_credentials"])
                check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "aws_region": aws_region,
                "table_name": table_name,
            }
            if delta_sync_config is not None:
                self._values["delta_sync_config"] = delta_sync_config
            if use_caller_credentials is not None:
                self._values["use_caller_credentials"] = use_caller_credentials
            if versioned is not None:
                self._values["versioned"] = versioned

        @builtins.property
        def aws_region(self) -> builtins.str:
            '''The AWS Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-awsregion
            '''
            result = self._values.get("aws_region")
            assert result is not None, "Required property 'aws_region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''The table name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def delta_sync_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DeltaSyncConfigProperty", _IResolvable_a771d0ef]]:
            '''The ``DeltaSyncConfig`` for a versioned datasource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-deltasyncconfig
            '''
            result = self._values.get("delta_sync_config")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DeltaSyncConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def use_caller_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Set to ``TRUE`` to use AWS Identity and Access Management with this data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-usecallercredentials
            '''
            result = self._values.get("use_caller_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def versioned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Set to TRUE to use Conflict Detection and Resolution with this data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-dynamodbconfig.html#cfn-appsync-datasource-dynamodbconfig-versioned
            '''
            result = self._values.get("versioned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.ElasticsearchConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_region": "awsRegion", "endpoint": "endpoint"},
    )
    class ElasticsearchConfigProperty:
        def __init__(self, *, aws_region: builtins.str, endpoint: builtins.str) -> None:
            '''The ``ElasticsearchConfig`` property type specifies the ``AwsRegion`` and ``Endpoints`` for an Amazon OpenSearch Service domain in your account for an AWS AppSync data source.

            ElasticsearchConfig is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            As of September 2021, Amazon Elasticsearch Service is Amazon OpenSearch Service . This property is deprecated. For new data sources, use *OpenSearchServiceConfig* to specify an OpenSearch Service data source.

            :param aws_region: The AWS Region.
            :param endpoint: The endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-elasticsearchconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                elasticsearch_config_property = appsync.CfnDataSource.ElasticsearchConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a472816ee8b6c7c75479bacb28bc57db1828bc476a2bf694128b1b777719e1d3)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "aws_region": aws_region,
                "endpoint": endpoint,
            }

        @builtins.property
        def aws_region(self) -> builtins.str:
            '''The AWS Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-elasticsearchconfig.html#cfn-appsync-datasource-elasticsearchconfig-awsregion
            '''
            result = self._values.get("aws_region")
            assert result is not None, "Required property 'aws_region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''The endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-elasticsearchconfig.html#cfn-appsync-datasource-elasticsearchconfig-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.HttpConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "authorization_config": "authorizationConfig",
        },
    )
    class HttpConfigProperty:
        def __init__(
            self,
            *,
            endpoint: builtins.str,
            authorization_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.AuthorizationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Use the ``HttpConfig`` property type to specify ``HttpConfig`` for an AWS AppSync data source.

            ``HttpConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ resource.

            :param endpoint: The endpoint.
            :param authorization_config: The authorization configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                http_config_property = appsync.CfnDataSource.HttpConfigProperty(
                    endpoint="endpoint",
                
                    # the properties below are optional
                    authorization_config=appsync.CfnDataSource.AuthorizationConfigProperty(
                        authorization_type="authorizationType",
                
                        # the properties below are optional
                        aws_iam_config=appsync.CfnDataSource.AwsIamConfigProperty(
                            signing_region="signingRegion",
                            signing_service_name="signingServiceName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a45b64328df1caa2ec1d85914400d158de5cc8a49d343fa665511e730682cc30)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint": endpoint,
            }
            if authorization_config is not None:
                self._values["authorization_config"] = authorization_config

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''The endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html#cfn-appsync-datasource-httpconfig-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authorization_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.AuthorizationConfigProperty", _IResolvable_a771d0ef]]:
            '''The authorization configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-httpconfig.html#cfn-appsync-datasource-httpconfig-authorizationconfig
            '''
            result = self._values.get("authorization_config")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.AuthorizationConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.LambdaConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_function_arn": "lambdaFunctionArn"},
    )
    class LambdaConfigProperty:
        def __init__(self, *, lambda_function_arn: builtins.str) -> None:
            '''The ``LambdaConfig`` property type specifies the Lambda function ARN for an AWS AppSync data source.

            ``LambdaConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param lambda_function_arn: The ARN for the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-lambdaconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                lambda_config_property = appsync.CfnDataSource.LambdaConfigProperty(
                    lambda_function_arn="lambdaFunctionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cbb038aa1971a0c3704f0ae253d7789ed9fac53b2b16587aa39b5272a567810)
                check_type(argname="argument lambda_function_arn", value=lambda_function_arn, expected_type=type_hints["lambda_function_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_function_arn": lambda_function_arn,
            }

        @builtins.property
        def lambda_function_arn(self) -> builtins.str:
            '''The ARN for the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-lambdaconfig.html#cfn-appsync-datasource-lambdaconfig-lambdafunctionarn
            '''
            result = self._values.get("lambda_function_arn")
            assert result is not None, "Required property 'lambda_function_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.OpenSearchServiceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_region": "awsRegion", "endpoint": "endpoint"},
    )
    class OpenSearchServiceConfigProperty:
        def __init__(self, *, aws_region: builtins.str, endpoint: builtins.str) -> None:
            '''The ``OpenSearchServiceConfig`` property type specifies the ``AwsRegion`` and ``Endpoints`` for an Amazon OpenSearch Service domain in your account for an AWS AppSync data source.

            ``OpenSearchServiceConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param aws_region: The AWS Region.
            :param endpoint: The endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-opensearchserviceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                open_search_service_config_property = appsync.CfnDataSource.OpenSearchServiceConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e3cf1b5f592283a36a78887e4c15e61657749972d80ff310698e9451ba6f3da)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "aws_region": aws_region,
                "endpoint": endpoint,
            }

        @builtins.property
        def aws_region(self) -> builtins.str:
            '''The AWS Region.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-opensearchserviceconfig.html#cfn-appsync-datasource-opensearchserviceconfig-awsregion
            '''
            result = self._values.get("aws_region")
            assert result is not None, "Required property 'aws_region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def endpoint(self) -> builtins.str:
            '''The endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-opensearchserviceconfig.html#cfn-appsync-datasource-opensearchserviceconfig-endpoint
            '''
            result = self._values.get("endpoint")
            assert result is not None, "Required property 'endpoint' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenSearchServiceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.RdsHttpEndpointConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_region": "awsRegion",
            "aws_secret_store_arn": "awsSecretStoreArn",
            "db_cluster_identifier": "dbClusterIdentifier",
            "database_name": "databaseName",
            "schema": "schema",
        },
    )
    class RdsHttpEndpointConfigProperty:
        def __init__(
            self,
            *,
            aws_region: builtins.str,
            aws_secret_store_arn: builtins.str,
            db_cluster_identifier: builtins.str,
            database_name: typing.Optional[builtins.str] = None,
            schema: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``RdsHttpEndpointConfig`` property type to specify the ``RdsHttpEndpoint`` for an AWS AppSync relational database.

            ``RdsHttpEndpointConfig`` is a property of the `AWS AppSync DataSource RelationalDatabaseConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html>`_ resource.

            :param aws_region: AWS Region for RDS HTTP endpoint.
            :param aws_secret_store_arn: The ARN for database credentials stored in AWS Secrets Manager .
            :param db_cluster_identifier: Amazon RDS cluster Amazon Resource Name (ARN).
            :param database_name: Logical database name.
            :param schema: Logical schema name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                rds_http_endpoint_config_property = appsync.CfnDataSource.RdsHttpEndpointConfigProperty(
                    aws_region="awsRegion",
                    aws_secret_store_arn="awsSecretStoreArn",
                    db_cluster_identifier="dbClusterIdentifier",
                
                    # the properties below are optional
                    database_name="databaseName",
                    schema="schema"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ab254f472dedea9a2341a5f1a0201694d5f07e35405db2366d53837c7ee7e5e)
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument aws_secret_store_arn", value=aws_secret_store_arn, expected_type=type_hints["aws_secret_store_arn"])
                check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "aws_region": aws_region,
                "aws_secret_store_arn": aws_secret_store_arn,
                "db_cluster_identifier": db_cluster_identifier,
            }
            if database_name is not None:
                self._values["database_name"] = database_name
            if schema is not None:
                self._values["schema"] = schema

        @builtins.property
        def aws_region(self) -> builtins.str:
            '''AWS Region for RDS HTTP endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-awsregion
            '''
            result = self._values.get("aws_region")
            assert result is not None, "Required property 'aws_region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def aws_secret_store_arn(self) -> builtins.str:
            '''The ARN for database credentials stored in AWS Secrets Manager .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-awssecretstorearn
            '''
            result = self._values.get("aws_secret_store_arn")
            assert result is not None, "Required property 'aws_secret_store_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def db_cluster_identifier(self) -> builtins.str:
            '''Amazon RDS cluster Amazon Resource Name (ARN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-dbclusteridentifier
            '''
            result = self._values.get("db_cluster_identifier")
            assert result is not None, "Required property 'db_cluster_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''Logical database name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema(self) -> typing.Optional[builtins.str]:
            '''Logical schema name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-rdshttpendpointconfig.html#cfn-appsync-datasource-rdshttpendpointconfig-schema
            '''
            result = self._values.get("schema")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RdsHttpEndpointConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnDataSource.RelationalDatabaseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relational_database_source_type": "relationalDatabaseSourceType",
            "rds_http_endpoint_config": "rdsHttpEndpointConfig",
        },
    )
    class RelationalDatabaseConfigProperty:
        def __init__(
            self,
            *,
            relational_database_source_type: builtins.str,
            rds_http_endpoint_config: typing.Optional[typing.Union[typing.Union["CfnDataSource.RdsHttpEndpointConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Use the ``RelationalDatabaseConfig`` property type to specify ``RelationalDatabaseConfig`` for an AWS AppSync data source.

            ``RelationalDatabaseConfig`` is a property of the `AWS::AppSync::DataSource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html>`_ property type.

            :param relational_database_source_type: The type of relational data source.
            :param rds_http_endpoint_config: Information about the Amazon RDS resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                relational_database_config_property = appsync.CfnDataSource.RelationalDatabaseConfigProperty(
                    relational_database_source_type="relationalDatabaseSourceType",
                
                    # the properties below are optional
                    rds_http_endpoint_config=appsync.CfnDataSource.RdsHttpEndpointConfigProperty(
                        aws_region="awsRegion",
                        aws_secret_store_arn="awsSecretStoreArn",
                        db_cluster_identifier="dbClusterIdentifier",
                
                        # the properties below are optional
                        database_name="databaseName",
                        schema="schema"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__936196738212b36f5ede32936516ef8771c3006966d5c21c86c03c0d1b6b6508)
                check_type(argname="argument relational_database_source_type", value=relational_database_source_type, expected_type=type_hints["relational_database_source_type"])
                check_type(argname="argument rds_http_endpoint_config", value=rds_http_endpoint_config, expected_type=type_hints["rds_http_endpoint_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "relational_database_source_type": relational_database_source_type,
            }
            if rds_http_endpoint_config is not None:
                self._values["rds_http_endpoint_config"] = rds_http_endpoint_config

        @builtins.property
        def relational_database_source_type(self) -> builtins.str:
            '''The type of relational data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html#cfn-appsync-datasource-relationaldatabaseconfig-relationaldatabasesourcetype
            '''
            result = self._values.get("relational_database_source_type")
            assert result is not None, "Required property 'relational_database_source_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rds_http_endpoint_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.RdsHttpEndpointConfigProperty", _IResolvable_a771d0ef]]:
            '''Information about the Amazon RDS resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-datasource-relationaldatabaseconfig.html#cfn-appsync-datasource-relationaldatabaseconfig-rdshttpendpointconfig
            '''
            result = self._values.get("rds_http_endpoint_config")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.RdsHttpEndpointConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationalDatabaseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnDataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "name": "name",
        "type": "type",
        "description": "description",
        "dynamo_db_config": "dynamoDbConfig",
        "elasticsearch_config": "elasticsearchConfig",
        "http_config": "httpConfig",
        "lambda_config": "lambdaConfig",
        "open_search_service_config": "openSearchServiceConfig",
        "relational_database_config": "relationalDatabaseConfig",
        "service_role_arn": "serviceRoleArn",
    },
)
class CfnDataSourceProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataSource``.

        :param api_id: Unique AWS AppSync GraphQL API identifier where this data source will be created.
        :param name: Friendly name for you to identify your AppSync data source after creation.
        :param type: The type of the data source. - *AWS_LAMBDA* : The data source is an AWS Lambda function. - *AMAZON_DYNAMODB* : The data source is an Amazon DynamoDB table. - *AMAZON_ELASTICSEARCH* : The data source is an Amazon OpenSearch Service domain. - *AMAZON_OPENSEARCH_SERVICE* : The data source is an Amazon OpenSearch Service domain. - *NONE* : There is no data source. This type is used when you wish to invoke a GraphQL operation without connecting to a data source, such as performing data transformation with resolvers or triggering a subscription to be invoked from a mutation. - *HTTP* : The data source is an HTTP endpoint. - *RELATIONAL_DATABASE* : The data source is a relational database.
        :param description: The description of the data source.
        :param dynamo_db_config: AWS Region and TableName for an Amazon DynamoDB table in your account.
        :param elasticsearch_config: AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account. As of September 2021, Amazon Elasticsearch Service is Amazon OpenSearch Service . This property is deprecated. For new data sources, use *OpenSearchServiceConfig* to specify an OpenSearch Service data source.
        :param http_config: Endpoints for an HTTP data source.
        :param lambda_config: An ARN of a Lambda function in valid ARN format. This can be the ARN of a Lambda function that exists in the current account or in another account.
        :param open_search_service_config: AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.
        :param relational_database_config: Relational Database configuration of the relational database data source.
        :param service_role_arn: The AWS Identity and Access Management service role ARN for the data source. The system assumes this role when accessing the data source. Required if ``Type`` is specified as ``AWS_LAMBDA`` , ``AMAZON_DYNAMODB`` , ``AMAZON_ELASTICSEARCH`` , or ``AMAZON_OPENSEARCH_SERVICE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_data_source_props = appsync.CfnDataSourceProps(
                api_id="apiId",
                name="name",
                type="type",
            
                # the properties below are optional
                description="description",
                dynamo_db_config=appsync.CfnDataSource.DynamoDBConfigProperty(
                    aws_region="awsRegion",
                    table_name="tableName",
            
                    # the properties below are optional
                    delta_sync_config=appsync.CfnDataSource.DeltaSyncConfigProperty(
                        base_table_ttl="baseTableTtl",
                        delta_sync_table_name="deltaSyncTableName",
                        delta_sync_table_ttl="deltaSyncTableTtl"
                    ),
                    use_caller_credentials=False,
                    versioned=False
                ),
                elasticsearch_config=appsync.CfnDataSource.ElasticsearchConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                ),
                http_config=appsync.CfnDataSource.HttpConfigProperty(
                    endpoint="endpoint",
            
                    # the properties below are optional
                    authorization_config=appsync.CfnDataSource.AuthorizationConfigProperty(
                        authorization_type="authorizationType",
            
                        # the properties below are optional
                        aws_iam_config=appsync.CfnDataSource.AwsIamConfigProperty(
                            signing_region="signingRegion",
                            signing_service_name="signingServiceName"
                        )
                    )
                ),
                lambda_config=appsync.CfnDataSource.LambdaConfigProperty(
                    lambda_function_arn="lambdaFunctionArn"
                ),
                open_search_service_config=appsync.CfnDataSource.OpenSearchServiceConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                ),
                relational_database_config=appsync.CfnDataSource.RelationalDatabaseConfigProperty(
                    relational_database_source_type="relationalDatabaseSourceType",
            
                    # the properties below are optional
                    rds_http_endpoint_config=appsync.CfnDataSource.RdsHttpEndpointConfigProperty(
                        aws_region="awsRegion",
                        aws_secret_store_arn="awsSecretStoreArn",
                        db_cluster_identifier="dbClusterIdentifier",
            
                        # the properties below are optional
                        database_name="databaseName",
                        schema="schema"
                    )
                ),
                service_role_arn="serviceRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461cab08db471753f15462f9f788c8833450b644b1e7837a0fe7d3b7014f4164)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamo_db_config", value=dynamo_db_config, expected_type=type_hints["dynamo_db_config"])
            check_type(argname="argument elasticsearch_config", value=elasticsearch_config, expected_type=type_hints["elasticsearch_config"])
            check_type(argname="argument http_config", value=http_config, expected_type=type_hints["http_config"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            check_type(argname="argument open_search_service_config", value=open_search_service_config, expected_type=type_hints["open_search_service_config"])
            check_type(argname="argument relational_database_config", value=relational_database_config, expected_type=type_hints["relational_database_config"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if dynamo_db_config is not None:
            self._values["dynamo_db_config"] = dynamo_db_config
        if elasticsearch_config is not None:
            self._values["elasticsearch_config"] = elasticsearch_config
        if http_config is not None:
            self._values["http_config"] = http_config
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if open_search_service_config is not None:
            self._values["open_search_service_config"] = open_search_service_config
        if relational_database_config is not None:
            self._values["relational_database_config"] = relational_database_config
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn

    @builtins.property
    def api_id(self) -> builtins.str:
        '''Unique AWS AppSync GraphQL API identifier where this data source will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Friendly name for you to identify your AppSync data source after creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the data source.

        - *AWS_LAMBDA* : The data source is an AWS Lambda function.
        - *AMAZON_DYNAMODB* : The data source is an Amazon DynamoDB table.
        - *AMAZON_ELASTICSEARCH* : The data source is an Amazon OpenSearch Service domain.
        - *AMAZON_OPENSEARCH_SERVICE* : The data source is an Amazon OpenSearch Service domain.
        - *NONE* : There is no data source. This type is used when you wish to invoke a GraphQL operation without connecting to a data source, such as performing data transformation with resolvers or triggering a subscription to be invoked from a mutation.
        - *HTTP* : The data source is an HTTP endpoint.
        - *RELATIONAL_DATABASE* : The data source is a relational database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamo_db_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.DynamoDBConfigProperty, _IResolvable_a771d0ef]]:
        '''AWS Region and TableName for an Amazon DynamoDB table in your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-dynamodbconfig
        '''
        result = self._values.get("dynamo_db_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.DynamoDBConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def elasticsearch_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.ElasticsearchConfigProperty, _IResolvable_a771d0ef]]:
        '''AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.

        As of September 2021, Amazon Elasticsearch Service is Amazon OpenSearch Service . This property is deprecated. For new data sources, use *OpenSearchServiceConfig* to specify an OpenSearch Service data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-elasticsearchconfig
        '''
        result = self._values.get("elasticsearch_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.ElasticsearchConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def http_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.HttpConfigProperty, _IResolvable_a771d0ef]]:
        '''Endpoints for an HTTP data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-httpconfig
        '''
        result = self._values.get("http_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.HttpConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.LambdaConfigProperty, _IResolvable_a771d0ef]]:
        '''An ARN of a Lambda function in valid ARN format.

        This can be the ARN of a Lambda function that exists in the current account or in another account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-lambdaconfig
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.LambdaConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def open_search_service_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, _IResolvable_a771d0ef]]:
        '''AWS Region and Endpoints for an Amazon OpenSearch Service domain in your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-opensearchserviceconfig
        '''
        result = self._values.get("open_search_service_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def relational_database_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, _IResolvable_a771d0ef]]:
        '''Relational Database configuration of the relational database data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-relationaldatabaseconfig
        '''
        result = self._values.get("relational_database_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management service role ARN for the data source.

        The system assumes this role when accessing the data source.

        Required if ``Type`` is specified as ``AWS_LAMBDA`` , ``AMAZON_DYNAMODB`` , ``AMAZON_ELASTICSEARCH`` , or ``AMAZON_OPENSEARCH_SERVICE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-datasource.html#cfn-appsync-datasource-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDomainName(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnDomainName",
):
    '''A CloudFormation ``AWS::AppSync::DomainName``.

    The ``AWS::AppSync::DomainName`` resource creates a ``DomainNameConfig`` object to configure a custom domain.

    :cloudformationResource: AWS::AppSync::DomainName
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_domain_name = appsync.CfnDomainName(self, "MyCfnDomainName",
            certificate_arn="certificateArn",
            domain_name="domainName",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        certificate_arn: builtins.str,
        domain_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::DomainName``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_arn: The Amazon Resource Name (ARN) of the certificate. This will be an AWS Certificate Manager certificate.
        :param domain_name: The domain name.
        :param description: The decription for your domain name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cd07ce7fc54ba9e3dec979c1d5e3e74a4b14ee1b7a55ba57cd2786c4f8ff07)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainNameProps(
            certificate_arn=certificate_arn,
            domain_name=domain_name,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3eee087600f3f00e81f4316ee26dcb291017a979c85649fff8e8d1c5a88b3aa)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a9c9a505716d85401effc76de7f028562c88ad8430a224e9c2f2e8443e71e0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppSyncDomainName")
    def attr_app_sync_domain_name(self) -> builtins.str:
        '''The domain name provided by AWS AppSync .

        :cloudformationAttribute: AppSyncDomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppSyncDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''The domain name.

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrHostedZoneId")
    def attr_hosted_zone_id(self) -> builtins.str:
        '''The ID of your Amazon Route 53 hosted zone.

        :cloudformationAttribute: HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the certificate.

        This will be an AWS Certificate Manager certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-certificatearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c267cc3ec351886e5b4b9eeb8f59b49c0bb00f1e753df2edc2c6e6f40f8bbc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bff469b1d6803182249cce539b2c5279ffc69e719d87a4569fe99096c32e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The decription for your domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e74c052fcbe0e208df2030185d3233fafabed6a6eaa09a148d38dae8c3cb63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnDomainNameApiAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnDomainNameApiAssociation",
):
    '''A CloudFormation ``AWS::AppSync::DomainNameApiAssociation``.

    The ``AWS::AppSync::DomainNameApiAssociation`` resource represents the mapping of your custom domain name to the assigned API URL.

    :cloudformationResource: AWS::AppSync::DomainNameApiAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_domain_name_api_association = appsync.CfnDomainNameApiAssociation(self, "MyCfnDomainNameApiAssociation",
            api_id="apiId",
            domain_name="domainName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_id: builtins.str,
        domain_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::AppSync::DomainNameApiAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The API ID.
        :param domain_name: The domain name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c111e17fdda67e1c931c1f91d860a523db0d11880404cf6c2ec4c888aceca5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainNameApiAssociationProps(
            api_id=api_id, domain_name=domain_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ce9d260f40f2cd1aa34b0d19210955a0b9b72ffcb87800a2d09c3ccfb23de3)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad77bfa6625db42cda10ee139bf625764e4bbd484792ebecbcc62fb585f3412)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApiAssociationIdentifier")
    def attr_api_association_identifier(self) -> builtins.str:
        '''
        :cloudformationAttribute: ApiAssociationIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApiAssociationIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The API ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html#cfn-appsync-domainnameapiassociation-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c124f6029727b6a0b445ccb4575dc8305afd5502a0cbaf5dda768b49255a7c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html#cfn-appsync-domainnameapiassociation-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1770662fa786f424d1da34acf174df57b58b1e5a095a19a8dba52dfc6085bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnDomainNameApiAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"api_id": "apiId", "domain_name": "domainName"},
)
class CfnDomainNameApiAssociationProps:
    def __init__(self, *, api_id: builtins.str, domain_name: builtins.str) -> None:
        '''Properties for defining a ``CfnDomainNameApiAssociation``.

        :param api_id: The API ID.
        :param domain_name: The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_domain_name_api_association_props = appsync.CfnDomainNameApiAssociationProps(
                api_id="apiId",
                domain_name="domainName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca963d0664c8ef45159b15ac49f48257a8d94428fd34cec32c455123b8c1bb8)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
            "domain_name": domain_name,
        }

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The API ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html#cfn-appsync-domainnameapiassociation-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainnameapiassociation.html#cfn-appsync-domainnameapiassociation-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameApiAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnDomainNameProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "domain_name": "domainName",
        "description": "description",
    },
)
class CfnDomainNameProps:
    def __init__(
        self,
        *,
        certificate_arn: builtins.str,
        domain_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomainName``.

        :param certificate_arn: The Amazon Resource Name (ARN) of the certificate. This will be an AWS Certificate Manager certificate.
        :param domain_name: The domain name.
        :param description: The decription for your domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_domain_name_props = appsync.CfnDomainNameProps(
                certificate_arn="certificateArn",
                domain_name="domainName",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de883ad249a4b3579f2993df07f3b93b5a7aadb0c35d5a58eebf43ae3e8a2b2e)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate_arn": certificate_arn,
            "domain_name": domain_name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def certificate_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the certificate.

        This will be an AWS Certificate Manager certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-certificatearn
        '''
        result = self._values.get("certificate_arn")
        assert result is not None, "Required property 'certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The decription for your domain name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-domainname.html#cfn-appsync-domainname-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFunctionConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnFunctionConfiguration",
):
    '''A CloudFormation ``AWS::AppSync::FunctionConfiguration``.

    The ``AWS::AppSync::FunctionConfiguration`` resource defines the functions in GraphQL APIs to perform certain operations. You can use pipeline resolvers to attach functions. For more information, see `Pipeline Resolvers <https://docs.aws.amazon.com/appsync/latest/devguide/pipeline-resolvers.html>`_ in the *AWS AppSync Developer Guide* .
    .. epigraph::

       When you submit an update, AWS CloudFormation updates resources based on differences between what you submit and the stack's current template. To cause this resource to be updated you must change a property value for this resource in the AWS CloudFormation template. Changing the Amazon S3 file content without changing a property value will not result in an update operation.

       See `Update Behaviors of Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html>`_ in the *AWS CloudFormation User Guide* .

    :cloudformationResource: AWS::AppSync::FunctionConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_function_configuration = appsync.CfnFunctionConfiguration(self, "MyCfnFunctionConfiguration",
            api_id="apiId",
            data_source_name="dataSourceName",
            name="name",
        
            # the properties below are optional
            code="code",
            code_s3_location="codeS3Location",
            description="description",
            function_version="functionVersion",
            max_batch_size=123,
            request_mapping_template="requestMappingTemplate",
            request_mapping_template_s3_location="requestMappingTemplateS3Location",
            response_mapping_template="responseMappingTemplate",
            response_mapping_template_s3_location="responseMappingTemplateS3Location",
            runtime=appsync.CfnFunctionConfiguration.AppSyncRuntimeProperty(
                name="name",
                runtime_version="runtimeVersion"
            ),
            sync_config=appsync.CfnFunctionConfiguration.SyncConfigProperty(
                conflict_detection="conflictDetection",
        
                # the properties below are optional
                conflict_handler="conflictHandler",
                lambda_conflict_handler_config=appsync.CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_id: builtins.str,
        data_source_name: builtins.str,
        name: builtins.str,
        code: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        function_version: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union[typing.Union["CfnFunctionConfiguration.AppSyncRuntimeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sync_config: typing.Optional[typing.Union[typing.Union["CfnFunctionConfiguration.SyncConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::FunctionConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The AWS AppSync GraphQL API that you want to attach using this function.
        :param data_source_name: The name of data source this function will attach.
        :param name: The name of the function.
        :param code: The ``resolver`` code that contains the request and response functions. When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .
        :param code_s3_location: The Amazon S3 endpoint.
        :param description: The ``Function`` description.
        :param function_version: The version of the request mapping template. Currently, only the 2018-05-29 version of the template is supported.
        :param max_batch_size: The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.
        :param request_mapping_template: The ``Function`` request mapping template. Functions support only the 2018-05-29 version of the request mapping template.
        :param request_mapping_template_s3_location: Describes a Sync configuration for a resolver. Contains information on which Conflict Detection, as well as Resolution strategy, should be performed when the resolver is invoked.
        :param response_mapping_template: The ``Function`` response mapping template.
        :param response_mapping_template_s3_location: The location of a response mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param runtime: Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function. Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.
        :param sync_config: Describes a Sync configuration for a resolver. Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97bd9bb1b61f79670b1ed1114a848ff51681eec780bc37428f72c52aa883e747)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFunctionConfigurationProps(
            api_id=api_id,
            data_source_name=data_source_name,
            name=name,
            code=code,
            code_s3_location=code_s3_location,
            description=description,
            function_version=function_version,
            max_batch_size=max_batch_size,
            request_mapping_template=request_mapping_template,
            request_mapping_template_s3_location=request_mapping_template_s3_location,
            response_mapping_template=response_mapping_template,
            response_mapping_template_s3_location=response_mapping_template_s3_location,
            runtime=runtime,
            sync_config=sync_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3b6ec2a694b35ffad067487492cda5beb79ba200ec410e19f519d71af17c0b)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f24e127821dd346004d39a1efba46ac7d62aaf3d363378ca7c9e1b61b808c5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDataSourceName")
    def attr_data_source_name(self) -> builtins.str:
        '''The name of data source this function will attach.

        :cloudformationAttribute: DataSourceName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDataSourceName"))

    @builtins.property
    @jsii.member(jsii_name="attrFunctionArn")
    def attr_function_arn(self) -> builtins.str:
        '''ARN of the function, such as ``arn:aws:appsync:us-east-1:123456789012:apis/graphqlapiid/functions/functionId`` .

        :cloudformationAttribute: FunctionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFunctionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFunctionId")
    def attr_function_id(self) -> builtins.str:
        '''The unique ID of this function.

        :cloudformationAttribute: FunctionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFunctionId"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the function.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The AWS AppSync GraphQL API that you want to attach using this function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78bb957d663d1d39f00f13fbc901555000f7b0332e130db9e63ddbbed7d665dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> builtins.str:
        '''The name of data source this function will attach.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-datasourcename
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSourceName"))

    @data_source_name.setter
    def data_source_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1341d085dcc76845871aa81af959a7788b4aed86125ce330817eee2c71a8ef92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceName", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44c5a3148a15daf6a594239e797a7f886e5a93a805dd6d33ed1c0bfed01d2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Optional[builtins.str]:
        '''The ``resolver`` code that contains the request and response functions.

        When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-code
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "code"))

    @code.setter
    def code(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02915802665709262323ce978beb957c80d72af0f58b6864ee51e58545fcac28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="codeS3Location")
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-codes3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeS3Location"))

    @code_s3_location.setter
    def code_s3_location(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f8aac15079b7ac9392331252791ce0d2ea519b145656031761510e435f10cf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c3d54d2f65363df2dc9af80783095b037ee81f80feba1e48380ac20834c1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> typing.Optional[builtins.str]:
        '''The version of the request mapping template.

        Currently, only the 2018-05-29 version of the template is supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-functionversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionVersion"))

    @function_version.setter
    def function_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0ce90d61e318cc3eec7044646937dbb8039e154ebc210821ccdb96604a5d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionVersion", value)

    @builtins.property
    @jsii.member(jsii_name="maxBatchSize")
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-maxbatchsize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBatchSize"))

    @max_batch_size.setter
    def max_batch_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319926703ac6061bb489cb76e2182b222bd5ff5ff6d8ef7b6b06988a7513778e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBatchSize", value)

    @builtins.property
    @jsii.member(jsii_name="requestMappingTemplate")
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` request mapping template.

        Functions support only the 2018-05-29 version of the request mapping template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-requestmappingtemplate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMappingTemplate"))

    @request_mapping_template.setter
    def request_mapping_template(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60367dc0631edac129464090fc5e0867c79f85c3f088cc2378c5c3a885d6c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMappingTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="requestMappingTemplateS3Location")
    def request_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''Describes a Sync configuration for a resolver.

        Contains information on which Conflict Detection, as well as Resolution strategy, should be performed when the resolver is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-requestmappingtemplates3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMappingTemplateS3Location"))

    @request_mapping_template_s3_location.setter
    def request_mapping_template_s3_location(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bf6e51f32f74b30ee9cc9f0384b6f617158693b54331598af151ba71572e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMappingTemplateS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="responseMappingTemplate")
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` response mapping template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-responsemappingtemplate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseMappingTemplate"))

    @response_mapping_template.setter
    def response_mapping_template(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3611601d262ec76de13659423e6cfa7bcfe6efb1e78e5695f517403554ba38ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMappingTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="responseMappingTemplateS3Location")
    def response_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a response mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-responsemappingtemplates3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseMappingTemplateS3Location"))

    @response_mapping_template_s3_location.setter
    def response_mapping_template_s3_location(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c50c4ea79818a708468afe01cf755b7c2bc1f9f8f4c683ad4dcd6683524cfe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMappingTemplateS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(
        self,
    ) -> typing.Optional[typing.Union["CfnFunctionConfiguration.AppSyncRuntimeProperty", _IResolvable_a771d0ef]]:
        '''Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function.

        Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-runtime
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunctionConfiguration.AppSyncRuntimeProperty", _IResolvable_a771d0ef]], jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(
        self,
        value: typing.Optional[typing.Union["CfnFunctionConfiguration.AppSyncRuntimeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e203e971b5408c83263cae9fd7d806cf359e4efed3c6b322eafc5192a69a6685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="syncConfig")
    def sync_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFunctionConfiguration.SyncConfigProperty", _IResolvable_a771d0ef]]:
        '''Describes a Sync configuration for a resolver.

        Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-syncconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFunctionConfiguration.SyncConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "syncConfig"))

    @sync_config.setter
    def sync_config(
        self,
        value: typing.Optional[typing.Union["CfnFunctionConfiguration.SyncConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37c741b235bdea6001262360617848c1c996713ff102a9f49303403a28aae53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnFunctionConfiguration.AppSyncRuntimeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "runtime_version": "runtimeVersion"},
    )
    class AppSyncRuntimeProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            runtime_version: builtins.str,
        ) -> None:
            '''Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function.

            Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

            :param name: The ``name`` of the runtime to use. Currently, the only allowed value is ``APPSYNC_JS`` .
            :param runtime_version: The ``version`` of the runtime to use. Currently, the only allowed version is ``1.0.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-appsyncruntime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                app_sync_runtime_property = appsync.CfnFunctionConfiguration.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a875d087cf34ba3d739fbb7ee1a93e2bc4ebb1b9d61f6963c6c580c03008f5a7)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "runtime_version": runtime_version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The ``name`` of the runtime to use.

            Currently, the only allowed value is ``APPSYNC_JS`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-appsyncruntime.html#cfn-appsync-functionconfiguration-appsyncruntime-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def runtime_version(self) -> builtins.str:
            '''The ``version`` of the runtime to use.

            Currently, the only allowed version is ``1.0.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-appsyncruntime.html#cfn-appsync-functionconfiguration-appsyncruntime-runtimeversion
            '''
            result = self._values.get("runtime_version")
            assert result is not None, "Required property 'runtime_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppSyncRuntimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_conflict_handler_arn": "lambdaConflictHandlerArn"},
    )
    class LambdaConflictHandlerConfigProperty:
        def __init__(
            self,
            *,
            lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LambdaConflictHandlerConfig`` object when configuring ``LAMBDA`` as the Conflict Handler.

            :param lambda_conflict_handler_arn: The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-lambdaconflicthandlerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                lambda_conflict_handler_config_property = appsync.CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11e44fc6adb323c7e663210e832622af4d7eeed913ca15af5545606d76e3b5d9)
                check_type(argname="argument lambda_conflict_handler_arn", value=lambda_conflict_handler_arn, expected_type=type_hints["lambda_conflict_handler_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_conflict_handler_arn is not None:
                self._values["lambda_conflict_handler_arn"] = lambda_conflict_handler_arn

        @builtins.property
        def lambda_conflict_handler_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-lambdaconflicthandlerconfig.html#cfn-appsync-functionconfiguration-lambdaconflicthandlerconfig-lambdaconflicthandlerarn
            '''
            result = self._values.get("lambda_conflict_handler_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConflictHandlerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnFunctionConfiguration.SyncConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_detection": "conflictDetection",
            "conflict_handler": "conflictHandler",
            "lambda_conflict_handler_config": "lambdaConflictHandlerConfig",
        },
    )
    class SyncConfigProperty:
        def __init__(
            self,
            *,
            conflict_detection: builtins.str,
            conflict_handler: typing.Optional[builtins.str] = None,
            lambda_conflict_handler_config: typing.Optional[typing.Union[typing.Union["CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes a Sync configuration for a resolver.

            Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

            :param conflict_detection: The Conflict Detection strategy to use. - *VERSION* : Detect conflicts based on object versions for this resolver. - *NONE* : Do not detect conflicts when invoking this resolver.
            :param conflict_handler: The Conflict Resolution strategy to perform in the event of a conflict. - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server. - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy. - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .
            :param lambda_conflict_handler_config: The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                sync_config_property = appsync.CfnFunctionConfiguration.SyncConfigProperty(
                    conflict_detection="conflictDetection",
                
                    # the properties below are optional
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync.CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__690c79dea5db529c5c4cf995a193e552acc73b2f4283cb485bd01fc6d7649090)
                check_type(argname="argument conflict_detection", value=conflict_detection, expected_type=type_hints["conflict_detection"])
                check_type(argname="argument conflict_handler", value=conflict_handler, expected_type=type_hints["conflict_handler"])
                check_type(argname="argument lambda_conflict_handler_config", value=lambda_conflict_handler_config, expected_type=type_hints["lambda_conflict_handler_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "conflict_detection": conflict_detection,
            }
            if conflict_handler is not None:
                self._values["conflict_handler"] = conflict_handler
            if lambda_conflict_handler_config is not None:
                self._values["lambda_conflict_handler_config"] = lambda_conflict_handler_config

        @builtins.property
        def conflict_detection(self) -> builtins.str:
            '''The Conflict Detection strategy to use.

            - *VERSION* : Detect conflicts based on object versions for this resolver.
            - *NONE* : Do not detect conflicts when invoking this resolver.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html#cfn-appsync-functionconfiguration-syncconfig-conflictdetection
            '''
            result = self._values.get("conflict_detection")
            assert result is not None, "Required property 'conflict_detection' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def conflict_handler(self) -> typing.Optional[builtins.str]:
            '''The Conflict Resolution strategy to perform in the event of a conflict.

            - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server.
            - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy.
            - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html#cfn-appsync-functionconfiguration-syncconfig-conflicthandler
            '''
            result = self._values.get("conflict_handler")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_conflict_handler_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty", _IResolvable_a771d0ef]]:
            '''The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-functionconfiguration-syncconfig.html#cfn-appsync-functionconfiguration-syncconfig-lambdaconflicthandlerconfig
            '''
            result = self._values.get("lambda_conflict_handler_config")
            return typing.cast(typing.Optional[typing.Union["CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SyncConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnFunctionConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "data_source_name": "dataSourceName",
        "name": "name",
        "code": "code",
        "code_s3_location": "codeS3Location",
        "description": "description",
        "function_version": "functionVersion",
        "max_batch_size": "maxBatchSize",
        "request_mapping_template": "requestMappingTemplate",
        "request_mapping_template_s3_location": "requestMappingTemplateS3Location",
        "response_mapping_template": "responseMappingTemplate",
        "response_mapping_template_s3_location": "responseMappingTemplateS3Location",
        "runtime": "runtime",
        "sync_config": "syncConfig",
    },
)
class CfnFunctionConfigurationProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        data_source_name: builtins.str,
        name: builtins.str,
        code: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        function_version: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sync_config: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFunctionConfiguration``.

        :param api_id: The AWS AppSync GraphQL API that you want to attach using this function.
        :param data_source_name: The name of data source this function will attach.
        :param name: The name of the function.
        :param code: The ``resolver`` code that contains the request and response functions. When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .
        :param code_s3_location: The Amazon S3 endpoint.
        :param description: The ``Function`` description.
        :param function_version: The version of the request mapping template. Currently, only the 2018-05-29 version of the template is supported.
        :param max_batch_size: The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.
        :param request_mapping_template: The ``Function`` request mapping template. Functions support only the 2018-05-29 version of the request mapping template.
        :param request_mapping_template_s3_location: Describes a Sync configuration for a resolver. Contains information on which Conflict Detection, as well as Resolution strategy, should be performed when the resolver is invoked.
        :param response_mapping_template: The ``Function`` response mapping template.
        :param response_mapping_template_s3_location: The location of a response mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param runtime: Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function. Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.
        :param sync_config: Describes a Sync configuration for a resolver. Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_function_configuration_props = appsync.CfnFunctionConfigurationProps(
                api_id="apiId",
                data_source_name="dataSourceName",
                name="name",
            
                # the properties below are optional
                code="code",
                code_s3_location="codeS3Location",
                description="description",
                function_version="functionVersion",
                max_batch_size=123,
                request_mapping_template="requestMappingTemplate",
                request_mapping_template_s3_location="requestMappingTemplateS3Location",
                response_mapping_template="responseMappingTemplate",
                response_mapping_template_s3_location="responseMappingTemplateS3Location",
                runtime=appsync.CfnFunctionConfiguration.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                ),
                sync_config=appsync.CfnFunctionConfiguration.SyncConfigProperty(
                    conflict_detection="conflictDetection",
            
                    # the properties below are optional
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync.CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84b7f7f1a55363f6363a905619a8929cba00d6f19c9bc0b6779a6e83502a19f)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument code_s3_location", value=code_s3_location, expected_type=type_hints["code_s3_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_version", value=function_version, expected_type=type_hints["function_version"])
            check_type(argname="argument max_batch_size", value=max_batch_size, expected_type=type_hints["max_batch_size"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument request_mapping_template_s3_location", value=request_mapping_template_s3_location, expected_type=type_hints["request_mapping_template_s3_location"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument response_mapping_template_s3_location", value=response_mapping_template_s3_location, expected_type=type_hints["response_mapping_template_s3_location"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument sync_config", value=sync_config, expected_type=type_hints["sync_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
            "data_source_name": data_source_name,
            "name": name,
        }
        if code is not None:
            self._values["code"] = code
        if code_s3_location is not None:
            self._values["code_s3_location"] = code_s3_location
        if description is not None:
            self._values["description"] = description
        if function_version is not None:
            self._values["function_version"] = function_version
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if request_mapping_template_s3_location is not None:
            self._values["request_mapping_template_s3_location"] = request_mapping_template_s3_location
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if response_mapping_template_s3_location is not None:
            self._values["response_mapping_template_s3_location"] = response_mapping_template_s3_location
        if runtime is not None:
            self._values["runtime"] = runtime
        if sync_config is not None:
            self._values["sync_config"] = sync_config

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The AWS AppSync GraphQL API that you want to attach using this function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_source_name(self) -> builtins.str:
        '''The name of data source this function will attach.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-datasourcename
        '''
        result = self._values.get("data_source_name")
        assert result is not None, "Required property 'data_source_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''The ``resolver`` code that contains the request and response functions.

        When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-codes3location
        '''
        result = self._values.get("code_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_version(self) -> typing.Optional[builtins.str]:
        '''The version of the request mapping template.

        Currently, only the 2018-05-29 version of the template is supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-functionversion
        '''
        result = self._values.get("function_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-maxbatchsize
        '''
        result = self._values.get("max_batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` request mapping template.

        Functions support only the 2018-05-29 version of the request mapping template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-requestmappingtemplate
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''Describes a Sync configuration for a resolver.

        Contains information on which Conflict Detection, as well as Resolution strategy, should be performed when the resolver is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-requestmappingtemplates3location
        '''
        result = self._values.get("request_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The ``Function`` response mapping template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-responsemappingtemplate
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a response mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-responsemappingtemplates3location
        '''
        result = self._values.get("response_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(
        self,
    ) -> typing.Optional[typing.Union[CfnFunctionConfiguration.AppSyncRuntimeProperty, _IResolvable_a771d0ef]]:
        '''Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function.

        Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-runtime
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[typing.Union[CfnFunctionConfiguration.AppSyncRuntimeProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sync_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFunctionConfiguration.SyncConfigProperty, _IResolvable_a771d0ef]]:
        '''Describes a Sync configuration for a resolver.

        Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-functionconfiguration.html#cfn-appsync-functionconfiguration-syncconfig
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional[typing.Union[CfnFunctionConfiguration.SyncConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGraphQLApi(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnGraphQLApi",
):
    '''A CloudFormation ``AWS::AppSync::GraphQLApi``.

    The ``AWS::AppSync::GraphQLApi`` resource creates a new AWS AppSync GraphQL API. This is the top-level construct for your application. For more information, see `Quick Start <https://docs.aws.amazon.com/appsync/latest/devguide/quickstart.html>`_ in the *AWS AppSync Developer Guide* .

    :cloudformationResource: AWS::AppSync::GraphQLApi
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_graph_qLApi = appsync.CfnGraphQLApi(self, "MyCfnGraphQLApi",
            authentication_type="authenticationType",
            name="name",
        
            # the properties below are optional
            additional_authentication_providers=[appsync.CfnGraphQLApi.AdditionalAuthenticationProviderProperty(
                authentication_type="authenticationType",
        
                # the properties below are optional
                lambda_authorizer_config=appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                ),
                open_id_connect_config=appsync.CfnGraphQLApi.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                ),
                user_pool_config=appsync.CfnGraphQLApi.CognitoUserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    user_pool_id="userPoolId"
                )
            )],
            lambda_authorizer_config=appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty(
                authorizer_result_ttl_in_seconds=123,
                authorizer_uri="authorizerUri",
                identity_validation_expression="identityValidationExpression"
            ),
            log_config=appsync.CfnGraphQLApi.LogConfigProperty(
                cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                exclude_verbose_content=False,
                field_log_level="fieldLogLevel"
            ),
            open_id_connect_config=appsync.CfnGraphQLApi.OpenIDConnectConfigProperty(
                auth_ttl=123,
                client_id="clientId",
                iat_ttl=123,
                issuer="issuer"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_pool_config=appsync.CfnGraphQLApi.UserPoolConfigProperty(
                app_id_client_regex="appIdClientRegex",
                aws_region="awsRegion",
                default_action="defaultAction",
                user_pool_id="userPoolId"
            ),
            xray_enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        authentication_type: builtins.str,
        name: builtins.str,
        additional_authentication_providers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGraphQLApi.AdditionalAuthenticationProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        lambda_authorizer_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        log_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.LogConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_id_connect_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.UserPoolConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        xray_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::GraphQLApi``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authentication_type: Security configuration for your GraphQL API. For allowed values (such as ``API_KEY`` , ``AWS_IAM`` , ``AMAZON_COGNITO_USER_POOLS`` , ``OPENID_CONNECT`` , or ``AWS_LAMBDA`` ), see `Security <https://docs.aws.amazon.com/appsync/latest/devguide/security.html>`_ in the *AWS AppSync Developer Guide* .
        :param name: The API name.
        :param additional_authentication_providers: A list of additional authentication providers for the ``GraphqlApi`` API.
        :param lambda_authorizer_config: A ``LambdaAuthorizerConfig`` holds configuration on how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode. Be aware that an AWS AppSync API may have only one Lambda authorizer configured at a time.
        :param log_config: The Amazon CloudWatch Logs configuration.
        :param open_id_connect_config: The OpenID Connect configuration.
        :param tags: An arbitrary set of tags (key-value pairs) for this GraphQL API.
        :param user_pool_config: Optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint.
        :param xray_enabled: A flag indicating whether to use AWS X-Ray tracing for this ``GraphqlApi`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35cdd9f83066545a18ab25e130890ddf3953f80b2e1aa8e4726b44a0d4e46bea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGraphQLApiProps(
            authentication_type=authentication_type,
            name=name,
            additional_authentication_providers=additional_authentication_providers,
            lambda_authorizer_config=lambda_authorizer_config,
            log_config=log_config,
            open_id_connect_config=open_id_connect_config,
            tags=tags,
            user_pool_config=user_pool_config,
            xray_enabled=xray_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826120bf7d041350b4055c8304d25894e07ccf1b04cf76ab62d30f03cfdecefb)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4bde0439df44816345508bca736a38db0f252296ab146e97372f75c8309fac)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApiId")
    def attr_api_id(self) -> builtins.str:
        '''Unique AWS AppSync GraphQL API identifier.

        :cloudformationAttribute: ApiId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApiId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the API key, such as ``arn:aws:appsync:us-east-1:123456789012:apis/graphqlapiid`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrGraphQlUrl")
    def attr_graph_ql_url(self) -> builtins.str:
        '''The Endpoint URL of your GraphQL API.

        :cloudformationAttribute: GraphQLUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGraphQlUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An arbitrary set of tags (key-value pairs) for this GraphQL API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        '''Security configuration for your GraphQL API.

        For allowed values (such as ``API_KEY`` , ``AWS_IAM`` , ``AMAZON_COGNITO_USER_POOLS`` , ``OPENID_CONNECT`` , or ``AWS_LAMBDA`` ), see `Security <https://docs.aws.amazon.com/appsync/latest/devguide/security.html>`_ in the *AWS AppSync Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-authenticationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a067b836aa3dde5d3aa6bb7773bf5ebc19a3a20a62332cdb8226e1a0679538ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The API name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b313f5ecbd74c90ca73a882dbe07294449e20153d217324ff130970ec391f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="additionalAuthenticationProviders")
    def additional_authentication_providers(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGraphQLApi.AdditionalAuthenticationProviderProperty", _IResolvable_a771d0ef]]]]:
        '''A list of additional authentication providers for the ``GraphqlApi`` API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-additionalauthenticationproviders
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGraphQLApi.AdditionalAuthenticationProviderProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "additionalAuthenticationProviders"))

    @additional_authentication_providers.setter
    def additional_authentication_providers(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGraphQLApi.AdditionalAuthenticationProviderProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68318736d06afb0a9920be900c3d0367e9c22349d281b5fd22c94355a7f248b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalAuthenticationProviders", value)

    @builtins.property
    @jsii.member(jsii_name="lambdaAuthorizerConfig")
    def lambda_authorizer_config(
        self,
    ) -> typing.Optional[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", _IResolvable_a771d0ef]]:
        '''A ``LambdaAuthorizerConfig`` holds configuration on how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode.

        Be aware that an AWS AppSync API may have only one Lambda authorizer configured at a time.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "lambdaAuthorizerConfig"))

    @lambda_authorizer_config.setter
    def lambda_authorizer_config(
        self,
        value: typing.Optional[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a1fe11bf87f9ffcc658c8eb8912d198f892f1cefef11b5c101f8713602fa76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaAuthorizerConfig", value)

    @builtins.property
    @jsii.member(jsii_name="logConfig")
    def log_config(
        self,
    ) -> typing.Optional[typing.Union["CfnGraphQLApi.LogConfigProperty", _IResolvable_a771d0ef]]:
        '''The Amazon CloudWatch Logs configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-logconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.LogConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "logConfig"))

    @log_config.setter
    def log_config(
        self,
        value: typing.Optional[typing.Union["CfnGraphQLApi.LogConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc15d0778d9ee3f37f51211ffc30e45cdfd1d19736a9dc8ab1441f87c9971718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logConfig", value)

    @builtins.property
    @jsii.member(jsii_name="openIdConnectConfig")
    def open_id_connect_config(
        self,
    ) -> typing.Optional[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", _IResolvable_a771d0ef]]:
        '''The OpenID Connect configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-openidconnectconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "openIdConnectConfig"))

    @open_id_connect_config.setter
    def open_id_connect_config(
        self,
        value: typing.Optional[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db793e163945b7c43dc2d9c033e3d12e3209e64adbf84ec50cb3c6a25437fb47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openIdConnectConfig", value)

    @builtins.property
    @jsii.member(jsii_name="userPoolConfig")
    def user_pool_config(
        self,
    ) -> typing.Optional[typing.Union["CfnGraphQLApi.UserPoolConfigProperty", _IResolvable_a771d0ef]]:
        '''Optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-userpoolconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.UserPoolConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "userPoolConfig"))

    @user_pool_config.setter
    def user_pool_config(
        self,
        value: typing.Optional[typing.Union["CfnGraphQLApi.UserPoolConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425b943bfc67e30cc27dc6fc69e234364124baad69cdf10f22f0b207be11f863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPoolConfig", value)

    @builtins.property
    @jsii.member(jsii_name="xrayEnabled")
    def xray_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag indicating whether to use AWS X-Ray tracing for this ``GraphqlApi`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-xrayenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "xrayEnabled"))

    @xray_enabled.setter
    def xray_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ef4ba154d8e6e4c0b121623c03ab1a74409ee2cb124b720ddfbb1ffa32d128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xrayEnabled", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnGraphQLApi.AdditionalAuthenticationProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_type": "authenticationType",
            "lambda_authorizer_config": "lambdaAuthorizerConfig",
            "open_id_connect_config": "openIdConnectConfig",
            "user_pool_config": "userPoolConfig",
        },
    )
    class AdditionalAuthenticationProviderProperty:
        def __init__(
            self,
            *,
            authentication_type: builtins.str,
            lambda_authorizer_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            open_id_connect_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            user_pool_config: typing.Optional[typing.Union[typing.Union["CfnGraphQLApi.CognitoUserPoolConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes an additional authentication provider.

            :param authentication_type: The authentication type for API key, AWS Identity and Access Management , OIDC, Amazon Cognito user pools , or AWS Lambda . Valid Values: ``API_KEY`` | ``AWS_IAM`` | ``OPENID_CONNECT`` | ``AMAZON_COGNITO_USER_POOLS`` | ``AWS_LAMBDA``
            :param lambda_authorizer_config: Configuration for AWS Lambda function authorization.
            :param open_id_connect_config: The OIDC configuration.
            :param user_pool_config: The Amazon Cognito user pool configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                additional_authentication_provider_property = appsync.CfnGraphQLApi.AdditionalAuthenticationProviderProperty(
                    authentication_type="authenticationType",
                
                    # the properties below are optional
                    lambda_authorizer_config=appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty(
                        authorizer_result_ttl_in_seconds=123,
                        authorizer_uri="authorizerUri",
                        identity_validation_expression="identityValidationExpression"
                    ),
                    open_id_connect_config=appsync.CfnGraphQLApi.OpenIDConnectConfigProperty(
                        auth_ttl=123,
                        client_id="clientId",
                        iat_ttl=123,
                        issuer="issuer"
                    ),
                    user_pool_config=appsync.CfnGraphQLApi.CognitoUserPoolConfigProperty(
                        app_id_client_regex="appIdClientRegex",
                        aws_region="awsRegion",
                        user_pool_id="userPoolId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2747361e42703d14d2893ba0fb94bb920962a49bdf3ff646b2e8bf752bae06c8)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
                check_type(argname="argument open_id_connect_config", value=open_id_connect_config, expected_type=type_hints["open_id_connect_config"])
                check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "authentication_type": authentication_type,
            }
            if lambda_authorizer_config is not None:
                self._values["lambda_authorizer_config"] = lambda_authorizer_config
            if open_id_connect_config is not None:
                self._values["open_id_connect_config"] = open_id_connect_config
            if user_pool_config is not None:
                self._values["user_pool_config"] = user_pool_config

        @builtins.property
        def authentication_type(self) -> builtins.str:
            '''The authentication type for API key, AWS Identity and Access Management , OIDC, Amazon Cognito user pools , or AWS Lambda .

            Valid Values: ``API_KEY`` | ``AWS_IAM`` | ``OPENID_CONNECT`` | ``AMAZON_COGNITO_USER_POOLS`` | ``AWS_LAMBDA``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-authenticationtype
            '''
            result = self._values.get("authentication_type")
            assert result is not None, "Required property 'authentication_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def lambda_authorizer_config(
            self,
        ) -> typing.Optional[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", _IResolvable_a771d0ef]]:
            '''Configuration for AWS Lambda function authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-lambdaauthorizerconfig
            '''
            result = self._values.get("lambda_authorizer_config")
            return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.LambdaAuthorizerConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def open_id_connect_config(
            self,
        ) -> typing.Optional[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", _IResolvable_a771d0ef]]:
            '''The OIDC configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-openidconnectconfig
            '''
            result = self._values.get("open_id_connect_config")
            return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.OpenIDConnectConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def user_pool_config(
            self,
        ) -> typing.Optional[typing.Union["CfnGraphQLApi.CognitoUserPoolConfigProperty", _IResolvable_a771d0ef]]:
            '''The Amazon Cognito user pool configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-additionalauthenticationprovider.html#cfn-appsync-graphqlapi-additionalauthenticationprovider-userpoolconfig
            '''
            result = self._values.get("user_pool_config")
            return typing.cast(typing.Optional[typing.Union["CfnGraphQLApi.CognitoUserPoolConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdditionalAuthenticationProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnGraphQLApi.CognitoUserPoolConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_id_client_regex": "appIdClientRegex",
            "aws_region": "awsRegion",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoUserPoolConfigProperty:
        def __init__(
            self,
            *,
            app_id_client_regex: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an Amazon Cognito user pool configuration.

            :param app_id_client_regex: A regular expression for validating the incoming Amazon Cognito user pool app client ID. If this value isn't set, no filtering is applied.
            :param aws_region: The AWS Region in which the user pool was created.
            :param user_pool_id: The user pool ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                cognito_user_pool_config_property = appsync.CfnGraphQLApi.CognitoUserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0cb54a365c973a25b44f1eb9ea59d5f1e5ddcc0a9ad1a8e6c6ff5a81299c207d)
                check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_id_client_regex is not None:
                self._values["app_id_client_regex"] = app_id_client_regex
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def app_id_client_regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validating the incoming Amazon Cognito user pool app client ID.

            If this value isn't set, no filtering is applied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html#cfn-appsync-graphqlapi-cognitouserpoolconfig-appidclientregex
            '''
            result = self._values.get("app_id_client_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region in which the user pool was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html#cfn-appsync-graphqlapi-cognitouserpoolconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The user pool ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-cognitouserpoolconfig.html#cfn-appsync-graphqlapi-cognitouserpoolconfig-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoUserPoolConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
            "authorizer_uri": "authorizerUri",
            "identity_validation_expression": "identityValidationExpression",
        },
    )
    class LambdaAuthorizerConfigProperty:
        def __init__(
            self,
            *,
            authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
            authorizer_uri: typing.Optional[builtins.str] = None,
            identity_validation_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for AWS Lambda function authorization.

            :param authorizer_result_ttl_in_seconds: The number of seconds a response should be cached for. The default is 5 minutes (300 seconds). The Lambda function can override this by returning a ``ttlOverride`` key in its response. A value of 0 disables caching of responses.
            :param authorizer_uri: The ARN of the Lambda function to be called for authorization. This may be a standard Lambda ARN, a version ARN ( ``.../v3`` ) or alias ARN. *Note* : This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To do so with the AWS CLI , run the following: ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``
            :param identity_validation_expression: A regular expression for validation of tokens before the Lambda function is called.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                lambda_authorizer_config_property = appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d43a4eb86ea093ff4548baee0ed3a82e4578b0193fdb2a2719d2346d58801ca6)
                check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
                check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
                check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorizer_result_ttl_in_seconds is not None:
                self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
            if authorizer_uri is not None:
                self._values["authorizer_uri"] = authorizer_uri
            if identity_validation_expression is not None:
                self._values["identity_validation_expression"] = identity_validation_expression

        @builtins.property
        def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds a response should be cached for.

            The default is 5 minutes (300 seconds). The Lambda function can override this by returning a ``ttlOverride`` key in its response. A value of 0 disables caching of responses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig-authorizerresultttlinseconds
            '''
            result = self._values.get("authorizer_result_ttl_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def authorizer_uri(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function to be called for authorization.

            This may be a standard Lambda ARN, a version ARN ( ``.../v3`` ) or alias ARN.

            *Note* : This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To do so with the AWS CLI , run the following:

            ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig-authorizeruri
            '''
            result = self._values.get("authorizer_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_validation_expression(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validation of tokens before the Lambda function is called.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig-identityvalidationexpression
            '''
            result = self._values.get("identity_validation_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaAuthorizerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnGraphQLApi.LogConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_role_arn": "cloudWatchLogsRoleArn",
            "exclude_verbose_content": "excludeVerboseContent",
            "field_log_level": "fieldLogLevel",
        },
    )
    class LogConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
            exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            field_log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LogConfig`` property type specifies the logging configuration when writing GraphQL operations and tracing to Amazon CloudWatch for an AWS AppSync GraphQL API.

            ``LogConfig`` is a property of the `AWS::AppSync::GraphQLApi <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html>`_ property type.

            :param cloud_watch_logs_role_arn: The service role that AWS AppSync will assume to publish to Amazon CloudWatch Logs in your account.
            :param exclude_verbose_content: Set to TRUE to exclude sections that contain information such as headers, context, and evaluated mapping templates, regardless of logging level.
            :param field_log_level: The field logging level. Values can be NONE, ERROR, or ALL. - *NONE* : No field-level logs are captured. - *ERROR* : Logs the following information only for the fields that are in error: - The error section in the server response. - Field-level errors. - The generated request/response functions that got resolved for error fields. - *ALL* : The following information is logged for all fields in the query: - Field-level tracing information. - The generated request/response functions that got resolved for each field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                log_config_property = appsync.CfnGraphQLApi.LogConfigProperty(
                    cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                    exclude_verbose_content=False,
                    field_log_level="fieldLogLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f818e71d03b36e227b74c1b69b93f5db0bedc918641237fbdcd5609a92eaf151)
                check_type(argname="argument cloud_watch_logs_role_arn", value=cloud_watch_logs_role_arn, expected_type=type_hints["cloud_watch_logs_role_arn"])
                check_type(argname="argument exclude_verbose_content", value=exclude_verbose_content, expected_type=type_hints["exclude_verbose_content"])
                check_type(argname="argument field_log_level", value=field_log_level, expected_type=type_hints["field_log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_role_arn is not None:
                self._values["cloud_watch_logs_role_arn"] = cloud_watch_logs_role_arn
            if exclude_verbose_content is not None:
                self._values["exclude_verbose_content"] = exclude_verbose_content
            if field_log_level is not None:
                self._values["field_log_level"] = field_log_level

        @builtins.property
        def cloud_watch_logs_role_arn(self) -> typing.Optional[builtins.str]:
            '''The service role that AWS AppSync will assume to publish to Amazon CloudWatch Logs in your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html#cfn-appsync-graphqlapi-logconfig-cloudwatchlogsrolearn
            '''
            result = self._values.get("cloud_watch_logs_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_verbose_content(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Set to TRUE to exclude sections that contain information such as headers, context, and evaluated mapping templates, regardless of logging level.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html#cfn-appsync-graphqlapi-logconfig-excludeverbosecontent
            '''
            result = self._values.get("exclude_verbose_content")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def field_log_level(self) -> typing.Optional[builtins.str]:
            '''The field logging level. Values can be NONE, ERROR, or ALL.

            - *NONE* : No field-level logs are captured.
            - *ERROR* : Logs the following information only for the fields that are in error:
            - The error section in the server response.
            - Field-level errors.
            - The generated request/response functions that got resolved for error fields.
            - *ALL* : The following information is logged for all fields in the query:
            - Field-level tracing information.
            - The generated request/response functions that got resolved for each field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-logconfig.html#cfn-appsync-graphqlapi-logconfig-fieldloglevel
            '''
            result = self._values.get("field_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnGraphQLApi.OpenIDConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_ttl": "authTtl",
            "client_id": "clientId",
            "iat_ttl": "iatTtl",
            "issuer": "issuer",
        },
    )
    class OpenIDConnectConfigProperty:
        def __init__(
            self,
            *,
            auth_ttl: typing.Optional[jsii.Number] = None,
            client_id: typing.Optional[builtins.str] = None,
            iat_ttl: typing.Optional[jsii.Number] = None,
            issuer: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``OpenIDConnectConfig`` property type specifies the optional authorization configuration for using an OpenID Connect compliant service with your GraphQL endpoint for an AWS AppSync GraphQL API.

            ``OpenIDConnectConfig`` is a property of the `AWS::AppSync::GraphQLApi <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html>`_ property type.

            :param auth_ttl: The number of milliseconds that a token is valid after being authenticated.
            :param client_id: The client identifier of the Relying party at the OpenID identity provider. This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so that AWS AppSync can validate against multiple client identifiers at a time.
            :param iat_ttl: The number of milliseconds that a token is valid after it's issued to a user.
            :param issuer: The issuer for the OIDC configuration. The issuer returned by discovery must exactly match the value of ``iss`` in the ID token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                open_iDConnect_config_property = appsync.CfnGraphQLApi.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ab933ba3d5962d9d6e491601744175586103ac2a1c6c99ab05cf53d7db5e30a)
                check_type(argname="argument auth_ttl", value=auth_ttl, expected_type=type_hints["auth_ttl"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument iat_ttl", value=iat_ttl, expected_type=type_hints["iat_ttl"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_ttl is not None:
                self._values["auth_ttl"] = auth_ttl
            if client_id is not None:
                self._values["client_id"] = client_id
            if iat_ttl is not None:
                self._values["iat_ttl"] = iat_ttl
            if issuer is not None:
                self._values["issuer"] = issuer

        @builtins.property
        def auth_ttl(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds that a token is valid after being authenticated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-authttl
            '''
            result = self._values.get("auth_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The client identifier of the Relying party at the OpenID identity provider.

            This identifier is typically obtained when the Relying party is registered with the OpenID identity provider. You can specify a regular expression so that AWS AppSync can validate against multiple client identifiers at a time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iat_ttl(self) -> typing.Optional[jsii.Number]:
            '''The number of milliseconds that a token is valid after it's issued to a user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-iatttl
            '''
            result = self._values.get("iat_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer for the OIDC configuration.

            The issuer returned by discovery must exactly match the value of ``iss`` in the ID token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-openidconnectconfig.html#cfn-appsync-graphqlapi-openidconnectconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIDConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnGraphQLApi.UserPoolConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_id_client_regex": "appIdClientRegex",
            "aws_region": "awsRegion",
            "default_action": "defaultAction",
            "user_pool_id": "userPoolId",
        },
    )
    class UserPoolConfigProperty:
        def __init__(
            self,
            *,
            app_id_client_regex: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            default_action: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``UserPoolConfig`` property type specifies the optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint for an AWS AppSync GraphQL API.

            :param app_id_client_regex: A regular expression for validating the incoming Amazon Cognito user pool app client ID. If this value isn't set, no filtering is applied.
            :param aws_region: The AWS Region in which the user pool was created.
            :param default_action: The action that you want your GraphQL API to take when a request that uses Amazon Cognito user pool authentication doesn't match the Amazon Cognito user pool configuration. When specifying Amazon Cognito user pools as the default authentication, you must set the value for ``DefaultAction`` to ``ALLOW`` if specifying ``AdditionalAuthenticationProviders`` .
            :param user_pool_id: The user pool ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                user_pool_config_property = appsync.CfnGraphQLApi.UserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    default_action="defaultAction",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d2b4691f85a7f106da611dcf4e7b8ffff78be58e10c683e745fe27f3d504fbf)
                check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_id_client_regex is not None:
                self._values["app_id_client_regex"] = app_id_client_regex
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if default_action is not None:
                self._values["default_action"] = default_action
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def app_id_client_regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for validating the incoming Amazon Cognito user pool app client ID.

            If this value isn't set, no filtering is applied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-appidclientregex
            '''
            result = self._values.get("app_id_client_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region in which the user pool was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_action(self) -> typing.Optional[builtins.str]:
            '''The action that you want your GraphQL API to take when a request that uses Amazon Cognito user pool authentication doesn't match the Amazon Cognito user pool configuration.

            When specifying Amazon Cognito user pools as the default authentication, you must set the value for ``DefaultAction`` to ``ALLOW`` if specifying ``AdditionalAuthenticationProviders`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-defaultaction
            '''
            result = self._values.get("default_action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The user pool ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-userpoolconfig.html#cfn-appsync-graphqlapi-userpoolconfig-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPoolConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnGraphQLApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "name": "name",
        "additional_authentication_providers": "additionalAuthenticationProviders",
        "lambda_authorizer_config": "lambdaAuthorizerConfig",
        "log_config": "logConfig",
        "open_id_connect_config": "openIdConnectConfig",
        "tags": "tags",
        "user_pool_config": "userPoolConfig",
        "xray_enabled": "xrayEnabled",
    },
)
class CfnGraphQLApiProps:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        name: builtins.str,
        additional_authentication_providers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGraphQLApi.AdditionalAuthenticationProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        lambda_authorizer_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        log_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LogConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_id_connect_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_pool_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.UserPoolConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        xray_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGraphQLApi``.

        :param authentication_type: Security configuration for your GraphQL API. For allowed values (such as ``API_KEY`` , ``AWS_IAM`` , ``AMAZON_COGNITO_USER_POOLS`` , ``OPENID_CONNECT`` , or ``AWS_LAMBDA`` ), see `Security <https://docs.aws.amazon.com/appsync/latest/devguide/security.html>`_ in the *AWS AppSync Developer Guide* .
        :param name: The API name.
        :param additional_authentication_providers: A list of additional authentication providers for the ``GraphqlApi`` API.
        :param lambda_authorizer_config: A ``LambdaAuthorizerConfig`` holds configuration on how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode. Be aware that an AWS AppSync API may have only one Lambda authorizer configured at a time.
        :param log_config: The Amazon CloudWatch Logs configuration.
        :param open_id_connect_config: The OpenID Connect configuration.
        :param tags: An arbitrary set of tags (key-value pairs) for this GraphQL API.
        :param user_pool_config: Optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint.
        :param xray_enabled: A flag indicating whether to use AWS X-Ray tracing for this ``GraphqlApi`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_graph_qLApi_props = appsync.CfnGraphQLApiProps(
                authentication_type="authenticationType",
                name="name",
            
                # the properties below are optional
                additional_authentication_providers=[appsync.CfnGraphQLApi.AdditionalAuthenticationProviderProperty(
                    authentication_type="authenticationType",
            
                    # the properties below are optional
                    lambda_authorizer_config=appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty(
                        authorizer_result_ttl_in_seconds=123,
                        authorizer_uri="authorizerUri",
                        identity_validation_expression="identityValidationExpression"
                    ),
                    open_id_connect_config=appsync.CfnGraphQLApi.OpenIDConnectConfigProperty(
                        auth_ttl=123,
                        client_id="clientId",
                        iat_ttl=123,
                        issuer="issuer"
                    ),
                    user_pool_config=appsync.CfnGraphQLApi.CognitoUserPoolConfigProperty(
                        app_id_client_regex="appIdClientRegex",
                        aws_region="awsRegion",
                        user_pool_id="userPoolId"
                    )
                )],
                lambda_authorizer_config=appsync.CfnGraphQLApi.LambdaAuthorizerConfigProperty(
                    authorizer_result_ttl_in_seconds=123,
                    authorizer_uri="authorizerUri",
                    identity_validation_expression="identityValidationExpression"
                ),
                log_config=appsync.CfnGraphQLApi.LogConfigProperty(
                    cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                    exclude_verbose_content=False,
                    field_log_level="fieldLogLevel"
                ),
                open_id_connect_config=appsync.CfnGraphQLApi.OpenIDConnectConfigProperty(
                    auth_ttl=123,
                    client_id="clientId",
                    iat_ttl=123,
                    issuer="issuer"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_pool_config=appsync.CfnGraphQLApi.UserPoolConfigProperty(
                    app_id_client_regex="appIdClientRegex",
                    aws_region="awsRegion",
                    default_action="defaultAction",
                    user_pool_id="userPoolId"
                ),
                xray_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118a47425725c6c7fa018eca797893634e7acf5e4ff26c3e7a15ac69848c4623)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument additional_authentication_providers", value=additional_authentication_providers, expected_type=type_hints["additional_authentication_providers"])
            check_type(argname="argument lambda_authorizer_config", value=lambda_authorizer_config, expected_type=type_hints["lambda_authorizer_config"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument open_id_connect_config", value=open_id_connect_config, expected_type=type_hints["open_id_connect_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_pool_config", value=user_pool_config, expected_type=type_hints["user_pool_config"])
            check_type(argname="argument xray_enabled", value=xray_enabled, expected_type=type_hints["xray_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
            "name": name,
        }
        if additional_authentication_providers is not None:
            self._values["additional_authentication_providers"] = additional_authentication_providers
        if lambda_authorizer_config is not None:
            self._values["lambda_authorizer_config"] = lambda_authorizer_config
        if log_config is not None:
            self._values["log_config"] = log_config
        if open_id_connect_config is not None:
            self._values["open_id_connect_config"] = open_id_connect_config
        if tags is not None:
            self._values["tags"] = tags
        if user_pool_config is not None:
            self._values["user_pool_config"] = user_pool_config
        if xray_enabled is not None:
            self._values["xray_enabled"] = xray_enabled

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Security configuration for your GraphQL API.

        For allowed values (such as ``API_KEY`` , ``AWS_IAM`` , ``AMAZON_COGNITO_USER_POOLS`` , ``OPENID_CONNECT`` , or ``AWS_LAMBDA`` ), see `Security <https://docs.aws.amazon.com/appsync/latest/devguide/security.html>`_ in the *AWS AppSync Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-authenticationtype
        '''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The API name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_authentication_providers(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGraphQLApi.AdditionalAuthenticationProviderProperty, _IResolvable_a771d0ef]]]]:
        '''A list of additional authentication providers for the ``GraphqlApi`` API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-additionalauthenticationproviders
        '''
        result = self._values.get("additional_authentication_providers")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGraphQLApi.AdditionalAuthenticationProviderProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def lambda_authorizer_config(
        self,
    ) -> typing.Optional[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, _IResolvable_a771d0ef]]:
        '''A ``LambdaAuthorizerConfig`` holds configuration on how to authorize AWS AppSync API access when using the ``AWS_LAMBDA`` authorizer mode.

        Be aware that an AWS AppSync API may have only one Lambda authorizer configured at a time.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-lambdaauthorizerconfig
        '''
        result = self._values.get("lambda_authorizer_config")
        return typing.cast(typing.Optional[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def log_config(
        self,
    ) -> typing.Optional[typing.Union[CfnGraphQLApi.LogConfigProperty, _IResolvable_a771d0ef]]:
        '''The Amazon CloudWatch Logs configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-logconfig
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional[typing.Union[CfnGraphQLApi.LogConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def open_id_connect_config(
        self,
    ) -> typing.Optional[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, _IResolvable_a771d0ef]]:
        '''The OpenID Connect configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-openidconnectconfig
        '''
        result = self._values.get("open_id_connect_config")
        return typing.cast(typing.Optional[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An arbitrary set of tags (key-value pairs) for this GraphQL API.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def user_pool_config(
        self,
    ) -> typing.Optional[typing.Union[CfnGraphQLApi.UserPoolConfigProperty, _IResolvable_a771d0ef]]:
        '''Optional authorization configuration for using Amazon Cognito user pools with your GraphQL endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-userpoolconfig
        '''
        result = self._values.get("user_pool_config")
        return typing.cast(typing.Optional[typing.Union[CfnGraphQLApi.UserPoolConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def xray_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag indicating whether to use AWS X-Ray tracing for this ``GraphqlApi`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlapi.html#cfn-appsync-graphqlapi-xrayenabled
        '''
        result = self._values.get("xray_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphQLApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGraphQLSchema(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnGraphQLSchema",
):
    '''A CloudFormation ``AWS::AppSync::GraphQLSchema``.

    The ``AWS::AppSync::GraphQLSchema`` resource is used for your AWS AppSync GraphQL schema that controls the data model for your API. Schema files are text written in Schema Definition Language (SDL) format. For more information about schema authoring, see `Designing a GraphQL API <https://docs.aws.amazon.com/appsync/latest/devguide/designing-a-graphql-api.html>`_ in the *AWS AppSync Developer Guide* .
    .. epigraph::

       When you submit an update, AWS CloudFormation updates resources based on differences between what you submit and the stack's current template. To cause this resource to be updated you must change a property value for this resource in the CloudFormation template. Changing the Amazon S3 file content without changing a property value will not result in an update operation.

       See `Update Behaviors of Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html>`_ in the *AWS CloudFormation User Guide* .

    :cloudformationResource: AWS::AppSync::GraphQLSchema
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_graph_qLSchema = appsync.CfnGraphQLSchema(self, "MyCfnGraphQLSchema",
            api_id="apiId",
        
            # the properties below are optional
            definition="definition",
            definition_s3_location="definitionS3Location"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_id: builtins.str,
        definition: typing.Optional[builtins.str] = None,
        definition_s3_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::GraphQLSchema``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The AWS AppSync GraphQL API identifier to which you want to apply this schema.
        :param definition: The text representation of a GraphQL schema in SDL format. For more information about using the ``Ref`` function, see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref>`_ .
        :param definition_s3_location: The location of a GraphQL schema file in an Amazon S3 bucket. Use this if you want to provision with the schema living in Amazon S3 rather than embedding it in your CloudFormation template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41fbc49a572f33a0ec287cc8f222b767678f6f6d7d81cd1d63eac0ba9deca3b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGraphQLSchemaProps(
            api_id=api_id,
            definition=definition,
            definition_s3_location=definition_s3_location,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63fcd85176b2a5d4253cda0d71e0decf878989fcbe28ff099fe52d89794d952f)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62dafbc3c1ea7a58255af9ca0491e2bc848110fe46bd54ac9d1914ffb512047f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The AWS AppSync GraphQL API identifier to which you want to apply this schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febc08037f81d08fc7c3271b8385b28dbc558dc15a9b74f584dd55dd8867555b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Optional[builtins.str]:
        '''The text representation of a GraphQL schema in SDL format.

        For more information about using the ``Ref`` function, see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-definition
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e24611a7cec5ed686a0fba4b722b26580ce4c0f6c6be962f3b63137060bdad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="definitionS3Location")
    def definition_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a GraphQL schema file in an Amazon S3 bucket.

        Use this if you want to provision with the schema living in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-definitions3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionS3Location"))

    @definition_s3_location.setter
    def definition_s3_location(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae574e2d8cbfc39fac65e1c0227be155e1808c9be0fb3a213d0520fe28ecf83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionS3Location", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnGraphQLSchemaProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "definition": "definition",
        "definition_s3_location": "definitionS3Location",
    },
)
class CfnGraphQLSchemaProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        definition: typing.Optional[builtins.str] = None,
        definition_s3_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGraphQLSchema``.

        :param api_id: The AWS AppSync GraphQL API identifier to which you want to apply this schema.
        :param definition: The text representation of a GraphQL schema in SDL format. For more information about using the ``Ref`` function, see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref>`_ .
        :param definition_s3_location: The location of a GraphQL schema file in an Amazon S3 bucket. Use this if you want to provision with the schema living in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_graph_qLSchema_props = appsync.CfnGraphQLSchemaProps(
                api_id="apiId",
            
                # the properties below are optional
                definition="definition",
                definition_s3_location="definitionS3Location"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1252139e4225ccd4d89a46bbcbb78e7056c85320a8e69df27f5edc6cf532af2)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_s3_location", value=definition_s3_location, expected_type=type_hints["definition_s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
        }
        if definition is not None:
            self._values["definition"] = definition
        if definition_s3_location is not None:
            self._values["definition_s3_location"] = definition_s3_location

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The AWS AppSync GraphQL API identifier to which you want to apply this schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition(self) -> typing.Optional[builtins.str]:
        '''The text representation of a GraphQL schema in SDL format.

        For more information about using the ``Ref`` function, see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a GraphQL schema file in an Amazon S3 bucket.

        Use this if you want to provision with the schema living in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-graphqlschema.html#cfn-appsync-graphqlschema-definitions3location
        '''
        result = self._values.get("definition_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphQLSchemaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolver(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.CfnResolver",
):
    '''A CloudFormation ``AWS::AppSync::Resolver``.

    The ``AWS::AppSync::Resolver`` resource defines the logical GraphQL resolver that you attach to fields in a schema. Request and response templates for resolvers are written in Apache Velocity Template Language (VTL) format. For more information about resolvers, see `Resolver Mapping Template Reference <https://docs.aws.amazon.com/appsync/latest/devguide/resolver-mapping-template-reference.html>`_ .
    .. epigraph::

       When you submit an update, AWS CloudFormation updates resources based on differences between what you submit and the stack's current template. To cause this resource to be updated you must change a property value for this resource in the CloudFormation template. Changing the Amazon S3 file content without changing a property value will not result in an update operation.

       See `Update Behaviors of Stack Resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html>`_ in the *AWS CloudFormation User Guide* .

    :cloudformationResource: AWS::AppSync::Resolver
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        cfn_resolver = appsync.CfnResolver(self, "MyCfnResolver",
            api_id="apiId",
            field_name="fieldName",
            type_name="typeName",
        
            # the properties below are optional
            caching_config=appsync.CfnResolver.CachingConfigProperty(
                ttl=123,
        
                # the properties below are optional
                caching_keys=["cachingKeys"]
            ),
            code="code",
            code_s3_location="codeS3Location",
            data_source_name="dataSourceName",
            kind="kind",
            max_batch_size=123,
            pipeline_config=appsync.CfnResolver.PipelineConfigProperty(
                functions=["functions"]
            ),
            request_mapping_template="requestMappingTemplate",
            request_mapping_template_s3_location="requestMappingTemplateS3Location",
            response_mapping_template="responseMappingTemplate",
            response_mapping_template_s3_location="responseMappingTemplateS3Location",
            runtime=appsync.CfnResolver.AppSyncRuntimeProperty(
                name="name",
                runtime_version="runtimeVersion"
            ),
            sync_config=appsync.CfnResolver.SyncConfigProperty(
                conflict_detection="conflictDetection",
        
                # the properties below are optional
                conflict_handler="conflictHandler",
                lambda_conflict_handler_config=appsync.CfnResolver.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        api_id: builtins.str,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[typing.Union["CfnResolver.CachingConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        code: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        pipeline_config: typing.Optional[typing.Union[typing.Union["CfnResolver.PipelineConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union[typing.Union["CfnResolver.AppSyncRuntimeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sync_config: typing.Optional[typing.Union[typing.Union["CfnResolver.SyncConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppSync::Resolver``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: The AWS AppSync GraphQL API to which you want to attach this resolver.
        :param field_name: The GraphQL field on a type that invokes the resolver.
        :param type_name: The GraphQL type that invokes this resolver.
        :param caching_config: The caching configuration for the resolver.
        :param code: The ``resolver`` code that contains the request and response functions. When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .
        :param code_s3_location: The Amazon S3 endpoint.
        :param data_source_name: The resolver data source name.
        :param kind: The resolver type. - *UNIT* : A UNIT resolver type. A UNIT resolver is the default resolver type. You can use a UNIT resolver to run a GraphQL query against a single data source. - *PIPELINE* : A PIPELINE resolver type. You can use a PIPELINE resolver to invoke a series of ``Function`` objects in a serial manner. You can use a pipeline resolver to run a GraphQL query against multiple data sources.
        :param max_batch_size: The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.
        :param pipeline_config: Functions linked with the pipeline resolver.
        :param request_mapping_template: The request mapping template. Request mapping templates are optional when using a Lambda data source. For all other data sources, a request mapping template is required.
        :param request_mapping_template_s3_location: The location of a request mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param response_mapping_template: The response mapping template.
        :param response_mapping_template_s3_location: The location of a response mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param runtime: Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function. Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.
        :param sync_config: The ``SyncConfig`` for a resolver attached to a versioned data source.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34883bfb7f0120bb0d5af960f9a86cf636e9b818fa745495955c56359acad5a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverProps(
            api_id=api_id,
            field_name=field_name,
            type_name=type_name,
            caching_config=caching_config,
            code=code,
            code_s3_location=code_s3_location,
            data_source_name=data_source_name,
            kind=kind,
            max_batch_size=max_batch_size,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            request_mapping_template_s3_location=request_mapping_template_s3_location,
            response_mapping_template=response_mapping_template,
            response_mapping_template_s3_location=response_mapping_template_s3_location,
            runtime=runtime,
            sync_config=sync_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c710480b97d448ed2b38cdd3b1f0871a5aa06435c05483beb296689896e18940)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f38295af893748bb923d7e848a7859e52805f74b244b9c41287834f096bd715)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFieldName")
    def attr_field_name(self) -> builtins.str:
        '''The GraphQL field on a type that invokes the resolver.

        :cloudformationAttribute: FieldName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFieldName"))

    @builtins.property
    @jsii.member(jsii_name="attrResolverArn")
    def attr_resolver_arn(self) -> builtins.str:
        '''ARN of the resolver, such as ``arn:aws:appsync:us-east-1:123456789012:apis/graphqlapiid/types/typename/resolvers/resolvername`` .

        :cloudformationAttribute: ResolverArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResolverArn"))

    @builtins.property
    @jsii.member(jsii_name="attrTypeName")
    def attr_type_name(self) -> builtins.str:
        '''The GraphQL type that invokes this resolver.

        :cloudformationAttribute: TypeName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTypeName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''The AWS AppSync GraphQL API to which you want to attach this resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-apiid
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791cf4a43a1e44e1b75cbf3c451962710226ca70b6d5b08520a28eaf0134e4a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="fieldName")
    def field_name(self) -> builtins.str:
        '''The GraphQL field on a type that invokes the resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-fieldname
        '''
        return typing.cast(builtins.str, jsii.get(self, "fieldName"))

    @field_name.setter
    def field_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ea86227c8edf0b5470f4331335f5453f5264c78ad6414340b36781b84f9c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldName", value)

    @builtins.property
    @jsii.member(jsii_name="typeName")
    def type_name(self) -> builtins.str:
        '''The GraphQL type that invokes this resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-typename
        '''
        return typing.cast(builtins.str, jsii.get(self, "typeName"))

    @type_name.setter
    def type_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff914f07b69b86703d1584f88f96c8313a81867391278a9b2b65f72c8a1e29cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "typeName", value)

    @builtins.property
    @jsii.member(jsii_name="cachingConfig")
    def caching_config(
        self,
    ) -> typing.Optional[typing.Union["CfnResolver.CachingConfigProperty", _IResolvable_a771d0ef]]:
        '''The caching configuration for the resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-cachingconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnResolver.CachingConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "cachingConfig"))

    @caching_config.setter
    def caching_config(
        self,
        value: typing.Optional[typing.Union["CfnResolver.CachingConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b44f0e8636b4db59d594d84c01eb1d917d11f4635534b53abc7139638075c0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cachingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Optional[builtins.str]:
        '''The ``resolver`` code that contains the request and response functions.

        When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-code
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "code"))

    @code.setter
    def code(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba238d284bacfd51ef130771d76490815e79c9ed8057d7e7a16f4bdf6e14f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="codeS3Location")
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-codes3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeS3Location"))

    @code_s3_location.setter
    def code_s3_location(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69d89718ecbadb2d8353e3b3709cffd0f705835b1c0ade46945924a921eddc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="dataSourceName")
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''The resolver data source name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-datasourcename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceName"))

    @data_source_name.setter
    def data_source_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03367193f799a1a52141c9666b4bdaa75d98f06abe7be9c4fb98785a926a78d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceName", value)

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> typing.Optional[builtins.str]:
        '''The resolver type.

        - *UNIT* : A UNIT resolver type. A UNIT resolver is the default resolver type. You can use a UNIT resolver to run a GraphQL query against a single data source.
        - *PIPELINE* : A PIPELINE resolver type. You can use a PIPELINE resolver to invoke a series of ``Function`` objects in a serial manner. You can use a pipeline resolver to run a GraphQL query against multiple data sources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-kind
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08edb19afb6f0c022ee3b57657785d74a0d82412e17c1d5deb9c62ac8207ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="maxBatchSize")
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-maxbatchsize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBatchSize"))

    @max_batch_size.setter
    def max_batch_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57316ff5e303e81df19142b4e37da5d3c01e7d624f84a850c0c220e2026a6b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBatchSize", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineConfig")
    def pipeline_config(
        self,
    ) -> typing.Optional[typing.Union["CfnResolver.PipelineConfigProperty", _IResolvable_a771d0ef]]:
        '''Functions linked with the pipeline resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-pipelineconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnResolver.PipelineConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "pipelineConfig"))

    @pipeline_config.setter
    def pipeline_config(
        self,
        value: typing.Optional[typing.Union["CfnResolver.PipelineConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5cc0ca3319d9c34dcd4eb08475f73ed73c6a3bc35920c82a0feb00cfe3d039a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineConfig", value)

    @builtins.property
    @jsii.member(jsii_name="requestMappingTemplate")
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The request mapping template.

        Request mapping templates are optional when using a Lambda data source. For all other data sources, a request mapping template is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-requestmappingtemplate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMappingTemplate"))

    @request_mapping_template.setter
    def request_mapping_template(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8132e260af6f20ed9ae1c3aa09202daf25ea3a81474c03dadf71b3a17b867b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMappingTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="requestMappingTemplateS3Location")
    def request_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a request mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-requestmappingtemplates3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestMappingTemplateS3Location"))

    @request_mapping_template_s3_location.setter
    def request_mapping_template_s3_location(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db6a5702988374594f917d7a5bb17ab6041e84750e78f5ddf4426c0350f4e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestMappingTemplateS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="responseMappingTemplate")
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The response mapping template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-responsemappingtemplate
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseMappingTemplate"))

    @response_mapping_template.setter
    def response_mapping_template(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fad24b55f173ceb2af4617f8e23f57fcfa3d9d8b31546b9585abf836ad75e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMappingTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="responseMappingTemplateS3Location")
    def response_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a response mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-responsemappingtemplates3location
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseMappingTemplateS3Location"))

    @response_mapping_template_s3_location.setter
    def response_mapping_template_s3_location(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcfc5b8755719e2fad9b19fef35ca73938cb6d70ce95495be2deedaa6442cb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseMappingTemplateS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(
        self,
    ) -> typing.Optional[typing.Union["CfnResolver.AppSyncRuntimeProperty", _IResolvable_a771d0ef]]:
        '''Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function.

        Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-runtime
        '''
        return typing.cast(typing.Optional[typing.Union["CfnResolver.AppSyncRuntimeProperty", _IResolvable_a771d0ef]], jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(
        self,
        value: typing.Optional[typing.Union["CfnResolver.AppSyncRuntimeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e092e546a7dd65912c5e6f79c561886b0c0721c1dd87de45894ee68e73ae640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="syncConfig")
    def sync_config(
        self,
    ) -> typing.Optional[typing.Union["CfnResolver.SyncConfigProperty", _IResolvable_a771d0ef]]:
        '''The ``SyncConfig`` for a resolver attached to a versioned data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-syncconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnResolver.SyncConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "syncConfig"))

    @sync_config.setter
    def sync_config(
        self,
        value: typing.Optional[typing.Union["CfnResolver.SyncConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a81ae3cdbcea9dc095123c0ebd20c3df7dd01ff2791b0bd239fcf580d898bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnResolver.AppSyncRuntimeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "runtime_version": "runtimeVersion"},
    )
    class AppSyncRuntimeProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            runtime_version: builtins.str,
        ) -> None:
            '''Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function.

            Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

            :param name: The ``name`` of the runtime to use. Currently, the only allowed value is ``APPSYNC_JS`` .
            :param runtime_version: The ``version`` of the runtime to use. Currently, the only allowed version is ``1.0.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-appsyncruntime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                app_sync_runtime_property = appsync.CfnResolver.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f54559dfeaa08bacc61e5fdc1f1d74730e7fd31f6c091a3b1357b8ef5418a3b9)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "runtime_version": runtime_version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The ``name`` of the runtime to use.

            Currently, the only allowed value is ``APPSYNC_JS`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-appsyncruntime.html#cfn-appsync-resolver-appsyncruntime-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def runtime_version(self) -> builtins.str:
            '''The ``version`` of the runtime to use.

            Currently, the only allowed version is ``1.0.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-appsyncruntime.html#cfn-appsync-resolver-appsyncruntime-runtimeversion
            '''
            result = self._values.get("runtime_version")
            assert result is not None, "Required property 'runtime_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppSyncRuntimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnResolver.CachingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl", "caching_keys": "cachingKeys"},
    )
    class CachingConfigProperty:
        def __init__(
            self,
            *,
            ttl: jsii.Number,
            caching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The caching configuration for a resolver that has caching activated.

            :param ttl: The TTL in seconds for a resolver that has caching activated. Valid values are 1–3,600 seconds.
            :param caching_keys: The caching keys for a resolver that has caching activated. Valid values are entries from the ``$context.arguments`` , ``$context.source`` , and ``$context.identity`` maps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-cachingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                caching_config_property = appsync.CfnResolver.CachingConfigProperty(
                    ttl=123,
                
                    # the properties below are optional
                    caching_keys=["cachingKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdca5b7bc5b314edaca5250353503ca5256d902a79fba3f85e74283bcb16e223)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
                check_type(argname="argument caching_keys", value=caching_keys, expected_type=type_hints["caching_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "ttl": ttl,
            }
            if caching_keys is not None:
                self._values["caching_keys"] = caching_keys

        @builtins.property
        def ttl(self) -> jsii.Number:
            '''The TTL in seconds for a resolver that has caching activated.

            Valid values are 1–3,600 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-cachingconfig.html#cfn-appsync-resolver-cachingconfig-ttl
            '''
            result = self._values.get("ttl")
            assert result is not None, "Required property 'ttl' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def caching_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The caching keys for a resolver that has caching activated.

            Valid values are entries from the ``$context.arguments`` , ``$context.source`` , and ``$context.identity`` maps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-cachingconfig.html#cfn-appsync-resolver-cachingconfig-cachingkeys
            '''
            result = self._values.get("caching_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CachingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnResolver.LambdaConflictHandlerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"lambda_conflict_handler_arn": "lambdaConflictHandlerArn"},
    )
    class LambdaConflictHandlerConfigProperty:
        def __init__(
            self,
            *,
            lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

            :param lambda_conflict_handler_arn: The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-lambdaconflicthandlerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                lambda_conflict_handler_config_property = appsync.CfnResolver.LambdaConflictHandlerConfigProperty(
                    lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__330290c3d36654285b554cdf4cb3be0e3300ec57ece1e2ace69b5b59a7517738)
                check_type(argname="argument lambda_conflict_handler_arn", value=lambda_conflict_handler_arn, expected_type=type_hints["lambda_conflict_handler_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lambda_conflict_handler_arn is not None:
                self._values["lambda_conflict_handler_arn"] = lambda_conflict_handler_arn

        @builtins.property
        def lambda_conflict_handler_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the Lambda function to use as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-lambdaconflicthandlerconfig.html#cfn-appsync-resolver-lambdaconflicthandlerconfig-lambdaconflicthandlerarn
            '''
            result = self._values.get("lambda_conflict_handler_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConflictHandlerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnResolver.PipelineConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"functions": "functions"},
    )
    class PipelineConfigProperty:
        def __init__(
            self,
            *,
            functions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Use the ``PipelineConfig`` property type to specify ``PipelineConfig`` for an AWS AppSync resolver.

            ``PipelineConfig`` is a property of the `AWS::AppSync::Resolver <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html>`_ resource.

            :param functions: A list of ``Function`` objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-pipelineconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                pipeline_config_property = appsync.CfnResolver.PipelineConfigProperty(
                    functions=["functions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79362fd469794e6596313597ab8e4a291d2dddf9a81b1e882c44e9bbaf1253bd)
                check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if functions is not None:
                self._values["functions"] = functions

        @builtins.property
        def functions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of ``Function`` objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-pipelineconfig.html#cfn-appsync-resolver-pipelineconfig-functions
            '''
            result = self._values.get("functions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PipelineConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appsync.CfnResolver.SyncConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "conflict_detection": "conflictDetection",
            "conflict_handler": "conflictHandler",
            "lambda_conflict_handler_config": "lambdaConflictHandlerConfig",
        },
    )
    class SyncConfigProperty:
        def __init__(
            self,
            *,
            conflict_detection: builtins.str,
            conflict_handler: typing.Optional[builtins.str] = None,
            lambda_conflict_handler_config: typing.Optional[typing.Union[typing.Union["CfnResolver.LambdaConflictHandlerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes a Sync configuration for a resolver.

            Specifies which Conflict Detection strategy and Resolution strategy to use when the resolver is invoked.

            :param conflict_detection: The Conflict Detection strategy to use. - *VERSION* : Detect conflicts based on object versions for this resolver. - *NONE* : Do not detect conflicts when invoking this resolver.
            :param conflict_handler: The Conflict Resolution strategy to perform in the event of a conflict. - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server. - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy. - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .
            :param lambda_conflict_handler_config: The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appsync as appsync
                
                sync_config_property = appsync.CfnResolver.SyncConfigProperty(
                    conflict_detection="conflictDetection",
                
                    # the properties below are optional
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync.CfnResolver.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04c1b8054b7e9962c4d63617b26af2796e76db8476ff424bef0e46ba4c24c255)
                check_type(argname="argument conflict_detection", value=conflict_detection, expected_type=type_hints["conflict_detection"])
                check_type(argname="argument conflict_handler", value=conflict_handler, expected_type=type_hints["conflict_handler"])
                check_type(argname="argument lambda_conflict_handler_config", value=lambda_conflict_handler_config, expected_type=type_hints["lambda_conflict_handler_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "conflict_detection": conflict_detection,
            }
            if conflict_handler is not None:
                self._values["conflict_handler"] = conflict_handler
            if lambda_conflict_handler_config is not None:
                self._values["lambda_conflict_handler_config"] = lambda_conflict_handler_config

        @builtins.property
        def conflict_detection(self) -> builtins.str:
            '''The Conflict Detection strategy to use.

            - *VERSION* : Detect conflicts based on object versions for this resolver.
            - *NONE* : Do not detect conflicts when invoking this resolver.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html#cfn-appsync-resolver-syncconfig-conflictdetection
            '''
            result = self._values.get("conflict_detection")
            assert result is not None, "Required property 'conflict_detection' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def conflict_handler(self) -> typing.Optional[builtins.str]:
            '''The Conflict Resolution strategy to perform in the event of a conflict.

            - *OPTIMISTIC_CONCURRENCY* : Resolve conflicts by rejecting mutations when versions don't match the latest version at the server.
            - *AUTOMERGE* : Resolve conflicts with the Automerge conflict resolution strategy.
            - *LAMBDA* : Resolve conflicts with an AWS Lambda function supplied in the ``LambdaConflictHandlerConfig`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html#cfn-appsync-resolver-syncconfig-conflicthandler
            '''
            result = self._values.get("conflict_handler")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_conflict_handler_config(
            self,
        ) -> typing.Optional[typing.Union["CfnResolver.LambdaConflictHandlerConfigProperty", _IResolvable_a771d0ef]]:
            '''The ``LambdaConflictHandlerConfig`` when configuring ``LAMBDA`` as the Conflict Handler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-resolver-syncconfig.html#cfn-appsync-resolver-syncconfig-lambdaconflicthandlerconfig
            '''
            result = self._values.get("lambda_conflict_handler_config")
            return typing.cast(typing.Optional[typing.Union["CfnResolver.LambdaConflictHandlerConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SyncConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.CfnResolverProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_id": "apiId",
        "field_name": "fieldName",
        "type_name": "typeName",
        "caching_config": "cachingConfig",
        "code": "code",
        "code_s3_location": "codeS3Location",
        "data_source_name": "dataSourceName",
        "kind": "kind",
        "max_batch_size": "maxBatchSize",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "request_mapping_template_s3_location": "requestMappingTemplateS3Location",
        "response_mapping_template": "responseMappingTemplate",
        "response_mapping_template_s3_location": "responseMappingTemplateS3Location",
        "runtime": "runtime",
        "sync_config": "syncConfig",
    },
)
class CfnResolverProps:
    def __init__(
        self,
        *,
        api_id: builtins.str,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[typing.Union[CfnResolver.CachingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        code: typing.Optional[builtins.str] = None,
        code_s3_location: typing.Optional[builtins.str] = None,
        data_source_name: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        max_batch_size: typing.Optional[jsii.Number] = None,
        pipeline_config: typing.Optional[typing.Union[typing.Union[CfnResolver.PipelineConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        request_mapping_template: typing.Optional[builtins.str] = None,
        request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        response_mapping_template: typing.Optional[builtins.str] = None,
        response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[typing.Union[typing.Union[CfnResolver.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sync_config: typing.Optional[typing.Union[typing.Union[CfnResolver.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResolver``.

        :param api_id: The AWS AppSync GraphQL API to which you want to attach this resolver.
        :param field_name: The GraphQL field on a type that invokes the resolver.
        :param type_name: The GraphQL type that invokes this resolver.
        :param caching_config: The caching configuration for the resolver.
        :param code: The ``resolver`` code that contains the request and response functions. When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .
        :param code_s3_location: The Amazon S3 endpoint.
        :param data_source_name: The resolver data source name.
        :param kind: The resolver type. - *UNIT* : A UNIT resolver type. A UNIT resolver is the default resolver type. You can use a UNIT resolver to run a GraphQL query against a single data source. - *PIPELINE* : A PIPELINE resolver type. You can use a PIPELINE resolver to invoke a series of ``Function`` objects in a serial manner. You can use a pipeline resolver to run a GraphQL query against multiple data sources.
        :param max_batch_size: The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.
        :param pipeline_config: Functions linked with the pipeline resolver.
        :param request_mapping_template: The request mapping template. Request mapping templates are optional when using a Lambda data source. For all other data sources, a request mapping template is required.
        :param request_mapping_template_s3_location: The location of a request mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param response_mapping_template: The response mapping template.
        :param response_mapping_template_s3_location: The location of a response mapping template in an Amazon S3 bucket. Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.
        :param runtime: Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function. Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.
        :param sync_config: The ``SyncConfig`` for a resolver attached to a versioned data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            cfn_resolver_props = appsync.CfnResolverProps(
                api_id="apiId",
                field_name="fieldName",
                type_name="typeName",
            
                # the properties below are optional
                caching_config=appsync.CfnResolver.CachingConfigProperty(
                    ttl=123,
            
                    # the properties below are optional
                    caching_keys=["cachingKeys"]
                ),
                code="code",
                code_s3_location="codeS3Location",
                data_source_name="dataSourceName",
                kind="kind",
                max_batch_size=123,
                pipeline_config=appsync.CfnResolver.PipelineConfigProperty(
                    functions=["functions"]
                ),
                request_mapping_template="requestMappingTemplate",
                request_mapping_template_s3_location="requestMappingTemplateS3Location",
                response_mapping_template="responseMappingTemplate",
                response_mapping_template_s3_location="responseMappingTemplateS3Location",
                runtime=appsync.CfnResolver.AppSyncRuntimeProperty(
                    name="name",
                    runtime_version="runtimeVersion"
                ),
                sync_config=appsync.CfnResolver.SyncConfigProperty(
                    conflict_detection="conflictDetection",
            
                    # the properties below are optional
                    conflict_handler="conflictHandler",
                    lambda_conflict_handler_config=appsync.CfnResolver.LambdaConflictHandlerConfigProperty(
                        lambda_conflict_handler_arn="lambdaConflictHandlerArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4ced33d747cc766f0f9ad98e6d46cb4cf1d9d2b3d3f6df2510542f97ff6f7b)
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument caching_config", value=caching_config, expected_type=type_hints["caching_config"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument code_s3_location", value=code_s3_location, expected_type=type_hints["code_s3_location"])
            check_type(argname="argument data_source_name", value=data_source_name, expected_type=type_hints["data_source_name"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument max_batch_size", value=max_batch_size, expected_type=type_hints["max_batch_size"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument request_mapping_template_s3_location", value=request_mapping_template_s3_location, expected_type=type_hints["request_mapping_template_s3_location"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument response_mapping_template_s3_location", value=response_mapping_template_s3_location, expected_type=type_hints["response_mapping_template_s3_location"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument sync_config", value=sync_config, expected_type=type_hints["sync_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
            "field_name": field_name,
            "type_name": type_name,
        }
        if caching_config is not None:
            self._values["caching_config"] = caching_config
        if code is not None:
            self._values["code"] = code
        if code_s3_location is not None:
            self._values["code_s3_location"] = code_s3_location
        if data_source_name is not None:
            self._values["data_source_name"] = data_source_name
        if kind is not None:
            self._values["kind"] = kind
        if max_batch_size is not None:
            self._values["max_batch_size"] = max_batch_size
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if request_mapping_template_s3_location is not None:
            self._values["request_mapping_template_s3_location"] = request_mapping_template_s3_location
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if response_mapping_template_s3_location is not None:
            self._values["response_mapping_template_s3_location"] = response_mapping_template_s3_location
        if runtime is not None:
            self._values["runtime"] = runtime
        if sync_config is not None:
            self._values["sync_config"] = sync_config

    @builtins.property
    def api_id(self) -> builtins.str:
        '''The AWS AppSync GraphQL API to which you want to attach this resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-apiid
        '''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field_name(self) -> builtins.str:
        '''The GraphQL field on a type that invokes the resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-fieldname
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''The GraphQL type that invokes this resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-typename
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caching_config(
        self,
    ) -> typing.Optional[typing.Union[CfnResolver.CachingConfigProperty, _IResolvable_a771d0ef]]:
        '''The caching configuration for the resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-cachingconfig
        '''
        result = self._values.get("caching_config")
        return typing.cast(typing.Optional[typing.Union[CfnResolver.CachingConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def code(self) -> typing.Optional[builtins.str]:
        '''The ``resolver`` code that contains the request and response functions.

        When code is used, the ``runtime`` is required. The runtime value must be ``APPSYNC_JS`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_s3_location(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-codes3location
        '''
        result = self._values.get("code_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source_name(self) -> typing.Optional[builtins.str]:
        '''The resolver data source name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-datasourcename
        '''
        result = self._values.get("data_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''The resolver type.

        - *UNIT* : A UNIT resolver type. A UNIT resolver is the default resolver type. You can use a UNIT resolver to run a GraphQL query against a single data source.
        - *PIPELINE* : A PIPELINE resolver type. You can use a PIPELINE resolver to invoke a series of ``Function`` objects in a serial manner. You can use a pipeline resolver to run a GraphQL query against multiple data sources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-kind
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batch_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resolver request inputs that will be sent to a single AWS Lambda function in a ``BatchInvoke`` operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-maxbatchsize
        '''
        result = self._values.get("max_batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pipeline_config(
        self,
    ) -> typing.Optional[typing.Union[CfnResolver.PipelineConfigProperty, _IResolvable_a771d0ef]]:
        '''Functions linked with the pipeline resolver.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-pipelineconfig
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.Union[CfnResolver.PipelineConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The request mapping template.

        Request mapping templates are optional when using a Lambda data source. For all other data sources, a request mapping template is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-requestmappingtemplate
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a request mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-requestmappingtemplates3location
        '''
        result = self._values.get("request_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[builtins.str]:
        '''The response mapping template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-responsemappingtemplate
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_mapping_template_s3_location(self) -> typing.Optional[builtins.str]:
        '''The location of a response mapping template in an Amazon S3 bucket.

        Use this if you want to provision with a template file in Amazon S3 rather than embedding it in your CloudFormation template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-responsemappingtemplates3location
        '''
        result = self._values.get("response_mapping_template_s3_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(
        self,
    ) -> typing.Optional[typing.Union[CfnResolver.AppSyncRuntimeProperty, _IResolvable_a771d0ef]]:
        '''Describes a runtime used by an AWS AppSync pipeline resolver or AWS AppSync function.

        Specifies the name and version of the runtime to use. Note that if a runtime is specified, code must also be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-runtime
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[typing.Union[CfnResolver.AppSyncRuntimeProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sync_config(
        self,
    ) -> typing.Optional[typing.Union[CfnResolver.SyncConfigProperty, _IResolvable_a771d0ef]]:
        '''The ``SyncConfig`` for a resolver attached to a versioned data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appsync-resolver.html#cfn-appsync-resolver-syncconfig
        '''
        result = self._values.get("sync_config")
        return typing.cast(typing.Optional[typing.Union[CfnResolver.SyncConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.DataSourceOptions",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name"},
)
class DataSourceOptions:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Optional configuration for data sources.

        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            data_source_options = appsync.DataSourceOptions(
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9892dac165c1272701c637c8e62590681d37f17384047fecdad4f07f602adb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the data source.

        :default: - No description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source, overrides the id given by cdk.

        :default: - generated by cdk given the id

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Directive(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.Directive"):
    '''(experimental) Directives for types.

    i.e. @aws_iam or @aws_subscribe

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # film: appsync.InterfaceType
        
        
        api.add_subscription("addedFilm", appsync.Field(
            return_type=film.attribute(),
            args={"id": appsync.GraphqlType.id(is_required=True)},
            directives=[appsync.Directive.subscribe("addFilm")]
        ))
    '''

    @jsii.member(jsii_name="apiKey")
    @builtins.classmethod
    def api_key(cls) -> "Directive":
        '''(experimental) Add the @aws_api_key directive.

        :stability: experimental
        '''
        return typing.cast("Directive", jsii.sinvoke(cls, "apiKey", []))

    @jsii.member(jsii_name="cognito")
    @builtins.classmethod
    def cognito(cls, *groups: builtins.str) -> "Directive":
        '''(experimental) Add the @aws_auth or @aws_cognito_user_pools directive.

        :param groups: the groups to allow access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4be52408fddbab98926376259cafdceaea556086e9a4c1ab88eaf9ec60dfab8)
            check_type(argname="argument groups", value=groups, expected_type=typing.Tuple[type_hints["groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Directive", jsii.sinvoke(cls, "cognito", [*groups]))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, statement: builtins.str) -> "Directive":
        '''(experimental) Add a custom directive.

        :param statement: - the directive statement to append.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56ae66cd66ef66cdd0423e92601632209454b6f1fa3bc05e28bf7da1c8ccde5)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast("Directive", jsii.sinvoke(cls, "custom", [statement]))

    @jsii.member(jsii_name="iam")
    @builtins.classmethod
    def iam(cls) -> "Directive":
        '''(experimental) Add the @aws_iam directive.

        :stability: experimental
        '''
        return typing.cast("Directive", jsii.sinvoke(cls, "iam", []))

    @jsii.member(jsii_name="oidc")
    @builtins.classmethod
    def oidc(cls) -> "Directive":
        '''(experimental) Add the @aws_oidc directive.

        :stability: experimental
        '''
        return typing.cast("Directive", jsii.sinvoke(cls, "oidc", []))

    @jsii.member(jsii_name="subscribe")
    @builtins.classmethod
    def subscribe(cls, *mutations: builtins.str) -> "Directive":
        '''(experimental) Add the @aws_subscribe directive.

        Only use for top level Subscription type.

        :param mutations: the mutation fields to link to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823b1bc735e936ae5d5483a1a44ec24f6bbb5d723075451b78190757888ed1ac)
            check_type(argname="argument mutations", value=mutations, expected_type=typing.Tuple[type_hints["mutations"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("Directive", jsii.sinvoke(cls, "subscribe", [*mutations]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the directive statement.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> typing.Optional[AuthorizationType]:
        '''(experimental) The authorization type of this directive.

        :default: - not an authorization directive

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AuthorizationType], jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="mutationFields")
    def mutation_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Mutation fields for a subscription directive.

        :default: - not a subscription directive

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "mutationFields"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(self) -> typing.Optional[typing.List[AuthorizationType]]:
        '''(experimental) the authorization modes for this intermediate type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(self, value: typing.Optional[typing.List[AuthorizationType]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbdf73f1105c55f67f62a27be6a13dd2d39ad2d0fa8040276e3cff33c6dd5c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.DomainOptions",
    jsii_struct_bases=[],
    name_mapping={"certificate": "certificate", "domain_name": "domainName"},
)
class DomainOptions:
    def __init__(
        self,
        *,
        certificate: _ICertificate_c7bbdc16,
        domain_name: builtins.str,
    ) -> None:
        '''(experimental) Domain name configuration for AppSync.

        :param certificate: (experimental) The certificate to use with the domain name.
        :param domain_name: (experimental) The actual domain name. For example, ``api.example.com``.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as acm
            import monocdk as route53
            
            # hosted zone and route53 features
            # hosted_zone_id: str
            zone_name = "example.com"
            
            
            my_domain_name = "api.example.com"
            certificate = acm.Certificate(self, "cert", domain_name=my_domain_name)
            api = appsync.GraphqlApi(self, "api",
                name="myApi",
                domain_name=acm.aws_appsync.DomainOptions(
                    certificate=certificate,
                    domain_name=my_domain_name
                )
            )
            
            # hosted zone for adding appsync domain
            zone = route53.HostedZone.from_hosted_zone_attributes(self, "HostedZone",
                hosted_zone_id=hosted_zone_id,
                zone_name=zone_name
            )
            
            # create a cname to the appsync domain. will map to something like xxxx.cloudfront.net
            route53.CnameRecord(self, "CnameApiRecord",
                record_name="api",
                zone=zone,
                domain_name=my_domain_name
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34addc08275c25f75760c0971b40e94f68344d17a1523bc6047bc32d8cca48c7)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "certificate": certificate,
            "domain_name": domain_name,
        }

    @builtins.property
    def certificate(self) -> _ICertificate_c7bbdc16:
        '''(experimental) The certificate to use with the domain name.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(_ICertificate_c7bbdc16, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) The actual domain name.

        For example, ``api.example.com``.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.EnumTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition"},
)
class EnumTypeOptions:
    def __init__(self, *, definition: typing.Sequence[builtins.str]) -> None:
        '''(experimental) Properties for configuring an Enum Type.

        :param definition: (experimental) the attributes of this type.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            
            episode = appsync.EnumType("Episode",
                definition=["NEWHOPE", "EMPIRE", "JEDI"
                ]
            )
            api.add_type(episode)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d086f0499f4f7ca70a13b9fd88c7674d643c2031d7257458cfae84a3bece9bef)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }

    @builtins.property
    def definition(self) -> typing.List[builtins.str]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnumTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ExtendedDataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "dynamo_db_config": "dynamoDbConfig",
        "elasticsearch_config": "elasticsearchConfig",
        "http_config": "httpConfig",
        "lambda_config": "lambdaConfig",
        "open_search_service_config": "openSearchServiceConfig",
        "relational_database_config": "relationalDatabaseConfig",
    },
)
class ExtendedDataSourceProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''(experimental) props used by implementations of BaseDataSource to provide configuration.

        Should not be used directly.

        :param type: (experimental) the type of the AppSync datasource.
        :param dynamo_db_config: (experimental) configuration for DynamoDB Datasource. Default: - No config
        :param elasticsearch_config: (deprecated) configuration for Elasticsearch data source. Default: - No config
        :param http_config: (experimental) configuration for HTTP Datasource. Default: - No config
        :param lambda_config: (experimental) configuration for Lambda Datasource. Default: - No config
        :param open_search_service_config: (experimental) configuration for OpenSearch data source. Default: - No config
        :param relational_database_config: (experimental) configuration for RDS Datasource. Default: - No config

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            extended_data_source_props = appsync.ExtendedDataSourceProps(
                type="type",
            
                # the properties below are optional
                dynamo_db_config=appsync.CfnDataSource.DynamoDBConfigProperty(
                    aws_region="awsRegion",
                    table_name="tableName",
            
                    # the properties below are optional
                    delta_sync_config=appsync.CfnDataSource.DeltaSyncConfigProperty(
                        base_table_ttl="baseTableTtl",
                        delta_sync_table_name="deltaSyncTableName",
                        delta_sync_table_ttl="deltaSyncTableTtl"
                    ),
                    use_caller_credentials=False,
                    versioned=False
                ),
                elasticsearch_config=appsync.CfnDataSource.ElasticsearchConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                ),
                http_config=appsync.CfnDataSource.HttpConfigProperty(
                    endpoint="endpoint",
            
                    # the properties below are optional
                    authorization_config=appsync.CfnDataSource.AuthorizationConfigProperty(
                        authorization_type="authorizationType",
            
                        # the properties below are optional
                        aws_iam_config=appsync.CfnDataSource.AwsIamConfigProperty(
                            signing_region="signingRegion",
                            signing_service_name="signingServiceName"
                        )
                    )
                ),
                lambda_config=appsync.CfnDataSource.LambdaConfigProperty(
                    lambda_function_arn="lambdaFunctionArn"
                ),
                open_search_service_config=appsync.CfnDataSource.OpenSearchServiceConfigProperty(
                    aws_region="awsRegion",
                    endpoint="endpoint"
                ),
                relational_database_config=appsync.CfnDataSource.RelationalDatabaseConfigProperty(
                    relational_database_source_type="relationalDatabaseSourceType",
            
                    # the properties below are optional
                    rds_http_endpoint_config=appsync.CfnDataSource.RdsHttpEndpointConfigProperty(
                        aws_region="awsRegion",
                        aws_secret_store_arn="awsSecretStoreArn",
                        db_cluster_identifier="dbClusterIdentifier",
            
                        # the properties below are optional
                        database_name="databaseName",
                        schema="schema"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e431f01e6bb0d5cf5b60971f759568ca1a6ce96bf590b6d505f1a34397ac3074)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument dynamo_db_config", value=dynamo_db_config, expected_type=type_hints["dynamo_db_config"])
            check_type(argname="argument elasticsearch_config", value=elasticsearch_config, expected_type=type_hints["elasticsearch_config"])
            check_type(argname="argument http_config", value=http_config, expected_type=type_hints["http_config"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            check_type(argname="argument open_search_service_config", value=open_search_service_config, expected_type=type_hints["open_search_service_config"])
            check_type(argname="argument relational_database_config", value=relational_database_config, expected_type=type_hints["relational_database_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if dynamo_db_config is not None:
            self._values["dynamo_db_config"] = dynamo_db_config
        if elasticsearch_config is not None:
            self._values["elasticsearch_config"] = elasticsearch_config
        if http_config is not None:
            self._values["http_config"] = http_config
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if open_search_service_config is not None:
            self._values["open_search_service_config"] = open_search_service_config
        if relational_database_config is not None:
            self._values["relational_database_config"] = relational_database_config

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) the type of the AppSync datasource.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dynamo_db_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.DynamoDBConfigProperty, _IResolvable_a771d0ef]]:
        '''(experimental) configuration for DynamoDB Datasource.

        :default: - No config

        :stability: experimental
        '''
        result = self._values.get("dynamo_db_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.DynamoDBConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def elasticsearch_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.ElasticsearchConfigProperty, _IResolvable_a771d0ef]]:
        '''(deprecated) configuration for Elasticsearch data source.

        :default: - No config

        :deprecated: - use ``openSearchConfig``

        :stability: deprecated
        '''
        result = self._values.get("elasticsearch_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.ElasticsearchConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def http_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.HttpConfigProperty, _IResolvable_a771d0ef]]:
        '''(experimental) configuration for HTTP Datasource.

        :default: - No config

        :stability: experimental
        '''
        result = self._values.get("http_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.HttpConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def lambda_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.LambdaConfigProperty, _IResolvable_a771d0ef]]:
        '''(experimental) configuration for Lambda Datasource.

        :default: - No config

        :stability: experimental
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.LambdaConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def open_search_service_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, _IResolvable_a771d0ef]]:
        '''(experimental) configuration for OpenSearch data source.

        :default: - No config

        :stability: experimental
        '''
        result = self._values.get("open_search_service_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def relational_database_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, _IResolvable_a771d0ef]]:
        '''(experimental) configuration for RDS Datasource.

        :default: - No config

        :stability: experimental
        '''
        result = self._values.get("relational_database_config")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExtendedDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ExtendedResolverProps",
    jsii_struct_bases=[BaseResolverProps],
    name_mapping={
        "field_name": "fieldName",
        "type_name": "typeName",
        "caching_config": "cachingConfig",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
        "data_source": "dataSource",
    },
)
class ExtendedResolverProps(BaseResolverProps):
    def __init__(
        self,
        *,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence["IAppsyncFunction"]] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
        data_source: typing.Optional[BaseDataSource] = None,
    ) -> None:
        '''(experimental) Additional property for an AppSync resolver for data source reference.

        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template
        :param data_source: (experimental) The data source this resolver is using. Default: - No datasource

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_appsync as appsync
            
            # appsync_function: appsync.AppsyncFunction
            # base_data_source: appsync.BaseDataSource
            # duration: monocdk.Duration
            # mapping_template: appsync.MappingTemplate
            
            extended_resolver_props = appsync.ExtendedResolverProps(
                field_name="fieldName",
                type_name="typeName",
            
                # the properties below are optional
                caching_config=appsync.CachingConfig(
                    ttl=duration,
            
                    # the properties below are optional
                    caching_keys=["cachingKeys"]
                ),
                data_source=base_data_source,
                pipeline_config=[appsync_function],
                request_mapping_template=mapping_template,
                response_mapping_template=mapping_template
            )
        '''
        if isinstance(caching_config, dict):
            caching_config = CachingConfig(**caching_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981882565e0c540777bba530f3f7716a431fc981bf4a32df207ec3258ba0d0cb)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument caching_config", value=caching_config, expected_type=type_hints["caching_config"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_name": field_name,
            "type_name": type_name,
        }
        if caching_config is not None:
            self._values["caching_config"] = caching_config
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if data_source is not None:
            self._values["data_source"] = data_source

    @builtins.property
    def field_name(self) -> builtins.str:
        '''(experimental) name of the GraphQL field in the given type this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''(experimental) name of the GraphQL type this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caching_config(self) -> typing.Optional[CachingConfig]:
        '''(experimental) The caching configuration for this resolver.

        :default: - No caching configuration

        :stability: experimental
        '''
        result = self._values.get("caching_config")
        return typing.cast(typing.Optional[CachingConfig], result)

    @builtins.property
    def pipeline_config(self) -> typing.Optional[typing.List["IAppsyncFunction"]]:
        '''(experimental) configuration of the pipeline resolver.

        :default:

        - no pipeline resolver configuration
        An empty array | undefined sets resolver to be of kind, unit

        :stability: experimental
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.List["IAppsyncFunction"]], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional["MappingTemplate"]:
        '''(experimental) The request mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional["MappingTemplate"], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional["MappingTemplate"]:
        '''(experimental) The response mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional["MappingTemplate"], result)

    @builtins.property
    def data_source(self) -> typing.Optional[BaseDataSource]:
        '''(experimental) The data source this resolver is using.

        :default: - No datasource

        :stability: experimental
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[BaseDataSource], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExtendedResolverProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_appsync.FieldLogLevel")
class FieldLogLevel(enum.Enum):
    '''(experimental) log-level for fields in AppSync.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) No logging.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) Error logging.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) All logging.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.FieldOptions",
    jsii_struct_bases=[],
    name_mapping={
        "return_type": "returnType",
        "args": "args",
        "directives": "directives",
    },
)
class FieldOptions:
    def __init__(
        self,
        *,
        return_type: "GraphqlType",
        args: typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''(experimental) Properties for configuring a field.

        :param return_type: (experimental) The return type for this field.
        :param args: (experimental) The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: (experimental) the directives for this field. Default: - no directives

        :stability: experimental
        :options:

        args - the variables and types that define the arguments

        i.e. { string: GraphqlType, string: GraphqlType }
        :exampleMetadata: infused

        Example::

            field = appsync.Field(
                return_type=appsync.GraphqlType.string(),
                args={
                    "argument": appsync.GraphqlType.string()
                }
            )
            type = appsync.InterfaceType("Node",
                definition={"test": field}
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e857771cf3c9a89258fbc8a976608ad4380bafec6b66b6175f06a22860a1f2e1)
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "return_type": return_type,
        }
        if args is not None:
            self._values["args"] = args
        if directives is not None:
            self._values["directives"] = directives

    @builtins.property
    def return_type(self) -> "GraphqlType":
        '''(experimental) The return type for this field.

        :stability: experimental
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast("GraphqlType", result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]]:
        '''(experimental) The arguments for this field.

        i.e. type Example (first: String second: String) {}

        - where 'first' and 'second' are key values for args
          and 'String' is the GraphqlType

        :default: - no arguments

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this field.

        :default: - no directives

        :stability: experimental
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FieldOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.GraphqlApiAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "graphql_api_id": "graphqlApiId",
        "graphql_api_arn": "graphqlApiArn",
    },
)
class GraphqlApiAttributes:
    def __init__(
        self,
        *,
        graphql_api_id: builtins.str,
        graphql_api_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Attributes for GraphQL imports.

        :param graphql_api_id: (experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.
        :param graphql_api_arn: (experimental) the arn for the GraphQL Api. Default: - autogenerated arn

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            # table: dynamodb.Table
            
            imported_api = appsync.GraphqlApi.from_graphql_api_attributes(self, "IApi",
                graphql_api_id=api.api_id,
                graphql_api_arn=api.arn
            )
            imported_api.add_dynamo_db_data_source("TableDataSource", table)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816b596f025d22de0b0f651c4c270bfb954f4e8c9ffb534ab26606125c2d0752)
            check_type(argname="argument graphql_api_id", value=graphql_api_id, expected_type=type_hints["graphql_api_id"])
            check_type(argname="argument graphql_api_arn", value=graphql_api_arn, expected_type=type_hints["graphql_api_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "graphql_api_id": graphql_api_id,
        }
        if graphql_api_arn is not None:
            self._values["graphql_api_arn"] = graphql_api_arn

    @builtins.property
    def graphql_api_id(self) -> builtins.str:
        '''(experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.

        :stability: experimental
        '''
        result = self._values.get("graphql_api_id")
        assert result is not None, "Required property 'graphql_api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def graphql_api_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) the arn for the GraphQL Api.

        :default: - autogenerated arn

        :stability: experimental
        '''
        result = self._values.get("graphql_api_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlApiAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.GraphqlApiProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "authorization_config": "authorizationConfig",
        "domain_name": "domainName",
        "log_config": "logConfig",
        "schema": "schema",
        "xray_enabled": "xrayEnabled",
    },
)
class GraphqlApiProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        authorization_config: typing.Optional[typing.Union[AuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_name: typing.Optional[typing.Union[DomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union["LogConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        schema: typing.Optional["Schema"] = None,
        xray_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for an AppSync GraphQL API.

        :param name: (experimental) the name of the GraphQL API.
        :param authorization_config: (experimental) Optional authorization configuration. Default: - API Key authorization
        :param domain_name: (experimental) The domain name configuration for the GraphQL API. The Route 53 hosted zone and CName DNS record must be configured in addition to this setting to enable custom domain URL Default: - no domain name
        :param log_config: (experimental) Logging configuration for this api. Default: - None
        :param schema: (experimental) GraphQL schema definition. Specify how you want to define your schema. Schema.fromFile(filePath: string) allows schema definition through schema.graphql file Default: - schema will be generated code-first (i.e. addType, addObjectType, etc.)
        :param xray_enabled: (experimental) A flag indicating whether or not X-Ray tracing is enabled for the GraphQL API. Default: - false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            api = appsync.GraphqlApi(self, "Api",
                name="demo"
            )
            demo = appsync.ObjectType("Demo",
                definition={
                    "id": appsync.GraphqlType.string(is_required=True),
                    "version": appsync.GraphqlType.string(is_required=True)
                }
            )
            
            api.add_type(demo)
        '''
        if isinstance(authorization_config, dict):
            authorization_config = AuthorizationConfig(**authorization_config)
        if isinstance(domain_name, dict):
            domain_name = DomainOptions(**domain_name)
        if isinstance(log_config, dict):
            log_config = LogConfig(**log_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20507e110e7b81011acf88cd122a8d6e58160562a62e8e22f556da92e08362e9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument log_config", value=log_config, expected_type=type_hints["log_config"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument xray_enabled", value=xray_enabled, expected_type=type_hints["xray_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if log_config is not None:
            self._values["log_config"] = log_config
        if schema is not None:
            self._values["schema"] = schema
        if xray_enabled is not None:
            self._values["xray_enabled"] = xray_enabled

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name of the GraphQL API.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_config(self) -> typing.Optional[AuthorizationConfig]:
        '''(experimental) Optional authorization configuration.

        :default: - API Key authorization

        :stability: experimental
        '''
        result = self._values.get("authorization_config")
        return typing.cast(typing.Optional[AuthorizationConfig], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[DomainOptions]:
        '''(experimental) The domain name configuration for the GraphQL API.

        The Route 53 hosted zone and CName DNS record must be configured in addition to this setting to
        enable custom domain URL

        :default: - no domain name

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[DomainOptions], result)

    @builtins.property
    def log_config(self) -> typing.Optional["LogConfig"]:
        '''(experimental) Logging configuration for this api.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("log_config")
        return typing.cast(typing.Optional["LogConfig"], result)

    @builtins.property
    def schema(self) -> typing.Optional["Schema"]:
        '''(experimental) GraphQL schema definition. Specify how you want to define your schema.

        Schema.fromFile(filePath: string) allows schema definition through schema.graphql file

        :default: - schema will be generated code-first (i.e. addType, addObjectType, etc.)

        :stability: experimental
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional["Schema"], result)

    @builtins.property
    def xray_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A flag indicating whether or not X-Ray tracing is enabled for the GraphQL API.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("xray_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.GraphqlTypeOptions",
    jsii_struct_bases=[BaseTypeOptions],
    name_mapping={
        "is_list": "isList",
        "is_required": "isRequired",
        "is_required_list": "isRequiredList",
        "intermediate_type": "intermediateType",
    },
)
class GraphqlTypeOptions(BaseTypeOptions):
    def __init__(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
        intermediate_type: typing.Optional["IIntermediateType"] = None,
    ) -> None:
        '''(experimental) Options for GraphQL Types.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false
        :param intermediate_type: (experimental) the intermediate type linked to this attribute. Default: - no intermediate type

        :stability: experimental
        :option: objectType - the object type linked to this attribute
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            # intermediate_type: appsync.IIntermediateType
            
            graphql_type_options = appsync.GraphqlTypeOptions(
                intermediate_type=intermediate_type,
                is_list=False,
                is_required=False,
                is_required_list=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701e3115cb1eb511424e158a875e766bdab9673a959457c7420bb599926af4ab)
            check_type(argname="argument is_list", value=is_list, expected_type=type_hints["is_list"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument is_required_list", value=is_required_list, expected_type=type_hints["is_required_list"])
            check_type(argname="argument intermediate_type", value=intermediate_type, expected_type=type_hints["intermediate_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_list is not None:
            self._values["is_list"] = is_list
        if is_required is not None:
            self._values["is_required"] = is_required
        if is_required_list is not None:
            self._values["is_required_list"] = is_required_list
        if intermediate_type is not None:
            self._values["intermediate_type"] = intermediate_type

    @builtins.property
    def is_list(self) -> typing.Optional[builtins.bool]:
        '''(experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type].

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required(self) -> typing.Optional[builtins.bool]:
        '''(experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type!

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_required_list(self) -> typing.Optional[builtins.bool]:
        '''(experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]!

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("is_required_list")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''(experimental) the intermediate type linked to this attribute.

        :default: - no intermediate type

        :stability: experimental
        '''
        result = self._values.get("intermediate_type")
        return typing.cast(typing.Optional["IIntermediateType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.HttpDataSourceOptions",
    jsii_struct_bases=[DataSourceOptions],
    name_mapping={
        "description": "description",
        "name": "name",
        "authorization_config": "authorizationConfig",
    },
)
class HttpDataSourceOptions(DataSourceOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Optional configuration for Http data sources.

        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id
        :param authorization_config: (experimental) The authorization config in case the HTTP endpoint requires authorization. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            api = appsync.GraphqlApi(self, "api",
                name="api",
                schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql"))
            )
            
            http_ds = api.add_http_data_source("ds", "https://states.amazonaws.com",
                name="httpDsWithStepF",
                description="from appsync to StepFunctions Workflow",
                authorization_config=appsync.aws_appsync.AwsIamConfig(
                    signing_region="us-east-1",
                    signing_service_name="states"
                )
            )
            
            http_ds.create_resolver(
                type_name="Mutation",
                field_name="callStepFunction",
                request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
                response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
            )
        '''
        if isinstance(authorization_config, dict):
            authorization_config = AwsIamConfig(**authorization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfae6856ffbe054657ab7dce6de39e2bf9c6dfe1d7cdf5183f940bb24fe8aa2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the data source.

        :default: - No description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source, overrides the id given by cdk.

        :default: - generated by cdk given the id

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorization_config(self) -> typing.Optional[AwsIamConfig]:
        '''(experimental) The authorization config in case the HTTP endpoint requires authorization.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("authorization_config")
        return typing.cast(typing.Optional[AwsIamConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpDataSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.HttpDataSourceProps",
    jsii_struct_bases=[BaseDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "endpoint": "endpoint",
        "authorization_config": "authorizationConfig",
    },
)
class HttpDataSourceProps(BaseDataSourceProps):
    def __init__(
        self,
        *,
        api: "IGraphqlApi",
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        endpoint: builtins.str,
        authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for an AppSync http datasource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param endpoint: (experimental) The http endpoint.
        :param authorization_config: (experimental) The authorization config in case the HTTP endpoint requires authorization. Default: - none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            # graphql_api: appsync.GraphqlApi
            
            http_data_source_props = appsync.HttpDataSourceProps(
                api=graphql_api,
                endpoint="endpoint",
            
                # the properties below are optional
                authorization_config=appsync.AwsIamConfig(
                    signing_region="signingRegion",
                    signing_service_name="signingServiceName"
                ),
                description="description",
                name="name"
            )
        '''
        if isinstance(authorization_config, dict):
            authorization_config = AwsIamConfig(**authorization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62602e83f3466a3b88682c8a5a3ff41732db29288e6f16af5ed9685f28316b9)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "endpoint": endpoint,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config

    @builtins.property
    def api(self) -> "IGraphqlApi":
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast("IGraphqlApi", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''(experimental) The http endpoint.

        :stability: experimental
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_config(self) -> typing.Optional[AwsIamConfig]:
        '''(experimental) The authorization config in case the HTTP endpoint requires authorization.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("authorization_config")
        return typing.cast(typing.Optional[AwsIamConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_appsync.IAppsyncFunction")
class IAppsyncFunction(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for AppSync Functions.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        '''(experimental) the ARN of the AppSync function.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="functionId")
    def function_id(self) -> builtins.str:
        '''(experimental) the name of this AppSync Function.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAppsyncFunctionProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Interface for AppSync Functions.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_appsync.IAppsyncFunction"

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        '''(experimental) the ARN of the AppSync function.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="functionId")
    def function_id(self) -> builtins.str:
        '''(experimental) the name of this AppSync Function.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppsyncFunction).__jsii_proxy_class__ = lambda : _IAppsyncFunctionProxy


@jsii.interface(jsii_type="monocdk.aws_appsync.IField")
class IField(typing_extensions.Protocol):
    '''(experimental) A Graphql Field.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="isList")
    def is_list(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is a list i.e. if true, attribute would be ``[Type]``.

        :default: false

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be ``Type!`` and this attribute must always have a value.

        :default: false

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="isRequiredList")
    def is_required_list(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be ``[ Type ]!`` and this attribute's list must always have a value.

        :default: false

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "Type":
        '''(experimental) the type of attribute.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional["ResolvableFieldOptions"]:
        '''(experimental) The options to make this field resolvable.

        :default: - not a resolvable field

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''(experimental) the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''(experimental) Generate the arguments for this field.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
    ) -> builtins.str:
        '''(experimental) Generate the directives for this field.

        :param modes: the authorization modes of the graphql api.

        :default: - no authorization modes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string for this attribute.

        :stability: experimental
        '''
        ...


class _IFieldProxy:
    '''(experimental) A Graphql Field.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_appsync.IField"

    @builtins.property
    @jsii.member(jsii_name="isList")
    def is_list(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is a list i.e. if true, attribute would be ``[Type]``.

        :default: false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isList"))

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be ``Type!`` and this attribute must always have a value.

        :default: false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequired"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredList")
    def is_required_list(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be ``[ Type ]!`` and this attribute's list must always have a value.

        :default: false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequiredList"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "Type":
        '''(experimental) the type of attribute.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional["ResolvableFieldOptions"]:
        '''(experimental) The options to make this field resolvable.

        :default: - not a resolvable field

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ResolvableFieldOptions"], jsii.get(self, "fieldOptions"))

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''(experimental) the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type

        :stability: experimental
        '''
        return typing.cast(typing.Optional["IIntermediateType"], jsii.get(self, "intermediateType"))

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''(experimental) Generate the arguments for this field.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "argsToString", []))

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
    ) -> builtins.str:
        '''(experimental) Generate the directives for this field.

        :param modes: the authorization modes of the graphql api.

        :default: - no authorization modes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4934a4b71ec4a71977f19728b4b65fb79dc0c82a3d8436d792b2c1c0b16f959)
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
        return typing.cast(builtins.str, jsii.invoke(self, "directivesToString", [modes]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string for this attribute.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IField).__jsii_proxy_class__ = lambda : _IFieldProxy


@jsii.interface(jsii_type="monocdk.aws_appsync.IGraphqlApi")
class IGraphqlApi(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for GraphQL.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) the ARN of the API.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addDynamoDbDataSource")
    def add_dynamo_db_data_source(
        self,
        id: builtins.str,
        table: _ITable_24826f7e,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "DynamoDbDataSource":
        '''(experimental) add a new DynamoDB data source to this API.

        :param id: The data source's id.
        :param table: The DynamoDB table backing this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addElasticsearchDataSource")
    def add_elasticsearch_data_source(
        self,
        id: builtins.str,
        domain: _IDomain_0b3cf46c,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "ElasticsearchDataSource":
        '''(deprecated) add a new elasticsearch data source to this API.

        :param id: The data source's id.
        :param domain: The elasticsearch domain for this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :deprecated: - use ``addOpenSearchDataSource``

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="addHttpDataSource")
    def add_http_data_source(
        self,
        id: builtins.str,
        endpoint: builtins.str,
        *,
        authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "HttpDataSource":
        '''(experimental) add a new http data source to this API.

        :param id: The data source's id.
        :param endpoint: The http endpoint.
        :param authorization_config: (experimental) The authorization config in case the HTTP endpoint requires authorization. Default: - none
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addLambdaDataSource")
    def add_lambda_data_source(
        self,
        id: builtins.str,
        lambda_function: _IFunction_6e14f09e,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "LambdaDataSource":
        '''(experimental) add a new Lambda data source to this API.

        :param id: The data source's id.
        :param lambda_function: The Lambda function to call to interact with this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addNoneDataSource")
    def add_none_data_source(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "NoneDataSource":
        '''(experimental) add a new dummy data source to this API.

        Useful for pipeline resolvers
        and for backend changes that don't require a data source.

        :param id: The data source's id.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addOpenSearchDataSource")
    def add_open_search_data_source(
        self,
        id: builtins.str,
        domain: _IDomain_cb64a2bc,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "OpenSearchDataSource":
        '''(experimental) Add a new OpenSearch data source to this API.

        :param id: The data source's id.
        :param domain: The OpenSearch domain for this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addRdsDataSource")
    def add_rds_data_source(
        self,
        id: builtins.str,
        serverless_cluster: _IServerlessCluster_8ed6177c,
        secret_store: _ISecret_22fb8757,
        database_name: typing.Optional[builtins.str] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "RdsDataSource":
        '''(experimental) add a new Rds data source to this API.

        :param id: The data source's id.
        :param serverless_cluster: The serverless cluster to interact with this data source.
        :param secret_store: The secret store that contains the username and password for the serverless cluster.
        :param database_name: The optional name of the database to use within the cluster.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addSchemaDependency")
    def add_schema_dependency(self, construct: _CfnResource_e0a482dc) -> builtins.bool:
        '''(experimental) Add schema dependency if not imported.

        :param construct: the dependee.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="createResolver")
    def create_resolver(
        self,
        *,
        data_source: typing.Optional[BaseDataSource] = None,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
    ) -> "Resolver":
        '''(experimental) creates a new resolver for this datasource and API using the given properties.

        :param data_source: (experimental) The data source this resolver is using. Default: - No datasource
        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        '''
        ...


class _IGraphqlApiProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Interface for GraphQL.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_appsync.IGraphqlApi"

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) the ARN of the API.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @jsii.member(jsii_name="addDynamoDbDataSource")
    def add_dynamo_db_data_source(
        self,
        id: builtins.str,
        table: _ITable_24826f7e,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "DynamoDbDataSource":
        '''(experimental) add a new DynamoDB data source to this API.

        :param id: The data source's id.
        :param table: The DynamoDB table backing this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f04a5729f355f43a37a6a1de40270eff41c8929a9dc3cc1c2b929d8df77f7c8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("DynamoDbDataSource", jsii.invoke(self, "addDynamoDbDataSource", [id, table, options]))

    @jsii.member(jsii_name="addElasticsearchDataSource")
    def add_elasticsearch_data_source(
        self,
        id: builtins.str,
        domain: _IDomain_0b3cf46c,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "ElasticsearchDataSource":
        '''(deprecated) add a new elasticsearch data source to this API.

        :param id: The data source's id.
        :param domain: The elasticsearch domain for this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :deprecated: - use ``addOpenSearchDataSource``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376265306270b4bd89ba850586e025a47b1cc869ef4d1456920ecdf261d57161)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("ElasticsearchDataSource", jsii.invoke(self, "addElasticsearchDataSource", [id, domain, options]))

    @jsii.member(jsii_name="addHttpDataSource")
    def add_http_data_source(
        self,
        id: builtins.str,
        endpoint: builtins.str,
        *,
        authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "HttpDataSource":
        '''(experimental) add a new http data source to this API.

        :param id: The data source's id.
        :param endpoint: The http endpoint.
        :param authorization_config: (experimental) The authorization config in case the HTTP endpoint requires authorization. Default: - none
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d355777072365de58f9930b93f5a10964d43359369e89e08bfc08658892cd86)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
        options = HttpDataSourceOptions(
            authorization_config=authorization_config,
            description=description,
            name=name,
        )

        return typing.cast("HttpDataSource", jsii.invoke(self, "addHttpDataSource", [id, endpoint, options]))

    @jsii.member(jsii_name="addLambdaDataSource")
    def add_lambda_data_source(
        self,
        id: builtins.str,
        lambda_function: _IFunction_6e14f09e,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "LambdaDataSource":
        '''(experimental) add a new Lambda data source to this API.

        :param id: The data source's id.
        :param lambda_function: The Lambda function to call to interact with this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f195ade1cf17298e2fe9d90de9f774eb79846a6d570516373a1e6b4ba74cab9a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("LambdaDataSource", jsii.invoke(self, "addLambdaDataSource", [id, lambda_function, options]))

    @jsii.member(jsii_name="addNoneDataSource")
    def add_none_data_source(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "NoneDataSource":
        '''(experimental) add a new dummy data source to this API.

        Useful for pipeline resolvers
        and for backend changes that don't require a data source.

        :param id: The data source's id.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308ac633c9c93010f488643569b0688c5a76010adf9ef3bf3dee8b5cd1fd6c82)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("NoneDataSource", jsii.invoke(self, "addNoneDataSource", [id, options]))

    @jsii.member(jsii_name="addOpenSearchDataSource")
    def add_open_search_data_source(
        self,
        id: builtins.str,
        domain: _IDomain_cb64a2bc,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "OpenSearchDataSource":
        '''(experimental) Add a new OpenSearch data source to this API.

        :param id: The data source's id.
        :param domain: The OpenSearch domain for this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c75924bb0041864c4bbda81e26827c24ff3bc199f8b47d75c64b2fd45b765f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("OpenSearchDataSource", jsii.invoke(self, "addOpenSearchDataSource", [id, domain, options]))

    @jsii.member(jsii_name="addRdsDataSource")
    def add_rds_data_source(
        self,
        id: builtins.str,
        serverless_cluster: _IServerlessCluster_8ed6177c,
        secret_store: _ISecret_22fb8757,
        database_name: typing.Optional[builtins.str] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "RdsDataSource":
        '''(experimental) add a new Rds data source to this API.

        :param id: The data source's id.
        :param serverless_cluster: The serverless cluster to interact with this data source.
        :param secret_store: The secret store that contains the username and password for the serverless cluster.
        :param database_name: The optional name of the database to use within the cluster.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c8173aa170f8963a191c22f32ccbac44d8b0ec39fae35ee8f83c57b9599bfe)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument serverless_cluster", value=serverless_cluster, expected_type=type_hints["serverless_cluster"])
            check_type(argname="argument secret_store", value=secret_store, expected_type=type_hints["secret_store"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("RdsDataSource", jsii.invoke(self, "addRdsDataSource", [id, serverless_cluster, secret_store, database_name, options]))

    @jsii.member(jsii_name="addSchemaDependency")
    def add_schema_dependency(self, construct: _CfnResource_e0a482dc) -> builtins.bool:
        '''(experimental) Add schema dependency if not imported.

        :param construct: the dependee.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2687ccca0fa0bcbad3055906a1bd9811372f5a26ef5a27963b0be21dd64deb9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addSchemaDependency", [construct]))

    @jsii.member(jsii_name="createResolver")
    def create_resolver(
        self,
        *,
        data_source: typing.Optional[BaseDataSource] = None,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional["MappingTemplate"] = None,
        response_mapping_template: typing.Optional["MappingTemplate"] = None,
    ) -> "Resolver":
        '''(experimental) creates a new resolver for this datasource and API using the given properties.

        :param data_source: (experimental) The data source this resolver is using. Default: - No datasource
        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        '''
        props = ExtendedResolverProps(
            data_source=data_source,
            field_name=field_name,
            type_name=type_name,
            caching_config=caching_config,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

        return typing.cast("Resolver", jsii.invoke(self, "createResolver", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphqlApi).__jsii_proxy_class__ = lambda : _IGraphqlApiProxy


@jsii.interface(jsii_type="monocdk.aws_appsync.IIntermediateType")
class IIntermediateType(typing_extensions.Protocol):
    '''(experimental) Intermediate Types are types that includes a certain set of fields that define the entirety of your schema.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of this type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="directives")
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this object type.

        :default: - no directives

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="interfaceTypes")
    def interface_types(self) -> typing.Optional[typing.List["InterfaceType"]]:
        '''(experimental) The Interface Types this Intermediate Type implements.

        :default: - no interface types

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional["IIntermediateType"]:
        '''(experimental) the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(self) -> typing.Optional[typing.List["Resolver"]]:
        '''(experimental) The resolvers linked to this data source.

        :stability: experimental
        '''
        ...

    @resolvers.setter
    def resolvers(self, value: typing.Optional[typing.List["Resolver"]]) -> None:
        ...

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Intermediate Type.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) Create an GraphQL Type representing this Intermediate Type.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this object type.

        :stability: experimental
        '''
        ...


class _IIntermediateTypeProxy:
    '''(experimental) Intermediate Types are types that includes a certain set of fields that define the entirety of your schema.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_appsync.IIntermediateType"

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of this type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="directives")
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this object type.

        :default: - no directives

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[Directive]], jsii.get(self, "directives"))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypes")
    def interface_types(self) -> typing.Optional[typing.List["InterfaceType"]]:
        '''(experimental) The Interface Types this Intermediate Type implements.

        :default: - no interface types

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["InterfaceType"]], jsii.get(self, "interfaceTypes"))

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional[IIntermediateType]:
        '''(experimental) the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IIntermediateType], jsii.get(self, "intermediateType"))

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(self) -> typing.Optional[typing.List["Resolver"]]:
        '''(experimental) The resolvers linked to this data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["Resolver"]], jsii.get(self, "resolvers"))

    @resolvers.setter
    def resolvers(self, value: typing.Optional[typing.List["Resolver"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3432386f03c08b8afc830abb4c9a6ce21f44edc4ced377343039a5e94fd73462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvers", value)

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Intermediate Type.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) Create an GraphQL Type representing this Intermediate Type.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this object type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIntermediateType).__jsii_proxy_class__ = lambda : _IIntermediateTypeProxy


class IamResource(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.IamResource"):
    '''(experimental) A class used to generate resource arns for AppSync.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        
        api.grant(role, appsync.IamResource.custom("types/Mutation/fields/updateExample"), "appsync:GraphQL")
    '''

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "IamResource":
        '''(experimental) Generate the resource names that accepts all types: ``*``.

        :stability: experimental
        '''
        return typing.cast("IamResource", jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, *arns: builtins.str) -> "IamResource":
        '''(experimental) Generate the resource names given custom arns.

        :param arns: The custom arns that need to be permissioned. Example: custom('/types/Query/fields/getExample')

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42a8f17ec4952d80ceb86207a672c14b862c1d8faafc1789e6039506874c80f2)
            check_type(argname="argument arns", value=arns, expected_type=typing.Tuple[type_hints["arns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IamResource", jsii.sinvoke(cls, "custom", [*arns]))

    @jsii.member(jsii_name="ofType")
    @builtins.classmethod
    def of_type(cls, type: builtins.str, *fields: builtins.str) -> "IamResource":
        '''(experimental) Generate the resource names given a type and fields.

        :param type: The type that needs to be allowed.
        :param fields: The fields that need to be allowed, if empty grant permissions to ALL fields. Example: ofType('Query', 'GetExample')

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2ddb611db428996ff81398192b106b8eda2251c59dda583f9d2e72e2d381d7)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IamResource", jsii.sinvoke(cls, "ofType", [type, *fields]))

    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self, api: "GraphqlApi") -> typing.List[builtins.str]:
        '''(experimental) Return the Resource ARN.

        :param api: The GraphQL API to give permissions.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ddca3ffeb86ffe7427c1a862c35f0d5ae3e8a15240a980f934788efef4fa08)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "resourceArns", [api]))


@jsii.implements(IIntermediateType)
class InputType(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.InputType"):
    '''(experimental) Input Types are abstract types that define complex objects.

    They are used in arguments to represent

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        
        review = appsync.InputType("Review",
            definition={
                "stars": appsync.GraphqlType.int(is_required=True),
                "commentary": appsync.GraphqlType.string()
            }
        )
        api.add_type(review)
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param name: -
        :param definition: (experimental) the attributes of this type.
        :param directives: (experimental) the directives for this object type. Default: - no directives

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b26ec10de4cd7e5cfef24016f1a83e61f13232d3d7abc409fe4241b49206fc1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IntermediateTypeOptions(definition=definition, directives=directives)

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Input Type.

        Input Types must have both fieldName and field options.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) Create a GraphQL Type representing this Input Type.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this input type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of this type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(self) -> typing.Optional[typing.List[AuthorizationType]]:
        '''(experimental) the authorization modes for this intermediate type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(self, value: typing.Optional[typing.List[AuthorizationType]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e18d54182aaa6e7ebd7fa26d6228ea0486062d1e7502ce7093e6fe4f89c3df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value)


@jsii.implements(IIntermediateType)
class InterfaceType(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.InterfaceType",
):
    '''(experimental) Interface Types are abstract types that includes a certain set of fields that other types must include if they implement the interface.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        node = appsync.InterfaceType("Node",
            definition={
                "id": appsync.GraphqlType.string(is_required=True)
            }
        )
        demo = appsync.ObjectType("Demo",
            interface_types=[node],
            definition={
                "version": appsync.GraphqlType.string(is_required=True)
            }
        )
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param name: -
        :param definition: (experimental) the attributes of this type.
        :param directives: (experimental) the directives for this object type. Default: - no directives

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b786998ae5818ce1bc065897dd2f2725116d0ca65ff1d3888acddbfb36fb3a7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IntermediateTypeOptions(definition=definition, directives=directives)

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Interface Type.

        Interface Types must have both fieldName and field options.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) Create a GraphQL Type representing this Intermediate Type.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this object type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of this type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="directives")
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this object type.

        :default: - no directives

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[Directive]], jsii.get(self, "directives"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(self) -> typing.Optional[typing.List[AuthorizationType]]:
        '''(experimental) the authorization modes for this intermediate type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(self, value: typing.Optional[typing.List[AuthorizationType]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc927def3f2a9aa5090003038edd46978296c87a8f19e2395e9ea4c8d7601d1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.IntermediateTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition", "directives": "directives"},
)
class IntermediateTypeOptions:
    def __init__(
        self,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''(experimental) Properties for configuring an Intermediate Type.

        :param definition: (experimental) the attributes of this type.
        :param directives: (experimental) the directives for this object type. Default: - no directives

        :stability: experimental
        :exampleMetadata: infused

        Example::

            node = appsync.InterfaceType("Node",
                definition={
                    "id": appsync.GraphqlType.string(is_required=True)
                }
            )
            demo = appsync.ObjectType("Demo",
                interface_types=[node],
                definition={
                    "version": appsync.GraphqlType.string(is_required=True)
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c592cedeb6bfe21a9bbaa3e69e2d784f31e2e104c2e9fb135d8bb5a56246304)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }
        if directives is not None:
            self._values["directives"] = directives

    @builtins.property
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Mapping[builtins.str, IField], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this object type.

        :default: - no directives

        :stability: experimental
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntermediateTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyCondition(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.KeyCondition",
):
    '''(experimental) Factory class for DynamoDB key conditions.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        key_condition = appsync.KeyCondition.begins_with("keyName", "arg")
    '''

    @jsii.member(jsii_name="beginsWith")
    @builtins.classmethod
    def begins_with(cls, key_name: builtins.str, arg: builtins.str) -> "KeyCondition":
        '''(experimental) Condition (k, arg).

        True if the key attribute k begins with the Query argument.

        :param key_name: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e161f9b06571781d54c584f77fe13eaa5463f878d7e3696704f55ea9ae3247)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "beginsWith", [key_name, arg]))

    @jsii.member(jsii_name="between")
    @builtins.classmethod
    def between(
        cls,
        key_name: builtins.str,
        arg1: builtins.str,
        arg2: builtins.str,
    ) -> "KeyCondition":
        '''(experimental) Condition k BETWEEN arg1 AND arg2, true if k >= arg1 and k <= arg2.

        :param key_name: -
        :param arg1: -
        :param arg2: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6b59cdc92d0e944cd7e1b185a854eee378a88d1f52b0050747fa05c2aa6c8c)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg1", value=arg1, expected_type=type_hints["arg1"])
            check_type(argname="argument arg2", value=arg2, expected_type=type_hints["arg2"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "between", [key_name, arg1, arg2]))

    @jsii.member(jsii_name="eq")
    @builtins.classmethod
    def eq(cls, key_name: builtins.str, arg: builtins.str) -> "KeyCondition":
        '''(experimental) Condition k = arg, true if the key attribute k is equal to the Query argument.

        :param key_name: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f917597f8680eac283b1ba41e4a89381a0eef9226b42dc2a8eb59951202b305c)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "eq", [key_name, arg]))

    @jsii.member(jsii_name="ge")
    @builtins.classmethod
    def ge(cls, key_name: builtins.str, arg: builtins.str) -> "KeyCondition":
        '''(experimental) Condition k >= arg, true if the key attribute k is greater or equal to the Query argument.

        :param key_name: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec86c17f25ce3981932ea0780da060c015dca3849ed709bfd32f870b1a89ec92)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "ge", [key_name, arg]))

    @jsii.member(jsii_name="gt")
    @builtins.classmethod
    def gt(cls, key_name: builtins.str, arg: builtins.str) -> "KeyCondition":
        '''(experimental) Condition k > arg, true if the key attribute k is greater than the the Query argument.

        :param key_name: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91de02843753c4cbfde7ce36b769a4ef46e30412155673b36794f2be8e18fa2)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "gt", [key_name, arg]))

    @jsii.member(jsii_name="le")
    @builtins.classmethod
    def le(cls, key_name: builtins.str, arg: builtins.str) -> "KeyCondition":
        '''(experimental) Condition k <= arg, true if the key attribute k is less than or equal to the Query argument.

        :param key_name: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44911ced99be783e4a0fa97170f79389bd1e0acb9395631018e2963a7815f1cf)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "le", [key_name, arg]))

    @jsii.member(jsii_name="lt")
    @builtins.classmethod
    def lt(cls, key_name: builtins.str, arg: builtins.str) -> "KeyCondition":
        '''(experimental) Condition k < arg, true if the key attribute k is less than the Query argument.

        :param key_name: -
        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3936723f500d9dfec5e9de47782edc973e57caae43311039ca60996651bee67c)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast("KeyCondition", jsii.sinvoke(cls, "lt", [key_name, arg]))

    @jsii.member(jsii_name="and")
    def and_(self, key_cond: "KeyCondition") -> "KeyCondition":
        '''(experimental) Conjunction between two conditions.

        :param key_cond: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b9608d3b9cb312aafc8faeb451080a81dcc26740032a66fcbea64083b09f3c)
            check_type(argname="argument key_cond", value=key_cond, expected_type=type_hints["key_cond"])
        return typing.cast("KeyCondition", jsii.invoke(self, "and", [key_cond]))

    @jsii.member(jsii_name="renderTemplate")
    def render_template(self) -> builtins.str:
        '''(experimental) Renders the key condition to a VTL string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderTemplate", []))


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.LambdaAuthorizerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "handler": "handler",
        "results_cache_ttl": "resultsCacheTtl",
        "validation_regex": "validationRegex",
    },
)
class LambdaAuthorizerConfig:
    def __init__(
        self,
        *,
        handler: _IFunction_6e14f09e,
        results_cache_ttl: typing.Optional[_Duration_070aa057] = None,
        validation_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration for Lambda authorization in AppSync.

        Note that you can only have a single AWS Lambda function configured to authorize your API.

        :param handler: (experimental) The authorizer lambda function. Note: This Lambda function must have the following resource-based policy assigned to it. When configuring Lambda authorizers in the console, this is done for you. To do so with the AWS CLI, run the following: ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``
        :param results_cache_ttl: (experimental) How long the results are cached. Disable caching by setting this to 0. Default: Duration.minutes(5)
        :param validation_regex: (experimental) A regular expression for validation of tokens before the Lambda function is called. Default: - no regex filter will be applied.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as lambda_
            # auth_function: lambda.Function
            
            
            appsync.GraphqlApi(self, "api",
                name="api",
                schema=appsync.Schema.from_asset(path.join(__dirname, "appsync.test.graphql")),
                authorization_config=lambda.aws_appsync.AuthorizationConfig(
                    default_authorization=lambda.aws_appsync.AuthorizationMode(
                        authorization_type=appsync.AuthorizationType.LAMBDA,
                        lambda_authorizer_config=lambda.aws_appsync.LambdaAuthorizerConfig(
                            handler=auth_function
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974fe82cae103adcc26ee99703edf9af3fe6fddd44f6e57a4ec948e1adfc024a)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument results_cache_ttl", value=results_cache_ttl, expected_type=type_hints["results_cache_ttl"])
            check_type(argname="argument validation_regex", value=validation_regex, expected_type=type_hints["validation_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "handler": handler,
        }
        if results_cache_ttl is not None:
            self._values["results_cache_ttl"] = results_cache_ttl
        if validation_regex is not None:
            self._values["validation_regex"] = validation_regex

    @builtins.property
    def handler(self) -> _IFunction_6e14f09e:
        '''(experimental) The authorizer lambda function.

        Note: This Lambda function must have the following resource-based policy assigned to it.
        When configuring Lambda authorizers in the console, this is done for you.
        To do so with the AWS CLI, run the following:

        ``aws lambda add-permission --function-name "arn:aws:lambda:us-east-2:111122223333:function:my-function" --statement-id "appsync" --principal appsync.amazonaws.com --action lambda:InvokeFunction``

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appsync-graphqlapi-lambdaauthorizerconfig.html
        :stability: experimental
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(_IFunction_6e14f09e, result)

    @builtins.property
    def results_cache_ttl(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) How long the results are cached.

        Disable caching by setting this to 0.

        :default: Duration.minutes(5)

        :stability: experimental
        '''
        result = self._values.get("results_cache_ttl")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def validation_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) A regular expression for validation of tokens before the Lambda function is called.

        :default: - no regex filter will be applied.

        :stability: experimental
        '''
        result = self._values.get("validation_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaAuthorizerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.LogConfig",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_verbose_content": "excludeVerboseContent",
        "field_log_level": "fieldLogLevel",
        "role": "role",
    },
)
class LogConfig:
    def __init__(
        self,
        *,
        exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        field_log_level: typing.Optional[FieldLogLevel] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Logging configuration for AppSync.

        :param exclude_verbose_content: (experimental) exclude verbose content. Default: false
        :param field_log_level: (experimental) log level for fields. Default: - Use AppSync default
        :param role: (experimental) The role for CloudWatch Logs. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_iam as iam
            
            # role: iam.Role
            
            log_config = appsync.LogConfig(
                exclude_verbose_content=False,
                field_log_level=appsync.FieldLogLevel.NONE,
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f074fb7f71902b2affa7bb5d0a63d9ee8071454fcb6e93fa6e1a085ff2dd2a6)
            check_type(argname="argument exclude_verbose_content", value=exclude_verbose_content, expected_type=type_hints["exclude_verbose_content"])
            check_type(argname="argument field_log_level", value=field_log_level, expected_type=type_hints["field_log_level"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_verbose_content is not None:
            self._values["exclude_verbose_content"] = exclude_verbose_content
        if field_log_level is not None:
            self._values["field_log_level"] = field_log_level
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def exclude_verbose_content(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''(experimental) exclude verbose content.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclude_verbose_content")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def field_log_level(self) -> typing.Optional[FieldLogLevel]:
        '''(experimental) log level for fields.

        :default: - Use AppSync default

        :stability: experimental
        '''
        result = self._values.get("field_log_level")
        return typing.cast(typing.Optional[FieldLogLevel], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role for CloudWatch Logs.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MappingTemplate(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_appsync.MappingTemplate",
):
    '''(experimental) MappingTemplates for AppSync resolvers.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # dummy_request: appsync.MappingTemplate
        # dummy_response: appsync.MappingTemplate
        
        info = appsync.ObjectType("Info",
            definition={
                "node": appsync.ResolvableField(
                    return_type=appsync.GraphqlType.string(),
                    args={
                        "id": appsync.GraphqlType.string()
                    },
                    data_source=api.add_none_data_source("none"),
                    request_mapping_template=dummy_request,
                    response_mapping_template=dummy_response
                )
            }
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="dynamoDbDeleteItem")
    @builtins.classmethod
    def dynamo_db_delete_item(
        cls,
        key_name: builtins.str,
        id_arg: builtins.str,
    ) -> "MappingTemplate":
        '''(experimental) Mapping template to delete a single item from a DynamoDB table.

        :param key_name: the name of the hash key field.
        :param id_arg: the name of the Mutation argument.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ca926fbcf331634a5987d4644d0758f6a80aa28649814d37e3e41bf5afebf4)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument id_arg", value=id_arg, expected_type=type_hints["id_arg"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbDeleteItem", [key_name, id_arg]))

    @jsii.member(jsii_name="dynamoDbGetItem")
    @builtins.classmethod
    def dynamo_db_get_item(
        cls,
        key_name: builtins.str,
        id_arg: builtins.str,
    ) -> "MappingTemplate":
        '''(experimental) Mapping template to get a single item from a DynamoDB table.

        :param key_name: the name of the hash key field.
        :param id_arg: the name of the Query argument.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae7bec2d029c104dc28f5eb887fa76d5a0429d5187e945213f4448fab0954bd)
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument id_arg", value=id_arg, expected_type=type_hints["id_arg"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbGetItem", [key_name, id_arg]))

    @jsii.member(jsii_name="dynamoDbPutItem")
    @builtins.classmethod
    def dynamo_db_put_item(
        cls,
        key: "PrimaryKey",
        values: AttributeValues,
    ) -> "MappingTemplate":
        '''(experimental) Mapping template to save a single item to a DynamoDB table.

        :param key: the assigment of Mutation values to the primary key.
        :param values: the assignment of Mutation values to the table attributes.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce90d3745c168f40afe25efcd346fe9e4d96c41a05ca71089092113d5fc9326)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbPutItem", [key, values]))

    @jsii.member(jsii_name="dynamoDbQuery")
    @builtins.classmethod
    def dynamo_db_query(
        cls,
        cond: KeyCondition,
        index_name: typing.Optional[builtins.str] = None,
    ) -> "MappingTemplate":
        '''(experimental) Mapping template to query a set of items from a DynamoDB table.

        :param cond: the key condition for the query.
        :param index_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617378a786cd042023325498eb31b8ac9c806db13e0bc7fb1958c1e8e0f3ef65)
            check_type(argname="argument cond", value=cond, expected_type=type_hints["cond"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbQuery", [cond, index_name]))

    @jsii.member(jsii_name="dynamoDbResultItem")
    @builtins.classmethod
    def dynamo_db_result_item(cls) -> "MappingTemplate":
        '''(experimental) Mapping template for a single result item from DynamoDB.

        :stability: experimental
        '''
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbResultItem", []))

    @jsii.member(jsii_name="dynamoDbResultList")
    @builtins.classmethod
    def dynamo_db_result_list(cls) -> "MappingTemplate":
        '''(experimental) Mapping template for a result list from DynamoDB.

        :stability: experimental
        '''
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbResultList", []))

    @jsii.member(jsii_name="dynamoDbScanTable")
    @builtins.classmethod
    def dynamo_db_scan_table(cls) -> "MappingTemplate":
        '''(experimental) Mapping template to scan a DynamoDB table to fetch all entries.

        :stability: experimental
        '''
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "dynamoDbScanTable", []))

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, file_name: builtins.str) -> "MappingTemplate":
        '''(experimental) Create a mapping template from the given file.

        :param file_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd639a8aab4ad9e256a3ae573949c7538243e97826d5693b5e00a6dd9da8c8f)
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "fromFile", [file_name]))

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, template: builtins.str) -> "MappingTemplate":
        '''(experimental) Create a mapping template from the given string.

        :param template: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae7a67a8ce4c0d526cb63b840375e161e0da0168a9913bc63bd536570f19809)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "fromString", [template]))

    @jsii.member(jsii_name="lambdaRequest")
    @builtins.classmethod
    def lambda_request(
        cls,
        payload: typing.Optional[builtins.str] = None,
        operation: typing.Optional[builtins.str] = None,
    ) -> "MappingTemplate":
        '''(experimental) Mapping template to invoke a Lambda function.

        :param payload: the VTL template snippet of the payload to send to the lambda. If no payload is provided all available context fields are sent to the Lambda function
        :param operation: the type of operation AppSync should perform on the data source.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93459584318a2776fc2c8bb8bd016ff93be645d355cbbde4a01a754805b835f1)
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "lambdaRequest", [payload, operation]))

    @jsii.member(jsii_name="lambdaResult")
    @builtins.classmethod
    def lambda_result(cls) -> "MappingTemplate":
        '''(experimental) Mapping template to return the Lambda result to the caller.

        :stability: experimental
        '''
        return typing.cast("MappingTemplate", jsii.sinvoke(cls, "lambdaResult", []))

    @jsii.member(jsii_name="renderTemplate")
    @abc.abstractmethod
    def render_template(self) -> builtins.str:
        '''(experimental) this is called to render the mapping template to a VTL string.

        :stability: experimental
        '''
        ...


class _MappingTemplateProxy(MappingTemplate):
    @jsii.member(jsii_name="renderTemplate")
    def render_template(self) -> builtins.str:
        '''(experimental) this is called to render the mapping template to a VTL string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderTemplate", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, MappingTemplate).__jsii_proxy_class__ = lambda : _MappingTemplateProxy


class NoneDataSource(
    BaseDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.NoneDataSource",
):
    '''(experimental) An AppSync dummy datasource.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        # graphql_api: appsync.GraphqlApi
        
        none_data_source = appsync.NoneDataSource(self, "MyNoneDataSource",
            api=graphql_api,
        
            # the properties below are optional
            description="description",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25cfb81c8754825df5b162fc72cdc14873a2d6e38c9cd871ac50a43549d986e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NoneDataSourceProps(api=api, description=description, name=name)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.NoneDataSourceProps",
    jsii_struct_bases=[BaseDataSourceProps],
    name_mapping={"api": "api", "description": "description", "name": "name"},
)
class NoneDataSourceProps(BaseDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an AppSync dummy datasource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            # graphql_api: appsync.GraphqlApi
            
            none_data_source_props = appsync.NoneDataSourceProps(
                api=graphql_api,
            
                # the properties below are optional
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329b16bb6252d611c55a19c99ee14089bef1956b2207d46021005706183884a4)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NoneDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIntermediateType)
class ObjectType(
    InterfaceType,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.ObjectType",
):
    '''(experimental) Object Types are types declared by you.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # dummy_request: appsync.MappingTemplate
        # dummy_response: appsync.MappingTemplate
        
        info = appsync.ObjectType("Info",
            definition={
                "node": appsync.ResolvableField(
                    return_type=appsync.GraphqlType.string(),
                    args={
                        "id": appsync.GraphqlType.string()
                    },
                    data_source=api.add_none_data_source("none"),
                    request_mapping_template=dummy_request,
                    response_mapping_template=dummy_response
                )
            }
        )
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param name: -
        :param interface_types: (experimental) The Interface Types this Object Type implements. Default: - no interface types
        :param definition: (experimental) the attributes of this type.
        :param directives: (experimental) the directives for this object type. Default: - no directives

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b67b2a9d13cc50545efc00ab34afd3e482c7f388b456bac8c017953ec5676c0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = ObjectTypeOptions(
            interface_types=interface_types,
            definition=definition,
            directives=directives,
        )

        jsii.create(self.__class__, self, [name, props])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Object Type.

        Object Types must have both fieldName and field options.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="generateResolver")
    def _generate_resolver(
        self,
        api: IGraphqlApi,
        field_name: builtins.str,
        *,
        data_source: typing.Optional[BaseDataSource] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
        return_type: "GraphqlType",
        args: typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> "Resolver":
        '''(experimental) Generate the resolvers linked to this Object Type.

        :param api: -
        :param field_name: -
        :param data_source: (experimental) The data source creating linked to this resolvable field. Default: - no data source
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array or undefined prop will set resolver to be of type unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template
        :param return_type: (experimental) The return type for this field.
        :param args: (experimental) The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: (experimental) the directives for this field. Default: - no directives

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aa1cb3cdaace7fc071497c20fed99795c9f2b8d8add176bfe738090343957c5)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
        options = ResolvableFieldOptions(
            data_source=data_source,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
            return_type=return_type,
            args=args,
            directives=directives,
        )

        return typing.cast("Resolver", jsii.invoke(self, "generateResolver", [api, field_name, options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this object type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypes")
    def interface_types(self) -> typing.Optional[typing.List[InterfaceType]]:
        '''(experimental) The Interface Types this Object Type implements.

        :default: - no interface types

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[InterfaceType]], jsii.get(self, "interfaceTypes"))

    @builtins.property
    @jsii.member(jsii_name="resolvers")
    def resolvers(self) -> typing.Optional[typing.List["Resolver"]]:
        '''(experimental) The resolvers linked to this data source.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["Resolver"]], jsii.get(self, "resolvers"))

    @resolvers.setter
    def resolvers(self, value: typing.Optional[typing.List["Resolver"]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c96c633c381e429818356aae1fdd81a43c68caa2cdef350b61cd86efcca11f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvers", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ObjectTypeOptions",
    jsii_struct_bases=[IntermediateTypeOptions],
    name_mapping={
        "definition": "definition",
        "directives": "directives",
        "interface_types": "interfaceTypes",
    },
)
class ObjectTypeOptions(IntermediateTypeOptions):
    def __init__(
        self,
        *,
        definition: typing.Mapping[builtins.str, IField],
        directives: typing.Optional[typing.Sequence[Directive]] = None,
        interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
    ) -> None:
        '''(experimental) Properties for configuring an Object Type.

        :param definition: (experimental) the attributes of this type.
        :param directives: (experimental) the directives for this object type. Default: - no directives
        :param interface_types: (experimental) The Interface Types this Object Type implements. Default: - no interface types

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            # dummy_request: appsync.MappingTemplate
            # dummy_response: appsync.MappingTemplate
            
            info = appsync.ObjectType("Info",
                definition={
                    "node": appsync.ResolvableField(
                        return_type=appsync.GraphqlType.string(),
                        args={
                            "id": appsync.GraphqlType.string()
                        },
                        data_source=api.add_none_data_source("none"),
                        request_mapping_template=dummy_request,
                        response_mapping_template=dummy_response
                    )
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31100a5405ae7b82a872bafa8bb148d108e97e4b7493094cf4d06cf42d7444cf)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
            check_type(argname="argument interface_types", value=interface_types, expected_type=type_hints["interface_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }
        if directives is not None:
            self._values["directives"] = directives
        if interface_types is not None:
            self._values["interface_types"] = interface_types

    @builtins.property
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Mapping[builtins.str, IField], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this object type.

        :default: - no directives

        :stability: experimental
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    @builtins.property
    def interface_types(self) -> typing.Optional[typing.List[InterfaceType]]:
        '''(experimental) The Interface Types this Object Type implements.

        :default: - no interface types

        :stability: experimental
        '''
        result = self._values.get("interface_types")
        return typing.cast(typing.Optional[typing.List[InterfaceType]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ObjectTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.OpenIdConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "oidc_provider": "oidcProvider",
        "client_id": "clientId",
        "token_expiry_from_auth": "tokenExpiryFromAuth",
        "token_expiry_from_issue": "tokenExpiryFromIssue",
    },
)
class OpenIdConnectConfig:
    def __init__(
        self,
        *,
        oidc_provider: builtins.str,
        client_id: typing.Optional[builtins.str] = None,
        token_expiry_from_auth: typing.Optional[jsii.Number] = None,
        token_expiry_from_issue: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Configuration for OpenID Connect authorization in AppSync.

        :param oidc_provider: (experimental) The issuer for the OIDC configuration. The issuer returned by discovery must exactly match the value of ``iss`` in the OIDC token.
        :param client_id: (experimental) The client identifier of the Relying party at the OpenID identity provider. A regular expression can be specified so AppSync can validate against multiple client identifiers at a time. Default: - - (All)
        :param token_expiry_from_auth: (experimental) The number of milliseconds an OIDC token is valid after being authenticated by OIDC provider. ``auth_time`` claim in OIDC token is required for this validation to work. Default: - no validation
        :param token_expiry_from_issue: (experimental) The number of milliseconds an OIDC token is valid after being issued to a user. This validation uses ``iat`` claim of OIDC token. Default: - no validation

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            open_id_connect_config = appsync.OpenIdConnectConfig(
                oidc_provider="oidcProvider",
            
                # the properties below are optional
                client_id="clientId",
                token_expiry_from_auth=123,
                token_expiry_from_issue=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624bd61e820e2ed8c903686757a87e6d3ceee30b30041aaeb891ae16b38bb652)
            check_type(argname="argument oidc_provider", value=oidc_provider, expected_type=type_hints["oidc_provider"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument token_expiry_from_auth", value=token_expiry_from_auth, expected_type=type_hints["token_expiry_from_auth"])
            check_type(argname="argument token_expiry_from_issue", value=token_expiry_from_issue, expected_type=type_hints["token_expiry_from_issue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oidc_provider": oidc_provider,
        }
        if client_id is not None:
            self._values["client_id"] = client_id
        if token_expiry_from_auth is not None:
            self._values["token_expiry_from_auth"] = token_expiry_from_auth
        if token_expiry_from_issue is not None:
            self._values["token_expiry_from_issue"] = token_expiry_from_issue

    @builtins.property
    def oidc_provider(self) -> builtins.str:
        '''(experimental) The issuer for the OIDC configuration.

        The issuer returned by discovery must exactly match the value of ``iss`` in the OIDC token.

        :stability: experimental
        '''
        result = self._values.get("oidc_provider")
        assert result is not None, "Required property 'oidc_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The client identifier of the Relying party at the OpenID identity provider.

        A regular expression can be specified so AppSync can validate against multiple client identifiers at a time.

        :default:

        -
        - (All)

        :stability: experimental

        Example::

            -"ABCD|CDEF"
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_expiry_from_auth(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of milliseconds an OIDC token is valid after being authenticated by OIDC provider.

        ``auth_time`` claim in OIDC token is required for this validation to work.

        :default: - no validation

        :stability: experimental
        '''
        result = self._values.get("token_expiry_from_auth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token_expiry_from_issue(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of milliseconds an OIDC token is valid after being issued to a user.

        This validation uses ``iat`` claim of OIDC token.

        :default: - no validation

        :stability: experimental
        '''
        result = self._values.get("token_expiry_from_issue")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenIdConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PartitionKeyStep(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.PartitionKeyStep",
):
    '''(experimental) Utility class to allow assigning a value or an auto-generated id to a partition key.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        partition_key_step = appsync.PartitionKeyStep("key")
    '''

    def __init__(self, key: builtins.str) -> None:
        '''
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef294cc43d1763f915b0d0120361eac33914d0f443839088669907b55defebe)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [key])

    @jsii.member(jsii_name="auto")
    def auto(self) -> "PartitionKey":
        '''(experimental) Assign an auto-generated value to the partition key.

        :stability: experimental
        '''
        return typing.cast("PartitionKey", jsii.invoke(self, "auto", []))

    @jsii.member(jsii_name="is")
    def is_(self, val: builtins.str) -> "PartitionKey":
        '''(experimental) Assign an auto-generated value to the partition key.

        :param val: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905a065a9ec478178b39085705c2d59e6f4c697ed9c7bbf222d8e45a730114e3)
            check_type(argname="argument val", value=val, expected_type=type_hints["val"])
        return typing.cast("PartitionKey", jsii.invoke(self, "is", [val]))


class PrimaryKey(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.PrimaryKey"):
    '''(experimental) Specifies the assignment to the primary key.

    It either
    contains the full primary key or only the partition key.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "Api",
            name="demo",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
            authorization_config=appsync.aws_appsync.AuthorizationConfig(
                default_authorization=appsync.aws_appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.IAM
                )
            ),
            xray_enabled=True
        )
        
        demo_table = dynamodb.Table(self, "DemoTable",
            partition_key=appsync.aws_dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
        
        # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
        demo_dS.create_resolver(
            type_name="Query",
            field_name="getDemos",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )
        
        # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
        demo_dS.create_resolver(
            type_name="Mutation",
            field_name="addDemo",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                appsync.PrimaryKey.partition("id").auto(),
                appsync.Values.projecting("input")),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )
    '''

    def __init__(self, pkey: Assign, skey: typing.Optional[Assign] = None) -> None:
        '''
        :param pkey: -
        :param skey: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1e45226ff94c0c0532ac7f20a48b28e86d3cc3f5b2d51f7cc2f9bac1a58e08)
            check_type(argname="argument pkey", value=pkey, expected_type=type_hints["pkey"])
            check_type(argname="argument skey", value=skey, expected_type=type_hints["skey"])
        jsii.create(self.__class__, self, [pkey, skey])

    @jsii.member(jsii_name="partition")
    @builtins.classmethod
    def partition(cls, key: builtins.str) -> PartitionKeyStep:
        '''(experimental) Allows assigning a value to the partition key.

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b91382f0d8f9886cf86663f33804f713f1ac027ab0de409e3c90e14494deea1)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(PartitionKeyStep, jsii.sinvoke(cls, "partition", [key]))

    @jsii.member(jsii_name="renderTemplate")
    def render_template(self) -> builtins.str:
        '''(experimental) Renders the key assignment to a VTL string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "renderTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="pkey")
    def _pkey(self) -> Assign:
        '''
        :stability: experimental
        '''
        return typing.cast(Assign, jsii.get(self, "pkey"))


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ResolvableFieldOptions",
    jsii_struct_bases=[FieldOptions],
    name_mapping={
        "return_type": "returnType",
        "args": "args",
        "directives": "directives",
        "data_source": "dataSource",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
    },
)
class ResolvableFieldOptions(FieldOptions):
    def __init__(
        self,
        *,
        return_type: "GraphqlType",
        args: typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
        data_source: typing.Optional[BaseDataSource] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
    ) -> None:
        '''(experimental) Properties for configuring a resolvable field.

        :param return_type: (experimental) The return type for this field.
        :param args: (experimental) The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: (experimental) the directives for this field. Default: - no directives
        :param data_source: (experimental) The data source creating linked to this resolvable field. Default: - no data source
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array or undefined prop will set resolver to be of type unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        :options: responseMappingTemplate - the mapping template for responses from this resolver
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            # film_node: appsync.ObjectType
            # dummy_request: appsync.MappingTemplate
            # dummy_response: appsync.MappingTemplate
            
            
            string = appsync.GraphqlType.string()
            int = appsync.GraphqlType.int()
            api.add_mutation("addFilm", appsync.ResolvableField(
                return_type=film_node.attribute(),
                args={"name": string, "film_number": int},
                data_source=api.add_none_data_source("none"),
                request_mapping_template=dummy_request,
                response_mapping_template=dummy_response
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d77cea2af350044d4a43bb857c5dde1dfe29f5d35d875430a1493c8de8b17bb)
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument directives", value=directives, expected_type=type_hints["directives"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "return_type": return_type,
        }
        if args is not None:
            self._values["args"] = args
        if directives is not None:
            self._values["directives"] = directives
        if data_source is not None:
            self._values["data_source"] = data_source
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template

    @builtins.property
    def return_type(self) -> "GraphqlType":
        '''(experimental) The return type for this field.

        :stability: experimental
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast("GraphqlType", result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]]:
        '''(experimental) The arguments for this field.

        i.e. type Example (first: String second: String) {}

        - where 'first' and 'second' are key values for args
          and 'String' is the GraphqlType

        :default: - no arguments

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "GraphqlType"]], result)

    @builtins.property
    def directives(self) -> typing.Optional[typing.List[Directive]]:
        '''(experimental) the directives for this field.

        :default: - no directives

        :stability: experimental
        '''
        result = self._values.get("directives")
        return typing.cast(typing.Optional[typing.List[Directive]], result)

    @builtins.property
    def data_source(self) -> typing.Optional[BaseDataSource]:
        '''(experimental) The data source creating linked to this resolvable field.

        :default: - no data source

        :stability: experimental
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[BaseDataSource], result)

    @builtins.property
    def pipeline_config(self) -> typing.Optional[typing.List[IAppsyncFunction]]:
        '''(experimental) configuration of the pipeline resolver.

        :default:

        - no pipeline resolver configuration
        An empty array or undefined prop will set resolver to be of type unit

        :stability: experimental
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.List[IAppsyncFunction]], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[MappingTemplate]:
        '''(experimental) The request mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[MappingTemplate], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[MappingTemplate]:
        '''(experimental) The response mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[MappingTemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolvableFieldOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Resolver(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.Resolver",
):
    '''(experimental) An AppSync resolver.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # appsync_function: appsync.AppsyncFunction
        
        
        pipeline_resolver = appsync.Resolver(self, "pipeline",
            api=api,
            data_source=api.add_none_data_source("none"),
            type_name="typeName",
            field_name="fieldName",
            request_mapping_template=appsync.MappingTemplate.from_file("beforeRequest.vtl"),
            pipeline_config=[appsync_function],
            response_mapping_template=appsync.MappingTemplate.from_file("afterResponse.vtl")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api: IGraphqlApi,
        data_source: typing.Optional[BaseDataSource] = None,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api: (experimental) The API this resolver is attached to.
        :param data_source: (experimental) The data source this resolver is using. Default: - No datasource
        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca83da8f023ec0d1dee3fa647ec37e13b837af62d9a8911ef1536824c86d173c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ResolverProps(
            api=api,
            data_source=data_source,
            field_name=field_name,
            type_name=type_name,
            caching_config=caching_config,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) the ARN of the resolver.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ResolverProps",
    jsii_struct_bases=[ExtendedResolverProps],
    name_mapping={
        "field_name": "fieldName",
        "type_name": "typeName",
        "caching_config": "cachingConfig",
        "pipeline_config": "pipelineConfig",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
        "data_source": "dataSource",
        "api": "api",
    },
)
class ResolverProps(ExtendedResolverProps):
    def __init__(
        self,
        *,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
        data_source: typing.Optional[BaseDataSource] = None,
        api: IGraphqlApi,
    ) -> None:
        '''(experimental) Additional property for an AppSync resolver for GraphQL API reference.

        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template
        :param data_source: (experimental) The data source this resolver is using. Default: - No datasource
        :param api: (experimental) The API this resolver is attached to.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            # appsync_function: appsync.AppsyncFunction
            
            
            pipeline_resolver = appsync.Resolver(self, "pipeline",
                api=api,
                data_source=api.add_none_data_source("none"),
                type_name="typeName",
                field_name="fieldName",
                request_mapping_template=appsync.MappingTemplate.from_file("beforeRequest.vtl"),
                pipeline_config=[appsync_function],
                response_mapping_template=appsync.MappingTemplate.from_file("afterResponse.vtl")
            )
        '''
        if isinstance(caching_config, dict):
            caching_config = CachingConfig(**caching_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd65b819d42170f1710a882b49608ad30e4689782c53b7c39cb1c7887c8c6f7)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument caching_config", value=caching_config, expected_type=type_hints["caching_config"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_name": field_name,
            "type_name": type_name,
            "api": api,
        }
        if caching_config is not None:
            self._values["caching_config"] = caching_config
        if pipeline_config is not None:
            self._values["pipeline_config"] = pipeline_config
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template
        if data_source is not None:
            self._values["data_source"] = data_source

    @builtins.property
    def field_name(self) -> builtins.str:
        '''(experimental) name of the GraphQL field in the given type this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type_name(self) -> builtins.str:
        '''(experimental) name of the GraphQL type this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("type_name")
        assert result is not None, "Required property 'type_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caching_config(self) -> typing.Optional[CachingConfig]:
        '''(experimental) The caching configuration for this resolver.

        :default: - No caching configuration

        :stability: experimental
        '''
        result = self._values.get("caching_config")
        return typing.cast(typing.Optional[CachingConfig], result)

    @builtins.property
    def pipeline_config(self) -> typing.Optional[typing.List[IAppsyncFunction]]:
        '''(experimental) configuration of the pipeline resolver.

        :default:

        - no pipeline resolver configuration
        An empty array | undefined sets resolver to be of kind, unit

        :stability: experimental
        '''
        result = self._values.get("pipeline_config")
        return typing.cast(typing.Optional[typing.List[IAppsyncFunction]], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[MappingTemplate]:
        '''(experimental) The request mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[MappingTemplate], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[MappingTemplate]:
        '''(experimental) The response mapping template for this resolver.

        :default: - No mapping template

        :stability: experimental
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[MappingTemplate], result)

    @builtins.property
    def data_source(self) -> typing.Optional[BaseDataSource]:
        '''(experimental) The data source this resolver is using.

        :default: - No datasource

        :stability: experimental
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[BaseDataSource], result)

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API this resolver is attached to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolverProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Schema(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.Schema"):
    '''(experimental) The Schema for a GraphQL Api.

    If no options are configured, schema will be generated
    code-first.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "api",
            name="api",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql"))
        )
        
        http_ds = api.add_http_data_source("ds", "https://states.amazonaws.com",
            name="httpDsWithStepF",
            description="from appsync to StepFunctions Workflow",
            authorization_config=appsync.aws_appsync.AwsIamConfig(
                signing_region="us-east-1",
                signing_service_name="states"
            )
        )
        
        http_ds.create_resolver(
            type_name="Mutation",
            field_name="callStepFunction",
            request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
            response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
        )
    '''

    def __init__(self, *, file_path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param file_path: (experimental) The file path for the schema. When this option is configured, then the schema will be generated from an existing file from disk. Default: - schema not configured through disk asset

        :stability: experimental
        '''
        options = SchemaOptions(file_path=file_path)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, file_path: builtins.str) -> "Schema":
        '''(experimental) Generate a Schema from file.

        :param file_path: the file path of the schema file.

        :return: ``SchemaAsset`` with immutable schema defintion

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480127c095c8643e78cf57067aab3071a7fa32b69d5e548923132e05f42f70a8)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast("Schema", jsii.sinvoke(cls, "fromAsset", [file_path]))

    @jsii.member(jsii_name="addMutation")
    def add_mutation(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> ObjectType:
        '''(experimental) Add a mutation field to the schema's Mutation. CDK will create an Object Type called 'Mutation'. For example,.

        type Mutation {
        fieldName: Field.returnType
        }

        :param field_name: the name of the Mutation.
        :param field: the resolvable field to for this Mutation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129ae640f9ef4c5c646545ad0df397839b88409e447f5fbade97caab3f3ab6a6)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(ObjectType, jsii.invoke(self, "addMutation", [field_name, field]))

    @jsii.member(jsii_name="addQuery")
    def add_query(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> ObjectType:
        '''(experimental) Add a query field to the schema's Query. CDK will create an Object Type called 'Query'. For example,.

        type Query {
        fieldName: Field.returnType
        }

        :param field_name: the name of the query.
        :param field: the resolvable field to for this query.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f7d285fbf0eee9eeb38af45b40c375be60ce1cd35b9e4b144a2529053f1c1a)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(ObjectType, jsii.invoke(self, "addQuery", [field_name, field]))

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(self, field_name: builtins.str, field: "Field") -> ObjectType:
        '''(experimental) Add a subscription field to the schema's Subscription. CDK will create an Object Type called 'Subscription'. For example,.

        type Subscription {
        fieldName: Field.returnType
        }

        :param field_name: the name of the Subscription.
        :param field: the resolvable field to for this Subscription.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7c79bd153eabe99ffc7f87c61e199e056ee26f800e47e91a73c9441b56c8d6)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(ObjectType, jsii.invoke(self, "addSubscription", [field_name, field]))

    @jsii.member(jsii_name="addToSchema")
    def add_to_schema(
        self,
        addition: builtins.str,
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Escape hatch to add to Schema as desired.

        Will always result
        in a newline.

        :param addition: the addition to add to schema.
        :param delimiter: the delimiter between schema and addition.

        :default: - ''

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f3a957f77841b8b0c3a793ec1e0ad6338eba41852b3385a00c704d2928312b)
            check_type(argname="argument addition", value=addition, expected_type=type_hints["addition"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        return typing.cast(None, jsii.invoke(self, "addToSchema", [addition, delimiter]))

    @jsii.member(jsii_name="addType")
    def add_type(self, type: IIntermediateType) -> IIntermediateType:
        '''(experimental) Add type to the schema.

        :param type: the intermediate type to add to the schema.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00955f29f0f15679f90494894a7f805867675a74df40ba5cdb33b5f3902d1884)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(IIntermediateType, jsii.invoke(self, "addType", [type]))

    @jsii.member(jsii_name="bind")
    def bind(self, api: "GraphqlApi") -> CfnGraphQLSchema:
        '''(experimental) Called when the GraphQL Api is initialized to allow this object to bind to the stack.

        :param api: The binding GraphQL Api.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43164c78a1ac78f9dea87d60214fc7f2f35bbe7f24f499ef895d77bb16f2fc2f)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        return typing.cast(CfnGraphQLSchema, jsii.invoke(self, "bind", [api]))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> builtins.str:
        '''(experimental) The definition for this schema.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "definition"))

    @definition.setter
    def definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c43bca490806cc0da50acec1d31cf487c236b454b0a1b7d269ff87192772ec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.SchemaOptions",
    jsii_struct_bases=[],
    name_mapping={"file_path": "filePath"},
)
class SchemaOptions:
    def __init__(self, *, file_path: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) The options for configuring a schema.

        If no options are specified, then the schema will
        be generated code-first.

        :param file_path: (experimental) The file path for the schema. When this option is configured, then the schema will be generated from an existing file from disk. Default: - schema not configured through disk asset

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            
            schema_options = appsync.SchemaOptions(
                file_path="filePath"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ba094010a357b67bb0abe2b2b75fe859d9df8c521f713bd91ce338f2fb597a)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_path is not None:
            self._values["file_path"] = file_path

    @builtins.property
    def file_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The file path for the schema.

        When this option is
        configured, then the schema will be generated from an
        existing file from disk.

        :default: - schema not configured through disk asset

        :stability: experimental
        '''
        result = self._values.get("file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SortKeyStep(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.SortKeyStep"):
    '''(experimental) Utility class to allow assigning a value or an auto-generated id to a sort key.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        # assign: appsync.Assign
        
        sort_key_step = appsync.SortKeyStep(assign, "skey")
    '''

    def __init__(self, pkey: Assign, skey: builtins.str) -> None:
        '''
        :param pkey: -
        :param skey: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edcb6bf19a7bf3b07bef2380491c97dd0d5c2414f1d61e0e6c7f02ea4f77d51)
            check_type(argname="argument pkey", value=pkey, expected_type=type_hints["pkey"])
            check_type(argname="argument skey", value=skey, expected_type=type_hints["skey"])
        jsii.create(self.__class__, self, [pkey, skey])

    @jsii.member(jsii_name="auto")
    def auto(self) -> PrimaryKey:
        '''(experimental) Assign an auto-generated value to the sort key.

        :stability: experimental
        '''
        return typing.cast(PrimaryKey, jsii.invoke(self, "auto", []))

    @jsii.member(jsii_name="is")
    def is_(self, val: builtins.str) -> PrimaryKey:
        '''(experimental) Assign an auto-generated value to the sort key.

        :param val: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef693a5898b9a8dad179b4b176ec06f5f16a790fae16b6f934fda52117a23815)
            check_type(argname="argument val", value=val, expected_type=type_hints["val"])
        return typing.cast(PrimaryKey, jsii.invoke(self, "is", [val]))


@jsii.enum(jsii_type="monocdk.aws_appsync.Type")
class Type(enum.Enum):
    '''(experimental) Enum containing the Types that can be used to define ObjectTypes.

    :stability: experimental
    '''

    ID = "ID"
    '''(experimental) ``ID`` scalar type is a unique identifier. ``ID`` type is serialized similar to ``String``.

    Often used as a key for a cache and not intended to be human-readable.

    :stability: experimental
    '''
    STRING = "STRING"
    '''(experimental) ``String`` scalar type is a free-form human-readable text.

    :stability: experimental
    '''
    INT = "INT"
    '''(experimental) ``Int`` scalar type is a signed non-fractional numerical value.

    :stability: experimental
    '''
    FLOAT = "FLOAT"
    '''(experimental) ``Float`` scalar type is a signed double-precision fractional value.

    :stability: experimental
    '''
    BOOLEAN = "BOOLEAN"
    '''(experimental) ``Boolean`` scalar type is a boolean value: true or false.

    :stability: experimental
    '''
    AWS_DATE = "AWS_DATE"
    '''(experimental) ``AWSDate`` scalar type represents a valid extended ``ISO 8601 Date`` string.

    In other words, accepts date strings in the form of ``YYYY-MM-DD``. It accepts time zone offsets.

    :see: https://en.wikipedia.org/wiki/ISO_8601#Calendar_dates
    :stability: experimental
    '''
    AWS_TIME = "AWS_TIME"
    '''(experimental) ``AWSTime`` scalar type represents a valid extended ``ISO 8601 Time`` string.

    In other words, accepts date strings in the form of ``hh:mm:ss.sss``. It accepts time zone offsets.

    :see: https://en.wikipedia.org/wiki/ISO_8601#Times
    :stability: experimental
    '''
    AWS_DATE_TIME = "AWS_DATE_TIME"
    '''(experimental) ``AWSDateTime`` scalar type represents a valid extended ``ISO 8601 DateTime`` string.

    In other words, accepts date strings in the form of ``YYYY-MM-DDThh:mm:ss.sssZ``. It accepts time zone offsets.

    :see: https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations
    :stability: experimental
    '''
    AWS_TIMESTAMP = "AWS_TIMESTAMP"
    '''(experimental) ``AWSTimestamp`` scalar type represents the number of seconds since ``1970-01-01T00:00Z``.

    Timestamps are serialized and deserialized as numbers.

    :stability: experimental
    '''
    AWS_EMAIL = "AWS_EMAIL"
    '''(experimental) ``AWSEmail`` scalar type represents an email address string (i.e.``username@example.com``).

    :stability: experimental
    '''
    AWS_JSON = "AWS_JSON"
    '''(experimental) ``AWSJson`` scalar type represents a JSON string.

    :stability: experimental
    '''
    AWS_URL = "AWS_URL"
    '''(experimental) ``AWSURL`` scalar type represetns a valid URL string.

    URLs wihtout schemes or contain double slashes are considered invalid.

    :stability: experimental
    '''
    AWS_PHONE = "AWS_PHONE"
    '''(experimental) ``AWSPhone`` scalar type represents a valid phone number. Phone numbers maybe be whitespace delimited or hyphenated.

    The number can specify a country code at the beginning, but is not required for US phone numbers.

    :stability: experimental
    '''
    AWS_IP_ADDRESS = "AWS_IP_ADDRESS"
    '''(experimental) ``AWSIPAddress`` scalar type respresents a valid ``IPv4`` of ``IPv6`` address string.

    :stability: experimental
    '''
    INTERMEDIATE = "INTERMEDIATE"
    '''(experimental) Type used for Intermediate Types (i.e. an interface or an object type).

    :stability: experimental
    '''


@jsii.implements(IIntermediateType)
class UnionType(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.UnionType"):
    '''(experimental) Union Types are abstract types that are similar to Interface Types, but they cannot to specify any common fields between types.

    Note that fields of a union type need to be object types. In other words,
    you can't create a union type out of interfaces, other unions, or inputs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        
        string = appsync.GraphqlType.string()
        human = appsync.ObjectType("Human", definition={"name": string})
        droid = appsync.ObjectType("Droid", definition={"name": string})
        starship = appsync.ObjectType("Starship", definition={"name": string})
        search = appsync.UnionType("Search",
            definition=[human, droid, starship]
        )
        api.add_type(search)
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Sequence[IIntermediateType],
    ) -> None:
        '''
        :param name: -
        :param definition: (experimental) the object types for this union type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318d1f80d1c432cb4ded544e30ac1be9021a2ead178eea2286ccef8d01672283)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = UnionTypeOptions(definition=definition)

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Union Type.

        Input Types must have field options and the IField must be an Object Type.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) Create a GraphQL Type representing this Union Type.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this Union type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of this type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(self) -> typing.Optional[typing.List[AuthorizationType]]:
        '''(experimental) the authorization modes supported by this intermediate type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(self, value: typing.Optional[typing.List[AuthorizationType]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87ebd02a8637e1358bf47bdb795d843037c568a9be37aed18d1f523006dc3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.UnionTypeOptions",
    jsii_struct_bases=[],
    name_mapping={"definition": "definition"},
)
class UnionTypeOptions:
    def __init__(self, *, definition: typing.Sequence[IIntermediateType]) -> None:
        '''(experimental) Properties for configuring an Union Type.

        :param definition: (experimental) the object types for this union type.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            
            string = appsync.GraphqlType.string()
            human = appsync.ObjectType("Human", definition={"name": string})
            droid = appsync.ObjectType("Droid", definition={"name": string})
            starship = appsync.ObjectType("Starship", definition={"name": string})
            search = appsync.UnionType("Search",
                definition=[human, droid, starship]
            )
            api.add_type(search)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba4279b311e3ec6581d01adea11fae7796457a41fa2024e04ade495b2b519a8)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
        }

    @builtins.property
    def definition(self) -> typing.List[IIntermediateType]:
        '''(experimental) the object types for this union type.

        :stability: experimental
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.List[IIntermediateType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnionTypeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.UserPoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "user_pool": "userPool",
        "app_id_client_regex": "appIdClientRegex",
        "default_action": "defaultAction",
    },
)
class UserPoolConfig:
    def __init__(
        self,
        *,
        user_pool: _IUserPool_5e500460,
        app_id_client_regex: typing.Optional[builtins.str] = None,
        default_action: typing.Optional["UserPoolDefaultAction"] = None,
    ) -> None:
        '''(experimental) Configuration for Cognito user-pools in AppSync.

        :param user_pool: (experimental) The Cognito user pool to use as identity source.
        :param app_id_client_regex: (experimental) the optional app id regex. Default: - None
        :param default_action: (experimental) Default auth action. Default: ALLOW

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_cognito as cognito
            
            # user_pool: cognito.UserPool
            
            user_pool_config = appsync.UserPoolConfig(
                user_pool=user_pool,
            
                # the properties below are optional
                app_id_client_regex="appIdClientRegex",
                default_action=appsync.UserPoolDefaultAction.ALLOW
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edbb91e242bcc7da75d6e393d4b01cd1c5a0b178b397d523996fa6fb348a7a2a)
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
            check_type(argname="argument app_id_client_regex", value=app_id_client_regex, expected_type=type_hints["app_id_client_regex"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_pool": user_pool,
        }
        if app_id_client_regex is not None:
            self._values["app_id_client_regex"] = app_id_client_regex
        if default_action is not None:
            self._values["default_action"] = default_action

    @builtins.property
    def user_pool(self) -> _IUserPool_5e500460:
        '''(experimental) The Cognito user pool to use as identity source.

        :stability: experimental
        '''
        result = self._values.get("user_pool")
        assert result is not None, "Required property 'user_pool' is missing"
        return typing.cast(_IUserPool_5e500460, result)

    @builtins.property
    def app_id_client_regex(self) -> typing.Optional[builtins.str]:
        '''(experimental) the optional app id regex.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("app_id_client_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_action(self) -> typing.Optional["UserPoolDefaultAction"]:
        '''(experimental) Default auth action.

        :default: ALLOW

        :stability: experimental
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional["UserPoolDefaultAction"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_appsync.UserPoolDefaultAction")
class UserPoolDefaultAction(enum.Enum):
    '''(experimental) enum with all possible values for Cognito user-pool default actions.

    :stability: experimental
    '''

    ALLOW = "ALLOW"
    '''(experimental) ALLOW access to API.

    :stability: experimental
    '''
    DENY = "DENY"
    '''(experimental) DENY access to API.

    :stability: experimental
    '''


class Values(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.Values"):
    '''(experimental) Factory class for attribute value assignments.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "Api",
            name="demo",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
            authorization_config=appsync.aws_appsync.AuthorizationConfig(
                default_authorization=appsync.aws_appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.IAM
                )
            ),
            xray_enabled=True
        )
        
        demo_table = dynamodb.Table(self, "DemoTable",
            partition_key=appsync.aws_dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
        
        # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
        demo_dS.create_resolver(
            type_name="Query",
            field_name="getDemos",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )
        
        # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
        demo_dS.create_resolver(
            type_name="Mutation",
            field_name="addDemo",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                appsync.PrimaryKey.partition("id").auto(),
                appsync.Values.projecting("input")),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="attribute")
    @builtins.classmethod
    def attribute(cls, attr: builtins.str) -> AttributeValuesStep:
        '''(experimental) Allows assigning a value to the specified attribute.

        :param attr: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2c3c824876eb01b9c6233d28ac499c3a1b54d5fa305d2a1cf37d46a379773a)
            check_type(argname="argument attr", value=attr, expected_type=type_hints["attr"])
        return typing.cast(AttributeValuesStep, jsii.sinvoke(cls, "attribute", [attr]))

    @jsii.member(jsii_name="projecting")
    @builtins.classmethod
    def projecting(cls, arg: typing.Optional[builtins.str] = None) -> AttributeValues:
        '''(experimental) Treats the specified object as a map of assignments, where the property names represent attribute names.

        It’s opinionated about how it represents
        some of the nested objects: e.g., it will use lists (“L”) rather than sets
        (“SS”, “NS”, “BS”). By default it projects the argument container ("$ctx.args").

        :param arg: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20aec3c65f45f7eb0fad9d10659ad55b87594ecafc7bb065670e110e3db214e)
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
        return typing.cast(AttributeValues, jsii.sinvoke(cls, "projecting", [arg]))


@jsii.implements(IAppsyncFunction)
class AppsyncFunction(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.AppsyncFunction",
):
    '''(experimental) AppSync Functions are local functions that perform certain operations onto a backend data source.

    Developers can compose operations (Functions)
    and execute them in sequence with Pipeline Resolvers.

    :stability: experimental
    :resource: AWS::AppSync::FunctionConfiguration
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        
        
        appsync_function = appsync.AppsyncFunction(self, "function",
            name="appsync_function",
            api=api,
            data_source=api.add_none_data_source("none"),
            request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
            response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api: IGraphqlApi,
        data_source: BaseDataSource,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api: (experimental) the GraphQL Api linked to this AppSync Function.
        :param data_source: (experimental) the data source linked to this AppSync Function.
        :param name: (experimental) the name of the AppSync Function.
        :param description: (experimental) the description for this AppSync Function. Default: - no description
        :param request_mapping_template: (experimental) the request mapping template for the AppSync Function. Default: - no request mapping template
        :param response_mapping_template: (experimental) the response mapping template for the AppSync Function. Default: - no response mapping template

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0132a977cda482b0bf447be6458ae6613dda0dfaea20dab8d1b80a49742c61ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppsyncFunctionProps(
            api=api,
            data_source=data_source,
            name=name,
            description=description,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAppsyncFunctionAttributes")
    @builtins.classmethod
    def from_appsync_function_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        function_arn: builtins.str,
    ) -> IAppsyncFunction:
        '''(experimental) Import Appsync Function from arn.

        :param scope: -
        :param id: -
        :param function_arn: (experimental) the ARN of the AppSync function.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8260122f7cb4ab9f59ecf9c41581fca64cb3c29e2fc75d89849089f8cfd903f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AppsyncFunctionAttributes(function_arn=function_arn)

        return typing.cast(IAppsyncFunction, jsii.sinvoke(cls, "fromAppsyncFunctionAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> BaseDataSource:
        '''(experimental) the data source of this AppSync Function.

        :stability: experimental
        :attribute: DataSourceName
        '''
        return typing.cast(BaseDataSource, jsii.get(self, "dataSource"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        '''(experimental) the ARN of the AppSync function.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="functionId")
    def function_id(self) -> builtins.str:
        '''(experimental) the ID of the AppSync function.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionId"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''(experimental) the name of this AppSync Function.

        :stability: experimental
        :attribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.AppsyncFunctionProps",
    jsii_struct_bases=[BaseAppsyncFunctionProps],
    name_mapping={
        "name": "name",
        "description": "description",
        "request_mapping_template": "requestMappingTemplate",
        "response_mapping_template": "responseMappingTemplate",
        "api": "api",
        "data_source": "dataSource",
    },
)
class AppsyncFunctionProps(BaseAppsyncFunctionProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
        api: IGraphqlApi,
        data_source: BaseDataSource,
    ) -> None:
        '''(experimental) the CDK properties for AppSync Functions.

        :param name: (experimental) the name of the AppSync Function.
        :param description: (experimental) the description for this AppSync Function. Default: - no description
        :param request_mapping_template: (experimental) the request mapping template for the AppSync Function. Default: - no request mapping template
        :param response_mapping_template: (experimental) the response mapping template for the AppSync Function. Default: - no response mapping template
        :param api: (experimental) the GraphQL Api linked to this AppSync Function.
        :param data_source: (experimental) the data source linked to this AppSync Function.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # api: appsync.GraphqlApi
            
            
            appsync_function = appsync.AppsyncFunction(self, "function",
                name="appsync_function",
                api=api,
                data_source=api.add_none_data_source("none"),
                request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
                response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319c0c1370b60552cd73d184ffbe51fad87559f39457ea1dcc565f459a9c8d1c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument request_mapping_template", value=request_mapping_template, expected_type=type_hints["request_mapping_template"])
            check_type(argname="argument response_mapping_template", value=response_mapping_template, expected_type=type_hints["response_mapping_template"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "api": api,
            "data_source": data_source,
        }
        if description is not None:
            self._values["description"] = description
        if request_mapping_template is not None:
            self._values["request_mapping_template"] = request_mapping_template
        if response_mapping_template is not None:
            self._values["response_mapping_template"] = response_mapping_template

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name of the AppSync Function.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description for this AppSync Function.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_mapping_template(self) -> typing.Optional[MappingTemplate]:
        '''(experimental) the request mapping template for the AppSync Function.

        :default: - no request mapping template

        :stability: experimental
        '''
        result = self._values.get("request_mapping_template")
        return typing.cast(typing.Optional[MappingTemplate], result)

    @builtins.property
    def response_mapping_template(self) -> typing.Optional[MappingTemplate]:
        '''(experimental) the response mapping template for the AppSync Function.

        :default: - no response mapping template

        :stability: experimental
        '''
        result = self._values.get("response_mapping_template")
        return typing.cast(typing.Optional[MappingTemplate], result)

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) the GraphQL Api linked to this AppSync Function.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def data_source(self) -> BaseDataSource:
        '''(experimental) the data source linked to this AppSync Function.

        :stability: experimental
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(BaseDataSource, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IGrantable_4c5a91d1)
class BackedDataSource(
    BaseDataSource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_appsync.BackedDataSource",
):
    '''(experimental) Abstract AppSync datasource implementation.

    Do not use directly but use subclasses for resource backed datasources

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union["BackedDataSourceProps", typing.Dict[builtins.str, typing.Any]],
        *,
        type: builtins.str,
        dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        :param type: (experimental) the type of the AppSync datasource.
        :param dynamo_db_config: (experimental) configuration for DynamoDB Datasource. Default: - No config
        :param elasticsearch_config: (deprecated) configuration for Elasticsearch data source. Default: - No config
        :param http_config: (experimental) configuration for HTTP Datasource. Default: - No config
        :param lambda_config: (experimental) configuration for Lambda Datasource. Default: - No config
        :param open_search_service_config: (experimental) configuration for OpenSearch data source. Default: - No config
        :param relational_database_config: (experimental) configuration for RDS Datasource. Default: - No config

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcaf1872b474204ef3c4d442476523d26c7337f4a647e8a92b8da85e15929235)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        extended = ExtendedDataSourceProps(
            type=type,
            dynamo_db_config=dynamo_db_config,
            elasticsearch_config=elasticsearch_config,
            http_config=http_config,
            lambda_config=lambda_config,
            open_search_service_config=open_search_service_config,
            relational_database_config=relational_database_config,
        )

        jsii.create(self.__class__, self, [scope, id, props, extended])

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) the principal of the data source to be IGrantable.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))


class _BackedDataSourceProxy(
    BackedDataSource,
    jsii.proxy_for(BaseDataSource), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BackedDataSource).__jsii_proxy_class__ = lambda : _BackedDataSourceProxy


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.BackedDataSourceProps",
    jsii_struct_bases=[BaseDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "service_role": "serviceRole",
    },
)
class BackedDataSourceProps(BaseDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) properties for an AppSync datasource backed by a resource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_iam as iam
            
            # graphql_api: appsync.GraphqlApi
            # role: iam.Role
            
            backed_data_source_props = appsync.BackedDataSourceProps(
                api=graphql_api,
            
                # the properties below are optional
                description="description",
                name="name",
                service_role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f1e182121e07ee604d42fc7dfb0df184d10169a2edbc979904ace9584a3699)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to be assumed by AppSync to interact with the data source.

        :default: - Create a new role

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackedDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoDbDataSource(
    BackedDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.DynamoDbDataSource",
):
    '''(experimental) An AppSync datasource backed by a DynamoDB table.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "Api",
            name="demo",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql")),
            authorization_config=appsync.aws_appsync.AuthorizationConfig(
                default_authorization=appsync.aws_appsync.AuthorizationMode(
                    authorization_type=appsync.AuthorizationType.IAM
                )
            ),
            xray_enabled=True
        )
        
        demo_table = dynamodb.Table(self, "DemoTable",
            partition_key=appsync.aws_dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        demo_dS = api.add_dynamo_db_data_source("demoDataSource", demo_table)
        
        # Resolver for the Query "getDemos" that scans the DynamoDb table and returns the entire list.
        demo_dS.create_resolver(
            type_name="Query",
            field_name="getDemos",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_scan_table(),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_list()
        )
        
        # Resolver for the Mutation "addDemo" that puts the item into the DynamoDb table.
        demo_dS.create_resolver(
            type_name="Mutation",
            field_name="addDemo",
            request_mapping_template=appsync.MappingTemplate.dynamo_db_put_item(
                appsync.PrimaryKey.partition("id").auto(),
                appsync.Values.projecting("input")),
            response_mapping_template=appsync.MappingTemplate.dynamo_db_result_item()
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        table: _ITable_24826f7e,
        read_only_access: typing.Optional[builtins.bool] = None,
        use_caller_credentials: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param table: (experimental) The DynamoDB table backing this data source.
        :param read_only_access: (experimental) Specify whether this DS is read only or has read and write permissions to the DynamoDB table. Default: false
        :param use_caller_credentials: (experimental) use credentials of caller to access DynamoDB. Default: false
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6e311489aad534662dae365cda4a9c10457ecb27996d04aecb62f5c818eb87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DynamoDbDataSourceProps(
            table=table,
            read_only_access=read_only_access,
            use_caller_credentials=use_caller_credentials,
            service_role=service_role,
            api=api,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.DynamoDbDataSourceProps",
    jsii_struct_bases=[BackedDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "service_role": "serviceRole",
        "table": "table",
        "read_only_access": "readOnlyAccess",
        "use_caller_credentials": "useCallerCredentials",
    },
)
class DynamoDbDataSourceProps(BackedDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        table: _ITable_24826f7e,
        read_only_access: typing.Optional[builtins.bool] = None,
        use_caller_credentials: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for an AppSync DynamoDB datasource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param table: (experimental) The DynamoDB table backing this data source.
        :param read_only_access: (experimental) Specify whether this DS is read only or has read and write permissions to the DynamoDB table. Default: false
        :param use_caller_credentials: (experimental) use credentials of caller to access DynamoDB. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_dynamodb as dynamodb
            from monocdk import aws_iam as iam
            
            # graphql_api: appsync.GraphqlApi
            # role: iam.Role
            # table: dynamodb.Table
            
            dynamo_db_data_source_props = appsync.DynamoDbDataSourceProps(
                api=graphql_api,
                table=table,
            
                # the properties below are optional
                description="description",
                name="name",
                read_only_access=False,
                service_role=role,
                use_caller_credentials=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25370a06169ecdd34cefba9ccd71c256ea23190c140b6cd23efd55eb214bac36)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument read_only_access", value=read_only_access, expected_type=type_hints["read_only_access"])
            check_type(argname="argument use_caller_credentials", value=use_caller_credentials, expected_type=type_hints["use_caller_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "table": table,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role
        if read_only_access is not None:
            self._values["read_only_access"] = read_only_access
        if use_caller_credentials is not None:
            self._values["use_caller_credentials"] = use_caller_credentials

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to be assumed by AppSync to interact with the data source.

        :default: - Create a new role

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def table(self) -> _ITable_24826f7e:
        '''(experimental) The DynamoDB table backing this data source.

        :stability: experimental
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(_ITable_24826f7e, result)

    @builtins.property
    def read_only_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify whether this DS is read only or has read and write permissions to the DynamoDB table.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("read_only_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_caller_credentials(self) -> typing.Optional[builtins.bool]:
        '''(experimental) use credentials of caller to access DynamoDB.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("use_caller_credentials")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoDbDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchDataSource(
    BackedDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.ElasticsearchDataSource",
):
    '''(deprecated) An Appsync datasource backed by Elasticsearch.

    :deprecated: - use ``OpenSearchDataSource``

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        from monocdk import aws_elasticsearch as elasticsearch
        from monocdk import aws_iam as iam
        
        # domain: elasticsearch.Domain
        # graphql_api: appsync.GraphqlApi
        # role: iam.Role
        
        elasticsearch_data_source = appsync.ElasticsearchDataSource(self, "MyElasticsearchDataSource",
            api=graphql_api,
            domain=domain,
        
            # the properties below are optional
            description="description",
            name="name",
            service_role=role
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: _IDomain_0b3cf46c,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain: (deprecated) The elasticsearch domain containing the endpoint for the data source.
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b724a05ca00ad168ea72dd6d7746274e35ad1d8f97860bb8abe9224634c2120c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ElasticsearchDataSourceProps(
            domain=domain,
            service_role=service_role,
            api=api,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.ElasticsearchDataSourceProps",
    jsii_struct_bases=[BackedDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "service_role": "serviceRole",
        "domain": "domain",
    },
)
class ElasticsearchDataSourceProps(BackedDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        domain: _IDomain_0b3cf46c,
    ) -> None:
        '''(deprecated) Properties for the Elasticsearch Data Source.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param domain: (deprecated) The elasticsearch domain containing the endpoint for the data source.

        :deprecated: - use ``OpenSearchDataSourceProps`` with ``OpenSearchDataSource``

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_elasticsearch as elasticsearch
            from monocdk import aws_iam as iam
            
            # domain: elasticsearch.Domain
            # graphql_api: appsync.GraphqlApi
            # role: iam.Role
            
            elasticsearch_data_source_props = appsync.ElasticsearchDataSourceProps(
                api=graphql_api,
                domain=domain,
            
                # the properties below are optional
                description="description",
                name="name",
                service_role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a139e90767ea8c5015925561ec1041c3438db9fab35752d2071d2481fbd1113)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "domain": domain,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to be assumed by AppSync to interact with the data source.

        :default: - Create a new role

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def domain(self) -> _IDomain_0b3cf46c:
        '''(deprecated) The elasticsearch domain containing the endpoint for the data source.

        :stability: deprecated
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(_IDomain_0b3cf46c, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElasticsearchDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIntermediateType)
class EnumType(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.EnumType"):
    '''(experimental) Enum Types are abstract types that includes a set of fields that represent the strings this type can create.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        
        episode = appsync.EnumType("Episode",
            definition=["NEWHOPE", "EMPIRE", "JEDI"
            ]
        )
        api.add_type(episode)
    '''

    def __init__(
        self,
        name: builtins.str,
        *,
        definition: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: -
        :param definition: (experimental) the attributes of this type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f35ba5d19bd6d93ee86b1bddec8015a740243fbcc7bec0f57ac77a48c991d94)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        options = EnumTypeOptions(definition=definition)

        jsii.create(self.__class__, self, [name, options])

    @jsii.member(jsii_name="addField")
    def add_field(
        self,
        *,
        field: typing.Optional[IField] = None,
        field_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a field to this Enum Type.

        To add a field to this Enum Type, you must only configure
        addField with the fieldName options.

        :param field: (experimental) The resolvable field to add. This option must be configured for Object, Interface, Input and Union Types. Default: - no IField
        :param field_name: (experimental) The name of the field. This option must be configured for Object, Interface, Input and Enum Types. Default: - no fieldName

        :stability: experimental
        '''
        options = AddFieldOptions(field=field, field_name=field_name)

        return typing.cast(None, jsii.invoke(self, "addField", [options]))

    @jsii.member(jsii_name="attribute")
    def attribute(
        self,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) Create an GraphQL Type representing this Enum Type.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.invoke(self, "attribute", [options]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string of this enum type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(self) -> typing.Mapping[builtins.str, IField]:
        '''(experimental) the attributes of this type.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, IField], jsii.get(self, "definition"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of this type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def _modes(self) -> typing.Optional[typing.List[AuthorizationType]]:
        '''(experimental) the authorization modes for this intermediate type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[AuthorizationType]], jsii.get(self, "modes"))

    @_modes.setter
    def _modes(self, value: typing.Optional[typing.List[AuthorizationType]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba17d33823e2a842edbb291e18fc3b7cacbcb3d246e6d70baca206301fb3f89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modes", value)


@jsii.implements(IGraphqlApi)
class GraphqlApiBase(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_appsync.GraphqlApiBase",
):
    '''(experimental) Base Class for GraphQL API.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: (experimental) The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: (experimental) ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: (experimental) The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: (experimental) The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2bbf15615501f62510ef6a13d244cbe1e440dafc6cdce46aaca07681fe2fa1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _ResourceProps_9b554c0f(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDynamoDbDataSource")
    def add_dynamo_db_data_source(
        self,
        id: builtins.str,
        table: _ITable_24826f7e,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> DynamoDbDataSource:
        '''(experimental) add a new DynamoDB data source to this API.

        :param id: The data source's id.
        :param table: The DynamoDB table backing this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe51ccbdc5dc70c7017a42aaafb3ce07d877f02da81992906e1459f5c84cc129)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast(DynamoDbDataSource, jsii.invoke(self, "addDynamoDbDataSource", [id, table, options]))

    @jsii.member(jsii_name="addElasticsearchDataSource")
    def add_elasticsearch_data_source(
        self,
        id: builtins.str,
        domain: _IDomain_0b3cf46c,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> ElasticsearchDataSource:
        '''(deprecated) add a new elasticsearch data source to this API.

        :param id: The data source's id.
        :param domain: The elasticsearch domain for this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :deprecated: - use ``addOpenSearchDataSource``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c375438ba40791f610d4409fb20b7165ea6da87ab9fcb17fc117b5649dad6f9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast(ElasticsearchDataSource, jsii.invoke(self, "addElasticsearchDataSource", [id, domain, options]))

    @jsii.member(jsii_name="addHttpDataSource")
    def add_http_data_source(
        self,
        id: builtins.str,
        endpoint: builtins.str,
        *,
        authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "HttpDataSource":
        '''(experimental) add a new http data source to this API.

        :param id: The data source's id.
        :param endpoint: The http endpoint.
        :param authorization_config: (experimental) The authorization config in case the HTTP endpoint requires authorization. Default: - none
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0476506c45c0541e8b87633c59fd6d43d2cc9e780fb42e927041e51cbbe55cab)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
        options = HttpDataSourceOptions(
            authorization_config=authorization_config,
            description=description,
            name=name,
        )

        return typing.cast("HttpDataSource", jsii.invoke(self, "addHttpDataSource", [id, endpoint, options]))

    @jsii.member(jsii_name="addLambdaDataSource")
    def add_lambda_data_source(
        self,
        id: builtins.str,
        lambda_function: _IFunction_6e14f09e,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "LambdaDataSource":
        '''(experimental) add a new Lambda data source to this API.

        :param id: The data source's id.
        :param lambda_function: The Lambda function to call to interact with this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114c4b0033e11dc87be73938252f58d518d13b1a74e2266e3d955d6bb726832a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("LambdaDataSource", jsii.invoke(self, "addLambdaDataSource", [id, lambda_function, options]))

    @jsii.member(jsii_name="addNoneDataSource")
    def add_none_data_source(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> NoneDataSource:
        '''(experimental) add a new dummy data source to this API.

        Useful for pipeline resolvers
        and for backend changes that don't require a data source.

        :param id: The data source's id.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e93f2a0cff6e8a7d1072c7f2767b9b41f6c6d3f0e97d80844fd4acc40e4a868)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast(NoneDataSource, jsii.invoke(self, "addNoneDataSource", [id, options]))

    @jsii.member(jsii_name="addOpenSearchDataSource")
    def add_open_search_data_source(
        self,
        id: builtins.str,
        domain: _IDomain_cb64a2bc,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "OpenSearchDataSource":
        '''(experimental) add a new OpenSearch data source to this API.

        :param id: The data source's id.
        :param domain: The OpenSearch domain for this data source.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b17af62f1f2838c00862311172ef9e73cb2045e8fb2cceb0fc986e9016cd492)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("OpenSearchDataSource", jsii.invoke(self, "addOpenSearchDataSource", [id, domain, options]))

    @jsii.member(jsii_name="addRdsDataSource")
    def add_rds_data_source(
        self,
        id: builtins.str,
        serverless_cluster: _IServerlessCluster_8ed6177c,
        secret_store: _ISecret_22fb8757,
        database_name: typing.Optional[builtins.str] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "RdsDataSource":
        '''(experimental) add a new Rds data source to this API.

        :param id: The data source's id.
        :param serverless_cluster: The serverless cluster to interact with this data source.
        :param secret_store: The secret store that contains the username and password for the serverless cluster.
        :param database_name: The optional name of the database to use within the cluster.
        :param description: (experimental) The description of the data source. Default: - No description
        :param name: (experimental) The name of the data source, overrides the id given by cdk. Default: - generated by cdk given the id

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73af86ef894062e776b9f84461020e34c60b6ccea0023ec609b40e62d3d369fd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument serverless_cluster", value=serverless_cluster, expected_type=type_hints["serverless_cluster"])
            check_type(argname="argument secret_store", value=secret_store, expected_type=type_hints["secret_store"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
        options = DataSourceOptions(description=description, name=name)

        return typing.cast("RdsDataSource", jsii.invoke(self, "addRdsDataSource", [id, serverless_cluster, secret_store, database_name, options]))

    @jsii.member(jsii_name="addSchemaDependency")
    def add_schema_dependency(self, construct: _CfnResource_e0a482dc) -> builtins.bool:
        '''(experimental) Add schema dependency if not imported.

        :param construct: the dependee.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2f4e4d0307cd929f0181a945cfd3fea09a09af6e7f0522bf2cd4277f03c446)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addSchemaDependency", [construct]))

    @jsii.member(jsii_name="createResolver")
    def create_resolver(
        self,
        *,
        data_source: typing.Optional[BaseDataSource] = None,
        field_name: builtins.str,
        type_name: builtins.str,
        caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
    ) -> Resolver:
        '''(experimental) creates a new resolver for this datasource and API using the given properties.

        :param data_source: (experimental) The data source this resolver is using. Default: - No datasource
        :param field_name: (experimental) name of the GraphQL field in the given type this resolver is attached to.
        :param type_name: (experimental) name of the GraphQL type this resolver is attached to.
        :param caching_config: (experimental) The caching configuration for this resolver. Default: - No caching configuration
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array | undefined sets resolver to be of kind, unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template

        :stability: experimental
        '''
        props = ExtendedResolverProps(
            data_source=data_source,
            field_name=field_name,
            type_name=type_name,
            caching_config=caching_config,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
        )

        return typing.cast(Resolver, jsii.invoke(self, "createResolver", [props]))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    @abc.abstractmethod
    def api_id(self) -> builtins.str:
        '''(experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="arn")
    @abc.abstractmethod
    def arn(self) -> builtins.str:
        '''(experimental) the ARN of the API.

        :stability: experimental
        '''
        ...


class _GraphqlApiBaseProxy(
    GraphqlApiBase,
    jsii.proxy_for(_Resource_abff4495), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) the ARN of the API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, GraphqlApiBase).__jsii_proxy_class__ = lambda : _GraphqlApiBaseProxy


@jsii.implements(IField)
class GraphqlType(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_appsync.GraphqlType"):
    '''(experimental) The GraphQL Types in AppSync's GraphQL.

    GraphQL Types are the
    building blocks for object types, queries, mutations, etc. They are
    types like String, Int, Id or even Object Types you create.

    i.e. ``String``, ``String!``, ``[String]``, ``[String!]``, ``[String]!``

    GraphQL Types are used to define the entirety of schema.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # dummy_request: appsync.MappingTemplate
        # dummy_response: appsync.MappingTemplate
        
        info = appsync.ObjectType("Info",
            definition={
                "node": appsync.ResolvableField(
                    return_type=appsync.GraphqlType.string(),
                    args={
                        "id": appsync.GraphqlType.string()
                    },
                    data_source=api.add_none_data_source("none"),
                    request_mapping_template=dummy_request,
                    response_mapping_template=dummy_response
                )
            }
        )
    '''

    def __init__(
        self,
        type: Type,
        *,
        intermediate_type: typing.Optional[IIntermediateType] = None,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param type: -
        :param intermediate_type: (experimental) the intermediate type linked to this attribute. Default: - no intermediate type
        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c963e166295c6604e8c6342b6a209bb490a754134a33ef0acd2dcb457fcec62)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        options = GraphqlTypeOptions(
            intermediate_type=intermediate_type,
            is_list=is_list,
            is_required=is_required,
            is_required_list=is_required_list,
        )

        jsii.create(self.__class__, self, [type, options])

    @jsii.member(jsii_name="awsDate")
    @builtins.classmethod
    def aws_date(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSDate`` scalar type represents a valid extended ``ISO 8601 Date`` string.

        In other words, accepts date strings in the form of ``YYYY-MM-DD``. It accepts time zone offsets.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsDate", [options]))

    @jsii.member(jsii_name="awsDateTime")
    @builtins.classmethod
    def aws_date_time(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSDateTime`` scalar type represents a valid extended ``ISO 8601 DateTime`` string.

        In other words, accepts date strings in the form of ``YYYY-MM-DDThh:mm:ss.sssZ``. It accepts time zone offsets.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsDateTime", [options]))

    @jsii.member(jsii_name="awsEmail")
    @builtins.classmethod
    def aws_email(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSEmail`` scalar type represents an email address string (i.e.``username@example.com``).

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsEmail", [options]))

    @jsii.member(jsii_name="awsIpAddress")
    @builtins.classmethod
    def aws_ip_address(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSIPAddress`` scalar type respresents a valid ``IPv4`` of ``IPv6`` address string.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsIpAddress", [options]))

    @jsii.member(jsii_name="awsJson")
    @builtins.classmethod
    def aws_json(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSJson`` scalar type represents a JSON string.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsJson", [options]))

    @jsii.member(jsii_name="awsPhone")
    @builtins.classmethod
    def aws_phone(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSPhone`` scalar type represents a valid phone number. Phone numbers maybe be whitespace delimited or hyphenated.

        The number can specify a country code at the beginning, but is not required for US phone numbers.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsPhone", [options]))

    @jsii.member(jsii_name="awsTime")
    @builtins.classmethod
    def aws_time(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSTime`` scalar type represents a valid extended ``ISO 8601 Time`` string.

        In other words, accepts date strings in the form of ``hh:mm:ss.sss``. It accepts time zone offsets.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsTime", [options]))

    @jsii.member(jsii_name="awsTimestamp")
    @builtins.classmethod
    def aws_timestamp(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSTimestamp`` scalar type represents the number of seconds since ``1970-01-01T00:00Z``.

        Timestamps are serialized and deserialized as numbers.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsTimestamp", [options]))

    @jsii.member(jsii_name="awsUrl")
    @builtins.classmethod
    def aws_url(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``AWSURL`` scalar type represetns a valid URL string.

        URLs wihtout schemes or contain double slashes are considered invalid.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "awsUrl", [options]))

    @jsii.member(jsii_name="boolean")
    @builtins.classmethod
    def boolean(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``Boolean`` scalar type is a boolean value: true or false.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "boolean", [options]))

    @jsii.member(jsii_name="float")
    @builtins.classmethod
    def float(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``Float`` scalar type is a signed double-precision fractional value.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "float", [options]))

    @jsii.member(jsii_name="id")
    @builtins.classmethod
    def id(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``ID`` scalar type is a unique identifier. ``ID`` type is serialized similar to ``String``.

        Often used as a key for a cache and not intended to be human-readable.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "id", [options]))

    @jsii.member(jsii_name="int")
    @builtins.classmethod
    def int(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``Int`` scalar type is a signed non-fractional numerical value.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "int", [options]))

    @jsii.member(jsii_name="intermediate")
    @builtins.classmethod
    def intermediate(
        cls,
        *,
        intermediate_type: typing.Optional[IIntermediateType] = None,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) an intermediate type to be added as an attribute (i.e. an interface or an object type).

        :param intermediate_type: (experimental) the intermediate type linked to this attribute. Default: - no intermediate type
        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = GraphqlTypeOptions(
            intermediate_type=intermediate_type,
            is_list=is_list,
            is_required=is_required,
            is_required_list=is_required_list,
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "intermediate", [options]))

    @jsii.member(jsii_name="string")
    @builtins.classmethod
    def string(
        cls,
        *,
        is_list: typing.Optional[builtins.bool] = None,
        is_required: typing.Optional[builtins.bool] = None,
        is_required_list: typing.Optional[builtins.bool] = None,
    ) -> "GraphqlType":
        '''(experimental) ``String`` scalar type is a free-form human-readable text.

        :param is_list: (experimental) property determining if this attribute is a list i.e. if true, attribute would be [Type]. Default: - false
        :param is_required: (experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be Type! Default: - false
        :param is_required_list: (experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be [ Type ]! or if isRequired true, attribe would be [ Type! ]! Default: - false

        :stability: experimental
        '''
        options = BaseTypeOptions(
            is_list=is_list, is_required=is_required, is_required_list=is_required_list
        )

        return typing.cast("GraphqlType", jsii.sinvoke(cls, "string", [options]))

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''(experimental) Generate the arguments for this field.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "argsToString", []))

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        _modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
    ) -> builtins.str:
        '''(experimental) Generate the directives for this field.

        :param _modes: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138312be10672193c1a27fd2b8040e40c9dad08342dea1943777780c3e6bd122)
            check_type(argname="argument _modes", value=_modes, expected_type=type_hints["_modes"])
        return typing.cast(builtins.str, jsii.invoke(self, "directivesToString", [_modes]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Generate the string for this attribute.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="isList")
    def is_list(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is a list i.e. if true, attribute would be ``[Type]``.

        :default: - false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isList"))

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is non-nullable i.e. if true, attribute would be ``Type!`` and this attribute must always have a value.

        :default: - false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequired"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredList")
    def is_required_list(self) -> builtins.bool:
        '''(experimental) property determining if this attribute is a non-nullable list i.e. if true, attribute would be ``[ Type ]!`` and this attribute's list must always have a value.

        :default: - false

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isRequiredList"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> Type:
        '''(experimental) the type of attribute.

        :stability: experimental
        '''
        return typing.cast(Type, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="intermediateType")
    def intermediate_type(self) -> typing.Optional[IIntermediateType]:
        '''(experimental) the intermediate type linked to this attribute (i.e. an interface or an object).

        :default: - no intermediate type

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IIntermediateType], jsii.get(self, "intermediateType"))


class HttpDataSource(
    BackedDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.HttpDataSource",
):
    '''(experimental) An AppSync datasource backed by a http endpoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "api",
            name="api",
            schema=appsync.Schema.from_asset(path.join(__dirname, "schema.graphql"))
        )
        
        http_ds = api.add_http_data_source("ds", "https://states.amazonaws.com",
            name="httpDsWithStepF",
            description="from appsync to StepFunctions Workflow",
            authorization_config=appsync.aws_appsync.AwsIamConfig(
                signing_region="us-east-1",
                signing_service_name="states"
            )
        )
        
        http_ds.create_resolver(
            type_name="Mutation",
            field_name="callStepFunction",
            request_mapping_template=appsync.MappingTemplate.from_file("request.vtl"),
            response_mapping_template=appsync.MappingTemplate.from_file("response.vtl")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        endpoint: builtins.str,
        authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param endpoint: (experimental) The http endpoint.
        :param authorization_config: (experimental) The authorization config in case the HTTP endpoint requires authorization. Default: - none
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3188bbce17e95a84da8dad16eb7ed6e76729e1f503b76ceb206a7c41e10980a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpDataSourceProps(
            endpoint=endpoint,
            authorization_config=authorization_config,
            api=api,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class LambdaDataSource(
    BackedDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.LambdaDataSource",
):
    '''(experimental) An AppSync datasource backed by a Lambda function.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        from monocdk import aws_iam as iam
        from monocdk import aws_lambda as lambda_
        
        # function_: lambda.Function
        # graphql_api: appsync.GraphqlApi
        # role: iam.Role
        
        lambda_data_source = appsync.LambdaDataSource(self, "MyLambdaDataSource",
            api=graphql_api,
            lambda_function=function_,
        
            # the properties below are optional
            description="description",
            name="name",
            service_role=role
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_function: _IFunction_6e14f09e,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_function: (experimental) The Lambda function to call to interact with this data source.
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099bce405bfdff64228535c6b3e6b958204d1be052564214ac6b9676af228c91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaDataSourceProps(
            lambda_function=lambda_function,
            service_role=service_role,
            api=api,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.LambdaDataSourceProps",
    jsii_struct_bases=[BackedDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "service_role": "serviceRole",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaDataSourceProps(BackedDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        lambda_function: _IFunction_6e14f09e,
    ) -> None:
        '''(experimental) Properties for an AppSync Lambda datasource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param lambda_function: (experimental) The Lambda function to call to interact with this data source.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_iam as iam
            from monocdk import aws_lambda as lambda_
            
            # function_: lambda.Function
            # graphql_api: appsync.GraphqlApi
            # role: iam.Role
            
            lambda_data_source_props = appsync.LambdaDataSourceProps(
                api=graphql_api,
                lambda_function=function_,
            
                # the properties below are optional
                description="description",
                name="name",
                service_role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fe10ae30483b3e4de861468f1cba36a67ef2aa217c2e4b9f230947c576e720)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "lambda_function": lambda_function,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to be assumed by AppSync to interact with the data source.

        :default: - Create a new role

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def lambda_function(self) -> _IFunction_6e14f09e:
        '''(experimental) The Lambda function to call to interact with this data source.

        :stability: experimental
        '''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_IFunction_6e14f09e, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OpenSearchDataSource(
    BackedDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.OpenSearchDataSource",
):
    '''(experimental) An Appsync datasource backed by OpenSearch.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as opensearch
        
        # api: appsync.GraphqlApi
        
        
        user = iam.User(self, "User")
        domain = opensearch.Domain(self, "Domain",
            version=opensearch.EngineVersion.OPENSEARCH_1_2,
            removal_policy=RemovalPolicy.DESTROY,
            fine_grained_access_control=opensearch.aws_opensearchservice.AdvancedSecurityOptions(master_user_arn=user.user_arn),
            encryption_at_rest=opensearch.aws_opensearchservice.EncryptionAtRestOptions(enabled=True),
            node_to_node_encryption=True,
            enforce_https=True
        )
        ds = api.add_open_search_data_source("ds", domain)
        
        ds.create_resolver(
            type_name="Query",
            field_name="getTests",
            request_mapping_template=appsync.MappingTemplate.from_string(JSON.stringify({
                "version": "2017-02-28",
                "operation": "GET",
                "path": "/id/post/_search",
                "params": {
                    "headers": {},
                    "query_string": {},
                    "body": {"from": 0, "size": 50}
                }
            })),
            response_mapping_template=appsync.MappingTemplate.from_string("""[
                    #foreach($entry in $context.result.hits.hits)
                    #if( $velocityCount > 1 ) , #end
                    $utils.toJson($entry.get("_source"))
                    #end
                  ]""")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: _IDomain_cb64a2bc,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain: (experimental) The OpenSearch domain containing the endpoint for the data source.
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400e5c966b25eb714c886bdbbc343c6873ce55fdb153182bc1f5f0a20704f33b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = OpenSearchDataSourceProps(
            domain=domain,
            service_role=service_role,
            api=api,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.OpenSearchDataSourceProps",
    jsii_struct_bases=[BackedDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "service_role": "serviceRole",
        "domain": "domain",
    },
)
class OpenSearchDataSourceProps(BackedDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        domain: _IDomain_cb64a2bc,
    ) -> None:
        '''(experimental) Properties for the OpenSearch Data Source.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param domain: (experimental) The OpenSearch domain containing the endpoint for the data source.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_iam as iam
            from monocdk import aws_opensearchservice as opensearchservice
            
            # domain: opensearchservice.Domain
            # graphql_api: appsync.GraphqlApi
            # role: iam.Role
            
            open_search_data_source_props = appsync.OpenSearchDataSourceProps(
                api=graphql_api,
                domain=domain,
            
                # the properties below are optional
                description="description",
                name="name",
                service_role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235ea9c69820965cf8d2b746e06d922051093030a19b53b615e7951ef7098018)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "domain": domain,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to be assumed by AppSync to interact with the data source.

        :default: - Create a new role

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def domain(self) -> _IDomain_cb64a2bc:
        '''(experimental) The OpenSearch domain containing the endpoint for the data source.

        :stability: experimental
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(_IDomain_cb64a2bc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenSearchDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PartitionKey(
    PrimaryKey,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.PartitionKey",
):
    '''(experimental) Specifies the assignment to the partition key.

    It can be
    enhanced with the assignment of the sort key.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appsync as appsync
        
        # assign: appsync.Assign
        
        partition_key = appsync.PartitionKey(assign)
    '''

    def __init__(self, pkey: Assign) -> None:
        '''
        :param pkey: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea7948fb50b16bbf86624fa544289da83cf883ae81ef0bd87108d8b904c9920)
            check_type(argname="argument pkey", value=pkey, expected_type=type_hints["pkey"])
        jsii.create(self.__class__, self, [pkey])

    @jsii.member(jsii_name="sort")
    def sort(self, key: builtins.str) -> SortKeyStep:
        '''(experimental) Allows assigning a value to the sort key.

        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a37e32f75471d8873e51226c4a9bdb92fb360d52c166e7d6e9f2b1861dcfc5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(SortKeyStep, jsii.invoke(self, "sort", [key]))


class RdsDataSource(
    BackedDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.RdsDataSource",
):
    '''(experimental) An AppSync datasource backed by RDS.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Build a data source for AppSync to access the database.
        # api: appsync.GraphqlApi
        # Create username and password secret for DB Cluster
        secret = rds.DatabaseSecret(self, "AuroraSecret",
            username="clusteradmin"
        )
        
        # The VPC to place the cluster in
        vpc = ec2.Vpc(self, "AuroraVpc")
        
        # Create the serverless cluster, provide all values needed to customise the database.
        cluster = rds.ServerlessCluster(self, "AuroraCluster",
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
            vpc=vpc,
            credentials={"username": "clusteradmin"},
            cluster_identifier="db-endpoint-test",
            default_database_name="demos"
        )
        rds_dS = api.add_rds_data_source("rds", cluster, secret, "demos")
        
        # Set up a resolver for an RDS query.
        rds_dS.create_resolver(
            type_name="Query",
            field_name="getDemosRds",
            request_mapping_template=appsync.MappingTemplate.from_string("""
                  {
                    "version": "2018-05-29",
                    "statements": [
                      "SELECT * FROM demos"
                    ]
                  }
                  """),
            response_mapping_template=appsync.MappingTemplate.from_string("""
                    $utils.toJson($utils.rds.toJsonObject($ctx.result)[0])
                  """)
        )
        
        # Set up a resolver for an RDS mutation.
        rds_dS.create_resolver(
            type_name="Mutation",
            field_name="addDemoRds",
            request_mapping_template=appsync.MappingTemplate.from_string("""
                  {
                    "version": "2018-05-29",
                    "statements": [
                      "INSERT INTO demos VALUES (:id, :version)",
                      "SELECT * WHERE id = :id"
                    ],
                    "variableMap": {
                      ":id": $util.toJson($util.autoId()),
                      ":version": $util.toJson($ctx.args.version)
                    }
                  }
                  """),
            response_mapping_template=appsync.MappingTemplate.from_string("""
                    $utils.toJson($utils.rds.toJsonObject($ctx.result)[1][0])
                  """)
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        secret_store: _ISecret_22fb8757,
        serverless_cluster: _IServerlessCluster_8ed6177c,
        database_name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secret_store: (experimental) The secret containing the credentials for the database.
        :param serverless_cluster: (experimental) The serverless cluster to call to interact with this data source.
        :param database_name: (experimental) The name of the database to use within the cluster. Default: - None
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5daf762ee6b6669f84ef3c64a11cd79b7cb918997de9afc87313d25401dfad1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RdsDataSourceProps(
            secret_store=secret_store,
            serverless_cluster=serverless_cluster,
            database_name=database_name,
            service_role=service_role,
            api=api,
            description=description,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_appsync.RdsDataSourceProps",
    jsii_struct_bases=[BackedDataSourceProps],
    name_mapping={
        "api": "api",
        "description": "description",
        "name": "name",
        "service_role": "serviceRole",
        "secret_store": "secretStore",
        "serverless_cluster": "serverlessCluster",
        "database_name": "databaseName",
    },
)
class RdsDataSourceProps(BackedDataSourceProps):
    def __init__(
        self,
        *,
        api: IGraphqlApi,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[_IRole_59af6f50] = None,
        secret_store: _ISecret_22fb8757,
        serverless_cluster: _IServerlessCluster_8ed6177c,
        database_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an AppSync RDS datasource.

        :param api: (experimental) The API to attach this data source to.
        :param description: (experimental) the description of the data source. Default: - None
        :param name: (experimental) The name of the data source. Default: - id of data source
        :param service_role: (experimental) The IAM service role to be assumed by AppSync to interact with the data source. Default: - Create a new role
        :param secret_store: (experimental) The secret containing the credentials for the database.
        :param serverless_cluster: (experimental) The serverless cluster to call to interact with this data source.
        :param database_name: (experimental) The name of the database to use within the cluster. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appsync as appsync
            from monocdk import aws_iam as iam
            from monocdk import aws_rds as rds
            from monocdk import aws_secretsmanager as secretsmanager
            
            # graphql_api: appsync.GraphqlApi
            # role: iam.Role
            # secret: secretsmanager.Secret
            # serverless_cluster: rds.ServerlessCluster
            
            rds_data_source_props = appsync.RdsDataSourceProps(
                api=graphql_api,
                secret_store=secret,
                serverless_cluster=serverless_cluster,
            
                # the properties below are optional
                database_name="databaseName",
                description="description",
                name="name",
                service_role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe8036fa2733542ce4aa4a5fcfdb1421dd399232880fb8b8c46f04c88644dab8)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument secret_store", value=secret_store, expected_type=type_hints["secret_store"])
            check_type(argname="argument serverless_cluster", value=serverless_cluster, expected_type=type_hints["serverless_cluster"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "secret_store": secret_store,
            "serverless_cluster": serverless_cluster,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if service_role is not None:
            self._values["service_role"] = service_role
        if database_name is not None:
            self._values["database_name"] = database_name

    @builtins.property
    def api(self) -> IGraphqlApi:
        '''(experimental) The API to attach this data source to.

        :stability: experimental
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(IGraphqlApi, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) the description of the data source.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the data source.

        :default: - id of data source

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to be assumed by AppSync to interact with the data source.

        :default: - Create a new role

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def secret_store(self) -> _ISecret_22fb8757:
        '''(experimental) The secret containing the credentials for the database.

        :stability: experimental
        '''
        result = self._values.get("secret_store")
        assert result is not None, "Required property 'secret_store' is missing"
        return typing.cast(_ISecret_22fb8757, result)

    @builtins.property
    def serverless_cluster(self) -> _IServerlessCluster_8ed6177c:
        '''(experimental) The serverless cluster to call to interact with this data source.

        :stability: experimental
        '''
        result = self._values.get("serverless_cluster")
        assert result is not None, "Required property 'serverless_cluster' is missing"
        return typing.cast(_IServerlessCluster_8ed6177c, result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the database to use within the cluster.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IField)
class Field(
    GraphqlType,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.Field",
):
    '''(experimental) Fields build upon Graphql Types and provide typing and arguments.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        field = appsync.Field(
            return_type=appsync.GraphqlType.string(),
            args={
                "argument": appsync.GraphqlType.string()
            }
        )
        type = appsync.InterfaceType("Node",
            definition={"test": field}
        )
    '''

    def __init__(
        self,
        *,
        return_type: GraphqlType,
        args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param return_type: (experimental) The return type for this field.
        :param args: (experimental) The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: (experimental) the directives for this field. Default: - no directives

        :stability: experimental
        '''
        options = FieldOptions(
            return_type=return_type, args=args, directives=directives
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="argsToString")
    def args_to_string(self) -> builtins.str:
        '''(experimental) Generate the args string of this resolvable field.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "argsToString", []))

    @jsii.member(jsii_name="directivesToString")
    def directives_to_string(
        self,
        modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
    ) -> builtins.str:
        '''(experimental) Generate the directives for this field.

        :param modes: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706d4a76118b94d0ac93ff4e2a733e24f5dcdea51135ec7af0dc8895ef474832)
            check_type(argname="argument modes", value=modes, expected_type=type_hints["modes"])
        return typing.cast(builtins.str, jsii.invoke(self, "directivesToString", [modes]))

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional[ResolvableFieldOptions]:
        '''(experimental) The options for this field.

        :default: - no arguments

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ResolvableFieldOptions], jsii.get(self, "fieldOptions"))


class GraphqlApi(
    GraphqlApiBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.GraphqlApi",
):
    '''(experimental) An AppSync GraphQL API.

    :stability: experimental
    :resource: AWS::AppSync::GraphQLApi
    :exampleMetadata: infused

    Example::

        api = appsync.GraphqlApi(self, "Api",
            name="demo"
        )
        demo = appsync.ObjectType("Demo",
            definition={
                "id": appsync.GraphqlType.string(is_required=True),
                "version": appsync.GraphqlType.string(is_required=True)
            }
        )
        
        api.add_type(demo)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        authorization_config: typing.Optional[typing.Union[AuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        domain_name: typing.Optional[typing.Union[DomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_config: typing.Optional[typing.Union[LogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        schema: typing.Optional[Schema] = None,
        xray_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) the name of the GraphQL API.
        :param authorization_config: (experimental) Optional authorization configuration. Default: - API Key authorization
        :param domain_name: (experimental) The domain name configuration for the GraphQL API. The Route 53 hosted zone and CName DNS record must be configured in addition to this setting to enable custom domain URL Default: - no domain name
        :param log_config: (experimental) Logging configuration for this api. Default: - None
        :param schema: (experimental) GraphQL schema definition. Specify how you want to define your schema. Schema.fromFile(filePath: string) allows schema definition through schema.graphql file Default: - schema will be generated code-first (i.e. addType, addObjectType, etc.)
        :param xray_enabled: (experimental) A flag indicating whether or not X-Ray tracing is enabled for the GraphQL API. Default: - false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02467b263fa8045081e369d3dd29eaffb8ed797f2227eb1239bded3808ea231f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GraphqlApiProps(
            name=name,
            authorization_config=authorization_config,
            domain_name=domain_name,
            log_config=log_config,
            schema=schema,
            xray_enabled=xray_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGraphqlApiAttributes")
    @builtins.classmethod
    def from_graphql_api_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        graphql_api_id: builtins.str,
        graphql_api_arn: typing.Optional[builtins.str] = None,
    ) -> IGraphqlApi:
        '''(experimental) Import a GraphQL API through this function.

        :param scope: scope.
        :param id: id.
        :param graphql_api_id: (experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.
        :param graphql_api_arn: (experimental) the arn for the GraphQL Api. Default: - autogenerated arn

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8a2899bd0c3f594aa11e730dcff682d399e51a71cc67dbdcf509ad19a4895b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = GraphqlApiAttributes(
            graphql_api_id=graphql_api_id, graphql_api_arn=graphql_api_arn
        )

        return typing.cast(IGraphqlApi, jsii.sinvoke(cls, "fromGraphqlApiAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addMutation")
    def add_mutation(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> ObjectType:
        '''(experimental) Add a mutation field to the schema's Mutation. CDK will create an Object Type called 'Mutation'. For example,.

        type Mutation {
        fieldName: Field.returnType
        }

        :param field_name: the name of the Mutation.
        :param field: the resolvable field to for this Mutation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__374a3832ffaa074ab09e44de8c556e31825a1d7ab1178981ec9bd7a9bbd67fbf)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(ObjectType, jsii.invoke(self, "addMutation", [field_name, field]))

    @jsii.member(jsii_name="addQuery")
    def add_query(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> ObjectType:
        '''(experimental) Add a query field to the schema's Query. CDK will create an Object Type called 'Query'. For example,.

        type Query {
        fieldName: Field.returnType
        }

        :param field_name: the name of the query.
        :param field: the resolvable field to for this query.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e2b829939b83dea1e9e306d13790d4807908c3bd71d34969d38a90d435c908)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(ObjectType, jsii.invoke(self, "addQuery", [field_name, field]))

    @jsii.member(jsii_name="addSchemaDependency")
    def add_schema_dependency(self, construct: _CfnResource_e0a482dc) -> builtins.bool:
        '''(experimental) Add schema dependency to a given construct.

        :param construct: the dependee.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807a365e5fa722a5756f18e864d6f48ec381cb73faf41fdcc8b7208ab8d345d6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addSchemaDependency", [construct]))

    @jsii.member(jsii_name="addSubscription")
    def add_subscription(
        self,
        field_name: builtins.str,
        field: "ResolvableField",
    ) -> ObjectType:
        '''(experimental) Add a subscription field to the schema's Subscription. CDK will create an Object Type called 'Subscription'. For example,.

        type Subscription {
        fieldName: Field.returnType
        }

        :param field_name: the name of the Subscription.
        :param field: the resolvable field to for this Subscription.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11a1c229f043bc04bb5add59a599fb51bd4e9990cebaee2e96b1ab60e9683c8)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(ObjectType, jsii.invoke(self, "addSubscription", [field_name, field]))

    @jsii.member(jsii_name="addToSchema")
    def add_to_schema(
        self,
        addition: builtins.str,
        delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Escape hatch to append to Schema as desired.

        Will always result
        in a newline.

        :param addition: the addition to add to schema.
        :param delimiter: the delimiter between schema and addition.

        :default: - ''

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd9763935faa03e372410bad7ed1860277685c20933aada8d2fc89e396018eb)
            check_type(argname="argument addition", value=addition, expected_type=type_hints["addition"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        return typing.cast(None, jsii.invoke(self, "addToSchema", [addition, delimiter]))

    @jsii.member(jsii_name="addType")
    def add_type(self, type: IIntermediateType) -> IIntermediateType:
        '''(experimental) Add type to the schema.

        :param type: the intermediate type to add to the schema.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487400b6ccbc63d5499625a6fa811c9d14a2434152fa85e4da7488aea0ca69d3)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        return typing.cast(IIntermediateType, jsii.invoke(self, "addType", [type]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        resources: IamResource,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement associated with this GraphQLApi to an IAM principal's policy.

        :param grantee: The principal.
        :param resources: The set of resources to allow (i.e. ...:[region]:[accountId]:apis/GraphQLId/...).
        :param actions: The actions that should be granted to the principal (i.e. appsync:graphql ).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca7e5ff46e26d07b70ef651962185b9a2e8368396c84d68b664249b484ddf1e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, resources, *actions]))

    @jsii.member(jsii_name="grantMutation")
    def grant_mutation(
        self,
        grantee: _IGrantable_4c5a91d1,
        *fields: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement for Mutation access to this GraphQLApi to an IAM principal's policy.

        :param grantee: The principal.
        :param fields: The fields to grant access to that are Mutations (leave blank for all).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e945a58acadde5aa7f3db6765954214f006b32b6c347fd2e12d9567466bf557e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantMutation", [grantee, *fields]))

    @jsii.member(jsii_name="grantQuery")
    def grant_query(
        self,
        grantee: _IGrantable_4c5a91d1,
        *fields: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement for Query access to this GraphQLApi to an IAM principal's policy.

        :param grantee: The principal.
        :param fields: The fields to grant access to that are Queries (leave blank for all).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3263ab8384c549a37797e8e47f26c6dbd46f4c33ca432e04fb06eccf0e1ee52)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantQuery", [grantee, *fields]))

    @jsii.member(jsii_name="grantSubscription")
    def grant_subscription(
        self,
        grantee: _IGrantable_4c5a91d1,
        *fields: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Adds an IAM policy statement for Subscription access to this GraphQLApi to an IAM principal's policy.

        :param grantee: The principal.
        :param fields: The fields to grant access to that are Subscriptions (leave blank for all).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db571759598abff5ff3d04c645bb9c57152679c9232e185e1c6b0535f4f33098)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantSubscription", [grantee, *fields]))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        '''(experimental) an unique AWS AppSync GraphQL API identifier i.e. 'lxz775lwdrgcndgz3nurvac7oa'.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) the ARN of the API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="graphqlUrl")
    def graphql_url(self) -> builtins.str:
        '''(experimental) the URL of the endpoint created by AppSync.

        :stability: experimental
        :attribute: GraphQlUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "graphqlUrl"))

    @builtins.property
    @jsii.member(jsii_name="modes")
    def modes(self) -> typing.List[AuthorizationType]:
        '''(experimental) The Authorization Types for this GraphQL Api.

        :stability: experimental
        '''
        return typing.cast(typing.List[AuthorizationType], jsii.get(self, "modes"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) the name of the API.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> Schema:
        '''(experimental) the schema attached to this api.

        :stability: experimental
        '''
        return typing.cast(Schema, jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) the configured API key, if present.

        :default: - no api key

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))


@jsii.implements(IField)
class ResolvableField(
    Field,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appsync.ResolvableField",
):
    '''(experimental) Resolvable Fields build upon Graphql Types and provide fields that can resolve into operations on a data source.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # api: appsync.GraphqlApi
        # dummy_request: appsync.MappingTemplate
        # dummy_response: appsync.MappingTemplate
        
        info = appsync.ObjectType("Info",
            definition={
                "node": appsync.ResolvableField(
                    return_type=appsync.GraphqlType.string(),
                    args={
                        "id": appsync.GraphqlType.string()
                    },
                    data_source=api.add_none_data_source("none"),
                    request_mapping_template=dummy_request,
                    response_mapping_template=dummy_response
                )
            }
        )
    '''

    def __init__(
        self,
        *,
        data_source: typing.Optional[BaseDataSource] = None,
        pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
        request_mapping_template: typing.Optional[MappingTemplate] = None,
        response_mapping_template: typing.Optional[MappingTemplate] = None,
        return_type: GraphqlType,
        args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
        directives: typing.Optional[typing.Sequence[Directive]] = None,
    ) -> None:
        '''
        :param data_source: (experimental) The data source creating linked to this resolvable field. Default: - no data source
        :param pipeline_config: (experimental) configuration of the pipeline resolver. Default: - no pipeline resolver configuration An empty array or undefined prop will set resolver to be of type unit
        :param request_mapping_template: (experimental) The request mapping template for this resolver. Default: - No mapping template
        :param response_mapping_template: (experimental) The response mapping template for this resolver. Default: - No mapping template
        :param return_type: (experimental) The return type for this field.
        :param args: (experimental) The arguments for this field. i.e. type Example (first: String second: String) {} - where 'first' and 'second' are key values for args and 'String' is the GraphqlType Default: - no arguments
        :param directives: (experimental) the directives for this field. Default: - no directives

        :stability: experimental
        '''
        options = ResolvableFieldOptions(
            data_source=data_source,
            pipeline_config=pipeline_config,
            request_mapping_template=request_mapping_template,
            response_mapping_template=response_mapping_template,
            return_type=return_type,
            args=args,
            directives=directives,
        )

        jsii.create(self.__class__, self, [options])

    @builtins.property
    @jsii.member(jsii_name="fieldOptions")
    def field_options(self) -> typing.Optional[ResolvableFieldOptions]:
        '''(experimental) The options to make this field resolvable.

        :default: - not a resolvable field

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ResolvableFieldOptions], jsii.get(self, "fieldOptions"))


__all__ = [
    "AddFieldOptions",
    "ApiKeyConfig",
    "AppsyncFunction",
    "AppsyncFunctionAttributes",
    "AppsyncFunctionProps",
    "Assign",
    "AttributeValues",
    "AttributeValuesStep",
    "AuthorizationConfig",
    "AuthorizationMode",
    "AuthorizationType",
    "AwsIamConfig",
    "BackedDataSource",
    "BackedDataSourceProps",
    "BaseAppsyncFunctionProps",
    "BaseDataSource",
    "BaseDataSourceProps",
    "BaseResolverProps",
    "BaseTypeOptions",
    "CachingConfig",
    "CfnApiCache",
    "CfnApiCacheProps",
    "CfnApiKey",
    "CfnApiKeyProps",
    "CfnDataSource",
    "CfnDataSourceProps",
    "CfnDomainName",
    "CfnDomainNameApiAssociation",
    "CfnDomainNameApiAssociationProps",
    "CfnDomainNameProps",
    "CfnFunctionConfiguration",
    "CfnFunctionConfigurationProps",
    "CfnGraphQLApi",
    "CfnGraphQLApiProps",
    "CfnGraphQLSchema",
    "CfnGraphQLSchemaProps",
    "CfnResolver",
    "CfnResolverProps",
    "DataSourceOptions",
    "Directive",
    "DomainOptions",
    "DynamoDbDataSource",
    "DynamoDbDataSourceProps",
    "ElasticsearchDataSource",
    "ElasticsearchDataSourceProps",
    "EnumType",
    "EnumTypeOptions",
    "ExtendedDataSourceProps",
    "ExtendedResolverProps",
    "Field",
    "FieldLogLevel",
    "FieldOptions",
    "GraphqlApi",
    "GraphqlApiAttributes",
    "GraphqlApiBase",
    "GraphqlApiProps",
    "GraphqlType",
    "GraphqlTypeOptions",
    "HttpDataSource",
    "HttpDataSourceOptions",
    "HttpDataSourceProps",
    "IAppsyncFunction",
    "IField",
    "IGraphqlApi",
    "IIntermediateType",
    "IamResource",
    "InputType",
    "InterfaceType",
    "IntermediateTypeOptions",
    "KeyCondition",
    "LambdaAuthorizerConfig",
    "LambdaDataSource",
    "LambdaDataSourceProps",
    "LogConfig",
    "MappingTemplate",
    "NoneDataSource",
    "NoneDataSourceProps",
    "ObjectType",
    "ObjectTypeOptions",
    "OpenIdConnectConfig",
    "OpenSearchDataSource",
    "OpenSearchDataSourceProps",
    "PartitionKey",
    "PartitionKeyStep",
    "PrimaryKey",
    "RdsDataSource",
    "RdsDataSourceProps",
    "ResolvableField",
    "ResolvableFieldOptions",
    "Resolver",
    "ResolverProps",
    "Schema",
    "SchemaOptions",
    "SortKeyStep",
    "Type",
    "UnionType",
    "UnionTypeOptions",
    "UserPoolConfig",
    "UserPoolDefaultAction",
    "Values",
]

publication.publish()

def _typecheckingstub__d5c4b5ba5ddc105148a19797b94b8291a268f45937207f8edc4fddc44c7a4146(
    *,
    field: typing.Optional[IField] = None,
    field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231f3250183cc31a44bfd28a36a4194a41f06c1dfd7be8b83343308f4d6c7445(
    *,
    description: typing.Optional[builtins.str] = None,
    expires: typing.Optional[_Expiration_505df041] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db829bb9d3941cda1e447de3022cc090de917aca302df8a954fd679ecea9b423(
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b3c4b5913e45e95b058dfcfd2c40d9b4e51dfc1b9c20e9e937a48d07d054e0(
    attr: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412d93a11445bd2d219e7628787a1cdeedf090de56d31c720935defb7cdaf3b8(
    map: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d382ab11578ec047f1a85108822bfe1eb552059c762eefa1fee55544e326a31c(
    container: builtins.str,
    assignments: typing.Optional[typing.Sequence[Assign]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432b5187af9b456765e04f46081a3db17e0ac0f39665f59fa6b1f1b126ff860f(
    attr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feee645b88bff9ed76fe8f2d7fb48c1ee81f6e4788e59d2770b8c3633ddcc167(
    attr: builtins.str,
    container: builtins.str,
    assignments: typing.Sequence[Assign],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dfec8500382f9b4a10831734f75973c88cbadc038eabc6b94b4af305dd655d(
    val: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f848df7434aeebf6be81eb6719f92a928024a60b10ddf122117f892ce385af3c(
    *,
    additional_authorization_modes: typing.Optional[typing.Sequence[typing.Union[AuthorizationMode, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_authorization: typing.Optional[typing.Union[AuthorizationMode, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37fd6e5348ae8cdad8e885cafe8fb4f61ae31174630831c10bd199a2362b959(
    *,
    authorization_type: AuthorizationType,
    api_key_config: typing.Optional[typing.Union[ApiKeyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[LambdaAuthorizerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    open_id_connect_config: typing.Optional[typing.Union[OpenIdConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    user_pool_config: typing.Optional[typing.Union[UserPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf50fd1171074e0c8e2cd82d65775d36b74bda43f87437414522135d3b916380(
    *,
    signing_region: builtins.str,
    signing_service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437cd7588080049d00ffa12e64d0b9283690d742bedea2f3ae376e2b5de9da16(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ada652827c62a80544a99a875a0d6add183d4724e27756d693413d167292ef(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[BackedDataSourceProps, typing.Dict[builtins.str, typing.Any]],
    *,
    type: builtins.str,
    dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8de15a2db1e815bf851adec5a0ea508d6103ed1905e54ed9a1cb260966dbc3(
    value: IGraphqlApi,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6ec40ecd72f76ba4438036f7cad4e938af94241b98bca9eadd7c45704c31b6(
    value: typing.Optional[_IRole_59af6f50],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae5bedb607ee01f50ce0f93bb0aa849e62481c6b4eb21263326d28ddef301b9(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82c10d3fa82355396b4b487e2da6c7e5bfabddbfd5d9a96f827f92fc45092ec(
    *,
    field_name: builtins.str,
    type_name: builtins.str,
    caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a62a9572878684cde53bd79baa23d3ce75a82e76d1b31c0131d69a9f98a8f4(
    *,
    is_list: typing.Optional[builtins.bool] = None,
    is_required: typing.Optional[builtins.bool] = None,
    is_required_list: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b85095182209411ec213c9887a34eeac0c3086ac918c64aa9610ea1662001dd(
    *,
    ttl: _Duration_070aa057,
    caching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cdfa82f8a00d54b852478e6dca196494ef6e27ea8753d1488137e7a5084bd1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_caching_behavior: builtins.str,
    api_id: builtins.str,
    ttl: jsii.Number,
    type: builtins.str,
    at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8aff2fce593096fdf95c82192af7d32fc14bd55cc5c8a06154f4517ea0453a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2bfb2ac9948e9fda22ff0bd7ce79ffd32a655acde3125efc21fd9cd67923bc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce7ff4041a1ae1111843e0ee8d3cba8fb207cda3b154dc0c72baff2d9ffcf7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1a0e916b7b0c74d551bfab209057efb424e6c1c43eca8a15752384e81d84b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114083910e6a9df2fee43dc42e9767b117a48f81594e07378a375d1095ee2e87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f507cf5618125723d74b80c438669bd10f3206628ffe638a64430a1d391229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7839cdbcff7bebd705ae658d2f6b76a54caed43046501cae192f20ea83f064df(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e2ab3c9c706ef5ff8a1054f3379e3f1531b8066995f14f21f72d0b0bbf4ad2(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d55a5bb56c62477c5e22957bb380ccacb31106fa2c989d2291f95befc788e31(
    *,
    api_caching_behavior: builtins.str,
    api_id: builtins.str,
    ttl: jsii.Number,
    type: builtins.str,
    at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1745329398fb4f72199eca022835c6074caedd37e668df16abdb9a9b4e5d6984(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_id: builtins.str,
    api_key_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    expires: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3e339ada370820eb79a9f5e8ebd75e18d38367f6c11141a2faf024238f9cfa(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cebfa9b7770aae191eeae939b654d51bcdc1e07df730452c5f0c3cb5fb4304(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae2c70284c80b8245add8dc7d84cdad15a74d6ec15562a15eb093de677bad9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7c008d27865ff54024321b431c9eb907868226f0dbc6b157b9749a0bcf4372(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a2bb63e3ecc8b090e43a5f3cc1d2c299dcc4a65dcf136a08bd6c505db1e65a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216fb64032d083c12ae64ef1684d526682f7781e6cf09789f6919cce5ee13a3b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9caca502fddf7e46a2b754450e9d49003c66dbdeaa9688d5d905c8a1c7a664(
    *,
    api_id: builtins.str,
    api_key_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    expires: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e431d54ec028379c69f90936ec4cf0f9985c93757792a0a189198ca63dd3417(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8989352e31e20213df451568da1421d13a2c2cd4bce0cb24f318832301db7912(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7e31af7eb72e51701963db17729da8ea28eb791981047c21e22712decf43b8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c65343426b168d311f189fbb09cf8e90d100020a734269e7eaa5b70031c5c28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe9b37238ec27282392ce35c07aa903de923c4cd651150cc57c21307d499e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbb29468a31f6c1178b0b8b1473a9192bcbb80367b00bf7c8d29fbf5e8e01f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d4d032ca0587858e15d01722950d5c8f508a8cfc582a3cf651013db7bb0497(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f4efecdb8ceeb7045c9ec8b1fc10409c55514aac08172ee8e032a0b61fe19e4(
    value: typing.Optional[typing.Union[CfnDataSource.DynamoDBConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a36bef672a8de25f720628b763e637aec206e5ddd474f98a49813bde94d7e8e(
    value: typing.Optional[typing.Union[CfnDataSource.ElasticsearchConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f59db87bddc78318d2a5982aca0be01132630bca4e430094b06743060da9b1b(
    value: typing.Optional[typing.Union[CfnDataSource.HttpConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39c10684ed637eeee09f1da0f73604586c6acc7bc158aab11224473627a4d5f(
    value: typing.Optional[typing.Union[CfnDataSource.LambdaConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2825b54c35598c2171e9332b4a1b2d55c336ec02e8d4a7ed6e06a9fd994b98(
    value: typing.Optional[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556d03654260bac78a94ad054991337eb8c28ceadcb2e0c2d96f163d86b3bde5(
    value: typing.Optional[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0d09146ba59b68e772788e4bba9fac807dbc42daed968db2ef1a2b7eacffc9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b04dfa1d3d91eafb88eb48c7ef694b6cbd4533734a9ce44a5c8efab25e52af5(
    *,
    authorization_type: builtins.str,
    aws_iam_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.AwsIamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d025a9f69b375ff9c14b4025695a09b43cad87f47cc54b86afe2abdccc82cb(
    *,
    signing_region: typing.Optional[builtins.str] = None,
    signing_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002fefce098119d7807f102bfb8fa5cb58a916dfea56d346c62a00b9f2229787(
    *,
    base_table_ttl: builtins.str,
    delta_sync_table_name: builtins.str,
    delta_sync_table_ttl: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f8bcd36bc52d321d0e2ef8d97d7f1d4747fe5cd92c0f4c75efc16a9cb62e93(
    *,
    aws_region: builtins.str,
    table_name: builtins.str,
    delta_sync_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DeltaSyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    versioned: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a472816ee8b6c7c75479bacb28bc57db1828bc476a2bf694128b1b777719e1d3(
    *,
    aws_region: builtins.str,
    endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45b64328df1caa2ec1d85914400d158de5cc8a49d343fa665511e730682cc30(
    *,
    endpoint: builtins.str,
    authorization_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.AuthorizationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbb038aa1971a0c3704f0ae253d7789ed9fac53b2b16587aa39b5272a567810(
    *,
    lambda_function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3cf1b5f592283a36a78887e4c15e61657749972d80ff310698e9451ba6f3da(
    *,
    aws_region: builtins.str,
    endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab254f472dedea9a2341a5f1a0201694d5f07e35405db2366d53837c7ee7e5e(
    *,
    aws_region: builtins.str,
    aws_secret_store_arn: builtins.str,
    db_cluster_identifier: builtins.str,
    database_name: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936196738212b36f5ede32936516ef8771c3006966d5c21c86c03c0d1b6b6508(
    *,
    relational_database_source_type: builtins.str,
    rds_http_endpoint_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RdsHttpEndpointConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461cab08db471753f15462f9f788c8833450b644b1e7837a0fe7d3b7014f4164(
    *,
    api_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cd07ce7fc54ba9e3dec979c1d5e3e74a4b14ee1b7a55ba57cd2786c4f8ff07(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    certificate_arn: builtins.str,
    domain_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3eee087600f3f00e81f4316ee26dcb291017a979c85649fff8e8d1c5a88b3aa(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a9c9a505716d85401effc76de7f028562c88ad8430a224e9c2f2e8443e71e0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c267cc3ec351886e5b4b9eeb8f59b49c0bb00f1e753df2edc2c6e6f40f8bbc3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bff469b1d6803182249cce539b2c5279ffc69e719d87a4569fe99096c32e19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e74c052fcbe0e208df2030185d3233fafabed6a6eaa09a148d38dae8c3cb63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c111e17fdda67e1c931c1f91d860a523db0d11880404cf6c2ec4c888aceca5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_id: builtins.str,
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ce9d260f40f2cd1aa34b0d19210955a0b9b72ffcb87800a2d09c3ccfb23de3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad77bfa6625db42cda10ee139bf625764e4bbd484792ebecbcc62fb585f3412(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c124f6029727b6a0b445ccb4575dc8305afd5502a0cbaf5dda768b49255a7c33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1770662fa786f424d1da34acf174df57b58b1e5a095a19a8dba52dfc6085bb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca963d0664c8ef45159b15ac49f48257a8d94428fd34cec32c455123b8c1bb8(
    *,
    api_id: builtins.str,
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de883ad249a4b3579f2993df07f3b93b5a7aadb0c35d5a58eebf43ae3e8a2b2e(
    *,
    certificate_arn: builtins.str,
    domain_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bd9bb1b61f79670b1ed1114a848ff51681eec780bc37428f72c52aa883e747(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_id: builtins.str,
    data_source_name: builtins.str,
    name: builtins.str,
    code: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    function_version: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sync_config: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3b6ec2a694b35ffad067487492cda5beb79ba200ec410e19f519d71af17c0b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f24e127821dd346004d39a1efba46ac7d62aaf3d363378ca7c9e1b61b808c5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bb957d663d1d39f00f13fbc901555000f7b0332e130db9e63ddbbed7d665dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1341d085dcc76845871aa81af959a7788b4aed86125ce330817eee2c71a8ef92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44c5a3148a15daf6a594239e797a7f886e5a93a805dd6d33ed1c0bfed01d2ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02915802665709262323ce978beb957c80d72af0f58b6864ee51e58545fcac28(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f8aac15079b7ac9392331252791ce0d2ea519b145656031761510e435f10cf1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c3d54d2f65363df2dc9af80783095b037ee81f80feba1e48380ac20834c1a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0ce90d61e318cc3eec7044646937dbb8039e154ebc210821ccdb96604a5d03(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319926703ac6061bb489cb76e2182b222bd5ff5ff6d8ef7b6b06988a7513778e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60367dc0631edac129464090fc5e0867c79f85c3f088cc2378c5c3a885d6c6d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bf6e51f32f74b30ee9cc9f0384b6f617158693b54331598af151ba71572e63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3611601d262ec76de13659423e6cfa7bcfe6efb1e78e5695f517403554ba38ef(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c50c4ea79818a708468afe01cf755b7c2bc1f9f8f4c683ad4dcd6683524cfe3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e203e971b5408c83263cae9fd7d806cf359e4efed3c6b322eafc5192a69a6685(
    value: typing.Optional[typing.Union[CfnFunctionConfiguration.AppSyncRuntimeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37c741b235bdea6001262360617848c1c996713ff102a9f49303403a28aae53(
    value: typing.Optional[typing.Union[CfnFunctionConfiguration.SyncConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a875d087cf34ba3d739fbb7ee1a93e2bc4ebb1b9d61f6963c6c580c03008f5a7(
    *,
    name: builtins.str,
    runtime_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e44fc6adb323c7e663210e832622af4d7eeed913ca15af5545606d76e3b5d9(
    *,
    lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690c79dea5db529c5c4cf995a193e552acc73b2f4283cb485bd01fc6d7649090(
    *,
    conflict_detection: builtins.str,
    conflict_handler: typing.Optional[builtins.str] = None,
    lambda_conflict_handler_config: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.LambdaConflictHandlerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84b7f7f1a55363f6363a905619a8929cba00d6f19c9bc0b6779a6e83502a19f(
    *,
    api_id: builtins.str,
    data_source_name: builtins.str,
    name: builtins.str,
    code: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    function_version: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sync_config: typing.Optional[typing.Union[typing.Union[CfnFunctionConfiguration.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35cdd9f83066545a18ab25e130890ddf3953f80b2e1aa8e4726b44a0d4e46bea(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    authentication_type: builtins.str,
    name: builtins.str,
    additional_authentication_providers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGraphQLApi.AdditionalAuthenticationProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    log_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LogConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_id_connect_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.UserPoolConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    xray_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826120bf7d041350b4055c8304d25894e07ccf1b04cf76ab62d30f03cfdecefb(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4bde0439df44816345508bca736a38db0f252296ab146e97372f75c8309fac(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a067b836aa3dde5d3aa6bb7773bf5ebc19a3a20a62332cdb8226e1a0679538ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b313f5ecbd74c90ca73a882dbe07294449e20153d217324ff130970ec391f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68318736d06afb0a9920be900c3d0367e9c22349d281b5fd22c94355a7f248b3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGraphQLApi.AdditionalAuthenticationProviderProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a1fe11bf87f9ffcc658c8eb8912d198f892f1cefef11b5c101f8713602fa76(
    value: typing.Optional[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc15d0778d9ee3f37f51211ffc30e45cdfd1d19736a9dc8ab1441f87c9971718(
    value: typing.Optional[typing.Union[CfnGraphQLApi.LogConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db793e163945b7c43dc2d9c033e3d12e3209e64adbf84ec50cb3c6a25437fb47(
    value: typing.Optional[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425b943bfc67e30cc27dc6fc69e234364124baad69cdf10f22f0b207be11f863(
    value: typing.Optional[typing.Union[CfnGraphQLApi.UserPoolConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ef4ba154d8e6e4c0b121623c03ab1a74409ee2cb124b720ddfbb1ffa32d128(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2747361e42703d14d2893ba0fb94bb920962a49bdf3ff646b2e8bf752bae06c8(
    *,
    authentication_type: builtins.str,
    lambda_authorizer_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_id_connect_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    user_pool_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.CognitoUserPoolConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb54a365c973a25b44f1eb9ea59d5f1e5ddcc0a9ad1a8e6c6ff5a81299c207d(
    *,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43a4eb86ea093ff4548baee0ed3a82e4578b0193fdb2a2719d2346d58801ca6(
    *,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    authorizer_uri: typing.Optional[builtins.str] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f818e71d03b36e227b74c1b69b93f5db0bedc918641237fbdcd5609a92eaf151(
    *,
    cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
    exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    field_log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab933ba3d5962d9d6e491601744175586103ac2a1c6c99ab05cf53d7db5e30a(
    *,
    auth_ttl: typing.Optional[jsii.Number] = None,
    client_id: typing.Optional[builtins.str] = None,
    iat_ttl: typing.Optional[jsii.Number] = None,
    issuer: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2b4691f85a7f106da611dcf4e7b8ffff78be58e10c683e745fe27f3d504fbf(
    *,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    default_action: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118a47425725c6c7fa018eca797893634e7acf5e4ff26c3e7a15ac69848c4623(
    *,
    authentication_type: builtins.str,
    name: builtins.str,
    additional_authentication_providers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGraphQLApi.AdditionalAuthenticationProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    lambda_authorizer_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LambdaAuthorizerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    log_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.LogConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_id_connect_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.OpenIDConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_pool_config: typing.Optional[typing.Union[typing.Union[CfnGraphQLApi.UserPoolConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    xray_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fbc49a572f33a0ec287cc8f222b767678f6f6d7d81cd1d63eac0ba9deca3b4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_id: builtins.str,
    definition: typing.Optional[builtins.str] = None,
    definition_s3_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fcd85176b2a5d4253cda0d71e0decf878989fcbe28ff099fe52d89794d952f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dafbc3c1ea7a58255af9ca0491e2bc848110fe46bd54ac9d1914ffb512047f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febc08037f81d08fc7c3271b8385b28dbc558dc15a9b74f584dd55dd8867555b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e24611a7cec5ed686a0fba4b722b26580ce4c0f6c6be962f3b63137060bdad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae574e2d8cbfc39fac65e1c0227be155e1808c9be0fb3a213d0520fe28ecf83(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1252139e4225ccd4d89a46bbcbb78e7056c85320a8e69df27f5edc6cf532af2(
    *,
    api_id: builtins.str,
    definition: typing.Optional[builtins.str] = None,
    definition_s3_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34883bfb7f0120bb0d5af960f9a86cf636e9b818fa745495955c56359acad5a5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    api_id: builtins.str,
    field_name: builtins.str,
    type_name: builtins.str,
    caching_config: typing.Optional[typing.Union[typing.Union[CfnResolver.CachingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    code: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    pipeline_config: typing.Optional[typing.Union[typing.Union[CfnResolver.PipelineConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[typing.Union[CfnResolver.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sync_config: typing.Optional[typing.Union[typing.Union[CfnResolver.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c710480b97d448ed2b38cdd3b1f0871a5aa06435c05483beb296689896e18940(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f38295af893748bb923d7e848a7859e52805f74b244b9c41287834f096bd715(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791cf4a43a1e44e1b75cbf3c451962710226ca70b6d5b08520a28eaf0134e4a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ea86227c8edf0b5470f4331335f5453f5264c78ad6414340b36781b84f9c71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff914f07b69b86703d1584f88f96c8313a81867391278a9b2b65f72c8a1e29cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44f0e8636b4db59d594d84c01eb1d917d11f4635534b53abc7139638075c0ba(
    value: typing.Optional[typing.Union[CfnResolver.CachingConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba238d284bacfd51ef130771d76490815e79c9ed8057d7e7a16f4bdf6e14f1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69d89718ecbadb2d8353e3b3709cffd0f705835b1c0ade46945924a921eddc5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03367193f799a1a52141c9666b4bdaa75d98f06abe7be9c4fb98785a926a78d0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08edb19afb6f0c022ee3b57657785d74a0d82412e17c1d5deb9c62ac8207ddc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57316ff5e303e81df19142b4e37da5d3c01e7d624f84a850c0c220e2026a6b1e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cc0ca3319d9c34dcd4eb08475f73ed73c6a3bc35920c82a0feb00cfe3d039a(
    value: typing.Optional[typing.Union[CfnResolver.PipelineConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8132e260af6f20ed9ae1c3aa09202daf25ea3a81474c03dadf71b3a17b867b0e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db6a5702988374594f917d7a5bb17ab6041e84750e78f5ddf4426c0350f4e85(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fad24b55f173ceb2af4617f8e23f57fcfa3d9d8b31546b9585abf836ad75e67(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcfc5b8755719e2fad9b19fef35ca73938cb6d70ce95495be2deedaa6442cb4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e092e546a7dd65912c5e6f79c561886b0c0721c1dd87de45894ee68e73ae640(
    value: typing.Optional[typing.Union[CfnResolver.AppSyncRuntimeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a81ae3cdbcea9dc095123c0ebd20c3df7dd01ff2791b0bd239fcf580d898bc(
    value: typing.Optional[typing.Union[CfnResolver.SyncConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54559dfeaa08bacc61e5fdc1f1d74730e7fd31f6c091a3b1357b8ef5418a3b9(
    *,
    name: builtins.str,
    runtime_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdca5b7bc5b314edaca5250353503ca5256d902a79fba3f85e74283bcb16e223(
    *,
    ttl: jsii.Number,
    caching_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330290c3d36654285b554cdf4cb3be0e3300ec57ece1e2ace69b5b59a7517738(
    *,
    lambda_conflict_handler_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79362fd469794e6596313597ab8e4a291d2dddf9a81b1e882c44e9bbaf1253bd(
    *,
    functions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c1b8054b7e9962c4d63617b26af2796e76db8476ff424bef0e46ba4c24c255(
    *,
    conflict_detection: builtins.str,
    conflict_handler: typing.Optional[builtins.str] = None,
    lambda_conflict_handler_config: typing.Optional[typing.Union[typing.Union[CfnResolver.LambdaConflictHandlerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4ced33d747cc766f0f9ad98e6d46cb4cf1d9d2b3d3f6df2510542f97ff6f7b(
    *,
    api_id: builtins.str,
    field_name: builtins.str,
    type_name: builtins.str,
    caching_config: typing.Optional[typing.Union[typing.Union[CfnResolver.CachingConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    code: typing.Optional[builtins.str] = None,
    code_s3_location: typing.Optional[builtins.str] = None,
    data_source_name: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    max_batch_size: typing.Optional[jsii.Number] = None,
    pipeline_config: typing.Optional[typing.Union[typing.Union[CfnResolver.PipelineConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    request_mapping_template: typing.Optional[builtins.str] = None,
    request_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    response_mapping_template: typing.Optional[builtins.str] = None,
    response_mapping_template_s3_location: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[typing.Union[typing.Union[CfnResolver.AppSyncRuntimeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sync_config: typing.Optional[typing.Union[typing.Union[CfnResolver.SyncConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9892dac165c1272701c637c8e62590681d37f17384047fecdad4f07f602adb(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4be52408fddbab98926376259cafdceaea556086e9a4c1ab88eaf9ec60dfab8(
    *groups: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56ae66cd66ef66cdd0423e92601632209454b6f1fa3bc05e28bf7da1c8ccde5(
    statement: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823b1bc735e936ae5d5483a1a44ec24f6bbb5d723075451b78190757888ed1ac(
    *mutations: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbdf73f1105c55f67f62a27be6a13dd2d39ad2d0fa8040276e3cff33c6dd5c2(
    value: typing.Optional[typing.List[AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34addc08275c25f75760c0971b40e94f68344d17a1523bc6047bc32d8cca48c7(
    *,
    certificate: _ICertificate_c7bbdc16,
    domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d086f0499f4f7ca70a13b9fd88c7674d643c2031d7257458cfae84a3bece9bef(
    *,
    definition: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e431f01e6bb0d5cf5b60971f759568ca1a6ce96bf590b6d505f1a34397ac3074(
    *,
    type: builtins.str,
    dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981882565e0c540777bba530f3f7716a431fc981bf4a32df207ec3258ba0d0cb(
    *,
    field_name: builtins.str,
    type_name: builtins.str,
    caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
    data_source: typing.Optional[BaseDataSource] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e857771cf3c9a89258fbc8a976608ad4380bafec6b66b6175f06a22860a1f2e1(
    *,
    return_type: GraphqlType,
    args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816b596f025d22de0b0f651c4c270bfb954f4e8c9ffb534ab26606125c2d0752(
    *,
    graphql_api_id: builtins.str,
    graphql_api_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20507e110e7b81011acf88cd122a8d6e58160562a62e8e22f556da92e08362e9(
    *,
    name: builtins.str,
    authorization_config: typing.Optional[typing.Union[AuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_name: typing.Optional[typing.Union[DomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[LogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schema: typing.Optional[Schema] = None,
    xray_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701e3115cb1eb511424e158a875e766bdab9673a959457c7420bb599926af4ab(
    *,
    is_list: typing.Optional[builtins.bool] = None,
    is_required: typing.Optional[builtins.bool] = None,
    is_required_list: typing.Optional[builtins.bool] = None,
    intermediate_type: typing.Optional[IIntermediateType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfae6856ffbe054657ab7dce6de39e2bf9c6dfe1d7cdf5183f940bb24fe8aa2(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62602e83f3466a3b88682c8a5a3ff41732db29288e6f16af5ed9685f28316b9(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    endpoint: builtins.str,
    authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4934a4b71ec4a71977f19728b4b65fb79dc0c82a3d8436d792b2c1c0b16f959(
    modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f04a5729f355f43a37a6a1de40270eff41c8929a9dc3cc1c2b929d8df77f7c8(
    id: builtins.str,
    table: _ITable_24826f7e,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376265306270b4bd89ba850586e025a47b1cc869ef4d1456920ecdf261d57161(
    id: builtins.str,
    domain: _IDomain_0b3cf46c,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d355777072365de58f9930b93f5a10964d43359369e89e08bfc08658892cd86(
    id: builtins.str,
    endpoint: builtins.str,
    *,
    authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f195ade1cf17298e2fe9d90de9f774eb79846a6d570516373a1e6b4ba74cab9a(
    id: builtins.str,
    lambda_function: _IFunction_6e14f09e,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308ac633c9c93010f488643569b0688c5a76010adf9ef3bf3dee8b5cd1fd6c82(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c75924bb0041864c4bbda81e26827c24ff3bc199f8b47d75c64b2fd45b765f(
    id: builtins.str,
    domain: _IDomain_cb64a2bc,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c8173aa170f8963a191c22f32ccbac44d8b0ec39fae35ee8f83c57b9599bfe(
    id: builtins.str,
    serverless_cluster: _IServerlessCluster_8ed6177c,
    secret_store: _ISecret_22fb8757,
    database_name: typing.Optional[builtins.str] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2687ccca0fa0bcbad3055906a1bd9811372f5a26ef5a27963b0be21dd64deb9(
    construct: _CfnResource_e0a482dc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3432386f03c08b8afc830abb4c9a6ce21f44edc4ced377343039a5e94fd73462(
    value: typing.Optional[typing.List[Resolver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a8f17ec4952d80ceb86207a672c14b862c1d8faafc1789e6039506874c80f2(
    *arns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2ddb611db428996ff81398192b106b8eda2251c59dda583f9d2e72e2d381d7(
    type: builtins.str,
    *fields: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ddca3ffeb86ffe7427c1a862c35f0d5ae3e8a15240a980f934788efef4fa08(
    api: GraphqlApi,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b26ec10de4cd7e5cfef24016f1a83e61f13232d3d7abc409fe4241b49206fc1(
    name: builtins.str,
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e18d54182aaa6e7ebd7fa26d6228ea0486062d1e7502ce7093e6fe4f89c3df(
    value: typing.Optional[typing.List[AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b786998ae5818ce1bc065897dd2f2725116d0ca65ff1d3888acddbfb36fb3a7(
    name: builtins.str,
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc927def3f2a9aa5090003038edd46978296c87a8f19e2395e9ea4c8d7601d1e(
    value: typing.Optional[typing.List[AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c592cedeb6bfe21a9bbaa3e69e2d784f31e2e104c2e9fb135d8bb5a56246304(
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e161f9b06571781d54c584f77fe13eaa5463f878d7e3696704f55ea9ae3247(
    key_name: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6b59cdc92d0e944cd7e1b185a854eee378a88d1f52b0050747fa05c2aa6c8c(
    key_name: builtins.str,
    arg1: builtins.str,
    arg2: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f917597f8680eac283b1ba41e4a89381a0eef9226b42dc2a8eb59951202b305c(
    key_name: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec86c17f25ce3981932ea0780da060c015dca3849ed709bfd32f870b1a89ec92(
    key_name: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91de02843753c4cbfde7ce36b769a4ef46e30412155673b36794f2be8e18fa2(
    key_name: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44911ced99be783e4a0fa97170f79389bd1e0acb9395631018e2963a7815f1cf(
    key_name: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3936723f500d9dfec5e9de47782edc973e57caae43311039ca60996651bee67c(
    key_name: builtins.str,
    arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b9608d3b9cb312aafc8faeb451080a81dcc26740032a66fcbea64083b09f3c(
    key_cond: KeyCondition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974fe82cae103adcc26ee99703edf9af3fe6fddd44f6e57a4ec948e1adfc024a(
    *,
    handler: _IFunction_6e14f09e,
    results_cache_ttl: typing.Optional[_Duration_070aa057] = None,
    validation_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f074fb7f71902b2affa7bb5d0a63d9ee8071454fcb6e93fa6e1a085ff2dd2a6(
    *,
    exclude_verbose_content: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    field_log_level: typing.Optional[FieldLogLevel] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ca926fbcf331634a5987d4644d0758f6a80aa28649814d37e3e41bf5afebf4(
    key_name: builtins.str,
    id_arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae7bec2d029c104dc28f5eb887fa76d5a0429d5187e945213f4448fab0954bd(
    key_name: builtins.str,
    id_arg: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce90d3745c168f40afe25efcd346fe9e4d96c41a05ca71089092113d5fc9326(
    key: PrimaryKey,
    values: AttributeValues,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617378a786cd042023325498eb31b8ac9c806db13e0bc7fb1958c1e8e0f3ef65(
    cond: KeyCondition,
    index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd639a8aab4ad9e256a3ae573949c7538243e97826d5693b5e00a6dd9da8c8f(
    file_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae7a67a8ce4c0d526cb63b840375e161e0da0168a9913bc63bd536570f19809(
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93459584318a2776fc2c8bb8bd016ff93be645d355cbbde4a01a754805b835f1(
    payload: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25cfb81c8754825df5b162fc72cdc14873a2d6e38c9cd871ac50a43549d986e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329b16bb6252d611c55a19c99ee14089bef1956b2207d46021005706183884a4(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b67b2a9d13cc50545efc00ab34afd3e482c7f388b456bac8c017953ec5676c0(
    name: builtins.str,
    *,
    interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aa1cb3cdaace7fc071497c20fed99795c9f2b8d8add176bfe738090343957c5(
    api: IGraphqlApi,
    field_name: builtins.str,
    *,
    data_source: typing.Optional[BaseDataSource] = None,
    pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
    return_type: GraphqlType,
    args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
    directives: typing.Optional[typing.Sequence[Directive]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c96c633c381e429818356aae1fdd81a43c68caa2cdef350b61cd86efcca11f4(
    value: typing.Optional[typing.List[Resolver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31100a5405ae7b82a872bafa8bb148d108e97e4b7493094cf4d06cf42d7444cf(
    *,
    definition: typing.Mapping[builtins.str, IField],
    directives: typing.Optional[typing.Sequence[Directive]] = None,
    interface_types: typing.Optional[typing.Sequence[InterfaceType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624bd61e820e2ed8c903686757a87e6d3ceee30b30041aaeb891ae16b38bb652(
    *,
    oidc_provider: builtins.str,
    client_id: typing.Optional[builtins.str] = None,
    token_expiry_from_auth: typing.Optional[jsii.Number] = None,
    token_expiry_from_issue: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef294cc43d1763f915b0d0120361eac33914d0f443839088669907b55defebe(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905a065a9ec478178b39085705c2d59e6f4c697ed9c7bbf222d8e45a730114e3(
    val: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1e45226ff94c0c0532ac7f20a48b28e86d3cc3f5b2d51f7cc2f9bac1a58e08(
    pkey: Assign,
    skey: typing.Optional[Assign] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b91382f0d8f9886cf86663f33804f713f1ac027ab0de409e3c90e14494deea1(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d77cea2af350044d4a43bb857c5dde1dfe29f5d35d875430a1493c8de8b17bb(
    *,
    return_type: GraphqlType,
    args: typing.Optional[typing.Mapping[builtins.str, GraphqlType]] = None,
    directives: typing.Optional[typing.Sequence[Directive]] = None,
    data_source: typing.Optional[BaseDataSource] = None,
    pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca83da8f023ec0d1dee3fa647ec37e13b837af62d9a8911ef1536824c86d173c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api: IGraphqlApi,
    data_source: typing.Optional[BaseDataSource] = None,
    field_name: builtins.str,
    type_name: builtins.str,
    caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd65b819d42170f1710a882b49608ad30e4689782c53b7c39cb1c7887c8c6f7(
    *,
    field_name: builtins.str,
    type_name: builtins.str,
    caching_config: typing.Optional[typing.Union[CachingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    pipeline_config: typing.Optional[typing.Sequence[IAppsyncFunction]] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
    data_source: typing.Optional[BaseDataSource] = None,
    api: IGraphqlApi,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480127c095c8643e78cf57067aab3071a7fa32b69d5e548923132e05f42f70a8(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129ae640f9ef4c5c646545ad0df397839b88409e447f5fbade97caab3f3ab6a6(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f7d285fbf0eee9eeb38af45b40c375be60ce1cd35b9e4b144a2529053f1c1a(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7c79bd153eabe99ffc7f87c61e199e056ee26f800e47e91a73c9441b56c8d6(
    field_name: builtins.str,
    field: Field,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f3a957f77841b8b0c3a793ec1e0ad6338eba41852b3385a00c704d2928312b(
    addition: builtins.str,
    delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00955f29f0f15679f90494894a7f805867675a74df40ba5cdb33b5f3902d1884(
    type: IIntermediateType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43164c78a1ac78f9dea87d60214fc7f2f35bbe7f24f499ef895d77bb16f2fc2f(
    api: GraphqlApi,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c43bca490806cc0da50acec1d31cf487c236b454b0a1b7d269ff87192772ec3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ba094010a357b67bb0abe2b2b75fe859d9df8c521f713bd91ce338f2fb597a(
    *,
    file_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edcb6bf19a7bf3b07bef2380491c97dd0d5c2414f1d61e0e6c7f02ea4f77d51(
    pkey: Assign,
    skey: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef693a5898b9a8dad179b4b176ec06f5f16a790fae16b6f934fda52117a23815(
    val: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318d1f80d1c432cb4ded544e30ac1be9021a2ead178eea2286ccef8d01672283(
    name: builtins.str,
    *,
    definition: typing.Sequence[IIntermediateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87ebd02a8637e1358bf47bdb795d843037c568a9be37aed18d1f523006dc3ea(
    value: typing.Optional[typing.List[AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba4279b311e3ec6581d01adea11fae7796457a41fa2024e04ade495b2b519a8(
    *,
    definition: typing.Sequence[IIntermediateType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbb91e242bcc7da75d6e393d4b01cd1c5a0b178b397d523996fa6fb348a7a2a(
    *,
    user_pool: _IUserPool_5e500460,
    app_id_client_regex: typing.Optional[builtins.str] = None,
    default_action: typing.Optional[UserPoolDefaultAction] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2c3c824876eb01b9c6233d28ac499c3a1b54d5fa305d2a1cf37d46a379773a(
    attr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20aec3c65f45f7eb0fad9d10659ad55b87594ecafc7bb065670e110e3db214e(
    arg: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0132a977cda482b0bf447be6458ae6613dda0dfaea20dab8d1b80a49742c61ed(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api: IGraphqlApi,
    data_source: BaseDataSource,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8260122f7cb4ab9f59ecf9c41581fca64cb3c29e2fc75d89849089f8cfd903f9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319c0c1370b60552cd73d184ffbe51fad87559f39457ea1dcc565f459a9c8d1c(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    request_mapping_template: typing.Optional[MappingTemplate] = None,
    response_mapping_template: typing.Optional[MappingTemplate] = None,
    api: IGraphqlApi,
    data_source: BaseDataSource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcaf1872b474204ef3c4d442476523d26c7337f4a647e8a92b8da85e15929235(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[BackedDataSourceProps, typing.Dict[builtins.str, typing.Any]],
    *,
    type: builtins.str,
    dynamo_db_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.DynamoDBConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    elasticsearch_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.ElasticsearchConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    http_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.HttpConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    lambda_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.LambdaConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    open_search_service_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.OpenSearchServiceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relational_database_config: typing.Optional[typing.Union[typing.Union[CfnDataSource.RelationalDatabaseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f1e182121e07ee604d42fc7dfb0df184d10169a2edbc979904ace9584a3699(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6e311489aad534662dae365cda4a9c10457ecb27996d04aecb62f5c818eb87(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table: _ITable_24826f7e,
    read_only_access: typing.Optional[builtins.bool] = None,
    use_caller_credentials: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25370a06169ecdd34cefba9ccd71c256ea23190c140b6cd23efd55eb214bac36(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    table: _ITable_24826f7e,
    read_only_access: typing.Optional[builtins.bool] = None,
    use_caller_credentials: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b724a05ca00ad168ea72dd6d7746274e35ad1d8f97860bb8abe9224634c2120c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: _IDomain_0b3cf46c,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a139e90767ea8c5015925561ec1041c3438db9fab35752d2071d2481fbd1113(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    domain: _IDomain_0b3cf46c,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f35ba5d19bd6d93ee86b1bddec8015a740243fbcc7bec0f57ac77a48c991d94(
    name: builtins.str,
    *,
    definition: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba17d33823e2a842edbb291e18fc3b7cacbcb3d246e6d70baca206301fb3f89(
    value: typing.Optional[typing.List[AuthorizationType]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2bbf15615501f62510ef6a13d244cbe1e440dafc6cdce46aaca07681fe2fa1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe51ccbdc5dc70c7017a42aaafb3ce07d877f02da81992906e1459f5c84cc129(
    id: builtins.str,
    table: _ITable_24826f7e,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c375438ba40791f610d4409fb20b7165ea6da87ab9fcb17fc117b5649dad6f9(
    id: builtins.str,
    domain: _IDomain_0b3cf46c,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0476506c45c0541e8b87633c59fd6d43d2cc9e780fb42e927041e51cbbe55cab(
    id: builtins.str,
    endpoint: builtins.str,
    *,
    authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114c4b0033e11dc87be73938252f58d518d13b1a74e2266e3d955d6bb726832a(
    id: builtins.str,
    lambda_function: _IFunction_6e14f09e,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e93f2a0cff6e8a7d1072c7f2767b9b41f6c6d3f0e97d80844fd4acc40e4a868(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b17af62f1f2838c00862311172ef9e73cb2045e8fb2cceb0fc986e9016cd492(
    id: builtins.str,
    domain: _IDomain_cb64a2bc,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73af86ef894062e776b9f84461020e34c60b6ccea0023ec609b40e62d3d369fd(
    id: builtins.str,
    serverless_cluster: _IServerlessCluster_8ed6177c,
    secret_store: _ISecret_22fb8757,
    database_name: typing.Optional[builtins.str] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2f4e4d0307cd929f0181a945cfd3fea09a09af6e7f0522bf2cd4277f03c446(
    construct: _CfnResource_e0a482dc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c963e166295c6604e8c6342b6a209bb490a754134a33ef0acd2dcb457fcec62(
    type: Type,
    *,
    intermediate_type: typing.Optional[IIntermediateType] = None,
    is_list: typing.Optional[builtins.bool] = None,
    is_required: typing.Optional[builtins.bool] = None,
    is_required_list: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138312be10672193c1a27fd2b8040e40c9dad08342dea1943777780c3e6bd122(
    _modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3188bbce17e95a84da8dad16eb7ed6e76729e1f503b76ceb206a7c41e10980a8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    endpoint: builtins.str,
    authorization_config: typing.Optional[typing.Union[AwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099bce405bfdff64228535c6b3e6b958204d1be052564214ac6b9676af228c91(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_function: _IFunction_6e14f09e,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fe10ae30483b3e4de861468f1cba36a67ef2aa217c2e4b9f230947c576e720(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    lambda_function: _IFunction_6e14f09e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400e5c966b25eb714c886bdbbc343c6873ce55fdb153182bc1f5f0a20704f33b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: _IDomain_cb64a2bc,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235ea9c69820965cf8d2b746e06d922051093030a19b53b615e7951ef7098018(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    domain: _IDomain_cb64a2bc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea7948fb50b16bbf86624fa544289da83cf883ae81ef0bd87108d8b904c9920(
    pkey: Assign,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a37e32f75471d8873e51226c4a9bdb92fb360d52c166e7d6e9f2b1861dcfc5(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5daf762ee6b6669f84ef3c64a11cd79b7cb918997de9afc87313d25401dfad1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret_store: _ISecret_22fb8757,
    serverless_cluster: _IServerlessCluster_8ed6177c,
    database_name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe8036fa2733542ce4aa4a5fcfdb1421dd399232880fb8b8c46f04c88644dab8(
    *,
    api: IGraphqlApi,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_role: typing.Optional[_IRole_59af6f50] = None,
    secret_store: _ISecret_22fb8757,
    serverless_cluster: _IServerlessCluster_8ed6177c,
    database_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706d4a76118b94d0ac93ff4e2a733e24f5dcdea51135ec7af0dc8895ef474832(
    modes: typing.Optional[typing.Sequence[AuthorizationType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02467b263fa8045081e369d3dd29eaffb8ed797f2227eb1239bded3808ea231f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    authorization_config: typing.Optional[typing.Union[AuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_name: typing.Optional[typing.Union[DomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_config: typing.Optional[typing.Union[LogConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    schema: typing.Optional[Schema] = None,
    xray_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8a2899bd0c3f594aa11e730dcff682d399e51a71cc67dbdcf509ad19a4895b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    graphql_api_id: builtins.str,
    graphql_api_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374a3832ffaa074ab09e44de8c556e31825a1d7ab1178981ec9bd7a9bbd67fbf(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e2b829939b83dea1e9e306d13790d4807908c3bd71d34969d38a90d435c908(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a365e5fa722a5756f18e864d6f48ec381cb73faf41fdcc8b7208ab8d345d6(
    construct: _CfnResource_e0a482dc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11a1c229f043bc04bb5add59a599fb51bd4e9990cebaee2e96b1ab60e9683c8(
    field_name: builtins.str,
    field: ResolvableField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd9763935faa03e372410bad7ed1860277685c20933aada8d2fc89e396018eb(
    addition: builtins.str,
    delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487400b6ccbc63d5499625a6fa811c9d14a2434152fa85e4da7488aea0ca69d3(
    type: IIntermediateType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca7e5ff46e26d07b70ef651962185b9a2e8368396c84d68b664249b484ddf1e(
    grantee: _IGrantable_4c5a91d1,
    resources: IamResource,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e945a58acadde5aa7f3db6765954214f006b32b6c347fd2e12d9567466bf557e(
    grantee: _IGrantable_4c5a91d1,
    *fields: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3263ab8384c549a37797e8e47f26c6dbd46f4c33ca432e04fb06eccf0e1ee52(
    grantee: _IGrantable_4c5a91d1,
    *fields: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db571759598abff5ff3d04c645bb9c57152679c9232e185e1c6b0535f4f33098(
    grantee: _IGrantable_4c5a91d1,
    *fields: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
