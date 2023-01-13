from tensorcraft_py import tf_dataclasses as data

import json

def test_filter_example1():
  actual = data.FilterExample.from_dict({
      "example_group": "testex",
      "filter_id": "testid",
      "strength": 0.5,
      "image_data": {
          "uri": "testuri",
           "size": {"width": 512,
          "height": 512},
          "id": "testimageid"
      },
      
      },infer_missing=True)
  expected = data.FilterExample(
      example_group="testex",
      filter_id="testid",
      strength=0.5,
      image_data=data.ImageData(
          uri="testuri",
           size=data.ImageSize(width= 512,
          height=512),
          id="testimageid"
      ),
  )
  assert actual == expected


def test_filter_example2():
  actual = data.FilterExample.from_dict({
      "filter_id": "testid",
      "strength": 0.5,
      "image_data": {
          "uri": "testuri",
           "size": {"width": 512,
          "height": 512},
          "id": "testimageid"
      },
       "source_image_data": {
          "uri": "testuri22",
           "size": {"width": 51222,
          "height": 51222},
          "id": "testimageid22"
      },
      "tags": ["face", "smile"]
      },infer_missing=True)
  expected = data.FilterExample(
      filter_id="testid",
      strength=0.5,
      image_data=data.ImageData(
          uri="testuri",
           size=data.ImageSize(width= 512,
          height=512),
          id="testimageid"
      ),
      source_image_data=data.ImageData(
          uri="testuri22",
           size=data.ImageSize(width= 51222,
          height=51222),
          id="testimageid22"
      ),
      tags=["face", "smile"]
  )
  assert actual == expected



# def test_filter_3():
#   json_str = '[{"id":"2278601d-1bf9-40fd-95c5-ea9bbc82761a","name":"Anime 1","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"examples":[{"filter_id":"2278601d-1bf9-40fd-95c5-ea9bbc82761a","strength":1.0,"image_data":{"id":"c46c71b6fd1f410188f6a8b7568330fe","prompt":"Anime visual,  by yoh yoshinari, katsura masakazu, dramatic lighting, dynamic pose, dynamic perspective, strong silhouette, ilya kuvshinov, anime cels, 1 8 mm lens, fstop of 8, rounded eyes, moody, detailed facial features","seed":57567,"size":{"width":512,"height":512},"source_image_id":"c852ed7c-3e71-4953-83ee-c5f4af7f9d50.png","job_id":"1cf11bea-85fc-4d6b-9e2e-29f1b5a80553","uri":"https://storage.googleapis.com/tensorcraft1/1cf11bea-85fc-4d6b-9e2e-29f1b5a80553/c46c71b6fd1f410188f6a8b7568330fe.png","creation_time":"2022-12-28T09:54:48.599723Z"},"tags":["male","teen","face"]}],"creation_time":1672250103},{"id":"a734d5ed-b25a-40e8-a4b4-2700071b4a2f","name":"Anime 2","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"examples":[{"filter_id":"a734d5ed-b25a-40e8-a4b4-2700071b4a2f","strength":1.0,"image_data":{"id":"057ca7ba931d403a8e23d65d2302b716","prompt":"anime fantasy illustration by tomoyuki yamasaki, kyoto studio, madhouse, ufotable, trending on artstation","seed":899472,"size":{"width":512,"height":512},"source_image_id":"c852ed7c-3e71-4953-83ee-c5f4af7f9d50.png","job_id":"c0ce21b2-fb8e-493e-9242-c32abcba6b3c","uri":"https://storage.googleapis.com/tensorcraft1/c0ce21b2-fb8e-493e-9242-c32abcba6b3c/057ca7ba931d403a8e23d65d2302b716.png","creation_time":"2022-12-28T17:54:50.841959Z"},"tags":["male","teen","face"]}],"creation_time":1672250103},{"id":"a1eb7ab0-c1ec-47f5-91d7-664aca659d23","name":"Cartoony","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"examples":[{"filter_id":"a1eb7ab0-c1ec-47f5-91d7-664aca659d23","strength":1.0,"image_data":{"id":"8dadd84bef4f4022ace3fb10d1379f6d","prompt":"scene from pixar's new movie","seed":74920,"size":{"width":512,"height":512},"source_image_id":"c852ed7c-3e71-4953-83ee-c5f4af7f9d50.png","job_id":"95aa2dc9-c23c-4b98-83bf-eb441c046d49","uri":"https://storage.googleapis.com/tensorcraft1/95aa2dc9-c23c-4b98-83bf-eb441c046d49/8dadd84bef4f4022ace3fb10d1379f6d.png","creation_time":"2022-12-28T09:54:52.119625Z"},"tags":["male","teen","face"]}],"creation_time":1672250103},{"id":"edfd024f-2a10-4115-8d9c-be3fa74a23f9","name":"Cyborg","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"examples":[{"filter_id":"edfd024f-2a10-4115-8d9c-be3fa74a23f9","strength":1.0,"image_data":{"id":"3596d5a90a684aeea93e44a6c28347de","prompt":"cyborg, battle-damaged, scarred, attractive face,  heterochromia, messy hair, symmetrical features, medical background, sci-fi, bio-mechanical, wires, cables, gadgets, digital art, detailed, anime, artist katsuhiro otomo. multi-racial.","seed":605247,"size":{"width":512,"height":512},"source_image_id":"c852ed7c-3e71-4953-83ee-c5f4af7f9d50.png","job_id":"92f593e1-b26e-43b1-bcb4-88b792345f8e","uri":"https://storage.googleapis.com/tensorcraft1/92f593e1-b26e-43b1-bcb4-88b792345f8e/3596d5a90a684aeea93e44a6c28347de.png","creation_time":"2022-12-28T17:54:55.564442Z"},"tags":["male","teen","face"]}],"creation_time":1672250103},{"id":"1fe016d5-58db-4d67-b674-eb7e15e64961","name":"Dali","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"64b9c7de-8506-4ce8-9929-9a55aed6052f","name":"Dreamy and Ethereal","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"bacc89b0-a7f3-437e-be7f-367ccedaf136","name":"Frankenstein","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"efdab39c-ca3c-4112-9673-87e82b585727","name":"Froggy","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"f28160f9-cb7c-4a2e-aa1e-dd2ef021c6da","name":"Furry","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"a1957789-9ffd-4893-bbfc-259be4bac17f","name":"Tribal","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"73c87668-9ee4-40e5-bdde-558d279cb3f8","name":"Werewolf","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"c745a047-6ad4-4d2a-9cb7-6e1185ab0f47","name":"Wooden Doll","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":false,"creation_time":1672250103},{"id":"b496e7f2-cc84-4bd3-aa61-a81f6f92d86d","name":"Ancient Egypt","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"b6a08fc2-a43a-4f0f-88fc-a3d710a675a4","name":"Anime Fantasy ","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"750be407-3c7d-4898-baad-ef3755504bbc","name":"Alien Bio-organism","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"131a94c5-6036-4c70-b4c8-8a4c00bedb5d","name":"Aztec","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"5022438f-b3ae-4bc9-bb97-f60b69e74ee1","name":"Burners","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"1f999fb8-84c3-4d8e-864b-c1f547bf5986","name":"Cyberpunk","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"864a148c-2058-4b54-a2ba-90f6a5a25957","name":"Da Vinci","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"6c9f9e28-0fe7-4a02-9fef-4fccd96c65e9","name":"Happy Future","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"dea40841-305c-4901-a956-24fb498f8ea2","name":"Magical Fairy","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"c1db89ca-0a4e-4e4a-850b-8e42abab8d78","name":"Marble Statue","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"77610b42-cb14-4b4f-85e3-a953d754950b","name":"Matisse","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"e191c6aa-bfe0-48f4-b85d-b0c66d3d0c54","name":"Reptile","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"634af975-df96-4316-a0c3-ad02abd2fb2c","name":"Retro Anime","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"a2755f92-e891-48e1-b391-896676da73ce","name":"Stoner","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"b4deb512-ce0e-404e-b1ef-5e86b2048b41","name":"trippy ornate","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103},{"id":"fa74f4d8-2ed3-43d1-965c-9b086ff31ea2","name":"Van Gogh","description":"","prompt":"","ddim_steps":30,"scale":7.5,"strength":0.5,"is_premium":true,"creation_time":1672250103}]'
#   request_data = json.loads(json_str)
#   filters = [data.Filter.from_dict(f) for f in request_data]
#   assert filters[0].examples
#   assert len(filters[0].examples) > 0

