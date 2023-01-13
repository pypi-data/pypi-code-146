import yiflow as yf
 
 
class AlgorithmInterface(yf.Interface):

    def __init__(self, config_file=None, **kwargs):
        super().__init__(config_file, **kwargs)

    # 必须实现该方法
    def __call__(self, req):
        image_name = req['imageName']
        image_data = req['imageData']

        feed_dict = dict(
            image=image_data
        )

        self.run(feed_dict)

        # construct response
        resp = {}
        resp['image_path'] = image_name
        resp['alarm'] = feed_dict['alarm']
        if 'drawed' in feed_dict:
            resp['drawed'] = feed_dict['drawed']

        return resp