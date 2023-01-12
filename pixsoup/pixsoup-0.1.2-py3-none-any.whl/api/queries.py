from gql import gql

# region GraphQL - queries
# =====================================================

f_dataset = """
  fragment DatasetFields on Dataset {
    id
    name
    createdAt
    sealedAt
  }
"""

f_job = """
  fragment JobFields on Job {
    id
    name
    state
    args
    createdAt
    startedAt
    finishedAt
  }
"""

q_account = gql("""
  query {
    viewer {
      email
      tokens
      verifiedEmail
      jobCallbackUri
    }
  }
""")

q_list_jobs = gql("""
  query {
    viewer {
      jobs {
        edges {
          node {
            ...JobFields
          }
        }
      }
    }
  }
""" + f_job)

q_job = gql("""
  query Job($id: ID!) {
    viewer {
      job(id: $id) {
        ...JobFields
        downloadLink
      }
    }
  }
""" + f_job)

q_list_datasets = gql("""
  query {
    viewer {
      datasets {
        edges {
          node {
          ...DatasetFields
          }
        }
      }
    }
  }
""" + f_dataset)

q_dataset_detail = gql("""
  query Dataset($id: ID!) {
    viewer {
      dataset(id: $id) {
        ...DatasetFields
        resources {
          id
          name
        }
      }
    }
  }
""" + f_dataset)

# endregion =====================================================

# region GraphQL - mutations
# =====================================================

m_create_dataset = gql("""
  mutation CreateDataset($input: CreateDatasetInput!) {
    createDataset(input: $input) {
      dataset {
        id
      }
    }
  }
""")

m_delete_dataset = gql("""
  mutation DeleteDataset($input: DeleteDatasetInput!) {
    deleteDataset(input: $input) {
      success
    }
  }
""")

m_seal_dataset = gql("""
  mutation SealDataset($input: SealDatasetInput!) {
    sealDataset(input: $input) {
      success
    }
  }
""")

m_create_resource = gql("""
  mutation CreateResource($input: CreateResourceInput!) {
    createResource(input: $input) {
      uploadUri
    }
  }
""")

m_delete_resource = gql("""
  mutation DeleteResource($input: DeleteResourceInput!) {
    deleteResource(input: $input) {
      success
    }
  }
""")

m_delete_job = gql("""
  mutation DeleteJob($input: DeleteJobInput!) {
    deleteJob(input: $input) {
      success
    }
  }
""")

m_run_dreambooth_job = gql("""
  mutation RunDreambooth($input: RunDreamboothJobInput!) {
    runDreamboothJob(input: $input) {
      job {
        id
        state
      }
    }
  }
""")

# endregion =====================================================