def test_image_data():
  json_str = '''
 {"id":"c46c71b6fd1f410188f6a8b7568330fe","prompt":"Anime visual","seed":57567,"size":{"width":512,"height":512},"source_image_id":"c852ed7c-3e71-4953-83ee-c5f4af7f9d50.png","job_id":"1cf11bea-85fc-4d6b-9e2e-29f1b5a80553","uri":"https://storage.googleapis.com/tensorcraft1/1cf11bea-85fc-4d6b-9e2e-29f1b5a80553/c46c71b6fd1f410188f6a8b7568330fe.png","creation_time":12344}
  '''
  request_data = json.loads(json_str)
  f = data.ImageData.from_dict(request_data)
  assert f !=None
  assert f.id=="c46c71b6fd1f410188f6a8b7568330fe"

def test_filter_example():
  json_str = '''
 {"filter_id":"2278601d-1bf9-40fd-95c5-ea9bbc82761a","strength":1.0,"image_data":{"id":"c46c71b6fd1f410188f6a8b7568330fe","prompt":"Anime visual,  by yoh yoshinari, katsura masakazu, dramatic lighting, dynamic pose, dynamic perspective, strong silhouette, ilya kuvshinov, anime cels, 1 8 mm lens, fstop of 8, rounded eyes, moody, detailed facial features","seed":57567,"size":{"width":512,"height":512},"source_image_id":"c852ed7c-3e71-4953-83ee-c5f4af7f9d50.png","job_id":"1cf11bea-85fc-4d6b-9e2e-29f1b5a80553","uri":"https://storage.googleapis.com/tensorcraft1/1cf11bea-85fc-4d6b-9e2e-29f1b5a80553/c46c71b6fd1f410188f6a8b7568330fe.png","creation_time":11111},"tags":["male","teen","face"]}
  '''
  request_data = json.loads(json_str,)
  f = data.FilterExample.from_dict(request_data)
  assert f !=None
  assert f.filter_id=="2278601d-1bf9-40fd-95c5-ea9bbc82761a"
