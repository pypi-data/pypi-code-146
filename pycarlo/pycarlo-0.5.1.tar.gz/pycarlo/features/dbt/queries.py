IMPORT_DBT_MANIFEST = """
mutation importDbtManifest($dbtSchemaVersion: String!, $manifestNodesJson: String!, $projectName: String, $defaultResource: String) {
  importDbtManifest(
    dbtSchemaVersion: $dbtSchemaVersion,
    manifestNodesJson: $manifestNodesJson,
    projectName: $projectName,
    defaultResource: $defaultResource
  ) {
    response {
      nodeIdsImported
    }
  }
}
"""

UPLOAD_DBT_MANIFEST = """
mutation uploadDbtManifest($invocationId: String!, $batch: Int, $dbtSchemaVersion: String!, $manifestNodesJson: String!, $projectName: String, $defaultResource: String) {
  uploadDbtManifest(
    invocationId: $invocationId,
    batch: $batch,
    dbtSchemaVersion: $dbtSchemaVersion,
    manifestNodesJson: $manifestNodesJson,
    projectName: $projectName,
    defaultResource: $defaultResource
  ) {
    ok
  }
}
"""

IMPORT_DBT_RUN_RESULTS = """
mutation importDbtRunResults($dbtSchemaVersion: String!, $runResultsJson: String!, $projectName: String, $runId: String, $runLogs: String) {
  importDbtRunResults(
    dbtSchemaVersion: $dbtSchemaVersion,
    runResultsJson: $runResultsJson,
    projectName: $projectName,
    runId: $runId,
    runLogs: $runLogs
  ) {
    response {
      numResultsImported
    }
  }
}
"""

UPLOAD_DBT_RUN_RESULTS = """
mutation uploadDbtRunResults(
  $dbtSchemaVersion: String!,
  $runResultsJson: String!,
  $invocationId: String!,
  $projectName: String,
  $runId: String,
  $runLogs: String
) {
  uploadDbtRunResults(
    dbtSchemaVersion: $dbtSchemaVersion,
    runResultsJson: $runResultsJson,
    invocationId: $invocationId,
    projectName: $projectName,
    runId: $runId,
    runLogs: $runLogs
  ) {
    ok
  }
}
"""

GET_DBT_UPLOAD_URL = """
query getDbtUploadUrl(
  $projectName: String!, 
  $invocationId: String!, 
  $fileName: String!) {
  getDbtUploadUrl(
    projectName: $projectName, 
    invocationId: $invocationId, 
    fileName: $fileName
  )
}
"""

SEND_DBT_ARTIFACTS_EVENT = """
mutation sendDbtArtifactsEvent(
  $projectName: String!,
  $jobName: String!,
  $invocationId: UUID!,
  $artifacts: DbtArtifactsInput!,
  $resourceId: UUID) {
  sendDbtArtifactsEvent(
    projectName: $projectName,
    jobName: $jobName,
    invocationId: $invocationId,
    artifacts: $artifacts,
    resourceId: $resourceId
  ) {
    ok
  }
}
"""
